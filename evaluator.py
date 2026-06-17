"""Compact qualitative evaluator for the thesis prototype.

This module is not a large benchmark. It provides a small, transparent scoring
framework that can support bachelor thesis discussion about differences between
conventional prompting and a simple agentic workflow.
"""

import csv
import re

from utils import OUTPUT_DIR, clean_for_metric


CRITERIA = [
    "Coherence",
    "Structure quality",
    "Controllability",
    "Consistency",
    "Practical usefulness",
]


def evaluate_outputs(baseline_output, agentic_output, scenario_name):
    """Compare baseline and agentic outputs and save a qualitative CSV report."""
    rows = build_evaluation_rows(baseline_output, agentic_output, scenario_name)
    output_path = OUTPUT_DIR / "evaluation_results.csv"
    save_evaluation_csv(rows, output_path)
    print_evaluation_table(rows)
    return rows


def build_evaluation_rows(baseline_output, agentic_output, scenario_name):
    """Build qualitative evaluation rows without saving or printing."""
    rows = []
    for approach, output in [
        ("baseline_prompt", baseline_output),
        ("agentic_workflow", agentic_output),
    ]:
        for criterion in CRITERIA:
            score, justification = score_criterion(output, criterion, approach)
            rows.append(
                {
                    "scenario_name": scenario_name,
                    "approach": approach,
                    "criterion": criterion,
                    "score": score,
                    "justification": justification,
                }
            )
    return rows


def score_criterion(output, criterion, approach):
    """Assign a simple 1-5 score and short justification for one criterion."""
    normalized = clean_for_metric(output)
    word_count = len(normalized.split())
    heading_count = len(re.findall(r"^#{1,3}\s+", output, flags=re.MULTILINE))
    bullet_count = len(re.findall(r"(^|\n)\s*(-|\d+\.)\s+", output))

    if criterion == "Coherence":
        return score_coherence(normalized, word_count)
    if criterion == "Structure quality":
        return score_structure_quality(heading_count, bullet_count, word_count)
    if criterion == "Controllability":
        return score_controllability(approach)
    if criterion == "Consistency":
        return score_consistency(normalized)
    if criterion == "Practical usefulness":
        return score_practical_usefulness(normalized)

    return 3, "Criterion not recognized, so a neutral score was assigned."


def score_coherence(normalized, word_count):
    """Estimate whether the output reads like one connected answer."""
    linking_terms = ["therefore", "because", "also", "then", "finally", "however"]
    hits = count_hits(normalized, linking_terms)
    score = clamp_score(2 + min(hits, 2) + (1 if word_count >= 70 else 0))
    justification = (
        "The text has a connected flow and enough detail for the scenario."
        if score >= 4
        else "The text is understandable but could connect ideas more clearly."
    )
    return score, justification


def score_structure_quality(heading_count, bullet_count, word_count):
    """Estimate whether the output is easy to scan and organized."""
    score = 1
    if heading_count >= 1:
        score += 1
    if heading_count >= 3:
        score += 1
    if bullet_count >= 3:
        score += 1
    if word_count >= 60:
        score += 1
    score = clamp_score(score)
    justification = (
        "The output uses headings or lists that make the structure easy to inspect."
        if score >= 4
        else "The output has limited visible structure for comparison or screenshots."
    )
    return score, justification


def score_controllability(approach):
    """Score how visible and controllable the generation process is."""
    if approach == "agentic_workflow":
        return (
            4,
            "Planner, reviewer, and refiner stages make the process more visible.",
        )

    return (
        2,
        "One direct prompt gives few visible control points after generation starts.",
    )


def score_consistency(normalized):
    """Estimate whether the output stays on topic without obvious drift."""
    consistency_terms = ["ai", "content", "draft", "plan", "audience", "use"]
    hits = count_hits(normalized, consistency_terms)
    score = clamp_score(1 + min(hits, 4))
    justification = (
        "The output stays aligned with the content-planning task."
        if score >= 4
        else "The output is broadly relevant but may not reinforce the same focus throughout."
    )
    return score, justification


def score_practical_usefulness(normalized):
    """Estimate whether the output gives advice that can be applied."""
    useful_terms = ["try", "use", "create", "list", "check", "review", "ask", "improve"]
    hits = count_hits(normalized, useful_terms)
    score = clamp_score(1 + min(hits, 4))
    justification = (
        "The output includes concrete actions that a reader could apply."
        if score >= 4
        else "The output gives some useful direction but remains fairly general."
    )
    return score, justification


def count_hits(normalized, terms):
    """Count how many rubric terms appear in the normalized output."""
    return sum(1 for term in terms if term in normalized)


def clamp_score(value):
    """Keep all qualitative scores on a 1-5 scale."""
    return max(1, min(5, int(value)))


def save_evaluation_csv(rows, path=None):
    """Write qualitative evaluation rows to a CSV file."""
    output_path = path or OUTPUT_DIR / "evaluation_results.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "scenario_name",
        "approach",
        "criterion",
        "score",
        "justification",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_evaluation_table(rows):
    """Print a clean compact table in the terminal."""
    headers = ["Approach", "Criterion", "Score", "Justification"]
    table_rows = [
        [
            row["approach"],
            row["criterion"],
            str(row["score"]),
            row["justification"],
        ]
        for row in rows
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in table_rows))
        for index in range(len(headers))
    ]

    divider = "-+-".join("-" * width for width in widths)
    print(" | ".join(headers[index].ljust(widths[index]) for index in range(len(headers))))
    print(divider)
    for row in table_rows:
        print(" | ".join(row[index].ljust(widths[index]) for index in range(len(row))))


def compare_outputs(scenario, baseline_output, agentic_output):
    """Compatibility helper used by main.py."""
    return build_evaluation_rows(
        baseline_output=baseline_output,
        agentic_output=agentic_output,
        scenario_name=scenario["name"],
    )
