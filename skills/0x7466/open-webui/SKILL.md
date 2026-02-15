---
name: open-webui
description: 完成 Open WebUI API 的集成，以实现 LLM 模型的管理、聊天功能、Ollama 代理操作、文件上传、知识库（RAG）管理、图像生成、音频处理等功能。在通过 REST API 与 Open WebUI 实例交互时，可以使用该技能：列出模型、与 LLM 进行聊天、上传文件以用于知识库（RAG）建设、管理知识库内容，或通过 Open WebUI 代理执行 Ollama 命令。需要使用 `OPENWEBUI_URL` 和 `OPENWEBUI_TOKEN` 环境变量或显式参数。
compatibility: Requires Python 3.8+ with requests library, or curl. Works with any Open WebUI instance (local or remote). Internet access required for external instances.
---

# Open WebUI API 技能

本技能提供了对 Open WebUI 的完整 API 集成支持，Open WebUI 是一个统一的接口，可用于调用包括 Ollama、OpenAI 在内的多种大型语言模型（LLMs）。

## 使用场景

**当用户需要执行以下操作时，请激活此技能：**
- 列出其 Open WebUI 实例中可用的模型
- 通过 Open WebUI 将聊天结果发送给模型
- 上传文件以用于检索增强生成（RAG，Retrieval Augmented Generation）
- 管理知识库并向其中添加文件
- 使用 Ollama 代理端点（生成、嵌入或拉取模型）
- 通过 Open WebUI 生成图像或处理音频
- 查查 Ollama 的状态或管理模型（加载、卸载、删除）
- 创建或管理处理流程

**不建议激活此技能的场景：**
- 安装或配置 Open WebUI 服务器本身（请使用系统管理技能）
- 有关 Open WebUI 的一般性问题（请参考通用知识）
- 解决 Open WebUI 服务器的问题（请参考故障排除指南）
- 与 Open WebUI API 无关的本地文件操作

## 先决条件

### 环境变量（推荐设置）

```bash
export OPENWEBUI_URL="http://localhost:3000"  # Your Open WebUI instance URL
export OPENWEBUI_TOKEN="your-api-key-here"    # From Settings > Account in Open WebUI
```

### 认证

- 需要使用 bearer token 进行认证
- 从 Open WebUI 获取 token：**设置 > 账户**
- 或者：对于高级用例，可以使用 JWT token

## 激活触发条件

**应激活此技能的示例请求：**
1. “列出我 Open WebUI 中所有可用的模型”
2. “通过 Open WebUI 向 llama3.2 发送聊天结果，提示为‘解释量子计算’”
3. “将 /path/to/document.pdf 上传到 Open WebUI 的知识库”
4. “在 Open WebUI 中创建一个名为‘Research Papers’的新知识库”
5. “使用 nomic-embed-text 模型生成‘Open WebUI 很棒’的嵌入内容”
6. “通过 Open WebUI Ollama 代理拉取 llama3.2 模型”
7. “从我的 Open WebUI 实例中获取 Ollama 的状态”
8. “在我的 Open WebUI 中与 gpt-4 进行聊天，并启用‘docs’知识库中的 RAG 功能”
9. “使用 Open WebUI 生成一张‘未来城市’的图像”
10. “从 Open WebUI Ollama 中删除旧模型”

**不应激活此技能的示例请求：**
1. “如何安装 Open WebUI？”（安装/管理相关问题）
2. “Open WebUI 是什么？”（通用知识问题）
3. “配置 Open WebUI 环境变量”（服务器配置相关问题）
4. “排查 Open WebUI 服务器无法启动的原因”（服务器故障排除相关问题）
5. “将 Open WebUI 与其他用户界面进行比较”（一般性比较问题）

## 工作流程

### 1. 配置检查

- 确保 `OPENWEBUI_URL` 和 `OPENWEBUI_TOKEN` 已设置
- 验证 URL 格式（http/https）
- 使用 GET /api/models 或 /ollama/api/tags 测试连接

### 2. 操作执行

可以使用 CLI 工具或直接进行 API 调用：

```bash
# Using the CLI tool (recommended)
python3 scripts/openwebui-cli.py --help
python3 scripts/openwebui-cli.py models list
python3 scripts/openwebui-cli.py chat --model llama3.2 --message "Hello"

# Using curl (alternative)
curl -H "Authorization: Bearer $OPENWEBUI_TOKEN" \
  "$OPENWEBUI_URL/api/models"
```

### 3. 响应处理

- HTTP 200：成功 - 解析并呈现 JSON 响应
- HTTP 401：认证失败 - 检查 token
- HTTP 404：端点/模型未找到
- HTTP 422：验证错误 - 检查请求参数

## 核心 API 端点

### 聊天与聊天结果

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/chat/completions` | POST | 与 OpenAI 兼容的聊天结果 |
| `/api/models` | GET | 列出所有可用模型 |
| `/ollama/api/chat` | POST | 原生的 Ollama 聊天结果 |
| `/ollama/api/generate` | POST | 使用 Ollama 生成文本

### Ollama 代理

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/ollama/api/tags` | GET | 列出 Ollama 模型 |
| `/ollama/api/pull` | POST | 拉取/下载模型 |
| `/ollama/api/delete` | DELETE | 删除模型 |
| `/ollama/api/embed` | POST | 生成嵌入内容 |
| `/ollama/api/ps` | GET | 列出已加载的模型 |

### 检索增强生成（RAG）与知识库

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/v1/files/` | POST | 上传文件以用于 RAG |
| `/api/v1/files/{id}/process/status` | GET | 检查文件处理状态 |
| `/api/v1/knowledge/` | GET/POST | 列出/创建知识库 |
| `/api/v1/knowledge/{id}/file/add` | POST | 向知识库中添加文件 |

### 图像与音频

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/v1/images/generations` | POST | 生成图像 |
| `/api/v1/audio/speech` | POST | 文本转语音 |
| `/api/v1/audio/transcriptions` | POST | 语音转文本 |

## 安全性与注意事项

### 必须确认的操作

在执行以下操作前，请务必确认：
- **删除模型**（`DELETE /ollama/api/delete`）——操作不可逆
- **拉取大型模型**——可能需要较长时间或大量带宽
- **删除知识库**——存在数据丢失的风险
- **上传敏感文件**——需注意隐私问题

### 数据保护与安全措施

- **切勿记录完整的 API token**——将其截断为 `sk-...XXXX` 格式
- **对文件路径进行清理**——上传前验证文件是否存在
- **验证 URL**——确保外部链接使用 HTTPS
- **优雅地处理错误**——不要泄露包含 token 的堆栈跟踪信息

### 工作区安全

- 文件默认上传到工作区目录
- 在访问工作区外的文件之前请先确认
- 无需使用 sudo 或 root 权限（纯 API 客户端）

## 示例

### 列出模型

```bash
python3 scripts/openwebui-cli.py models list
```

### 聊天结果

```bash
python3 scripts/openwebui-cli.py chat \
  --model llama3.2 \
  --message "Explain the benefits of RAG" \
  --stream
```

### 上传文件以用于 RAG

```bash
python3 scripts/openwebui-cli.py files upload \
  --file /path/to/document.pdf \
  --process
```

### 向知识库添加文件

```bash
python3 scripts/openwebui-cli.py knowledge add-file \
  --collection-id "research-papers" \
  --file-id "doc-123-uuid"
```

### 生成嵌入内容（Ollama）

```bash
python3 scripts/openwebui-cli.py ollama embed \
  --model nomic-embed-text \
  --input "Open WebUI is great for LLM management"
```

### 拉取模型（需确认）

```bash
python3 scripts/openwebui-cli.py ollama pull \
  --model llama3.2:70b
# Agent must confirm: "This will download ~40GB. Proceed? [y/N]"
```

### 查查 Ollama 状态

```bash
python3 scripts/openwebui-cli.py ollama status
```

## 错误处理

| 错误代码 | 原因 | 解决方案 |
|-------|-------|----------|
| 401 未经授权 | Token 无效或缺失 | 重新验证 OPENWEBUI_TOKEN |
| 404 未找到 | 模型/端点不存在 | 检查模型名称的拼写 |
| 422 验证错误 | 参数无效 | 检查请求参数的格式 |
| 400 错误请求 | 文件仍在处理中 | 等待处理完成 |
| 连接被拒绝 | URL 错误 | 重新验证 OPENWEBUI_URL |

## 边缘情况

### 文件处理竞争条件

上传用于 RAG 的文件是异步处理的。在将文件添加到知识库之前，请执行以下步骤：
1. 上传文件 → 获取文件 ID
2. 轮询 `/api/v1/files/{id}/process/status`，直到状态显示为“completed”
3. 然后将其添加到知识库中

### 大型模型下载

拉取大型模型（例如参数量达到 70B）可能需要较长时间。请务必：
- 在开始操作前征求用户同意
- 如果可能的话，显示处理进度
- 允许用户取消操作

### 流式响应

聊天结果支持流式输出。可以使用 `--stream` 标志实现实时输出，或收集完整响应以供非流式使用。

## CLI 工具参考

随附的 CLI 工具（`scripts/openwebui-cli.py`）提供以下功能：
- 从环境变量自动进行认证
- 结构化的 JSON 输出（支持自定义格式）
- 所有命令的内置帮助信息
- 对错误进行友好的错误处理
- 对长时间运行的操作提供进度显示

运行 `python3 scripts/openwebui-cli.py --help` 可查看完整的使用说明。