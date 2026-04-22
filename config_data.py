
md5_path = "./md5.text"
#chroma
# 向量库参数     knowledge_base
collection_name="rag"    # 向量库名称
persist_directory="./chroma_db"     # 向量库保存路径

#spliter
# 文本分割参数
chunk_size=1000
chunk_overlap=100
separator=["\n", "。", "？", "！", "；", "，", "、", "：", "（", "）", "《", "》", "「", "」", "『", "』", "【", "】", "、", "、", "、", "、", "、", "、", "、", "、", "、", "、", "、", "、", "、", "、"," "]
max_split_chat_number=10

#vector_store
similarity_threshold = 1   #检索返回匹配的文档数量

#   rag
embedding_model_name="text-embedding-v4"
chat_model_name="qwen3-max"


#file_history_story
chat_history_path="./chat_history"


#app_qa
session_config = {
    "configurable": {
        "session_id": "user_001"  # 可以改为从 st.session_state 获取，例如 st.session_state.get("session_id", "default")
    }
}