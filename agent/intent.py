import ollama
import json
import re

class IntentClassifier:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name
        self.system_prompt = (
            "You are a precise intent classifier for a voice-controlled AI agent. "
            "Your goal is to analyze the user's transcription and return a structured JSON "
            "object containing a list of intents to execute. "
            "\n\nAvailable Intents:\n"
            "1. `create_file`: Create a new empty file.\n"
            "2. `write_code`: Generate code and write it to a file.\n"
            "3. `summarize_text`: Summarize a given piece of text.\n"
            "4. `general_chat`: Answer a question or engage in conversation.\n"
            "\nJSON Schema Requirements:\n"
            "Return ONLY a JSON object with the following structure:\n"
            "{\n"
            "  \"intents\": [\n"
            "    {\n"
            "      \"intent\": \"intent_name\",\n"
            "      \"params\": {\n"
            "        \"filename\": \"name_of_file\",\n"
            "        \"description\": \"what the code/file should do\",\n"
            "        \"language\": \"programming_language\",\n"
            "        \"text\": \"text to summarize or chat query\"\n"
            "      }\n"
            "    }\n"
            "  ],\n"
            "  \"confidence\": float (0.0 to 1.0)\n"
            "}\n"
            "\nExample:\n"
            "User: 'Create a python file called utils.py and write a function to calculate fibonacci'\n"
            "Response: {\"intents\": [{\"intent\": \"create_file\", \"params\": {\"filename\": \"utils.py\"}}, {\"intent\": \"write_code\", \"params\": {\"filename\": \"utils.py\", \"description\": \"fibonacci function\", \"language\": \"python\"}}], \"confidence\": 0.98}"
        )

    def classify(self, text: str) -> dict:
        """
        Sends the transcription to Ollama and parses the JSON response.
        """
        try:
            print(f"\n[Brain] Analyzing intent for: '{text}'...")
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': text},
                ],
                format='json' # Forces Ollama to return JSON
            )

            content = response['message']['content']
            print(f"[Brain] Intent identified: {content}")
            return json.loads(content)
        except Exception as e:

            print(f"Intent Classification Error: {e}")
            # Return a graceful fallback
            return {
                "intents": [{"intent": "general_chat", "params": {"text": text}}],
                "confidence": 0.0,
                "error": str(e)
            }

if __name__ == "__main__":
    # Quick test
    classifier = IntentClassifier()
    test_text = "Create a file called greeting.py and write a print hello world in it"
    print(f"Input: {test_text}")
    print(f"Output: {classifier.classify(test_text)}")
