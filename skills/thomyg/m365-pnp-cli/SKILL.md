---
name: m365-pnp-cli
description: Microsoft 365 命令行界面（CLI）：用于管理 Microsoft 365 租户、SharePoint Online、Teams、OneDrive 等服务。这是一个官方的 PnP（Patterns and Practices）命令行工具。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["m365"],
            "node": ">=20.0.0",
            "npmPackages": ["@pnp/cli-microsoft365"]
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@pnp/cli-microsoft365",
              "label": "Install m365 CLI (npm)",
              "description": "Install the CLI for Microsoft 365 globally: npm install -g @pnp/cli-microsoft365"
            }
          ],
        "homepage": "https://pnp.github.io/cli-microsoft365",
        "repository": "https://github.com/pnp/cli-microsoft365",
        "author": "Microsoft PnP (Patterns and Practices)",
        "keywords": ["microsoft365", "m365", "sharepoint", "teams", "onenote", "outlook", "cli", "microsoft", "pnp"],
        "npmPackage": "@pnp/cli-microsoft365"
      }
  }
---
# m365-pnp-cli 技能

此技能提供了对 **Microsoft 365 命令行界面 (CLI)** 的访问权限——这是用于管理 Microsoft 365 的官方 PnP (Patterns and Practices) 工具。

## ⚠️ 对代理人员的重要提示

**如有疑问，请务必先执行 `m365 --help` 命令，以查看所有可用功能！**

```bash
# Always call help when unsure!
m365 --help

# For specific commands:
m365 login --help
m365 spo --help
m365 teams --help
```

## 安装

必须安装该 CLI：
```bash
npm install -g @pnp/cli-microsoft365
```

或者使用 npx（沙箱环境）进行安装：
```bash
npx @pnp/cli-microsoft365 --help
```

## 源代码与验证信息

- **NPM 包**：https://www.npmjs.com/package/@pnp/cli-microsoft365
- **GitHub 仓库**：https://github.com/pnp/cli-microsoft365
- **文档**：https://pnp.github.io/cli-microsoft365
- **作者**：Microsoft PnP (Patterns and Practices 社区

## CLI 的功能

### 支持的工作负载
- Microsoft Teams
- SharePoint Online
- OneDrive
- Outlook
- Microsoft To Do
- Microsoft Planner
- Power Automate
- Power Apps
- Microsoft Entra ID
- Microsoft Purview
- Bookings
- 以及更多……

### 认证方式
- 设备代码（默认方式）
- 用户名/密码
- 客户端证书
- 客户端密钥
- Azure 管理身份
- 联合身份

## 命令概览

### 登录/登出
```bash
m365 login                    # Device Code Login
m365 logout                  # Logout
m365 status                  # Check login status
```

### SharePoint Online
```bash
m365 spo site list           # List all sites
m365 spo site get --url <url>  # Get site details
m365 spo list list --webUrl <url>  # Lists in a site
m365 spo file list           # List files
m365 spo folder add          # Create folder
```

### Teams
```bash
m365 teams channel list       # List channels
m365 teams channel get       # Get channel details
m365 teams user list         # List team members
m365 teams chat list         # List chats
m365 teams meeting list      # List meetings
```

### OneDrive
```bash
m365 onedrive drive list    # OneDrive Drives
m365 onedrive file list     # List files
m365 onedrive file get      # Get file content
```

### Outlook
```bash
m365 outlook mail list       # List emails
m365 outlook calendar list   # List calendar events
```

### Microsoft Planner
```bash
m365 planner task list       # Planner Tasks
m365 planner plan get        # Get plan details
```

### Azure AD / Entra ID
```bash
m365 entra user list         # List users
m365 entra group list        # List groups
m365 entra app list          # List apps
```

## 作为辅助工具的使用 - 重要提示

### ⚡ 第一步：务必先执行 `help` 命令！

```bash
# When in doubt - call help first!
m365 --help

# For specific commands:
m365 spo --help
m365 teams --help
m365 login --help
```

### 基本用法
```bash
# Login (Device Code Flow)
m365 login

# Check status
m365 status

# SharePoint: List sites
m365 spo site list

# SharePoint: Get specific site
m365 spo site get --url "https://contoso.sharepoint.com/sites/test"

# Teams: List channels
m365 teams channel list --teamId <team-id>

# OneDrive: Files
m365 onedrive file list

# Outlook: Emails
m365 outlook mail list --folder Inbox

# Planner: Tasks
m365 planner task list
```

## 输出格式选项
```bash
# As JSON (default)
m365 spo site list

# As text
m365 spo site list --output text

# Filter with JMESPath
m365 spo site list --query "[?Template==\`GROUP#0\`].{Title:Title, Url:Url}"
```

## 认证方式

该 CLI 默认使用 **设备代码认证** 方式：

```bash
m365 login
# → You'll receive a code on another device
# → Use that code to authenticate with Microsoft
```

对于自动化脚本，还可以使用以下认证方式：
- **客户端证书**（推荐在生产环境中使用）
- **客户端密钥**（安全性较低）
- **用户名/密码**（仅用于测试）

## 重要提示

- **如有疑问，请务必执行 `m365 --help` 命令！**
- **大多数命令都需要登录**
- **JSON 格式的输出最易于解析**
- **使用 JMESPath 可以实现高效的数据过滤**
- 该 CLI 需要 **Node.js 20 及以上版本**