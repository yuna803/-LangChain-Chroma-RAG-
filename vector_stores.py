from langchain_chroma import Chroma
import config_data as config

"""向量数据库 的索引"""

class VectorStoreService(object):

    def __init__(self,embedding):
        self.embeding=embedding
        self.vector_store=Chroma(
            collection_name=config.collection_name,         # 向量库名称
            embedding_function=self.embeding,               # 模型
            persist_directory=config.persist_directory      # 向量库存放地址
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kargs={"k":config.similarity_threshold})






