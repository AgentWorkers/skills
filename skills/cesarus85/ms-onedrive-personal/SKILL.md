---
name: ms-onedrive-personal-graph
description: 通过 Microsoft Graph 和 OAuth 设备代码流访问 OneDrive 个人账户（消费者 Microsoft 账户）。支持执行 `ls`、`mkdir`、`upload`、`download` 和 `info` 操作；默认设置为“安全模式”（不允许删除文件）。
metadata:
  openclaw:
    requires:
      bins: ["bash","curl","jq","python3"]
---

# 通过 Microsoft Graph 访问个人 OneDrive（消费者账户）

这是一个简单且默认设置为安全的脚本，用于使用 **Microsoft Graph API** 访问 **个人 OneDrive**（消费者 Microsoft 账户）。

该脚本采用 **OAuth 2.0 设备代码流**（无需在服务器端进行浏览器自动化操作），并将访问令牌存储在本地。

## 功能
- 通过设备代码进行身份验证
- 列出文件夹（`ls`）
- 创建文件夹（`mkdir`）
- 上传文件（适用于小型/中型文件）
- 下载文件
- 查看文件元数据（`info`）

## 安全性/限制
- **不允许执行删除操作**（设计上的限制）
- 不支持批量移动/重命名文件（这些功能可后续添加）

## 设置（首次使用）
### 1) 创建 Microsoft Entra 应用注册
您需要一个 **客户端 ID**。

建议按照以下步骤创建应用注册：
1. 访问 Entra 门户：https://entra.microsoft.com/
2. 选择 **应用注册** → **新建注册**
3. 支持的账户类型：**任何组织目录中的账户以及个人 Microsoft 账户**
4. 完成注册
5. 在应用设置中，启用 **允许公共客户端流**（**Authentication** → **Allow public client flows**）
   - （部分租户可能还需要设置 `isFallbackPublicClient=true`——脚本会提示您是否需要此设置。）

> 注意：部分用户可能会遇到 Azure 门户登录错误，例如“由于账户不活跃而被封禁”。虽然这对 OneDrive 本身没有影响，但可能会导致无法创建应用注册。在这种情况下，请在您控制的另一个 Entra 租户下创建应用，确保该租户允许个人 Microsoft 账户的使用。

### 2) 运行设置脚本
在运行 OpenClaw 的机器上执行以下命令：
```bash
cd /root/clawd/skills/ms-onedrive-personal-graph
./scripts/onedrive-setup.sh
```

脚本将：
- 请求客户端 ID
- 显示设备登录 URL 及验证码
- 等待您批准登录
- 将访问令牌保存到 `~/.onedrive-mcp/credentials.json` 文件中
- 测试访问 `https://graph.microsoft.com/v1.0/me/drive` 的功能

## 使用方法
所有命令都需要使用 `~/.onedrive-mcp/credentials.json` 文件中的令牌。

```bash
./scripts/onedrive-cli.sh ls /
./scripts/onedrive-cli.sh mkdir "/Invoices"
./scripts/onedrive-cli.sh upload ./invoice.pdf "/Invoices/invoice.pdf"
./scripts/onedrive-cli.sh download "/Invoices/invoice.pdf" ./invoice.pdf
./scripts/onedrive-cli.sh info "/Invoices/invoice.pdf"
```

## 令牌刷新
如果遇到 401/无效令牌的错误，可以使用以下命令刷新令牌：
```bash
./scripts/onedrive-token.sh refresh
```

## 故障排除
### AADSTS5000225：账户因不活跃被封禁
当您的登录信息关联到被 Microsoft 标记为不活跃的 Entra 租户时，可能会出现此错误。
- 使用消费者账户的登录页面（https://account.microsoft.com/）进行登录（通常可以解决问题）
- 在您控制的另一个租户下创建应用注册（或使用其他管理员身份进行操作）

### AADSTS70002：客户端必须被标记为“移动设备”
请确保在应用设置中启用 **允许公共客户端流**（**Allow public client flows**），或设置 `isFallbackPublicClient=true`。

### 上传限制
该脚本目前仅支持使用 **简单上传** 方法（`...:/content`）。对于大型文件，我们未来需要添加上传会话的支持。