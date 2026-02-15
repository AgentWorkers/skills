---
name: unipile-linkedin
description: 通过 Unipile API 与 LinkedIn 交互：发送消息、查看个人资料、管理联系人、创建帖子以及对内容进行互动。当用户需要向 LinkedIn 上的某人发送消息、查看 LinkedIn 消息、查看个人资料、发送联系人请求、创建 LinkedIn 帖子或与 LinkedIn 内容进行互动时，可以使用此功能。
---

# 通过 Unipile API 访问 LinkedIn

您可以使用 CLI 脚本通过 Unipile API 访问 LinkedIn。

## 设置

需要在 `~/.openclaw/workspace/TOOLS.md` 或 shell 中设置以下环境变量：
- `UNIPILE_DSN` - 您的 Unipile API 端点（例如：`https://api1.unipile.com:13111`）
- `UNIPILE_ACCESS_TOKEN` - 您的 Unipile 访问令牌

您可以从 [dashboard.unipile.com](https://dashboard.unipile.com) 获取凭据。

## 使用方法

通过 CLI 脚本运行相应的命令：

```bash
./scripts/linkedin.mjs <command> [options]
```

## 命令

### 账户管理
```bash
./scripts/linkedin.mjs accounts                    # List connected accounts
./scripts/linkedin.mjs account <account_id>        # Get account details
```

### 消息传递
```bash
./scripts/linkedin.mjs chats [--account_id=X] [--limit=N] [--unread]   # List chats
./scripts/linkedin.mjs chat <chat_id>                                   # Get chat details
./scripts/linkedin.mjs messages <chat_id> [--limit=N]                   # List messages in chat
./scripts/linkedin.mjs send <chat_id> "<text>"                          # Send message
./scripts/linkedin.mjs start-chat <account_id> "<text>" --to=<user_id>[,<user_id>] [--inmail]  # Start new chat
```

### 个人资料
```bash
./scripts/linkedin.mjs profile <account_id> <identifier> [--sections=experience,education,skills] [--notify]
./scripts/linkedin.mjs my-profile <account_id>                          # Your own profile
./scripts/linkedin.mjs company <account_id> <identifier>                # Company profile
./scripts/linkedin.mjs relations <account_id> [--limit=N]               # Your connections
```

### 邀请
```bash
./scripts/linkedin.mjs invite <account_id> <provider_id> ["message"]    # Send connection request
./scripts/linkedin.mjs invitations <account_id> [--limit=N]             # List pending invites
./scripts/linkedin.mjs cancel-invite <account_id> <invitation_id>       # Cancel invitation
```

### 帖子
```bash
./scripts/linkedin.mjs posts <account_id> <identifier> [--company] [--limit=N]  # List posts
./scripts/linkedin.mjs post <account_id> <post_id>                              # Get post
./scripts/linkedin.mjs create-post <account_id> "<text>"                        # Create post
./scripts/linkedin.mjs comments <account_id> <post_id> [--limit=N]              # List comments
./scripts/linkedin.mjs comment <account_id> <post_id> "<text>"                  # Add comment
./scripts/linkedin.mjs react <account_id> <post_id> [--type=like|celebrate|support|love|insightful|funny]
```

### 参与者
```bash
./scripts/linkedin.mjs attendees [--account_id=X] [--limit=N]           # List chat contacts
```

## 示例

```bash
# List all chats, only unread
./scripts/linkedin.mjs chats --unread

# Send a message
./scripts/linkedin.mjs send "abc123" "Thanks for connecting!"

# View someone's profile with experience section
./scripts/linkedin.mjs profile "myaccount" "john-doe-123" --sections=experience,about

# Send connection request with note
./scripts/linkedin.mjs invite "myaccount" "jane-smith-456" "Hi Jane, let's connect!"

# Create a LinkedIn post
./scripts/linkedin.mjs create-post "myaccount" "Excited to announce our new product launch! 🚀"

# React to a post
./scripts/linkedin.mjs react "myaccount" "post789" --type=celebrate
```

## 注意事项

- `identifier` 可以是 LinkedIn 用户 ID 或个人资料 URL 的缩写形式
- `account_id` 是您连接的 LinkedIn 账户 ID（可通过 `accounts` 命令获取）
- 在向非联系人发送消息时，请使用 `--inmail` 标志（需要 LinkedIn Premium 订阅）