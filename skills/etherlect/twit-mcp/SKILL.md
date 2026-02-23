---
name: twit-mcp
description: 通过 x402 微支付实时获取 X/Twitter 数据：可以查询用户信息、获取推文、搜索全部历史记录——每次请求按 USDC 在 Base 平台上收费。无需 API 密钥。
version: 1.0.0
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

这是一个用于AI代理的实时X/Twitter数据服务，由[x402](https://x402.org)提供的微支付技术支持。每次工具调用费用为0.0025至0.01美元（USDC），费用会自动从您的Base钱包中扣除。无需API密钥。

## 设置

在OpenClaw的环境设置中配置您的钱包私钥：

```
WALLET_PRIVATE_KEY=0xYourPrivateKeyHere
```

> 请使用一个余额较少的专用钱包，切勿使用您的主钱包。

然后将以下配置添加到您的`mcp.json`文件中：

```json
{
  "mcpServers": {
    "twit": {
      "command": "npx",
      "args": ["-y", "twit-mcp"],
      "env": {
        "WALLET_PRIVATE_KEY": "${WALLET_PRIVATE_KEY}"
      }
    }
  }
}
```

## 可用工具

### 用户相关工具

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_user_by_username` | 通过用户名获取用户信息 | 0.005美元（USDC） |
| `get_user_by_id` | 通过用户ID获取用户信息 | 0.005美元（USDC） |
| `search_users` | 按关键词搜索用户（分页显示） | 0.01美元（USDC） |
| `get_user_followers` | 获取用户的关注者（分页显示） | 0.01美元（USDC） |
| `get_user_following` | 获取用户所关注的账户（分页显示） | 0.01美元（USDC） |
| `get_users` | 批量查询最多50个用户信息 | 0.01美元（USDC） |

### 推文相关工具

| 工具 | 描述 | 费用 |
|------|-------------|-------|
| `get_tweet_by_id` | 通过ID获取推文内容 | 0.0025美元（USDC） |
| `get_user_tweets` | 获取用户的最新推文（分页显示） | 0.01美元（USDC） |
| `search_tweets` | 带过滤条件的推文全文搜索 | 0.01美元（USDC） |
| `get_tweets` | 批量查询最多50条推文 | 0.01美元（USDC） |

## 使用示例

```
Get me the latest tweets from @elonmusk about doge
```

```
Look up the Twitter profile of vitalik.eth
```

```
Search for tweets from @sama since 2025-01-01 mentioning Claude
```

```
How many followers does @jack have?
```

## 支付方式

每次工具调用都会向`x402.twit.sh`发送HTTP请求。服务器会返回“402 Payment Required”（需要支付）的响应。MCP服务器会使用您的`WALLET_PRIVATE_KEY`在本地完成USDC支付，并自动重试请求——整个过程都是自动完成的，无需人工干预。您的私钥永远不会离开您的设备。

## 链接

- [twit.sh](https://twit.sh) — API参考与价格信息 |
- [npm: twit-mcp](https://www.npmjs.com/package/twit-mcp) — 包安装链接 |
- [x402.org](https://x402.org) — 支付协议文档 |