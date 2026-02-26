---
name: outlook-hack
version: 5.0.0
description: "你的代理程序整天都在读取Outlook邮件，并为你起草回复内容，但却一个回复也不会发送出去。每次点击浏览器都会消耗90天的时间。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "os": ["linux", "darwin"],
        "requires": { "capabilities": ["browser"] },
        "notes":
          {
            "security": "This skill captures a refresh token from Microsoft Teams' localStorage via browser tab sharing, then uses it to call Microsoft Graph API. No API keys or admin approval needed. SENDING IS CODE-DISABLED: the fetch script physically blocks /sendmail, /reply, /replyall, /forward. It reads, searches, and creates drafts only. Drafts land in the user's Drafts folder for manual review and sending. Tokens are stored at ~/.openclaw/credentials/outlook-msal.json with 0600 permissions. Refresh tokens auto-rotate and last 90+ days.",
          },
      },
  }
---
# Outlook 非法操作技巧

**注意：** 你的 AI 代理不会在凌晨 3 点给 CEO 发送邮件。  
这既不是因为设置了相关限制，也不是因为违反了公司政策，而是因为代码本身根本无法发送邮件。我们彻底移除了这一功能——就像从小孩手中拿走电锯一样，没有任何商量的余地。

## 功能介绍：  
- 📧 阅读、搜索并批量获取所有文件夹中的邮件  
- 📎 为每封邮件索引所有附件（包括名称、类型和大小）  
- 📊 生成邮件摘要，显示主要发件人、未读邮件数量以及邮件正文内容  
- ✏️ 创建邮件草稿（保存在“草稿”文件夹中，不会实际发送）  
- 📅 访问日历事件，浏览联系人信息  

## 快速入门：  
### 1. 获取令牌（只需一次，约 30 秒）  
在 Chrome 浏览器中打开 **Microsoft Teams**（`teams.cloud.microsoft`），并使用 OpenClaw 浏览器中继工具。然后从 `localStorage` 中提取刷新令牌：  
```javascript
// Extract the MSAL refresh token from Teams localStorage
const keys = Object.keys(localStorage).filter(k => k.includes('refreshtoken'));
const parsed = JSON.parse(localStorage.getItem(keys[0]));
// parsed.secret is the refresh token
```  

将凭据保存到 `~/.openclaw/credentials/outlook-msal.json` 文件中：  
```json
{
  "client_id": "5e3ce6c0-2b1f-4285-8d4b-75ee78787346",
  "tenant_id": "<your-tenant-id>",
  "refresh_token": "<the-secret-value>",
  "origin": "https://teams.cloud.microsoft",
  "scope": "https://graph.microsoft.com/.default offline_access",
  "api": "graph",
  "updated_at": "<iso-timestamp>"
}
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

**输出结果：**  
`~/.openclaw/workspace/data/outlook-emails/`  
- `raw-emails.jsonl`：完整的邮件数据（主题、发件人、收件人、正文内容、预览）  
- `attachments-index.jsonl`：每封邮件的所有附件信息  
- `email-summary.md`：包含统计信息和每封邮件摘要的可读性摘要文件  

## 关于 Teams 刷新令牌的原理：  
Microsoft 在 2026 年停止了对传统 Outlook 网页应用的支持。新的 Outlook（`outlook.cloud.microsoft`）使用基于“Proof-of-Possession”（PoP）机制的令牌，这些令牌与浏览器紧密绑定，无法被提取或重复使用。  

**解决方法：**  
Microsoft Teams 会在 `localStorage` 中存储一个标准的 MSAL 刷新令牌。这个令牌可以用来换取 Graph API 访问令牌，而无需管理员的额外授权，因为 Teams 的第一方客户端 ID 已经预先获得了所需的权限。  

**关键点：**  
令牌请求的头部必须包含 `Origin: https://teams.cloud.microsoft`，这可以通过 `curl` 或 `fetch` 命令轻松实现。  

### 为何无需管理员授权：  
- Teams 的客户端 ID（`5e3ce6c0-2b1f-4285-8d4b-75ee78787346`）属于微软的第一方应用  
- 第一方应用已经获得了对 Graph API 的访问权限  
- 刷新令牌继承了用户的现有会话信息，因此无需再次请求授权  
- 由于没有授权流程，你的团队管理员根本看不到任何授权请求  

## 令牌的有效期与更新：  
- 刷新令牌的有效期为 90 天以上，每次使用后都会自动更新  
- 脚本会在每次令牌交换后保存新的令牌  
- 只要脚本至少每 90 天运行一次，你就无需再操作浏览器  
- 仅会在以下情况下失效：密码更改、Teams 会话被撤销，或用户长时间未使用（超过 90 天）  
- 每季度最多只需点击浏览器一次即可。实际上，可能永远都不需要再次操作。  

## 技术原理：  
1. 通过浏览器中继工具将你的 Teams 页面共享给 OpenClaw  
2. 代理程序从 `localStorage` 中提取 MSAL 刷新令牌  
3. 令牌被保存到 `~/.openclaw/credentials/outlook-msal.json` 文件中  
4. `outlook-mail-fetch.mjs` 脚本使用该令牌换取 Graph API 访问令牌  
5. 脚本通过 `https://graph.microsoft.com/v1.0/` 发起 REST 请求  
6. 每次令牌交换后都会保存新的令牌，从而实现永久访问权限  

## 架构说明：  
- **完全依赖 Node.js（v18 及以上版本），不使用任何 npm 包**  
- **无发送功能**：该脚本不具备发送、回复或转发邮件的能力  
- **限制请求频率**：每次请求最多获取 50 封邮件，并支持自动分页  
- **邮件正文处理**：去除 HTML 标签，统一空白字符格式，并将正文长度限制在 3000 个字符以内  
- **使用 Graph API v1.0**：采用微软当前支持的 API，而非已弃用的 Outlook REST v2.0  

## 相关技能：**  
[**teams-hack**](https://clawhub.com/globalcaos/teams-hack) 也可以使用相同的 MSAL 刷新令牌。只需从 Teams 的 `localStorage` 中提取一次令牌，即可同时获取邮件访问权限和聊天/频道搜索功能。  
这两个技能会共享同一个凭据文件：  
```
~/.openclaw/credentials/outlook-msal.json
```  
如果其中一个技能更新了令牌，另一个技能也会自动获得更新后的权限。令牌每次使用后都会自动更新，有效期为 90 天以上。  

| 技能        | 功能                        | 是否支持发送邮件？       |
|------------|---------------------------|-------------------|
| **outlook-hack**   | 邮件：阅读、搜索、创建草稿、访问文件夹和附件、日历、联系人 | ✅ 无法发送邮件           |
| **[teams-hack]**   | 聊天：阅读、发送消息、访问频道、搜索、查看在线状态、组织目录 | 可以发送聊天消息         |

## 完整解决方案：  
结合 [**teams-hack**](https://clawhub.com/globalcaos/teams-hack) 可实现聊天功能，  
结合 [**whatsapp-ultimate**](https://clawhub.com/globalcaos/whatsapp-ultimate) 可实现消息传递功能，  
结合 [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice) 可实现语音通信功能。  

👉 **[克隆它，修改它，让它成为你的工具吧。](https://github.com/globalcaos/clawdbot-moltbot-openclaw)**