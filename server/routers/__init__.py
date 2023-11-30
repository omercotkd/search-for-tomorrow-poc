from fastapi import APIRouter, Depends, Request
from pydantic.v1.json import pydantic_encoder

from interfaces import CreateDocumentPayload, SearchQuery
from redis_embedding import RedisStorageVector
from env import ENV_VARIABLES
from db.models import Document

router = APIRouter()
redis_embedding_client = RedisStorageVector(redis_uri=ENV_VARIABLES.REDIS_URI)


## Will use it for many and one document as well - same process just one element [doc]
@router.post("/document/bulk")
def create_documents(request: Request, payload: list[CreateDocumentPayload]):

    ## save on mongodb
    for item in payload:
        Document(
            extrnal_id=None,
            title=item.title,
            content=item.content,
            contact=None,
            link=None,
        ).save()

    ## save on redis
    documents = [item.model_dump() for item in payload]

    redis_embedding_client.load(documents)

    return {"message": "create documents"}


@router.get("/search")
def search_documents(request: Request, query: SearchQuery = Depends()):
    docs = redis_embedding_client.find_similarity_documents(
        question=query.text, threshold=query.threshold
    )

    return {"docs": docs}


@router.put("/load")
def load_documents_to_redis():
    documents = Document.find()

    redis_embedding_client.load([item.model_dump() for item in documents])

    return {"message": "load documents to redis"}
