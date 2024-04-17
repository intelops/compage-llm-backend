"""
This module provides a class to store chat history in Cassandra.
"""

import uuid
from datetime import datetime
from typing import Any, Dict

import pytz
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from pkg.src.config.database import KEYSPACE


class ChatHistory(Model):
    """
    This class represents the chat history table in the Cassandra database.
    """

    __keyspace__ = KEYSPACE
    __table_name__ = "chat_history"
    id = columns.UUID(primary_key=True, partition_key=True, default=uuid.uuid1)
    main_prompt = columns.Text()
    history = columns.Map(columns.UUID(default=uuid.uuid1), columns.Map(columns.Text(), columns.Text()))
    created_at = columns.DateTime()
    updated_at = columns.DateTime()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Chat_History(id={self.id}, main_prompt={self.main_prompt}, history={self.history}, created_at={self.created_at}), updated_at={self.updated_at}"

    @staticmethod
    def store_history_entry(main_prompt: str, prompt: str, language: str, code: Dict[str, Any]) -> "ChatHistory":
        """
        Stores the chat history entry in the Cassandra database.
        """
        current_history, _ = ChatHistory.objects.get_or_create(main_prompt=main_prompt, defaults={"history": {}})
        history_entry = {str(uuid.uuid1()): {"prompt": prompt, "language": language, "code": code}}
        current_history.history.update(history_entry)
        current_history.created_at = datetime.now(pytz.utc)
        current_history.updated_at = datetime.now(pytz.utc)
        current_history.save()
        return current_history
