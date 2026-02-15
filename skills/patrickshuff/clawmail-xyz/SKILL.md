---
name: clawmail
description: 专为AI代理设计的电子邮件服务，支持钱包认证和加密货币支付功能。
metadata:
  openclaw:
    emoji: "📧"
    bins:
      - node
      - npx
    os:
      - darwin
      - linux
      - win32
    install:
      npm: clawmail
    homepage: https://clawmail.xyz
    capabilities:
      - email
      - mcp
      - wallet-auth
      - x402
---

# ClawMail

**clawmail.xyz** 为 AI 代理提供的电子邮件基础设施。

## 功能概述

ClawMail 为大型语言模型（LLMs）和 AI 代理提供以下电子邮件服务：

- **基于钱包的认证**：无需密码，使用以太坊钱包签名（EIP-191）进行身份验证。
- **x402 加密支付**：支持使用 USDC 在 Base 主网上进行支付。
- **MCP 集成**：可通过 Model Context Protocol 直接访问相关工具。
- **免费 tier**：提供随机生成的电子邮件地址，支持发送 1000 条消息。

## 价格方案

| 计费等级 | 费用 | 功能 |
|------|------|----------|
| 免费 | $0 | 随机生成的电子邮件地址，1000 条消息 |
| 付费 | $1 USDC | 自定义电子邮件地址，无限消息发送量 |

## MCP 工具

该技能提供了 5 个用于电子邮件管理的工具：

### `check_mailbox_availability`  
检查指定的电子邮件地址是否可用于注册。

```json
{ "address": "myagent" }
```

### `login`  
使用钱包签名进行身份验证，并返回会话令牌。

```json
{
  "address": "myagent@clawmail.xyz",
  "walletAddress": "0x...",
  "signature": "0x...",
  "message": "Sign in to ClawMail..."
}
```

### `list_messages`  
列出收件箱中的所有消息。

```json
{
  "address": "myagent",
  "token": "jwt-token",
  "limit": 50,
  "unreadOnly": false
}
```

### `read_message`  
根据消息 ID 读取特定消息，并将其标记为已读。

```json
{
  "address": "myagent",
  "messageId": "uuid",
  "token": "jwt-token"
}
```

### `delete_message`  
从收件箱中删除指定消息。

```json
{
  "address": "myagent",
  "messageId": "uuid",
  "token": "jwt-token"
}
```

## 使用方法

- **推荐使用 npx 命令行工具**：[使用方法](```bash
npx clawmail
```)

- **全局安装**：[安装步骤](```bash
npm install -g clawmail
clawmail
```

- **在 Claude Desktop 中配置**：将相关配置添加到 `claude_desktop_config.json` 文件中。

## API 接口

REST API 的地址为 `https://clawmail.xyz`，提供以下接口：

| 接口 | 方法 | 描述 |
|----------|--------|-------------|
| `/health` | GET | 系统健康检查 |
| `/api/mailbox/available/:address` | GET | 检查电子邮件地址的可用性 |
| `/api/mailbox` | POST | 创建新的邮箱账户（需要 x402 加密验证） |
| `/api/auth/challenge` | GET | 获取登录挑战信息 |
| `/api/auth/login` | POST | 使用钱包进行身份验证 |
| `/api/messages` | GET | 列出所有消息 |
| `/api/messages/:id` | GET | 读取指定消息 |
| `/api/messages/:id` | DELETE | 删除指定消息 |

## 认证流程

1. 获取登录挑战信息：`GET /api/auth/challenge`
2. 使用以太坊钱包的签名（EIP-191）完成挑战验证。
3. 提交签名结果：`POST /api/auth/login`
4. 使用返回的 JWT 令牌进行后续请求。

## 相关链接

- **官方网站**：https://clawmail.xyz
- **项目源代码**：https://github.com/patrickshuff/clawmail