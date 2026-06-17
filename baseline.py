"""Conventional prompt-based generation for comparison.

The baseline represents the simplest approach in the thesis prototype:
one direct prompt is sent to the model and the model response is used as the
final content. This makes it easier to compare against the agentic workflow,
where planning, drafting, critique, and revision happen as separate steps.
"""

from prompts import baseline_prompt
from utils import OUTPUT_DIR, call_llm, call_mock_llm, write_text


SYSTEM_PROMPT = (
    "You are a clear, responsible content planning assistant for a thesis "
    "prototype. Follow the user's task and return concise markdown."
)


def generate_outline_baseline(topic):
    """Generate a content outline using one conventional direct prompt."""
    # This prompt is intentionally simple: no planning agent, no reviewer, and
    # no revision loop. It is the comparison point for the agentic workflow.
    user_prompt = f"""
Create a clear markdown content outline about:

{topic}

Return only the outline in markdown.
""".strip()

    # The baseline makes exactly one model call for this task.
    markdown_output = call_llm(SYSTEM_PROMPT, user_prompt)

    # Save the markdown output so it can be inspected in the thesis analysis.
    write_text(OUTPUT_DIR / "baseline_outline_output.md", markdown_output)
    return markdown_output


def refine_draft_baseline(draft):
    """Refine a draft using one conventional direct prompt."""
    # This prompt asks directly for a polished version of the draft. It does
    # not ask the model to plan, critique itself, or run multiple steps.
    user_prompt = f"""
Improve the following draft and return the revised version in markdown:

{draft}
""".strip()

    # The baseline makes exactly one model call for this task.
    markdown_output = call_llm(SYSTEM_PROMPT, user_prompt)

    # Save the markdown output so it can be compared with agentic results.
    write_text(OUTPUT_DIR / "baseline_refinement_output.md", markdown_output)
    return markdown_output


def run_baseline(scenario, model, mock=False):
    """Generate content with a single prompt and no intermediate steps."""
    prompt = baseline_prompt(scenario)
    if mock:
        output = call_mock_llm(prompt, mock_label="baseline")
    else:
        output = call_llm(SYSTEM_PROMPT, prompt, model=model)

    return {
        "approach": "baseline_prompt",
        "prompt": prompt,
        "output": output,
    }
