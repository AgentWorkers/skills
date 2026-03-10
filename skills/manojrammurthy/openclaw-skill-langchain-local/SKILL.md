# LangChain Local — 一个基于 Ollama 的离线 AI 工具

您可以使用 Ollama 和 phi4-mini（或其他本地模型）在本地运行 LangChain 流程。无需 API 密钥，完全离线，且不依赖云端服务。

## 必备条件
- 已安装并运行 Ollama（通过 `ollama serve` 命令启动）
- 已下载 phi4-mini 模型（通过 `ollama pull phi4-mini` 命令）
- 安装以下 Python 包：`pip install langchain langchain-ollama langchain-community`

## 运行模式
- `coding`：用于生成 Python/Django 代码（计算量较小，但结果较为精确）
- `devops`：用于执行 Linux/Nginx/Docker 命令
- `chat`：用于进行日常对话
- `rag`：基于文档的问答系统（能够理解上下文）

## 使用示例
- “让 LangChain Local 生成一个 Django REST API 视图”
- “在 devops 模式下使用 LangChain Local 查看磁盘使用情况”
- “启动 LangChain Local 的聊天模式，询问什么是 RAG（Document-Aided Generation）”
- “使用 LangChain Local 的 coding 模式编写 PostgreSQL 备份脚本”

## 使用方法
执行命令：`python3 ~/.openclaw/skills/langchain-local/main.py`

## 参数
- `mode`：`coding` | `devops` | `chat` | `rag`（默认值：`coding`）
- `query`：您的问题或指令

## 开发者
Manoj — [GitHub 仓库链接](https://github.com/manoj)