---
name: opencode-acp-control
description: 可以通过代理客户端协议（Agent Client Protocol, ACP）直接控制 OpenCode。该协议支持启动会话、发送提示信息、恢复对话以及管理 OpenCode 的更新。此外，还具备自动恢复功能、检测会话是否陷入僵局（即无法继续进行）以及会话管理的能力。
metadata: {"version": "2.0.0", "author": "Bastian Berrios <bastianberrios.a@gmail.com>", "license": "MIT", "github_url": "https://github.com/berriosb/Opencode-Acp-Control"}
---
# OpenCode ACP Skill v2.0

通过代理客户端协议（ACP）直接控制OpenCode，支持**自动恢复**和**卡顿检测**功能。

## 🆕 v2.0的新功能

| 功能 | 描述 |
|---------|-------------|
| **自动重试** | 在失败时自动重试（最多3次） |
| **卡顿检测** | 检测OpenCode是否无响应 |
| **锁定文件清理** | 自动删除过期的锁定文件 |
| **自适应轮询** | 启动时轮询频率较高，运行稳定后轮询频率降低 |
| **健康检查** | 定期检查OpenCode是否正常运行 |
| **可配置的超时时间** | 支持自定义超时时间，并在超时时进行升级处理 |
| **会话恢复** | 可以在任务执行过程中崩溃后恢复 |

---

## 快速参考

| 操作 | 方法 |
|--------|-----|
| 启动OpenCode | `exec(command: "opencode acp --cwd /path", background: true)` |
| 发送消息 | `process.write(sessionId, data: "<json-rpc>\n")` |
| 读取响应 | `process.poll(sessionId)` - 使用自适应轮询 |
| 健康检查 | `process.poll(sessionId, timeout: 5000)` - 仅在没有输出超过60秒时执行 |
| 停止OpenCode | `process.kill(sessionId)` + 清理锁定文件 |
| 清理锁定文件 | `exec(command: "rm -f ~/.openclaw/agents/*/sessions/*.lock")` |
| 列出会话 | `exec(command: "opencode session list", workdir: "...")` |
| 恢复会话 | 列出会话 → `session/load` |

---

## 🚀 快速入门（简单流程）

对于大多数使用场景，可以使用以下简单的工作流程：

```
1. exec(command: "opencode acp --cwd /path/to/project", background: true)
   -> sessionId: "bg_42"

2. process.write(sessionId: "bg_42", data: initialize_json + "\n")
   process.poll(sessionId: "bg_42", timeout: 10000)

3. process.write(sessionId: "bg_42", data: session_new_json + "\n")
   process.poll(sessionId: "bg_42", timeout: 10000)
   -> opencodeSessionId: "sess_xyz"

4. process.write(sessionId: "bg_42", data: prompt_json + "\n")
   adaptivePoll(sessionId: "bg_42", maxWaitMs: 120000)

5. When done: process.kill(sessionId: "bg_42")
   cleanupLocks()
```

---

## 📁 技能文件

| 文件 | 用途 |
|------|---------|
| `SKILL.md` | 主要文档 |
| `config.default.json` | 默认配置（复制到`config.json`进行自定义） |
| `templates.md` | 常见任务的提示模板 |

---

## ⚙️ 配置

### 选项1：使用默认设置
所有默认设置都已内置，无需配置文件。

### 选项2：自定义配置
将`config.default.json`复制到同一文件夹下的`config.json`文件，并进行修改：

```bash
cp config.default.json config.json
# Edit config.json with your preferences
```

**配置结构：**
```json
{
  "timeouts": { "initialize": 10000, "prompt": {...} },
  "retry": { "maxAttempts": 3, "initialDelay": 2000 },
  "polling": { "initial": 1000, "active": 2000 },
  "healthCheck": { "noOutputThreshold": 60000 },
  "recovery": { "autoRecover": true },
  "mcpServers": { "default": [], "supabase": ["supabase"] }
}
```

---

### 超时时间（可配置）

| 操作 | 默认值 | 最大值 | 何时需要增加超时时间 |
|-----------|---------|-----|------------------|
| 初始化 | 10秒 | 30秒 | 适用于运行缓慢的机器 |
| 新会话创建 | 10秒 | 30秒 | 适用于大型项目 |
| 简单提示 | 60秒 | 120秒 | 适用于复杂查询 |
| 复杂提示 | 120秒 | 300秒 | 适用于重构或代码生成 |
| 健康检查 | 5秒 | 10秒 | 适用于网络问题 |

### 重试配置

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| 最大重试次数 | 3次 | 失败后重试的次数 |
| 重试间隔 | 2秒 | 每次重试之间的延迟时间 |
| 重试倍增因子 | 2 | 每次重试后的延迟时间翻倍 |
| 最大重试间隔 | 10秒 | 最大重试间隔时间 |

### 自适应轮询

| 阶段 | 轮询间隔 | 轮询持续时间 |
|-------|----------|----------|
| 初始阶段 | 1秒 | 开始的10秒内 |
| 活动阶段 | 2秒 | 10秒至60秒 |
| 稳定阶段 | 3秒 | 60秒至120秒 |
| 运行缓慢阶段 | 5秒 | 120秒以上 |

---

## 🔄 自动恢复

### 卡顿检测

当满足以下条件时，OpenCode被视为“卡顿”：
- 超过两次预期超时时间后仍未响应 |
- 连续三次健康检查失败 |
- 进程仍在运行但未响应轮询请求

### 恢复步骤

检测到卡顿时，将执行以下操作：

```
1. Cancel current operation: session/cancel
2. Wait 2 seconds
3. If still stuck: process.kill
4. Clean up locks
5. Restart OpenCode
6. Resume from last known session (if available)
```

### 锁定文件清理

当OpenCode崩溃时，锁定文件可能会变得无效。请务必定期清理这些文件：

```bash
# Before starting a new session
exec(command: "find ~/.openclaw/agents -name '*.lock' -mmin +30 -delete")

# After killing a stuck process
exec(command: "rm -f ~/.openclaw/agents/*/sessions/*.lock")
```

---

## 📋 逐步操作流程

### 第1步：预检查

在开始之前，验证环境是否满足运行要求：

```bash
# Check OpenCode is installed
exec(command: "opencode --version")

# Clean stale locks (older than 30 minutes)
exec(command: "find ~/.openclaw/agents -name '*.lock' -mmin +30 -delete")
```

### 第2步：启动OpenCode

```bash
exec(
  command: "opencode acp --cwd /path/to/project",
  background: true,
  workdir: "/path/to/project"
)
# Save sessionId for all subsequent operations
```

### 第3步：初始化（包含重试机制）

```json
// Send initialize
{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{"fs":{"readTextFile":true,"writeTextFile":true},"terminal":true},"clientInfo":{"name":"clawdbot","title":"Clawdbot","version":"2.0.0"}}}
```

**重试逻辑：**
```
for attempt in 1..3:
    process.write(sessionId, initialize_json + "\n")
    response = process.poll(sessionId, timeout: 10000)
    
    if response contains protocolVersion:
        break  # Success
    
    if attempt < 3:
        sleep(2 * attempt)  # Backoff: 2s, 4s
    else:
        # Recovery mode
        process.kill(sessionId)
        cleanupLocks()
        restart from Step 2
```

### 第4步：创建会话（包含重试机制）

```json
{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":"/path/to/project","mcpServers":[]}}
```

**重试逻辑与初始化步骤相同。**

### 第5步：发送提示（使用自适应轮询）

```json
{"jsonrpc":"2.0","id":2,"method":"session/prompt","params":{"sessionId":"sess_xyz","prompt":[{"type":"text","text":"Your question here"}]}}
```

**自适应轮询机制：**
```
elapsed = 0
interval = 1000  # Start at 1s
maxWait = 120000  # 2 minutes for complex tasks

while elapsed < maxWait:
    response = process.poll(sessionId, timeout: interval)
    
    if response contains stopReason:
        return response  # Done
    
    if response contains error:
        handle_error(response)
        break
    
    # Adaptive interval
    elapsed += interval
    if elapsed < 10000:
        interval = 1000      # First 10s: poll every 1s
    elif elapsed < 60000:
        interval = 2000      # 10-60s: poll every 2s
    elif elapsed < 120000:
        interval = 3000      # 60-120s: poll every 3s
    else:
        interval = 5000      # 120s+: poll every 5s

# Timeout reached - check if stuck
if is_stuck(sessionId):
    recover(sessionId)
```

### 第6步：健康检查（智能判断，避免浪费令牌）

**⚠️ 不要频繁进行健康检查——会浪费令牌！**
仅在以下情况下进行健康检查：
- 超过60秒没有输出（可能表示卡顿）
- 接近超时时间（在宣布卡顿之前进行验证）
- 发生异常（如部分错误等）

**以下情况无需进行健康检查：**
- OpenCode正在积极生成输出
- 自上次输出后不到60秒

```
# Smart health check - only when needed
if time_since_last_output > 60000:  # 60s
    response = process.poll(sessionId, timeout: 5000)
    
    if response contains new data:
        last_output_time = now()
        continue  # Not stuck, just slow
    
    if response is "Process still running" with no data:
        # Still alive, just thinking - wait more
        continue
    
    if response is "No active session":
        # Process died - recover
        recover(sessionId)
```

### 第7步：清理操作

完成后，务必清理相关资源：

```
process.kill(sessionId)
exec(command: "rm -f ~/.openclaw/agents/*/sessions/*.lock")
```

---

## 🛠️ 错误处理

### 常见错误及解决方法

| 错误 | 检测方法 | 解决方案 |
|-------|-----------|----------|
| 进程崩溃 | `process.poll`返回“无活跃会话” | 重启OpenCode并恢复会话 |
| 卡顿（无响应） | 超过两次超时后仍未响应 | 取消操作，杀死进程，清理锁定文件，然后重启 |
| 存在锁定文件 | 之前运行生成的`.lock`文件 | 删除超过30分钟的过期锁定文件 |
| JSON解析错误 | 响应格式错误 | 跳过错误行，继续轮询 |
| 超时 | `elapsed >= maxWait` | 检查是否卡顿，然后重试或采取其他措施 |
| 被限制请求速率 | OpenCode返回HTTP 429错误 | 使用指数级退避策略，最大延迟10秒 |

### 恢复函数

```
function recover(sessionId, opencodeSessionId):
    # Step 1: Try to cancel gracefully
    process.write(sessionId, cancel_json + "\n")
    sleep(2000)
    
    # Step 2: Check if recovered
    response = process.poll(sessionId, timeout: 5000)
    if response is valid:
        return  # Recovered!
    
    # Step 3: Force kill
    process.kill(sessionId)
    
    # Step 4: Clean up
    exec("rm -f ~/.openclaw/agents/*/sessions/*.lock")
    
    # Step 5: Restart
    newSessionId = startOpenCode()
    initialize(newSessionId)
    
    # Step 6: Resume if we had a session
    if opencodeSessionId:
        session_load(newSessionId, opencodeSessionId)
    
    return newSessionId
```

---

## 🔌 会话管理

### 多个会话

OpenCode支持同时处理多个会话。请妥善管理这些会话：

```json
{
  "sessions": {
    "process_42": {
      "processSessionId": "bg_42",
      "opencodeSessionId": "sess_abc",
      "project": "/path/to/project1",
      "lastActivity": "2026-03-05T10:00:00Z",
      "status": "active"
    },
    "process_43": {
      "processSessionId": "bg_43",
      "opencodeSessionId": "sess_def",
      "project": "/path/to/project2",
      "lastActivity": "2026-03-05T09:30:00Z",
      "status": "idle"
    }
  }
}
```

### 会话恢复

如果OpenCode在任务执行过程中崩溃：

```
1. Find the last opencodeSessionId
2. Start new OpenCode process
3. Initialize
4. session/load with the old sessionId
5. Continue from where it left off
```

---

## 📊 监控

### 健康指标

通过以下指标可以提前发现潜在问题：

| 指标 | 正常 | 警告 | 危险 |
|--------|---------|---------|----------|
| 响应时间 | <5秒 | 5-15秒 | >15秒 |
| 无数据的轮询次数 | <10次 | 10-30次 | >30次 |
| 锁定文件存活时间 | <5分钟 | 5-30分钟 | >30分钟 |
| 连续错误次数 | 0次 | 1-2次 | ≥3次 |

### 日志记录

记录重要事件以便调试：

```
[2026-03-05 10:00:00] Started OpenCode, sessionId=bg_42
[2026-03-05 10:00:02] Initialized successfully
[2026-03-05 10:00:03] Created session sess_abc
[2026-03-05 10:00:05] Sent prompt: "Refactor auth module"
[2026-03-05 10:00:15] Received update (thinking)
[2026-03-05 10:00:45] Received update (tool use)
[2026-03-05 10:01:30] Completed, stopReason=end_turn
```

---

## 🎯 最佳实践

### 应该做的：
- ✅ 在开始前务必清理锁定文件 |
- ✅ 使用自适应轮询机制（节省令牌） |
- ✅ 实现重试逻辑（提高系统稳定性） |
- ✅ 跟踪会话状态（便于恢复） |
- ✅ 根据任务类型设置合适的超时时间 |
- ✅ 如果卡顿时间超过两次超时限制，立即重启进程 |

### 不应该做的：
- ❌ 每2秒轮询一次（浪费令牌） |
- ✅ 在输出正常时每30秒进行健康检查（浪费令牌） |
- ❌ 忽略卡顿的进程（影响后续操作） |
- ❌ 卡顿后不清理锁定文件 |
- ❌ 对所有操作使用相同的超时设置 |
- ❌ 在输出超过60秒时忽略健康检查（错过卡顿检测）

---

## 📝 示例：稳健的实现方式

```
# State tracking
state = {
  processSessionId: null,
  opencodeSessionId: null,
  messageId: 0,
  retries: 0,
  lastActivity: null
}

# Start with cleanup
cleanupStaleLocks()

# Start OpenCode
state.processSessionId = exec("opencode acp --cwd /path", background: true)

# Initialize with retry
for attempt in 1..3:
  process.write(state.processSessionId, initialize())
  response = process.poll(state.processSessionId, timeout: 10000)
  
  if is_valid(response):
    break
  
  if attempt == 3:
    throw Error("Failed to initialize after 3 attempts")

# Create session with retry
for attempt in 1..3:
  process.write(state.processSessionId, session_new())
  response = process.poll(state.processSessionId, timeout: 10000)
  
  if is_valid(response):
    state.opencodeSessionId = response.result.sessionId
    break
  
  if attempt == 3:
    throw Error("Failed to create session after 3 attempts")

# Send prompt with adaptive polling
process.write(state.processSessionId, prompt(state.messageId, "Your task"))

elapsed = 0
interval = 1000
maxWait = 120000

while elapsed < maxWait:
  response = process.poll(state.processSessionId, timeout: interval)
  state.lastActivity = now()
  
  if contains_stop_reason(response):
    return parse_response(response)
  
  elapsed += interval
  interval = get_adaptive_interval(elapsed)
  
  # Smart health check - only if no output for >60s
  if elapsed > 60000 && no_recent_output:
    if is_stuck(state.processSessionId):
      state = recover(state)
      # Re-send prompt
      process.write(state.processSessionId, prompt(state.messageId, "Your task"))
      elapsed = 0

# Timeout
throw Error("Operation timed out after ${maxWait}ms")
```

---

## 🔧 实用工具函数

### cleanupStaleLocks()

```bash
# Remove locks older than 30 minutes
find ~/.openclaw/agents -name '*.lock' -mmin +30 -delete
```

### isStuck(sessionId)

```
# Check if process is alive but not responding
response = process.poll(sessionId, timeout: 5000)
return response == "Process still running" && no_data_for_60s
```

### getAdaptiveInterval(elapsedMs)

```
if elapsedMs < 10000: return 1000
if elapsedMs < 60000: return 2000
if elapsedMs < 120000: return 3000
return 5000
```

---

## 📝 提示模板

请参阅`templates.md`文件，其中包含常见任务的预设提示模板：

| 类别 | 模板内容 |
|----------|-----------|
| **重构** | 提取函数、转换为TypeScript、提高代码可读性 |
| **功能添加** | 添加新的API端点、组件或实现新功能 |
| **错误修复** | 调试和修复代码错误 |
| **测试** | 编写单元测试和集成测试 |
| **文档编写** | 更新JSDoc/TSDoc文档和README文件 |
| **数据库** | 数据库迁移和配置RLS策略 |
| **性能优化** | 优化查询效率和打包文件大小 |
| **安全性** | 进行安全审计 |

**使用方法：**
```
1. Read templates.md
2. Find appropriate template
3. Replace placeholders with your specifics
4. Send as prompt
```

---

## 📊 监控指标

### 用于健康状况监控的指标：

| 指标 | 监测方法 | 正常范围 | 警告范围 | 危险范围 |
|--------|--------------|---------|---------|----------|
| **平均响应时间** | 记录响应时间戳 | <30秒 | 30-60秒 | >60秒 |
| 每次请求的轮询次数 | 计算轮询次数 | <20次 | 20-50次 | >50次 |
| 重试率 | 每次请求的重试次数 | <5% | 5-15% | >15% |
| 卡顿率 | 卡顿发生的会话比例 | <1% | 1-5% | >5% |
| 成功率 | 完成的会话比例 | >95% | 85-95% | <85% |

### 日志记录格式：

```
[2026-03-05 10:00:00] INFO: Started OpenCode, sessionId=bg_42
[2026-03-05 10:00:02] INFO: Initialized successfully
[2026-03-05 10:00:03] INFO: Created session sess_abc
[2026-03-05 10:00:05] INFO: Sent prompt (refactor)
[2026-03-05 10:00:15] DEBUG: Received update (thinking)
[2026-03-05 10:00:45] DEBUG: Received update (tool use)
[2026-03-05 10:01:30] INFO: Completed, stopReason=end_turn
[2026-03-05 10:01:31] INFO: Metrics: duration=91s, polls=15, retries=0
```

### 日志级别：
- `ERROR`：表示失败、异常或检测到卡顿 |
- `WARN`：表示重试失败、响应缓慢或接近超时 |
- `INFO`：表示操作开始、完成或清理过程 |
- `DEBUG`：记录详细日志和接收到的更新信息 |

---

## 📦 技能文件列表

```
opencode-acp-control-3/
├── SKILL.md              # This file
├── opencode-session.sh   # Helper script (executable)
├── config.default.json   # Default configuration
├── templates.md          # Prompt templates
├── _meta.json            # Skill metadata
└── .clawhub/             # ClawHub metadata
```

---

## 🚀 建议使用的辅助脚本

**使用`opencode-session.sh`来实现自动化工作流程：**

```bash
# Simple usage
~/.openclaw/workspace/skills/opencode-acp-control-3/opencode-session.sh \
  --project /path/to/project \
  --prompt "Add error handling to the API"

# With template
opencode-session.sh \
  --project ~/myapp \
  --template "Add API endpoint" \
  --prompt "POST /api/users with validation"

# Complex task
opencode-session.sh \
  --project ~/myapp \
  --timeout complex \
  --mcp '["supabase"]' \
  --prompt "Create migration for users table"
```

### 脚本参数说明：

| 参数 | 描述 |
|--------|-------------|
| `--project PATH` | 项目目录（必填） |
| `--prompt "TEXT"` | 要发送的提示内容（如果没有预设模板时使用） |
| `--template NAME` | 使用`templates.md`中的模板 |
| `--timeout TYPE` | 轮询超时类型：简单（60秒）| 中等（120秒）| 复杂（300秒） |
| `--mcp SERVERS` | MCP服务器的JSON数组 |
| `--verbose` | 启用详细日志记录 |
| `--dry-run` | 仅输出JSON-RPC请求，不执行实际操作 |
| `--help` | 显示脚本使用说明 |

**脚本功能：**
- 自动执行完整的工作流程 |
- 包含正确的JSON-RPC请求内容 |
- 提供重试逻辑建议 |
- 设置自适应轮询间隔 |
- 设置健康检查阈值 |
- 提供必要的清理命令

**CYPHER的操作步骤：**
1. 使用相应参数执行脚本 |
2. 解析脚本输出结果 |
3. 按顺序执行脚本中的各个步骤 |
4. 在操作结束后记录相关指标数据

---

*版本2.2.0 - 发布于2026-03-05*
*新增功能：`opencode-session.sh`辅助脚本*