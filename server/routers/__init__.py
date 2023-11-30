import os

from fastapi import APIRouter, Depends,Request

from server.interfaces import CreateDocumentPayload, SearchQuery
from server.redis_embedding import RedisStorageVector
from env import ENV_VARIABLES

router = APIRouter()

print(ENV_VARIABLES.REDIS_URI)

redis_embedding_client = RedisStorageVector(redis_uri=os.getenv("REDIS_URI"))

## Will use it for many and one document as well - same process just one element [doc]
@router.post("/document/bulk")
def create_documents(
        request: Request,
        payload: list[CreateDocumentPayload]
):
    # TODO create documents

    ## save on mongodb

    ## save on redis

    redis_embedding_client.load(payload)

    return {"message": "create documents"}

@router.get("/search")
def search_documents(request: Request, query: SearchQuery = Depends()):
    # TODO search documents

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
