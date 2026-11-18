
from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.models import (
    ChatRequest,
    ChatResponse,
    UploadResponse
)

from app.services.document_loader import extract_text_from_pdf
from app.services.chunking import create_document_chunks
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.rag import RAGService


router = APIRouter()

UPLOAD_DIR = Path("documents")
UPLOAD_DIR.mkdir(exist_ok=True)

embedding_service = EmbeddingService()
vector_store = VectorStore()
rag_service = RAGService()


@router.post("/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):

    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Envie um arquivo PDF válido."
        )

    # Salvar o PDF recebido
    file_path = UPLOAD_DIR / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extrair texto
        pages = extract_text_from_pdf(str(file_path))

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível extrair texto do PDF."
            )

        # Dividir em chunks
        chunks = create_document_chunks(pages)

        for chunk in chunks:
            chunk["source"] = file.filename

        # Gerar embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.encode_documents(texts)

        # Armazenar no Qdrant
        vector_store.create_collection()
        vector_store.insert_chunks(chunks, embeddings)

        return UploadResponse(
            filename=file.filename,
            pages_processed=len(pages),
            chunks_created=len(chunks),
            message="Documento processado e armazenado com sucesso."
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar documento: {str(error)}"
        )

    finally:
        await file.close()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        result = rag_service.ask(request.question)
        return result

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar resposta: {str(error)}"
        )
