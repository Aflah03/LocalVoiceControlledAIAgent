import os
import ollama

class Summarizer:
    def __init__(self, model_name="llama3.2:3b", output_dir="output"):
        self.model_name = model_name
        self.output_dir = os.path.abspath(output_dir)

    def execute(self, params: dict) -> str:
        text = params.get("text")
        filename = params.get("filename")

        # If a filename is provided, try to read the file content
        if filename:
            target_path = os.path.abspath(os.path.join(self.output_dir, filename))
            if not target_path.startswith(self.output_dir):
                return "Security Error: Attempted to read outside output directory."

            try:
                with open(target_path, 'r') as f:
                    text = f.read()
            except Exception as e:
                return f"Error reading file {filename}: {str(e)}"

        if not text:
            return "Error: No text or valid filename provided to summarize."

        prompt = f"Summarize the following text concisely:\n\n{text}"

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"Error during summarization: {str(e)}"
