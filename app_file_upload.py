"""
基于streamlit完成web网页上传
"""
import streamlit as st
import time
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,    # False表示仅接受一个文件的上传
)
if "counter" not in st.session_state:
    """页面刷新st.session_state不会更着刷新"""
    st.session_state["counter"] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024    # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")
    # 获取文件内容
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中。。。"):
        time.sleep(1)
        result=st.session_state["counter"].upload_by_str(text, file_name)  #上传文件
        st.write(result)

    # st.write(text)
    # st.session_state["counter"] += 1
# print(f'上传了 {st.session_state["counter"]} 个文件')