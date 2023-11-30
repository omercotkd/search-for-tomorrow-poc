import json
import os

from fastapi import APIRouter, Depends,Request
from pydantic.v1.json import pydantic_encoder

from server.interfaces import CreateDocumentPayload, SearchQuery
from server.redis_embedding import RedisStorageVector
from env import ENV_VARIABLES

router = APIRouter()
redis_embedding_client = RedisStorageVector(redis_uri=ENV_VARIABLES.REDIS_URI)

## Will use it for many and one document as well - same process just one element [doc]
@router.post("/document/bulk")
def create_documents(
        request: Request,
        payload: list[CreateDocumentPayload]
):
    # TODO create documents

    ## save on mongodb

    ## save on redis
    documents = [item.model_dump() for item in payload]

    print(documents)
    redis_embedding_client.load(documents)

    return {"message": "create documents"}

@router.get("/search")
def search_documents(request: Request, query: SearchQuery = Depends()):
    # TODO search documents
    print(query.text)
    docs = redis_embedding_client.find_similarity_documents(question=query.text, threshold=query.threshold)
    print(docs)

    return {"docs": docs}


@router.put("/load")
def load_documents_to_redis():
    # TODO load documents to redis

    # query mongodb , take all documents collections

    # then do flush on redis

    # call redisEmbeddingClient.load(documents from collection)
    return {"message": "load documents to redis"}
