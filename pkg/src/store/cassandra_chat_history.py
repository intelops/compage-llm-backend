import uuid
from langchain.memory import CassandraChatMessageHistory

from pkg.src.config.env_config import settings
from pkg.src.constants.cassandra_store import TABLE_NAME

from cassandra.cluster import Session

settings = settings()


def chat_history_store(username: str, session: Session):
    memory_history = CassandraChatMessageHistory(
        session_id=username + str(uuid.uuid4()),
        session=session,
        keyspace=settings.ASTRADB_KEYSPACE,
        table_name=TABLE_NAME,
    )
    return memory_history

