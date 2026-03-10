---
name: outlook-hack
version: 3.0.0
description: "你的代理程序整天都在读取Outlook中的邮件，并为你草拟回复内容，但却一个都不会发送出去。即使你礼貌地请求它发送，它也不会照做。"
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
# Outlook 功能扩展

**你的 AI 代理不会在凌晨 3 点给 CEO 发送邮件。**

这并不是因为设置了相关限制，也不是因为有政策规定，而是因为代码本身无法执行发送邮件的功能。我们像从小孩手中拿走电锯一样彻底移除了这一功能——没有任何商量余地。

## 功能概述

- 📧 阅读、搜索并批量获取所有文件夹中的邮件
- 📎 为每封邮件生成附件索引（包括附件名称、类型和大小）
- 📊 生成邮件摘要，显示主要发件人、未读邮件数量以及邮件正文内容
- ✏️ 创建邮件草稿（保存在“草稿”文件夹中，不会实际发送）
- 📅 访问日历事件，浏览联系人信息

## 快速入门

### 1. 令牌提取（一次性操作，约 30 秒）

**请从“Microsoft Teams”标签页中提取令牌，** **切勿从 Outlook 中提取。** 大多数组织已不再使用传统的 Outlook，新的 Outlook 使用的是 PoP（Proof-of-Possession）令牌，这类令牌无法被提取。“Microsoft Teams”标签页提供的 MSAL 刷新令牌（有效期 90 天，会自动更新）同时支持本功能以及 `teams-hack` 功能。

在 Chrome 浏览器中打开 **Microsoft Teams**（`teams.cloud.microsoft`），并使用 OpenClaw 浏览器中继工具。然后运行以下代码以获取令牌：

```javascript
(() => {
  const keys = Object.keys(localStorage).filter(
    (k) => k.includes("refreshtoken") || k.includes("RefreshToken"),
  );
  const parsed = JSON.parse(localStorage.getItem(keys[0]));
  const accountKeys = Object.keys(localStorage).filter((k) => {
    try {
      return JSON.parse(localStorage.getItem(k)).tenantId;
    } catch {
      return false;
    }
  });
  let tenantId = null;
  for (const k of accountKeys) {
    try {
      tenantId = JSON.parse(localStorage.getItem(k)).tenantId;
      break;
    } catch {}
  }
  return { secret: parsed.secret, tenantId };
})();
```

通过 `teams` CLI（而非 `outlook-mail-fetch` 脚本）保存令牌：

```bash
teams token store --refresh-token "<secret>" --tenant-id "<tenantId>"
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

**输出路径：`~/.openclaw/workspace/data/outlook-emails/`

- `raw-emails.jsonl`：包含完整的邮件信息（主题、发件人、收件人、正文内容、邮件预览）
- `attachments-index.jsonl`：每封邮件的附件信息
- `email-summary.md`：包含邮件统计信息和摘要的易读格式文件

## 重要提示：**令牌来源**

| 来源                        | 令牌类型                          | 是否可提取？         | 有效期                |
| --------------------------------------- | ------------------------------- | ------------------ | ----------------------- |
| Microsoft Teams (`teams.cloud.microsoft`) | MSAL 刷新令牌                     | ✅ 可提取             | 90 天，自动更新           |
| 新版 Outlook (`outlook.cloud.microsoft`) | PoP 令牌                          | ❌ 无法提取           | 令牌与浏览器绑定           |
| 传统 Outlook (`outlook.office.com`)      | 携带者访问令牌                      | ⚠️ 已弃用             | 大多数组织已迁移至新版 Outlook     |

**请始终从“Microsoft Teams”标签页中提取令牌。** 新版 Outlook 使用的 PoP 令牌无法被提取或重复使用；传统 Outlook 已被弃用，大多数组织也已不再使用。

## 工作原理（技术细节）

1. 通过浏览器中继工具将你的 **Microsoft Teams** 标签页信息共享给 OpenClaw
2. 代理程序从 `localStorage` 中获取 MSAL 刷新令牌
3. 令牌会被存储并通过 `teams-token-store` 交换为 Graph API 访问令牌
4. 本功能与 `teams-hack` 功能都会使用 `~/.openclaw/credentials/outlook-msal.json` 文件（权限配置）
5. `outlook-mail-fetch.mjs` 脚本使用 Graph API 访问令牌来执行邮件操作
6. 刷新令牌的有效期为 90 天，每次使用后都会自动更新

**注意：** 该功能并不会抓取网页内容，而是直接通过你的浏览器会话与 Outlook 的 REST API 进行交互。

## 令牌有效期与更新规则

- **MSAL 刷新令牌**：有效期 90 天，每次使用后自动更新（与 `teams-hack` 功能共享）
- **访问令牌**：有效期约 1 小时，由脚本自动更新
- 使用任一功能的定时任务都会保持令牌的有效性
- 令牌过期后：需要重新从“Microsoft Teams”标签页中提取令牌（在同一浏览器会话内操作）

## 架构特点

- **完全依赖 Node.js（v18+）**，不使用 npm 包
- **无发送/回复/转发功能**：该脚本不具备发送、回复或转发邮件的能力
- **速率限制**：每次请求最多获取 50 封邮件，支持自动分页
- **邮件正文处理**：去除 HTML 标签，统一空白字符格式，并将正文长度限制在 3000 个字符以内

## 完整技术栈

该功能可与 [**whatsapp-ultimate**](https://clawhub.com/globalcaos/whatsapp-ultimate) 结合使用实现消息传递，也可与 [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice) 结合使用实现语音功能。

👉 **[克隆它，修改它，让它成为属于你的工具。](https://github.com/globalcaos/tinkerclaw)**