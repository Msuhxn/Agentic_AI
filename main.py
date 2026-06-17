"""Terminal runner for the thesis prototype.

The program compares two approaches:
1. Conventional prompt-based generation.
2. A simple agentic workflow with multiple role-based steps.
"""

import argparse

from agents import (
    run_agentic_outline_workflow,
    run_agentic_refinement_workflow,
)
from baseline import generate_outline_baseline, refine_draft_baseline
from evaluator import (
    build_evaluation_rows,
    print_evaluation_table,
    save_evaluation_csv,
)
from utils import OUTPUT_DIR, call_mock_llm, setup_environment, write_text


SCENARIO_1_TOPIC = "Benefits and limitations of AI-assisted academic writing"

SCENARIO_2_DRAFT = (
    "AI tools are useful for writing. They can help students make content faster. "
    "But sometimes the output is not perfect and needs checking. People should "
    "not fully depend on AI."
)


def run(live=False):
    """Run both thesis scenarios from the terminal."""
    setup_environment()
    all_evaluation_rows = []
    mock = not live

    scenario_1 = run_scenario_1(mock=mock)
    all_evaluation_rows.extend(
        build_evaluation_rows(
            baseline_output=scenario_1["baseline_output"],
            agentic_output=scenario_1["agentic_output"],
            scenario_name="Scenario 1 - Structured outline",
        )
    )
    print_section("SCENARIO 1 - EVALUATION")
    print_evaluation_table(all_evaluation_rows[-10:])

    scenario_2 = run_scenario_2(mock=mock)
    all_evaluation_rows.extend(
        build_evaluation_rows(
            baseline_output=scenario_2["baseline_output"],
            agentic_output=scenario_2["agentic_output"],
            scenario_name="Scenario 2 - Draft refinement",
        )
    )
    print_section("SCENARIO 2 - EVALUATION")
    print_evaluation_table(all_evaluation_rows[-10:])

    save_evaluation_csv(all_evaluation_rows, OUTPUT_DIR / "evaluation_results.csv")
    print(f"\nAll final evidence files saved in: {OUTPUT_DIR}")


def run_scenario_1(mock=False):
    """Scenario 1: generate a structured outline from a topic."""
    topic = SCENARIO_1_TOPIC

    if mock:
        baseline_output = call_mock_llm(topic, mock_label="baseline")
        agentic_result = mock_agentic_outline_result(topic)
    else:
        baseline_output = generate_outline_baseline(topic)
        agentic_result = run_agentic_outline_workflow(topic)

    agentic_output = agentic_result["refined"]

    print_section("SCENARIO 1 - BASELINE OUTPUT")
    print(baseline_output)
    print_section("SCENARIO 1 - AGENTIC WORKFLOW OUTPUT")
    print_agentic_outline_result(agentic_result)

    save_outline_evidence(baseline_output, agentic_result)

    return {
        "baseline_output": baseline_output,
        "agentic_output": agentic_output,
    }


def run_scenario_2(mock=False):
    """Scenario 2: refine an existing draft into an academic paragraph."""
    draft = SCENARIO_2_DRAFT

    if mock:
        baseline_output = call_mock_llm(draft, mock_label="baseline")
        agentic_result = mock_agentic_refinement_result(draft)
    else:
        baseline_output = refine_draft_baseline(draft)
        agentic_result = run_agentic_refinement_workflow(draft)

    agentic_output = agentic_result["refined"]

    print_section("SCENARIO 2 - BASELINE OUTPUT")
    print(baseline_output)
    print_section("SCENARIO 2 - AGENTIC WORKFLOW OUTPUT")
    print_agentic_refinement_result(agentic_result)

    save_refinement_evidence(baseline_output, agentic_result)

    return {
        "baseline_output": baseline_output,
        "agentic_output": agentic_output,
    }


def save_outline_evidence(baseline_output, agentic_result):
    """Save Scenario 1 outputs as clean markdown evidence files."""
    write_text(OUTPUT_DIR / "baseline_outline_output.md", baseline_output)
    write_text(OUTPUT_DIR / "agentic_outline_01_plan.md", agentic_result["plan"])
    write_text(OUTPUT_DIR / "agentic_outline_02_draft.md", agentic_result["draft"])
    write_text(OUTPUT_DIR / "agentic_outline_03_review.md", agentic_result["review"])
    write_text(OUTPUT_DIR / "agentic_outline_04_refined.md", agentic_result["refined"])


def save_refinement_evidence(baseline_output, agentic_result):
    """Save Scenario 2 outputs as clean markdown evidence files."""
    write_text(OUTPUT_DIR / "baseline_refinement_output.md", baseline_output)
    write_text(OUTPUT_DIR / "agentic_refinement_01_review.md", agentic_result["review"])
    write_text(OUTPUT_DIR / "agentic_refinement_02_refined.md", agentic_result["refined"])


def print_agentic_outline_result(result):
    """Print all outline workflow steps for screenshot-friendly terminal output."""
    print("Planner Agent:\n")
    print(result["plan"])
    print("\nWriter Agent:\n")
    print(result["draft"])
    print("\nReviewer Agent:\n")
    print(result["review"])
    print("\nRefiner Agent:\n")
    print(result["refined"])


def print_agentic_refinement_result(result):
    """Print refinement workflow steps for screenshot-friendly terminal output."""
    print("Reviewer Agent:\n")
    print(result["review"])
    print("\nRefiner Agent:\n")
    print(result["refined"])


def mock_agentic_outline_result(topic):
    """Create deterministic mock outputs for Scenario 1."""
    plan = call_mock_llm(topic, mock_label="plan")
    draft = call_mock_llm(topic, mock_label="draft")
    review = call_mock_llm(draft, mock_label="critique")
    refined = call_mock_llm(topic, mock_label="final")
    return {
        "plan": plan,
        "draft": draft,
        "review": review,
        "refined": refined,
    }


def mock_agentic_refinement_result(draft):
    """Create deterministic mock outputs for Scenario 2."""
    review = call_mock_llm(draft, mock_label="critique")
    refined = call_mock_llm(draft, mock_label="final")
    return {
        "review": review,
        "refined": refined,
    }


def print_section(title):
    """Print a clear heading for screenshots and terminal logs."""
    print(f"\n{'=' * len(title)}")
    print(title)
    print(f"{'=' * len(title)}\n")


def parse_args():
    """Parse optional terminal arguments."""
    parser = argparse.ArgumentParser(
        description="Run the agentic content planner thesis prototype."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use the OpenAI API instead of deterministic local sample outputs.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(live=args.live)
