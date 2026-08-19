#!/usr/bin/env python
"""Small Hermes run triage CLI.

Reads a JSONL export or plain text log and writes a Markdown report.
I use it to catch the kinds of things that make real Hermes runs messy:
stale browser refs, tool failures, retry loops, and missing verification.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Any


SIGNALS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "stale_browser_ref",
        re.compile(r"ref [\w-]+ not found|stale element|current page snapshot|recaptur|fresh snapshot", re.I),
        "The browser ref went stale. Take a fresh snapshot, find the target again, then retry once.",
    ),
    (
        "tool_error",
        re.compile(r"\berror\b|exception|traceback|failed|isError", re.I),
        "A tool returned an error. Pull out the smallest repro instead of burying it in the full run.",
    ),
    (
        "timeout",
        re.compile(r"timeout|timed out|exceeded .* seconds|deadline", re.I),
        "A call timed out. Record the tool name, duration, and whether a retry worked.",
    ),
    (
        "auth_or_permission",
        re.compile(r"unauthorized|forbidden|permission|login|oauth|token|credential|401|403", re.I),
        "This looks like auth or permissions. Do not expose secrets. Record only where it failed.",
    ),
    (
        "rate_limit",
        re.compile(r"rate.?limit|429|too many requests|quota", re.I),
        "This looks like a rate limit or quota issue. Add backoff or use a cheaper check.",
    ),
    (
        "redaction_risk",
        re.compile(r"api[_-]?key|secret|password|bearer |credential|token=|sk-[A-Za-z0-9]", re.I),
        "This may contain a secret. Redact it before sharing anything.",
    ),
    (
        "verification",
        re.compile(r"verified|confirmed|landed|sent|exit_code.?[:=]?\s*0|passed|success", re.I),
        "This is useful proof. Keep the exact evidence line in the report.",
    ),
]

TOOL_PATTERNS = [
    re.compile(r"mcp__[\w-]+__[\w-]+"),
    re.compile(r"functions\.[\w-]+"),
    re.compile(r"\b(browser_[\w-]+|terminal|read_file|write_file|patch|web_search|web_extract)\b"),
]


@dataclass
class Finding:
    line_no: int
    category: str
    text: str
    recommendation: str


def _json_to_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts: list[str] = []
        for key in ("role", "name", "content", "result", "error", "message", "output"):
            if key in value:
                parts.append(_json_to_text(value[key]))
        if parts:
            return " | ".join(p for p in parts if p)
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, list):
        return "\n".join(_json_to_text(item) for item in value)
    return str(value)


def load_lines(path: Path) -> list[str]:
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    extracted: list[str] = []
    for raw in raw_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        try:
            extracted.append(_json_to_text(json.loads(stripped)))
        except json.JSONDecodeError:
            extracted.append(stripped)
    return extracted


def detect_tools(text: str) -> list[str]:
    tools: list[str] = []
    for pattern in TOOL_PATTERNS:
        tools.extend(match.group(0) for match in pattern.finditer(text))
    return tools


def analyze_lines(lines: Iterable[str]) -> dict[str, Any]:
    findings: list[Finding] = []
    category_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    repeated_tool_windows: dict[str, int] = defaultdict(int)

    previous_tool: str | None = None
    repeat_count = 0

    for idx, text in enumerate(lines, start=1):
        clean = " ".join(text.split())
        if not clean:
            continue

        for tool in detect_tools(clean):
            tool_counts[tool] += 1
            if tool == previous_tool:
                repeat_count += 1
            else:
                if previous_tool and repeat_count >= 3:
                    repeated_tool_windows[previous_tool] += repeat_count
                previous_tool = tool
                repeat_count = 1

        for category, pattern, recommendation in SIGNALS:
            if pattern.search(clean):
                category_counts[category] += 1
                findings.append(Finding(idx, category, clean[:280], recommendation))
                break

    if previous_tool and repeat_count >= 3:
        repeated_tool_windows[previous_tool] += repeat_count

    return {
        "line_count": len(list(lines)) if not isinstance(lines, list) else len(lines),
        "findings": findings,
        "category_counts": category_counts,
        "tool_counts": tool_counts,
        "repeated_tool_windows": dict(repeated_tool_windows),
    }


def risk_level(category_counts: Counter[str], repeated_tool_windows: dict[str, int]) -> str:
    hard_failures = sum(category_counts[c] for c in ("tool_error", "timeout", "auth_or_permission"))
    if category_counts["redaction_risk"]:
        return "high"
    if hard_failures >= 3 or repeated_tool_windows:
        return "medium"
    if hard_failures or category_counts["stale_browser_ref"]:
        return "low"
    return "clean"


def render_markdown(title: str, source: Path, analysis: dict[str, Any]) -> str:
    findings: list[Finding] = analysis["findings"]
    category_counts: Counter[str] = analysis["category_counts"]
    tool_counts: Counter[str] = analysis["tool_counts"]
    repeated_tool_windows: dict[str, int] = analysis["repeated_tool_windows"]
    level = risk_level(category_counts, repeated_tool_windows)

    out: list[str] = []
    out.append(f"# {title}")
    out.append("")
    out.append("## quick summary")
    out.append("")
    out.append(f"- Source: `{source}`")
    out.append(f"- Lines scanned: {analysis['line_count']}")
    out.append(f"- Findings: {len(findings)}")
    out.append(f"- Risk level: `{level}`")
    out.append("")

    out.append("## signals found")
    out.append("")
    if category_counts:
        for category, count in category_counts.most_common():
            out.append(f"- `{category}`: {count}")
    else:
        out.append("- No obvious failure signals found.")
    out.append("")

    out.append("## tools seen most")
    out.append("")
    if tool_counts:
        for tool, count in tool_counts.most_common(10):
            out.append(f"- `{tool}`: {count}")
    else:
        out.append("- I did not find tool names in this input.")
    out.append("")

    if repeated_tool_windows:
        out.append("## possible retry loops")
        out.append("")
        for tool, count in sorted(repeated_tool_windows.items()):
            out.append(f"- `{tool}` repeated {count} times in a row")
        out.append("")

    out.append("## findings")
    out.append("")
    if findings:
        for item in findings[:30]:
            out.append(f"### Line {item.line_no}: `{item.category}`")
            out.append("")
            out.append(f"> {item.text}")
            out.append("")
            out.append(f"What I would check: {item.recommendation}")
            out.append("")
    else:
        out.append("I did not find anything worth triaging.")
        out.append("")

    out.append("## what I would check next")
    out.append("")
    if category_counts["redaction_risk"]:
        out.append("1. Redact sensitive strings before sharing the run.")
    if category_counts["stale_browser_ref"]:
        out.append("1. Add a browser recovery path: fresh snapshot, find the target again, retry once.")
    if category_counts["tool_error"] or category_counts["timeout"]:
        out.append("1. Turn the top failure into a small repro with the tool name, inputs, expected result, actual result, and recovery result.")
    if not any(category_counts.values()):
        out.append("1. Keep this run as a clean baseline.")
    out.append("1. Attach the verified final state, not just the attempted action.")
    out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Triage Hermes session exports/logs into Markdown.")
    parser.add_argument("input", type=Path, help="JSONL transcript or plain text log")
    parser.add_argument("--title", default="Hermes Run Triage Report")
    parser.add_argument("--out", type=Path, help="Write Markdown report to this path")
    args = parser.parse_args(argv)

    lines = load_lines(args.input)
    analysis = analyze_lines(lines)
    markdown = render_markdown(args.title, args.input, analysis)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
