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
Make sure python is installed in the system
using a vitual python environment is recomended
python 3.12 recomended
1. Install Ollama and run `ollama pull llama3.2:3b`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
