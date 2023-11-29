from fastapi import APIRouter
from . import load, document, search

router = APIRouter()

router.include_router(load.router, prefix="/load", tags=["load"])
router.include_router(document.router, prefix="/document", tags=["document"])
router.include_router(search.router, prefix="/search", tags=["search"])
