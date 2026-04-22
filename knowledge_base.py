"""
知识库的创建与上传
"""
import datetime
import os

import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def check_md5(md5_str):
    """检查传入的md5是否被处理过  存在True"""
    if not os.path.exists(config.md5_path):
        # 文件不存在则创建md5文件
        open(config.md5_path, "w",encoding="utf-8").close()
        return  False
    else:
        # 文件存在则读取
        for line in open(config.md5_path, "r",encoding="utf-8").readlines():
            line = line.strip() # 去除换行符
            if line == md5_str:
                return True
        return  False


def save_md5(str_md5):
    """将传入的字符串转换为md5"""
    with open(config.md5_path, "a",encoding="utf-8") as f:
        f.write(str_md5 + "\n")


def get_string_md5(input_str,encod="utf-8"):
    """将传入的字符串转换为md5"""
    # 将字符串转换为str_bytes
    str_bytes=input_str.encode(encoding= encod)
    md5_obj=hashlib.md5()       # 创建md5对象
    md5_obj.update(str_bytes)   # 更新md5对象
    md5_hex=md5_obj.hexdigest() # 获取md5
    return md5_hex


class KnowledgeBaseService(object):

    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)                    # 创建向量库存放目录
        self.chroma=Chroma(
            collection_name =config.collection_name,                            # 向量库名称
            embedding_function = DashScopeEmbeddings(model="text-embedding-v4"),# 模型
            persist_directory = config.persist_directory                        # 向量库存放地址
        )    #向量存储的实例chroma向量库对象

        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,         # 分块大小
            chunk_overlap = config.chunk_overlap,   # 分块重叠
            separators=config.separator,            # 分块分隔符
            length_function=len,                    # 长度函数
        )   #文本分割器实例对象

    def upload_by_str(self,data,file_name):
        """上传字符串"""
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]文件已处理过已在知识库中"
        if len(data)>config.max_split_chat_number:
            knowledge_chunks: list[str]=self.spliter.split_text(data)   # 长度大于设定的量则分块
        else:
            knowledge_chunks=[data]                                     # 长度小于设定的量则不分块

        metadata={
            "source": file_name,
            "create_time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"夏生"
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[ metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)
        return "[成功]文件已处理成功已添加到知识库中"

#
# if __name__ == "__main__":
#     # r1 =get_string_md5("蔡徐姬")
#     # r2=get_string_md5("蔡徐姬")
#     # r3=get_string_md5("蔡徐坤")
#     # print(r1,r2,r3)
#     # save_md5("17c0fee819b9c79696a382f9634dbd87")
#     # print(check_md5("17c0fee819b9c79696a382f9634dbd87"))
#     service = knowledgeBaseService()
#     r = service.upload_by_str("蔡徐姬 ", "testfile")
#     print(r)