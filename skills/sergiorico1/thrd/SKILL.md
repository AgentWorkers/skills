---
name: thrd
description: "通过 thrd.email API 自动化电子邮件账户的配置和管理。该 API 可用于：  
(1) 即时创建新的电子邮件账户（可选择租户名称）；  
(2) 获取 API 密钥和收件箱详情；  
(3) 监控收到的电子邮件；  
(4) 发送/回复电子邮件（要求操作具有幂等性，即多次执行相同操作不会产生不同结果）；  
(5) 跟踪邮件的发送状态；  
(6) 为计划升级生成 Stripe 结账链接。"
---

# 第三电子邮件技能

该技能允许您使用 [thrd.email](https://thrd.email) 基础设施来管理 AI 代理的电子邮件账户。

## 工作流程

### 创建新电子邮件账户
要创建一个新的电子邮件账户，请运行入职脚本：
```bash
python3 scripts/onboard.py [tenant_name]
```

### 升级计划（计费）
要将当前租户升级到更高级别的套餐（Limited 或 Verified），请使用结算脚本：
```bash
python3 scripts/checkout.py <plan_name>
```
将生成的 Stripe 结算链接转发给您的负责人以完成支付。

### 管理电子邮件并跟踪送达情况
有关详细的 API 使用说明（轮询、发送、回复以及检查送达状态），请参阅 [references/api.md](references/api.md)。

## 工具
- `scripts/onboard.py`：用于立即创建新的电子邮件收件箱。
- `scripts/checkout.py`：用于生成用于升级的 Stripe 结算链接。