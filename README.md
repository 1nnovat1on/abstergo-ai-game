# Archon

Archon is a terminal-native agent loop that calls DeepSeek-R1 through Ollama Cloud, records each interaction in SQLite, and renders status panels with Rich. It initializes its own session state, snapshots local context, calls the LLM, applies any returned changes (UI state, attributes, or prompt updates), and then idles while showing a simple menu.

## Prerequisites
- Python 3.10+.
- Network access to the Ollama Cloud DeepSeek endpoint at `https://ollama.com/library/deepseek-r1:latest`.
- The `rich` Python package for terminal rendering.
- Optional: a terminal that supports the ASCII bell (or `winsound.Beep` on Windows) for the notification tone.

## Setup
1. From the repository root, create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the Python dependency:
   ```bash
   pip install rich
   ```

## Running Archon
1. From the repository root (the folder that contains the `archon/` package), start the loop:
   ```bash
   python -m archon.main
   ```
2. Archon will:
   - Create or migrate `archon.db` in the working directory.
   - Seed the schema from `archon/database/schema.sql` and back it up.
   - Build a snapshot that includes disk usage, the current `archon` attributes, UI state, and a squared "effective" complexity metric.
   - Call the LLM using `archon.cognition.llm.call_archon`, passing the system prompt in `archon/prompts/system_prompt.json` and the snapshot to the Ollama Cloud `deepseek-r1:latest` endpoint.
   - Log the interaction, render the returned thoughts, apply any proposed changes (UI state, prompt tweaks, or attribute updates), and ring a notification tone.
   - Enter the idle loop, refreshing the status panel and options every two seconds. Exit with `Ctrl+C`.

## Adjusting behavior
- **System prompt**: Edit `archon/prompts/system_prompt.json` to change the base instruction sent to the model. Updates proposed by the model will overwrite this file.
- **Complexity growth**: `archon/engine/complexity.py` increases the stored `complexity_level` once every 24 hours. You can seed a different starting value directly in the database if needed.
- **UI and attributes**: The model can return `ui_state` or `archon_attributes` keys in its response; these are persisted via SQLite and shown in the terminal panels.
- **Offline simulation**: If Ollama or the model is unavailable, you can temporarily stub `archon.cognition.llm.call_archon` to return a mock JSON object. The rest of the pipeline (logging, applying changes, rendering) will still run, which is useful for demoing the idle loop and UI updates.

See `REVIEW.txt` for a simulated thread walkthrough of the runtime pipeline.
