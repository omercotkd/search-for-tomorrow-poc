import pymongo
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from env import ENV_VARIABLES
from typing_extensions import Self

DB = pymongo.MongoClient(ENV_VARIABLES.MONGO_URI)[ENV_VARIABLES.DB_NAME]


class DBModel(BaseModel):
    @staticmethod
    def collection_name() -> str:
        raise NotImplementedError("Implement this method")

    id: Optional[ObjectId] = Field(None, alias="_id")
    create_date: datetime = Field(default_factory=datetime.utcnow)
    update_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

    def _to_db_model(self):
        exclude = []

        if self.id is None:
            exclude = ["_id", "id"]

        return self.model_dump(by_alias=True, exclude=exclude)

    def save(self) -> "Self":
        if self.id is None:
            self.id = (
                DB[self.collection_name()].insert_one(self._to_db_model()).inserted_id
            )
        else:
            DB[self.collection_name()].update_one(
                {"_id": self.id}, {"$set": self._to_db_model()}
            )
        return self

    @classmethod
    def find(cls, *args, **kwargs) -> list["Self"]:

        results = list(DB[cls.collection_name()].find(*args, **kwargs))

        return [cls(**item) for item in results]
    
