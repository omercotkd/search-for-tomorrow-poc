from pydantic import BaseModel
from db.models import Document

class EtlData(BaseModel):

    @classmethod
    def from_list(cls, data: list[dict]) -> list["EtlData"]:
        raise NotImplementedError("Convert json to this class")

    def into_document(self) -> "Document":
        raise NotImplementedError("Convert this class to a db document model")


