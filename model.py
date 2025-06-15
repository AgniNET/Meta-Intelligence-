from transformers import pipeline

# Load a basic model (like distilbert)
qa_model = pipeline("text-generation", model="gpt3.5")  # Use a local model

def get_ai_response(prompt: str) -> str:
    output = qa_model(prompt, max_length=100, num_return_sequences=1)
    return output[0]['generated_text']
