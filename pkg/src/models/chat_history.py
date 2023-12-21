import uuid
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns, functions
from cassandra.cqlengine.query import UpdateStatement

from cassandra.query import SimpleStatement
from typing import Dict, Any

from pkg.src.config.env_config import settings

settings = settings()


class Chat_History(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    id = columns.UUID(primary_key=True, partition_key=True, default=uuid.uuid1)
    main_prompt = columns.Text()
    history = columns.Map(
        columns.UUID(default=uuid.uuid1), columns.Map(columns.Text(), columns.Text())
    )
    created_at = columns.DateTime()
    updated_at = columns.DateTime()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Chat_History(id={self.id}, main_prompt={self.main_prompt}, history={self.history}, created_at={self.created_at}), updated_at={self.updated_at}"

    @staticmethod
    def store_history_entry(main_prompt, prompt, language, code: Dict[str, Any]):
        # Retrieve the current history or create a new one if it doesn't exist
        current_history = Chat_History.objects.filter(main_prompt=main_prompt).first()
        if current_history is None:
            current_history = Chat_History.create(main_prompt=main_prompt, history={})

        # Create a new history entry
        history_entry = {
            uuid.uuid1(): {"prompt": prompt, "language": language, "code": code}
        }

        # Update the history map with the new entry
        current_history.history.update(history_entry)

        # Update the created_at and updated_at fields
        current_history.created_at = functions.now()
        current_history.updated_at = functions.now()

        # Save the existing record in the database
        current_history.save()

        return current_history
