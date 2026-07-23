import time
import requests


OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
MODEL_NAME = "phi3:latest"


def main():
    print("🚀 AeroGrid AI - Starting Ollama Local Engine Test...")

    payload = {
        "model": MODEL_NAME,
        "prompt": "Explain the safety procedure for wind turbine maintenance.",
        "stream": False
    }

    print(f"🔎 Testing local model: {MODEL_NAME}")

    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        elapsed = time.time() - start_time

        print("✅ Ollama connection successful!")
        print(f"⏱️ Response time: {elapsed:.2f}s")
        print("\n🤖 Model Response:")
        print(result.get("response", ""))

    except Exception as e:
        print("❌ Ollama test failed:")
        print(e)


if __name__ == "__main__":
    main()
