import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -------------------------------
# Environment Variables
# -------------------------------
HF_API_KEY = os.getenv("HF_API_KEY")

if not HF_API_KEY:
    raise EnvironmentError("❌ HF_API_KEY not found. Add it to your .env file")

# Hugging Face Router Chat Completion endpoint
MODEL_URL = os.getenv(
    "HF_MODEL_URL",
    "https://router.huggingface.co/v1/chat/completions"
)

# Default model (can be changed later)
# Common working models on router.huggingface.co:
# - meta-llama/Llama-3.1-8B-Instruct
# - mistralai/Mistral-7B-Instruct-v0.2
# - google/gemma-7b-it
MODEL_NAME = os.getenv(
    "HF_MODEL_NAME",
    "meta-llama/Llama-3.1-8B-Instruct"  # Updated to a commonly available model
)

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# -------------------------------
# LLM Call Function
# -------------------------------
def call_llm(prompt: str, max_tokens: int = 1500, return_array: bool = False):
    """
    Calls Hugging Face LLM via Router API and extracts JSON safely.

    Args:
        prompt (str): User prompt (must ask for JSON output)
        max_tokens (int): Maximum tokens to generate
        return_array (bool): Expect JSON array if True, else JSON object

    Returns:
        dict or list: Parsed JSON output from LLM
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "Return ONLY valid JSON. "
                    "No markdown, no explanation, no text outside JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(
            MODEL_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ Network error while calling LLM: {e}")

    # -------------------------------
    # Error Handling
    # -------------------------------
    if response.status_code != 200:
        error_text = response.text
        error_msg = f"❌ LLM API Error {response.status_code}:\n{error_text}"
        
        # Provide helpful suggestions for common errors
        if response.status_code == 400:
            try:
                error_json = response.json()
                if "model_not_supported" in error_text or "model" in error_json.get("error", {}).get("code", ""):
                    error_msg += "\n\n💡 Suggestion: The model is not available on this endpoint."
                    error_msg += "\n   Try setting HF_MODEL_NAME in .env to one of these:"
                    error_msg += "\n   - meta-llama/Llama-3.1-8B-Instruct"
                    error_msg += "\n   - mistralai/Mistral-7B-Instruct-v0.2"
                    error_msg += "\n   - google/gemma-7b-it"
            except:
                pass
        
        raise Exception(error_msg)

    result = response.json()

    # -------------------------------
    # Extract text from HF response
    # -------------------------------
    try:
        text = result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise Exception(f"❌ Unexpected LLM response format:\n{result}")

    # -------------------------------
    # Extract JSON safely
    # -------------------------------
    if return_array:
        start = text.find("[")
        end = text.rfind("]") + 1
    else:
        start = text.find("{")
        end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError(
            f"❌ No JSON found in LLM response:\n{text}"
        )

    json_text = text[start:end]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"❌ JSON parsing failed:\n{e}\n\nExtracted text:\n{json_text}"
        )
