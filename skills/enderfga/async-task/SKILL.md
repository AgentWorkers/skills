# OpenClaw 异步任务

## 说明

该功能用于执行耗时较长的任务，避免因 HTTP 超时而导致任务中断。适用于以下场景：
- 运行可能需要超过 5 秒的命令
- 分析大型文件或代码库
- 执行多步骤操作
- 调用响应时间不可预测的外部 API

**重要提示**：当任务可能超时时，必须使用此功能以避免出现“服务器返回空响应”的错误。

**触发条件**：`async task`、`long running`、`timeout`、`background task`、`push result`

## 安装

```bash
# Clone and link globally
git clone https://github.com/Enderfga/openclaw-async-task.git
cd openclaw-async-task
npm link

# Or just copy async-task.js to your PATH
chmod +x async-task.js
cp async-task.js /usr/local/bin/async-task
```

## 命令

```bash
async-task start "<description>"  # Start task, returns immediately
async-task done "<result>"        # Complete task, push result to user
async-task fail "<error>"         # Task failed, push error message
async-task push "<message>"       # Push message directly (no start needed)
async-task status                 # Show current task status
```

## 使用流程（必须严格遵循）

1. **启动任务**：`async-task start "正在扫描文件..."`
2. **执行实际操作**：运行所需的命令
3. **推送结果**：`async-task done "找到 42 个文件..."`

## 示例

用户请求：“统计该项目中的所有 TypeScript 文件”

```bash
# Step 1: Acknowledge immediately
async-task start "Counting TypeScript files..."

# Step 2: Do the actual work
count=$(find . -name "*.ts" | wc -l)

# Step 3: Push the result
async-task done "Found $count TypeScript files"
```

## 工作原理

1. `start` 命令会立即保存任务状态并返回确认信息。
2. 用户执行所需的命令。
3. `done` 或 `fail` 命令会通过 OpenClaw/Clawdbot CLI 将结果推送到当前的活动会话中。

**无需任何配置**——系统会自动通过 `openclaw sessions` 或 `clawdbot sessions` 检测当前的活动会话。

## 高级功能：自定义推送端点

若需要将结果发送到自定义的 WebChat 或通知系统，可进行如下配置：

```bash
export ASYNC_TASK_PUSH_URL="https://your-server.com/api/push"
export ASYNC_TASK_AUTH_TOKEN="your-token"
```

**推送端点的接收内容**：
```json
{
  "sessionId": "session-id",
  "content": "message",
  "role": "assistant"
}
```

## 环境变量

| 变量          | 是否必填 | 说明                        |
|-----------------|---------|---------------------------|
| `OPENCLAW_SESSION` | 否       | 目标会话（系统自动检测）                |
| `ASYNC_TASK_push_URL` | 否       | 自定义 HTTP 推送端点地址             |
| `ASYNC_TASK_AUTH_TOKEN` | 否       | 自定义端点的认证令牌                 |

## 系统要求

- Node.js 16 及以上版本
- 已安装 OpenClaw 或 Clawdbot CLI

**重要规则**：
- 必须同时使用 `start` 和 `done` 或 `fail` 命令。
- 请勿在未完成任务的情况下直接使用 `done` 命令。
- 请勿承诺“稍后推送结果”后却忘记实际执行推送操作。

## 链接

- [GitHub](https://github.com/Enderfga/openclaw-async-task)
- [OpenClaw](https://openclaw.ai)