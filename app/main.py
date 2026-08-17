from fastapi import FastAPI, UploadFile, File,HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.rag.embeddings import vector_db
from services.pdf_services import extract_text, create_chunks

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


app = FastAPI(
    title="Production level RAG system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "welcome to RAG pipeline"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        content = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # Extract PDF text
        documents = extract_text(file_path)

        print("Number of documents:", len(documents))

        # Create chunks
        chunks = create_chunks(documents)

        print("Number of chunks:", len(chunks))

        # Add chunks to Qdrant
        vector_db.add_documents(chunks)

        print("Chunks added to Qdrant")

        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "message": "PDF uploaded and processed successfully",
            "filename": file.filename,
            "documents": len(documents),
            "chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as e:

        print("UPLOAD ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
app.include_router(chat_router)