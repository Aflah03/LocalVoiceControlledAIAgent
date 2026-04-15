import os

class FileCreator:
    def __init__(self, output_dir="output"):
        self.output_dir = os.path.abspath(output_dir)

    def execute(self, params: dict) -> str:
        filename = params.get("filename")
        if not filename:
            # Fallback: Use a timestamped generic name if the model failed to provide one
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"file_{timestamp}.txt"
            params["filename"] = filename

        # Security: Prevent path traversal
        target_path = os.path.abspath(os.path.join(self.output_dir, filename))
        if not target_path.startswith(self.output_dir):
            return f"Security Error: Attempted to write outside output directory."

        try:
            with open(target_path, 'w') as f:
                pass # Create empty file
            return f"Successfully created empty file: {filename}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
