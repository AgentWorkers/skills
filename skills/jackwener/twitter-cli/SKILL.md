---
name: twitter-cli
description: 无需使用 API 密钥，即可从终端读取 Twitter/X 的时间线、书签以及用户发布的帖子。
---
# twitter-cli 技能

当用户希望在不使用 API 密钥的情况下通过终端读取 Twitter/X 的内容时，可以使用此技能。

## 要求

- 已安装 `twitter-cli` 并且该工具已添加到系统的 PATH 环境变量中。
- 用户已在 Chrome/Edge/Firefox/Brave 浏览器中登录到 `x.com`，或者设置了以下环境变量：
  - `TWITTER_AUTH_TOKEN`
  - `TWITTER_CT0`

## 核心命令

```bash
# Home timeline (For You)
twitter feed

# Following timeline
twitter feed -t following

# Bookmarks
twitter favorite

# User profile and posts
twitter user <screen_name>
twitter user-posts <screen_name> --max 20
```

## JSON / 脚本编写

```bash
# Export feed as JSON
twitter feed --json > tweets.json

# Read from local JSON file
twitter feed --input tweets.json
```

## 排名筛选

筛选功能是可选的（默认为关闭状态）。可以使用 `--filter` 参数来启用该功能。

```bash
twitter feed --filter
twitter favorite --filter
```

评分公式：

```text
score = likes_w * likes
      + retweets_w * retweets
      + replies_w * replies
      + bookmarks_w * bookmarks
      + views_log_w * log10(max(views, 1))
```

请在 `config.yaml` 文件中配置相应的权重和模式。

## 安全提示

- 请勿要求用户在聊天记录中分享原始的 cookie 值。
- 建议优先使用浏览器的本地 cookie 功能来获取数据，而非手动复制/粘贴敏感信息。
- 如果认证失败（出现 401/403 错误），请让用户重新登录 `x.com`。