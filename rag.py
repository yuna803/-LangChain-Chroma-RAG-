# from xml.dom.minidom import Document
from operator import itemgetter
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document


class RagService(object):
    """
    RAG服务
    """
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template =  ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，"
                           "简洁和专业的回答用户的问题。参考资料：{context}"),
                ("system","并且根据我提供的用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("human", "请回答用户提问:{input}")
            ]
        )

        self.chat_model = ChatTongyi(
            model=config.chat_model_name,
        )

        self.chat = self.__get_chain()

    def __get_chain(self):
        """获取最终 的执行链"""
        retriever=self.vector_service.get_retriever() # 获取向量库检索器

        def format_document(docs : list[Document]):
            """
            self.prompt_template:提示词
            self.chat_model:模型
            StrOutputParser():解析器
            """
            if not docs:
                return "无相关参考材料"
            formatted_str=""
            for doc in docs:
                formatted_str+=f"文档片段：{doc.page_content}\n 文档元数据：{doc.metadata}\n\n"
            return formatted_str

        rag_chain = (
                RunnablePassthrough.assign(
                    context=itemgetter("input") | retriever | format_document
                )
                | self.prompt_template
                | self.chat_model
                | StrOutputParser()
        )

        conversation_chain=RunnableWithMessageHistory(
            rag_chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return conversation_chain


if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    res = RagService().chat.invoke(
        {"input": "我的身高173cm"},
        session_config
    )
    print(res)