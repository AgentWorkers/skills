---
name: x-bookmarks
version: 1.1.0
description: >
  Fetch, summarize, and manage X/Twitter bookmarks via bird CLI or X API v2.
  Use when: (1) user says "check my bookmarks", "what did I bookmark", "bookmark digest",
  "summarize my bookmarks", "x bookmarks", "twitter bookmarks", (2) user wants a periodic
  digest of saved tweets, (3) user wants to categorize, search, or analyze their bookmarks,
  (4) scheduled bookmark digests via cron.
  Auth: bird CLI with browser cookies, OR X API v2 with OAuth 2.0 tokens.
requires:
  env:
    - AUTH_TOKEN: "X/Twitter auth token (from browser cookies, for bird CLI auth)"
    - CT0: "X/Twitter CSRF token (from browser cookies, for bird CLI auth)"
    - X_API_BEARER_TOKEN: "Optional: X API v2 Bearer token (alternative to bird CLI)"
  bins:
    - bird: "bird-cli (npm i -g bird-cli) - preferred backend"
  files:
    - .env.bird: "Optional: stores AUTH_TOKEN and CT0 for bird CLI"
    - ~/.config/x-bookmarks/tokens.json: "OAuth 2.0 tokens for X API v2 backend"
security:
  credentials: >
    This skill accesses X/Twitter bookmarks, which requires authentication.
    Two methods are supported: (1) bird CLI using browser cookies (AUTH_TOKEN/CT0 env vars
    sourced from .env.bird), or (2) X API v2 with OAuth 2.0 tokens stored locally.
    All credentials are stored locally on the user's machine and never transmitted
    to third parties. The user must explicitly provide or authorize credentials.
  permissions:
    - read: "X/Twitter bookmarks (read-only access)"
    - write: "Local files only (bookmark state, token storage)"
---

# X 书签 v2

将 X/Twitter 书签从一堆“好主意”的集合转化为可执行的行动。

**核心理念：** 不仅仅是总结内容，还要提出代理可以执行的操作。

## 数据源选择

该功能支持 **两种后端**。请选择其中一种可用且适合您需求的后端：

### 1. bird CLI（优先推荐）
- 快速，无需 API 密钥，使用浏览器 cookie
- 安装方式：`npm install -g bird-cli`
- 测试命令：`bird whoami` — 如果输出用户名，说明安装成功

### 2. X API v2（备用方案）
- 不需要 bird CLI
- 需要 X 开发者账户和 OAuth 2.0 认证
- 设置方法：请参考 [references/auth-setup.md](references/auth-setup.md) → “X API 设置”

### 自动检测逻辑

```
1. Check if `bird` command exists → try `bird whoami`
2. If bird works → use bird CLI path
3. If not → check for X API tokens (~/.config/x-bookmarks/tokens.json)
4. If tokens exist → use X API path (auto-refresh)
5. If neither → guide user through setup (offer both options)
```

## 获取书签信息

### 使用 bird CLI

```bash
# Latest 20 bookmarks (default)
bird bookmarks --json

# Specific count
bird bookmarks -n 50 --json

# All bookmarks (paginated)
bird bookmarks --all --json

# With thread context
bird bookmarks --include-parent --thread-meta --json

# With Chrome cookie auth
bird --chrome-profile "Default" bookmarks --json

# With manual tokens
bird --auth-token "$AUTH_TOKEN" --ct0 "$CT0" bookmarks --json
```

如果用户有 `.env.bird` 文件或环境变量 `AUTH_TOKEN`/`CT0`，请先加载这些配置：
`source .env.bird`

### 使用 X API v2

```bash
# First-time setup (opens browser for OAuth)
python3 scripts/x_api_auth.py --client-id "YOUR_CLIENT_ID" --client-secret "YOUR_SECRET"

# Fetch bookmarks (auto-refreshes token)
python3 scripts/fetch_bookmarks_api.py -n 20

# All bookmarks
python3 scripts/fetch_bookmarks_api.py --all

# Since a specific tweet
python3 scripts/fetch_bookmarks_api.py --since-id "1234567890"

# Pretty print
python3 scripts/fetch_bookmarks_api.py -n 50 --pretty
```

X API 返回的 JSON 格式与 bird CLI 相同，因此所有后续处理流程都可以正常运行。

**令牌管理是自动的：** 令牌存储在 `~/.config/x-bookmarks/tokens.json` 文件中，并通过 `refresh_token` 重新生成。如果刷新失败，系统会提示用户重新运行 `x_api_auth.py`。

### 环境变量覆盖

如果用户已经拥有Bearer 令牌（例如来自其他工具），可以跳过 OAuth 认证步骤：
```bash
X_API_BEARER_TOKEN="your_token" python3 scripts/fetch_bookmarks_api.py -n 20
```

## JSON 输出格式（两种后端均相同）

每个书签都会返回以下信息：
```json
{
  "id": "tweet_id",
  "text": "tweet content",
  "createdAt": "2026-02-11T01:00:06.000Z",
  "replyCount": 46,
  "retweetCount": 60,
  "likeCount": 801,
  "bookmarkCount": 12,
  "viewCount": 50000,
  "author": { "username": "handle", "name": "Display Name" },
  "media": [{ "type": "photo|video", "url": "..." }],
  "quotedTweet": { "id": "..." }
}
```

## 核心工作流程

### 1. 以行动为导向的摘要（主要使用场景）

关键区别在于：不仅仅是总结内容，还要提出具体的操作建议。

1. 获取书签信息（通过 bird CLI 或 X API，系统会自动检测）
2. 按主题对书签进行分类（自动识别类别：加密技术、人工智能、市场营销、工具、个人内容等）
3. 对每个类别提出具体建议：
   - **工具/仓库书签** → “我可以测试这个工具，或者设置它的配置，或者分析其代码”
   - **策略/建议书签** → “以下是可执行的步骤——需要我帮忙实现吗？”
   - **新闻/趋势** → “这与您的业务相关。这是相关内容的创作方向”
   - **内容创意** → “这个内容很适合用您的声音制作成推文或视频。这里有一个草稿”
   - **问题/讨论** → “我可以深入研究并为您总结”
4. 标记过期的书签（超过 2 周）——“要么使用这些内容，要么删除它们”
5. 以分类的形式输出摘要及相应的操作建议

输出格式如下：
```
📂 CATEGORY (count)
• Bookmark summary (@author)
→ 🤖 I CAN: [specific action the agent can take]
```

### 2. 定时摘要（通过 Cron 任务）

设置定期检查书签的机制。向用户推荐以下 Cron 配置：

```
Schedule: daily or weekly
Payload: "Check my X bookmarks for new saves since last check.
  Fetch bookmarks, compare against last digest, summarize only NEW ones.
  Categorize and propose actions. Deliver to me."
```

通过保存最近处理的书签 ID 来跟踪状态：
`memory/bookmark-state.json` → `{ "lastSeenId": "...", "lastDigestAt": "..." }`

### 3. 内容再利用

当用户请求从书签中获取内容创意时：
1. 获取最新的书签信息
2. 筛选出获得高互动量（超过 500 个赞）的推文（包含框架、技巧或见解）
3. 用用户的声音重新表述这些关键内容（如果用户有语音数据）
4. 根据书签的原始互动情况建议合适的发布时间

### 4. 模式识别

当用户有足够多的书签记录时：
1. 获取所有书签信息（使用 `--all` 参数）
2. 按主题或关键词对书签进行分类
3. 报告： “您已经收藏了 N 条关于 [主题] 的推文。需要我进一步研究吗？”
4. 根据分类结果推荐研究报告、内容系列或相关工具

### 5. 书签清理

对于过期的书签：
1. 找出超过指定时间限制（默认为 30 天）的书签
2. 对每个书签提取核心内容及一个可执行的建议
3. 提示用户： “今天就应用这个建议，否则请删除它”
4. 用户可以通过 `bird unbookmark <tweet-id>` 命令取消书签的收藏（仅适用于 bird CLI）

## 错误处理

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `bird: command not found` | 未安装 bird CLI | 使用 X API 的路径，或运行 `npm install -g bird-cli` |
| “未找到 Twitter cookie” | 用户未在浏览器中登录 X 账户 | 在 Chrome/Firefox 中登录 x.com，或使用 X API |
| Safari 中的权限问题 | macOS 系统权限限制 | 使用 Chrome/Firefox 或 X API |
| 结果为空 | Cookie/令牌过期 | 重新登录或重新运行 `x_api_auth.py` |
| 超过 API 请求限制（429 错误） | API 请求过多 | 等待一段时间后重试，可以使用 `--count` 参数限制请求次数 |
| “未找到 X API 令牌” | 未完成认证设置 | 运行 `x_api_auth.py --client-id YOUR_ID` |
| 令牌刷新失败 | 令牌过期 | 重新运行 `x_api_auth.py` 以重新授权 |

## 使用技巧

- 使用 `-n 20` 参数快速获取简要摘要，使用 `--all` 参数进行详细分析
- 使用 `bird: --include-parent` 可以在回复中显示讨论的上下文
- X API 提供 `bookmarkCount` 和 `viewCount` 参数（bird CLI 可能不提供）
- 使用 `bird --folder-id <id>` 可以按文件夹管理书签
- 两种后端返回的 JSON 格式相同，因此处理流程不受后端限制