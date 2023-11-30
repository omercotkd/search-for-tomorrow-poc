import logging
from abc import ABC
from typing import List

import numpy as np
import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer, util

from server.interfaces import Document


class RedisStorageVector(ABC):
    def __init__(self, redis_uri=None):
        self.prefix = 'documents:'
        self.redis_client = redis.Redis.from_url(url=redis_uri)
        self.dim = 768
        self.index_name = 'documents:index'
        self.embedding_model = SentenceTransformer('sentence-transformers/quora-distilbert-multilingual')
        self.VECTOR_FIELD_NAME = 'embedding'
        self.TITLE_FIELD_NAME = 'title'
        self.CONTENT_FIELD_NAME = 'content'

    def create_schema_redis(self):
        schema = (VectorField(self.VECTOR_FIELD_NAME, "FLAT",
                              {"TYPE": "FLOAT32", "DIM": self.dim, "DISTANCE_METRIC": "COSINE"}),
                  TagField(self.TITLE_FIELD_NAME),
                  TagField(self.CONTENT_FIELD_NAME))

        try:
            logging.info(msg="create index")
            self.redis_client.ft(self.index_name).create_index(schema)
        except Exception as error:
            logging.info(msg="index already exists")
            pass

        self.redis_client.ft(self.index_name).config_set("default_dialect", "2")

    def load(self, documents: List[Document]):
        logging.info(msg="Load vectors")
        self.create_schema_redis()

        for document in documents:
            record_key = self.generate_record_key(document.__getattribute__(self.TITLE_FIELD_NAME))
            document[self.VECTOR_FIELD_NAME] = self.embedding_document(document)
            self.redis_client.hset(record_key,
                                   mapping={
                                       self.VECTOR_FIELD_NAME: document[self.VECTOR_FIELD_NAME].tobytes(),
                                       self.TITLE_FIELD_NAME: document[self.TITLE_FIELD_NAME],
                                       self.CONTENT_FIELD_NAME: document[self.CONTENT_FIELD_NAME]
                                   })

    def find_similarity_documents(self, question: str, threshold: float):
        docs: List[Document] = []

        image_vector = self.embedding(text=question)

        if image_vector is not None and threshold is not None:
            radius = 1 - threshold
            q = Query(
                f'@{self.VECTOR_FIELD_NAME}:[VECTOR_RANGE {radius} $vec_param]=>{{$yield_distance_as: dist}}').sort_by(
                f'dist')
            res = self.redis_client.ft(self.index_name).search(q,
                                                               query_params={'vec_param': image_vector.tobytes()})
            if len(res.docs) > 0:
                docs = list(map(self.convert_doc, docs))
        else:
            logging.error(image_vector, threshold)

        return docs

    def embedding(self, text: str) -> np.array:
        return self.embedding_model.encode(text)

    def convert_doc(self, doc: Document):
        dist = float(doc["dist"]) if float(doc["dist"]) > 1e-5 else 0
        return {"dist": 1 - dist, [self.TITLE_FIELD_NAME]: doc[self.TITLE_FIELD_NAME],
                [self.CONTENT_FIELD_NAME]: doc[self.CONTENT_FIELD_NAME]}

    def generate_record_key(self, title: str):
        return f"{self.prefix}:{title}"

    def embedding_document(self, document: Document) -> np.array:
        text = document[self.TITLE_FIELD_NAME] + document[self.CONTENT_FIELD_NAME]
        return self.embedding(text=text)
