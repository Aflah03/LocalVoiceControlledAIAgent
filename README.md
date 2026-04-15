# Voice AI Agent
This project is a voice-enabled AI agent designed for the Mem0 Internship assignment.

## Architecture
Audio Input -> Whisper (STT) -> Llama 3.2 (Intent) -> Tool Executor -> Gradio UI

## Project Structure
- `app.py`: Main entry point (Gradio UI)
- `agent/`: Core logic for STT, Intent classification, and Execution
- `agent/tools/`: Individual tool implementations
- `output/`: Safe zone for all generated files
- `tests/`: Layer-specific tests

## Setup
Python 3.12 is recommended.

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Ollama and pull the model:**
   ```bash
   ollama pull llama3.2:3b
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app:**
   ```bash
   python app.py
   ```
