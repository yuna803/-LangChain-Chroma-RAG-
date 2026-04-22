# -LangChain-Chroma-RAG-
# RAG-Chat：基于 LangChain 的多轮知识增强型智能客服系统

> **项目简介**  
> 一个面向企业场景的智能客服系统，基于 **RAG（检索增强生成）** 架构，结合大语言模型与本地向量知识库，支持多轮对话历史记忆、流式响应与知识库动态更新。前端采用 Streamlit 快速搭建，后端以 LangChain 编排核心链路，使用 Chroma 向量数据库存储知识片段。

---

## 🧠 核心功能

- **知识库管理**  
  - 上传 TXT 文档，自动分块、向量化并存入 Chroma 向量库  
  - MD5 去重机制，避免重复处理同一文件  
  - 支持自定义分块策略（大小、重叠、分隔符）

- **智能问答**  
  - 基于检索到的相关文档片段生成回答，降低大模型幻觉  
  - 多轮对话记忆，通过本地文件持久化历史记录  
  - 流式输出回答内容，提升用户体验

- **技术栈**  
  - LLM：通义千问 `qwen3-max`  
  - Embedding：`text-embedding-v4`  
  - 框架：LangChain、Streamlit  
  - 向量库：Chroma  
  - 文本分割：RecursiveCharacterTextSplitter  

---

## 📁 项目结构
