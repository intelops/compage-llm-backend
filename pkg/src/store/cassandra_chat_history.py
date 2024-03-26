"""
This module provides a function to store chat history in Cassandra.
"""

import uuid

from cassandra.cluster import Session  # pylint: disable = no-name-in-module
from langchain.memory import CassandraChatMessageHistory


def chat_history_store(session: Session):
    """
    A function to get the cluster and establish a session to a specific keyspace.
    """
    memory_history = CassandraChatMessageHistory(
        session_id=str(uuid.uuid4()),
        session=session,
        keyspace="backend_llm",
        table_name="chat_history",
    )
    return memory_history
