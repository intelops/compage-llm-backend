from datetime import datetime
from pkg.src.config.env_config import settings
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

import uuid


settings = settings()


class OpenAI_Token(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    id = columns.UUID(primary_key=True, partition_key=True, default=uuid.uuid1)
    api_key = columns.Text()
    username = columns.Text()
    created_at = columns.DateTime(default=datetime.utcnow())
    updated_at = columns.DateTime(default=datetime.utcnow())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"OpenAI_Token(id={self.id}, api_key={self.api_key}, username={self.username}, created_at={self.created_at})"

    @staticmethod
    def create_openai_apikey(api_key, username):
        result = OpenAI_Token.objects.create(api_key=api_key, username=username)
        result.save()
        return result
