---
name: cdp-browser
description: CDP浏览器控制端，地址为localhost:9222。当您需要检查标签页、截图、浏览页面、滚动内容、将数据发布到X平台，或在持续的浏览器会话中运行JavaScript代码（例如，在已登录X平台或使用Gmail的情况下）时，请使用该控制端。
---
# cdp-browser

这是一个用于 Chrome/Chromium 的命令行工具（CLI），支持在本地地址 `localhost:9222` 上进行操作。该工具支持查看标签页、截图、导航、滚动页面内容、将内容发布到 Telegram，以及在持久化的浏览器会话中执行 JavaScript 代码。

**仓库地址：** https://github.com/gostlightai/cdp-browser

**先决条件：** 需要运行配置了 `--remote-debugging-port=9222` 的 Chromium；或者使用启用了远程调试功能的本地 Chrome 浏览器。同时，还需要 Docker Compose 环境或具备远程调试功能的本地 Chrome 浏览器。

## 命令

从 `bin/` 目录下的脚本中运行以下命令：

| 命令 | 功能描述 |
|---------|-------------|
| `status` | 列出所有标签页的信息（以 JSON 格式返回） |
| `tabs` | 与 `status` 功能相同 |
| `new <url>` | 打开一个新的标签页 |
| `goto <tabId> <url>` | 导航到指定标签页的指定 URL |
| `snapshot <tabId>` | 生成该标签页的全屏截图（PNG 格式） |
| `close-popup <tabId>` | 关闭弹出窗口或模态框 |
| `scroll <tabId> <px\|sel> [down\|up]` | 按指定像素数或选择器内容滚动页面 |
| `query <tabId> getUrl` | 获取当前标签页的 URL |
| `query <tabId> getText [selector]` | 获取指定元素的内容（文本或 HTML） |
| `query <tabId> getHtml [selector]` | 获取指定元素的 HTML 内容（包括标签页的 HTML 结构） |
| `tweet-draft <tabId> "text"` | 仅填充 Twitter 的撰写框，不会实际发送推文 |
| `tweet-post <tabId> --confirm "text"` | 发送推文（需要使用 `--confirm` 作为第二个参数） |
| `tweet <tabId> "text"` | 是 `tweet-draft` 的别名，仅用于填充 Twitter 撰写框 |

## 推文发送流程

- **tweet-draft**（默认模式）：仅填充 Twitter 的撰写框，用户需要在浏览器中手动审核并发送推文。
- **tweet-post**：必须使用 `--confirm` 作为第二个参数。该模式适用于用户明确表示同意发送推文的情况（例如点击“发送”按钮或通过 Telegram 确认）。
- **可选的 Telegram 确认机制**：如果在配置中启用了 `tweet-confirmButton`，代理程序可以执行 `tweet-draft --save-pending` 来保存待发送的推文内容，然后发送一条带有“Confirm Post”按钮的消息。用户点击“Confirm Post”按钮后，代理程序会执行 `tweet-post --confirm` 来发送推文。

### 配置（启用 Telegram 确认功能所需）

Telegram 的“Confirm Post”按钮 **仅在配置文件存在时生效**。请参考以下示例配置，并将其保存到工作目录中：

```bash
# From the skill dir (e.g. ~/.openclaw/workspace/skills/cdp-browser):
cp .cdp-browser.json.example ~/.openclaw/workspace/.cdp-browser.json
```

**配置文件位置：** `~/.openclaw/workspace/.cdp-browser.json`（或 `$OPENCLAW_WORKSPACE/.cdp-browser.json`）

| 配置项 | 默认值 | 说明 |
|---------|---------|-------------|
| `tweet-confirmButton` | `false` | 如果设置为 `true`，代理程序会在 Telegram 中发送带有“Confirm Post”按钮的推文草稿。用户需要点击该按钮或输入“发送”来确认推文。 |

**注意：** 如果未配置此选项，代理程序将使用普通的 `tweet-draft` 模式（不显示确认按钮），用户必须通过文本输入来确认推文。

### 使用 Telegram 确认按钮的代理程序操作流程

当 `tweet-confirmButton` 为 `true`（配置文件存在）且当前处于 Telegram 会话中时：

1. **生成推文草稿**：从 `bin/` 目录下运行 `tweet-draft --save-pending <tabId> "text"` 命令。这会生成一个待发送的推文草稿文件（保存在 `~/.openclaw/workspace/.cdp-browser/pending-tweet.json`）。
2. **通过按钮发送推文**：可以从 `bin/` 目录下运行以下命令：
   ```bash
   ./scripts/send-tweet-confirm.sh <chat_id> "<tweet_text>"
   ```
   或者直接使用 `openclaw message send` 命令，并传入参数 `--buttons '[[{"text":"Confirm Post","callback_data":"cdp:tweet:confirm"}]]'`。其中 `<chat_id>` 应设置为当前会话的聊天 ID。
3. **用户确认**：当用户点击“Confirm Post”按钮或输入“发送”后，OpenClaw 会接收到 `callback_data: cdp:tweet:confirm`。此时：
   - 从 `~/.openclaw/workspace/.cdp-browser/pending-tweet.json` 中读取推文内容（`text`）和标签页 ID（`tabId`）。
   - 运行 `tweet-post <tabId> --confirm "<text>"` 命令来发送推文。
   - （可选）使用按钮来编辑或删除已发送的推文。
   - 删除临时生成的推文草稿文件（`pending-tweet.json`）。

## 相关脚本

- **cdp.js**：仅用于调用 CDP 的 HTTP API（`/json`, `/json/list`, `/json/new`），不涉及 shell 操作。
- **pw.js**：使用 Playwright 库与 Chrome 浏览器建立连接，执行截图、导航、滚动、查询和发送推文等操作。其中包含用于触发这些操作的脚本，例如 `SideNav_NewTweet_Button` 和 `Post`；`tweetButton` 用于直接发送推文，`tweetButtonInline` 用于显示确认按钮。

## 安全性

有关安全性的详细信息，请参阅 [SECURITY.md] 文件。