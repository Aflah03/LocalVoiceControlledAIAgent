import ollama

class ChatHandler:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name
        self.history = [] # Simple session memory

    def execute(self, params: dict) -> str:
        text = params.get("text")
        if not text:
            return "Error: No chat message provided."

        # Add user message to history
        self.history.append({'role': 'user', 'content': text})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self.history
            )
            reply = response['message']['content']

            # Add assistant response to history
            self.history.append({'role': 'assistant', 'content': reply})

            # Keep history manageable (last 10 turns)
            if len(self.history) > 20:
                self.history = self.history[-20:]

            return reply
        except Exception as e:
            return f"Error in chat handler: {str(e)}"
