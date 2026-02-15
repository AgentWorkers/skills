---
name: db-query
description: 查询项目数据库，并具备自动SSH隧道管理功能。适用于需要针对已配置的数据库执行SQL查询的情况，尤其是那些仅能通过SSH隧道访问的数据库。系统会自动管理SSH连接的生命周期（在查询前建立隧道，在查询后关闭隧道）。支持根据配置文件中的描述或名称来区分不同的数据库。
---

# 数据库查询

## 概述

通过一个集中式的配置文件来查询数据库，并实现自动的 SSH 隧道管理。该脚本负责处理连接细节、SSH 隧道的建立/销毁以及查询的执行。

## 配置

### 设置

1. 在 `~/.config/clawdbot/db-config.json` 文件中创建配置文件：
   ```bash
   mkdir -p ~/.config/clawdbot
   # Copy example config and edit
   cp /usr/lib/node_modules/clawdbot/skills/db-query/scripts/config.example.json ~/.config/clawdbot/db-config.json
   ```

2. 添加数据库条目，包含以下字段：
   - `name`：用于识别数据库的描述（必填）
   - `host`：数据库主机（必填）
   - `port`：数据库端口（默认：3306）
   - `database`：数据库名称（必填）
   - `user`：数据库用户名（必填）
   - `password`：数据库密码（必填）
   - `ssh_tunnel`：可选的 SSH 隧道配置

3. **SSH 隧道配置**（如需要）：
   - `enabled`：是否启用 SSH 隧道（true/false）
   - `ssh_host`：远程 SSH 主机
   - `ssh_user`：SSH 用户名
   - `ssh_port`：SSH 端口（默认：22）
   - `local_port`：用于转发的本地端口（例如：3307）
   - `remote_host`：SSH 隧道后的远程数据库主机（默认：localhost）
   - `remote_port`：远程数据库端口（默认：3306）

### 示例配置

```json
{
  "databases": [
    {
      "name": "生产用户库",
      "host": "localhost",
      "port": 3306,
      "database": "user_db",
      "user": "db_user",
      "password": "secret",
      "ssh_tunnel": {
        "enabled": true,
        "ssh_host": "prod.example.com",
        "ssh_user": "deploy",
        "local_port": 3307
      }
    }
  ]
}
```

## 使用方法

### 列出所有数据库

```bash
python3 /usr/lib/node_modules/clawdbot/skills/db-query/scripts/db_query.py --list
```

### 查询数据库

```bash
python3 /usr/lib/node_modules/clawdbot/skills/db-query/scripts/db_query.py \
  --database "生产用户库" \
  --query "SELECT * FROM users LIMIT 10"
```

脚本将执行以下操作：
1. 根据配置文件中的描述查找对应的数据库
2. （如果已配置）启动 SSH 隧道
3. 执行查询
4. **自动关闭 SSH 隧道**（确保系统整洁）

### 使用自定义配置文件路径

```bash
python3 /usr/lib/node_modules/clawdbot/skills/db-query/scripts/db_query.py \
  --config /path/to/custom-config.json \
  --database "test" \
  --query "SHOW TABLES"
```

## 系统要求

- MySQL 客户端：`apt install mysql-client` 或相应软件
- SSH 客户端：通常已预装在 Linux/Mac 系统上
- Python 3.6 或更高版本

## 注意事项

- 查询执行完成后，SSH 隧道会自动关闭
- 使用 `--list` 命令可以查看所有配置的数据库及其描述
- 数据库名称的搜索支持不区分大小写的部分匹配
- 每个数据库的本地端口必须是唯一的