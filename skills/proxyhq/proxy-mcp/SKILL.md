---
name: proxy-mcp
description: **AI代理支付的Proxy MCP服务器集成**：  
使用Proxy的Model Context Protocol工具来创建支付请求、配置虚拟卡片、查询余额以及追踪交易记录。此功能需要Proxy账户和代理令牌（agent token）的支持。
---

# MCP代理集成

连接到Proxy的MCP服务器以处理AI代理的支付请求。

## MCP服务器设置

### 选项1：NPX（推荐）

```json
{
  "mcpServers": {
    "proxy": {
      "command": "npx",
      "args": ["-y", "proxy-mcp-server"],
      "env": {
        "PROXY_AGENT_TOKEN": "your-agent-token"
      }
    }
  }
}
```

### 选项2：HTTP传输

```json
{
  "mcpServers": {
    "proxy": {
      "transport": "http",
      "url": "https://api.proxy.app/mcp",
      "headers": {
        "Authorization": "Bearer your-agent-token"
      }
    }
  }
}
```

## 13个MCP工具

### 用户与入职流程
- `proxy.user.get` - 获取用户资料和账户信息
- `proxy.kyc.status` - 检查KYC（了解客户）验证状态
- `proxy.kyc.link` - 获取KYC验证完成的链接

### 余额与资金
- `proxy.balance.get` - 获取可使用的支付额度
- `proxy.funding.get` - 获取ACH/电汇/加密货币存款的说明

### 意图（核心流程）
- `proxy.intents.create` - 创建支付意图（触发卡片发放）
- `proxy.intents.list` - 列出该代理的所有支付意图
- `proxy.intents.get` - 获取意图详情（包括卡片信息）

### 卡片
- `proxy_cards.get` - 获取卡片详情（屏蔽部分信息，如PAN码）
- `proxy_cards.getSensitive` - 获取完整的卡片号码、CVV码和有效期

### 交易
- `proxytransactions.list_for_card` - 列出某张卡的交易记录
- `proxy.transactions.get` - 获取详细的交易信息

### 实用工具
- `proxy.tools.list` - 列出所有可用的Proxy工具

## 核心支付流程

```
proxy.balance.get → proxy.intents.create → proxy.cards.get_sensitive → Pay
```

## 错误响应格式

```json
{
  "success": false,
  "error": {
    "code": "POLICY_REQUIRED",
    "message": "No policy configured",
    "hint": "Assign a policy to this agent",
    "context": "intents.create"
  }
}
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| `POLICY_REQUIRED` | 代理需要分配策略 |
| `ONBOARDING_INCOMPLETE` | 请先完成KYC验证 |
| `INSUFFICIENT_BALANCE` | 资金不足 |
| `AGENT_NOT_FOUND` | 无效的代理令牌 |
| `FORBIDDEN` | 权限被拒绝 |
| `INTENT_NOT_FOUND` | 意图ID无效 |
| `CARD_NOT_FOUND` | 卡片ID无效 |

## 开始使用

1. 在[proxy.app](https://proxy.app)注册
2. 完成KYC验证
3. 在控制面板中创建代理账户
4. 为代理分配支付策略（设置消费限额）
5. 生成代理令牌
6. 配置上述MCP设置