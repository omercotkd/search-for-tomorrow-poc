from fastapi import APIRouter

router = APIRouter()

@router.put("/")
def load_documents_to_redis():
    # TODO load documents to redis
    return {"message": "load documents to redis"}
