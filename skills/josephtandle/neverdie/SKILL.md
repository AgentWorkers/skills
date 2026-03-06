---
name: neverdie
description: Your OpenClaw should never have zero LLMs. NeverDie protects against the silent killer — every model in your fallback chain going down at once. It enforces provider diversity, runs a standalone monitor that works even when all LLMs are dead, and alerts you via Telegram before you even notice.
read_when:
  - User asks about fallback, resilience, or neverdie
  - User mentions model failure or LLM down
  - User wants to ensure OpenClaw is always available
  - User asks to check LLM resilience or health
metadata: {"clawdbot":{"emoji":"\ud83d\udee1\ufe0f","requires":{"bins":["node"]}}}
---

# NeverDie — LLM 弹性技能

该技能通过实施多样化的提供商 fallback 链路、部署独立的监控工具（无需 LLM），并在发生问题时通过 Telegram 发送警报，来确保 OpenClaw 能够在模型故障时继续运行。

## 核心原则：提供商多样性

**禁止** 连续使用来自同一提供商的 3 个或更多模型**。应交替使用不同的提供商，以防止某个提供商的故障导致整个系统崩溃。**务必** 将本地模型（Ollama）作为最后的备用方案——本地模型不会受到速率限制、身份验证问题或网络故障的影响。

**正确的配置示例**：`anthropic/claude-haiku-4-5` → `openai/gpt-4.1-mini` → `ollama/llama3.2:3b`  
**错误的配置示例**：`anthropic/claude-haiku-4-5` → `anthropic/claude-sonnet-4-6` → `anthropic/claude-opus-4-6`

## 操作步骤

### 1. 诊断当前配置

**仅** 读取 `~/.openclaw/openclaw.json` 文件中的模型配置信息（**不要** 读取或输出 API 密钥、令牌或身份验证配置）：
- 检查 `primary` 和 `fallbacks` 配置项，确保使用的是不同提供商的模型。
- 如果所有模型都来自同一提供商，请标记出来。
- 如果系统中没有本地模型（Ollama），也请标记出来。
- 如果 `NeverDie` 监控任务缺失或被禁用，也请标记出来。

```bash
node -e "
  const cfg = JSON.parse(require('fs').readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const m = cfg.agents.defaults.model;
  console.log('Primary:', m.primary);
  console.log('Fallbacks:', JSON.stringify(m.fallbacks));
  const providers = [m.primary, ...m.fallbacks].map(id => id.split('/')[0]);
  const unique = [...new Set(providers)];
  console.log('Providers:', unique.join(', '));
  if (unique.length < 2) console.log('WARNING: All models from same provider!');
  if (!providers.includes('ollama')) console.log('WARNING: No local Ollama fallback!');
"
```

**安全提示**：此脚本仅输出模型 ID 和提供商名称，**不会** 从配置文件中读取或显示 API 密钥、令牌或凭证。

### 2. 配置多样化的 fallback 链路

确保 fallback 链路中至少包含 2 个不同的云服务提供商和 1 个本地模型（Ollama）。推荐配置模式如下：

```json
{
  "primary": "anthropic/claude-haiku-4-5",
  "fallbacks": [
    "openai/gpt-4.1-mini",
    "ollama/llama3.2:3b",
    "nvidia/moonshotai/kimi-k2.5"
  ]
}
```

**规则**：
- **主要模型** 应该是处理当前工作负载最快/成本最低的模型。
- **第一个 fallback 模型** 必须来自不同的云服务提供商。
- **Ollama** 应始终被包含在 fallback 链路中（理想位置为第 2 或第 3 个模型）。
- 其他提供商的 fallback 模型可以提供额外的冗余保障。

### 3. 部署独立的监控工具

将监控脚本复制到工作区：

```bash
cp ~/.openclaw/workspace/skills/neverdie/scripts/fallback-monitor.js ~/.openclaw/workspace/fallback-monitor.js
chmod +x ~/.openclaw/workspace/fallback-monitor.js
```

该监控工具从 `~/.openclaw/workspace/.neverdie-config.json` 文件中读取配置信息：

```json
{
  "telegramBotToken": "YOUR_BOT_TOKEN",
  "telegramChatId": "YOUR_CHAT_ID",
  "cooldownMinutes": 15,
  "timezone": "UTC",
  "hostname": "my-openclaw"
}
```

使用 Telegram 是可选的。即使不使用 Telegram，监控工具也会将警报信息写入 `.fallback-alert-latest.json` 文件和标准输出（stdout）。

如果配置文件不存在，系统会使用环境变量：
- `NEVERDIE_TELEGRAM_TOKEN`
- `NEVERDIE_TELEGRAM_chat_ID`

### 4. 注册 Cron 任务

添加一个 `systemEvent` 类型的 Cron 任务（**注意**：此任务需要在所有 LLM 服务都不可用时仍然执行）。

请使用监控工具的完整绝对路径（而非 `~/`）来配置任务：

```json
{
  "id": "<generate-uuid>",
  "agentId": "main",
  "name": "NeverDie Fallback Monitor",
  "enabled": true,
  "createdAtMs": <now>,
  "updatedAtMs": <now>,
  "schedule": {
    "kind": "every",
    "everyMs": 300000,
    "anchorMs": <now>
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "exec:node /home/USER/.openclaw/workspace/fallback-monitor.js"
  },
  "delivery": {
    "mode": "announce",
    "channel": "session",
    "bestEffort": true
  },
  "state": {}
}
```

### 5. 配置警报机制

请求用户提供他们的 Telegram 机器人令牌和聊天 ID，然后将其保存到 `~/.openclaw/workspace/.neverdie-config.json` 文件中。

获取这些信息的步骤如下：
1. 在 Telegram 上给 `@BotFather` 发送消息 `/newbot`，然后复制收到的令牌。
2. 向机器人发送消息，接着访问 `https://api.telegram.org/bot<TOKEN>/getUpdates` 以获取聊天 ID。

**注意**：即使不使用 Telegram，监控工具也能正常工作（仅通过文件和标准输出发送警报）。

### 6. 验证配置

```bash
# Check status
node ~/.openclaw/workspace/fallback-monitor.js --status

# Send a test Telegram alert
node ~/.openclaw/workspace/fallback-monitor.js --test

# Normal run (scan logs)
node ~/.openclaw/workspace/fallback-monitor.js
```

### 7. 检查系统状态

当用户询问 NeverDie 的运行状态时，运行 `node ~/.openclaw/workspace/fallback-monitor.js --status`，并检查以下内容：
- **fallback 链路**：读取 `openclaw.json` 文件，确认提供商的多样性。
- **监控任务**：检查 `jobs.json` 文件中是否配置了该任务？任务是否已启用？上次运行的状态如何？
- **Ollama**：确认本地模型是否可以正常访问？

```bash
curl -s --max-time 3 http://localhost:11434/api/tags | node -e "
  let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
    try{const r=JSON.parse(d);console.log('Ollama:',r.models.map(m=>m.name).join(', '))}
    catch(e){console.log('Ollama: NOT REACHABLE')}
  })
"
```

## 监控工具能检测到的问题类型及其严重性

| 问题类型 | 严重程度 | 含义 |
|---------|----------|---------|
| **所有模型都失败** | **严重** | 所有 LLM 服务都无法使用 |
| **负载过重** | **警告** | 某个提供商暂时无法处理请求 |
| **速率限制** / **429 错误** | **警告**：遇到速率限制，系统正在使用 fallback 模型 |
| **身份验证错误** | **严重**：API 密钥无效 |
| **LLM 请求超时** | **警告**：请求超时，可能是暂时性的问题 |
| **ECONNREFUSED** / **网络错误** | **警告**：无法连接到相应的提供商 |

## 安全性措施

- **日志内容不会被外部发送**：Telegram 警报仅包含预定义的固定字符串（例如 “所有模型都失败 — 无 LLM 可用”）。日志摘要和错误详细信息仅保存在本地文件中，不会被传输到外部。
- **代码中不包含敏感信息**：Telegram 机器人令牌在运行时存储在 `.neverdie-config.json` 文件中，**不会** 保存在技能配置文件中。
- **配置信息隔离**：诊断工具仅从 `openclaw.json` 文件中读取模型 ID，**不会** 访问 API 密钥或凭证。
- **无网络依赖**：完全不依赖 npm 包或远程下载，仅使用 Node.js 的内置模块（`fs`、`path`、`https`）。
- **Telegram 是可选的**：即使不使用 Telegram，系统也能通过文件和标准输出发送警报。
- **外部通信限制**：唯一会访问的外部接口是 `apiTelegram.org`，且仅在用户明确配置了 Telegram 服务的情况下才会进行通信。
- **系统独立运行**：监控任务作为 `systemEvent` 类型的 Cron 任务运行，与 LLM 服务的可用性无关。
- **配置可重置**：如果已经存在相应的 Cron 任务，重新配置时系统会跳过该任务。