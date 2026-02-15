---
name: falcon
description: 通过 TwexAPI 搜索、阅读并与 Twitter/X 交互
user-invocable: true
command-dispatch: tool
command-tool: Bash
command-arg-mode: raw
metadata: {"openclaw":{"requires":{"bins":["curl","jq"],"env":["TWEXAPI_KEY"]},"primaryEnv":"TWEXAPI_KEY","emoji":"🦅","os":["darwin","linux"]}}
---

**falcon**

使用 `falcon` 命令可以读取、搜索和与 Twitter/X 交互。

**快速入门**

```bash
falcon check      # 检查 `falcon` 是否可用
falcon user elonmusk    # 查找用户 "elonmusk"
falcon tweets elonmusk 5    # 查看用户 "elonmusk" 的 5 条推文
falcon read <url-or-id>   # 通过 URL 或 ID 读取推文
falcon search "bitcoin" 10    # 搜索包含 "bitcoin" 的推文（返回 10 条结果）
```

**用户操作**

```bash
falcon user <username>      # 查看单个用户的个人信息
falcon users <u1,u2,...>    # 查看多个用户（用逗号分隔）
falcon find <keyword> [count]  # 按关键词搜索用户（默认返回 5 条结果）
falcon followers <username> [count]  # 查看用户的关注者（默认返回 20 个）
falcon following <username> [count]  # 查看用户关注的人（默认返回 20 个）
```

**推文操作**

```bash
falcon tweets <username> [count]   # 查看用户的所有推文及回复（默认返回 20 条）
falcon read <id-or-url>     # 通过 ID 或 URL 读取特定推文
falcon replies <id-or-url> [count]   # 查看某条推文的回复（默认返回 20 条）
falcon similar <id-or-url>    # 查找相似的推文
falcon retweeters <id-or-url> [count]  # 查看某条推文的转发者（默认返回 20 个）
```

**搜索**

```bash
falcon search <query> [count]      # 进行高级搜索（默认返回 10 条结果）
falcon hashtag <tag> [count]    # 按标签搜索（默认返回 20 条结果）
falcon cashtag <tag> [count]    # 按话题标签搜索（默认返回 20 条结果）
falcon trending [country]   # 查看指定国家的热门话题（默认为全球范围）
```

**发布内容（需先获取用户授权）**

```bash
falcon tweet "text"      # 发布新推文
falcon reply <id-or-url> "text"    # 回复某条推文
falcon quote <tweet-url> "text"   # 引用某条推文
```

**互动操作**

```bash
falcon like <id-or-url>      # 点赞某条推文
falcon unlike <id-or-url>     # 取消点赞
falcon retweet <id-or-url>    # 转发某条推文
falcon bookmark <id-or-url>    # 将推文添加书签
falcon follow <username>     # 关注用户
falcon unfollow <username>    # 取消关注用户
```

**账户管理**

```bash
falcon check         # 确认 API 密钥和 Cookie 已设置
falcon balance        # 查看剩余的 API 信用额度
```

**认证信息**

- `TWEXAPI_KEY`：环境变量，用于存储 TwexAPI 的 bearer token（所有命令均需此信息）
- `TWITTER_COOKIE`：环境变量，用于存储 Twitter 的认证 cookie（写入/互动操作需此信息）

**重要说明：**

- `falcon` 脚本位于 `{baseDir}/falcon.sh` 文件中。
- 所有命令均支持使用推文的 URL（格式如 `x.com` 或 `twitter.com`）或推文的 ID。
- 在执行任何写入或互动操作前，请务必先获取用户的授权。
- 搜索功能支持 Twitter 的高级搜索语法。
- 标签（# 开头）和话题标签（$ 开头）均可被使用。
- 热门话题的国家和地区名称需使用特定格式（如 `united-states`、`united-kingdom`、`japan` 等）。