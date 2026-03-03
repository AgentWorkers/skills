---
name: ssh-config-manager
description: 这是一个用于管理SSH配置文件、整理主机信息、生成配置文件以及测试连接功能的命令行工具（CLI）。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# SSH 配置管理器

## 功能简介

这是一个命令行（CLI）工具，用于管理 SSH 配置文件（`~/.ssh/config`）。它可以帮助您整理 SSH 主机信息、生成配置文件、测试连接，并保持 SSH 配置的整洁性和可维护性。

主要功能包括：
- **解析并显示**现有的 SSH 配置文件（以易读的格式）
- **添加/删除/编辑** SSH 配置中的主机信息
- **使用标签、组或类别**对主机进行分类管理
- **测试 SSH 连接**以确认主机的可用性
- **根据模板或 JSON/YAML 输入生成配置文件**
- **验证配置文件的语法**以确保其正确性
- **在修改配置文件前进行备份和恢复**

## 使用场景

- 当您的 `~/.ssh/config` 文件因包含大量主机信息而变得混乱时
- 当您需要快速测试 SSH 连接是否正常工作时
- 当您希望与团队成员共享 SSH 配置时
- 当您经常在不同环境（工作/家庭/云环境）之间切换时
- 当您希望按项目、环境或团队来组织主机信息时
- 当您需要在应用更改前验证 SSH 配置的语法正确性时

## 使用方法

基本命令如下：

```bash
# List all hosts in your SSH config
python3 scripts/main.py list

# Add a new host
python3 scripts/main.py add --host myserver --hostname 192.168.1.100 --user admin

# Test SSH connection to a host
python3 scripts/main.py test --host myserver

# Organize hosts by tags
python3 scripts/main.py organize --tag work --hosts server1,server2,server3

# Generate SSH config from YAML template
python3 scripts/main.py generate --template servers.yaml --output ~/.ssh/config

# Validate SSH config syntax
python3 scripts/main.py validate --file ~/.ssh/config
```

## 示例

### 示例 1：列出并整理主机信息

```bash
python3 scripts/main.py list --format table
```

输出：
```
┌─────────────────┬──────────────────────┬───────────┬───────────────┐
│ Host            │ Hostname             │ User      │ Tags          │
├─────────────────┼──────────────────────┼───────────┼───────────────┤
│ github          │ github.com           │ git       │ git           │
│ work-server     │ 192.168.1.100       │ admin     │ work,prod     │
│ staging         │ staging.example.com  │ deploy    │ work,staging  │
│ personal-vps    │ 45.33.22.11          │ root      │ personal      │
└─────────────────┴──────────────────────┴───────────┴───────────────┘
```

### 示例 2：添加带有高级选项的新主机

```bash
python3 scripts/main.py add \
  --host new-server \
  --hostname server.example.com \
  --user ec2-user \
  --port 2222 \
  --identity ~/.ssh/id_rsa \
  --tag "aws,production" \
  --description "Production web server"
```

### 示例 3：测试多个主机

```bash
python3 scripts/main.py test --hosts work-server,staging,personal-vps
```

输出：
```
Testing SSH connections...
✅ work-server (192.168.1.100): Connected successfully
✅ staging (staging.example.com): Connected successfully
❌ personal-vps (45.33.22.11): Connection timeout
```

### 示例 4：根据模板生成配置文件

```yaml
# servers.yaml
hosts:
  web-prod:
    hostname: web.example.com
    user: deploy
    port: 22
    identityfile: ~/.ssh/deploy_key
    tags: [web, production]
    
  db-backup:
    hostname: db-backup.internal
    user: backup
    port: 2222
    proxycommand: "ssh -W %h:%p bastion"
    tags: [database, backup]
```

```bash
python3 scripts/main.py generate --template servers.yaml --output ~/.ssh/config
```

## 系统要求

- Python 3.x
- 已安装 SSH 客户端（`ssh` 命令必须在 PATH 环境变量中可用）
- 具有读取/写入 `~/.ssh/config` 文件的权限（或指定的配置文件）

## 限制

- 该工具仅为命令行工具，不提供自动集成功能
- 需要安装 Python 3.x 和 SSH 客户端
- 对 SSH 配置文件的语法验证较为基础（可能无法检测所有复杂情况）
- 连接测试需要正确设置 SSH 密钥
- 该工具不负责管理 SSH 密钥或证书
- 仅支持标准的 SSH 配置选项
- 工具的性能会受到配置文件中主机数量的影响
- 网络延迟可能会影响连接测试的结果
- 不支持所有高级的 SSH 配置功能（如匹配规则等）
- 备份文件采用简单的时间戳命名格式