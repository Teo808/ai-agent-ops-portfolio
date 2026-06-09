from dataclasses import dataclass


@dataclass
class Scenario:
    title: str
    symptoms: list[str]
    environment: list[str]


CHECKS = {
    "memory_scope": [
        "Confirm the active project/container scope.",
        "Run the same recall query with and without profile context.",
        "Check whether stale global memories are outranking project memories.",
        "Verify the final answer cites the project-specific source.",
    ],
    "tool_config": [
        "List available tools and confirm the expected tool name is present.",
        "Check auth state without printing secrets.",
        "Verify config paths and transport type.",
        "Run a minimal tool call and capture the exact error.",
    ],
    "browser_workflow": [
        "Confirm the target page loads in a normal browser.",
        "Capture the accessibility tree or screenshot at the failure point.",
        "Check for login, CAPTCHA, dynamic selectors, or blocked popups.",
        "Retry with a slower step-by-step navigation path.",
    ],
    "provider_routing": [
        "Confirm the selected model/provider is available.",
        "Run a minimal prompt against the provider.",
        "Check OpenAI-compatible base URL and model name formatting.",
        "Compare behavior against a known working fallback provider.",
    ],
}


def classify(scenario: Scenario) -> str:
    text = " ".join([scenario.title, *scenario.symptoms, *scenario.environment]).lower()

    if any(term in text for term in ["memory", "recall", "project", "stale"]):
        return "memory_scope"
    if any(term in text for term in ["mcp", "tool", "auth", "config", "transport"]):
        return "tool_config"
    if any(term in text for term in ["browser", "page", "form", "selector", "captcha"]):
        return "browser_workflow"
    if any(term in text for term in ["provider", "model", "openrouter", "portal", "endpoint"]):
        return "provider_routing"

    return "tool_config"


def priority_for(category: str) -> str:
    if category in {"memory_scope", "tool_config"}:
        return "high"
    return "medium"


def build_report(scenario: Scenario) -> str:
    category = classify(scenario)
    checks = CHECKS[category]
    priority = priority_for(category)

    lines = [
        f"Scenario: {scenario.title}",
        f"Likely category: {category}",
        f"Priority: {priority}",
        "",
        "Symptoms:",
        *[f"- {symptom}" for symptom in scenario.symptoms],
        "",
        "Environment:",
        *[f"- {item}" for item in scenario.environment],
        "",
        "Recommended checks:",
        *[f"- {check}" for check in checks],
        "",
        "Operator report:",
        (
            "The issue appears actionable through deployment/support checks. "
            "Start by reproducing the symptom, then run the smallest verification "
            "step that separates configuration, memory scope, browser workflow, "
            "and provider routing problems."
        ),
    ]
    return "\n".join(lines)


def main() -> None:
    scenario = Scenario(
        title="Hermes Agent cannot recall project-specific setup notes after a tool config change.",
        symptoms=[
            "Recall returns broad personal history instead of the current project.",
            "The user asks for a setup fix and receives unrelated memories.",
            "A recent MCP/provider configuration change may have affected routing.",
        ],
        environment=[
            "Windows PowerShell",
            "Hermes-style agent",
            "Supermemory-style project memory",
            "MCP/tool integrations",
        ],
    )

    print(build_report(scenario))


if __name__ == "__main__":
    main()

