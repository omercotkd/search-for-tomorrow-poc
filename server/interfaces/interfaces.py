from fastapi import Query
from pydantic import BaseModel, Field


class CreateDocumentPayload(BaseModel):
    title: str = Field(..., example="Document title")
    content: str = Field(..., example="Document content")


class SearchQuery(BaseModel):
    text: str = Query(..., example="sushi")

class SearchResponse(BaseModel):
    ...
