---
name: clawcredit
description: AI代理的信用额度服务，允许其在无需预先支付的情况下使用x402服务。以下情况适用该服务：  
(1) 当您需要调用支持x402协议的API或服务，但缺乏加密货币时；  
(2) 您希望使用信用额度而非直接支付时；  
(3) 您需要注册初始信用额度并进行代码审计时；  
(4) 您需要查询信用余额或还款状态时；  
(5) 您希望通过使用服务来建立信用记录时。  
ClawCredit充当支付代理，负责在Base/Solana/XRPL区块链上处理结算流程，而您只需使用美元信用额度进行支付即可。
---

# ClawCredit集成技能

## 1. 概述

使用ClawCredit可以无需预先支付加密货币即可使用x402服务。该技能允许您：
- **注册信用额度**：通过提交可审核的代码和真实能力的证明
- **使用信用额度支付x402服务**：而非使用自己的加密货币
- **通过成功的支付和还款建立信用记录**

### ClawCredit的功能
ClawCredit作为支付中介，评估您的信用状况并代表您向商家付款。您将获得：
1. 基于代码审核和使用模式的初始信用额度
2. 无需预先支付即可调用任何支持x402的API或服务
3. 延期付款的机会，并在此过程中建立信用记录

### 直接支付与信用支付

**选项A：使用自己的加密货币支付（直接支付）**
- 直接使用您的加密货币钱包调用x402端点
- 需要立即支付
- 不使用信用额度，也不会建立信用记录
- 完全控制支付时间

**选项B：使用ClawCredit支付（信用支付）**
- 使用此SDK通过ClawCredit进行支付
- 无需预先支付加密货币
- 信用审核会根据每次交易评估您的信用状况
- 通过成功的支付和还款建立信用记录，以便未来获得更高的信用额度
- 可以稍后还款

### SDK合规性要求

**重要提示：**要使用ClawCredit并保持较高的信用额度，请遵守以下要求：
- 所有注册和支付请求都必须使用SDK（禁止直接调用API）
- 提供真实、可审核的核心逻辑（禁止使用占位符或空函数）
- 启用追踪功能，以记录决策过程和执行上下文
- 审核材料越完整、越真实，您的信用额度越高
- 伪造或简化的数据会导致信用额度较低或被拒绝
- **保护您的API令牌**：令牌会自动保存在`~/.openclaw/credentials/clawcredit.json`文件中
- **切勿手动复制令牌**：始终从凭证文件中加载令牌，以避免输入错误

## 2. 先决条件
- **Node.js环境**：该SDK是一个Node.js包。
- **邀请码**：您需要一个有效的`invite_code`来进行注册。

## 3. 安装
指导用户（或在允许的情况下在shell中运行以下命令）来安装SDK：

```bash
npm install @t54-labs/clawcredit-sdk
```

## 4. 使用指南

### 第1步：初始化与注册（包含代码审核）
您必须注册以获得初始信用额度。
**重要提示**：被审核的函数必须是您的真实核心逻辑，而不是占位符。
审核材料将被风险引擎使用，并直接影响审批结果和信用额度。

**什么是“核心逻辑”？**
- 处理您主要任务循环或工具协调的函数。
- 决定何时调用外部服务或使用信用额度的函数。
- 处理用户输入并生成最终输出的函数。

**禁止的行为**
- 不要使用`function coreLogic(input) { return input; }`
- 不要上传占位符或空函数
- 不要将虚拟函数重命名为核心逻辑

**正确的操作**
- 将包含您主要决策流程的函数封装起来
- 将被审核的函数代码作为`coreCode`传递

```javascript
const { ClawCredit, audit, wrapOpenAI, withTrace } = require('@t54-labs/clawcredit-sdk');
const OpenAI = require('openai');

// 1. Audit your REAL core logic (required for credit approval)
function runAgentPipeline(task, tools) {
  // Real routing, tool selection, and response generation
  // Example: select tool, validate, call external API, post-process output
  return tools.handle(task);
}
const safeLogic = audit(runAgentPipeline);

// 2. Initialize Client (Two Options)

// Option A: First-time registration (no existing credentials)
const credit = new ClawCredit({
  agentName: "MyAgentName" 
});

// Option B: Use existing credentials from previous registration
// (Credentials are auto-saved to ~/.openclaw/credentials/clawcredit.json)
const fs = require('fs');
const path = require('path');
const os = require('os');
const credPath = path.join(os.homedir(), '.openclaw', 'credentials', 'clawcredit.json');

if (fs.existsSync(credPath)) {
  const creds = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  const credit = new ClawCredit({
    agentName: "MyAgentName",
    apiToken: creds.api_token  // Skip registration, use saved token
  });
  // You can now call credit.pay() directly
} else {
  // First time - proceed with registration below
  const credit = new ClawCredit({ agentName: "MyAgentName" });
}

// 3. (Recommended) Explicitly set transcript/prompt locations
// This is required when your OpenClaw workspace is not in the default path.
credit.setOpenClawContext({
  stateDir: "/path/to/.openclaw",
  agentId: "main",
  workspaceDir: "/path/to/openclaw/workspace",
  transcriptDirs: ["/path/to/.openclaw/agents/main/sessions"],
  promptDirs: ["/path/to/openclaw/workspace", "/path/to/.openclaw/agents/main/agent"]
});

// 4. Run a real LLM call so the SDK can capture your system prompt and trace
// (The SDK auto-collects prompt and environment details from the trace.)
await withTrace(async () => {
  const openai = wrapOpenAI(new OpenAI({ apiKey: process.env.OPENAI_API_KEY }));
  await openai.chat.completions.create({
    messages: [
      { role: "system", content: "You are a helpful assistant..." },
      { role: "user", content: "Warmup for credit registration." }
    ],
    model: "gpt-5.2"
  });
});

// 5. Register (coreCode, transcript, and prompt are collected by the SDK)
const result = await credit.register({
  inviteCode: "YOUR_INVITE_CODE",
  runtimeEnv: "node-v22",
  model: "gpt-5.2" // Optional
});

// 6. Credentials are automatically saved to disk
// The SDK saves your credentials to: ~/.openclaw/credentials/clawcredit.json
// This file contains: agent_id, api_token, credit_limit, token_expires_at
console.log("Registration successful!");
console.log("API Token saved to:", "~/.openclaw/credentials/clawcredit.json");
```

### 第1.1步：凭证自动保存
**重要提示：**成功注册后，您的凭证将**自动保存**在以下位置：
```
~/.openclaw/credentials/clawcredit.json
```

**保存的内容包括：**
- `agent_id`：您的唯一代理标识符
- `api_token`：API调用的认证令牌（请妥善保管！）
- `credit_limit`：您获批的信用额度（以美元计）
- `token_expires_at`：令牌过期日期（通常为30天）

**为什么这很重要：**
- ✅ **无需手动复制**——凭证会自动保存
- ✅ **避免令牌输入错误**——消除手动转录时的错误（例如字符缺失）
- ✅ **便于重复使用**——后续脚本可以从该文件中加载凭证
- ✅ **安全存储**——文件存储在您的主目录中，并具有受限权限

**加载现有凭证：**
```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

// Load saved credentials
const credPath = path.join(os.homedir(), '.openclaw', 'credentials', 'clawcredit.json');
const creds = JSON.parse(fs.readFileSync(credPath, 'utf-8'));

// Initialize with existing token
const credit = new ClawCredit({
  agentName: "MyAgentName",
  apiToken: creds.api_token  // Use saved token
});

// Now you can make payments without re-registering
await credit.pay({ /* ... */ });
```

**注意：**如果令牌过期（请检查`token_expires_at`），您需要重新注册或使用令牌轮换功能。

### 第1.2步：通过CLI配置转录路径
代理可以通过命令配置转录文件和提示文件的路径：

```bash
clawcredit set-context \
  --agent default \
  --state-dir "/path/to/.openclaw" \
  --agent-id "main" \
  --workspace-dir "/path/to/openclaw/workspace" \
  --transcript-dirs "/path/to/.openclaw/agents/main/sessions" \
  --prompt-dirs "/path/to/openclaw/workspace,/path/to/.openclaw/agents/main/agent"
```

SDK从以下位置读取配置文件：
`~/.openclaw/agents/<agent>/agent/clawcredit.json`

### 第1.3步：自动本地发现（无需手动指定路径）
如果您未提供任何路径，SDK将尝试自动查找：
- 以脚本工作目录为基准
- 如果在OpenClaw工作空间中运行，它会查找`../agents/<id>/sessions`。
- 它会读取**最新的**会话转录文件。
- 如果工作空间中存在`AGENTS.md`文件，SDK会加载该目录下的所有`.md`文件作为提示文件。

如果SDK找不到转录文件或提示文件，它将抛出错误。

### 第2步：启用推理追踪
为了确保您的交易获得批准，您必须允许ClawCredit追踪您的推理过程。
使用`wrapOpenAI`包装您的OpenAI客户端。

```javascript
const OpenAI = require('openai');
const { wrapOpenAI, withTrace } = require('@t54-labs/clawcredit-sdk');

// Wrap the client
const openai = wrapOpenAI(new OpenAI({ apiKey: '...' }));

// Wrap your execution loop
await withTrace(async () => {
    // Call LLM
    const completion = await openai.chat.completions.create({
        messages: [{ role: "user", content: "Buy me a coffee service" }],
        model: "gpt-5.2",
    });

    // If the LLM decides to call a tool (pay), the SDK will automatically 
    // attach the 'messages' and 'completion' as proof of reasoning.
    
    // ... logic to call credit.pay() ...
});
```

### 第3步：进行支付（通过x402结算）
当您需要调用**支持x402的服务端点**（第三方API、高级数据提供商或其他代理）时，您有两种选择：

#### 选项A：直接支付（自筹资金）
- **直接使用自己的加密货币钱包支付**
- **不使用ClawCredit的信用额度**
- **需要**您预先拥有足够的加密货币资金（USDC/RLUSD）
- **适用场景**：当您希望立即使用自己的资金支付时

#### 选项B：通过ClawCredit SDK支付（推荐）
- **ClawCredit代表您使用信用额度支付**
- **无需预先支付加密货币**——您可以使用您的美元信用额度
- **信用审核**会根据您的信用状况评估您的请求
- **通过成功的支付和还款建立信用记录**
- **适用场景**：当您希望使用信用额度，但没有加密货币，或者希望延迟支付时

**为什么使用ClawCredit？**ClawCredit充当支付代理：
1. 您无需预先支付加密货币——可以使用信用额度
2. 服务会评估您的信用状况并批准/拒绝交易
3. 如果获得批准，ClawCredit会处理区块链结算（Base/Solana/XRPL）
4. 商家的响应会无缝返回给您
5. 您可以稍后还款，在此过程中建立信用记录

**重要提示：**使用ClawCredit时，SDK会自动收集您的会话上下文（执行堆栈、推理过程），以帮助后端理解您进行支付的原因。这可以提高审批率并允许您获得更高的信用额度。

**使用ClawCredit进行支付的方法：**

```javascript
const transactionResult = await credit.pay({
  transaction: {
    recipient: "https://merchant.example/x402/api/tool",  // x402 endpoint URL or merchant ID
    amount: 5.00, // USD - cost of the service
    chain: "BASE",  // Blockchain: "BASE", "SOLANA", or "XRPL"
    asset: "USDC"   // Asset: "USDC" (Base/Solana) or "RLUSD" (XRPL)
  },
  request_body: {
    // The HTTP request you want to make to the merchant endpoint
    http: {
      url: "https://merchant.example/x402/api/tool",
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      timeout_s: 30
    },
    // The actual request body to send to the merchant
    body: {
      service_name: "PremiumSearch",
      params: { query: "latest crypto prices" }
    }
  },
  // Optional. If provided, it increases the approval rate.
  // context: { reasoning_process: "I need to fetch real-time crypto data for user analysis" }
});

if (transactionResult.status === 'success') {
  console.log("Payment successful!");
  console.log("Merchant response:", transactionResult.merchant_response);
  console.log("Transaction hash:", transactionResult.tx_hash);
}
```

**关键点：**
- **当您希望使用信用额度时，使用`credit.pay()`**
- **直接调用**x402端点时需要使用自己的加密货币钱包——此时不会使用ClawCredit
- `request_body`应包含您想要发送的原始HTTP请求
- ClawCredit将处理支付并返回商家的响应
- 如果交易被拒绝（信用不足或存在风险问题），将抛出错误
- 成功的信用支付会建立您的信用记录，并可能随着时间的推移提高您的信用额度
- SDK会自动附加一个**Idempotency-Key**，以防止重复支付

## 5. 结算与区块链
ClawCredit处理区块链相关的复杂性。
- 您的信用额度以**美元**计价。
- 结算发生在**Base（USDC）**、**Solana（USDC）**或**XRPL（RLUSD）**上。
- 商家收到加密货币；您使用信用额度进行支付。

## 6. 仪表板链接（临时）
当用户请求状态或还款信息时，通过SDK生成一个临时仪表板链接。
该链接在24小时后失效，过期后需要重新生成。

```javascript
const { ClawCredit } = require('@t54-labs/clawcredit-sdk');
const credit = new ClawCredit({ agentName: "MyAgent" });

const dashboard = await credit.getDashboardLink();
// dashboard.url is the temporary URL for the user
```

## 7. 信用监控 + 还款提醒（定时任务）
每12小时运行一次定时任务（如果您希望更频繁地接收提醒，可以设置为每2小时一次）。
仅在欠款金额发生变化或到期日临近时通知用户。

```javascript
const { ClawCredit } = require('@t54-labs/clawcredit-sdk');
const credit = new ClawCredit({ agentName: "MyAgent" });

async function checkAndNotify() {
  const repayment = await credit.getRepaymentStatus();
  const amountDue = repayment.repayment_amount_due_usd || 0;
  const dueAt = repayment.repayment_due_at ? new Date(repayment.repayment_due_at) : null;

  const nearDue =
    dueAt && (dueAt.getTime() - Date.now()) <= 3 * 24 * 60 * 60 * 1000;

  if (amountDue > 0 && nearDue) {
    const link = await credit.getDashboardLink();
    // Use the OpenClaw default messaging tool to notify the user
    // sendMessage(`You need to repay soon. Dashboard: ${link.url}`);
  }
}

// Example schedule (every 12 hours)
setInterval(checkAndNotify, 12 * 60 * 60 * 1000);
```

**到期日临近且未付款时的提醒信息：**
```
You need to repay soon. Here is your Dashboard link: <URL>
```

## 8. 还款流程（第一阶段）
在当前阶段，还款由**人工用户**通过仪表板完成：

1) 代理运行定时任务来检查还款金额和到期日。
2) 当信用额度接近用完或到期日临近时，代理会提醒用户并提供仪表板链接。
3) 用户在仪表板中连接钱包并点击**Repay**。
4) 仪表板发送交易信息并将生成的`tx_hash`提交给后端。

**重要提示：**
- 在第一阶段，代理不应尝试直接还款。
- SDK的直接还款功能将在后续添加（待开发）。

## 9. 故障排除

### 常见问题

#### 支付时出现“未经授权”（401）错误

**症状：**
- `ClawCredit API错误：401 - {"detail":"Unauthorized"}`
- 支付请求因认证错误而失败

**常见原因：**
1. **令牌输入错误**——手动复制的令牌中缺少或包含错误的字符
2. **令牌过期**——请检查凭证文件中的`token_expires_at`
3. **使用错误的令牌**——使用了来自其他代理或环境的令牌

**解决方法：**
```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

// Always load from saved credentials file
const credPath = path.join(os.homedir(), '.openclaw', 'credentials', 'clawcredit.json');
const creds = JSON.parse(fs.readFileSync(credPath, 'utf-8'));

// Check expiration
const expiresAt = new Date(creds.token_expires_at);
if (expiresAt < new Date()) {
  console.log("Token expired! Please re-register.");
  // Re-register to get new token
  await credit.register({ inviteCode: "YOUR_INVITE_CODE" });
} else {
  console.log(`Token valid until: ${expiresAt.toISOString()}`);
  console.log(`Token: ${creds.api_token}`);
  // Use the token
  const credit = new ClawCredit({
    agentName: "MyAgent",
    apiToken: creds.api_token
  });
}
```

**预防措施：**
- ✅ **切勿手动复制令牌**——始终使用自动保存的凭证文件
- ✅ **使用前检查令牌是否过期**——令牌通常在30天后过期
- ✅ **始终使用正确的凭证文件路径**——`~/.openclaw/credentials/clawcredit.json`

#### 证书文件丢失或损坏

**症状：**
- 无法找到`~/.openclaw/credentials/clawcredit.json`
- 文件存在但内容无效

**解决方法：**
1. 重新注册以生成新的凭证：
   ```javascript
   const credit = new ClawCredit({ agentName: "MyAgent" });
   await credit.register({ inviteCode: "YOUR_NEW_INVITE_CODE" });
   // Credentials will be auto-saved
   ```

2. 检查文件权限（Unix/Linux/Mac）：
   ```bash
   chmod 600 ~/.openclaw/credentials/clawcredit.json
   ```

#### 令牌长度问题

**症状：**
- 令牌的长度与预期不符
- 令牌中间缺少字符

**验证方法：**
```javascript
const creds = JSON.parse(fs.readFileSync(credPath, 'utf-8'));
console.log('Token length:', creds.api_token.length);
console.log('Expected length: 37 (claw_ + 32 hex chars)');

if (creds.api_token.length !== 37) {
  console.log('⚠️  Token length incorrect! Re-register to fix.');
}
```

**有效的令牌格式：**
- 以`claw_`开头
- 后面紧跟着32个十六进制字符
- 总长度为37个字符
- 例如：`claw_13eef2bf75bd408d89451d00d4b35997`