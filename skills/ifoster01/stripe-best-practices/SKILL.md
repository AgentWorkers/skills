---
name: stripe-best-practices
description: 构建 Stripe 支付集成的最佳实践
metadata:
  version: "245b3bbb"
  type: knowledge
  format: uasp
---

# Stripe最佳实践

构建Stripe支付集成的最佳实践

## 关键词

Stripe、支付、结账、订阅、计费

## 目的

- 集成支付处理功能  
- 管理订阅服务  
- 处理信用卡交易  

## 约束条件  

### 绝对不要使用：  
- `Charges` API  
- `Sources` API  
- `Card Element`（仅适用于基于信用卡的支付方式）  
- `Tokens` API（除非有特殊需求）  
- 混合使用不同的`Connect`支付类型  
- 旧版的`Connect`支付方式（Standard/Express/Custom）  

### 必须使用：  
- 最新的API/SDK版本（除非另有说明）  
- 对于处理原始PAN（Card Number）数据，需提供PCI合规性证明  
- 在使用`Connect`支付方式时，应使用控制器属性（而非旧版接口）  

## 推荐做法：  
- 在进行会话内支付时，优先使用`CheckoutSessions`而非`PaymentIntents`  
- 当默认选项为基于Stripe的结账流程时，优先选择`Stripe-hosted Checkout`  
- 当需要更多控制权时，优先使用`embedded Checkout`而非`Payment Element`  
- 在使用`Payment Element`时，优先选择动态支付方式（而非固定的`payment_method_types`）  
- 在保存支付方式信息时，优先使用`SetupIntents`而非`Sources`  
- 在支付前检查信用卡信息时，优先使用`Confirmation Tokens`而非`createPaymentMethod`/`createToken`  
- 在处理订阅或定期收费业务时，优先使用`Billing` API而非原始的`PaymentIntents`  
- 当平台希望Stripe承担风险时，优先选择“直接收费”（direct charges）模式；  
- 当平台自行承担费用责任时，优先选择“目的地收费”（destination charges）模式  

## 决策指南：  
- 当用户需要使用`Charges` API时，建议将其迁移到`CheckoutSessions`或`PaymentIntents`  
- 当用户需要使用`Card Element`时，建议将其迁移到`Payment Element`  
- 在处理定期收入、订阅或SaaS业务时，推荐使用`Billing` API并结合`Checkout`前端界面  
- 在进行集成时，应遵循Stripe的官方建议，并使用控制器属性  
- 在从其他支付处理商迁移PAN数据时，需遵循相应的迁移流程  
- 在创建支付意图（payment intent）之前渲染`Payment Element`时，应使用`Confirmation Tokens`  

## 参考资料：  
- [stripe:integration-options](https://docs.stripe.com/payments/payment-methods/integration-options) – 主要的集成设计参考  
- [stripe:api-tour](https://docs.stripe.com/payments-api/tour) – API概述  
- [stripe:go-live](https://docs.stripe.com/get-started/checklist/go-live) – 上线前的检查清单  
- [stripe:migration/charges](https://docs.stripe.com/payments/payment-intents/migration/charges) – 从`Charges` API迁移到`PaymentIntents`的流程  
- [stripe:migration/payment-element](https://docs.stripe.com/payments/payment-element/migration) – 从`Card Element`迁移到`Payment Element`的流程  
- [stripe:billing/design-integration](https://docs.stripe.com/billing/subscriptions/designing-integration) – 订阅服务的集成规划  
- [stripe:connect/recommendations](https://docs.stripe.com/connect/integration-recommendations) – `Connect`支付方式的选择建议  
- [stripe:pan-import](https://docs.stripe.com/get-started/data-migrations/pan-import) – PAN数据的迁移方法