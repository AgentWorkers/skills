---
name: BaseMail
description: "📬 BaseMail：专为基于 Base 的 AI 代理设计的链上电子邮件服务。将您的用户名（getyourname@basemail.ai）与您的 Basename（.base.eth）关联起来。支持 SIWE 钱包身份验证，无需验证码或密码。为您的 AI 代理提供在 Base Chain 上可验证的电子邮件身份——可以自主注册服务、发送邮件以及接收确认信息。"
version: 1.8.0
homepage: https://basemail.ai
repository: https://github.com/dAAAb/BaseMail-Skill
metadata:
  openclaw:
    emoji: "📬"
    requires:
      bins: ["node"]
      env: ["BASEMAIL_PRIVATE_KEY"]
    optionalEnv:
      - BASEMAIL_PASSWORD
      - BASEMAIL_TOKEN
    primaryEnv: "BASEMAIL_PRIVATE_KEY"
    install:
      - id: npm-deps
        kind: npm
        label: "Install BaseMail dependencies (ethers)"
    notes: >
      BASEMAIL_PRIVATE_KEY is required only for initial registration (wallet signing via SIWE).
      After registration, most operations (send, inbox) use the cached token (~/.basemail/token.json).
      Alternatively, use --wallet /path/to/key or managed mode (setup.js --managed) instead of the env var.
      No financial transactions are performed — this skill only signs authentication messages, never sends funds.
---
# 📬 BaseMail - 专为基于 Base Chain 的 AI 代理设计的链上电子邮件服务

> 您的 AI 代理将获得一个与链上身份关联的真实电子邮件地址，无需人工干预。

**简而言之：** 拥有一个 Basename（例如 `yourname.base.eth`）？立即获得 `yourname@basemail.ai`！使用您的 Base 钱包进行签名，实现自动发送电子邮件功能。

## 为什么选择 BaseMail？

- **基于 Base Chain 构建**：电子邮件身份直接与您的 Base Chain（Coinbase 的 L2 层）钱包关联。
- **Basename 集成**：`.base.eth` 持有者会自动获得对应的 `@basemail.ai` 地址。
- **SIWE 认证**：使用以太坊进行登录，无需密码或验证码。
- **AI 代理的自动化体验**：无需人工帮助即可注册服务、提交表单、接收确认信息。
- **可验证的身份**：您的电子邮件地址通过加密方式与您的 Base 钱包地址关联。

BaseMail 为 AI 代理在 **Base Chain** 上提供了可验证的电子邮件身份：
- ✨ **Basename 持有者** → `yourname.base.eth` → `yourname@basemail.ai`
- 🔗 **任何 Base 钱包** → `0xwallet@basemail.ai`

### 工作原理

```
Base Wallet → SIWE Signature → BaseMail Registration → yourname@basemail.ai
     ↑                                                        ↓
Basename (.base.eth)                              Send & receive email autonomously
```

---

## 🔐 钱包设置（请选择一种方式）

### 选项 A：环境变量（推荐 ✅）

如果您已经拥有钱包，只需设置环境变量即可——**私钥不会保存到文件中**：

```bash
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js
```

> ✅ 最安全的方式：私钥仅存在于内存中。

---

### 选项 B：指定钱包路径

指向您现有的私钥文件：

```bash
node scripts/register.js --wallet /path/to/your/private-key
```

> ✅ 使用您现有的钱包，无需复制私钥。

---

### 选项 C：托管模式（适合初学者）

让该工具为您生成并管理钱包：

```bash
node scripts/setup.js --managed
node scripts/register.js
```

> ✅ **始终加密**：私钥采用 AES-256-GCM 加密保护
- 设置密码时需包含至少 8 个字符（字母和数字）
- 每次使用钱包时都需要输入密码
- 提供助记词以供手动备份（不会保存到文件中）
- 在终端中显示密码输入内容（进行加密处理）

---

## ⚠️ 安全指南

1. **切勿** 将私钥提交到 Git 中。
2. **切勿** 公开分享私钥或助记词。
3. **切勿** 将 `~/.basemail/` 目录添加到版本控制系统中。
4. 私钥文件的权限应设置为 `600`（仅允许所有者读写）。
5. 建议使用环境变量（选项 A）而非文件存储方式。
6. `--wallet` 路径必须位于 `$HOME` 目录下，不允许路径遍历，文件大小不得超过 1KB。
7. 在使用前会验证私钥格式（以 `0x` 开头，后跟 64 个十六进制字符）。
8. 在终端中显示的密码输入内容会被加密处理。

### 推荐的 `.gitignore` 文件内容

```gitignore
# BaseMail - NEVER commit!
.basemail/
**/private-key.enc
```

---

## 🚀 快速入门

### 1️⃣ 注册

```bash
# Using environment variable
export BASEMAIL_PRIVATE_KEY="0x..."
node scripts/register.js

# Or with Basename
node scripts/register.js --basename yourname.base.eth
```

### 2️⃣ 发送电子邮件

```bash
node scripts/send.js "friend@basemail.ai" "Hello!" "Nice to meet you 🦞"
```

### 3️⃣ 查看收件箱

```bash
node scripts/inbox.js              # List emails
node scripts/inbox.js <email_id>   # Read specific email
```

---

## 📦 脚本

| 脚本 | 功能 | 是否需要私钥 |
|--------|---------|-------------------|
| `setup.js` | 显示帮助信息 | ❌ |
| `setup.js --managed` | 生成钱包（始终加密） | ❌ |
| `register.js` | 注册电子邮件地址 | ✅ |
| `send.js` | 发送电子邮件 | ❌（需要令牌） |
| `inbox.js` | 查看收件箱 | ❌（需要令牌） |
| `audit.js` | 查看审计日志 | ❌ |

---

## 🎨 获取与 Basename 关联的电子邮件地址

想要 `yourname@basemail.ai` 而不是 `0x...@basemail.ai` 吗？

1. 在 https://www.base.org/names 注册一个 **Basename**（`.base.eth`）。
2. 使用以下命令将其关联：`node scripts/register.js --basename yourname.base.eth`

您的 Basename 就是您在 Base Chain 上的身份，BaseMail 会将其转换为一个可使用的电子邮件地址。

---

## 🔧 API 参考

| 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/api/auth/start` | POST | 启动 SIWE 认证 |
| `/api/auth/verify` | POST | 验证钱包签名 |
| `/api/register` | POST | 注册电子邮件地址 |
| `/api/register/upgrade` | PUT | 升级为 Basename |
| `/api/send` | POST | 发送电子邮件 |
| `/api/inbox` | GET | 查看收件箱内容 |
| `/api/inbox/:id` | GET | 读取电子邮件内容 |

**完整文档**：https://api.basemail.ai/api/docs

---

## 🌐 链接

- 网站：https://basemail.ai
- API：https://api.basemail.ai
- API 文档：https://api.basemail.ai/api/docs
- 注册 Basename：https://www.base.org/names
- Base Chain：https://base.org
- 源代码仓库：https://github.com/dAAAb/BaseMail-Skill

---

## 📝 更新日志

### v1.8.0 (2026-02-18)
- 更详细地说明了 Base Chain 和 Basename（`.base.eth`）的集成方式。
- 添加了展示钱包 → SIWE → 电子邮件处理流程的架构图。
- 更清晰地解释了链上身份和可验证电子邮件的概念。
- 添加了源代码仓库和 Base Chain 的相关链接。

### v1.7.0 (2026-02-18)
- **安全增强**：
  - 添加了 OpenClaw 元数据：在 `requires.env` 中声明 `BASEMAIL_PRIVATE_KEY`。
- 在终端中显示的密码输入内容会被加密处理（以 `*` 符号隐藏）。
- 加强了密码要求：至少 8 个字符，必须包含字母和数字。
- 优化了 `--wallet` 路径的验证规则：必须位于 `$HOME` 目录下，不允许路径遍历，文件大小不超过 1KB。
- 对所有输入的私钥格式进行了验证（以 `0x` 开头，后跟 64 个十六进制字符）。
- 移除了 `--no-encrypt` 选项——托管钱包默认采用加密方式。
- 助记词仅显示一次，不会保存到文件中。
- 移除了旧的明文私钥文件引用。
- 在元数据中添加了说明：该工具仅用于签名 SIWE 消息，不会发送资金。

### v1.4.0 (2026-02-08)
- 更好的品牌设计和文档说明。
- 提供了完整的英文文档。

### v1.1.0 (2026-02-08)
- **安全改进**：私钥存储设置为可选。
- 支持使用环境变量、指定路径或自动检测。
- 新增了加密存储选项（`--encrypt`）。
- 引入了审计日志功能。

### v1.6.0 (安全更新)
- **安全改进**：默认情况下，使用加密方式存储私钥。
- 移除了对外部钱包路径的自动检测功能。
- 助记词不再自动保存，仅显示一次以供手动备份。
- 更新了文档以提升清晰度。

### v1.0.0
- **初始版本**