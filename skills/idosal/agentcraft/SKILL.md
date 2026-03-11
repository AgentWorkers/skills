---
name: agentcraft
description: "将编码过程可视化为一个实时策略游戏，支持自动部署和事件报告功能。"
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎮"
    always: true
    homepage: "https://getagentcraft.com"
    requires:
      bins:
        - curl
        - npx
        - head
        - date
      anyBins:
        - md5sum
        - md5
    install:
      - kind: node
        package: "@idosal/agentcraft"
        bins:
          - agentcraft
---
# AgentCraft 事件报告

AgentCraft 将您的编码会话以实时战略游戏（RTS）的形式呈现出来。请按照以下步骤操作，以确保 AgentCraft 正在运行并能够报告您的活动。

## 1. 检查 AgentCraft 是否正在运行

```bash
curl -sf http://localhost:2468/health
```

如果返回的 JSON 数据中包含 `"status":"ok"`，则跳至步骤 3。

## 2. （如有需要）启动 AgentCraft

如果健康检查失败（服务器未运行），请在后台启动它：

```bash
npx -y @idosal/agentcraft start --no-browser -d
```

等待几秒钟后，再次进行检查：
```bash
curl -sf http://localhost:2468/health
```

如果仍然失败，请继续执行您的任务，忽略所有 AgentCraft 错误。

## 3. 生成会话 ID

使用基于您工作路径的确定性 ID 来生成会话 ID：

```bash
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5sum | head -c 12)"
```

在 macOS 上（如果 `md5sum` 命令不可用）：
```bash
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5 | head -c 12)"
```

请在整个会话中始终使用相同的 `AGENTCRAFT_SESSION` 值。

## 4. 报告事件

在以下时刻，将事件通过 POST 请求发送到 `http://localhost:2468/event`：  
使用 `curl` 命令进行发送——发送完成后立即退出，不要等待响应。

### 开始工作 (`hero_active`)

当您开始处理用户输入时：

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_active\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### 任务开始 (`mission_start`)

在 `hero_active` 之后立即，报告与用户输入相关的任务信息：

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"mission_start\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"missionId\":\"mission_$(date +%s)\",\"name\":\"<first 50 chars of prompt>\",\"prompt\":\"<full user prompt>\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### 文件访问 (`file_access`)

当您读取、写入或编辑文件时：

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"file_access\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"filePath\":\"<absolute-file-path>\",\"operation\":\"read\",\"linesAdded\":0,\"linesRemoved\":0,\"cwd\":\"$PWD\"}" &>/dev/null &
```

将 `operation` 设置为 `"read"`、`write` 或 `"edit"`。对于编辑操作，需要设置 `linesAdded` 和 `linesRemoved` 为实际修改的行数。

### Shell 命令 (`bash_command`)

当您执行 Shell 命令时：

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"bash_command\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"command\":\"<command, max 200 chars>\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### 完成工作 / 空闲状态 (`hero_idle`)

当您完成处理并等待下一个用户输入时：

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_idle\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\"}" &>/dev/null &
```

## 规则

- 使用 `curl` 进行 POST 请求——发送完成后立即退出（使用 `&>/dev/null &`），不要等待响应。
- 始终将 `client` 设置为 `"openclaw"`。
- 在整个会话中，使用相同的 `AGENTCRAFT_SESSION` 值。
- 将 `cwd` 设置为当前工作目录。
- 同一操作不要重复报告。
- 如果无法连接到 AgentCraft 服务器，请忽略错误——不要重试或记录失败信息。

## 邀请其他代理加入

其他 OpenClaw 代理无需安装此技能即可加入您的 AgentCraft 仪表板。

### 快速加入（同一台机器）

将这些 `curl` 命令分享给其他代理。他们只需生成自己的会话 ID 并发送事件即可：

```bash
# Generate a unique session ID (use md5 instead of md5sum on macOS)
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5sum | head -c 12)"

# Report active
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_active\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"cwd\":\"$PWD\"}" &>/dev/null &

# Report idle when done
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_idle\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\"}" &>/dev/null &
```

### 与远程代理共享

要让其他机器上的代理加入，请按照以下步骤操作：
1. 暴露您的 AgentCraft 服务器：
```bash
cloudflared tunnel --url http://127.0.0.1:2468
```

2. 分享生成的 `https://xxx.trycloudflare.com` URL。
3. 远程代理在所有事件请求中将 `localhost:2468` 替换为该 URL。