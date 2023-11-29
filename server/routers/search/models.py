from pydantic import BaseModel, Field
from fastapi import Query

class SearchQuery(BaseModel):
    text: str = Query(..., example="sushi")

class SearchResponse(BaseModel):
    ...
