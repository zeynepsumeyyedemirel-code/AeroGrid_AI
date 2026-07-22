from retriever import retrieve_context

TEST_BENCHMARK = [
    {
        "query": "What is the maximum wind speed limit for climbing?",
        "expected_source": "fall-protection-height.txt"
    },
    {
        "query": "How to isolate stator overheating E-301?",
        "expected_source": "E-301-stator-overheating.txt"
    },
    {
        "query": "Explain LOTO 8 step lockout procedure",
        "expected_source": "loto-8-step-procedure.txt"
    }
]

def test_retrieval_precision():
    print("\n🧪 Running RAG Retrieval Precision Evaluation...")
    total_queries = len(TEST_BENCHMARK)
    hit_count = 0

    for test in TEST_BENCHMARK:
        results = retrieve_context(test["query"], top_k=3)
        sources = [res["source"] for res in results]
        
        hit = any(test["expected_source"] in src for src in sources)
        if hit:
            hit_count += 1
            print(f"✅ PASS | Query: '{test['query']}' -> Found in top matches.")
        else:
            print(f"❌ FAIL | Query: '{test['query']}' -> Expected {test['expected_source']} not in {sources}")

    precision = (hit_count / total_queries) * 100
    print(f"\n📊 Retrieval Hit Rate (Precision@3): {precision:.2f}%\n")
    assert precision >= 80.0, "Retrieval Precision fell below acceptable 80% threshold!"

if __name__ == "__main__":
    test_retrieval_precision()
