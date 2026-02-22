---
name: praxis-gws
description: >
  **Google Workspace CLI（用于Gmail、Calendar和Drive）**  
  这是一个官方的Google API封装工具，支持安全、直接的API访问，无需使用第三方代理。适用于管理电子邮件、日历事件或搜索Google Drive文件。该工具支持Gmail的搜索操作符、标签管理、草稿功能、日历事件创建以及Drive文件的搜索。
---
# Praxis Google Workspace CLI

这是一个用于操作Gmail、Calendar和Drive的官方Google API封装工具，支持直接与Google服务器进行交互，无需使用第三方代理。

## 设置

### 1. 创建Google Cloud项目

1. 访问 [https://console.cloud.google.com](https://console.cloud.google.com)
2. 创建一个新的项目。
3. 启用以下API：
   - Gmail API
   - Google Calendar API
   - Google Drive API

### 2. 创建OAuth凭证

1. 转到 **APIs & Services → Credentials**（APIs与服务 → 凭证）
2. 点击 **Create Credentials → OAuth client ID**（创建凭证 → OAuth客户端ID）
3. 选择应用程序类型为 **Desktop app**（桌面应用程序）。
4. 下载生成的JSON文件。

### 3. 配置Praxis Google Workspace CLI

```bash
praxis-gws auth credentials /path/to/client_secret.json
```

### 4. 进行身份验证

```bash
praxis-gws gmail labels
```

系统会生成一个Google OAuth授权码。请在浏览器中打开该链接，完成授权流程，然后将授权码复制并粘贴回Praxis Google Workspace CLI中。

## 使用方法

### Gmail命令

- **搜索邮件：**
```bash
praxis-gws gmail search "is:unread from:example.com"
praxis-gws gmail search "subject:meeting has:attachment" --max 20
```

- **获取邮件：**
```bash
praxis-gws gmail get <messageId>
```

- **发送邮件：**
```bash
praxis-gws gmail send "recipient@example.com" "Subject" "Body text"
```

- **创建邮件草稿：**
```bash
praxis-gws gmail draft "recipient@example.com" "Subject" "Draft body"
```

- **列出邮件标签：**
```bash
praxis-gws gmail labels
```

- **修改邮件标签：**
```bash
praxis-gws gmail modify <messageId> --add STARRED --remove UNREAD
```

### Calendar命令

- **列出事件：**
```bash
praxis-gws calendar list primary --max 10
praxis-gws calendar list primary --from "2026-02-22T00:00:00" --to "2026-03-01T23:59:59"
```

- **创建事件：**
```bash
praxis-gws calendar create primary "Meeting Title" \
  --from "2026-02-25T14:00:00" \
  --to "2026-02-25T15:00:00"
```

### Drive命令

- **搜索文件：**
```bash
praxis-gws drive search "name contains 'project'"
praxis-gws drive search "mimeType = 'application/vnd.google-apps.document'"
```

- **获取文件元数据：**
```bash
praxis-gws drive get <fileId>
```

## Gmail搜索操作符

- `is:unread` - 查找未读邮件
- `is:starred` - 查找已标记为星号的邮件
- `from:email@example.com` - 查找来自特定发件人的邮件
- `to:email@example.com` - 查找发送给特定收件人的邮件
- `subject:keyword` - 查找主题中包含关键词的邮件
- `after:2026/01/01` - 查找在指定日期之后的邮件
- `before:2026/12/31` - 查找在指定日期之前的邮件
- `has:attachment` - 查找包含附件的邮件
- `in:inbox` - 查找在收件箱中的邮件
- `label:important` - 查找带有特定标签的邮件

## 常见标签

- `INBOX` - 收件箱
- `SENT` - 已发送的邮件
- `DRAFT` - 草稿
- `STARRED` - 已标记为星号的邮件
- `UNREAD` - 未读的邮件
- `IMPORTANT` - 重要的邮件
- `TRASH` - 垃圾箱中的邮件
- `SPAM` - 垃圾邮件

## 安全性

- OAuth令牌存储在本地文件 `~/.config/praxis-gws/` 中。
- 支持直接与Google API进行交互（无需代理）。
- 使用官方的 `googleapis` Node.js 库。
- 需要的权限范围：
  - `https://www.googleapis.com/auth/gmail.modify`
  - `https://www.googleapis.com/auth/calendar`
  - `https://www.googleapis.com/auth/drive.readonly`

## 故障排除

- **错误：credentials.json文件未找到**  
  → 运行 `praxis-gws auth credentials /path/to/client_secret.json` 命令来重新生成凭证。

- **错误：授权令牌无效/已过期**  
  → 删除 `~/.config/praxis-gws/token.json` 文件，然后重新运行Praxis Google Workspace CLI以触发新的OAuth授权流程。

- **出现“Google尚未验证此应用”警告**  
  → 点击 **Advanced → Go to [项目名称] (unsafe)**（高级设置 → 前往[项目名称]（不安全））以继续使用该工具。

## CLI脚本

Praxis Google Workspace CLI的下载地址：
```
scripts/praxis-gws.js
```

使用Praxis Google Workspace CLI需要Node.js环境以及`googleapis` npm包：
```bash
npm install -g googleapis
```