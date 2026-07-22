from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.retrieval.retriever import retrieve_context
from src.generation.llm import LocalLLM
from src.security.guardrails import check_input_safety


app = FastAPI(
    title="AeroGrid AI API",
    description="Enterprise Renewable Energy Maintenance RAG Engine",
    version="1.0.0"
)


llm = LocalLLM()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AeroGrid AI"
    }


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    question = request.question

    security_result = check_prompt(question)

    if not security_result["allowed"]:
        raise HTTPException(
            status_code=400,
            detail="Unsafe prompt detected"
        )

    context = retrieve_context(
        question,
        top_k=3,
        use_reranker=True
    )

    if not context:
        return {
            "answer": "INSUFFICIENT_CONTEXT",
            "sources": []
        }


    answer = llm.generate(
        question,
        context
    )


    sources = [
        item["source"]
        for item in context
    ]


    return {
        "answer": answer,
        "sources": sources
    }

