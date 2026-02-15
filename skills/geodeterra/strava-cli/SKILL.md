---
name: strava-cli
description: 通过 `strava-client-cli` Python 工具与 Strava 进行交互。该工具可用于查看活动记录、运动员资料、统计数据以及导出数据。文档涵盖了设置流程（创建 Strava 账户、配置 API 应用程序以及启用 OAuth 认证）以及所有可用的 CLI 命令。
---

# Strava CLI

## 安装

```bash
uvx --from strava-client-cli strava --help
# Or install persistently:
uv tool install strava-client-cli
```

## 设置

### 1. 创建 Strava 账户（如需要）

请访问 https://www.strava.com/register 进行注册。只需提供姓名、电子邮件和密码即可。

### 2. 创建 Strava API 应用程序

1. 访问 https://www.strava.com/settings/api
2. 填写以下信息：
   - **应用程序名称**：任意描述性的名称
   - **类别**：选择最合适的选项（例如“其他”）
   - **网站**：任意网址（例如您的 GitHub 仓库）
   - **授权回调域名**：`localhost`
   - **描述**：简要说明该应用程序的用途
3. 勾选“同意 API 协议”选项
4. 点击“创建”
5. 记下您的 **客户端 ID** 和 **客户端密钥**

> **重要提示**：新的 Strava API 应用程序仅允许连接 **1 名运动员**。如需连接其他运动员，请在“设置” → “我的应用程序” → “撤销访问权限”中撤销当前运动员的授权。

### 3. 进行身份验证

```bash
strava auth
```

按照提示输入客户端 ID 和客户端密钥。在浏览器中打开显示的 URL，完成身份验证后，从重定向 URL（`http://localhost/?code=XXXXX`）中复制 `code` 参数，并将其粘贴回相应的输入框中。

令牌会自动更新（每 6 小时更新一次）。配置文件位于：`~/.config/strava-cli/config.json`；令牌文件位于：`~/.config/strava-cli/tokens.json`。

#### 手动更换令牌（无浏览器环境/自动化操作）

如果无法使用浏览器，可以手动完成 OAuth 流程：

1. 构建授权 URL：
   ```
   https://www.strava.com/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all,profile:read_all
   ```
2. 在任意浏览器中打开该 URL，完成身份验证
3. 获取重定向 URL 中的 `code` 参数
4. 使用该 `code` 参数进行令牌交换：
   ```bash
   curl -s -X POST https://www.strava.com/oauth/token \
     -d client_id=CLIENT_ID \
     -d client_secret=CLIENT_SECRET \
     -d code=CODE \
     -d grant_type=authorization_code
   ```
5. 将交换后的令牌保存到 `~/.config/strava-cli/tokens.json` 文件中：
   ```json
   {
     "access_token": "...",
     "refresh_token": "...",
     "expires_at": 1234567890,
     "token_type": "Bearer"
   }
   ```

## 命令

```bash
strava profile                              # Athlete profile
strava stats                                # Run/ride/swim stats summary
strava activities --limit 10                # Recent activities
strava activities --type Run --after 2024-01-01  # Filter by type/date
strava activity 12345678                    # Detailed activity view
strava export --output ./data --format json # Bulk export
```

## 项目来源

https://github.com/geodeterra/strava-cli