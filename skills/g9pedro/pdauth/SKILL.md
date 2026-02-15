---
name: pdauth
description: 通过 Pipedream 为 AI 代理实现动态 OAuth 功能：生成超过 2500 个 API 的 OAuth 链接，允许用户进行授权，之后再代表用户调用 MCP 工具。
homepage: https://github.com/Versatly/pdauth
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["pdauth"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "pdauth",
              "bins": ["pdauth"],
              "label": "Install pdauth (node)",
            },
          ],
      },
  }
---

# pdauth — 为 AI 代理提供动态 OAuth 访问功能

使用 `pdauth`，您可以通过 OAuth 访问 2500 多个 API。具体流程如下：

1. 代理需要访问某个应用程序（如 Spotify、Slack、Notion 等）。
2. 使用 `pdauth connect <应用程序>` 生成一个 OAuth 链接。
3. 将链接分享给用户，用户点击链接后进行授权。
4. 代理随后可以通过 `pdauth call <应用程序.工具名>` 来调用相应的工具。

## 快速参考

```bash
# Configure (one-time setup)
pdauth config

# Search for apps
pdauth apps --search spotify

# Generate OAuth link
pdauth connect spotify --user USER_ID

# Check what's connected
pdauth status --user USER_ID

# List available tools
pdauth tools spotify --user USER_ID

# Call a tool
pdauth call spotify.get_my_playlists --user USER_ID
pdauth call slack.send_message channel=general text="Hello!"
```

## OAuth 访问流程（如何请求访问权限）

当您需要访问某个尚未被用户授权的应用程序时，操作步骤如下：

```
1. Run: pdauth connect <app> --user <user_id>
2. Get the OAuth link from output
3. Send link to user: "To do this, I need access to <App>. Click here to authorize: <link>"
4. User clicks, authorizes via Pipedream
5. Confirm with: pdauth status --user <user_id>
6. Now you can call tools!
```

### 用户 ID 策略

为每个用户使用统一的标识符：
- Telegram：`telegram:5439689035`
- 电子邮件：`pedro@example.com`
- 自定义标识符：`pedro-mainframe`

相同的用户 ID 可确保用户在多个会话中能够保持连接的账户状态。

## 调用工具

```bash
# Format: pdauth call <app>.<tool_name> [key=value ...]

# Simple args
pdauth call slack.send_message channel=general text="Hello"

# JSON args for complex data
pdauth call notion.create_page --args '{"title": "My Page", "content": "..."}'

# Get JSON output for parsing
pdauth call spotify.get_my_playlists --json
```

## 检查状态

```bash
# See what user has connected
pdauth status --user pedro

# See all users
pdauth status --all

# JSON for scripting
pdauth status --user pedro --json
```

## 常用应用程序

所有应用程序的列表请访问：https://mcp.pipedream.com

| 应用程序 | Slug | 可用工具示例 |
|-----|------|---------------|
| Slack | `slack` | send_message, list_channels |
| Spotify | `spotify` | get_my_playlists, add_to_playlist |
| Notion | `notion` | create_page, query_database |
| Google Sheets | `google_sheets` | get_values, update_values |
| Gmail | `gmail` | send_email, list_messages |
| GitHub | `github` | create_issue, list_repos |
| Linear | `linear` | create_issue, list_issues |
| Airtable | `airtable` | list_records, create_record |

## 错误处理

- **“应用程序未连接”**：使用 `pdauth connect` 生成新的链接，并请求用户进行授权。
- **“工具未找到”**：使用 `pdauth tools <应用程序>` 列出可用的工具。
- **“凭证无效”**：运行 `pdauth config` 以设置 Pipedream 的登录凭证。

## 提示：

1. 在尝试调用工具之前，请务必先检查连接状态。
2. 使用统一的用户 ID，以确保连接在多个会话中保持有效。
3. 使用 JSON 格式（`--json`）输出结果，便于程序解析。
4. OAuth 链接的有效期为 4 小时，需要时请重新生成链接。

## 示例工作流程

```
User: "Add 'Bohemian Rhapsody' to my Spotify playlist"

Agent:
1. pdauth status --user telegram:5439689035 --json
   → No Spotify connection

2. pdauth connect spotify --user telegram:5439689035
   → Gets OAuth link

3. Send to user: "I need Spotify access. Click here: <link>"

4. User authorizes

5. pdauth status --user telegram:5439689035
   → Spotify ✓ connected

6. pdauth call spotify.search_tracks query="Bohemian Rhapsody" --json
   → Get track ID

7. pdauth call spotify.add_to_playlist playlist_id=... track_id=...
   → Done!

8. Reply: "Added Bohemian Rhapsody to your playlist! 🎵"
```