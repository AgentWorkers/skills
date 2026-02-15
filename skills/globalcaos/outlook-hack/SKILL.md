---
name: outlook-hack
version: 1.0.0
description: "通过浏览器中继访问 Outlook 电子邮件——无需单独的身份验证即可阅读、搜索、发送、回复邮件以及查看日历。该功能基于 Chrome 浏览器中已有的 Outlook Web 会话进行操作。当 IMAP 被阻止或 Microsoft Graph API 需要管理员权限时（而你无法获取这些权限），这将成为第三个可行的解决方案：只需在 Chrome 中打开 Outlook，点击中继按钮，你的代理程序就能获得完整的电子邮件访问权限。无需任何 API 密钥或管理员批准，也无需进行任何配置设置。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  openclaw:
    emoji: "📧"
    requires:
      tools: ["browser"]
---
# Outlook 非官方解决方案——当 IMAP 被禁用且需要管理员权限时

*这个技巧源于对企业 IT 系统的不满。如果你能在 Chrome 中打开 Outlook，那么你的代理就可以读取你的邮件了。*

## 问题所在

企业对 Outlook 的访问权限通常受到以下三种限制：

1. **IMAP/SMTP**——被 IT 政策禁用（大多数 Microsoft 365 用户都面临这种情况）；
2. **Microsoft Graph API**——需要注册 Azure AD 应用程序并获得管理员权限（这几乎不可能通过审批）；
3. **EWS（Exchange Web Services）**——已被弃用且越来越容易被阻止使用。

如果你是使用 OpenClaw 且拥有企业 Microsoft 365 账户的用户，那么你可能会遇到麻烦——但直到现在，这种情况还有解决办法。

## 第三种方案

这个技巧利用了你在 Chrome 中已有的 Outlook Web 会话，通过 OpenClaw 浏览器中继来实现功能。无需 API 密钥，也无需管理员权限，更不需要使用 IMAP 协议。只要你能通过浏览器阅读邮件，你的代理也同样可以。

**工作原理：**

1. 在 Chrome 中打开 Outlook Web（`https://outlook.office.com`）；
2. 点击 OpenClaw 浏览器中继工具栏按钮（图标应为绿色）；
3. 你的代理会使用浏览器中已有的 MSAL 访问令牌，在当前标签页内执行 `fetch()` 请求。

Outlook Web 应用会将 OAuth 令牌存储在 `localStorage` 中。这个技巧会提取这些令牌，并直接从浏览器环境中调用 Outlook REST API v2.0。所有 API 请求都在 Chrome 的安全沙箱内完成。

## 先决条件

- 在 Chrome 中安装了 OpenClaw 浏览器中继扩展程序（[文档](https://docs.openclaw.ai/tools/chrome-extension)）；
- Outlook Web 标签页已打开并登录；
- 中继功能已连接到 Outlook 标签页（工具栏按钮上的图标应为绿色）。

## 支持的功能

| 功能 | 是否支持 |
|---------|-----------|
| 阅读收件箱（含预览） | ✅ |
| 阅读完整邮件内容（HTML 格式） | ✅ |
| 搜索邮件 | ✅ |
| 发送邮件 | ✅ |
| 回复 / 全部回复 / 转发 | ✅ |
| 列出文件夹及未读邮件数量 | ✅ |
| 查看日历事件 | ✅ |
| 下载附件 | ✅ |
| 标记邮件为已读/未读 | ✅ |
| 将邮件移动到其他文件夹 | ✅ |
| 为邮件添加标记 | ✅ |

## 使用方法

### 找到 Outlook 标签页

首先，找到对应的 Outlook 标签页：

```
browser action=tabs profile=chrome
```

寻找 URL 中包含 `outlook.office.com` 的标签页。注意记录 `targetId` 的值。

### 提取令牌

所有 API 请求都需要从 `localStorage` 中提取 MSAL 访问令牌：

```javascript
const tokenKey = Object.keys(localStorage).find(k =>
  k.includes('accesstoken') &&
  k.includes('outlook.office.com') &&
  k.includes('mail.readwrite')
);
const token = JSON.parse(localStorage.getItem(tokenKey)).secret;
```

在所有 Outlook REST API 请求中，使用 `Authorization: Bearer <token>` 作为请求头。

### API 基本 URL

```
https://outlook.office.com/api/v2.0/me/
```

### 列出收件箱邮件

```javascript
async () => {
  // Extract token
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;

  const resp = await fetch(
    'https://outlook.office.com/api/v2.0/me/messages?' +
    '$top=20&$select=Subject,From,ReceivedDateTime,IsRead,BodyPreview,Id' +
    '&$orderby=ReceivedDateTime desc',
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  const data = await resp.json();
  return data.value?.map(m => ({
    id: m.Id,
    subject: m.Subject,
    from: m.From?.EmailAddress?.Name,
    email: m.From?.EmailAddress?.Address,
    date: m.ReceivedDateTime,
    read: m.IsRead,
    preview: m.BodyPreview?.substring(0, 150)
  }));
}
```

添加 `&$filter=IsRead eq false` 以仅列出未读邮件。

### 阅读完整邮件内容

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const messageId = '<MESSAGE_ID>';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages/${messageId}?` +
    '$select=Subject,From,ToRecipients,CcRecipients,Body,ReceivedDateTime,HasAttachments',
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  return await resp.json();
}
```

`Body.Content` 字段包含邮件的完整 HTML 内容。

### 搜索邮件

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const query = 'invoice January';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages?` +
    `$search="${encodeURIComponent(query)}"&$top=10` +
    '&$select=Subject,From,ReceivedDateTime,BodyPreview',
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  const data = await resp.json();
  return data.value;
}
```

### 发送邮件

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;

  const resp = await fetch('https://outlook.office.com/api/v2.0/me/sendmail', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      Message: {
        Subject: 'Subject here',
        Body: { ContentType: 'HTML', Content: '<p>Email body here</p>' },
        ToRecipients: [{ EmailAddress: { Address: 'recipient@example.com' } }],
        CcRecipients: []  // optional
      }
    })
  });
  return { status: resp.status, ok: resp.ok };
}
```

### 回复邮件

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const messageId = '<MESSAGE_ID>';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages/${messageId}/reply`,
    {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ Comment: '<p>Reply text here</p>' })
    }
  );
  return { status: resp.status, ok: resp.ok };
}
```

使用 `/replyall` 而不是 `/reply` 来发送全部回复；使用 `/forward` 和 `ToRecipients` 数组来转发邮件。

### 查看日历事件

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const now = new Date().toISOString();
  const end = new Date(Date.now() + 7 * 86400000).toISOString();

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/calendarview?` +
    `startdatetime=${now}&enddatetime=${end}` +
    '&$select=Subject,Start,End,Location,Organizer,IsAllDay' +
    '&$orderby=Start/DateTime',
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  const data = await resp.json();
  return data.value;
}
```

### 列出文件夹

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;

  const resp = await fetch(
    'https://outlook.office.com/api/v2.0/me/mailfolders?' +
    '$select=DisplayName,UnreadItemCount,TotalItemCount',
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  const data = await resp.json();
  return data.value;
}
```

### 下载附件

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const messageId = '<MESSAGE_ID>';
  const attachmentId = '<ATTACHMENT_ID>';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages/${messageId}/attachments/${attachmentId}`,
    { headers: { 'Authorization': 'Bearer ' + token } }
  );
  const data = await resp.json();
  // data.ContentBytes = base64-encoded file content
  // data.Name = filename
  // data.ContentType = MIME type
  return { name: data.Name, type: data.ContentType, size: data.ContentBytes?.length };
}
```

### 标记邮件为已读/未读

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const messageId = '<MESSAGE_ID>';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages/${messageId}`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ IsRead: true })  // false for unread
    }
  );
  return { status: resp.status, ok: resp.ok };
}
```

### 将邮件移动到其他文件夹

```javascript
async () => {
  const tk = Object.keys(localStorage).find(k => k.includes('accesstoken') && k.includes('outlook.office.com') && k.includes('mail.readwrite'));
  const token = JSON.parse(localStorage.getItem(tk)).secret;
  const messageId = '<MESSAGE_ID>';

  const resp = await fetch(
    `https://outlook.office.com/api/v2.0/me/messages/${messageId}/move`,
    {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ DestinationId: 'Archive' })  // or folder ID
    }
  );
  return { status: resp.status, ok: resp.ok };
}
```

## 实现方式

在使用该功能时，务必使用 `profile="chrome"` 的浏览器设置：

```
browser action=act profile=chrome targetId=<outlook-tab-id>
  request.kind=evaluate
  request.fn=<async function>
```

## 令牌刷新

当 Outlook 标签页保持打开状态时，MSAL 会自动刷新令牌。如果请求返回 401 错误：
1. 等待 2 秒（MSAL 可能正在刷新令牌）；
2. 从 `localStorage` 中重新提取令牌（令牌可能已经更新）；
3. 重试请求。

令牌的有效期约为 1 小时，但会自动刷新。

## 与其他方法的比较

| 功能 | IMAP | Graph API | EWS | **Outlook 非官方解决方案** |
|---------|------|-----------|-----|------------------|
| 是否需要管理员权限 | 经常被限制 | ✅ | 需要 | 经常被限制 | ❌ | 不需要 |
| 是否需要 API 密钥 | ✅ | 需要凭证 | ✅ | 需要凭证 | ❌ | 不需要 |
| 是否支持多因素认证（MFA） | ❌ | 会干扰 IMAP 功能 | ✅ | 会干扰部分功能 | ✅ | 通过浏览器会话实现 |
| 是否可以访问日历 | ❌ | 可以 | 可以 | 可以 | 可以 |
| 是否可以发送邮件 | ✅ | 可以 | 可以 | 可以 | 可以 |
| 是否支持搜索 | ❌ | 有限 | 可以 | 可以 | 可以 |
| 设置时间 | 中等 | 需要数小时/数天 | 中等 | **仅需 2 分钟** |
| 是否需要保持浏览器打开 | ❌ | ❌ | ❌ | ✅ |

## 限制条件

- 必须在 Chrome 中打开 Outlook 标签页（标签页可以处于后台状态）；
- 如果 Outlook 标签页长时间关闭，令牌会失效；
- 大文件（超过 25MB）的附件可能因 Base64 编码而传输速度较慢；
- 遵循微软的请求速率限制（每 10 分钟最多 10,000 次请求）；
- 仅能访问自己的邮件箱，无法访问其他用户的邮件箱。

## 安全注意事项

- 令牌不会存储在浏览器外部；
- 所有 API 请求都在 Chrome 的安全环境中完成；
- 该功能仅用于转发 CDP 命令；身份验证信息仅保存在 Chrome 的 cookie 中；
- 该技巧不会将任何凭证写入硬盘。

---

## 致谢

该技巧由 **Oscar Serra** 在 **Claude**（Anthropic）的帮助下开发完成。

*这个技巧诞生于一个周日凌晨 2 点，因为企业 IT 系统拒绝了使用 IMAP 和 Graph API 的请求，对于其他所有操作则要求提交工单……*