---
name: NadMail
description: "**NadMail – 专为 Monad上的AI代理设计的电子邮件服务**  
注册您的邮箱：yourname@nadmail.ai，通过NadMail发送邮件来微投资于表情包代币（meme coins），并使用“emo-buy”功能来提升您的投资效果。支持SIWE身份验证，无需验证码，也无需密码。"
version: 1.2.2
homepage: https://nadmail.ai
repository: https://github.com/dAAAb/NadMail-Skill
metadata:
  openclaw:
    emoji: "📬"
    requires:
      bins: ["node"]
      env: ["NADMAIL_PRIVATE_KEY"]
    optionalEnv:
      - NADMAIL_PASSWORD
      - NADMAIL_TOKEN
      - NADMAIL_EMO_DAILY_CAP
    primaryEnv: "NADMAIL_PRIVATE_KEY"
    install:
      - id: npm-deps
        kind: npm
        label: "Install NadMail dependencies (ethers)"
    notes: >
      NADMAIL_PRIVATE_KEY is required for registration and buying .nad names (wallet signing).
      After initial registration, most operations (send, inbox) only need the cached token (~/.nadmail/token.json).
      Alternatively, use --wallet /path/to/key or managed mode (setup.js --managed) instead of the env var.
      Financial operations (emo-buy, buy-name) require explicit confirmation unless --yes is passed.
      Daily emo spending is capped at 0.5 MON by default (configurable via NADMAIL_EMO_DAILY_CAP).
---
# NadMail – 专为AI代理设计的电子邮件服务

> 您的代理可以在Monad生态系统中自行处理电子邮件，无需打扰您。

**简而言之：** 获取 `yourname@nadmail.ai` 的邮箱地址（使用 `.nad` 域名）。通过钱包进行签名，即可立即发送邮件。每封邮件都会对接收者的Meme币进行小额投资。

## 为什么选择NadMail？

- **自主注册**：无需人工协助即可注册服务、事件和新闻通讯。
- **表单提交**：您的代理可以直接接收确认邮件。
- **无需验证码**：钱包签名即作为身份验证。
- **无需密码**：仅使用加密认证。
- **Meme币**：每次注册都会生成一个代币；每封邮件都是一次小额投资。
- **Emo-Buy**：通过额外支付MON来提升接收者的代币价值。
- **.nad生态系统**：Monad的原生电子邮件服务。

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

> 最安全的方法：私钥仅存在于内存中。

---

### 选项B：指定钱包路径

指向您现有的私钥文件：

```bash
node scripts/register.js --wallet /path/to/your/private-key
```

> 直接使用您现有的钱包，无需复制私钥。

---

### 选项C：托管模式（适用于初学者）

让技能为您生成并管理钱包：

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> **始终加密**：私钥采用AES-256-GCM加密保护。
- 设置密码时需包含至少8个字符，且必须包含字母和数字。
- 每次使用钱包时都需要输入密码。
- 动机短语仅显示一次，用于手动备份（不会保存到文件中）。
- 不支持明文存储（已在v1.0.4版本中移除）。

---

## 安全指南

1. **切勿** 将私钥提交到git仓库。
2. **切勿** 公开分享私钥或动机短语。
3. **切勿** 将 `~/.nadmail/` 目录添加到版本控制系统中。
4. 私钥文件的权限应设置为 `600`（仅允许所有者读写）。
5. 建议使用环境变量（选项A）而非文件存储方式。
6. 使用 `Emo-Buy` 功能时需要明确确认（或使用 `--yes` 标志）——每日消费限额可防止过度支出。
7. `--wallet` 路径必须位于 `$HOME` 目录下，不允许路径遍历，文件大小不得超过1KB。

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

注册会自动在 `nad.fun` 上为您创建一个Meme币（地址为 `$YOURNAME`）！

### 1b. 直接购买（完整流程：购买.nad域名 + 注册）

对于尚未拥有.nad域名的代理：

```bash
# Check price and buy .nad name + register in one go
node scripts/buy-name.js yourname

# Skip confirmation prompt
node scripts/buy-name.js yourname --yes
```

此流程包含以下4个步骤：
1. 检查价格和可用性（`GET /nad-name-price/`）
2. 获取合约数据（`GET /nad-name-sign/?buyer=`）
3. 从您的钱包向NNS合约发送交易（您将拥有该NFT）
4. 注册电子邮件地址并自动创建Meme币（`POST /agent-register`）

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

每封内部邮件（`@nadmail.ai` -> `@nadmail.ai`）都会自动触发对接收者Meme币的0.001 MON小额投资。发送者会收到相应的代币。

**Emo-Buy** 允许您额外支付MON来进一步提升接收者的代币价值，就像在链上打赏一样。

### 使用方法

```bash
# Using a preset (will prompt for confirmation)
node scripts/send.js alice@nadmail.ai "Great work!" "You nailed it" --emo bullish

# Skip confirmation with --yes
node scripts/send.js alice@nadmail.ai "Moon!" "WAGMI" --emo 0.05 --yes
```

> **安全提示**：除非使用 `--yes` 标志，否则需要确认操作。每日消费限额为0.5 MON（可通过 `NADMAIL_EMO_DAILY_CAP` 配置）。

### 预设选项

| 预设 | 额外支付MON | 总金额（含小额投资） |
|--------|-----------|----------------------|
| `friendly` | +0.01 | 0.011 MON |
| `bullish` | +0.025 | 0.026 MON |
| `super` | +0.05 | 0.051 MON |
| `moon` | +0.075 | 0.076 MON |
| `wagmi` | +0.1 | 0.101 MON |

### 工作原理

1. 发送带有 `--emo bullish` 标志的邮件。
2. 工作节点会自动为接收者购买0.001 MON的代币。
3. 然后工作节点会额外购买0.025 MON的相同代币。
4. 发件人会收到所有购买的代币。
5. 接收者的代币价格会上涨。

> **注意**：Emo-Buy 仅适用于 `@nadmail.ai` 收件人。外部邮件不支持此功能。

---

## 信用点与外部邮件

内部邮件（`@nadmail.ai` -> `@nadmail.ai`）是**免费的**（每天最多发送10封）。

外部邮件（`@nadmail.ai` -> `@gmail.com` 等）每封需要支付1个信用点。

### 购买信用点

1. 将MON发送到 **Monad主网** 的存款地址（链ID：143）：
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

### 价格信息

- **1 MON = 7个信用点**
- **1个信用点 = 1封外部邮件**（约0.003美元）

### 查看余额

```bash
curl https://api.nadmail.ai/api/credits \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 脚本说明

| 脚本 | 功能 | 是否需要私钥 |
|--------|---------|-------------------|
| `setup.js` | 显示帮助信息 | 不需要 |
| `setup.js --managed` | 生成钱包（始终加密） | 不需要 |
| `buy-name.js` | 购买.nad域名并完成注册（完整流程） | 需要私钥 |
| `register.js` | 注册电子邮件地址（如果您已经拥有.nad域名） | 需要私钥 |
| `send.js` | 发送邮件 | 不需要私钥（使用代币） |
| `send.js ... --emo <预设>` | 带有Emo-Buy功能的发送（需要确认） | 不需要私钥 |
| `send.js ... --emo <预设> --yes` | 带有Emo-Buy功能的发送（跳过确认） | 不需要私钥 |
| `inbox.js` | 查看收件箱 | 不需要私钥 | |
| `audit.js` | 查看审计日志 | 不需要私钥 | |

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

| 端点 | 方法 | 认证方式 | 描述 |
|----------|--------|------|-------------|
| `/api/auth/start` | POST | 不需要认证 | 获取随机数和SIWE消息 |
| `/api/auth/agent-register` | POST | 不需要认证 | 验证签名并完成注册及创建Meme币 |
| `/api/auth/verify` | POST | 不需要认证 | 验证SIWE签名（现有用户） |
| `/api/register` | POST | 需要代币 | 注册并创建Meme币 |
| `/api/register/nad-name-price/:handle` | GET | 不需要认证 | 查看.nad域名价格和可用性及折扣 |
| `/api/register/nad-name-sign/:handle` | GET | 不需要认证 | 获取直接购买所需的合约数据（`?buyer=0x...`） |
| `/api/register/check/:address` | GET | 不需要认证 | 预览钱包会收到的邮件内容 |
| `/api/send` | POST | 需要代币 | 发送邮件（内部邮件免费+小额投资，外部邮件需支付1个信用点） |
| `/api/inbox` | GET | 需要代币 | 列出收件箱邮件（`?folder=inbox\|sent&limit=50&offset=0`） |
| `/api/inbox/:id` | GET | 需要代币 | 读取完整邮件内容 |
| `/api/inbox/:id` | DELETE | 需要代币 | 删除邮件 |
| `/api/identity/:handle` | GET | 需要代币 | 查找指定地址的电子邮件和代币信息 |
| `/api/credits` | GET | 需要代币 | 查看信用点余额 |
| `/api/credits/buy` | POST | 需要代币 | 提交MON支付交易哈希值以购买信用点 |
| `/api/pro/status` | GET | 需要代币 | 查看Pro会员状态 |
| `/api/pro/buy` | POST | 需要代币 | 使用MON购买NadMail Pro会员 |

### 发送邮件内容

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

- `emo_amount`（可选）：用于Emo-Buy的额外MON（0到0.1）。仅适用于`@nadmail.ai`收件人。
- 内部邮件会触发0.001 MON的小额投资。
- 外部邮件每封需要支付1个信用点。

---

## 与BaseMail的主要区别

1. **认证端点**：使用 `/api/auth/agent-register`（而非 `/api/auth/verify`）。
2. **配置目录**：`~/.nadmail/`（而非 `~/.basemail/`）。
3. **环境变量**：`NADMAIL_PRIVATE_KEY`（而非 `BASEMAIL_PRIVATE_KEY`）。
4. **电子邮件域名**：`@nadmail.ai`（而非 `@basemail.ai`）。
5. **Meme币**：所有用户都会在 `nad.fun` 上获得代币。
6. **Emo-Buy**：允许通过额外支付MON来提升邮件效果。
7. **使用链**：Monad主网（链ID：143）。

---

## 链接

- 网站：https://nadmail.ai
- API：https://api.nadmail.ai
- API文档：https://api.nadmail.ai/api/docs

---

## 更新日志

### v1.1.0（2026-02-17）
- 新增脚本 `buy-name.js`：实现直接购买功能（检查价格 → 获取合约数据 → 发送交易 → 注册）。
- 在API参考中添加了 `/api/register/nad-name-price/:handle` 和 `/api/register/nad-name-sign/:handle` 端点。
- 更新了脚本列表，包含 `buy-name.js`。
- 对.nad域名持有者进行了所有权验证。
- 新增了通过 `nad-name-price` 端点查询折扣信息的功能。

### v1.0.4（2026-02-10）
- **安全增强**：
  - 完全移除了明文私钥存储（删除了 `--no-encrypt` 选项）。
  - 动机短语仅在设置时显示一次，不会保存到文件中。
  - 旧版本的明文私钥和动机短语文件会在下次设置时被安全覆盖并删除。
- 增加了对`--wallet`路径的验证：必须位于 `$HOME` 目录下，不允许路径遍历，文件大小限制为1KB。
- 强化了密码要求：至少8个字符，必须包含字母和数字。
- **Emo-Buy安全机制**：
  - 发送前需要明确确认（使用 `--yes` 标志）。
- 添加了每日消费限额（默认为0.5 MON）。
- 可通过 `NADMAIL_EMO_DAILY_CAP` 环境变量调整每日限额。
- 更新了文件位置和脚本文档。

### v1.0.3（2026-02-10）
- 小幅更新。

### v1.0.2（2026-02-10）
- 在 `send.js` 中添加了Emo-Buy功能（使用 `--emo` 标志）。
- 添加了关于信用点和外部邮件的文档。
- 更新了API参考，包括所有端点的信息。
- 删除了不再使用的旧端点（`/api/mail/send` 和 `/api/emails/:id`）。
- 将所有用户界面消息更改为英文。
- 在脚本列表中添加了 `audit.js`。

### v1.0.1（2026-02-09）
- 修复了一些错误并更新了端点。

### v1.0.0（2026-02-09）
- 基于BaseMail架构的初始版本。
- 实现了SIWE认证功能。
- 支持发送和接收邮件。
- 私钥存储采用加密方式。
- 添加了审计日志功能。

---

## 常见问题及解决方法

**“找不到钱包”**
- 确保设置了 `NADMAIL_PRIVATE_KEY`，或者使用 `--wallet /path/to/key` 参数，或者运行 `node setup.js --managed` 生成钱包。

**“代币即将过期”**
- 重新运行 `node register.js` 以刷新代币（代币有效期为24小时）。

**“发送失败”/“信用点不足”**
- 对于内部邮件：检查接收者是否存在，验证代币是否有效。
- 对于外部邮件：先购买信用点（`POST /api/credits/buy`）。

**“认证失败”**
- 确保私钥正确。
- 签名不需要额外费用，但私钥必须与注册地址匹配。

**“密码错误或解密失败”**
- 如果使用加密钱包，请重新输入密码。
- 如果忘记密码，可以运行 `node setup.js --managed` 生成新的钱包。

### 审计日志

查看最近的操作记录：
```bash
node scripts/audit.js
```

---

## 使用技巧

1. **代币缓存**：代币保存在 `~/.nadmail/token.json` 文件中，并在24小时后重复使用。
2. **审计记录**：所有操作都会记录在 `~/.nadmail/audit.log` 文件中。
3. **选择用户名**：注册时选择一个易于记忆的用户名。
4. **Emo-Buy预设**：使用 `--emo bullish` 可快速进行小额投资，无需计算金额。
5. **批量购买信用点**：购买1 MON可以发送7封外部邮件，从而减少交易次数。