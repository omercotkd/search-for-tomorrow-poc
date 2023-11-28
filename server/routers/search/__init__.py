from fastapi import APIRouter, Request, Depends
from .models import SearchQuery

router = APIRouter()


@router.get("/")
def search_documents(request: Request, query: SearchQuery = Depends()):
    # TODO search documents
    return {"message": "search documents"}
