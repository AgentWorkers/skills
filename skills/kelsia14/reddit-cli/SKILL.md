---
name: reddit-cli
version: 1.0.2
description: Reddit命令行工具（Reddit CLI）使用cookie进行身份验证。支持读取帖子、执行搜索以及获取子版块（subreddit）的相关信息。
author: kelsia14
---

# Reddit CLI

使用您的会话cookie访问Reddit，无需API密钥。

## 快速入门

```bash
reddit-cli posts programming 10       # Get 10 hot posts
reddit-cli posts gaming 5 top         # Get top 5 posts
reddit-cli search "python tutorial"   # Search all Reddit
reddit-cli search "help" --sub linux  # Search in subreddit
reddit-cli info AskReddit             # Subreddit info
reddit-cli check                      # Test connection
```

## 命令

### 从子版块获取帖子
```bash
reddit-cli posts <subreddit> [limit] [sort]
```
- limit: 帖子数量（默认：10）
- sort: 热门、最新、顶部、上升趋势（默认：热门）

### 在Reddit上搜索
```bash
reddit-cli search <query> [--sub <subreddit>] [limit]
```

### 获取子版块信息
```bash
reddit-cli info <subreddit>
```

### 检查连接
```bash
reddit-cli check
```

## 环境配置

将这些设置添加到`~/.bashrc`文件中：
```bash
export REDDIT_SESSION="your_reddit_session_cookie"
export TOKEN_V2="your_token_v2_cookie"  # optional
```

## 获取cookie

1. 访问reddit.com（已登录）
2. 使用开发者工具（F12）→ 应用程序 → Cookies → reddit.com
3. 复制`reddit_session`值
4. （可选）复制`token_v2`值

## 注意事项

- Cookie会过期，您可能需要定期刷新它们
- 该工具遵守Reddit的速率限制
- 仅限个人使用