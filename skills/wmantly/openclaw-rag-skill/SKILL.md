---
name: rag
description: OpenClaw的完整RAG（Retrieval-Augmented Generation，检索增强生成）系统：该系统将聊天记录、工作区代码、文档以及技能信息索引到本地的ChromaDB数据库中，以实现语义搜索。用户可以即时查找过去的解决方案、代码模式和决策记录。系统使用本地预训练的嵌入模型（MiniLM-L6-v2），无需任何API密钥。它还会自动从`~/.openclaw/agents/main/sessions`和工作区文件中获取并更新知识库内容。
---

# OpenClaw RAG知识系统

**OpenClaw的检索增强生成功能——支持语义理解，可搜索聊天记录、代码、文档和技能**

## 概述

该功能为OpenClaw提供了一个完整的检索增强生成（RAG）系统。它能够索引您的整个知识库（包括聊天记录、工作区代码和技能文档），并支持跨所有内容进行语义搜索。

**主要特性：**
- 🧠 支持对所有聊天记录和代码进行语义搜索
- 📚 自动管理知识库
- 🔍 可即时查找过去的解决方案、代码模式和决策记录
- 💾 采用本地ChromaDB存储（无需API密钥）
- 🚀 支持自动AI集成——透明地检索相关上下文

## 安装

### 先决条件

- Python 3.7及以上版本
- OpenClaw工作区

### 设置

```bash
# Navigate to your OpenClaw workspace
cd ~/.openclaw/workspace/skills/rag-openclaw

# Install ChromaDB (one-time)
pip3 install --user chromadb

# That's it!
```

## 快速入门

### 1. 索引您的知识库

```bash
# Index all chat history
python3 ingest_sessions.py

# Index workspace code and docs
python3 ingest_docs.py workspace

# Index skill documentation
python3 ingest_docs.py skills
```

### 2. 搜索知识库

```bash
# Interactive search mode
python3 rag_query.py -i

# Quick search
python3 rag_query.py "how to send SMS via voip.ms"

# Search by type
python3 rag_query.py "porkbun DNS" --type skill
python3 rag_query.py "chromedriver" --type workspace
python3 rag_query.py "Reddit automation" --type session
```

### 3. 查看统计信息

```bash
# See what's indexed
python3 rag_manage.py stats
```

## 使用示例

### 查找过去的解决方案

遇到问题了吗？可以搜索您之前是如何解决的：

```bash
python3 rag_query.py "cloudflare bypass selenium"
python3 rag_query.py "voip.ms SMS configuration"
python3 rag_query.py "porkbun update DNS record"
```

### 在代码库中搜索

查找特定的代码或文档：

```bash
python3 rag_query.py --type workspace "unifi gateway API"
python3 rag_query.py --type workspace "SMS client"
```

### 快速参考

无需翻阅文件即可访问技能文档：

```bash
python3 rag_query.py --type skill "how to monitor UniFi"
python3 rag_query.py --type skill "Porkbun tool usage"
```

### 程序化使用

您可以在Python脚本或OpenClaw会话中直接使用该系统：

```python
import sys
sys.path.insert(0, '/home/william/.openclaw/workspace/skills/rag-openclaw')
from rag_query_wrapper import search_knowledge, format_for_ai

# Search and get structured results
results = search_knowledge("Reddit account automation")
print(f"Found {results['count']} relevant items")

# Format for AI consumption
context = format_for_ai(results)
print(context)
```

## 文件参考

| 文件 | 用途 |
|------|---------|
| `rag_system.py` | 核心RAG类（ChromaDB封装） |
| `ingest_sessions.py` | 索引聊天记录 |
| `ingest_docs.py` | 索引工作区文件和技能文档 |
| `rag_query.py` | 搜索接口（命令行界面和交互式界面） |
| `rag_manage.py` | 文档管理（统计、删除、重置） |
| `rag_query_wrapper.py` | 用于程序化使用的简单Python API |
| `README.md` | 完整的文档说明 |

## 工作原理

### 索引

**聊天记录：**
- 读取`~/.openclaw/agents/main/sessions/*.jsonl`文件
- 处理OpenClaw的事件格式（会话元数据、消息、工具调用）
- 将消息分块处理（每块20条消息，每块之间有5条消息的重叠）
- 提取并格式化用户的思考过程、工具调用结果

**工作区文件：**
- 扫描`.py`、`.js`、`.ts`、`.md`、`.json`、`.yaml`、`.sh`、`.html`、`.css`文件
- 跳过大于1MB的文件和二进制文件
- 将长文档分块处理以提升检索效率

**技能文档：**
- 索引所有`SKILL.md`文件
- 按技能名称组织以便于查找

### 搜索

ChromaDB使用`all-MiniLM-L6-v2`嵌入模型将文本转换为向量。相似的含义会被聚类在一起，从而实现基于“含义”而非“关键词”的语义搜索。

### 自动集成

当AI给出响应时，它会自动：
1. 在知识库中搜索相关上下文
2. 检索过去的对话记录、代码或文档
3. 将这些上下文包含在响应中

这一过程是透明的——AI会“记住”您之前的操作。

## 管理

### 查看统计信息

```bash
python3 rag_manage.py stats
```

### 删除文档

```bash
# Delete all sessions
python3 rag_manage.py delete --by-type session

# Delete specific file
python3 rag_manage.py delete --by-source "scripts/voipms_sms_client.py"

# Reset entire collection
python3 rag_manage.py reset
```

### 手动添加文档

```bash
python3 rag_manage.py add \
  --text "API endpoint: https://api.example.com/endpoint" \
  --source "api-docs:example.com" \
  --type "manual"
```

## 配置

### 自定义会话目录

```bash
python3 ingest_sessions.py --sessions-dir /path/to/sessions
```

### 分块大小控制

```bash
python3 ingest_sessions.py --chunk-size 30 --chunk-overlap 10
```

### 自定义收集规则

```python
from rag_system import RAGSystem
rag = RAGSystem(collection_name="my_knowledge")
```

## 数据类型

| 类型 | 来源格式 | 描述 |
|------|--------------|-------------|
| `session` | `session:{key}` | 聊天记录 |
| `workspace` | `relative/path/to/file` | 代码、配置文件、文档 |
| `skill` | `skill:{name}` | 技能文档 |
| `memory` | `MEMORY.md` | 长期存储的条目 |
| `manual` | `{custom}` | 手动添加的文档 |
| `api` | `api-docs:{name}` | API文档 |

## 性能

- **嵌入模型**：`all-MiniLM-L6-v2`（79MB，本地缓存）
- **存储空间**：每1,000份文档约占用100MB
- **索引速度**：约每分钟索引1,000份文档
- **搜索速度**：首次查询后小于100毫秒

## 故障排除

### 未找到结果

```bash
# Check what's indexed
python3 rag_manage.py stats

# Try broader query
python3 rag_query.py "SMS"  # instead of "voip.ms SMS API endpoint"
```

### 首次搜索速度较慢

首次搜索时需要加载嵌入模型（约1-2秒），后续搜索则非常快速。

### ID重复错误

```bash
# Reset and re-index
python3 rag_manage.py reset
python3 ingest_sessions.py
python3 ingest_docs.py workspace
```

### ChromaDB模型下载

首次运行时需要下载嵌入模型（79MB），耗时1-2分钟。请等待完成。

## 最佳实践

### 定期重新索引

在进行重大修改后，请重新索引知识库：

```bash
python3 ingest_sessions.py  # New conversations
python3 ingest_docs.py workspace  # New code/changes
```

### 使用特定查询

可以使用特定的查询条件来缩小搜索范围：

```bash
# Better
python3 rag_query.py "voip.ms getSMS method"

# Too broad
python3 rag_query.py "SMS"
```

### 按类型过滤

可以根据文件类型进行过滤：

```bash
# Looking for code
python3 rag_query.py --type workspace "chromedriver"

# Looking for past conversations
python3 rag_query.py --type session "Reddit"
```

### 手动添加文档

在做出重要决策后，可以手动将相关文档添加到索引中：

```bash
python3 rag_manage.py add \
  --text "Decision: Use Playwright for Reddit automation. Reason: Cloudflare bypass handles" \
  --source "decision:reddit-automation" \
  --type "decision"
```

## 限制

- 大于1MB的文件会被自动跳过（为了提高性能）
- 需要Python 3.7及以上版本
- 每1,000份文档占用约100MB的磁盘空间
- 首次搜索速度较慢（因为需要加载嵌入模型）

## 与OpenClaw的集成

该功能与OpenClaw无缝集成：
- **自动RAG**：AI在响应时会自动检索相关上下文
- **会话历史记录**：所有聊天记录都被索引并可供搜索
- **工作区内容**：代码和文档都被索引以便参考
- **技能文档**：可以从任何OpenClaw会话或脚本中访问

## 安全注意事项

**⚠️ 重要隐私提示：** 该RAG系统会索引本地数据，其中可能包含：
- API密钥、令牌或会话记录中的凭据
- 包含敏感数据的私人消息
- 工作区配置文件

**建议：**
- 如果担心隐私问题，请在数据入库前审查会话文件
- 考虑从会话文件中删除敏感信息
- 可使用`rag_manage.py reset`命令删除整个索引
- 可通过删除`~/.openclaw/data/rag/`目录来清除所有索引数据
- 自动更新脚本仅执行本地数据导入，不会从远程获取数据

**路径兼容性：**
所有脚本现在都使用动态路径解析（`os.path.expanduser()`、`Path(__file__).parent`），以确保在不同用户环境中的兼容性。代码库中不再包含硬编码的绝对路径。

**网络调用：**
- 嵌入模型（all-MiniLM-L6-v2）会在首次使用时通过pip下载
- 不涉及自定义的网络调用、HTTP请求或子进程操作
- 不会向外部服务上传任何数据（ChromaDB的遥测功能已禁用）
- 所有处理和存储操作均在本地完成

## 示例工作流程

**场景示例：** 您正在开发一个新的自动化脚本，但遇到了Cloudflare相关的问题。

```bash
# Search for past Cloudflare solutions
python3 rag_query.py "Cloudflare bypass selenium"

# Result shows relevant past conversation:
# "Used undetected-chromedriver but failed. Switched to Playwright which handles challenges better."

# Now you know the solution before trying it!
```

## 与Moltbook的集成

可以将RAG功能的更新信息发布到Moltbook社交网络。

### 快速发布

```bash
# Post from draft file
python3 scripts/moltbook_post.py --file drafts/moltbook-post-rag-release.md

# Post directly
python3 scripts/moltbook_post.py "Title" "Content"
```

### 使用示例

**发布更新公告：**
```bash
cd ~/.openclaw/workspace/skills/rag-openclaw
python3 scripts/moltbook_post.py --file drafts/moltbook-post-rag-release.md --submolt general
```

**发布快速更新：**
```bash
python3 scripts/moltbook_post.py "RAG Update" "Fixed path portability issues"
```

**发布到Moltbook：**
```bash
python3 scripts/moltbook_post.py "Feature Drop" "New semantic search" "aiskills"
```

### 配置

**（可选）使用Moltbook进行发布：**

设置环境变量：
```bash
export MOLTBOOK_API_KEY="your-key"
```

或创建凭证文件：
```bash
mkdir -p ~/.config/moltbook
cat > ~/.config/moltbook/credentials.json << EOF
{
  "api_key": "moltbook_sk_YOUR_KEY_HERE"
}
EOF
```

**注意：** 使用Moltbook发布RAG更新是可选的。核心的RAG功能无需依赖外部服务，完全可以离线使用。

### 速率限制

- **发布内容**：每30分钟最多发布1条
- **评论**：每20秒最多发布1条

如果遇到速率限制，请等待错误提示中显示的`retry_after_minutes`时间。

### 文档说明

详细文档和API参考请参见`scripts/MOLTBOOK_POST.md`。

## 仓库地址

https://git(theta42.com/nova/openclaw-rag-skill

**发布平台：** clawhub.com
**维护者：** Nova AI Assistant
**开发者：** William Mantly (Theta42)

## 许可证

MIT许可证——免费使用和修改