import ollama
import json
import re

def fix_malformed_json(json_str: str) -> str:
    """
    Attempt to fix common JSON formatting issues from LLM output.
    """
    # Remove any leading/trailing markdown code blocks
    json_str = re.sub(r'^```(?:json)?\s*', '', json_str.strip())
    json_str = re.sub(r'\s*```$', '', json_str)

    # Fix missing values (e.g., "confidence"  ]} -> "confidence": 0.98]})
    json_str = re.sub(r'"confidence"\s*]', '"confidence": 0.98]', json_str)
    json_str = re.sub(r'"confidence"\s*}', '"confidence": 0.98}', json_str)

    # Fix missing closing braces/brackets
    open_braces = json_str.count('{') - json_str.count('}')
    open_brackets = json_str.count('[') - json_str.count(']')

    json_str += '}' * open_braces + ']' * open_brackets

    return json_str

class IntentClassifier:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name
        self.system_prompt = (
            "You are a precise intent classifier for a voice-controlled AI agent. "
            "Your goal is to analyze the user's transcription and return a structured JSON "
            "object containing a list of intents to execute. "
            "\n\nAvailable Intents:\n"
            "1. `create_file`: Create a new empty file.\n"
            "2. `write_code`: Generate code and write it to a file (works for both new and existing files).\n"
            "3. `summarize_text`: Summarize a given piece of text.\n"
            "4. `general_chat`: Answer a question or engage in conversation.\n"
            "\n=== CRITICAL RULES FOR COMPOUND COMMANDS ===\n"
            "- When you see BOTH 'create/make a file' AND 'write/generate code' in the same request → return TWO intents.\n"
            "- Pattern: 'Create a [language] file called X AND write/generate/do Y' = create_file + write_code.\n"
            "- Pattern: 'In file X, write code that does Y' = write_code only (file already exists).\n"
            "- ALWAYS check: does the user want code written? If yes → write_code intent is REQUIRED.\n"
            "- NEVER return only create_file when the user also asks for code to be written.\n"
            "\n=== CRITICAL: EDITING/UPDATING EXISTING FILES ===\n"
            "- When user says 'edit', 'update', 'modify', 'change' a file → use `write_code` intent.\n"
            "- `write_code` works for BOTH creating new code AND overwriting existing files.\n"
            "- Example: 'Edit hello.js to print a triangle' → `write_code` with filename: 'hello.js'\n"
            "- Example: 'Update main.py to add a login function' → `write_code` with filename: 'main.py'\n"
            "\n=== CRITICAL: EXTRACTING DESCRIPTION FOR write_code ===\n"
            "- The `description` field is REQUIRED for write_code intent - NEVER leave it empty.\n"
            "- Extract WHAT the code should do from the user's request (e.g., 'print 1 to 100', 'calculate fibonacci').\n"
            "- If user says 'Write a code in C++ to print 1 to 100', description = 'print numbers from 1 to 100'.\n"
            "- If user says 'create a script that adds two numbers', description = 'add two numbers'.\n"
            "- ALWAYS include the language when explicitly mentioned (e.g., 'in C++' -> language: 'cpp', 'in JavaScript' -> language: 'javascript').\n"
            "- If user mentions 'take user input' or 'ask user for size', include this in description (e.g., 'print triangle, size from user input').\n"
            "\n=== RECOGNITION PATTERNS ===\n"
            "- 'Create a file called X and write code...' → create_file + write_code (TWO intents)\n"
            "- 'Create X and in it write...' → create_file + write_code (TWO intents)\n"
            "- 'Write code in X to do Y' → write_code only\n"
            "- 'Edit X to do Y' → write_code only\n"
            "\nInstructions for Classification:\n"
            "- If the user mentions 'write', 'create', 'make', 'generate', 'code', 'script', 'edit', 'update', or 'modify' in the context of a file or program, "
            "strongly prioritize `write_code` or `create_file` over `general_chat`.\n"
            "- If the user wants a file but doesn't specify a name, YOU MUST generate a suitable, descriptive filename (e.g., 'hello_world.py' for a print hello world script) and include it in the `params`.\n"
            "- Only use `general_chat` if the request is purely conversational or a general question with no output file required.\n"
            "\nJSON Schema Requirements:\n"
            "Return ONLY a JSON object with the following structure:\n"
            "{\n"
            "  \"intents\": [\n"
            "    {\n"
            "      \"intent\": \"intent_name\",\n"
            "      \"params\": {\n"
            "        \"filename\": \"name_of_file\",\n"
            "        \"description\": \"what the code/file should do (REQUIRED for write_code)\",\n"
            "        \"language\": \"programming_language\",\n"
            "        \"text\": \"text to summarize or chat query\"\n"
            "      }\n"
            "    }\n"
            "  ],\n"
            "  \"confidence\": float (0.0 to 1.0)\n"
            "}\n"
            "\n=== EXAMPLES ===\n"
            "User: 'Create a file called utils.py and write a function to calculate fibonacci'\n"
            "Response: {\"intents\": [{\"intent\": \"create_file\", \"params\": {\"filename\": \"utils.py\"}}, {\"intent\": \"write_code\", \"params\": {\"filename\": \"utils.py\", \"description\": \"fibonacci function\", \"language\": \"python\"}}], \"confidence\": 0.98}\n"
            "User: 'Create a python file called hi.py and write a code to generate first n prime numbers'\n"
            "Response: {\"intents\": [{\"intent\": \"create_file\", \"params\": {\"filename\": \"hi.py\"}}, {\"intent\": \"write_code\", \"params\": {\"filename\": \"hi.py\", \"description\": \"generate first n prime numbers with user input\", \"language\": \"python\"}}], \"confidence\": 0.98}\n"
            "User: 'Write a code in C++ to print 1 to 100 in a file called hi.cpp'\n"
            "Response: {\"intents\": [{\"intent\": \"create_file\", \"params\": {\"filename\": \"hi.cpp\"}}, {\"intent\": \"write_code\", \"params\": {\"filename\": \"hi.cpp\", \"description\": \"print numbers from 1 to 100\", \"language\": \"cpp\"}}], \"confidence\": 0.98}\n"
            "User: 'Edit the file hello.js and print a triangle, take user input for size'\n"
            "Response: {\"intents\": [{\"intent\": \"write_code\", \"params\": {\"filename\": \"hello.js\", \"description\": \"print a triangle with size from user input\", \"language\": \"javascript\"}}], \"confidence\": 0.98}\n"
            "User: 'Update main.py to add a login function with username and password'\n"
            "Response: {\"intents\": [{\"intent\": \"write_code\", \"params\": {\"filename\": \"main.py\", \"description\": \"login function with username and password parameters\", \"language\": \"python\"}}], \"confidence\": 0.98}\n"
            "User: 'Create a Python file called hello.py and in it write a code to print the first n prime numbers, n from user input'\n"
            "Response: {\"intents\": [{\"intent\": \"create_file\", \"params\": {\"filename\": \"hello.py\"}}, {\"intent\": \"write_code\", \"params\": {\"filename\": \"hello.py\", \"description\": \"print first n prime numbers with n from user input\", \"language\": \"python\"}}], \"confidence\": 0.98}"
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
            print(f"[Brain] Raw LLM output: {content}")

            # Try parsing directly first
            try:
                result = json.loads(content)
                print(f"[Brain] Intent identified: {result}")
                return result
            except json.JSONDecodeError as je:
                print(f"[Brain] JSON parse error: {je}, attempting to fix...")
                # Try to fix malformed JSON
                fixed_content = fix_malformed_json(content)
                print(f"[Brain] Fixed JSON: {fixed_content}")
                result = json.loads(fixed_content)
                print(f"[Brain] Intent identified: {result}")
                return result

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
