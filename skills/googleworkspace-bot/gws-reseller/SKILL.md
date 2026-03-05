---
name: gws-reseller
version: 1.0.0
description: "**Google Workspace经销商：管理Workspace订阅服务**"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws reseller --help"
---
# 经销商（v1）

> **前提条件：** 阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局标志和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

```bash
gws reseller <resource> <method> [flags]
```

## API 资源

### 客户

  - `get` — 获取客户账户信息。此操作可用于查看您在经销商管理中的客户账户，或查看您未管理的现有客户的最低限度账户信息。有关现有客户 API 响应的更多信息，请参阅 [检索客户账户](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_customers#get_customer)。
  - `insert` — 注册新客户账户。
  - `patch` — 更新客户账户设置。该方法支持增量更新（patch）语义。您无法通过经销商 API 更改 `customerType`，但 “team” 类型的客户可以验证其域名并使 `customerType` 变为 “domain”。有关更多信息，请参阅 [验证域名以解锁基础功能](https://support.google.com/a/answer/9122284)。
  - `update` — 更新客户账户设置。您无法通过经销商 API 更改 `customerType`，但 “team” 类型的客户可以验证其域名并使 `customerType` 变为 “domain”。有关更多信息，请参阅 [更新客户设置](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_customers#update_customer)。

### resellernotify

  - `getwatchdetails` — 返回与经销商相关的所有监控信息。
  - `register` — 注册经销商以接收通知。
  - `unregister` — 取消经销商的订阅通知接收权限。

### 订阅

  - `activate` — 恢复之前被经销商暂停的订阅。如果您没有暂停客户的订阅，而订阅因其他原因（如滥用或待接受的条款和条件）被暂停，此调用将不会恢复客户的订阅。
  - `changePlan` — 更改订阅计划。使用此方法可以将 30 天免费试用计划或灵活计划订阅更改为按月或按年支付的年度订阅计划。计划的具体更新方式取决于计划和产品类型。有关更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#update_subscription_plan) 的说明。
  - `changeRenewalSettings` — 更新用户许可证的续订设置。此功能仅适用于具有年度订阅计划的账户。有关更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#update_renewal) 的说明。
  - `changeSeats` — 更新订阅的用户许可证设置。有关更新年度订阅计划或灵活计划订阅许可证的更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#update_subscription_seat)。
  - `delete` — 取消、暂停或直接转移订阅。
  - `get` — 获取特定订阅信息。您可以使用 [检索所有经销商订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#get_all_subscriptions) 方法获取 `subscriptionId`。有关检索特定订阅的更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#get_subscription) 的说明。
  - `insert` — 创建或转移订阅。您可以使用 [订购新客户账户](https://developers.google.com/workspace/admin/reseller/v1/reference/customers/insert.html) 方法为已订购的客户账户创建订阅。
  - `list` — 列出经销商管理的所有订阅。列表可以包括所有订阅、某个客户的全部订阅，或某个客户可转移的所有订阅。可选地，此方法可以通过 `customerNamePrefix` 对响应进行过滤。有关更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions)。
  - `startPaidService` — 立即将 30 天免费试用订阅转换为付费服务订阅。此方法仅适用于已为 30 天免费试用订阅设置支付计划的订阅。有关更多信息，请参阅 [管理订阅](https://developers.google.com/workspace/admin/reseller/v1/how-tos/manage_subscriptions#paid_service)。
  - `suspend` — 暂停正在运行的订阅。您可以使用此方法暂停当前处于 `ACTIVE` 状态的付费订阅。* 对于 “FLEXIBLE” 类型的订阅，账单会暂停。* 对于 “ANNUAL_MONTHLY_PAY” 或 “ANNUAL_YEARLY_PAY” 类型的订阅：暂停订阅不会更改原本约定的续订日期。* 被暂停的订阅不会自动续订。

## 查看命令

在调用任何 API 方法之前，请先检查其文档：

```bash
# Browse resources and methods
gws reseller --help

# Inspect a method's required params, types, and defaults
gws schema reseller.<resource>.<method>
```

使用 `gws schema` 的输出来构建您的 `--params` 和 `--json` 标志。