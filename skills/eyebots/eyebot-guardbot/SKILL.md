---
name: eyebot-guardbot
description: 安全监控与威胁警报系统
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: security-monitoring
---

# GuardBot 🛡️

**实时安全监控**

实时监控您的钱包、合约和持仓，及时发现潜在威胁，并接收关于可疑活动的警报。

## 主要功能

- **钱包监控**：追踪所有钱包交易活动
- **合约监控**：监控合约的升级或变更情况
- **批准流程跟踪**：在token被批准时发出警报
- **异常检测**：利用人工智能识别潜在威胁
- **即时警报**：通过Telegram/Discord发送通知

## 警报类型

| 警报类型 | 触发条件 |
|---------|-----------|
| 大额转账 | 检测到异常资金流出 |
| 新的批准请求 | Token获得批准 |
| 合约变更 | 被监控的合约被修改 |
| 可疑交易 | 识别出可疑的交易模式 |
| 骗局合约 | 发现可能用于诈骗的合约 |

## 保护措施

- 提供撤销批准的功能
- 具备紧急转账能力
- 实施黑名单机制
- 能够检测网络钓鱼攻击
- 拥有专门用于识别诈骗行为的数据库

## 使用方法

```bash
# Watch a wallet
eyebot guardbot watch <wallet_address>

# Check approvals
eyebot guardbot approvals <wallet>

# Revoke approval
eyebot guardbot revoke <token> <spender>
```

## 帮助支持

Telegram: @ILL4NE