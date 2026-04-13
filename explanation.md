# 🎙️ Voice-Enabled AI Agent: Full Technical Explanation

This document is designed to help you understand every single part of the project. Even if you are new to coding, you can use this guide to explain exactly how the system works to an interviewer.

---

## 🧩 High-Level Concept: The Pipeline
Think of this project as a **relay race**. Data starts as sound and passes through different "runners" (modules) until it becomes a finished action.

**Audio** $\rightarrow$ **STT** (Text) $\rightarrow$ **Classifier** (Intent) $\rightarrow$ **Executor** (Action) $\rightarrow$ **UI** (Display)

---

## 📂 1. Project Structure & Foundation

### `/output` Folder
- **What is it?** A dedicated folder where all files created by the AI are stored.
- **Why?** For **Security**. We don't want the AI to accidentally overwrite your system files or delete important data. By locking it to this folder, we create a "Sandbox."

### `requirements.txt`
- **What is it?** A list of external libraries (packages) the project needs.
- **Key Terms**:
    - `faster-whisper`: A high-performance version of OpenAI's Whisper model for converting speech to text.
    - `ollama`: A tool that allows you to run powerful LLMs (like Llama 3.2) locally on your own computer.
    - `gradio`: A library for quickly building a web interface for AI models.

---

## 🎤 2. Speech-to-Text (`agent/stt.py`)

This file handles the "hearing" part of the agent.

- **`WhisperModel`**: This is the AI model that converts audio waves into words.
- **`device="cpu"` & `compute_type="int8"`**: 
    - `cpu`: Tells the model to run on your processor (not requiring an expensive GPU).
    - `int8`: This is **Quantization**. It means we "compress" the model's numbers to make it run faster and use less RAM without losing much accuracy.
- **`transcribe_file`**: Takes a path to an audio file and returns the text.
- **`transcribe_live`**: Uses `sounddevice` to record a few seconds of audio from your mic, converts it into a "NumPy array" (a list of numbers representing the sound wave), and sends it to Whisper.

---

## 🧠 3. The Intent Classifier (`agent/intent.py`)

This is the "Brain." It doesn't do the work; it decides **what work needs to be done**.

- **`system_prompt`**: This is the "Instruction Manual" given to the LLM. We tell it: *"You are a classifier. Don't talk to me like a human; just give me a JSON object."*
- **JSON (JavaScript Object Notation)**: A structured way of storing data that computers can read easily. 
    - *Example*: Instead of saying "I want to create a file," the AI says `{"intent": "create_file"}`.
- **`format='json'`**: A special setting in Ollama that forces the AI to only return valid JSON. This prevents the AI from adding conversational filler like *"Sure! Here is your JSON:"* which would crash the program.
- **Compound Commands**: Because we ask for a **list** of intents (`"intents": [...]`), the AI can identify multiple tasks in one sentence.

---

## 🛠️ 4. The Tool Suite (`agent/tools/`)

These are the "Hands" of the agent. Each tool does one specific job.

### `file_creator.py`
- **Path Traversal Security**: I use `os.path.abspath` and `.startswith()`. This checks if the final file path is actually inside the `/output` folder. If a user tries to say *"Create a file in C:/Windows"*, the code will block it.

### `code_generator.py`
- **The Prompt**: We tell the LLM to provide **only** the code. If the LLM adds "Here is your code:" at the top, the file will contain that text, which would make the code crash when run.

### `summarizer.py` & `chat_handler.py`
- **Session Memory**: In `chat_handler.py`, we have a list called `self.history`. 
    - Every time you speak, we add your message to the list.
    - Every time the AI answers, we add its answer to the list.
    - We send the **entire list** back to the AI every time, so it remembers what you said two minutes ago.

---

## ⚙️ 5. The Orchestrator (`agent/executor.py`)

The "Manager" that coordinates everything.

- **`AgentExecutor`**: This class initializes the STT, the Classifier, and all the Tools.
- **The Loop**: It takes the list of intents from the classifier and loops through them:
    - *Intent 1: create_file* $\rightarrow$ Call `FileCreator.execute()`
    - *Intent 2: write_code* $\rightarrow$ Call `CodeGenerator.execute()`
- **Aggregation**: It collects the results from every tool and puts them into an `execution_log`.

---

## 💻 6. The User Interface (`app.py`)

The "Face" of the project.

- **`gr.Blocks`**: The main container for the Gradio layout.
- **`gr.Audio`**: A magic component that handles both the microphone recording and the file upload button automatically.
- **Pipeline View**: Instead of just showing the final result, we show the **Internal State**:
    1. Transcription (What was heard)
    2. JSON (What the AI thought)
    3. Log (What actually happened)
- **`list_output_files`**: A helper function that looks at the `/output` folder and tells the user what files are currently there.

---

## 🎓 Summary Table for Quick Reference

| Term | Plain English Explanation |
| :--- | :--- |
| **LLM** | Large Language Model (the AI that understands text). |
| **STT** | Speech-to-Text (converting voice to words). |
| **Quantization** | Making the AI model smaller and faster (e.g., `int8`). |
| **JSON** | A structured "dictionary" format for data. |
| **Intent** | The "goal" or "purpose" behind a user's words. |
| **Path Traversal** | A security flaw where someone tries to access folders they shouldn't. |
| **Session Memory** | The AI's ability to remember the current conversation history. |
| **Orchestrator** | The code that manages the flow between different modules. |
