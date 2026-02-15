---
name: Subscriptions
description: 构建一个个人订阅跟踪工具，用于管理定期付款、续订事务，并减少不必要的开支。
metadata: {"clawdbot":{"emoji":"🔄","os":["linux","darwin","win32"]}}
---

## 核心功能
- 当用户提及订阅服务时，将其添加到跟踪列表中。
- 当用户询问费用支出情况时，显示总费用信息。
- 在订阅服务续订或价格调整前发出提醒。
- 创建名为 `~/subscriptions/` 的工作文件夹用于存储相关数据。

## 文件结构
```
~/subscriptions/
├── active/
│   ├── streaming.md
│   ├── software.md
│   └── services.md
├── cancelled.md
└── totals.md
```

## 订阅信息记录
```markdown
## Netflix
- Cost: $15.99/month
- Billing: 15th
- Card: Visa •4242
- Last used: Yesterday
- Value: High
```

## 费用统计
```markdown
# totals.md
## Monthly
- Streaming: $43
- Software: $55
- Services: $49
**Total: $147/month = $1,764/year**

## Annual Renewals Coming
- Adobe: Sep 15 ($660)
- Amazon Prime: Oct 1 ($139)
```

## 需要跟踪的信息
- 费用金额及计费频率
- 计费日期和支付方式
- 最后使用时间
- 用户对服务的满意度（高/中/低）

## 需要展示的信息
- “您每月在订阅服务上的支出为165美元。”
- “HBO服务已3周未被使用。”
- “Adobe订阅服务将在30天后自动续订，费用为660美元。”
- “本周有三项订阅服务需要付费。”

## 审查触发条件
- 如果服务超过30天未被使用，建议用户取消订阅。
- 当价格发生变化时，需要立即通知用户。
- 年度续订前7天需要提醒用户。
- 每季度提醒用户：“您是否仍然认为这项服务有价值？”

## 取消订阅的记录
```markdown
# cancelled.md
## 2024
- Hulu: Feb 1 (never used) — saved $18/mo
```

## 逐步改进计划
- 初始阶段：列出用户当前所有的订阅服务。
- 添加每个订阅服务的计费日期和费用信息。
- 跟踪用户的订阅使用情况。
- 培养用户每季度定期审查订阅服务的习惯。

## 不应做的事情
- 直到费用被收取才想起年度续订的事宜。
- 忽视那些长期未被使用的订阅服务。
- 忽略价格变动的信息。
- 仅仅为了“以防万一”而保留某些服务。