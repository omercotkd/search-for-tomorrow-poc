from fastapi import APIRouter, Depends ,Request

from server.interfaces.interfaces import CreateDocumentPayload, SearchQuery

router = APIRouter()


## Will use it for many and one document as well - same process just one element [doc]
@router.post("/document/bulk")
def create_documents(
        request: Request,
        payload: list[CreateDocumentPayload]
):
    # TODO create documents
    return {"message": "create documents"}

@router.get("/search")
def search_documents(request: Request, query: SearchQuery = Depends()):
    # TODO search documents
    return {"message": "search documents"}


@router.put("/load")
def load_documents_to_redis():
    # TODO load documents to redis
    return {"message": "load documents to redis"}
