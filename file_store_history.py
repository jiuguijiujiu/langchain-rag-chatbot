from langchain_core.chat_history import BaseChatMessageHistory
import os
from typing import Sequence
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict
import json
import config

def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path=config.history_path)

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages:Sequence[BaseMessage]):
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages = messages_to_dict(all_messages)
        with open(file=self.file_path, mode='w', encoding='utf-8') as f:
            json.dump(obj=new_messages, fp=f, ensure_ascii=False)

    @property
    def messages(self)->list[BaseMessage]:
        try:
            with open(file=self.file_path, mode='r', encoding='utf-8') as f:
                messages = json.load(fp=f)
                return messages_from_dict(messages)
        except FileNotFoundError:
            return []

    def clear(self):
        with open(file=self.file_path, mode='w', encoding='utf-8') as f:
            json.dump(obj=[], fp=f)