# Briefly: Meeting Action Tracker

Briefly turns a raw meeting transcript into a reviewable list of follow-up work. It is a small Streamlit workbench for testing how reliably an LLM can identify commitments, preserve the details people actually said, and expose uncertainty instead of quietly filling in gaps.

The app has two useful modes:

- **Extract** a set of tasks from a pasted transcript or a built-in example.
- **Evaluate** the full pipeline against labelled examples or your own reference answers.

## Why the pipeline has multiple passes

A single model response is easy to read but difficult to trust. Briefly keeps the process visible:

```text
transcript
    |
    v
normalise text -> extract structured tasks -> run deterministic checks
                                                       |
                                                       v
                                        review against the original transcript
                                                       |
                                                       v
                                            display final action items
```

The transcript remains the authority at every stage. The first model call proposes structured tasks, `validator.py` flags basic quality problems, and a second model call can correct omissions or unsupported details. The result is shown as a table with:

- the task description;
- the owner, when one is stated;
- the original deadline wording, when available;
- the current status; and
- a confidence value between 0 and 1.

## What is included

### Transcript preparation

`cleaner.py` removes empty lines, trims speaker text, and makes whitespace and speaker separators consistent. This keeps formatting noise from competing with the meeting content.

### Structured extraction

The Gemini chat model is asked for Pydantic-backed output rather than free-form prose. The extraction instructions explicitly prohibit invented people, dates, and tasks.

### Verification

The extracted list is checked against the cleaned transcript a second time. The verification pass looks for missing commitments, duplicate work, incorrect ownership, unsupported dates, and status mistakes.

### Evaluation

The evaluation screen reports precision, recall, F1, and field-level accuracy for owners, deadlines, and statuses. It also shows per-case comparisons, including true positives, false positives, and false negatives. A separate form accepts a transcript plus one pipe-delimited reference task per line.

## Repository map

```text
.
|-- main.py              Streamlit interface and pipeline orchestration
|-- cleaner.py           Transcript normalisation
|-- validator.py         Deterministic checks for extracted tasks
|-- evaluator.py         Matching and metric calculations
|-- evaluation_data.py   Example transcripts and labelled cases
|-- system_prompts.py    Extraction and verification instructions
|-- requirements.txt     Runtime dependencies
|-- pyproject.toml       Project metadata
`-- .devcontainer/       Optional development-container setup
```

## Run it locally

### Requirements

- Python 3.13 or newer
- A Google Gemini API key

Create an environment and install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then install the application packages:

```bash
pip install -r requirements.txt
```

Add a `.env` file beside `main.py`:

```env
GEMINI_API_KEY2=your_api_key_here
```

Launch Streamlit:

```bash
streamlit run main.py
```

The deployed version, when configured, should receive the same value through Streamlit Secrets instead of a committed file. Keep `.env` and API keys out of version control.

## Using the evaluation form

Each reference row uses four fields separated by `|`:

```text
Task | Owner | Deadline | Status
Refresh the release notes | Morgan | Friday | pending
Review the incident report | Casey | None | in_progress
```

Use `None` when the transcript does not give a deadline. The same cleaning, extraction, validation, and verification sequence is used for this custom run as for the bundled evaluation cases.

## Design boundaries

This project intentionally stays small and inspectable. It does not add retrieval, a vector database, fine-tuning, transcription, a task-management service, or a multi-agent runtime. Those would be natural next experiments, but keeping them out makes it easier to reason about the effect of each pipeline stage.

Possible follow-up work includes transcript file uploads, CSV/JSON export, calendar integrations, longer-context handling, and a larger labelled benchmark.

## Project note

This workspace is a personal adaptation of the public [AI Meeting action item extractor repository](https://github.com/drishti-g/AI-Meeting-action-item-extractor). The application flow is intentionally kept compatible while the documentation, naming, and presentation have been reorganised for this version.
