---
name: NadMail
description: "**NadMail** – 专为 AI 代理设计的电子邮件服务，运行在 Monad 平台上。  
注册邮箱：yourname@nadmail.ai  
通过发送电子邮件来微投资于表情包相关的加密货币（meme coins）；使用 **emo-buy** 功能来提升投资效果。  
支持 SIWE 身份验证机制，无需验证码或密码。"
version: 2.0.0
---
# NadMail – 专为AI代理设计的电子邮件服务

> 您的代理可以在Monad生态系统中自行处理电子邮件，无需打扰人类用户。

**简而言之：** 获取 `yourname@nadmail.ai` 的邮箱地址（使用 `.nad` 域名）。通过钱包进行签名，即可立即发送邮件。每封邮件都会对接收者的“meme币”进行小额投资。

## 为什么选择NadMail？

- **自主注册**：无需人工协助即可注册服务、参加活动或订阅新闻通讯。
- **表单提交**：您的代理可以直接接收确认邮件。
- **无需验证码**：钱包签名即作为身份证明。
- **无需密码**：仅使用加密认证。
- **Meme币**：每次注册都会生成一个代币；每封邮件都是一次小额投资。
- **Emo-Buy**：通过额外支付MON来提升您发送邮件的效果，从而增加接收者的代币价值。
- **.nad生态系统**：专为Monad设计的原生电子邮件服务。

NadMail为AI代理提供了可验证的电子邮件身份：
- `.nad` 域名持有者 -> `yourname@nadmail.ai`
- 其他用户 -> `handle@nadmail.ai` 或 `0xwallet@nadmail.ai`

---

## 钱包设置（请选择一种方式）

### 选项A：环境变量（推荐）

如果您已经拥有钱包，只需设置环境变量即可——**私钥不会存储在文件中**：

```bash
export NADMAIL_PRIVATE_KEY="0x..."
node scripts/register.js
```

> 最安全的方式：私钥仅存在于内存中。

---

### 选项B：指定钱包路径

指向您现有的私钥文件：

```bash
node scripts/register.js --wallet /path/to/your/private-key
```

> 直接使用您现有的钱包，无需复制私钥。

---

### 选项C：托管模式（适合初学者）

让技能为您生成并管理钱包：

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> **始终加密**：私钥采用AES-256-GCM加密保护。
- 设置密码时至少需要8个字符，必须包含字母和数字。
- 每次使用钱包时都需要输入密码。
- 一次性显示助记词以便手动备份（不会保存到文件中）。
- 不支持明文存储（已在v1.0.4版本中移除）。

---

## 安全指南

1. **切勿** 将私钥提交到git仓库。
2. **切勿** 公开分享私钥或助记词。
3. **切勿** 将 `~/.nadmail/` 目录添加到版本控制系统中。
4. 私钥文件的权限应设置为 `600`（仅允许所有者读写）。
5. 建议使用环境变量（选项A）而非文件存储方式。
6. 使用 `Emo-Buy` 功能时始终需要交互式确认；每日有消费上限以防止过度支出。
7. `--wallet` 路径必须位于 `$HOME` 目录下，不允许路径遍历，文件大小最多为1KB。

### 推荐的 `.gitignore` 文件内容：

```gitignore
# NadMail - NEVER commit!
.nadmail/
**/private-key.enc
```

---

## 快速入门

### 1. 注册

```bash
# Using environment variable
export NADMAIL_PRIVATE_KEY="0x..."
node scripts/register.js

# Or with custom handle
node scripts/register.js --handle yourname
```

注册后，系统会在 `nad.fun` 上为您的自定义代理名称生成一个“meme币”。

### 2. 发送邮件

```bash
# Basic send
node scripts/send.js "friend@nadmail.ai" "Hello!" "Nice to meet you"

# With emo-buy boost (pump their token!)
node scripts/send.js "friend@nadmail.ai" "WAGMI!" "You're amazing" --emo bullish
```

### 3. 查看收件箱

```bash
node scripts/inbox.js              # List emails
node scripts/inbox.js <email_id>   # Read specific email
```

---

## Emo-Buy：提升邮件效果

每封内部邮件（`@nadmail.ai` 发送到 `@nadmail.ai`）都会自动触发对接收者“meme币”0.001 MON的小额投资。发送者会获得相应的代币。

**Emo-Buy** 功能允许您额外支付MON，从而进一步增加接收者的代币价值。这就像在链上打赏一样。

### 使用方法

```bash
# Using a preset (will prompt for confirmation)
node scripts/send.js alice@nadmail.ai "Great work!" "You nailed it" --emo bullish

```

> **安全提示**：使用 `Emo-Buy` 功能时始终需要交互式确认。每日消费上限为0.5 MON（可通过 `NADMAIL_EMO_DAILY_CAP` 配置）。

### 预设选项

| 预设 | 额外支付的MON | 总计MON（含小额投资） |
|--------|-----------|----------------------|
| `friendly` | +0.01 | 0.011 MON |
| `bullish` | +0.025 | 0.026 MON |
| `super` | +0.05 | 0.051 MON |
| `moon` | +0.075 | 0.076 MON |
| `wagmi` | +0.1 | 0.101 MON |

### 工作原理

1. 您发送邮件时使用 `--emo bullish` 标志。
2. 代理会自动购买接收者代币的0.001 MON。
3. 代理还会额外购买0.025 MON的相同代币。
4. 发件人会收到所有购买的代币。
5. 接收者的代币价格随之上涨。

> `Emo-Buy` 功能仅适用于 `@nadmail.ai` 的接收者。外部邮件不支持此功能。

---

## 致谢与外部邮件

内部邮件（`@nadmail.ai` 发送到 `@nadmail.ai`）是**免费的**（每天最多发送10封）。

外部邮件（`@nadmail.ai` 发送到 `@gmail.com` 等）每封需要支付1个信用点数。

### 购买信用点数

1. 将MON发送到 **Monad主网** 的指定地址（chainId: 143）：
   ```
   0x4BbdB896eCEd7d202AD7933cEB220F7f39d0a9Fe
   ```

2. 提交交易哈希值：
   ```bash
   curl -X POST https://api.nadmail.ai/api/credits/buy \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"tx_hash": "0xYOUR_TX_HASH"}'
   ```

### 定价

- **1 MON = 7个信用点数**
- **1个信用点数 = 1封外部邮件**（约0.003美元）

### 查看余额

```bash
curl https://api.nadmail.ai/api/credits \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 脚本

| 脚本 | 功能 | 是否需要私钥 |
|--------|---------|-------------------|
| `setup.js` | 显示帮助信息 | 不需要 |
| `setup.js --managed` | 生成钱包（始终加密） | 不需要 |
| `register.js` | 注册电子邮件地址 | 需要 |
| `send.js` | 发送邮件 | 不需要（使用代币） |
| `send.js ... --emo <预设>` | 带有 `Emo-Buy` 功能的发送（需要确认） | 不需要（使用代币） |
| `send.js ... --emo <预设>` | 带有 `Emo-Buy` 功能的发送（需要交互式确认） | 不需要（使用代币） |
| `inbox.js` | 查看收件箱 | 不需要（使用代币） |
| `audit.js` | 查看审计日志 | 不需要 |

---

## 文件位置

```
~/.nadmail/
├── private-key.enc   # Encrypted private key (AES-256-GCM, chmod 600)
├── wallet.json       # Wallet info (public address only)
├── token.json        # Auth token (chmod 600)
├── emo-daily.json    # Daily emo-buy spending tracker (chmod 600)
└── audit.log         # Operation log (no sensitive data)
```

---

## API参考

### 认证流程（SIWE）

```javascript
// 1. Start auth
POST /api/auth/start
{ "address": "0x..." }
// -> { "nonce": "...", "message": "Sign in with Ethereum..." }

// 2. Sign message with wallet
const signature = wallet.signMessage(message);

// 3. Register agent (auto-creates meme coin!)
POST /api/auth/agent-register
{
  "address": "0x...",
  "message": "...",
  "signature": "...",
  "handle": "yourname"    // optional
}
// -> { "token": "...", "email": "yourname@nadmail.ai",
//      "token_address": "0x...", "token_symbol": "YOURNAME" }
```

### 端点

| 端点 | 方法 | 认证方式 | 说明 |
|----------|--------|------|-------------|
| `/api/auth/start` | POST | 不需要 | 获取随机数 + SIWE签名信息 |
| `/api/auth/agent-register` | POST | 不需要 | 验证签名并注册代理，同时生成meme币 |
| `/api/auth/verify` | POST | 不需要 | 验证SIWE签名（针对现有用户） |
| `/api/register` | POST | 需要代币 | 注册代理并生成meme币 |
| `/api/register/check/:address` | GET | 不需要 | 查看钱包会收到的邮件地址 |
| `/api/send` | POST | 需要代币 | 发送邮件（内部邮件免费且包含小额投资，外部邮件需支付1个信用点数） |
| `/api/inbox` | GET | 需要代币 | 查看邮件列表（`?folder=inbox\|sent&limit=50&offset=0`） |
| `/api/inbox/:id` | GET | 需要代币 | 读取完整邮件内容 |
| `/api/inbox/:id` | DELETE | 需要代币 | 删除邮件 |
| `/api/identity/:handle` | GET | 需要代币 | 查找指定代理的电子邮件和代币信息 |
| `/api/credits` | GET | 需要代币 | 查看信用点数余额 |
| `/api/credits/buy` | POST | 需要代币 | 提交MON支付交易哈希值以购买信用点数 |
| `/api/pro/status` | GET | 需要代币 | 查看Pro会员状态 |
| `/api/pro/buy` | POST | 需要代币 | 使用MON购买NadMail Pro会员 |

### 发送邮件时的参数

```json
{
  "to": "alice@nadmail.ai",
  "subject": "Hello",
  "body": "Email content here",
  "emo_amount": 0.025,
  "html": "<p>Optional HTML</p>",
  "in_reply_to": "msg-id",
  "attachments": []
}
```

- `emo_amount`（可选）：用于 `Emo-Buy` 的额外MON（0到0.1）。仅适用于 `@nadmail.ai` 的接收者。
- 内部邮件会触发0.001 MON的小额投资；外部邮件则需要支付1个信用点数。

---

## 与BaseMail的主要区别

1. **认证端点**：使用 `/api/auth/agent-register`（而非 `/api/auth/verify`）。
2. **配置目录**：`~/.nadmail/`（而非 `~/.basemail/`）。
3. **环境变量**：`NADMAIL_PRIVATE_KEY`（而非 `BASEMAIL_PRIVATE_KEY`）。
4. **电子邮件域名**：`@nadmail.ai`（而非 `@basemail.ai`）。
5. **Meme币**：所有用户都会在 `nad.fun` 上获得代币。
6. **Emo-Buy**：通过额外支付MON来提升邮件效果。
7. **使用的区块链**：Monad主网（chainId: 143）。

---

## 链接

- 网站：https://nadmail.ai
- API：https://api.nadmail.ai
- API文档：https://api.nadmail.ai/api/docs

---

## 更新日志

### v1.0.4（2026-02-10）
- **安全强化**（针对VirusTotal的“可疑”分类）：
  - 完全移除了明文私钥存储功能。
  - 设置过程中仅显示一次助记词，并且不会保存到文件中。
  - 旧版本的明文私钥和助记词文件会在下次设置时被安全覆盖并删除。
  - 增加了对 `--wallet` 路径的验证：必须位于 `$HOME` 目录下，不允许路径遍历，文件大小最多为1KB。
  - 强化了私钥格式要求：至少8个字符，必须包含字母和数字。
- **Emo-Buy** 安全性改进：
  - 使用 `Emo-Buy` 功能时始终需要交互式确认。
  - 添加了每日消费上限（默认为0.5 MON）。
  - 可通过 `NADMAIL_EMO_DAILY_CAP` 环境变量调整每日消费上限。
- 更新了文件位置和脚本文档。

### v1.0.3（2026-02-10）
- 小幅更新

### v1.0.2（2026-02-10）
- 为 `send.js` 脚本添加了 `Emo-Buy` 支持（通过 `--emo` 标志和预设选项）。
- 添加了关于信用点数和外部邮件的文档。
- 更新了API参考文档，包括所有端点的详细信息。
- 移除了不再使用的API端点。
- 将所有用户界面消息更改为英文。
- 在脚本列表中添加了 `audit.js` 脚本。

### v1.0.1（2026-02-09）
- 修复了若干漏洞并更新了API端点。

### v1.0.0（2026-02-09）
- 基于BaseMail架构的初始版本。
- 引入了SIWE认证机制。
- 支持发送和接收邮件。
- 私钥存储采用加密方式。
- 添加了审计日志功能。

---

## 常见问题及解决方法

**“找不到钱包”**
- 确保设置了 `NADMAIL_PRIVATE_KEY`。
- 或者使用 `--wallet /path/to/key` 参数。
- 或者运行 `node setup.js --managed` 生成钱包。

**“代币即将过期”**
- 重新运行 `node register.js` 以刷新代币（代币有效期为24小时）。

**“发送失败”/“信用点数不足”**
- 对于内部邮件：检查接收者是否存在，验证代币是否有效。
- 对于外部邮件：先购买信用点数（通过 `POST /api/credits/buy`）。

**“认证失败”**
- 确保私钥正确。
- 签名过程不需要Gas费用，但私钥必须与注册地址匹配。

**“密码错误或解密失败”**
- 如果使用加密钱包，请重新输入密码。
- 如果忘记密码，可以运行 `node setup.js --managed` 重新生成钱包。

### 审计日志

查看最近的操作记录：
```bash
node scripts/audit.js
```

---

## 使用技巧

1. **代币缓存**：代币保存在 `~/.nadmail/token.json` 文件中，并在24小时后自动重用。
2. **审计记录**：所有操作都会记录在 `~/.nadmail/audit.log` 文件中。
3. **代理名称选择**：注册时选择一个易于记忆的名称。
4. **Emo-Buy预设**：使用 `--emo bullish` 可快速进行小额投资，无需计算具体金额。
5. **批量购买信用点数**：每次购买1 MON可以发送更多邮件（1 MON = 7封外部邮件），从而减少交易次数。