"""Utility functions shared across the prototype."""

from pathlib import Path
import os
import textwrap

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


DEFAULT_MODEL = "gpt-5.4-mini"
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def setup_environment():
    """Load .env values and make sure the outputs directory exists."""
    load_dotenv()
    OUTPUT_DIR.mkdir(exist_ok=True)


def get_model(cli_model=None):
    """Choose a model from CLI, environment, or a beginner-friendly default."""
    return cli_model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def get_openai_client():
    """Create an OpenAI client using OPENAI_API_KEY from the environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key, "
            "or run with --mock for the offline teaching demo."
        )
    return OpenAI(api_key=api_key)


def call_llm(system_prompt, user_prompt, model="gpt-5.4-mini"):
    """Call an OpenAI model and return the generated text.

    The function is intentionally small because this project is a bachelor
    thesis prototype. It keeps all OpenAI-specific code in one place, so the
    baseline and agentic workflow files can focus on the experiment design.
    """
    # Load variables from .env, if the user created one from .env.example.
    load_dotenv()

    # Read the API key from the environment. The key is never hardcoded.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    try:
        # Create the OpenAI client using the official Python SDK.
        client = OpenAI(api_key=api_key)

        # Send the system/developer instruction and the user task to the model.
        response = client.responses.create(
            model=model,
            instructions=system_prompt,
            input=user_prompt,
        )

        # output_text is the SDK's convenience field for plain text responses.
        return response.output_text

    except OpenAIError as error:
        # Convert SDK errors into a readable message for terminal users.
        raise RuntimeError(f"OpenAI API request failed: {error}") from error


def call_mock_llm(prompt, mock_label="output"):
    """Return deterministic demo text without calling the OpenAI API."""
    return mock_response(prompt, mock_label)


def write_text(path, content):
    """Write markdown or text content with a final newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def clean_for_metric(text):
    """Normalize text for simple word-count based evaluation."""
    return " ".join(text.lower().split())


def mock_response(prompt, label):
    """Small deterministic substitute used only for demos without an API key."""
    prompt_lower = prompt.lower()
    academic_topic = "benefits and limitations of ai-assisted academic writing"
    academic_draft = "ai tools are useful for writing"

    if label == "critique":
        return textwrap.dedent(
            """
            ## Strengths
            - The draft is understandable and relevant to the target audience.
            - It has a practical direction and avoids technical language.

            ## Weaknesses
            - The advice is still broad and needs more concrete steps.
            - The audience benefit should be stated earlier.

            ## Specific revision instructions
            - Add a simple workflow.
            - Include one ethical or practical caution.
            - End with a clear action step.
            """
        ).strip()

    if label == "plan":
        if academic_topic in prompt_lower:
            return textwrap.dedent(
                """
                ## Purpose
                - Explain how AI-assisted academic writing can support students while also creating risks.

                ## Target Audience
                - University students and instructors evaluating responsible AI use in academic work.

                ## Main Sections
                - Introduction to AI-assisted writing
                - Benefits for planning, drafting, and revision
                - Limitations related to accuracy, dependence, and integrity
                - Responsible use recommendations

                ## Logical Order
                - Start with a definition, then discuss benefits, then limitations, and end with responsible-use guidance.
                """
            ).strip()

        return textwrap.dedent(
            """
            ## Audience Needs
            - Clear examples instead of abstract claims.
            - Guidance that saves time without ignoring responsibility.

            ## Content Angle
            - Present AI as a planning assistant, not a replacement for judgment.

            ## Suggested Structure
            - Hook
            - Three-step workflow
            - Risk or limitation
            - Practical next step

            ## Risks or Limitations
            - Avoid implying that AI output is automatically accurate.
            - Remind readers to adapt content to their own context.
            """
        ).strip()

    if label == "final" and academic_topic in prompt_lower:
        return textwrap.dedent(
            """
            # Benefits and Limitations of AI-Assisted Academic Writing

            ## 1. Introduction
            - Define AI-assisted academic writing as the use of tools for brainstorming, drafting support, language improvement, and revision.
            - Present the central argument: AI can support learning, but it requires critical human control.

            ## 2. Benefits
            - AI tools can help students generate ideas and organize early outlines.
            - They can improve clarity by suggesting alternative wording.
            - They can support revision by identifying unclear passages.

            ## 3. Limitations
            - AI output may include inaccurate claims or weak reasoning.
            - Overreliance can reduce independent thinking and writing practice.
            - Academic integrity rules may limit how AI tools can be used.

            ## 4. Responsible Use
            - Students should verify claims, adapt suggestions, and keep ownership of the argument.
            - AI should be treated as a support tool rather than a substitute author.

            ## 5. Conclusion
            - AI-assisted writing is useful when it improves process and reflection, but risky when it replaces judgment.
            """
        ).strip()

    if label == "final" and academic_draft in prompt_lower:
        return (
            "AI tools can support academic writing by helping students develop "
            "ideas, organize content, and revise language more efficiently. "
            "However, their output is not automatically accurate or appropriate, "
            "so students must check facts, improve weak reasoning, and make sure "
            "the final text reflects their own understanding. Therefore, AI "
            "should be used as a supportive writing aid rather than as a complete "
            "replacement for independent academic work."
        )

    if label == "draft" and academic_topic in prompt_lower:
        return textwrap.dedent(
            """
            # Benefits and Limitations of AI-Assisted Academic Writing

            ## Introduction
            AI-assisted academic writing can help students plan, draft, and revise their work.

            ## Benefits
            - It can support brainstorming and outline creation.
            - It can suggest clearer wording.
            - It can help students notice gaps in structure.

            ## Limitations
            - The output may contain errors.
            - Students may become too dependent on the tool.
            - Course rules may restrict acceptable use.

            ## Conclusion
            AI tools are useful when students remain responsible for checking and improving the final text.
            """
        ).strip()

    if academic_topic in prompt_lower:
        return textwrap.dedent(
            """
            # Benefits and Limitations of AI-Assisted Academic Writing

            ## Introduction
            - Define AI-assisted academic writing.
            - Explain why students increasingly use these tools.

            ## Benefits
            - Brainstorming ideas
            - Structuring an argument
            - Improving clarity and grammar

            ## Limitations
            - Possible factual errors
            - Risk of overdependence
            - Academic integrity concerns

            ## Responsible Use
            - Verify claims.
            - Revise in your own voice.
            - Follow course guidelines.
            """
        ).strip()

    if academic_draft in prompt_lower:
        return (
            "AI tools can be useful in academic writing because they help students "
            "generate ideas, organize content, and revise text more efficiently. "
            "Nevertheless, AI-generated output is not always accurate, complete, "
            "or suitable for academic expectations. Students should therefore "
            "check the content carefully and avoid depending on AI as a substitute "
            "for their own reasoning and writing skills."
        )

    if label == "final" and "responsible use of ai writing assistants" in prompt_lower:
        return textwrap.dedent(
            """
            # Responsible Use of AI Writing Assistants

            ## 1. Why Students Use AI Tools
            - First-year university students can brainstorm possible essay topics before choosing one.
            - Ask for a simpler explanation of a difficult reading.
            - Get feedback on whether a paragraph is clear and logically ordered.

            ## 2. Where Responsible Use Matters
            - Course rules may differ, so check the assignment instructions first.
            - AI-generated facts, sources, and quotations must be verified.
            - Submitting generated text as your own work can create academic integrity problems.

            ## 3. Practical Habits
            - Use AI to support your process, not to replace your thinking.
            - Start with your own notes or draft before asking for suggestions.
            - Keep a short record of what you asked and how you used the response.

            ## 4. Next Step
            - Bring one assignment question to the learning center and discuss how AI can be used responsibly in that specific course.
            """
        ).strip()

    if label == "final":
        return textwrap.dedent(
            """
            For small business owners, planning social posts every month can feel like starting from zero. AI can make that first step easier.

            Try this workflow for your next content calendar:

            1. List four customer questions you hear often.
            2. Turn each question into one weekly theme.
            3. Ask an AI tool for three post ideas per theme.
            4. Rewrite the best ideas in your own brand voice.
            5. Check facts, prices, dates, and offers before scheduling.

            The opportunity is speed. The limitation is judgment: AI can draft options, but you still know your customers, promises, and standards best.

            For your next calendar, test this process for one month and compare it with your usual planning routine.
            """
        ).strip()

    if "responsible use of ai writing assistants" in prompt_lower:
        return textwrap.dedent(
            """
            # Responsible Use of AI Writing Assistants

            ## 1. Why Students Use AI Tools
            - Brainstorming topics
            - Explaining difficult readings
            - Checking structure and clarity

            ## 2. Where the Risks Begin
            - Submitting generated text as your own work
            - Depending on inaccurate or invented information
            - Losing your own academic voice

            ## 3. Practical Habits
            - Ask for explanations, not finished answers
            - Keep notes about how AI supported your process
            - Check course rules before using any tool

            ## 4. Call to Action
            - Bring one assignment question to the learning center and discuss how to use AI responsibly.
            """
        ).strip()

    return textwrap.dedent(
        """
        AI can help small businesses plan a monthly content calendar without turning every post into generic filler.

        Start by listing four customer questions you hear often. Turn each question into one weekly theme, then ask an AI tool for draft post ideas, captions, and simple variations. Review every suggestion for accuracy, tone, and fit with your actual offers before scheduling anything.

        A useful rule: let AI speed up the first draft, but keep strategy, facts, and final approval human.
        """
    ).strip()
