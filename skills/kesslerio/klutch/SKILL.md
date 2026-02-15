---
name: klutch
description: OpenClaw技能：用于集成Klutch的可编程信用卡API。可以查看信用卡信息、交易记录、消费类别，并分析消费模式。
metadata:
  openclaw:
    emoji: 💳
    requires:
      env: []
      optional_env:
        - KLUTCH_CLIENT_ID
        - KLUTCH_SECRET_KEY
        - KLUTCH_API_KEY
        - KLUTCH_API_SECRET
        - KLUTCH_1PASSWORD_ITEM
    install:
      - id: pip
        kind: pip
        requirements: requirements.txt
---

# Klutch Skill

这是一个用于集成Klutch可编程信用卡API的OpenClaw技能。

## 概述

该技能提供了一个命令行接口，用于通过Klutch的GraphQL API访问信用卡数据。它支持查看卡片信息、交易历史、消费类别以及消费分析。

## 先决条件

1. **Klutch账户**：一个活跃的Klutch信用卡账户。
2. **API凭据**：来自Klutch开发者门户的客户端ID和密钥。
3. **Python 3.10+**：运行脚本所必需的版本。

## 配置

### 环境变量

设置您的Klutch API凭据：

```bash
# Option 1: Direct credentials
export KLUTCH_CLIENT_ID="your-client-id"
export KLUTCH_SECRET_KEY="your-secret-key"

# Option 2: 1Password CLI integration (requires 'op' CLI)
export KLUTCH_1PASSWORD_ITEM="Klutch API Credential"
```

### 配置文件

该技能将配置信息和会话令牌存储在`~/.config/klutch/`目录下：

```bash
~/.config/klutch/
├── config.json      # User preferences
└── token.json       # Cached session token (auto-managed)
```

### 配置选项

编辑`~/.config/klutch/config.json`文件以进行自定义设置：

```json
{
  "api": {
    "endpoint": "https://graphql.klutchcard.com/graphql",
    "timeout": 30
  }
}
```

## 命令参考

### 查看余额

```bash
# Check card information
python scripts/klutch.py balance

# Example output:
{
  "cards": [
    {
      "id": "crd_xxx",
      "name": "Martin Kessler",
      "status": "ACTIVE"
    }
  ]
}
```

### 查看交易记录

```bash
# List recent transactions (last 30 days)
python scripts/klutch.py transactions

# Limit results
python scripts/klutch.py transactions --limit 25

# Example output:
{
  "transactions": [
    {
      "id": "txn_xxx",
      "amount": -100.0,
      "merchantName": "Checking",
      "transactionStatus": "SETTLED"
    }
  ]
}
```

### 卡片管理

#### 列出卡片

```bash
python scripts/klutch.py card list
```

#### 查看消费类别

```bash
python scripts/klutch.py card categories
```

#### 按类别查看消费情况

```bash
python scripts/klutch.py card spending
```

### 配置管理

```bash
# Get configuration value
python scripts/klutch.py config get api.timeout

# Set configuration value
python scripts/klutch.py config set api.timeout 60

# View all configuration
python scripts/klutch.py config get
```

## API端点

该技能连接到Klutch的GraphQL API：

| 环境 | 端点 |
|---------|--------|
| 生产环境 | `https://graphql.klutchcard.comgraphql` |
| 沙盒环境 | `https://sandbox.klutchcard.comgraphql` |

## 认证流程

该技能使用Klutch的会话令牌进行认证：

1. **初始请求**：使用客户端ID和密钥发送`createSessionToken` mutation。
2. **令牌缓存**：将JWT会话令牌存储在`~/.config/klutch/token.json`文件中。
3. **后续请求**：使用缓存的令牌，直到其过期。
4. **自动刷新**：当缓存的令牌失效时，会自动创建新的会话令牌。

## 假设的代理使用场景

Klutch技能使代理能够管理自己的预算或提供个人财务帮助：

*   **子代理预算管理**：为子代理创建虚拟卡片，以便其支付自己的费用（例如AWS、OpenAI），并设置使用上限。
*   **预算监控**：监控消费类别（例如“食品”），并在超出月度预算时提醒用户。
* **交易警报**：监控特定商家或异常交易，并立即通知用户。
* **费用汇总**：汇总每月的消费情况，并按类别分类以便个人记录。

## 错误处理

该技能能够处理以下常见错误情况：

- **认证失败**：提示用户验证凭据。
- **会话过期**：自动创建新的会话令牌。
- **网络错误**：显示错误信息并提供重试建议。
- **GraphQL错误**：显示来自API的详细错误信息。

## 与OpenClaw的集成

### 从OpenClaw会话中使用该技能

```bash
# OpenClaw can invoke the skill directly
klutch balance
klutch transactions --limit 5
klutch card list
```

## 故障排除

### 认证问题

如果您遇到认证错误：
1. 使用`python scripts/klutch.py config get`命令验证您的凭据。
2. 删除`~/.config/klutch/token.json`文件以强制重新认证。
3. 确保您的API凭据正确无误。

### 会话令牌问题

强制刷新令牌：
```bash
rm ~/.config/klutch/token.json
```

## 安全注意事项

- **切勿将凭据提交到版本控制系统中**。
- 该技能将令牌存储在`~/.config/klutch/token.json`文件中。
- 会话令牌会在需要时自动刷新。