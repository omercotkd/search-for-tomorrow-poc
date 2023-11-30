from fastapi import Query
from pydantic import BaseModel, Field


class Document(BaseModel):
    title: str
    content: str
    dist: float


class CreateDocumentPayload(Document, BaseModel):
    title: str = Field(..., example="Document title")
    content: str = Field(..., example="Document content")


class SearchQuery(BaseModel):
    text: str = Query(..., example="sushi")
    threshold: float = Query(0.85, examples="0~1 threshold , 1 - close semantic , 0 - not close semantic")


class SearchResponse(BaseModel):
    ...
