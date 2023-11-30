from .common import DBModel
from pydantic import Field
from typing import Optional

class Document(DBModel):

    @staticmethod
    def collection_name() -> str:
        return "documents"

    extrnal_id: Optional[str] = Field(None, alias="extrnal_id")
    title: str = Field(..., alias="title")
    content: str = Field(..., alias="content")
    contact: Optional[str] = Field(None, alias="contact")
    link: Optional[str] = Field(None, alias="link")


