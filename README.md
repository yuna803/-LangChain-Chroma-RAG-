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
RAG-Chat/
├── app_qa.py # Streamlit 智能问答界面
├── app_file_upload.py # Streamlit 知识库上传界面
├── rag.py # RAG 核心服务类（检索+生成链）
├── vector_stores.py # Chroma 向量库封装与检索器
├── knowledge_base.py # 知识库文本处理与入库逻辑
├── file_history_store.py # 对话历史本地文件存储实现
├── config_data.py # 全局配置（模型名、路径、参数等）
├── requirements.txt # Python 依赖清单
└── README.md # 项目说明文档


## 🚀 快速开始

### 1. 环境准备

- Python 3.10+  
- 安装依赖：

```bash
pip install -r requirements.txt
2. 配置参数
在 config_data.py 中修改必要配置（如模型名称、API Key 环境变量等）。
建议通过环境变量设置通义千问的 API Key：

bash
export DASHSCOPE_API_KEY="your-api-key"
3. 启动应用
启动知识库上传界面
bash
streamlit run app_file_upload.py
启动智能问答界面
bash
streamlit run app_qa.py
两个界面可同时运行，上传知识后即可在问答界面测试。

⚙️ 系统架构
text
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Streamlit UI  │ ───▶ │   RagService    │ ───▶ │  VectorStore    │
│  (app_qa.py)    │      │    (rag.py)     │      │ (Chroma 检索)   │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │   LLM (Tongyi)  │
                        └─────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │  History Store  │
                        │  (本地 JSON)    │
                        └─────────────────┘
处理流程

用户输入问题 → 前端捕获并传递给 RagService.chat

从 Chroma 检索相关文档片段，格式化后注入 Prompt

结合历史对话记录（通过 RunnableWithMessageHistory 自动加载）

大模型生成回答，流式返回前端展示

新对话内容自动追加到本地历史文件

🔧 关键技术实现
多轮对话记忆
自定义 FileChatMessageHistory 类，将 LangChain 的 BaseMessage 序列化为 JSON 存储于本地文件，每次会话通过 session_id 读取对应记录。

RAG 链构建
使用 RunnablePassthrough.assign 动态注入检索结果，结合 RunnableWithMessageHistory 包装，实现无侵入的历史记录集成。

流式响应
调用 chat.stream() 获取生成器，通过 Streamlit 的 write_stream 逐步渲染输出，模拟真实对话效果。

知识库去重
计算上传文本的 MD5 值，与本地记录比对，已存在则跳过入库，避免重复处理。

📦 依赖清单（requirements.txt）
text
langchain
langchain-community
langchain-chroma
dashscope
streamlit
chromadb
📌 注意事项
请确保通义千问 API Key 有效，否则模型调用会失败。

首次运行时，向量库目录 (./chroma_db) 和对话历史目录 (./chat_history) 会自动创建。

上传的 TXT 文件请使用 UTF-8 编码，否则可能解码异常。

向量检索返回数量 similarity_threshold 在配置中可调，建议根据知识库规模设置为 1~3。

✨ 后续优化方向
支持 PDF、Word 等多格式文档上传

增加用户认证与会话隔离

引入检索重排序（Rerank）提升相关性

提供 Docker 一键部署方案

👨‍💻 作者
夏生

项目时间：2026.04

项目用途：实习项目 / 个人技术实践

📄 许可证
本项目仅供学习与展示使用，未经授权不得用于商业用途。

