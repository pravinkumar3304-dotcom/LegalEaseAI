from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator
)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------
# AI GENERATOR
# ---------------------------------------------------------

generator = GeminiDocumentGenerator()


# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000,
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000,
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    jurisdiction: str = Field(
        default="Not specified",
        max_length=200,
    )

    language: str = Field(
        default="English",
        max_length=50,
    )


# ---------------------------------------------------------
# GENERATE DOCUMENT
# ---------------------------------------------------------

@router.post("/generate")
def generate_document(
    request: DocumentRequest,
):

    try:

        document = generator.generate_document(
            request.model_dump()
        )

        return {
            "success": True,
            "document_type": request.document_type,
            "document": document,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {error}",
        )