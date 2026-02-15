---
name: private-connect
description: 无需使用 VPN 或 SSH 隧道，即可从任何地点通过名称访问私有服务。
homepage: https://privateconnect.co
repository: https://github.com/treadiehq/private-connect
author: Treadie
gating:
  binary: connect
---

# Private Connect

无论身处何地，都可以通过名称访问私有服务。无需使用 VPN 或 SSH 隧道。

## 功能介绍

Private Connect 允许您使用简单的名称（而非 IP 地址和端口号）来访问私有基础设施（如数据库、API、GPU 集群），从而快速与团队成员共享开发环境。

## 命令

### connect_reach
通过名称连接到私有服务。

**示例：**
- “将我连接到 staging 数据库”
- “访问 prod API”
- “连接到 jupyter-gpu”

### connect_status
显示可用的服务及其连接状态。

**示例：**
- “有哪些服务可用？”
- “显示我当前连接的服务”
- “staging 数据库是否在线？”

### connect_share
与团队成员共享您的当前开发环境。

**示例：**
- “共享我的开发环境”
- “创建一个有效期为 7 天的共享链接”
- “将我的环境设置共享给团队，共享期限为 1 周”

### connect_join
从团队成员那里加入一个共享的环境。

**示例：**
- “加入 share code x7k9m2”
- “连接到 Bob 的环境”

### connect_clone
克隆团队成员的整个开发环境设置。

**示例：**
- “克隆 Alice 的环境”
- “将我的环境设置设置为与资深开发人员相同”

### connect_list_shares
列出当前正在共享的环境。

**示例：**
- “显示我正在共享的环境”
- “我正在共享哪些环境？”

### connect_revoke
撤销对某个环境的共享权限。

**示例：**
- “撤销 share x7k9m2 的共享权限”
- “停止与承包商共享环境”

## 设置步骤

1. 安装 Private Connect：
```bash
curl -fsSL https://privateconnect.co/install.sh | bash
```

2. 进行身份验证：
```bash
connect up
```

3. 该工具将使用您的已认证会话进行操作。

## 使用要求

- 确保已安装并配置了 Private Connect 的命令行界面（CLI），并且已完成身份验证。
- 确保 `connect` 命令可以在系统的 PATH 环境变量中找到。