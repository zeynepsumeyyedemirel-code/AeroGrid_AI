import time
import requests
from retriever import AeroGridRetriever

class AeroGridAssistant:
    def __init__(self):
        print("\n🌐 Initializing AeroGrid AI Engine...")
        self.retriever = AeroGridRetriever()
        print("⚡ AeroGrid AI is ONLINE (Powered by Ollama Local LLM)!")

    def ask(self, user_query):
        print(f"\n❓ User Question: {user_query}")
        
        # 1. RAG ile dokümanlardan bilgiyi getir
        results = self.retriever.search(user_query, top_k=2)
        context_str = "\n".join([f"[Source: {r['source']}]\n{r['text']}" for r in results])
        
        prompt = f"""You are AeroGrid AI, an offline field service assistant for wind and solar farms.
Use ONLY the provided official field documents below to answer the user's question concisely.

FIELD DOCUMENTS:
{context_str}

USER QUESTION: {user_query}
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
                }
            )
            output_text = response.json().get("response", "No response generated.")
        except Exception as e:
            output_text = f"Ollama Connection Error: {e}"

        elapsed = round(time.time() - start_time, 2)
        
        print(f"\n💬 AeroGrid AI Response (generated in {elapsed}s):")
        print("==================================================")
        print(output_text)
        print("==================================================")
        return output_text

if __name__ == "__main__":
    assistant = AeroGridAssistant()
    assistant.ask("What should I do if Error Code E-301 occurs on a wind turbine?")