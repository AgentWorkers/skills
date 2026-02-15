# Microsoft 365 集成

## 描述
通过 MS Graph API 访问 Microsoft 365 服务，包括电子邮件（Outlook）、日历、OneDrive、待办事项以及联系人。

## 激活条件
当用户提及以下关键词时，该功能会被激活：outlook、email、calendar、onedrive、microsoft、office 365、o365、ms365、my meetings、my emails、schedule meeting、send email、check calendar、to do、microsoft tasks。

## 配置
首次登录后，认证信息会被缓存。设备代码流程不需要任何环境变量。

对于无界面/自动化操作，请设置以下环境变量：
- MS365_MCP_CLIENT_ID：Azure AD 应用程序客户端 ID
- MS365_MCP_CLIENT_SECRET：Azure AD 应用程序密钥
- MS365_MCP_TENANT_ID：租户 ID（个人账户使用 “consumers”）

## 可用命令

### 认证
```bash
# Login via device code (interactive)
python3 /root/clawd/skills/ms365/ms365_cli.py login

# Check authentication status
python3 /root/clawd/skills/ms365/ms365_cli.py status

# List cached accounts
python3 /root/clawd/skills/ms365/ms365_cli.py accounts

# Get current user info
python3 /root/clawd/skills/ms365/ms365_cli.py user
```

### 电子邮件（Outlook）
```bash
# List recent emails
python3 /root/clawd/skills/ms365/ms365_cli.py mail list [--top N]

# Read specific email
python3 /root/clawd/skills/ms365/ms365_cli.py mail read MESSAGE_ID

# Send email
python3 /root/clawd/skills/ms365/ms365_cli.py mail send --to "recipient@example.com" --subject "Subject" --body "Message body"
```

### 日历
```bash
# List upcoming events
python3 /root/clawd/skills/ms365/ms365_cli.py calendar list [--top N]

# Create event
python3 /root/clawd/skills/ms365/ms365_cli.py calendar create --subject "Meeting" --start "2026-01-15T10:00:00" --end "2026-01-15T11:00:00" [--body "Description"] [--timezone "America/Chicago"]
```

### OneDrive 文件
```bash
# List files in root
python3 /root/clawd/skills/ms365/ms365_cli.py files list

# List files in folder
python3 /root/clawd/skills/ms365/ms365_cli.py files list --path "Documents"
```

### 待办事项
```bash
# List task lists
python3 /root/clawd/skills/ms365/ms365_cli.py tasks lists

# Get tasks from a list
python3 /root/clawd/skills/ms365/ms365_cli.py tasks get LIST_ID

# Create task
python3 /root/clawd/skills/ms365/ms365_cli.py tasks create LIST_ID --title "Task title" [--due "2026-01-20"]
```

### 联系人
```bash
# List contacts
python3 /root/clawd/skills/ms365/ms365_cli.py contacts list [--top N]

# Search contacts
python3 /root/clawd/skills/ms365/ms365_cli.py contacts search "John"
```

## 使用示例

用户：“查看我的 Outlook 邮件”
机器人：运行 `mail list --top 10` 命令

用户：“我今天有哪些会议？”
机器人：运行 `calendar list` 命令

用户：“向 john@company.com 发送关于项目更新的邮件”
机器人：使用相应的参数运行 `mail send` 命令

用户：“显示我的 OneDrive 文件”
机器人：运行 `files list` 命令

用户：“添加一个审查预算的任务”
机器人：首先列出所有任务列表，然后在相应的列表中创建新任务

## 提示说明
在协助使用 Microsoft 365 服务时：
- 所有操作均使用 `ms365_cli.py` 脚本
- 如果命令执行失败，请先检查认证状态
- 如果用户未登录，引导用户完成设备代码登录流程
- 日历事件的日期时间格式需遵循 ISO 8601 标准
- 默认时区为 America/Chicago
- 发送邮件前请确认收件人和邮件内容
- 对于待办事项，先列出所有可用的任务列表供用户选择

## 来源说明
该功能基于 Softeria 开发的 **ms-365-mcp-server** 实现。
- **NPM 包**：[@softeria/ms-365-mcp-server](https://www.npmjs.com/package/@softeria/ms-365-mcp-server)
- **GitHub 仓库**：https://github.com/Softeria/ms-365-mcp-server
- **许可证**：MIT 许可证