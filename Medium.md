# Building a Local Voice AI Agent: My Mem0 Internship Journey

When I started this internship project at Mem0, I had one goal: build a voice-controlled AI agent that runs entirely locally. No cloud APIs, no latency from external calls, no privacy concerns. Just pure, offline voice interaction.

Here's how it went — and the struggles I faced along the way.

---

## The Architecture

The project follows a clean pipeline architecture:

```
Audio Input → Whisper (STT) → Llama 3.2 (Intent) → Tool Executor → Gradio UI
```

### Components

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Speech-to-Text** | Faster Whisper | Transcribes audio to text |
| **Intent Classification** | Llama 3.2:3b via Ollama | Understands what the user wants |
| **Tool Execution** | Custom Python tools | Executes the identified actions |
| **UI** | Gradio | Web interface for voice input |

### Project Structure

```
.
├── app.py                 # Main Gradio UI
├── agent/
│   ├── stt.py            # Speech-to-text handler
│   ├── intent.py         # Intent classifier
│   ├── executor.py       # Pipeline orchestrator
│   └── tools/
│       ├── file_creator.py
│       ├── code_generator.py
│       ├── file_editor.py
│       ├── summarizer.py
│       └── chat_handler.py
├── output/               # Safe directory for generated files
└── tests/                # Layer-specific tests
```

---

## How It Works

1. **User speaks** into the microphone or uploads an audio file
2. **Whisper transcribes** the audio to text
3. **Llama 3.2 analyzes** the text and identifies intents (as JSON)
4. **Executor routes** each intent to the appropriate tool
5. **Tools execute** and generate results in the `/output` directory
6. **UI displays** transcription, detected intents, and execution logs

### Example Commands

| Voice Command | What Happens |
|---------------|--------------|
| "Create a Python file called hello.py and write a function to calculate fibonacci" | Creates `hello.py` + writes fibonacci code |
| "Summarize the file report.txt" | Reads and summarizes the file |
| "What is machine learning?" | Conversational response |
| "Edit main.py to add a login function" | Updates existing file with new code |

---

## The Struggles

### 1. The Compound Intent Problem

**The Issue:** When I said *"Create a Python file called hello.py and in it write code to print the first n prime numbers"*, the system only created the file — it didn't write any code.

**Why:** The intent classifier (Llama 3.2:3b) was focusing on the first action ("create file") and returning early, missing the second intent ("write code").

**The Fix:** I restructured the system prompt with explicit pattern recognition:

```
=== RECOGNITION PATTERNS ===
- 'Create a file called X and write code...' → create_file + write_code (TWO intents)
- 'Create X and in it write...' → create_file + write_code (TWO intents)
```

I also added specific examples matching real user commands directly in the prompt.

### 2. Malformed JSON from the LLM

**The Issue:** Llama 3.2:3b sometimes returned broken JSON like:

```json
{  "intents": [...],  "confidence"  ]}  // Missing value, wrong brackets
```

This crashed the entire pipeline with `AttributeError`.

**The Fix:** I built a `fix_malformed_json()` function that:
- Strips markdown code blocks
- Fixes missing values
- Repairs mismatched brackets

And implemented two-stage parsing — try normal parse first, then fix and retry.

### 3. Markdown Code Blocks in Output

**The Issue:** Generated code included markdown wrappers:

```python
print("Hello")
```

**The Fix:** Added regex cleanup in the code generator:

```python
code = re.sub(r'^```[a-zA-Z]*\n', '', code)  # Remove opening
code = re.sub(r'\n```$', '', code)           # Remove closing
```

### 4. Missing Description Fields

**The Issue:** Commands like *"Write C++ code to print 1 to 100"* returned `write_code` intent but with an empty `description` field, causing the code generator to fail.

**The Fix:** Added explicit instructions in the system prompt:

```
=== CRITICAL: EXTRACTING DESCRIPTION FOR write_code ===
- The `description` field is REQUIRED - NEVER leave it empty.
- Extract WHAT the code should do from the user's request.
```

### 5. Editing Existing Files Not Recognized

**The Issue:** *"Edit hello.js to print a triangle"* was classified as `general_chat` because "edit" wasn't recognized as a code-writing action.

**The Fix:** Added a dedicated section for file editing patterns with clear examples.

---

## Key Learnings

1. **Small models need explicit patterns** — Llama 3.2:3b is fast but requires very clear, structured instructions. Examples alone aren't enough.

2. **Never trust LLM output** — Always validate and sanitize. JSON parsing with fallback is essential.

3. **Compound commands are hard** — Users naturally combine actions with "and". The system must detect and handle multiple intents.

4. **Security matters** — Path traversal prevention in all file operations (`if not target_path.startswith(self.output_dir)`).

---

## Running the Project

### Prerequisites

```bash
# Install Ollama and pull the model
ollama pull llama3.2:3b

# Install Python dependencies
pip install -r requirements.txt
```

### Run the App

```bash
python app.py
```

Then open `http://localhost:7860` in your browser.

---

## What's Next

- [ ] Support for more tools (web search, API calls)
- [ ] Multi-file project generation
- [ ] Voice feedback (text-to-speech)
- [ ] Conversation memory across sessions

---

This project taught me more about LLM integration, prompt engineering, and defensive programming than any tutorial could. The struggles were real, but so were the lessons.

If you're building with local LLMs, feel free to reach out — I'd love to compare notes!

---

*Built as part of the Mem0 Internship program.*
