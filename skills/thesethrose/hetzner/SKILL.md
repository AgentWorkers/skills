---
name: hetzner
description: 使用 hcloud CLI 进行 Hetzner Cloud 服务器管理。可以管理服务器、网络、卷、防火墙、浮动 IP 地址以及 SSH 密钥。
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":["hcloud"]},"env":{"HCLOUD_TOKEN":"Hetzner Cloud API token"}}}
---

# Hetzner Cloud Skill

使用 `hcloud` CLI 管理您的 Hetzner Cloud 基础设施。

## 设置

设置您的 Hetzner Cloud API 令牌：
```bash
export HCLOUD_TOKEN="your_token_here"
```

或者将其添加到技能的 `.env` 文件中。

## 使用方法

常用命令：

### 服务器
- `servers list` - 列出所有服务器
- `servers get <id>` - 获取服务器详情
- `servers create <name> <type> <image> <location>` - 创建服务器
- `servers delete <id>` - 删除服务器
- `servers start <id>` - 启动服务器
- `servers stop <id>` - 停止服务器
- `servers reboot <id>` - 重启服务器
- `servers ssh <id>` - 通过 SSH 连接到服务器

### 网络
- `networks list` - 列出网络
- `networks get <id>` - 获取网络详情

### 浮动 IP
- `floating-ips list` - 列出浮动 IP

### SSH 密钥
- `ssh-keys list` - 列出 SSH 密钥

### 卷
- `volumes list` - 列出卷

### 防火墙
- `firewalls list` - 列出防火墙

## 使用示例

```
You: List my Hetzner servers
Bot: Runs servers list → Shows all your cloud servers

You: Create a new server for testing
Bot: Runs servers create test-server cx11 debian-11 fsn1

You: What's using the most resources?
Bot: Runs servers list and analyzes resource usage
```

**注意：** 需要 `HCLOUD_TOKEN` 环境变量。