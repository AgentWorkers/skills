---
name: surrealfs
description: "SurrealFS：专为AI代理设计的虚拟文件系统。采用Rust语言开发核心组件，配合Python代理（基于Pydantic框架实现AI功能）。文件操作具有持久性，数据存储由SurrealDB提供支持。该组件属于surreal-skills系列软件的一部分。"
license: MIT
metadata:
  version: "1.0.2"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-19"
  upstream:
    repo: "surrealdb/surrealfs"
    sha: "0008a3a94dbe"
---
# SurrealFS -- 专为AI代理设计的虚拟文件系统

SurrealFS提供了一个持久化、可查询的虚拟文件系统，该系统基于SurrealDB技术实现。它专为需要可靠文件操作、分层存储以及跨会话内容搜索功能的AI代理而设计。

## 组件

| 组件 | 包名/库名 | 语言 | 用途 |
|-----------|---------------|----------|---------|
| 核心库 | `surrealfs` | Rust | 文件系统操作、命令行交互界面（CLI REPL）以及SurrealDB存储层 |
| AI代理 | `surrealfs-ai` | Python（使用Pydantic框架） | 代理接口及工具集成，支持HTTP服务 |

## Rust核心组件 -- 命令

`surrealfs`库提供了一个具备POSIX风格命令的命令行交互界面（REPL）：

| 命令 | 描述 |
|---------|-------------|
| `ls` | 列出目录内容 |
| `cat` | 显示文件内容 |
| `tail` | 显示文件的最后几行 |
| `nl` | 显示文件的总行数 |
| `grep` | 在文件内容中搜索指定字符串 |
| `touch` | 创建空文件 |
| `mkdir` | 创建目录 |
| `write_file` | 向文件写入内容 |
| `edit` | 编辑文件内容 |
| `cp` | 复制文件 |
| `cd` | 更改目录 |
| `pwd` | 打印当前工作目录 |

支持从外部命令进行数据传输：`curl https://example.com > /pages/example.html`

**存储后端：**
- 内置的RocksDB（本地存储）
- 通过WebSocket访问远程的SurrealDB

## Python AI代理

该代理基于Pydantic AI框架构建，提供了与文件系统命令相对应的功能。

```python
from surrealfs_ai import build_chat_agent

# Create the agent (default LLM: Claude Haiku)
agent = build_chat_agent()

# Expose over HTTP
import uvicorn
app = agent.to_web()
uvicorn.run(app, host="127.0.0.1", port=7932)
```

**主要特性：**
- 默认的LLM模型：Claude Haiku
- 通过Pydantic Logfire（OpenTelemetry）实现遥测功能
- 所有文件系统操作均可作为代理工具使用
- 支持HTTP服务（默认端口为7932）
- 路径规范化功能（无法使用`/`作为路径分隔符）

## 快速入门

```bash
# Install the Rust core
cargo install surrealfs

# Start the REPL with embedded storage
surrealfs

# Or connect to a remote SurrealDB instance
surrealfs --endpoint ws://localhost:8000 --user root --pass root --ns agent --db workspace

# Install the Python agent
pip install surrealfs-ai

# Run the agent HTTP server
python -m surrealfs_ai --host 127.0.0.1 --port 7932
```

**使用场景：**
- 为AI代理会话提供持久化的工作空间
- 支持带有元数据查询的分层文档存储
- 支持多代理之间的文件共享及权限控制（通过SurrealDB实现）
- 用于内容策略和知识管理
- 项目框架搭建及模板管理

## 完整文档

请参阅以下规则文件以获取完整的使用指南：
- **[rules/surrealfs.md](../../rules/surrealfs.md)** -- 包含系统架构、Rust核心API、Python代理配置、SurrealDB数据库模式、多代理协作方式及部署指南
- **[surrealdb/surrealfs](https://github.com/surrealdb/surrealfs)** -- 上游代码仓库