from agent.stt import STTHandler
from agent.intent import IntentClassifier
from agent.tools.file_creator import FileCreator
from agent.tools.code_generator import CodeGenerator
from agent.tools.summarizer import Summarizer
from agent.tools.chat_handler import ChatHandler
from agent.tools.file_editor import FileEditor

class AgentExecutor:
    def __init__(self):
        # Initialize all core components
        print("\n--- Initializing Voice Agent Engine ---")
        self.stt = STTHandler()
        self.classifier = IntentClassifier()

        # Note on Hardware: Ollama manages GPU/CPU acceleration automatically.
        # If a GPU is detected, Ollama will prioritize it for Llama 3.2.
        print("[System] Ollama backend is active. GPU acceleration is handled by the Ollama server.")

        # Initialize tool suite
        self.tools = {
            "create_file": FileCreator(),
            "write_code": CodeGenerator(),
            "edit_code": FileEditor(),
            "summarize_text": Summarizer(),
            "general_chat": ChatHandler()
        }

    def process_audio(self, audio_source, is_file=True) -> dict:
        """
        Full pipeline: Audio -> Text -> Intent -> Execution -> Results
        """
        results = {"transcription": "", "intents": [], "execution_log": []}

        # 1. Speech to Text
        if is_file:
            text = self.stt.transcribe_file(audio_source)
        else:
            text = self.stt.transcribe_live()

        results["transcription"] = text
        if not text:
            results["execution_log"].append("No speech detected.")
            return results

        # 2. Intent Classification
        classification = self.classifier.classify(text)
        intents = classification.get("intents", [])
        results["intents"] = intents

        if not intents:
            results["execution_log"].append("Could not determine any clear intent.")
            return results

        # 3. Tool Execution (Handles Compound Commands)
        for item in intents:
            intent_name = item.get("intent")
            params = item.get("params", {})

            if intent_name in self.tools:
                tool = self.tools[intent_name]
                try:
                    # Execute tool and capture result
                    execution_result = tool.execute(params)
                    results["execution_log"].append(f"[{intent_name}] {execution_result}")
                except Exception as e:
                    results["execution_log"].append(f"[{intent_name}] Error: {str(e)}")
            else:
                results["execution_log"].append(f"Unknown intent: {intent_name}")

        return results

if __name__ == "__main__":
    # Smoke test the full pipeline
    executor = AgentExecutor()
    print("Executor initialized. Ready for integration tests.")
