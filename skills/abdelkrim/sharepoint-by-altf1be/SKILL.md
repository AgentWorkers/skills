---
name: sharepoint-by-altf1be
description: "通过 Microsoft Graph API 保护 SharePoint 文件操作和 Office 文档的安全性：支持证书认证（certificate auth），能够读取/写入 Word 文件（使用 mammoth 库）、Excel 文件（使用 exceljs 库）、PowerPoint 文件（使用 jszip 库）以及 PDF 文件（使用 pdf-parse 库）。"
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint
metadata:
  {"openclaw": {"emoji": "📁", "requires": {"env": ["SP_TENANT_ID", "SP_CLIENT_ID", "SP_CERT_PATH", "SP_SITE_ID"]}, "primaryEnv": "SP_TENANT_ID"}}
---
# 使用 @altf1be 提供的 SharePoint 工具

通过基于证书的身份验证，使用 Microsoft Graph API 与 SharePoint 文档库进行交互。

## 设置

1. 创建一个具有 `Sites.Selected` 权限和证书认证功能的 Entra 应用程序。
2. 通过 Microsoft Graph PowerShell 授予站点级别的写入权限。
3. 设置环境变量（或在 `{baseDir}` 目录下创建 `.env` 文件）：

```
SP_TENANT_ID=your-azure-tenant-id
SP_CLIENT_ID=your-app-client-id
SP_CERT_PATH=/path/to/certificate.pem
SP_SITE_ID=your-sharepoint-site-id
SP_DRIVE_ID=optional-specific-drive-id
```

4. 安装依赖项：`cd {baseDir} && npm install`

## 命令

```bash
# Show site and drive info
node {baseDir}/scripts/sharepoint.mjs info

# List files in library root
node {baseDir}/scripts/sharepoint.mjs list

# List files in a subfolder
node {baseDir}/scripts/sharepoint.mjs list --path "Meeting Notes/2026"

# Read file content (extracts text from Office formats)
node {baseDir}/scripts/sharepoint.mjs read --path "Report.docx"

# Upload a file
node {baseDir}/scripts/sharepoint.mjs upload --local ./report.docx --remote "Reports/Q1-2026.docx"

# Search for files
node {baseDir}/scripts/sharepoint.mjs search --query "quarterly review"

# Create folder
node {baseDir}/scripts/sharepoint.mjs mkdir --path "Meeting Notes/2026"

# Delete (requires --confirm flag)
node {baseDir}/scripts/sharepoint.mjs delete --path "Drafts/old-file.txt" --confirm
```

## 支持的 Office 格式

`read` 命令可以从以下格式的文件中提取文本内容：
- `.docx` → 使用 `mammoth` 提取全部文本内容
- `.xlsx` → 使用 `exceljs` 提取工作表名称和单元格数据
- `.pptx` → 使用 `jszip` 提取幻灯片文本
- `.pdf` → 使用 `pdf-parse` 提取文本内容
- `.txt` / `.md` → 提取原始内容

输出为适合 AI 处理的纯文本（可用于摘要生成、重新格式化或提取待办事项）。

## 依赖项

- `@azure/identity` — 基于证书的 Azure AD 认证
- `@microsoft/microsoft-graph-client` — Microsoft Graph API 客户端
- `mammoth` — 用于提取 Word 文档内容的工具
- `exceljs` — 用于解析 Excel 电子表格的工具
- `jszip` — 用于提取 PowerPoint XML 内容的工具
- `pdf-parse` — 用于提取 PDF 文本内容的工具
- `commander` — 命令行接口（CLI）框架
- `dotenv` — 用于加载环境变量的工具

## 安全性

- 仅支持基于证书的身份验证（无需客户端密钥或密码）
- 仅允许访问具有 `Sites.Selected` 权限的 SharePoint 站点
- 防止路径遍历（拒绝访问 `../` 路径）
- 删除文件时需要使用 `--confirm` 标志
- 不会将任何令牌或密钥输出到标准输出（stdout）
- 文件大小有限制（默认最大为 50MB）

## 完整设置指南

有关从零开始设置（包括创建 Entra 应用程序、配置证书以及使用 Key Vault）的详细信息，请参阅 [GitHub 仓库](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint) 的 README 文件。

## 作者

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be)，布鲁塞尔 🇧🇪
X: [@altf1be](https://x.com/altf1be)