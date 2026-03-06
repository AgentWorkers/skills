---
name: clawnexus
description: "在您的局域网（LAN）中发现、命名并管理 OpenClaw 实例。通过 ClawNexus 守护进程扫描 AI 代理，检查其状态，设置别名，解析 `.claw` 文件名，并获取连接 URL。"
version: 0.2.7
metadata: {"clawdbot": {"emoji": "🦞", "homepage": "https://github.com/SilverstreamsAI/ClawNexus", "requires": {"env": [], "bins": ["curl"]}}}
---
# ClawNexus

## 概述

ClawNexus 是 OpenClaw 的命名与发现层。它运行一个本地守护进程，该进程会自动检测网络中的 OpenClaw 实例，并为这些实例分配易于识别的名称，这样您就可以通过别名（例如 “home”）而不是 IP 地址来引用这些实例。

## 先决条件

```bash
# Install and start the daemon
npm install -g clawnexus
clawnexus start
```

## 适用场景

- 当守护进程未运行时，应提示用户先运行 `clawnexus start` 命令。
- 当用户只有一个 OpenClaw 实例且不需要发现功能时。
- 在没有 `.claw` 名称的情况下进行跨互联网连接时（仅使用本地局域网）。

## 命令

### 列出所有已知的 OpenClaw 实例

```bash
curl -s http://localhost:17890/instances | jq '.instances[] | {name: (.alias // .auto_name), status, address}'
```

### 检查特定实例（通过别名、自动名称或地址:端口）

```bash
curl -s http://localhost:17890/instances/home
curl -s http://localhost:17890/instances/olivia
curl -s http://localhost:17890/instances/192.168.1.10:18789
```

### 扫描本地网络中的 OpenClaw 实例

```bash
curl -s -X POST http://localhost:17890/scan
```

### 为某个实例设置一个友好的别名

```bash
curl -s -X PUT http://localhost:17890/instances/olivia/alias \
  -H "Content-Type: application/json" \
  -d '{"alias": "home"}'
```

### 获取用于连接实例的 WebSocket URL

```bash
# Get address and port, then build URL
curl -s http://localhost:17890/instances/home | jq '"ws://\(.address):\(.gateway_port)"'
```

### 检查守护进程的运行状态

```bash
curl -s http://localhost:17890/health
```

### 解析 `.claw` 名称（需要互联网连接且 OpenClaw 版本需大于或等于 v0.2）

```bash
curl -s http://localhost:17890/resolve/myagent.id.claw
```

## 工作流程：“home” 实例是否在线？

1. 检查实例状态：`curl -s http://localhost:17890/instances`
2. 在响应中查找别名 “home”。
3. 如果状态显示为 “online”，则确认给用户。
4. 如果找不到该实例，则建议执行扫描：`curl -X POST http://localhost:17890/scan`

## 工作流程：“将我连接到 raspi”

1. 解析目标实例的详细信息：`curl -s http://localhost:17890/instances/raspi`
2. 构建 WebSocket 连接 URL：`ws://<地址>:<网关端口>`
3. 将生成的 URL 告知用户，以便通过 OpenClaw 的网关功能进行连接。

## 故障排除

- 如果在访问 `localhost:17890` 时出现 “连接被拒绝”的错误，说明 ClawNexus 守护进程未运行。请提示用户运行 `clawnexus start`。
- 如果未找到任何实例，可能是守护进程刚刚启动。尝试运行 `curl -s -X POST http://localhost:17890/scan` 以触发网络扫描，然后再尝试列出实例。
- 如果某个实例的状态显示为 “offline”，可能是该实例上的 OpenClaw 网关已停止。虽然该实例之前已被检测到，但目前无法访问。

## 注意事项

- 实例的标识方式包括：别名（alias）、自动名称（auto_name）、显示名称（display_name）、代理 ID（agent_id）、IP 地址或地址:端口（address:port）。
- 自动名称（auto_name）是根据主机名生成的（例如，主机名为 “Olivia” 时，自动名称为 “olivia”）。
- 标志 `is_self: true` 表示该实例是本地机器（地址为 `127.0.0.1`），适用于健康检查。
- 守护进程会将所有实例信息保存到 `~/.clawnexus/registry.json` 文件中。