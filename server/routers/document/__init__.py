from fastapi import APIRouter, Request
from .models import CreateDocumentPayload

router = APIRouter()

@router.post("/")
def create_document(
    request: Request,
    payload: CreateDocumentPayload
):
    # TODO create document
    return {"message": "create document"}

@router.post("/bulk")
def create_documents(
    request: Request,
    payload: list[CreateDocumentPayload]
):
    # TODO create documents
    return {"message": "create documents"}