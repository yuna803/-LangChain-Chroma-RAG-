import os, json
from typing import Sequence
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
import config_data as config
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

def get_history(session_id):
    """获取会话历史记录"""
    file_path = os.path.join(config.chat_history_path, session_id)
    os.makedirs(config.chat_history_path, exist_ok=True)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            messages_data = json.load(f)
            return messages_from_dict(messages_data)
    except FileNotFoundError:
        return []

class FileChatMessageHistory(BaseChatMessageHistory):
    """基于文件的会话历史记录"""
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(self.storage_path, exist_ok=True)   # 确保目录存在

    @property
    def messages(self) -> list[BaseMessage]:
        """获取所有消息"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                # messages_from_dict：[字典、字典...]  -> [消息、消息...]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """添加消息"""
        all_messages = self.messages + list(messages)
        with open(self.file_path, "w", encoding="utf-8") as f:
            # message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
            json.dump([message_to_dict(m) for m in all_messages], f, ensure_ascii=False, indent=2)

    def clear(self) -> None:
        """清空所有消息"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


model = ChatTongyi(model="qwen3-max")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回应用户问题。"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

str_parser = StrOutputParser()

base_chain = prompt |  model | str_parser

store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(session_id, "./chat_history")
    return store[session_id]


conversation_chain = RunnableWithMessageHistory(
    base_chain,     # 被增强的原有chain
    get_history,    # 通过会话id获取FileChatMessageHistory类对象
    input_messages_key="input",             # 输入消息的key
    history_messages_key="chat_history"     # 历史消息的key
)
