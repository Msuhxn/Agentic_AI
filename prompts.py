"""Prompt templates and synthetic scenarios for the thesis prototype."""

SCENARIOS = [
    {
        "id": "scenario_1",
        "name": "Outline generation",
        "task": "Create a content outline",
        "audience": "first-year university students",
        "topic": "responsible use of AI writing assistants in academic work",
        "channel": "university learning center blog",
        "goal": "help students understand opportunities, risks, and practical habits",
        "notes": (
            "Synthetic example only. Include study tips, ethical concerns, and a "
            "short call to action."
        ),
    },
    {
        "id": "scenario_2",
        "name": "Content refinement",
        "task": "Refine an existing short post",
        "audience": "small business owners",
        "topic": "using AI tools for a monthly social media calendar",
        "channel": "LinkedIn post",
        "goal": "make the content clearer, more concrete, and less generic",
        "draft": (
            "AI can help with content. Businesses should use it to make posts faster. "
            "It is useful for planning and saving time. Try it for your marketing."
        ),
        "notes": (
            "Synthetic example only. Keep the tone practical and include a realistic "
            "workflow."
        ),
    },
]


def baseline_prompt(scenario):
    """Create a conventional one-shot prompt for the baseline condition."""
    if scenario["id"] == "scenario_1":
        return f"""
You are a helpful content writer.

Write a clear content outline for a {scenario["channel"]}.

Audience: {scenario["audience"]}
Topic: {scenario["topic"]}
Goal: {scenario["goal"]}
Notes: {scenario["notes"]}

Return the answer as markdown with headings and bullet points.
""".strip()

    return f"""
You are a helpful content editor.

Improve the following draft for a {scenario["channel"]}.

Audience: {scenario["audience"]}
Topic: {scenario["topic"]}
Goal: {scenario["goal"]}
Notes: {scenario["notes"]}

Draft:
{scenario["draft"]}

Return only the improved post in markdown.
""".strip()


def planning_prompt(scenario):
    """Prompt used by the first agentic step: analyze and plan."""
    return f"""
You are a content strategist. Analyze the task and create a short plan before writing.

Task: {scenario["task"]}
Audience: {scenario["audience"]}
Channel: {scenario["channel"]}
Topic: {scenario["topic"]}
Goal: {scenario["goal"]}
Notes: {scenario["notes"]}

Return:
1. Audience needs
2. Content angle
3. Suggested structure
4. Risks or limitations to watch for
""".strip()


def drafting_prompt(scenario, plan):
    """Prompt used by the second agentic step: generate content from a plan."""
    draft_text = scenario.get("draft", "No existing draft. Create from scratch.")
    return f"""
You are a content writer. Use the plan to produce the content.

Plan:
{plan}

Task: {scenario["task"]}
Audience: {scenario["audience"]}
Channel: {scenario["channel"]}
Topic: {scenario["topic"]}
Goal: {scenario["goal"]}
Existing draft, if any:
{draft_text}

Return markdown content suitable for the channel.
""".strip()


def critique_prompt(scenario, draft):
    """Prompt used by the third agentic step: identify improvement points."""
    return f"""
You are a careful content reviewer. Critique the draft against the task.

Audience: {scenario["audience"]}
Channel: {scenario["channel"]}
Goal: {scenario["goal"]}
Notes: {scenario["notes"]}

Draft:
{draft}

Return a concise critique with:
- Strengths
- Weaknesses
- Specific revision instructions
""".strip()


def revision_prompt(scenario, draft, critique):
    """Prompt used by the final agentic step: revise using critique."""
    return f"""
You are a content editor. Revise the draft using the critique.

Audience: {scenario["audience"]}
Channel: {scenario["channel"]}
Goal: {scenario["goal"]}

Original draft:
{draft}

Critique:
{critique}

Return the final improved content in markdown. Do not include process notes.
""".strip()
