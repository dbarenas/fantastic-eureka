import os
import ollama

# Ollama connection details from environment variables
ollama_model = os.environ.get("OLLAMA_MODEL", "llama3:8b")
ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

client = ollama.Client(host=ollama_base_url)

def call_llm(prompt: str) -> str:
    """Sends a prompt to the Ollama service and returns the response."""
    try:
        response = client.chat(model=ollama_model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "Error: Could not get a response from the language model."
