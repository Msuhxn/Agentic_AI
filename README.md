# Agentic AI for Automated Content Planning and Generation

This repository contains the Python prototype for the Bachelor thesis:

**Agentic AI for Automated Content Planning and Generation: A Lightweight Evaluation of Opportunities and Limitations**

The code is a small terminal-based prototype. It compares conventional prompt-based generation with a simple multi-step agentic workflow for two synthetic content-generation scenarios.

This is not a production system. It is a bachelor-level prototype for demonstrating workflow structure, output transparency, and qualitative evaluation.

## Thesis Purpose

The practical part of the thesis examines whether a lightweight agentic workflow can make content generation more transparent and controllable than a single direct prompt.

The prototype supports the thesis by showing:

- how a baseline prompt produces content in one step
- how an agentic workflow separates planning, drafting, reviewing, and refining
- how outputs can be compared using compact qualitative criteria

## Research Relevance

Recent language-model applications increasingly move from one-step prompting toward multi-step workflows. This project gives a small practical example of that difference. The focus is not model performance at scale, but whether the workflow structure itself provides useful advantages for simple academic content-planning tasks.

## Project Structure

```text
agentic-content-planner/
├── main.py
├── agents.py
├── baseline.py
├── evaluator.py
├── prompts.py
├── utils.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── notebooks/
│   └── agentic_content_workflow_demo.ipynb
└── outputs/
    ├── agentic_outline_01_plan.md
    ├── agentic_outline_02_draft.md
    ├── agentic_outline_03_review.md
    ├── agentic_outline_04_refined.md
    ├── agentic_refinement_01_review.md
    ├── agentic_refinement_02_refined.md
    ├── baseline_outline_output.md
    ├── baseline_refinement_output.md
    └── evaluation_results.csv
```

## Baseline and Agentic Workflow

The baseline method is implemented in `baseline.py`. It sends one direct prompt to the model and uses the response as the final output.

The agentic workflow is implemented in `agents.py`. It breaks the task into smaller stages:

- `planner_agent()` creates a content plan
- `writer_agent()` creates a draft from the plan
- `reviewer_agent()` evaluates the draft
- `refiner_agent()` improves the draft using the review

This separation makes the intermediate reasoning steps visible for comparison and thesis screenshots.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## OpenAI API Key

The API key must be stored as an environment variable. It must not be hardcoded in the Python files.

Copy the example file:

```bash
cp .env.example .env
```

Add the API key to `.env`:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.4-mini
```

The `.env` file is ignored by Git.

## Running the Project

Run the screenshot-safe local version:

```bash
python3 main.py
```

This uses deterministic local example outputs and does not require an API key.

Run the live OpenAI API version:

```bash
python3 main.py --live
```

The live version requires `OPENAI_API_KEY` to be set in the environment or in `.env`.

## Scenario 1

Task: Generate a structured outline.

Topic:

```text
Benefits and limitations of AI-assisted academic writing
```

The baseline produces the outline directly from one prompt. The agentic workflow first creates a plan, then a draft, then a review, and finally a refined outline.

## Scenario 2

Task: Refine a short draft into a more organized academic paragraph.

Input draft:

```text
AI tools are useful for writing. They can help students make content faster. But sometimes the output is not perfect and needs checking. People should not fully depend on AI.
```

The baseline refines the draft in one prompt. The agentic workflow reviews the draft first and then refines it based on the review.

## Evaluation

The qualitative evaluation is implemented in `evaluator.py`. It compares baseline and agentic outputs using five criteria:

- Coherence
- Structure quality
- Controllability
- Consistency
- Practical usefulness

Scores range from 1 to 5. Each score includes a short justification. The results are saved in:

```text
outputs/evaluation_results.csv
```

The evaluation is compact and qualitative. It is intended for bachelor-level analysis, not as a large benchmark.

## Ethical Note

The prototype uses only synthetic, non-sensitive example text. It does not process personal data, private documents, or confidential academic work. API keys and account information must not be included in screenshots or submitted files.
