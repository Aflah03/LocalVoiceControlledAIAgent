import os

class FileEditor:
    def __init__(self, output_dir="output"):
        self.output_dir = os.path.abspath(output_dir)

    def execute(self, params: dict) -> str:
        filename = params.get("filename")
        content = params.get("content")

        if not filename:
            return "Error: No filename provided for editing."
        if content is None:
            return "Error: No content provided to write to the file."

        # Security: Prevent path traversal
        target_path = os.path.abspath(os.path.join(self.output_dir, filename))
        if not target_path.startswith(self.output_dir):
            return f"Security Error: Attempted to edit outside output directory."

        try:
            with open(target_path, 'w') as f:
                f.write(content)
            return f"Successfully updated file: {filename}"
        except Exception as e:
            return f"Error editing file: {str(e)}"
