
from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Assistente inteligente para perguntas e respostas sobre documentos PDF.",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG Assistant está funcionando!",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "online"
    }
