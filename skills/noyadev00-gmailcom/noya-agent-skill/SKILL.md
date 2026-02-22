---
name: noya-agent-skill
description: 通过 `curl` 命令与 Noya AI 代理进行交互，以执行加密货币交易、预测市场分析、代币评估以及定期定额投资（DCA）策略的相关操作。当用户需要交易代币、查看投资组合、分析市场行情、管理定期定额投资策略，或与 Polymarket/Rain 预测市场进行交互时，可以使用该命令。
metadata: {"openclaw":{"emoji":"🤖","homepage":"https://agent.noya.ai","requires":{"env":["NOYA_API_KEY"],"bins":["curl","jq"]},"primaryEnv":"NOYA_API_KEY"}}
---
# Noya Agent

Noya 是一个多智能体 AI 系统，可用于加密货币交易、预测市场（如 Polymarket、Rain）、代币分析以及定期投资（DCA）策略的制定。所有交易均需要支付网络手续费（“gas fees”），但用户无需额外承担这些费用。

- **官方网站：** [agent.noya.ai](https://agent.noya.ai)
- **API 基本地址：** `https://safenet.one`

## 信任与安全

- 所有 API 调用均使用 HTTPS 协议。系统仅从环境变量中读取 `NOYA_API_KEY`。
- 所有链上交易在执行前都需要用户明确确认。
- 测试期间请使用临时 API 密钥（有效期为 30 天）。若密钥被泄露，请在设置 > API 密钥中将其撤销。

## 设置

1. 在 [agent.noya.ai](https://agent.noya.ai) 注册账户。
2. 进入设置 > API 密钥，生成新的 API 密钥。
3. 请妥善保管该密钥（该密钥仅会显示一次）。
4. 设置环境变量：

```bash
export NOYA_API_KEY="noya_your_key_here"
```

在 `~/.openclaw/openclaw.json` 文件中进行配置：

```json
{
  "skills": {
    "entries": {
      "noya-agent": {
        "enabled": true,
        "apiKey": "noya_your_key_here",
        "env": {
          "NOYA_API_KEY": "noya_your_key_here"
        }
      }
    }
  }
}
```

## 使用场景

当用户需要执行以下操作时，可以使用 Noya：
- 查看代币价格或投资组合余额
- 进行代币交易、跨链操作或发送代币
- 分析代币市场趋势
- 在 Polymarket 或 Rain 预测市场上进行交易
- 设置或管理定期投资策略
- 查看去中心化金融（DeFi）持仓情况
- 与 Noya 代理进行语音对话

**不适用场景：** 非加密货币相关任务、本地文件操作或一般性知识查询。

## 核心工作流程

所有交互均通过 Noya 的 REST API 完成。主要接口为 `POST /api/messages/stream`，该接口会返回流式响应。**务必使用提供的 `noya-message.sh` 脚本** 来发送消息——该脚本负责处理数据流、解析数据块并生成格式化输出。切勿直接使用 `curl` 命令调用该接口。

### 1. 了解 Noya 的功能（首次使用）

调用该接口可获取 Noya 支持的所有功能（代币分析、预测市场、定期投资等）及其相关工具。只需调用一次即可了解 Noya 的全部能力。

### 2. 生成对话线程 ID（新对话）

为每个新对话生成一个唯一的 UUID v4：

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

在 macOS/Linux 系统上，也可以使用以下命令：

```bash
uuidgen | tr '[:upper:]' '[:lower:]'
```

每个对话都需要一个唯一的 UUID。请为每个对话生成一个 UUID，并在后续对话中重复使用它。

### 3. 发送消息（流式传输）

使用提供的脚本发送消息并接收解析后的响应：

```bash
bash {baseDir}/noya-message.sh "What tokens do I have in my portfolio?" "THREAD_ID_HERE"
```

该脚本会处理流式响应，解析以 `--breakpoint--` 为分隔符的 JSON 数据块，并输出格式化的文本（包括消息内容、工具结果、进度提示等）。

### 4. 继续对话

后续对话请使用相同的线程 ID——Noya 会保留对话上下文。

```bash
bash {baseDir}/noya-message.sh "Swap 0.1 ETH to USDC" "SAME_THREAD_ID"
```

### 5. 回应用户指令

当 Noya 需要用户确认操作（例如执行代币交易）时，响应中会包含 `[REQUIRES INPUT]` 字样及相关选项。用户需在同一对话线程中回复确认信息。

```bash
bash {baseDir}/noya-message.sh "Yes" "SAME_THREAD_ID"
```

## 启动语音聊天

用户可以在浏览器中开启 Noya 代理的语音聊天模式。适合希望通过语音与 Noya 交流的情况。

**启动新语音对话：**

```bash
open "https://agent.noya.ai?mode=voice"
```

**在语音模式下恢复特定对话**（传递现有的线程 ID）：

```bash
open "https://agent.noya.ai?mode=voice&threadIdToUse=THREAD_ID_HERE"
```

在 Linux 系统上，建议使用 `xdg-open` 而不是 `open` 命令。`threadIdToUse` 参数是可选的——省略该参数即可开始新的语音会话。

## API 参考（curl 命令）

所有 API 调用都需要添加 `x-api-key` 头部信息。基础地址为 `https://safenet.one`。

### 发送消息（流式传输）——务必使用脚本

**切勿直接使用 `curl` 命令调用 `/api/messages/stream`。** 该接口返回的响应为自定义的流式数据格式，需要使用脚本进行解析。务必使用提供的 `noya-message.sh` 脚本：

```bash
bash {baseDir}/noya-message.sh "<message>" "<threadId>"
```

该脚本负责处理身份验证、数据流传输、数据块解析，并生成格式化的输出（包括消息、工具结果、进度提示等）。

### 列出所有对话线程

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/threads" | jq '.data.threads'
```

### 获取对话内容

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/threads/THREAD_ID/messages" | jq '.data.messages'
```

### 删除对话线程

```bash
curl -s -X DELETE -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/threads/THREAD_ID"
```

### 获取代理信息摘要

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/agents/summarize" | jq '.data'
```

### 获取用户信息摘要（所有持仓、定期投资策略、Polymarket 交易记录）

该接口会返回与当前登录用户相关的所有信息摘要，非常适合用于传递给其他智能体作为上下文数据。

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/user/summary" | jq '.data'
```

响应内容包括：
- `holdings`：所有钱包中的代币及去中心化金融应用持仓（附带美元价值）
- `dcaStrategies`：所有定期投资策略（活跃状态、非活跃状态、错误状态、已完成状态）
- `polymarket.openPositions`：当前在 Polymarket 上的未平仓交易记录（包含盈亏情况）
- `polymarket.closedPositions`：最近 20 笔已平仓的交易记录

### 结束对话（兼容 OpenAI，不支持代理工具）

```bash
curl -s -X POST "https://safenet.one/api/chat/completions" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $NOYA_API_KEY" \
  -d '{"sessionId": "SESSION_ID", "message": "Hello, what can you do?"}'
```

### 获取会话历史记录

```bash
curl -s -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/chat/session/SESSION_ID" | jq '.messages'
```

### 清除会话记录

```bash
curl -s -X DELETE -H "x-api-key: $NOYA_API_KEY" \
  "https://safenet.one/api/chat/session/SESSION_ID"
```

## 常用操作模式

- **查看投资组合**：[此处应添加相应代码]
- **进行代币交易**：[此处应添加相应代码]
- **分析代币市场**：[此处应添加相应代码]
- **制定定期投资策略**：[此处应添加相应代码]
- **为其他智能体提供用户信息**：[此处应添加相应代码]
- **开启语音聊天**：[此处应添加相应代码]

## 重要提示

### 交易确认

Noya 在执行任何链上交易（如代币交易、跨链操作等）前，总会要求用户确认。响应中会包含 `[REQUIRES INPUT]` 字样及具体操作选项。务必将确认信息传达给用户，并在相同对话线程中接收用户的回复。切勿自动执行交易。

### 钱包委托（仅限网站操作）

如果 Noya 显示 **委托请求**，用户需在官方网站上完成相关操作：

```
"To delegate your wallet, visit https://agent.noya.ai and click
'Delegate Wallet' in the chat. This is a one-time action."
```

### 安全部署（仅限网站操作）

如果 Noya 显示 **安全部署请求**，用户需在官方网站上完成相关操作：

```
"To deploy your Polymarket Safe, visit https://agent.noya.ai and click
'Deploy Safe Now'. This is free, takes ~30 seconds, and only needs to be done once."
```

## 错误处理

| 错误代码 | 处理方法 |
|---------|-----------|
| `401 Unauthorized` | API 密钥无效、过期或已被撤销。请在 [agent.noya.ai] 重新生成密钥。|
| `400 Bad Request` | 请求体中缺少 `message` 或 `threadId` 参数。|
| `429 Rate limit` | 等待几分钟后再尝试。每 5 分钟内最多允许 15 次请求。|

## 脚本说明

该技能目录中包含以下脚本：

| 脚本 | 用途 |
|--------|---------|
| `noya-message.sh` | 向 Noya 代理发送消息并解析返回的流式响应。使用方法：`bash {baseDir}/noya-message.sh "<message>" "<threadId>"` |

## 额外资源

- 完整的 REST API 规范请参阅 [reference.md](reference.md)。