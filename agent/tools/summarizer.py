import ollama

class Summarizer:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name

    def execute(self, params: dict) -> str:
        text = params.get("text")
        if not text:
            return "Error: No text provided to summarize."

        prompt = f"Summarize the following text concisely:\n\n{text}"

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            return f"Error during summarization: {str(e)}"
