---
name: outlook-hack
version: 3.0.0
description: "你的代理程序整天都在读取Outlook中的电子邮件，并为你草拟回复内容，但却一个都不会发送出去。即使你礼貌地请求它发送，它也不会照做。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "os": ["linux", "darwin"],
        "requires": { "capabilities": ["browser"] },
        "notes":
          {
            "security": "This skill captures Outlook Web session tokens via browser tab sharing to make direct REST calls to Microsoft's Outlook REST API v2.0. No API keys or admin approval needed. SENDING IS CODE-DISABLED: the fetch script physically blocks /sendmail, /reply, /replyall, /forward. It reads, searches, and creates drafts only. Drafts land in the user's Drafts folder for manual review and sending. Tokens are stored at ~/.openclaw/credentials/outlook-msal.json with 0600 permissions.",
          },
      },
  }
---
# Outlook 小技巧

**你的 AI 代理不会在凌晨 3 点给 CEO 发邮件。**

这既不是因为设置了限制，也不是因为有相关政策，而是因为代码本身无法发送邮件。我们彻底移除了这个功能——就像从小孩手中拿走电锯一样，没有任何商量的余地。

## 功能介绍

- 📧 阅读、搜索并批量获取所有文件夹中的邮件
- 📎 为每封邮件索引所有附件（名称、类型、大小）
- 📊 生成邮件摘要，包括主要发件人、未读邮件数量和邮件正文
- ✏️ 创建邮件草稿（保存在“草稿”文件夹中，不会实际发送）
- 📅 访问日历事件，👥 浏览联系人

## 快速入门

### 1. 生成访问令牌（一次性操作，约 30 秒）

在 Chrome 浏览器中打开 **经典版 Outlook**（`outlook.office.com`），并使用 OpenClaw 浏览器中继工具。然后运行以下代码：

```javascript
// Extract the Outlook REST API bearer token from localStorage
const keys = Object.keys(localStorage);
const outlookKey = keys.find(k =>
  k.includes('accesstoken') &&
  k.includes('outlook.office.com') &&
  k.includes('mail.readwrite')
);
const parsed = JSON.parse(localStorage.getItem(outlookKey));
// parsed.secret is the bearer token (valid ~25 hours)
```

保存生成的令牌：

```bash
node {baseDir}/scripts/outlook-mail-fetch.mjs --store-token <token>
```

### 2. 验证访问权限

```bash
node {baseDir}/scripts/outlook-mail-fetch.mjs --test
```

### 3. 批量获取邮件数据

```bash
# Last 6 months (default)
node {baseDir}/scripts/outlook-mail-fetch.mjs --fetch-all

# Custom range
node {baseDir}/scripts/outlook-mail-fetch.mjs --fetch-all --months 12
```

**输出目录：** `~/.openclaw/workspace/data/outlook-emails/`
- `raw-emails.jsonl` — 完整的邮件数据（主题、发件人、收件人、正文、预览）
- `attachments-index.jsonl` — 每封邮件的附件信息
- `email-summary.md` — 可读的邮件摘要，包含统计信息和每封邮件的详细信息

## 注意：经典版 Outlook 与新版 Outlook 的区别

| 功能 | 经典版 Outlook (`outlook.office.com`) | 新版 Outlook (`outlook.cloud.microsoft`) |
|---------|------|-----|
| 令牌类型 | **Bearer**（存储在 `localStorage` 中的明文 `secret`） | **PoP**（加密的 `data` 和 `nonce`） |
| 是否可提取 | ✅ 是 | ❌ 否 |
| Service Worker 支持 | 不支持 | 支持（拦截所有 API 调用） |
| 使用的 API | Outlook REST v2.0 | MessageService + OWA 技术栈 |

**请始终使用经典版 Outlook。** 新版 Outlook 使用基于 Proof-of-Possession（PoP）的令牌，这些令牌与浏览器紧密绑定，无法被提取或重放。

如果 Outlook 将你重定向到 `outlook.cloud.microsoft`，请直接访问 `https://outlook.office.com/mail/`。

## 工作原理（技术细节）

1. 通过浏览器中继工具将你的经典版 Outlook Web 页面共享给 OpenClaw。
2. 代理程序从 `localStorage` 中读取 MSAL 令牌（请求目标：`https://outlook.office.com`）。
3. 令牌会被保存到 `~/.openclaw/credentials/outlook-msal.json` 文件中（权限设置为 0600）。
4. `outlook-mail-fetch.mjs` 脚本会通过 `https://outlook.office.com/api/v2.0/` 发起 REST 请求。
5. 令牌的有效期为约 25 小时。次日需要再次执行上述步骤以重新获取令牌。

需要注意的是，这个工具并不会直接抓取网页内容，而是通过你的现有浏览器会话来调用 Outlook 的 REST API 进行操作。

## 令牌的有效期与刷新

- 令牌从生成之日起有效约 25 小时。
- 脚本会在每次请求前检查令牌是否过期。
- 令牌过期后，需要通过浏览器重新获取令牌（只需执行一次 `evaluate` 函数）。
- Microsoft 的第一方客户端 ID 需要使用加密的客户端认证机制。

## 架构说明

- **完全依赖 Node.js（v18+）开发，不使用任何 npm 包**。
- **无发送/回复/转发功能**——该工具不具备发送、回复或转发邮件的能力。
- **速率限制**：每次请求最多获取 50 封邮件，支持自动分页。
- **邮件正文处理**：去除 HTML 标签，统一空白字符格式，并将正文截断为 3000 个字符。

## 完整技术栈

该工具可与 [**whatsapp-ultimate**](https://clawhub.com/globalcaos/whatsapp-ultimate) 结合使用以实现消息传递功能，也可与 [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice) 结合使用以实现语音交互。

👉 **[克隆它，修改它，让它成为属于你的工具。](https://github.com/globalcaos/clawdbot-moltbot-openclaw)**