---
name: opencode-acp-control
description: 通过代理客户端协议（Agent Client Protocol, ACP）直接控制 OpenCode。可以启动会话、发送提示、恢复对话以及管理 OpenCode 的更新。
metadata: {"version": "1.0.2", "author": "Benjamin Jesuiter <bjesuiter@gmail.com>", "license": "MIT", "github_url": "https://github.com/bjesuiter/opencode-acp-skill"}
---

# OpenCode ACP 技能

通过代理客户端协议（ACP）直接控制 OpenCode。

## 元数据

- ACP 协议文档（适用于代理/大型语言模型）：https://agentclientprotocol.com/llms.txt
- GitHub 仓库：https://github.com/bjesuiter/opencode-acp-skill
- 如果您遇到此技能的问题，请在此处提交问题票：https://github.com/bjesuiter/opencode-acp-skill/issues

## 快速参考

| 操作 | 方法 |
|--------|-----|
| 启动 OpenCode | `bash(command: "opencode acp", background: true)` |
| 发送消息 | `process.write(sessionId, data: "<json-rpc>\n")` |
| 读取响应 | `process.poll(sessionId)` - 每 2 秒轮询一次 |
| 停止 OpenCode | `process.kill(sessionId)` |
| 列出会话 | `bash(command: "opencode session list", workdir: "...")` |
| 恢复会话 | 列出会话 → 询问用户 → `session/load` |
| 检查版本 | `bash(command: "opencode --version")` |

## 启动 OpenCode

```
bash(
  command: "opencode acp",
  background: true,
  workdir: "/path/to/your/project"
)
```

保存返回的 `sessionId`——后续所有命令都需要它。

## 协议基础

- 所有消息均为 **JSON-RPC 2.0** 格式
- 消息以 **换行符分隔**（每条消息以 `\n` 结尾）
- 从 0 开始维护一个 **消息 ID 计数器**

## 逐步工作流程

### 第 1 步：初始化连接

在启动 OpenCode 后立即发送请求：

```json
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{"fs":{"readTextFile":true,"writeTextFile":true},"terminal":true},"clientInfo":{"name":"clawdbot","title":"Clawdbot","version":"1.0.0"}}}
```

轮询响应。预期返回 `result.protocolVersion: 1`。

### 第 2 步：创建会话

```json
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/path/to/project","mcpServers":[]}}
```

轮询响应。保存 `result.sessionId`（例如，`"sess_abc123"`）。

### 第 3 步：发送提示

```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"sess_abc123","prompt":[{"type":"text","text":"Your question here"}]}}
```

每 2 秒轮询一次。您将收到：
- `session/update` 通知（流式内容）
- 包含 `result.stopReason` 的最终响应

### 第 4 步：读取响应

每次轮询可能返回多行内容。将每行解析为 JSON：

- **通知**：`method: "session/update"`——收集这些通知
- **响应**：如果包含与您的请求匹配的 `id`，则停止轮询

### 第 5 步：取消（如需要）

```json
{"jsonrpc":"2.0","method":"session/cancel","params":{"sessionId":"sess_abc123"}}
```

不期待响应——这表示收到的是通知。

## 需要跟踪的状态

对于每个 OpenCode 实例，跟踪以下信息：
- `processSessionId`——来自 bash 工具（clawdbot 的进程 ID）
- `opencodeSessionId`——来自 session/new 响应（OpenCode 的会话 ID）
- `messageId`——每次发送请求时递增

## 轮询策略

- 每 **2 秒轮询一次**
- 继续轮询，直到收到包含 `stopReason` 的响应
- 最大等待时间：**5 分钟**（150 次轮询）
- 如果没有响应，视为操作超时

## 常见停止原因

| stopReason | 含义 |
|------------|---------|
| `end_turn` | 代理停止响应 |
| `cancelled` | 您取消了提示 |
| `max_tokens` | 达到令牌限制 |

## 错误处理

| 问题 | 解决方案 |
|-------|----------|
| 轮询响应为空 | 继续轮询——代理正在处理中 |
| 解析错误 | 跳过格式错误的行，继续轮询 |
| 进程退出 | 重新启动 OpenCode |
| 5 分钟后仍无响应 | 结束进程，重新开始

## 示例：完整交互流程

```
1. bash(command: "opencode acp", background: true, workdir: "/home/user/myproject")
   -> processSessionId: "bg_42"

2. process.write(sessionId: "bg_42", data: '{"jsonrpc":"2.0","id":0,"method":"initialize",...}\n')
   process.poll(sessionId: "bg_42") -> initialize response

3. process.write(sessionId: "bg_42", data: '{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/home/user/myproject","mcpServers":[]}}\n')
   process.poll(sessionId: "bg_42") -> opencodeSessionId: "sess_xyz789"

4. process.write(sessionId: "bg_42", data: '{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"sess_xyz789","prompt":[{"type":"text","text":"List all TypeScript files"}]}}\n')
   
5. process.poll(sessionId: "bg_42") every 2 sec until stopReason
   -> Collect all session/update content
   -> Final response: stopReason: "end_turn"

6. When done: process.kill(sessionId: "bg_42")
```

---

## 恢复会话

通过让用户从可用会话中选择来恢复之前的 OpenCode 会话。

### 第 1 步：列出可用会话

```
bash(command: "opencode session list", workdir: "/path/to/project")
```

示例输出：
```
ID                                  Updated              Messages
ses_451cd8ae0ffegNQsh59nuM3VVy      2026-01-11 15:30     12
ses_451a89e63ffea2TQIpnDGtJBkS      2026-01-10 09:15     5
ses_4518e90d0ffeJIpOFI3t3Jd23Q      2026-01-09 14:22     8
```

### 第 2 步：询问用户选择

向用户展示会话列表，并询问要恢复哪个会话：

```
"Which session would you like to resume?
 
1. ses_451cd8ae... (12 messages, updated 2026-01-11)
2. ses_451a89e6... (5 messages, updated 2026-01-10)
3. ses_4518e90d... (8 messages, updated 2026-01-09)

Enter session number or ID:"
```

### 第 3 步：加载选定的会话

用户响应后（例如，输入“1”、“第一个”或“ses_451cd8ae...”）：

1. **启动 OpenCode ACP**：
   ```
   bash(command: "opencode acp", background: true, workdir: "/path/to/project")
   ```

2. **初始化**：
   ```json
   {"jsonrpc":"2.0","id":0,"method":"initialize","params":{...}}
   ```

3. **加载会话**：
   ```json
   {"jsonrpc":"2.0","id":1,"method":"session/load","params":{"sessionId":"ses_451cd8ae0ffegNQsh59nuM3VVy","cwd":"/path/to/project","mcpServers":[]}}
   ```

**注意**：`session/load` 需要 `cwd` 和 `mcpServers` 参数。

加载会话后，OpenCode 会将完整的对话历史记录流式传输给您。

### 恢复会话的工作流程总结

```
function resumeSession(workdir):
    # List available sessions
    output = bash("opencode session list", workdir: workdir)
    sessions = parseSessionList(output)
    
    if sessions.empty:
        notify("No previous sessions found. Starting fresh.")
        return createNewSession(workdir)
    
    # Ask user to choose
    choice = askUser("Which session to resume?", sessions)
    selectedId = matchUserChoice(choice, sessions)
    
    # Start OpenCode and load session
    process = bash("opencode acp", background: true, workdir: workdir)
    initialize(process)
    
    session_load(process, selectedId, workdir, mcpServers: [])
    
    notify("Session resumed. Conversation history loaded.")
    return process
```

### 重要说明

- **历史记录重放**：加载会话时，所有之前的消息都会被重新传输
- **数据保留**：代理会记住完整的对话内容
- **进程独立**：会话在 OpenCode 重启后仍然存在

---

## 更新 OpenCode

OpenCode 会在重启时自动更新。使用此工作流程来检查和触发更新。

### 第 1 步：检查当前版本

```
bash(command: "opencode --version")
```

返回类似 `opencode version 1.1.13` 的信息

提取版本号（例如，`1.1.13`）。

### 第 2 步：检查最新版本

```
webfetch(url: "https://github.com/anomalyco/opencode/releases/latest", format: "text")
```

重定向 URL 包含最新版本的标签：
- 重定向到：`https://github.com/anomalyco/opencode/releases/tag/v1.2.0`
- 从 URL 路径中提取版本号（例如，`1.2.0`）

### 第 3 步：比较并更新

如果最新版本高于当前版本：

1. **停止所有正在运行的 OpenCode 进程**：
   ```
   process.list()  # Find all "opencode acp" processes
   process.kill(sessionId) # For each running instance
   ```

2. **重启实例**（OpenCode 会在启动时自动下载新版本）：
   ```
   bash(command: "opencode acp", background: true, workdir: "/path/to/project")
   ```

3. **重新初始化** 每个实例（对现有会话执行初始化和加载操作）

### 第 4 步：验证更新

```
bash(command: "opencode --version")
```

如果版本号仍然不匹配最新版本：
- 通知用户：“OpenCode 自动更新可能失败。当前版本：X.X.X，最新版本：Y.Y.Y”
- 建议手动更新：`curl -fsSL https://opencode.dev/install | bash`

### 更新工作流程总结

```
function updateOpenCode():
    current = bash("opencode --version")  # e.g., "1.1.13"
    
    latestPage = webfetch("https://github.com/anomalyco/opencode/releases/latest")
    latest = extractVersionFromRedirectUrl(latestPage)  # e.g., "1.2.0"
    
    if semverCompare(latest, current) > 0:
        # Stop all instances
        for process in process.list():
            if process.command.includes("opencode"):
                process.kill(process.sessionId)
        
        # Wait briefly for processes to terminate
        sleep(2 seconds)
        
        # Restart triggers auto-update
        bash("opencode acp", background: true)
        
        # Verify
        newVersion = bash("opencode --version")
        if newVersion != latest:
            notify("Auto-update may have failed. Manual update recommended.")
    else:
        notify("OpenCode is up to date: " + current)
```

### 重要说明

- **会话持久化**：`opencodeSessionId` 在重启后仍然有效——使用 `session/load` 来恢复会话
- **自动更新**：OpenCode 会在重启时自动下载新版本
- **数据不丢失**：对话历史记录会保存在服务器端