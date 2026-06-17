"""Simple agentic workflow for content planning and refinement.

In this prototype, "agentic" does not mean a complex autonomous system. It
means the task is split into multiple role-based steps: planning, writing,
reviewing, and refining. Each step has its own prompt, its own output, and a
clear purpose. This makes the workflow easier to compare against the baseline,
where a single prompt directly asks for the final answer.
"""

import re

from utils import OUTPUT_DIR, call_llm, call_mock_llm, write_text


SYSTEM_PROMPT = (
    "You are a careful content planning assistant in a bachelor thesis "
    "prototype. Complete only the assigned workflow step and return markdown."
)

_ACTIVE_MODEL = "gpt-5.4-mini"


def planner_agent(topic):
    """Create a structured content plan before any draft is written."""
    # Agentic step 1: the model first reasons about the content structure.
    # This separates planning from writing, unlike the one-shot baseline.
    user_prompt = f"""
Create a structured content plan for the following topic:

{topic}

Return the plan in markdown with exactly these sections:

## Purpose
## Target Audience
## Main Sections
## Logical Order
""".strip()

    plan = call_llm(SYSTEM_PROMPT, user_prompt, model=_ACTIVE_MODEL)
    _save_agent_output("outline", "01_plan", plan)
    return plan


def writer_agent(topic, plan):
    """Write a first draft using the plan created by the planner agent."""
    # Agentic step 2: the writer receives context from the planner. This makes
    # the workflow stateful because one step influences the next step.
    user_prompt = f"""
Write a markdown draft for this topic:

{topic}

Use this content plan:

{plan}

Return only the draft.
""".strip()

    draft = call_llm(SYSTEM_PROMPT, user_prompt, model=_ACTIVE_MODEL)
    _save_agent_output("outline", "02_draft", draft)
    return draft


def reviewer_agent(draft):
    """Review a draft and suggest improvements using fixed criteria."""
    # Agentic step 3: the reviewer evaluates the draft before final refinement.
    # The criteria make the review more systematic and screenshot-friendly.
    user_prompt = f"""
Review the following draft:

{draft}

Use these criteria:
- coherence
- structure quality
- clarity
- controllability
- consistency
- usefulness

Return the review in markdown with exactly these sections:

## Strengths
## Weaknesses
## Improvement Suggestions
""".strip()

    review = call_llm(SYSTEM_PROMPT, user_prompt, model=_ACTIVE_MODEL)
    _save_agent_output("shared", "03_review", review)
    return review


def refiner_agent(draft, review):
    """Improve a draft based on the reviewer agent's feedback."""
    # Agentic step 4: the refiner uses feedback from the reviewer. This gives
    # the workflow a simple self-improvement loop.
    user_prompt = f"""
Improve the draft using the review feedback.

Draft:
{draft}

Review:
{review}

Return only the improved markdown version.
""".strip()

    refined = call_llm(SYSTEM_PROMPT, user_prompt, model=_ACTIVE_MODEL)
    _save_agent_output("shared", "04_refined", refined)
    return refined


def run_agentic_outline_workflow(topic):
    """Run planner -> writer -> reviewer -> refiner for a new outline."""
    plan = planner_agent(topic)
    draft = writer_agent(topic, plan)
    review = reviewer_agent(draft)
    refined = refiner_agent(draft, review)

    _save_agent_output("outline", "03_review", review)
    _save_agent_output("outline", "04_refined", refined)
    _save_agent_output("outline", "05_final", refined)
    return {
        "plan": plan,
        "draft": draft,
        "review": review,
        "refined": refined,
    }


def run_agentic_refinement_workflow(draft):
    """Run reviewer -> refiner for an existing draft."""
    review = reviewer_agent(draft)
    refined = refiner_agent(draft, review)

    _save_agent_output("refinement", "01_review", review)
    _save_agent_output("refinement", "02_refined", refined)
    return {
        "review": review,
        "refined": refined,
    }


def run_agentic_workflow(scenario, model, mock=False):
    """Compatibility wrapper used by main.py for the two existing scenarios."""
    global _ACTIVE_MODEL
    _ACTIVE_MODEL = model
    topic = scenario["topic"]

    if mock:
        return _run_mock_agentic_workflow(topic)

    if scenario["id"] == "scenario_1":
        result = run_agentic_outline_workflow(topic)
        return {
            "approach": "agentic_workflow",
            "plan": result["plan"],
            "draft": result["draft"],
            "critique": result["review"],
            "final_output": result["refined"],
        }

    draft = scenario.get("draft", "")
    result = run_agentic_refinement_workflow(draft)
    return {
        "approach": "agentic_workflow",
        "plan": "Existing draft provided, so no planner step was used.",
        "draft": draft,
        "critique": result["review"],
        "final_output": result["refined"],
    }


def _save_agent_output(workflow_name, step_name, content):
    """Save intermediate agent outputs for thesis screenshots."""
    safe_workflow = _safe_filename(workflow_name)
    safe_step = _safe_filename(step_name)
    path = OUTPUT_DIR / f"agentic_{safe_workflow}_{safe_step}.md"
    write_text(path, content)


def _safe_filename(value):
    """Convert a label to a simple filename component."""
    return re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_").lower()


def _run_mock_agentic_workflow(topic):
    """Keep the offline demo mode working without calling the OpenAI API."""
    plan = call_mock_llm(topic, mock_label="plan")
    draft = call_mock_llm(topic, mock_label="draft")
    review = call_mock_llm(draft, mock_label="critique")
    refined = call_mock_llm(topic, mock_label="final")

    _save_agent_output("mock", "01_plan", plan)
    _save_agent_output("mock", "02_draft", draft)
    _save_agent_output("mock", "03_review", review)
    _save_agent_output("mock", "04_refined", refined)

    return {
        "approach": "agentic_workflow",
        "plan": plan,
        "draft": draft,
        "critique": review,
        "final_output": refined,
    }
