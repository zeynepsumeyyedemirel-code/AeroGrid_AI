import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def main():
    print("🚀 AeroGrid AI - Starting Local Engine Test...")
    
    # Hugging Face üzerindeki resmi Phi-3.5-mini modeli
    model_id = "microsoft/Phi-3.5-mini-instruct"
    
    print(f"🔎 Loading model and tokenizer: {model_id}...")
    start_time = time.time()
    
    # Tokenizer ve Model yükleme
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype="auto", 
        device_map="auto"
    )
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    
    print(f"⚡ Model ready! (Load time: {round(time.time() - start_time, 2)} seconds)")

    # Test mesajları
    messages = [
        {
            "role": "system", 
            "content": "You are AeroGrid AI, an offline field service assistant for wind and solar farms. You provide concise, accurate technical support."
        },
        {
            "role": "user", 
            "content": "Hello! What is the maximum wind speed limit for climbing a wind turbine tower?"
        }
    ]
    
    print("\n🤖 Sending test query to AeroGrid AI...")
    outputs = pipe(messages, max_new_tokens=150)
    
    response = outputs[0]["generated_text"][-1]["content"]
    
    print("\n💬 AeroGrid AI Response:")
    print("--------------------------------------------------")
    print(response)
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()