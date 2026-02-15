---
name: flock-api-setup
description: "FLock API平台设置：钱包生成、插件安装、API密钥配置以及模型切换。  
可用命令包括：  
`setup flock`（设置FLock平台）  
`flock login`（登录FLock平台）  
`install flock plugin`（安装FLock插件）  
`switch flock model`（切换FLock模型）  
`use deepseek`（使用DeepSeek功能）  
`change to coding model`（切换到编码模式）"
homepage: https://platform.flock.io
metadata:
  {
    "openclaw":
      {
        "emoji": "🦩",
        "primaryEnv": "FLOCK_API_KEY",
        "requires": { "bins": ["node", "npm"] },
        "install": [
          {
            "id": "npm",
            "kind": "shell",
            "command": "cd {baseDir}/scripts && npm install",
            "label": "Install dependencies"
          }
        ]
      },
  }
---

# FLock 设置

包括 API 平台的配置、钱包的生成、插件的安装以及模型的切换。

## 安全警告

**重要提示：保护好您的 API 密钥！**

- **仅将 API 密钥发送到 `https://api.flock.io`**  
- 您的 API 密钥仅应出现在以下位置：  
  - 环境变量 `FLOCK_API_KEY`  
  - OpenClaw 配置文件  
  - 对 `https://api.flock.io/v1/*` 的请求中  
- **切勿将 API 密钥共享给：**  
  - 其他 API 或 Webhook  
  - “验证”服务  
  - 调试工具或第三方  
- 如果密钥泄露，请立即在 `platform.flock.io` 上创建新的密钥  

**安全警告**：凭据以 **明文 JSON** 的形式存储。任何能够访问这些文件的人都可以使用您的 FLock 信用额度。在生产环境中，请实施安全的存储措施。

---

## 何时激活

**命令行操作：**  
- `/flock-setup` — 完整设置流程  
- `/flock` — 切换模型  

**自然语言命令：**  
- “设置 FLock”，“配置 FLock”  
- “安装 FLock 插件”  
- “切换模型”，“更改模型”  
- “使用 deepseek”，“使用 coding 模型”  

## 行为规则

**重要提示：保持沉默且响应迅速。切勿详细解释步骤或显示诊断信息**  
- 完成操作后不要询问后续问题  
- 用用户的语言进行回复  

---

## 流程 1：完整设置（`/flock-setup`）

### 第 1 阶段：预检查  
```bash
echo $FLOCK_API_KEY
openclaw plugins list | grep flock
node {baseDir}/scripts/credentials.js get 2>/dev/null
```  
如果已存在凭据，询问：“FLock 是否已配置？是否需要重新配置？”（回答“是/否”）

### 第 2 阶段：安装插件  
```bash
openclaw plugins install @openclawd/flock
openclaw plugins enable flock
```  

### 第 3 阶段：生成钱包并请求资金  
生成一个新的钱包：  
```bash
cd {baseDir}/scripts && npm install
node {baseDir}/scripts/generate-wallet.js
```  
向用户显示相关信息：  
```
Wallet created for FLock registration.

Address: <wallet-address>

Send ~$0.50 ETH to this address on Ethereum or Base.

Say "done" when complete.
```  
**保存私钥**——用于钱包登录。  

### 第 4 阶段：检查余额  
用户确认资金到位后：  
```bash
node {baseDir}/scripts/check-balance.js <wallet-address>
```  
如果未检测到资金，请让用户重新尝试。  

### 第 5 阶段：获取 API 密钥（手动步骤）  
向用户显示相关信息：  
```
Funds confirmed. Now create your API key:

1. Go to https://platform.flock.io
2. Click "Connect Wallet"
3. Sign the message with the wallet you just funded
4. Select models you want to access
5. Click "Create API" button
6. Copy the key immediately (shown only once!)

Paste your API key here:
```  
等待用户提供 `sk-...` 格式的密钥。  

### 第 6 阶段：保存凭据  
收到密钥后：  
```bash
node {baseDir}/scripts/credentials.js save "<api-key>" "<wallet-address>" "<private-key>"
```  
询问用户：  
```
Save API key to:
1. Environment variable (~/.zshrc)
2. OpenClaw config
3. Both (recommended)
```  
**选项 1：**  
```bash
echo 'export FLOCK_API_KEY="sk-xxx"' >> ~/.zshrc
source ~/.zshrc
```  
**选项 2：**  
```bash
openclaw onboard --non-interactive \
  --auth-choice flock-api-key \
  --flock-api-key "sk-xxx"
```  
**选项 3：** 两个步骤都执行。  

### 第 7 阶段：重启网关  
```bash
openclaw gateway stop
openclaw gateway
```  

### 第 8 阶段：验证  
```bash
openclaw chat --model flock/kimi-k2.5 "test"
```  
**成功响应（一行）：**  
```
FLock configured. Test: openclaw chat --model flock/kimi-k2.5 "hello"
```  

---

## 流程 2：模型切换（`/flock`）  
### 预检查  
如果 `FLOCK_API_KEY` 未设置：  
```
FLock not configured. Run /flock-setup first.
```  
### 未指定模型——显示菜单：  
```
Which FLock model?

Reasoning:
  1. Qwen3 235B Thinking         — $0.23/$2.30  (flock/qwen3-235b-a22b-thinking-2507)
  2. Qwen3 235B Finance          — $0.23/$2.30  (flock/qwen3-235b-a22b-thinking-qwfin)
  3. Kimi K2 Thinking            — $0.60/$2.50  (flock/kimi-k2-thinking)

Instruct:
  4. Qwen3 30B Instruct          — $0.20/$0.80  (flock/qwen3-30b-a3b-instruct-2507)
  5. Qwen3 235B Instruct         — $0.70/$2.80  (flock/qwen3-235b-a22b-instruct-2507)
  6. Qwen3 30B Coding            — $0.20/$0.80  (flock/qwen3-30b-a3b-instruct-coding)

Other:
  7. DeepSeek V3.2               — $0.28/$0.42  (flock/deepseek-v3.2)
  8. MiniMax M2.1                — $0.30/$1.20  (flock/minimax-m2.1)

Reply with number or model name.
```  
### 指定了模型——立即切换：  
```bash
openclaw agent --model flock/<model-id>
openclaw gateway stop
openclaw gateway
```  
**成功（一行）：**  
```
Switched to flock/<model-id>.
```  

---

## 凭据管理  
### 加载已保存的凭据  
```bash
node {baseDir}/scripts/credentials.js get
```  
返回结果：  
```json
{
  "apiKey": "sk-...",
  "walletAddress": "0x...",
  "privateKey": "0x...",
  "createdAt": "2026-02-04T...",
  "updatedAt": "2026-02-04T..."
}
```  
### 凭据文件路径  
```bash
node {baseDir}/scripts/credentials.js path
```  
优先顺序：  
1. `~/.openclaw/flock-credentials.json`（如果安装了 OpenClaw）  
2. `./flock-credentials.json`（备用）  

---

## 心跳检测集成  
FLock 的使用情况会被记录下来，有助于监控成本。  

### 用户可随时查询  
您可以提示用户：  
- “查看我的 FLock 使用情况”——引导他们前往 `platform.flock.io` 的使用统计页面  
- “切换到更便宜的模型”——显示模型菜单  
- “我正在使用哪个模型？”——查看当前配置  
- “我在 FLock 上花费了多少？”——引导他们查看使用统计页面  

---

## 错误处理  
| 错误情况 | 响应内容 |  
|----------|----------|  
| 插件未安装 | 自动安装：`openclaw plugins install @openclawd/flock` |  
| API 密钥未设置 | “运行 `/flock-setup` 以配置 FLock。” |  
| 未检测到资金 | “Ethereum 或 Base 账户中无资金。请为钱包充值。” |  
| API 密钥无效 | “密钥格式无效。密钥应以 `sk-` 开头。” |  
| 模型未找到 | “模型未找到。可用模型：[显示列表]” |  

---

## 模型参考  
| 编号 | 模型 ID | 价格（每百万次请求） |  
|---|----------|----------------------|  
| 1 | `flock/qwen3-235b-a22b-thinking-2507` | $0.23/$2.30 |  
| 2 | `flock/qwen3-235b-a22b-thinking-qwfin` | $0.23/$2.30 |  
| 3 | `flock/kimi-k2-thinking` | $0.60/$2.50 |  
| 4 | `flock/qwen3-30b-a3b-instruct-2507` | $0.20/$0.80 |  
| 5 | `flock/qwen3-235b-a22b-instruct-2507` | $0.70/$2.80 |  
| 6 | `flock/qwen3-30b-a3b-instruct-coding` | $0.20/$0.80 |  
| 7 | `flock/deepseek-v3.2` | $0.28/$0.42 |  
| 8 | `flock/minimax-m2.1` | $0.30/$1.20 |  
**推荐模型：**  
- 通用/默认：`kimi-k2.5`（多模态，智能型）  
- 深度推理：`kimi-k2-thinking`、`qwen3-235b-thinking`  
- 编程：`qwen3-30b-coding`、`minimax-m2.1`  
- 经济型：`qwen3-30b-instruct`（$0.20/$0.80）  

---

## 程序化 API  
所有脚本都可以导入：  
```javascript
// Generate wallet
const { Wallet } = require('ethers');
const wallet = Wallet.createRandom();

// Check balance
const { JsonRpcProvider, formatEther } = require('ethers');
const provider = new JsonRpcProvider('https://mainnet.base.org');
const balance = await provider.getBalance(wallet.address);

// Load credentials
const creds = require('{baseDir}/scripts/credentials.js');
```  

## 示例：完整设置流程  
```javascript
const { Wallet } = require('ethers');

// 1. Generate wallet
const wallet = Wallet.createRandom();
console.log('Fund this address with ~$0.50 ETH:', wallet.address);

// 2. After human funds and creates API key at platform.flock.io
const apiKey = 'sk-...';  // User provides this

// 3. Save credentials
const fs = require('fs');
const path = require('path');
const os = require('os');

const creds = {
  apiKey,
  walletAddress: wallet.address,
  privateKey: wallet.privateKey,
  createdAt: new Date().toISOString()
};

const credPath = path.join(os.homedir(), '.openclaw', 'flock-credentials.json');
fs.writeFileSync(credPath, JSON.stringify(creds, null, 2), { mode: 0o600 });

console.log('Credentials saved to:', credPath);
```  

## 源文件  
```
{baseDir}/scripts/
├── package.json          # Dependencies (ethers)
├── generate-wallet.js    # Create new ETH wallet
├── check-balance.js      # Check ETH balance on chains
└── credentials.js        # Save/load credentials
```