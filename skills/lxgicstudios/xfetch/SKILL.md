---
name: xfetch
description: 这是一个快速的 X/Twitter 命令行界面（CLI） scraper 工具。当你需要获取推文、用户资料、搜索结果、时间线、关注者或任何 X/Twitter 数据时，可以使用它。无需 API 密钥——该工具采用基于 cookie 的身份验证方式。
metadata: {"clawdbot":{"emoji":"🐦","requires":{"bins":["xfetch"]},"install":[{"id":"npm","kind":"node","package":"xfetch-cli","bins":["xfetch"],"label":"Install xfetch (npm)"}]}}
---

# xfetch 🐦

这是一个快速的X/Twitter命令行工具（CLI），无需使用API密钥，只需使用cookies即可进行数据抓取。

## 安装

```bash
npm install -g xfetch-cli
```

## 认证

xfetch需要Twitter的会话cookies（`auth_token`和`ct0`）。

**直接设置tokens：**
```bash
xfetch auth set --auth-token <token> --ct0 <token>
```

**检查认证状态：**
```bash
xfetch auth check
```

**从浏览器中获取cookies：** 在Chrome开发者工具中打开X.com → 应用程序 → Cookies → 复制`auth_token`和`ct0`的值。

## 命令

### 用户数据
```bash
xfetch user @handle              # Profile by handle
xfetch user 12345678             # Profile by ID
xfetch followers @handle -n 100  # Followers list
xfetch following @handle -n 100  # Following list
```

### 推文
```bash
xfetch tweets @handle -n 50      # User timeline
xfetch tweet <url-or-id>         # Single tweet
xfetch thread <url-or-id>        # Full conversation thread
```

### 搜索
```bash
xfetch search "query" -n 100
xfetch search "from:handle since:2024-01-01"
xfetch search "query" --type latest   # top|latest|people|photos|videos
```

### 时间线
```bash
xfetch home                      # Algorithmic home
xfetch home --following          # Chronological
xfetch bookmarks -n 50           # Your bookmarks
xfetch likes @handle -n 50       # User's likes
```

## 输出格式

```bash
xfetch tweets @handle --format json   # Default, pretty
xfetch tweets @handle --format jsonl  # Line-delimited JSON
xfetch tweets @handle --json          # Shorthand for JSON
xfetch tweets @handle --plain         # No formatting
```

## 分页

```bash
xfetch tweets @handle --all              # All pages
xfetch tweets @handle --max-pages 10     # Limit pages
xfetch tweets @handle --cursor <cursor>  # Resume from cursor
xfetch tweets @handle --delay 1000       # Delay between pages (ms)
```

## 查询ID管理

Twitter会频繁更改GraphQL查询ID，xfetch会自动更新这些ID。

```bash
xfetch query-ids --list      # Show cached IDs
xfetch query-ids --refresh   # Fetch latest from X
```

## 全局选项

```bash
--auth-token <token>   # Set auth_token directly
--ct0 <token>          # Set ct0 directly  
--format <format>      # json|jsonl|csv|sqlite
--timeout <ms>         # Request timeout (default: 30000)
--delay <ms>           # Delay between requests (default: 500)
--proxy <url>          # Proxy URL
```

## 示例

**获取用户的最新推文：**
```bash
xfetch tweets @elonmusk -n 20 --format jsonl
```

**搜索AI相关内容：**
```bash
xfetch search "AI agents" --type latest -n 50
```

**获取话题/对话：**
```bash
xfetch thread https://x.com/user/status/123456789
```

**将关注者导出为JSON格式：**
```bash
xfetch followers @handle --all > followers.json
```

## 速率限制

xfetch会监控每个端点的速率限制，并在接近限制时自动暂停请求。对于大量数据抓取，可以使用`--delay`参数来增加请求之间的时间间隔。

## 来源

GitHub: https://github.com/LXGIC-Studios/xfetch