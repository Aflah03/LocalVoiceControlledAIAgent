# Voice AI Agent

A locally-run voice agent that transcribes speech, figures out what you want done, and executes it. Built as part of the Mem0 internship.

## What It Does

You speak a command -> it gets transcribed -> the model figures out your intent -> the right tool runs -> you get results.

**Example commands:**
- "Create a Python file called hello.py and write code to print numbers from 1 to 100"
- "Edit main.py to add a login function"
- "Summarize the text in notes.txt"
- "What's the capital of France?"

## Architecture

```
Audio Input (mic or file)
       |
       v
Whisper STT (transcription)
       |
       v
Llama 3.2 via Ollama (intent classification)
       |
       v
Tool Executor (routes to the right handler)
       |
       v
Gradio UI (shows transcription, intents, and execution log)
```

## Components

### Core Pipeline (`agent/`)
- **`stt.py`** - Speech-to-text using Faster Whisper. Handles both file transcription and live mic recording.
- **`intent.py`** - Sends transcribed text to Llama 3.2 to classify intent and extract parameters. Includes fallback parsing for malformed JSON from the model.
- **`executor.py`** - Wires everything together. Runs the full pipeline: audio -> text -> intent -> tool execution.

### Tools (`agent/tools/`)
- **`file_creator.py`** - Creates empty files in the `output/` directory.
- **`code_generator.py`** - Generates code via Ollama and writes it to a file. Handles multiple languages.
- **`file_editor.py`** - Updates existing files with new content.
- **`summarizer.py`** - Summarizes text or file contents.
- **`chat_handler.py`** - General conversation, keeps a short history for context.

### Frontend
- **`app.py`** - Gradio interface with audio input (mic or upload), live transcription display, intent JSON view, and execution log. Also includes a file browser for generated outputs.

## Project Structure

```
.
├── app.py                 # Gradio UI, main entry point
├── agent/
│   ├── stt.py            # Speech-to-text (Faster Whisper)
│   ├── intent.py         # Intent classification (Ollama + Llama 3.2)
│   ├── executor.py       # Pipeline orchestration
│   └── tools/
│       ├── file_creator.py
│       ├── code_generator.py
│       ├── file_editor.py
│       ├── summarizer.py
│       └── chat_handler.py
├── output/               # All generated files land here
├── tests/                # Tests per component
└── requirements.txt
```

## Setup

Python 3.12 is recommended.

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux/macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 2. Install Ollama and the model

Download Ollama from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull llama3.2:3b
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Gradio will start a local server - open the link it prints (usually `http://127.0.0.1:7860`).

## Usage

1. Click the microphone or upload an audio file
2. Speak your command
3. Watch the pipeline execute:
   - Transcription appears first
   - Identified intents show as JSON
   - Execution log shows what each tool did
4. Check `output/` for generated files

## Notes

- All file operations are sandboxed to the `output/` directory
- GPU acceleration is handled automatically by Ollama if available
- The intent classifier can handle compound commands (e.g., "create a file and write code in it" triggers two intents)
