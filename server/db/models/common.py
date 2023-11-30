import pymongo
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime




class DBModel(BaseModel):
    _id: ObjectId 
    created_at: datetime


