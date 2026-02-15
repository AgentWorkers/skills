---
name: dropbox-integration
description: 仅读的 Dropbox 集成功能，支持浏览、搜索和下载您 Dropbox 账户中的文件。该功能包含自动刷新 OAuth 令牌、安全的凭证存储以及详细的设置指南。非常适合在 OpenClaw 中访问您的 Dropbox 文件，而无需赋予写入权限。
---

# Dropbox 集成

## 概述

此功能允许您以**只读**方式访问您的 Dropbox 账户，从而可以浏览文件夹、搜索文件并从 OpenClaw 下载内容。它使用 OAuth 2.0 进行身份验证，并自动刷新令牌，以实现无缝的长期访问。

**适用场景：**安全地访问您的 Dropbox 文件，无需担心意外修改或删除。

## 功能

### 浏览文件和文件夹
- 列出 Dropbox 中任何文件夹的内容
- 查看文件大小和修改日期
- 导航文件夹层次结构

### 搜索文件
- 对文件名进行全文搜索
- 在 Dropbox 中的任何位置查找文件
- 获取文件元数据和位置信息

### 下载文件
- 从 Dropbox 下载任何文件
- 保存到本地文件系统
- 支持批量下载

### 自动令牌管理
- 使用 OAuth 2.0 进行身份验证，并自动刷新令牌
- 无需手动重新认证
- 安全存储凭证
- 令牌在过期前 5 分钟自动刷新

## 安全性与权限

此功能的配置为**只读**访问权限，包含以下 Dropbox 权限范围：
- `files.metadata.read` - 读取文件/文件夹元数据
- `files.content.read` - 读取文件内容
- `account_info.read` - 读取账户信息

**不包括以下权限：**
- ❌ `files.content.write` - 无法上传或修改文件
- ❌ `files.metadata.write` - 无法重命名或移动文件
- ❌ `files.permanent_delete` - 无法删除文件

这确保您的 Dropbox 内容不会被意外修改。

## 先决条件

在使用此功能之前，您需要：
1. 一个 **Dropbox 账户**（免费或付费）
2. 注册一个 **Dropbox 应用**（只需 5 分钟）
3. 从您的 Dropbox 应用中获取 **应用密钥** 和 **应用秘钥**
4. 安装了包含 `dropbox` 包的 Node.js 环境（已自动安装）

**设置时间：约 10 分钟**

请参阅 [设置指南](references/setup-guide.md) 以获取详细步骤。

## 快速入门

### 1. 创建 Dropbox 应用

访问 https://www.dropbox.com/developers/apps/create 并创建一个新的应用：
- **API：** 有限制的访问权限
- **访问类型：** 全部 Dropbox（或受限访问的应用文件夹）
- **应用名称：** 例如 "OpenClaw-YourName"

### 2. 配置 OAuth

在应用设置中：
1. 添加重定向 URI：`http://localhost:3000/callback`
2. 复制您的 **应用密钥** 和 **应用秘钥**
3. 在 **权限** 标签下，启用以下权限：
   - `files.metadata.read`
   - `files.content.read`
   - `account_info.read`

### 3. 保存凭证

在技能目录下创建 `credentials.json` 文件：

```json
{
  "app_key": "your_dropbox_app_key_here",
  "app_secret": "your_dropbox_app_secret_here"
}
```

**注意：** 该文件会被 Git 忽略，不会被提交到代码仓库。

### 4. 运行 OAuth 设置

```bash
node setup-oauth.js
```

此步骤将：
1. 打开浏览器进行 Dropbox 认证
2. 启动本地服务器以捕获授权码
3. 用授权码交换访问令牌和刷新令牌
4. 将令牌安全地保存到 `token.json` 文件中

### 5. 测试连接

```bash
node test-connection.js
```

如果成功，您将看到您的 Dropbox 账户信息！

## 使用示例

### 浏览文件夹

```bash
# List root folder
node browse.js

# List specific folder
node browse.js "/Documents"
node browse.js "/Photos/2024"
```

输出：
```
📁 Listing: /Documents

📄 report.pdf (2.3 MB) - 2024-02-01
📄 presentation.pptx (5.1 MB) - 2024-01-28
📁 Projects
📁 Archive

Total: 4 items
```

### 搜索文件

```bash
node search-files.js "budget 2024"
node search-files.js "contract"
```

输出：
```
🔍 Searching for: "budget 2024"

✅ Found 3 matches:

📄 /Finance/budget-2024-q1.xlsx
   Size: 156.3 KB
   Modified: 2024-01-15T10:30:00Z

📄 /Reports/budget-2024-summary.pdf
   Size: 2.1 MB
   Modified: 2024-02-01T14:22:00Z
```

### 下载文件

```bash
# Download to local file
node download.js "/Documents/report.pdf" "./downloads/report.pdf"

# Download to current directory
node download.js "/Photos/vacation.jpg" "./vacation.jpg"
```

输出：
```
📥 Downloading: /Documents/report.pdf
✅ Saved to: ./downloads/report.pdf (2.3 MB)
```

## 与 OpenClaw 的集成

在 OpenClaw 中，您可以使用 `exec` 工具运行以下脚本：
- **浏览文件：**
```
Run: node /path/to/dropbox-integration/browse.js "/Documents"
```

- **搜索文件：**
```
Run: node /path/to/dropbox-integration/search-files.js "contract"
```

- **下载文件：**
```
Run: node /path/to/dropbox-integration/download.js "/path/in/dropbox" "./local/path"
```

或者直接使用 `dropbox-helper.js` 模块创建自定义自动化工作流程。

## 工作原理

### 认证流程

1. **初始设置：** 用户通过 OAuth 2.0 授权应用
2. **令牌存储：** 访问令牌和刷新令牌保存在 `token.json` 文件中
3. **自动刷新：** 在每次 API 调用之前，检查令牌是否需要刷新
4. **无缝访问：** 在令牌过期前 5 分钟自动刷新令牌

### 令牌生命周期
- **访问令牌：** 寿命较短（通常为 4 小时）
- **刷新令牌：** 寿命较长（除非被撤销）
- **自动刷新：** 在 `dropbox-helper.js` 中透明地执行
- **刷新缓冲时间：** 在令牌过期前 5 分钟，以防意外情况

### 文件结构

```
dropbox-integration/
├── SKILL.md                 # This file
├── dropbox-helper.js        # Auto-refresh Dropbox client
├── setup-oauth.js           # OAuth setup script
├── browse.js                # Browse folders
├── search-files.js          # Search files
├── download.js              # Download files
├── test-connection.js       # Test authentication
├── credentials.json.example # Template for credentials
├── .gitignore               # Excludes credentials.json and token.json
└── references/
    └── setup-guide.md       # Detailed setup instructions
```

## 故障排除

### “找不到 credentials.json”
使用您的 Dropbox 应用密钥和秘钥创建 `credentials.json` 文件（参见快速入门步骤 3）。

### “令牌刷新失败”
可能是您的刷新令牌已被撤销。请重新运行 `node setup-oauth.js` 以重新认证。

### “权限被拒绝” 错误
请检查您是否已在 Dropbox 应用设置中的 **权限** 标签下启用了所需的权限。

### “redirect_uri_mismatch”
确保您已在 Dropbox 应用控制台中将 `http://localhost:3000/callback` 添加到应用的重定向 URI 中。

### OAuth 设置卡住
如果本地服务器未捕获到重定向，请手动从浏览器中复制完整的 URL，并查找 `code=` 参数。

## 限制

- **只读权限：** 无法上传、修改或删除文件（按设计要求）
- **文件大小：** 每次下载的实际限制约为 150MB（Dropbox API 规定）
- **速率限制：** Dropbox API 有速率限制（个人使用通常不受影响）
- **共享文件夹：** 访问权限取决于您的 Dropbox 账户设置

## 安全最佳实践

1. **切勿提交凭证：** `credentials.json` 和 `token.json` 文件会被 Git 忽略
2. **文件权限：** 令牌以 0600 模式保存（用户仅具有读写权限）
3. **应用专用令牌：** 每个应用都有自己的令牌（可轻松撤销）
4. **权限限制：** 仅请求实际需要的权限
5. **令牌轮换：** 令牌会自动轮换

## 资源

### 参考资料

- [设置指南](references/setup-guide.md) - 带有截图的详细步骤说明
- [Dropbox API 文档](https://www.dropbox.com/developers/documentation)
- [OAuth 2.0 文档](https://www.dropbox.com/developers/reference/oauth-guide)

### Dropbox 开发者资源

- [应用控制台](https://www.dropbox.com/developers/apps) - 管理您的应用
- [API 探索器](https://www.dropbox.github.io/dropbox-api-v2-explorer/) - 测试 API 调用
- [SDK 文档](https://dropbox.github.io/dropbox-sdk-js/) - JavaScript SDK 参考

## 高级用法

### 使用辅助模块

对于自定义集成，可以直接导入辅助模块：

```javascript
const { getDropboxClient } = require('./dropbox-helper');

async function myCustomFunction() {
  const dbx = await getDropboxClient(); // Auto-refreshing client
  
  // Use any Dropbox SDK method
  const response = await dbx.filesListFolder({ path: '/Photos' });
  console.log(response.result.entries);
}
```

该辅助模块会自动处理令牌刷新，因此您无需担心令牌过期问题。

### 批量操作

可以顺序下载多个文件：

```javascript
const { getDropboxClient } = require('./dropbox-helper');
const fs = require('fs').promises;

async function downloadMultiple(files) {
  const dbx = await getDropboxClient();
  
  for (const file of files) {
    const response = await dbx.filesDownload({ path: file.dropboxPath });
    await fs.writeFile(file.localPath, response.result.fileBinary);
    console.log(`Downloaded: ${file.dropboxPath}`);
  }
}
```

## 依赖项

此功能需要 `dropbox` npm 包：

```bash
npm install dropbox
```

当您通过 ClawHub 安装此功能时，该包会自动安装。

## 许可证

MIT 许可证 - 可以免费使用、修改和分发。

## 支持

如遇问题或疑问：
- 查看 [设置指南](references/setup-guide.md) 以获取详细说明
- 查阅 [API 文档](https://www.dropbox.com/developers/documentation) 中的错误信息
- 在技能仓库中提交问题

---

**注意：** 此功能专为个人使用设计。对于有多个用户的生产环境应用，请考虑实现适当的 OAuth 流程，并处理并发用户的权限管理和错误处理。