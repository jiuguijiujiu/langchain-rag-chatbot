# 🤖 基于 LangChain 与通义千问的 RAG 智能客服系统

## 📖 项目简介
本项目是一个基于 **RAG（检索增强生成）** 架构的智能客服问答系统。项目分为**离线知识库构建**与**在线智能问答**两大模块。通过引入外部私有知识库，有效解决了大语言模型（LLM）在垂直领域存在的“幻觉”问题，并支持多轮对话记忆与流式打字机输出。

## 🛠️ 核心技术栈
*   **大语言模型**：通义千问 (Qwen) API
*   **开发框架**：LangChain (LCEL 表达式)
*   **向量数据库**：Chroma DB
*   **Embedding 模型**：DashScope Embeddings (text-embedding-v4)
*   **前端界面**：Streamlit
*   **核心特性**：RAG 架构、MD5 知识去重、多轮对话记忆 (Memory)、流式输出 (Generator)

## ✨ 项目亮点 (Highlight)
1.  **离线知识库自动化构建**：支持 TXT 文件上传，自动完成文本解析、MD5 查重、文本切分 (TextSplitter) 与向量化入库。
2.  **真正的流式输出**：摒弃了原教程中阻塞线程的“假流式 (time.sleep)”，利用 Python 生成器 (`yield`) 配合 Streamlit `write_stream`，实现了丝滑的 Token 级打字机效果。
3.  **自定义持久化记忆**：重写了 `BaseChatMessageHistory`，基于 JSON 文件实现了多轮对话历史记录的本地化持久存储，避免了页面刷新导致记忆丢失。
4.  **元数据溯源**：在向量入库时注入 `source` 与 `create_time` 等元数据，支持在回答中追溯知识来源。

## 📂 项目结构
```text
RAG_Project/
├── data                      # 数据
├── upload_file_app.py        # 知识库上传网页 (Streamlit)
├── knowledge_base.py         # 核心建库逻辑 (MD5去重、切分、入库)
├── qa_app.py                 # 智能客服对话网页 (Streamlit)
├── rag.py                    # RAG 核心链路 (LCEL 拼装)
├── file_store_history.py     # 历史记录持久化存储
├── config.py                 # 全局配置文件
├── requirements.txt          # 依赖包
└── README.md                 # 项目说明文档
```

## 🚀 快速开始
### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
配置环境变量，填入你的 DashScope API Key：
```bash
DASHSCOPE_API_KEY="你的API_KEY"
```

### 3. 运行项目
**步骤一：启动知识库上传服务**
```bash
streamlit run upload_file_app.py
```
上传 `.txt` 文件，等待知识库构建完成。

**步骤二：启动智能客服服务**
```bash
streamlit run qa_app.py
```
在聊天框中进行提问，体验 RAG 问答与流式输出。

## 🔧 待优化项 (Future Work)
*   [ ] 引入 FastAPI 重构后端，实现前后端分离。