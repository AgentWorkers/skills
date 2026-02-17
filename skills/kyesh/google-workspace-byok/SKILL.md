---
name: google-workspace-byok
description: >
  **使用您自己的 GCP 项目凭证（BYoK – Bring Your Own Key）集成 Google 日历和 Gmail**  
  通过直接使用您自己的 Google Cloud 项目凭证（BYoK）进行 OAuth2 认证，您可以访问多个 Google 账户中的日历、事件和电子邮件信息。  
  **功能支持：**  
  - 查看日历和事件  
  - 阅读电子邮件  
  - 下载附件  
  - 从 PDF 附件中提取文本  
  - 列出日历  
  - 获取事件详情  
  - 查看日程安排（空闲/忙碌状态）  
  - 管理多个 Google 账户  
  **适用场景：**  
  当用户需要查看日历、阅读电子邮件或管理日程安排时，此功能非常实用。
---
# Google Workspace BYoK（使用您自己的密钥）

通过您自己的 GCP 项目 OAuth2 凭据直接访问 Google 日历和 Gmail API。支持多个 Google 账户。

## 先决条件

- **Node.js**（v18+）
- 一个已启用 Google 日历和 Gmail API 的 **Google Cloud 项目**
- 来自您的 GCP 项目的 OAuth2 **桌面应用** 凭据

## 设置

### 第 1 步：安装依赖项

```bash
cd {baseDir}/scripts && npm install
```

这会安装 `googleapis`（Google API 客户端）和 `mupdf`（用于提取电子邮件附件中的 PDF 文本的工具）。

### 第 2 步：创建一个 Google Cloud 项目

1. 访问 [Google Cloud 控制台](https://console.cloud.google.com) 并创建一个新项目（或使用现有项目）。
2. 启用 **Google 日历 API** 和 **Gmail API**：
   - 转到 **APIs & Services → Library**
   - 搜索 “Google 日历 API” → 点击 **Enable**
   - 搜索 “Gmail API” → 点击 **Enable**

### 第 3 步：配置 OAuth 同意屏幕

1. 转到 **Google Auth Platform → Audience**（[直接链接](https://console.cloud.google.com/auth/audience)）
2. 如果有提示，配置同意屏幕：
   - **应用名称**：任意名称（例如：“OpenClaw”）
   - **用户支持邮箱**：您的邮箱
   - **权限范围**：跳过（授权脚本会在运行时请求权限范围）
3. 如果您的应用处于 **测试** 发布状态（默认设置），将您想要授权的每个 Google 账户添加为 **测试用户**：
   - 在 **Test users** 下，点击 **Add users**
   - 输入您要连接的每个账户的邮箱地址
   - 保存

> **⚠️ 重要提示：** 处于 “测试” 状态的应用的令牌有效期为 7 天。要获取长期有效的令牌，请将您的应用发布到 “Production” 状态。对于个人 Gmail 账户（外部用户类型），您可以跳过 Google 的验证审核——在同意过程中您只会看到 “未验证的应用” 警告。这对于个人使用是可行的。

### 第 4 步：创建 OAuth 凭据

1. 转到 **Google Auth Platform → Clients**（[直接链接](https://console.cloud.google.com/auth/clients)）
2. 点击 **Create Client** → 选择 **Desktop app** 作为应用类型
3. 为其命名（例如：“OpenClaw”）
4. 点击 **Create** 并 **下载凭据 JSON 文件**
5. 运行设置脚本：

```bash
node {baseDir}/scripts/setup.js --credentials /path/to/downloaded-credentials.json
```

这将把您的凭据复制到 `~/.openclaw/google-workspace-byok/credentials.json` 文件中。

### 第 5 步：授权 Google 账户

对于您想要连接的每个 Google 账户：

```bash
node {baseDir}/scripts/auth.js --account <label>
```

`<label>` 是您用来引用该账户的友好名称（例如：“personal”（个人）、“work”（工作）或 “household”（家庭）。

**授权流程：**
1. 脚本会打印出一个授权 URL。
2. 在浏览器中打开该 URL 并使用相应的 Google 账户登录。
3. 授予所需的权限。
4. 您将被重定向到 `http://localhost/...` —— 这是正常的，页面不会加载。
5. 从浏览器地址栏复制完整的 URL 并将其粘贴回脚本中。
6. 脚本会将代码转换为令牌并保存它们。

**请求的权限范围（默认值——读写权限）：**
- `calendar` —— 对 Google 日历的完整读写访问权限
- `gmail.readonly` —— 对 Gmail 的只读访问权限

如果需要只读日历访问权限，可以使用 `--readonly` 参数。

令牌存储在 `~/.openclaw/google-workspace-byok/tokens/<label>.json` 文件中。

## 使用方法

所有脚本都位于 `{baseDir}/scripts/` 目录下。使用 `node` 命令来运行它们。

### 日历

```bash
# List all calendars
node {baseDir}/scripts/calendar.js --account <label> --action list-calendars

# List upcoming events (default: next 7 days, primary calendar)
node {baseDir}/scripts/calendar.js --account <label> --action events

# List events with options
node {baseDir}/scripts/calendar.js --account <label> --action events --calendar <calendarId> --days <number> --max <number>

# Get a specific event
node {baseDir}/scripts/calendar.js --account <label> --action get-event --calendar <calendarId> --event-id <eventId>

# Check free/busy
node {baseDir}/scripts/calendar.js --account <label> --action freebusy --days <number>
```

### Gmail

```bash
# List recent emails (default: 10)
node {baseDir}/scripts/gmail.js --account <label> --action list

# Search emails
node {baseDir}/scripts/gmail.js --account <label> --action list --query "from:someone@example.com" --max 20

# Read a specific email (includes attachment metadata with IDs)
node {baseDir}/scripts/gmail.js --account <label> --action read --message-id <messageId>

# Download all attachments from an email
node {baseDir}/scripts/gmail.js --account <label> --action attachment --message-id <messageId> --out-dir /tmp/attachments

# Download a specific attachment
node {baseDir}/scripts/gmail.js --account <label> --action attachment --message-id <messageId> --attachment-id <id> --out-dir /tmp

# List labels
node {baseDir}/scripts/gmail.js --account <label> --action labels
```

Gmail 搜索使用与 Gmail 网页搜索框相同的查询语法（例如：`is:unread`、`from:`、`newer_than:1d`、`has:attachment`）。

### 读取 PDF 附件

该工具使用了 `mupdf` 来提取 PDF 附件中的文本——适用于新闻通讯、发票、学校通知等文件。它能够很好地处理多语言文本（日语、中文等）。

```bash
# 1. Download the attachment
mkdir -p /tmp/attachments
node {baseDir}/scripts/gmail.js --account <label> --action attachment --message-id <id> --out-dir /tmp/attachments

# 2. Extract text from the PDF
node --input-type=module -e "
import * as mupdf from '{baseDir}/scripts/node_modules/mupdf/dist/mupdf.js';
import fs from 'fs';
const data = fs.readFileSync('/tmp/attachments/filename.pdf');
const doc = mupdf.Document.openDocument(data, 'application/pdf');
for (let i = 0; i < doc.countPages(); i++) {
  const page = doc.loadPage(i);
  console.log(page.toStructuredText('preserve-whitespace').asText());
}
"
```

> **注意：** `mupdf` 是一个 ESM 模块——请使用 `node --input-type=module` 和 `import` 语法来导入它，而不是 `require()`。

### 账户管理

```bash
# List configured accounts
node {baseDir}/scripts/accounts.js --action list

# Check token status
node {baseDir}/scripts/accounts.js --action status --account <label>
```

## 文件结构

```
~/.openclaw/google-workspace-byok/
├── credentials.json          # Your GCP OAuth credentials
└── tokens/
    ├── personal.json          # Token for "personal" account
    └── work.json              # Token for "work" account
```

## 故障排除

### `Error 403: access_denied` —— “尚未完成 Google 验证流程”
您的应用处于 **测试** 模式，且该 Google 账户未列为测试用户。解决方法：在 **Google Auth Platform → Audience → Test users** 中添加该账户的邮箱。

### `Error: invalid_grant`
刷新令牌已过期或被撤销。重新运行 `node {baseDir}/scripts/auth.js --account <label>` 以重新授权。

### 令牌在 7 天后过期
处于 “测试” 发布状态的应用生成的令牌会在 7 天后过期。请将您的应用发布到 “Production” 状态以获取长期有效的令牌。对于个人 Gmail 账户（外部用户类型），您可以跳过验证流程，只需接受 “未验证的应用” 警告即可。

### `Error: redirect_uri_mismatch`
您的 credentials.json 文件中未包含 `http://localhost` 作为重定向 URI。请在 GCP 控制台的 **Authorized redirect URIs** 中添加 `http://localhost`。

### `npm install` 失败或 `mupdf` 无法安装
在某些平台上，`mupdf` 需要 C++ 构建工具链。如果安装失败，您仍然可以使用其他所有功能——只有 PDF 文本提取功能需要这个工具链。可以尝试使用 `npm install --ignore-scripts` 来跳过本地编译，然后根据需要单独安装 `mupdf`。