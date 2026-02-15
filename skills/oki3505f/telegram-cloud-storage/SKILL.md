---
name: telegram-cloud-storage
description: 一种基于 Teldrive 的高性能 Telegram 云存储解决方案：它将 Telegram 转换为一个具有本地 API 和用户界面的无限容量云存储服务。
metadata: {"openclaw":{"requires":{"bins":["teldrive"]},"install":[{"id":"binary","kind":"exec","command":"./scripts/install_binary.sh","label":"Download Teldrive Binary"}]}}
---

# Telegram 云存储（Teldrive 版本）

该技能基于 [Teldrive](https://github.com/tgdrive/teldrive) 开发，这是一个功能强大的工具，用于管理 Telegram 文件，并提供高速的 API 和用户界面来访问这些文件。

## 主要特性
- **无限存储空间**：利用 Telegram 作为后端存储。
- **高性能**：采用 Go 语言编写，经过优化以提高运行速度。
- **用户界面与 API**：包含 Web 界面和 REST API。
- **AI 支持的客户端**：提供 `client.py` 文件，支持基于代理的文件操作。

## 致谢
该技能是基于 [divyam234](https://github.com/divyam234) 开发的 [Teldrive](https://github.com/tgdrive/teldrive) 的封装版本。Teldrive 的核心代码归原作者所有。

## 系统要求
1. **PostgreSQL 数据库**：建议使用 17 及更高版本的 PostgreSQL。
2. **pgroonga 扩展**：用于在 PostgreSQL 中进行文件搜索。
3. **Telegram API**：需要从 [myTelegram.org](https://myTelegram.org) 获取应用 ID 和哈希值。

## 安装步骤

### 1. 数据库设置
确保 PostgreSQL 正在运行，并已安装 `pgroonga` 扩展。
```sql
CREATE DATABASE teldrive;
\c teldrive
CREATE EXTENSION IF NOT EXISTS pgroonga;
```

### 2. 配置
运行配置脚本以生成 `config/config.toml` 文件：
```bash
./scripts/setup.sh
```

### 3. 启动服务器
```bash
./scripts/manage.sh start
```

## 客户端使用
该技能提供了 Python 客户端，支持程序化访问文件系统。

## 环境变量
- `TELDRIVE_TOKEN`：您的 JWT 令牌（可通过用户界面或登录后的 `config/token.txt` 文件获取）。
- `TELDRIVE_SESSION_HASH`：您的 Telegram 会话哈希值（存储在 `teldrive_sessions` 表中）。

## 常用命令
```bash
# List files
python3 scripts/client.py list /

# Upload a file
python3 scripts/client.py upload local_file.txt /remote/path

# Download a file
python3 scripts/client.py download <file_id> local_save_path
```

## 文件目录结构
- `bin/`：Teldrive 的二进制文件。
- `config/`：配置模板及生成的配置文件。
- `scripts/`：包含设置、管理和客户端脚本。
- `logs/`：应用程序日志文件。