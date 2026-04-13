import os
import ollama

class CodeGenerator:
    def __init__(self, model_name="llama3.2:3b", output_dir="output"):
        self.model_name = model_name
        self.output_dir = os.path.abspath(output_dir)

    def execute(self, params: dict) -> str:
        filename = params.get("filename")
        description = params.get("description")
        language = params.get("language", "python")

        if not filename or not description:
            return "Error: Filename and description are required for code generation."

        # Security: Prevent path traversal
        target_path = os.path.abspath(os.path.join(self.output_dir, filename))
        if not target_path.startswith(self.output_dir):
            return "Security Error: Attempted to write outside output directory."

        prompt = f"Write only the source code for a {language} file that does the following: {description}. Do not include any explanations, markdown blocks, or preamble. Just the code."

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            code = response['response']

            with open(target_path, 'w') as f:
                f.write(code)

            return f"Successfully generated and wrote code to {filename}"
        except Exception as e:
            return f"Error generating code: {str(e)}"
