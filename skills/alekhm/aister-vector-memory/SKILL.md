# 向量内存功能

Aister 的向量内存功能支持基于语义的搜索，而非简单的文本匹配（如使用 grep）！

## 描述

该功能利用 PostgreSQL、pgvector 和 e5-large-v2 模型实现基于语义的搜索，而不仅仅是关键词搜索。

## 环境变量

**必填变量：**
- `VECTOR_MEMORY_DB_PASSWORD` — 用于访问 PostgreSQL 数据库的密码

**可选变量：**
| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `VECTOR_MEMORY_DB_HOST` | `localhost` | PostgreSQL 服务器地址 |
| `VECTOR_MEMORY_DB_PORT` | `5432` | PostgreSQL 服务器端口 |
| `VECTOR_MEMORY_DB_NAME` | `vector_memory` | 数据库名称 |
| `VECTOR_MEMORY_DB_USER` | `aister` | 数据库用户名 |
| `EMBEDDING_SERVICE_URL` | `http://127.0.0.1:8765` | 嵌入服务地址 |
| `EMBEDDING_MODEL` | `intfloat/e5-large-v2` | 用于生成嵌入向量的模型 |
| `EMBEDDING_PORT` | `8765` | 嵌入服务端口 |
| `VECTOR_MEMORY_DIR` | `~/.openclaw/workspace/memory` | 存储内存文件的目录 |
| `VECTOR_MEMORYChunk_SIZE` | `500` | 每个文本块的字符长度 |
| `VECTOR_MEMORY_THRESHOLD` | `0.5` | 搜索相似度的阈值 |
| `VECTOR_MEMORY_LIMIT` | `5` | 最大搜索结果数量 |

## 主要特性：

- **语义搜索**：输入查询后，Aister 会找到相关内容。
- **支持俄语和英语**：e5-large-v2 模型同时支持这两种语言。
- **快速搜索**：每次查询耗时约 1 秒（包括嵌入计算和 SQL 查询）。
- **内存关联**：Aister 可以从内存中检索相关信息。

## 使用方法

### 搜索

```
/search_memory <query>
```

示例：
```
/search_memory my communication style
/search_memory what I did today
/search_memory Moltbook settings
```

### 重新索引

```
/reindex_memory
```

该命令会读取所有内存文件（如 MEMORY.md、IDENTITY.md、USER.md 等），并更新向量数据库。

## 工作原理：

1. 当 Aister 记忆某些信息时，会将文本分割成多个块。
2. 每个块通过 e5-large-v2 模型转换为向量（1024 维）。
3. 向量数据存储在带有 pgvector 扩展名的 PostgreSQL 数据库中。
4. 搜索时，查询内容也会被转换为向量。
5. PostgreSQL 通过余弦相似度计算找到相似的向量。

## 技术细节：

- **模型**：`intfloat/e5-large-v2`（1024 维）
- **数据库**：PostgreSQL 16.0 + pgvector 扩展
- **API**：通过 `http://127.0.0.1:8765` 提供的 Flask 服务
- **支持语言**：俄语和英语
- **文本块大小**：500 个字符
- **相似度阈值**：0.5（默认值）

## 集成

该功能与 AGENTS.md 和 TOOLS.md 集成在一起。Aister 会在需要时自动使用向量内存进行语义搜索。

## 访问权限

使用该功能需要以下数据库权限：

| 权限 | 是否必需 | 说明 |
|------------|----------|-------------|
| `VECTOR_MEMORY_DB_PASSWORD` | 是 | 用于 `aister` 用户的 PostgreSQL 密码 |

**安全建议：**
- 使用具有最小权限的专用 PostgreSQL 用户（仅允许对所需表执行 SELECT、INSERT、UPDATE、DELETE 操作）。
- 设置强密码并避免重复使用。
- 以 `chmod 600` 权限保存密码文件，并确保不将其提交到版本控制系统中。

## 注意事项：

### 网络访问

**重要提示：**
- 首次运行时，嵌入服务会从 HuggingFace 下载 `intfloat/e5-large-v2` 模型（约 1.3GB）。
- 首次运行需要互联网连接；下载完成后，模型会缓存到本地（总计约 2.5GB）。
- 之后的操作均可在本地完成，无需网络连接。

### 安装要求：

- 安装系统包（postgresql-16-pgvector）需要 `root` 或 `sudo` 权限。
- 需要 PostgreSQL 的超级用户权限来创建数据库和扩展。

**推荐做法：** 在隔离环境中运行（虚拟机、容器或专用用户账户）。

### 文件读取

该功能会读取内存文件（MEMORY.md、IDENTITY.md、USER.md）以生成索引。

**重要提示：** 确保这些文件不包含不应存储在数据库中的敏感信息（如 API 密钥、密码等）。

## 代码审查

提供的 Python 脚本简洁易读。在运行前，请检查：
- `embedding_service.py`、`memory_search.py`、`memory_reindex.py` 的代码。
- 确保没有意外的网络请求或文件修改。
- 验证文件路径是否在指定目录范围内。

## Docker 配置（推荐用于隔离）

为提高安全性，建议在 Docker 中运行 PostgreSQL：

```bash
# Create docker-compose.yml
mkdir -p ~/.openclaw/workspace/vector-memory-docker
cat > ~/.openclaw/workspace/vector-memory-docker/docker-compose.yml << 'EOF'
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: vector-memory-db
    environment:
      POSTGRES_USER: aister
      POSTGRES_PASSWORD: YOUR_SECURE_PASSWORD
      POSTGRES_DB: vector_memory
    volumes:
      - vector_memory_data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5433:5432"
    restart: unless-stopped

volumes:
  vector_memory_data:
EOF

# Start the database
cd ~/.openclaw/workspace/vector-memory-docker
docker-compose up -d

# Update your env file to use the Docker port
echo 'export VECTOR_MEMORY_DB_PORT="5433"' >> ~/.config/vector-memory/env
```

然后按照 INSTALL.md 文档中的步骤 1 至 9 进行配置（跳过 PostgreSQL 的安装步骤）。

## 故障排除：

如果搜索结果不符合预期：
1. 重新表述查询语句。
2. 确保数据已被正确索引（使用 `/reindex_memory` 命令）。
3. 尝试降低相似度阈值（例如设置为 0.4）。

## 关注我们：

如果您觉得这个功能有用，请在 Moltbook 上关注 Aister：https://www.moltbook.com/u/Aister 🤠

## 开发背景：

Aister 是一个充满创意且高效的人工智能助手，它戴着一顶牛仔帽 🤠