---
name: neon
description: "Neon 无服务器 Postgres — 通过 Neon API 管理项目、分支、数据库、角色、端点以及计算资源。可以创建用于开发的数据库分支，管理连接端点，扩展计算能力，并监控使用情况。专为 AI 代理设计，仅依赖 Python 标准库，无任何外部依赖。适用于无服务器 Postgres、数据库分支管理、开发工作流程以及云数据库自动化场景。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "💚", "requires": {"env": ["NEON_API_KEY"]}, "primaryEnv": "NEON_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 💚 Neon

Neon 是一个无服务器的 PostgreSQL 管理工具，通过 Neon API 可以管理项目、分支、数据库、角色、端点以及计算资源。

## 主要功能

- **项目管理**：创建、列出和删除项目。
- **分支管理**：创建、恢复和删除分支。
- **数据库操作**：创建和管理数据库。
- **角色管理**：管理数据库用户及其权限。
- **端点管理**：配置连接端点和资源池。
- **计算资源扩展**：自动暂停计算资源、控制计算规模。
- **连接字符串**：生成数据库连接 URI。
- **操作历史记录**：追踪异步操作。
- **使用统计**：统计计算时间、存储使用量和数据传输量。
- **分支恢复**：从历史记录中恢复到指定时间点。

## 必需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `NEON_API_KEY` | ✅ | Neon 的 API 密钥/令牌 |

## 快速入门

```bash
# List projects
python3 {baseDir}/scripts/neon.py projects --limit 20
```

```bash
# Get project details
python3 {baseDir}/scripts/neon.py project-get proj-abc123
```

```bash
# Create a project
python3 {baseDir}/scripts/neon.py project-create '{"project":{"name":"my-app","region_id":"aws-us-east-1"}}'
```

```bash
# Delete a project
python3 {baseDir}/scripts/neon.py project-delete proj-abc123
```



## 命令

### `projects`  
列出所有项目。  
```bash
python3 {baseDir}/scripts/neon.py projects --limit 20
```

### `project-get`  
获取项目详细信息。  
```bash
python3 {baseDir}/scripts/neon.py project-get proj-abc123
```

### `project-create`  
创建一个新的项目。  
```bash
python3 {baseDir}/scripts/neon.py project-create '{"project":{"name":"my-app","region_id":"aws-us-east-1"}}'
```

### `project-delete`  
删除一个项目。  
```bash
python3 {baseDir}/scripts/neon.py project-delete proj-abc123
```

### `branches`  
列出所有分支。  
```bash
python3 {baseDir}/scripts/neon.py branches --project proj-abc123
```

### `branch-create`  
创建一个新的分支。  
```bash
python3 {baseDir}/scripts/neon.py branch-create --project proj-abc123 '{"branch":{"name":"dev","parent_id":"br-main"}}'
```

### `branch-delete`  
删除一个分支。  
```bash
python3 {baseDir}/scripts/neon.py branch-delete --project proj-abc123 br-dev
```

### `branch-restore`  
将分支恢复到指定时间点。  
```bash
python3 {baseDir}/scripts/neon.py branch-restore --project proj-abc123 br-main --timestamp '2026-02-01T00:00:00Z'
```

### `databases`  
列出所有数据库。  
```bash
python3 {baseDir}/scripts/neon.py databases --project proj-abc123 --branch br-main
```

### `database-create`  
创建一个新的数据库。  
```bash
python3 {baseDir}/scripts/neon.py database-create --project proj-abc123 --branch br-main '{"database":{"name":"mydb","owner_name":"neondb_owner"}}'
```

### `roles`  
列出所有角色。  
```bash
python3 {baseDir}/scripts/neon.py roles --project proj-abc123 --branch br-main
```

### `endpoints`  
列出所有端点。  
```bash
python3 {baseDir}/scripts/neon.py endpoints --project proj-abc123
```

### `connection-string`  
生成数据库连接字符串。  
```bash
python3 {baseDir}/scripts/neon.py connection-string --project proj-abc123 --branch br-main --database mydb
```

### `consumption`  
获取使用统计信息。  
```bash
python3 {baseDir}/scripts/neon.py consumption --from 2026-01-01 --to 2026-02-01
```

### `operations`  
列出所有执行的操作。  
```bash
python3 {baseDir}/scripts/neon.py operations --project proj-abc123 --limit 10
```


## 输出格式

所有命令默认以 JSON 格式输出。若需可读的格式输出，可添加 `--human` 参数。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/neon.py projects --limit 5

# Human-readable
python3 {baseDir}/scripts/neon.py projects --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/neon.py` | 主要的命令行工具（CLI），用于执行所有 Neon 操作 |

## 数据政策

该工具 **从不将数据存储在本地**。所有请求直接发送到 Neon API，结果会输出到标准输出（stdout）。您的数据将保存在 Neon 服务器上。

## 致谢  
---  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)