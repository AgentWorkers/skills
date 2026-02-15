---
name: gram
description: Instagram CLI：通过Cookie查看动态、帖子、个人资料以及用户互动情况。
homepage: https://github.com/arein/gram
metadata: {"clawdbot":{"emoji":"📸","requires":{"bins":["gram"]},"install":[{"id":"npm","kind":"node","package":"@cyberdrk/gram","bins":["gram"],"label":"Install gram (npm)"}]}}
---

# gram 📸

这是一个使用 REST/GraphQL API 以及基于 Cookie 的认证机制的 Instagram 命令行工具（CLI）。

## 安装

```bash
# npm/pnpm/bun
npm install -g @cyberdrk/gram

# One-shot (no install)
bunx @cyberdrk/gram whoami
```

## 认证

`gram` 通过 Instagram 的 Web 会话中的 Cookie 来实现认证。

你可以使用 `--session-id`、`--csrf-token` 和 `--ds-user-id` 直接传递 Cookie，或者使用 `--cookie-source` 来指定 Cookie 的来源（例如浏览器）。运行 `gram check` 命令可以查看当前使用的 Cookie 来源。对于 Arc/Brave 浏览器，可以使用 `--chrome-profile-dir <path>` 参数来指定 Chrome 配置文件的路径。

## 命令

### 账户与认证相关操作

```bash
gram whoami                    # Show logged-in account
gram check                     # Show credential sources
gram query-ids --refresh       # Refresh GraphQL query ID cache
```

### 阅读帖子

```bash
gram post <shortcode-or-url>   # View a post
gram <shortcode-or-url>        # Shorthand for post
gram comments <shortcode> -n 20 # View comments on a post
gram likers <shortcode>        # View users who liked a post
```

### 查看动态流（Feeds）

```bash
gram feed -n 20                # Home feed
gram explore -n 20             # Explore/discover feed
```

### 查看用户资料

```bash
gram user <username>           # View user profile
gram user @instagram --json    # JSON output
gram posts <username> -n 20    # User's posts
gram following [username]      # Users someone follows (defaults to you)
gram followers [username]      # Someone's followers (defaults to you)
```

### 搜索

```bash
gram search "query"            # Search users, hashtags, places
gram search "coffee" --type users
gram search "nyc" --type places
gram search "#photography" --type hashtags
```

### 互动操作（Engagement Actions）

```bash
gram like <shortcode>          # Like a post
gram unlike <shortcode>        # Unlike a post
gram save <shortcode>          # Save/bookmark a post
gram unsave <shortcode>        # Unsave a post
gram comment <shortcode> "nice!" # Comment on a post
gram follow <username>         # Follow a user
gram unfollow <username>       # Unfollow a user
```

## 输出选项

```bash
--json          # JSON output
--json-full     # JSON with raw API response in _raw field
--plain         # No emoji, no color (script-friendly)
--no-emoji      # Disable emoji
--no-color      # Disable ANSI colors (or set NO_COLOR=1)
```

## 全局配置选项

```bash
--session-id <token>           # Instagram sessionid cookie
--csrf-token <token>           # Instagram csrftoken cookie
--ds-user-id <id>              # Instagram ds_user_id cookie
--cookie-source <source>       # Cookie source for browser cookies (repeatable)
--chrome-profile <name>        # Chrome profile name
--chrome-profile-dir <path>    # Chrome/Chromium profile dir or cookie DB path
--firefox-profile <name>       # Firefox profile
--timeout <ms>                 # Request timeout
--cookie-timeout <ms>          # Cookie extraction timeout
```

## 配置文件

配置文件位于 `~/.config/gram/config.json5`（全局配置）或 `./.gramrc.json5`（项目级配置）：

```json5
{
  cookieSource: ["safari", "chrome"],
  chromeProfile: "Profile 1",
  timeoutMs: 60000
}
```

环境变量：`GRAM_TIMEOUT_MS`、`GRAM COOKIE_TIMEOUT_MS`

## 故障排除

### 查询 ID 过期（导致 404 错误）
```bash
gram query-ids --refresh
```

### 提取 Cookie 失败
- 确保浏览器已登录 Instagram
- 尝试使用不同的 `--cookie-source` 参数
- 对于 Arc/Brave 浏览器，请使用 `--chrome-profile-dir` 参数
- 可以手动提供 Cookie：`--session-id`、`--csrf-token`、`--ds-user-id`

### 用户代理不匹配错误
- 该 CLI 默认使用桌面浏览器的用户代理
- 如果你的会话是在移动设备上创建的，可能会导致问题
- 请通过桌面浏览器重新登录以创建新的会话

---

**简而言之**：通过这个 CLI，你可以查看 Instagram 的动态流、用户资料、进行搜索以及与其他用户互动。📸