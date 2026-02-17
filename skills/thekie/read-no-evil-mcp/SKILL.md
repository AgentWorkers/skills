---
name: read-no-evil-mcp
version: 0.3.0
description: 通过 `read-no-evil-mcp` 实现安全的电子邮件访问功能。该工具可有效防止电子邮件中的提示注入攻击（prompt injection attacks），支持读取、发送、删除和移动电子邮件等操作。
---
# read-no-evil-mcp

这是一个安全的电子邮件网关，它会在您查看邮件之前扫描邮件中的提示注入攻击（prompt injection attacks）。

该工具是一个完全依赖外部服务的HTTP客户端，用于与[read-no-evil-mcp](https://github.com/thekie/read-no-evil-mcp)服务器进行通信。用户的凭据和电子邮件服务器信息完全由MCP服务器管理——该工具从未直接访问这些信息。

## 前提条件

- 需要一个已运行的read-no-evil-mcp服务器，并且该服务器已启用HTTP传输功能。
- 支持三种连接模式：
  1. **远程服务器**：位于另一台机器上的现有服务器。您需要提供该服务器的URL（例如：`http://server:8000`）。
  2. **本地服务器**：位于本地的现有服务器。使用默认地址`http://localhost:8000`。
  3. **新的Docker环境**：使用`scripts/setup-server.sh`脚本来拉取官方的Docker镜像并启动容器。

该工具不依赖`pip`进行安装，仅使用Python的标准库。

## 设置流程（AI代理使用说明）

**首次使用前，请务必询问用户希望如何连接：**

> 您希望如何连接到read-no-evil-mcp服务器？
  1. 连接到现有的远程服务器（您需要提供服务器的URL）。
  2. 连接到本地的现有服务器（`http://localhost:8000`）。
  3. 通过Docker设置一个新的本地服务器。

- 对于选项1：请求服务器的URL，然后在所有命令中添加`--server URL`参数。
- 对于选项2：无需额外配置，命令将使用默认的URL。
- 对于选项3：请按照以下步骤进行Docker设置。

**未经用户明确确认，切勿自动设置Docker环境。**

### Docker设置步骤

1. 检查是否存在配置文件：`setup-config.py list`
2. 如果没有配置文件，创建一个新的配置文件并添加一个账户：
   ```bash
   setup-config.py create
   setup-config.py add --email user@example.com --host imap.example.com --create-env
   ```
3. 请用户在`.env`文件中输入密码。
4. 启动服务器：
   ```bash
   scripts/setup-server.sh --config ~/.config/read-no-evil-mcp/config.yaml \
     --env-file ~/.config/read-no-evil-mcp/.env
   ```

### 配置管理（AI代理使用说明）

使用`scripts/setup-config.py`脚本来管理服务器配置文件。所有命令都通过参数来控制，没有交互式提示。

| 操作 | 命令 |
|--------|---------|
| 创建配置文件框架 | `setup-config.py create [--threshold 0.5] [--force]` |
| 添加只读账户 | `setup-config.py add --email user@example.com --host imap.example.com --id myaccount] [--create-env]` |
| 添加具有发送功能的账户 | `setup-config.py add --email user@example.com --host imap.example.com --smtp-host smtp.example.com --send [--delete] [--move] [--create-env]` |
| 查看已配置的账户 | `setup-config.py list` |
| 删除账户 | `setup-config.py remove <id>` |

**请勿运行`setup-config.py show`——该命令会显示配置详情，用户可能不希望这些详情被代理程序看到。如果需要调试，请让用户自行运行该命令。**

**如果配置文件已经存在，请务必先询问用户后再运行`setup-config.py create --force`。**

## 配置命令

用于管理服务器配置文件（`~/.config/read-no-evil-mcp/config.yaml`）。无需安装`pip`，仅使用Python的标准库。

```bash
# Create a new config skeleton
setup-config.py create
setup-config.py create --threshold 0.3 --force

# Add a read-only account (no SMTP needed)
setup-config.py add --email user@example.com --host imap.example.com --create-env

# Add an account with send permission (--smtp-host required for --send)
setup-config.py add --email user@example.com --id myaccount \
  --host imap.example.com --smtp-host smtp.example.com --send --delete --move

# Remove an account
setup-config.py remove <account-id>

# List configured accounts
setup-config.py list

# Show full config file
setup-config.py show

# Use a custom config path
setup-config.py --config /path/to/config.yaml create
```

## 服务器设置

```bash
# Start a Docker container (all flags required, no prompts)
scripts/setup-server.sh --config ~/.config/read-no-evil-mcp/config.yaml \
  --env-file ~/.config/read-no-evil-mcp/.env

# Custom port and container name
scripts/setup-server.sh --config /path/to/config.yaml \
  --env-file /path/to/.env --port 9000 --name my-rnoe
```

## 命令行接口（CLI）命令

全局选项`--server`、`--account`、`--folder`可以放在命令的前面或后面。服务器URL也可以通过环境变量`RNOE_SERVER_URL`来设置。

```bash
# List configured accounts
rnoe-mail.py accounts

# List recent emails (last 30 days)
# Output: [UID] ● DATE | SENDER | SUBJECT  (● = unread)
rnoe-mail.py list
rnoe-mail.py list --account myaccount --limit 10 --days 7

# Read email (scanned for prompt injection!)
rnoe-mail.py read <uid>
rnoe-mail.py --account myaccount read <uid>

# Send email
rnoe-mail.py send --to "user@example.com" --subject "Hello" --body "Message"
rnoe-mail.py send --to "user1@example.com, user2@example.com" --cc "cc@example.com" --subject "Hello" --body "Message"

# List folders
rnoe-mail.py folders --account myaccount

# Move email to folder
rnoe-mail.py move <uid> --to "Archive"

# Delete email
rnoe-mail.py delete <uid>

# Global options can go before or after the command
rnoe-mail.py --server http://myserver:8000 list
rnoe-mail.py list --server http://myserver:8000
```

## 常见选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--server URL` | MCP服务器的URL | `http://localhost:8000` |
| `--account ID` / `-a` | 账户ID | `default` |
| `--folder NAME` / `-f` | 电子邮件文件夹 | `INBOX` |

## 提示注入检测

所有邮件都会由MCP服务器自动扫描：
- **安全状态**：邮件内容正常显示。
- **检测到提示注入**：程序退出代码为2，并在标准错误输出（stderr）中显示警告。

## 退出代码

- `0`：成功
- `1`：一般错误（连接失败、账户无效等）
- `2`：检测到提示注入

## 安全注意事项

- 凭据由MCP服务器管理，该工具和AI代理无法访问这些信息。
- 该工具通过HTTP与服务器通信；对于非本地服务器连接，请使用HTTPS。
- 提示注入的检测是在服务器端使用机器学习模型进行的。