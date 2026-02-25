---
name: surrealfs
description: "SurrealFS：专为AI代理设计的虚拟文件系统。采用Rust语言作为核心框架，配合Python代理（基于Pydantic库实现AI功能）。文件操作具有持久化特性，数据存储由SurrealDB数据库提供支持。该组件属于surreal-skills技术栈的一部分。"
license: MIT
metadata:
  version: "1.0.4"
  author: "24601"
  parent_skill: "surrealdb"
  snapshot_date: "2026-02-22"
  upstream:
    repo: "surrealdb/surrealfs"
    sha: "0008a3a94dbe"
requires:
  env_vars:
    - name: SURREAL_ENDPOINT
      purpose: "SurrealDB server URL (for remote backend)"
      sensitive: false
    - name: SURREAL_USER
      purpose: "SurrealDB authentication username"
      sensitive: true
    - name: SURREAL_PASS
      purpose: "SurrealDB authentication password"
      sensitive: true
security:
  no_network: false
  no_network_note: "Connects to user-specified SurrealDB endpoint. Python agent hosts HTTP on localhost by default."
  no_credentials: false
  no_credentials_note: "Requires SurrealDB credentials for remote backend connections."
  scripts_auditable: true
  no_obfuscated_code: true
  no_binary_blobs: true
---
# SurrealFS -- 专为AI代理设计的虚拟文件系统

SurrealFS提供了一个持久化、可查询的虚拟文件系统，该系统基于SurrealDB进行存储。它专为需要稳定文件操作、分层存储以及在会话间进行内容搜索的AI代理而设计。

## 组件

| 组件 | 包名 | 语言 | 用途 |
|-----------|---------------|----------|---------|
| 核心库 | `surrealfs` | Rust | 文件系统操作、命令行界面（CLI）以及SurrealDB存储层 |
| AI代理 | `surrealfs-ai` | Python (Pydantic AI) | 代理接口及工具集成、HTTP服务 |

## Rust核心组件 -- 命令

`surrealfs`库提供了一个支持POSIX命令的命令行界面（REPL）：

| 命令 | 描述 |
|---------|-------------|
| `ls` | 列出目录内容 |
| `cat` | 显示文件内容 |
| `tail` | 显示文件的最后几行 |
| `nl` | 显示文件的行数 |
| `grep` | 在文件内容中搜索 |
| `touch` | 创建空文件 |
| `mkdir` | 创建目录 |
| `write_file` | 向文件写入内容 |
| `edit` | 编辑文件内容 |
| `cp` | 复制文件 |
| `cd` | 更改目录 |
| `pwd` | 打印当前工作目录 |

支持从外部命令传递数据：`curl https://example.com > /pages/example.html`

**存储后端**：
- 内置的RocksDB（本地存储）
- 通过WebSocket访问远程的SurrealDB

## Python AI代理

该代理基于Pydantic AI构建，提供了与文件系统命令相匹配的功能。

```python
from surrealfs_ai import build_chat_agent

# Create the agent (default LLM: Claude Haiku)
agent = build_chat_agent()

# Expose over HTTP
import uvicorn
app = agent.to_web()
uvicorn.run(app, host="127.0.0.1", port=7932)
```

**特性**：
- 默认的LLM模型：Claude Haiku
- 通过Pydantic Logfire（OpenTelemetry）实现遥测功能（可关闭）——详见安全章节
- 所有文件系统操作均可作为代理工具使用
- 提供HTTP服务（默认端口7932，绑定到127.0.0.1）
- 路径规范化：虚拟文件系统的根目录`/`是隔离的；路径无法穿透到宿主文件系统

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

**使用场景**：
- 为AI代理会话提供持久化的工作空间
- 支持带有元数据查询的分层文档存储
- 多代理间共享文件访问，并支持SurrealDB权限控制
- 内容策略与知识管理
- 项目框架搭建及模板管理

## 安全注意事项

**凭证**：远程访问SurrealDB需要使用`--user`/`--pass`参数。请使用专用的、权限最低的凭证，并将其限制在特定的命名空间/数据库范围内。切勿在共享环境或生产环境中使用`root`凭证。

**遥测**：Python代理使用Pydantic Logfire（OpenTelemetry）进行数据传输。如需禁用遥测功能，请设置`export LOGFIRE_SEND_TO_LOGFIRE=false`，或在代码中配置`send_to_logfire=False`。在处理敏感数据的环境中启用遥测功能前，请先进行审计。

**HTTP绑定**：代理默认绑定到`127.0.0.1`。切勿在未经身份验证和TLS保护的情况下将其暴露到`0.0.0.0`或公共网络。如果在容器中运行，请使用网络隔离措施。

**命令传递**：Rust核心支持`curl URL > /path`的语法来传递数据。该命令会在宿主机上执行相应的操作。仅在受控环境中使用此功能，并确保只传递来自可信来源的URL。切勿允许未经验证的输入用于构建命令。

**沙箱环境**：虚拟文件系统的根目录`/`是基于SurrealDB的抽象层，而非宿主文件系统。虽然路径遍历（如`../../etc/passwd`）会被规范化处理，但命令仍然会在宿主机上执行。因此，在接受不可信代理输入的情况下，请确保在容器或沙箱环境中运行程序。

## 完整文档

有关详细信息，请参阅以下文档文件：
- **[rules/surrealfs.md](../../rules/surrealfs.md)**：系统架构、Rust核心API、Python代理配置、SurrealDB数据模型、多代理协作模式及部署指南
- **[surrealdb/surrealfs](https://github.com/surrealdb/surrealfs)**：项目源代码仓库