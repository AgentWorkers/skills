---
name: twit-mcp
description: 实时获取X/Twitter数据，并通过x402微支付功能执行相关操作。可以获取文章、推文、用户、列表和社区信息；支持发布推文、点赞、转发、添加书签、关注等功能。所有请求均按USDC计费，通过Base平台进行支付。无需使用API密钥。
version: 1.4.1
homepage: https://twit.sh
metadata:
  openclaw:
    requires:
      env: [WALLET_PRIVATE_KEY]
      bins: [npx]
    primaryEnv: WALLET_PRIVATE_KEY
    emoji: 🐦
    install:
      - kind: node
        package: twit-mcp
        bins: [twit-mcp]
---
# twit-mcp

您可以通过这个MCP服务器访问实时的X/Twitter数据并执行各种操作。每次工具调用费用为0.0025至0.01美元（USDC），费用会自动从您在Base平台上配置的钱包中扣除。无需使用API密钥。

## 可用工具

### 文章

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_article_by_id` | 通过推文ID获取X平台的文章全文（Markdown格式）。该功能不在官方X API中提供。 | 0.01美元（USDC） |

### 推文

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_tweet_by_id` | 通过ID获取推文内容 | 0.0025美元（USDC） |
| `get_user_tweets` | 获取用户的最新推文（分页显示） | 0.01美元（USDC） |
| `get_tweet_replies` | 获取推文的回复（分页显示） | 0.01美元（USDC） |
| `get_tweet_quote_tweets` | 获取推文的引用推文（分页显示） | 0.01美元（USDC） |
| `get_tweet_retweeted_by` | 获取转发该推文的用户（分页显示） | 0.01美元（USDC） |
| `search_tweets` | 带有过滤条件的推文搜索（完整存档） | 0.01美元（USDC） |
| `get_tweets` | 通过ID批量查询最多50条推文 | 0.01美元（USDC） |
| `post_tweet` | 以认证用户的身份发布新推文 | 0.0025美元（USDC） |
| `delete_tweet` | 删除用户拥有的推文 | 0.0025美元（USDC） |
| `like_tweet` | 以认证用户的身份点赞推文 | 0.0075美元（USDC） |
| `unlike_tweet` | 以认证用户的身份取消点赞 | 0.005美元（USDC） |
| `bookmark_tweet` | 将推文添加到书签 | 0.0025美元（USDC） |
| `unbookmark_tweet` | 从书签中删除推文 | 0.0025美元（USDC） |
| `retweet` | 以认证用户的身份转发推文 | 0.0075美元（USDC） |
| `unretweet` | 取消转发 | 0.005美元（USDC） |

### 用户

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_user_by_username` | 通过用户名获取用户信息 | 0.005美元（USDC） |
| `get_user_by_id` | 通过用户ID获取用户信息 | 0.005美元（USDC） |
| `search_users` | 按关键词搜索用户（分页显示） | 0.01美元（USDC） |
| `get_user_followers` | 获取用户的关注者（分页显示） | 0.01美元（USDC） |
| `get_user_following` | 获取用户关注的账户（分页显示） | 0.01美元（USDC） |
| `get_users` | 通过ID批量查询最多50个用户 | 0.01美元（USDC） |
| `follow_user` | 以认证用户的身份关注用户 | 0.0075美元（USDC） |
| `unfollow_user` | 以认证用户的身份取消关注 | 0.005美元（USDC） |

### 列表

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_list_by_id` | 通过ID获取列表详情 | 0.0025美元（USDC） |
| `get_list_members` | 获取列表的成员（分页显示） | 0.01美元（USDC） |
| `get_list_followers` | 获取列表的关注者（分页显示） | 0.01美元（USDC） |
| `get_list_tweets` | 获取列表的最新推文（分页显示） | 0.01美元（USDC） |

### 社区

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_community_by_id` | 通过ID获取社区详情。该功能不在官方X API中提供。 | 0.0025美元（USDC） |
| `get_community_posts` | 获取社区的最新帖子（分页显示）。该功能不在官方X API中提供。 | 0.01美元（USDC） |
| `get_community_members` | 获取社区的成员及其角色（分页显示）。该功能不在官方X API中提供。 | 0.01美元（USDC） |

### Twitter认证

执行写入操作（发布、删除、点赞、添加书签、转发、关注）需要连接Twitter/X账户。在尝试任何写入操作之前，请先调用`twitter_account_status`来检查账户是否已连接。

| 工具 | 描述 |
|------|-------------|
| `connect_twitter` | 连接Twitter/X账户（会打开浏览器窗口） |
| `twitter_account_status` | 检查Twitter账户是否已连接 |
| `disconnect_twitter` | 断开连接并清除存储的凭据 |

**连接账户：**

1. 调用`connect_twitter`——Chrome窗口将打开在x.com |
2. 如果系统提示，用户需要登录 |
3. 登录完成后，凭据会保存在本地文件`~/.twit-mcp-credentials.json`中 |
4. 之后即可立即使用各种写入功能——无需重新启动应用。

如果请求执行写入操作但账户未连接，请先调用`connect_twitter`并等待确认后再继续操作。

## 支付方式

每次工具调用都会向`x402.twit.sh`发送HTTP请求。服务器会返回“402 Payment Required”响应。MCP服务器会使用配置的`WALLET_PRIVATE_KEY`在本地完成USDC支付，并自动尝试多次支付（整个过程为一次往返请求）。私钥永远不会离开本地机器。

## 链接

- [twit.sh](https://twit.sh) — API参考和价格信息 |
- [npm: twit-mcp](https://www.npmjs.com/package/twit-mcp) |
- [x402.org](https://x402.org) — 支付协议文档