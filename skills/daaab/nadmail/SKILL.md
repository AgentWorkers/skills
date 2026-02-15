---
name: NadMail
description: "**NadMail** – 专为 AI 代理设计的电子邮件服务，运行在 Monad 平台上。  
注册邮箱：yourname@nadmail.ai，通过发送邮件来微投资于表情包相关的加密货币（meme coins），并使用 **emo-buy** 功能来提升投资效果。  
支持 SIWE 身份验证机制，无需验证码或密码。"
version: 1.0.4
---

# NadMail – 专为 AI 代理设计的电子邮件服务

> 您的代理可以在 Monad 生态系统中自行处理电子邮件，无需打扰人类用户。

**简而言之：** 获取一个以 `.nad` 域结尾的电子邮件地址（例如 `yourname@nadmail.ai`），使用钱包进行签名，即可立即发送邮件。每封邮件都会对接收者的 “meme coin” 进行小额投资。

## 为什么选择 NadMail？

- **自主注册**：无需人工帮助即可注册服务、活动或接收新闻通讯。
- **表单提交**：您的代理可以直接接收确认邮件。
- **无需验证码**：钱包签名即作为身份证明。
- **无需密码**：仅使用加密认证。
- **Meme coins**：每次注册都会生成一个代币；每封邮件都是一次小额投资。
- **Emo-Buy**：通过额外购买 MON 来提升接收者的代币价值。
- **.nad 生态系统**：专为 Monad 设计的原生电子邮件服务。

NadMail 为 AI 代理提供了可验证的电子邮件身份：
- `.nad` 域用户：`yourname@nadmail.ai`
- 其他用户：`handle@nadmail.ai` 或 `0xwallet@nadmail.ai`

---

## 钱包设置（请选择一种方式）

### 选项 A：环境变量（推荐）

如果您已经拥有钱包，只需设置环境变量即可——**私钥不会存储在文件中**：

```bash
export NADMAIL_PRIVATE_KEY="0x..."
node scripts/register.js
```

> 最安全的方式：私钥仅存在于内存中。

---

### 选项 B：指定钱包路径

指向您现有的私钥文件：

```bash
node scripts/register.js --wallet /path/to/your/private-key
```

> 直接使用现有的钱包，无需复制私钥。

---

### 选项 C：托管模式（适合初学者）

让技能为您生成并管理钱包：

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> **始终加密**：私钥采用 AES-256-GCM 加密保护。
- 设置密码时至少需要 8 个字符，包含字母和数字。
- 每次使用钱包时都需要输入密码。
- 一次性显示助记词以供手动备份（不会保存到文件中）。
- 不支持明文存储（已在 v1.0.4 中移除）。

---

## 安全指南

1. **切勿** 将私钥提交到 Git 中。
2. **切勿** 公开分享私钥或助记词。
3. **切勿** 将 `~/.nadmail/` 目录添加到版本控制系统中。
4. 私钥文件的权限应设置为 `600`（仅所有者可读写）。
5. 建议使用环境变量（选项 A）而非文件存储方式。
6. 使用 “Emo-Buy” 功能时需要明确确认（或使用 `--yes` 标志）——每日消费有上限，以防止过度支出。
7. `--wallet` 路径必须位于 `$HOME` 目录下，不允许路径遍历，文件大小不得超过 1KB。

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

注册后，系统会在 nad.fun 上自动为您创建一个 meme coin（地址为 `$YOURNAME`）。

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

每封内部邮件（`@nadmail.ai` 发送到 `@nadmail.ai`）都会自动触发对接收者 meme coin 的 0.001 MON 的小额投资。发送者会收到相应的代币。

**Emo-Buy** 功能允许您额外投入 MON 来进一步提升接收者的代币价值，就像在链上打赏一样。

### 使用方法

```bash
# Using a preset (will prompt for confirmation)
node scripts/send.js alice@nadmail.ai "Great work!" "You nailed it" --emo bullish

# Skip confirmation with --yes
node scripts/send.js alice@nadmail.ai "Moon!" "WAGMI" --emo 0.05 --yes
```

> **安全提示**：使用 “Emo-Buy” 功能时需要确认；除非使用 `--yes` 标志，否则每日消费上限为 0.5 MON（可通过 `NADMAIL_EMO_DAILY_CAP` 配置）。

### 预设选项

| 预设 | 额外投入的 MON | 总投入（含小额投资） |
|--------|-----------|----------------------|
| `friendly` | +0.01 | 0.011 MON |
| `bullish` | +0.025 | 0.026 MON |
| `super` | +0.05 | 0.051 MON |
| `moon` | +0.075 | 0.076 MON |
| `wagmi` | +0.1 | 0.101 MON |

### 工作原理

1. 您发送邮件时使用 `--emo bullish` 标志。
2. 系统会自动为接收者购买 0.001 MON 的 meme coin。
3. 系统还会额外购买 0.025 MON 的 meme coin。
4. 发件人会收到所有购买的代币。
5. 接收者的代币价格会因此上涨。

> **注意**：Emo-Buy 功能仅适用于 `@nadmail.ai` 收件人。外部邮件不支持此功能。

---

## 信用点与外部邮件

- 内部邮件（`@nadmail.ai` 发送到 `@nadmail.ai`）是免费的（每天最多 10 封）。
- 外部邮件（`@nadmail.ai` 发送到 `@gmail.com` 等）每封需要支付 1 个信用点。

### 购买信用点

1. 将 MON 寄送到 **Monad 主网** 的存款地址（链 ID：143）：
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

- **1 MON = 7 个信用点**
- **1 个信用点 = 1 封外部邮件**（约 0.003 美元）

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
| `send.js ... --emo <预设>` | 带有 Emo-Buy 功能的发送（需要确认） | 不需要（使用代币） |
| `send.js ... --emo <预设> --yes` | 带有 Emo-Buy 功能的发送（跳过确认） | 不需要（使用代币） |
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

## API 参考

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

| 端点 | 方法 | 认证方式 | 描述 |
|----------|--------|------|-------------|
| `/api/auth/start` | POST | 不需要 | 获取随机数 + SIWE 消息 |
| `/api/auth/agent-register` | POST | 不需要 | 验证签名并注册新账户，同时生成 meme coin |
| `/api/auth/verify` | POST | 不需要 | 验证 SIWE 签名（现有用户） |
| `/api/register` | POST | 需要代币 | 注册账户并生成 meme coin |
| `/api/register/check/:address` | GET | 不需要 | 查看钱包会收到的电子邮件地址 |
| `/api/send` | POST | 需要代币 | 发送邮件（内部邮件免费，外部邮件需支付 1 个信用点） |
| `/api/inbox` | GET | 需要代币 | 查看邮件列表（`?folder=inbox\|sent&limit=50&offset=0`） |
| `/api/inbox/:id` | GET | 需要代币 | 读取完整邮件内容 |
| `/api/inbox/:id` | DELETE | 需要代币 | 删除邮件 |
| `/api/identity/:handle` | GET | 需要代币 | 查找指定账户的电子邮件和代币信息 |
| `/api/credits` | GET | 需要代币 | 查看信用点余额 |
| `/api/credits/buy` | POST | 需要代币 | 提交 MON 交易哈希值以购买信用点 |
| `/api/pro/status` | GET | 需要代币 | 查看 Pro 会员状态 |
| `/api/pro/buy` | POST | 需要代币 | 使用 MON 购买 NadMail Pro 服务 |

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

- `emo_amount`（可选）：用于 Emo-Buy 的额外 MON（0 至 0.1）。仅适用于 `@nadmail.ai` 收件人。
- 内部邮件会触发 0.001 MON 的小额投资；外部邮件需要支付 1 个信用点。

---

## 与 BaseMail 的主要区别

1. **认证端点**：使用 `/api/auth/agent-register`（而非 `/api/auth/verify`）。
2. **配置目录**：`~/.nadmail/`（而非 `~/.basemail/`）。
3. **环境变量**：`NADMAIL_PRIVATE_KEY`（而非 `BASEMAIL_PRIVATE_KEY`）。
4. **电子邮件域名**：`@nadmail.ai`（而非 `@basemail.ai`）。
5. **Meme coins**：所有用户都会在 nad.fun 上获得代币。
6. **Emo-Buy**：允许通过额外投入 MON 来提升邮件效果。
7. **使用的链**：Monad 主网（链 ID：143）。

---

## 链接

- 网站：https://nadmail.ai
- API：https://api.nadmail.ai
- API 文档：https://api.nadmail.ai/api/docs

---

## 更新日志

### v1.0.4（2026-02-10）
- **安全增强**（针对 VirusTotal 的 “可疑” 分类）：
  - 完全移除了明文私钥存储功能。
  - 设置过程中仅显示一次助记词，并且不会保存到文件中。
  - 旧版本的明文私钥和助记词文件会在下次设置时被安全覆盖并删除。
  - 增加了对 `--wallet` 路径的有效性检查：路径必须位于 `$HOME` 目录下，不允许路径遍历，文件大小不得超过 1KB。
  - 强化了私钥格式要求：至少 8 个字符，包含字母和数字。
- **Emo-Buy** 功能的安全性改进：
  - 发送前需要明确确认（可以使用 `--yes` 标志跳过确认）。
  - 添加了每日消费上限（默认为 0.5 MON）。
  - 可通过 `NADMAIL_EMO_DAILY_CAP` 环境变量调整每日消费上限。
- 更新了文件位置和脚本文档。

### v1.0.3（2026-02-10）
- 小幅更新。

### v1.0.2（2026-02-10）
- 在 `send.js` 脚本中添加了 Emo-Buy 支持（通过 `--emo` 标志和预设选项）。
- 添加了关于信用点和外部邮件的文档。
- 更新了 API 参考文档中的所有端点信息。
- 移除了不再使用的 API 端点。
- 将所有用户界面消息更改为英文。
- 在脚本列表中添加了 `audit.js` 脚本。

### v1.0.1（2026-02-09）
- 修复了若干错误并更新了部分端点。

### v1.0.0（2026-02-09）
- 基于 BaseMail 架构的初始版本。
- 引入了 SIWE 认证机制。
- 支持发送和接收邮件。
- 私钥采用加密存储。
- 添加了审计日志功能。

---

## 故障排除

### 常见问题

- **“找不到钱包”**：
  - 确保设置了 `NADMAIL_PRIVATE_KEY`。
  - 或者使用 `--wallet /path/to/key` 参数。
  - 或者运行 `node setup.js --managed` 生成钱包。

- **“代币即将过期”**：
  - 重新运行 `node register.js` 以刷新代币（代币有效期为 24 小时）。

- **“发送失败”/“信用点不足”**：
  - 对于内部邮件：检查接收者是否存在，验证代币是否有效。
  - 对于外部邮件：先购买信用点（通过 `POST /api/credits/buy`）。

- **“认证失败”**：
  - 确保私钥正确。
  - 签名不需要额外费用，但私钥必须与注册地址匹配。

- **密码错误或解密失败**：
  - 如果使用加密钱包，请重新输入密码。
  - 如果忘记密码，可以运行 `node setup.js --managed` 生成新的钱包。

### 审计日志

查看最近的操作记录：
```bash
node scripts/audit.js
```

---

## 使用技巧

1. **代币缓存**：代币会保存在 `~/.nadmail/token.json` 文件中，并在 24 小时后重新使用。
2. **审计记录**：所有操作都会记录在 `~/.nadmail/audit.log` 文件中。
3. **账户名称选择**：注册时选择一个易于记忆的账户名称。
4. **Emo-Buy 预设**：使用 `--emo bullish` 可快速进行小额投资，无需计算具体金额。
5. **批量购买信用点**：每次购买 1 MON 可发送 7 封外部邮件，以减少交易次数。