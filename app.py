import time
import requests
from retriever import retrieve_context


class AeroGridAssistant:

    def __init__(self):
        print("\n🌐 Initializing AeroGrid AI Engine...")
        print("⚡ AeroGrid AI Retrieval System Loaded")


    def ask(self, user_query):

        print(f"\n❓ User Question: {user_query}")

        results = retrieve_context(
            user_query,
            top_k=3,
            use_reranker=True
        )

        context_str = "\n\n".join(
            [
                f"[Source: {r['source']}]\n{r['content']}"
                for r in results
            ]
        )

        prompt = f"""
You are AeroGrid AI, an offline renewable energy maintenance assistant.

Answer ONLY using the provided technical documents.

If information is missing:
return INSUFFICIENT_CONTEXT.

DOCUMENTS:

{context_str}


QUESTION:

{user_query}

ANSWER:
"""


        print("🤖 Generating response via Local LLM...")

        start_time = time.time()

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=45
            )

            output_text = response.json().get(
                "response",
                "No response generated."
            )

        except Exception as e:
            output_text = f"Ollama Connection Error: {e}"


        elapsed = round(time.time() - start_time, 2)

        print(f"\n💬 AeroGrid AI Response ({elapsed}s)")
        print("=" * 50)
        print(output_text)
        print("=" * 50)

        return output_text


if __name__ == "__main__":
    assistant = AeroGridAssistant()

    assistant.ask(
        "What should I do if Error Code E-301 occurs on a wind turbine?"
    )
