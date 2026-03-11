---
name: Card Management
description: 通过 MasterPay Global 创建和管理虚拟卡片。支持一次性购买的单次使用卡片，以及可重复使用的多用途卡片。
version: 1.0.0
---
# 卡片管理

当用户需要创建虚拟卡片、查看卡片详情或管理卡片生命周期（锁定、解锁、取消）时，请使用此技能。

## 可用工具

- `list_card_wallets` — 列出所有 MasterPay 卡片钱包及其余额（创建卡片前必须使用） | `GET /api/v1/masterpay/wallets` | 需要身份验证
- `create_single_use_card` — 为一次性购买创建单次使用的虚拟卡片 | `POST /api/v1/masterpay/cards/single-use` | 需要身份验证
- `create_multi_use_card` — 为多次购买创建多用途虚拟卡片 | `POST /api/v1/masterpay/cards/multi-use` | 需要身份验证
- `list_cards` — 列出钱包中的所有卡片（默认为第一个钱包） | `GET /api/v1/masterpay/wallets/cards` | 需要身份验证
- `list_cards_by_wallet` — 列出特定钱包 UUID 的卡片 | `GET /api/v1/masterpay/wallets/:wallet_uuid/cards` | 需要身份验证
- `get_card` — 根据 UUID 获取特定卡片的详细信息（包括卡片 ATM PIN，无需交易 PIN） | `GET /api/v1/masterpay/cards/:id` | 需要身份验证
- `get_card_details` — 获取完整的未屏蔽卡片号码、CVV 和有效期（敏感信息） | `POST /api/v1/masterpay/cards/:id/details` | 需要交易 PIN
- `get_card_types` — 获取可用的卡片类型及其属性 | `GET /api/v1/masterpay/cards/types` | 需要身份验证
- `lock_card` — 锁定卡片以防止交易 | `POST /api/v1/masterpay/cards/:id/lock` | 需要身份验证 | 需要交易 PIN
- `unlock_card` — 解锁之前被锁定的卡片 | `POST /api/v1/masterpay/cards/:id/unlock` | 需要身份验证 | 需要交易 PIN
- `cancel_card` — 永久取消（暂停）卡片 | `POST /api/v1/masterpay/cards/:id/cancel` | 需要身份验证 | 需要交易 PIN
- `list_applied_cards` — 列出所有卡片申请及其状态 | `GET /api/v1/cards` | 需要身份验证
- `get_applied_card` — 获取特定卡片申请的详细信息 | `GET /api/v1/cards/:id` | 需要身份验证
- `apply_card` — 申请新的支付卡片（实体卡或虚拟卡） | `POST /api/v1/cards/apply` | 需要身份验证

## 推荐流程

### 创建虚拟卡片（MasterPay）

通过 MasterPay 创建单次使用或多用途的虚拟卡片：

1. 检查 KYC 状态：`GET /api/v1/masterpay/kyc/status` — 状态必须为“已批准”（可使用 `kyc-identity` 技能中的 `get_kyc_status` 功能）
2. 列出钱包：`GET /api/v1/masterpay/wallets` — 确认至少存在一个钱包（如果没有钱包，则表示 KYC 尚未批准）
3. 创建卡片：`POST /api/v1/masterpay/cards/single-use` 或 `POST /api/v1/masterpay/cards/multi-use` — 返回屏蔽后的 PAN 号码和卡片 ATM PIN
4. 获取完整详细信息：`POST /api/v1/masterpay/cards/:id/details`（需要交易 PIN） — 返回完整的卡片号码和 CVV

### 申请卡片

通过卡片申请流程申请新的实体卡或虚拟卡：

1. 获取卡片类型：`GET /api/v1/masterpay/cards/types` — 查看可用的类型（银卡、金卡、钛金卡、混合金属卡、数字虚拟卡、数字虚拟 2）
2. 申请：`POST /api/v1/cards/apply`，并提供 `card_type`、`delivery_method`、`full_name`、`phone_number`、`email`、`address` 等信息
3. 查看申请状态：`GET /api/v1/cards/:id`

## 规则

- 在创建任何 MasterPay 卡片之前，必须先完成 KYC 审核。如果 KYC 未完成，创建卡片会失败（返回错误代码 `NO_WALLETS`）。
- MasterPay 卡片的响应中包含屏蔽后的 PAN 号码和卡片 ATM PIN；如需获取完整的卡片号码和 CVV，请使用 `GET /api/v1/masterpay/cards/:id/details` 并提供交易 PIN。
- 卡片 ATM PIN（在 `get_card`、`list_cards` 和卡片创建响应中显示）仅用于 ATM/POS 交易；它与用于敏感操作的交易 PIN 不同。
- 锁定/解锁/取消操作都需要验证交易 PIN。
- 已取消的卡片无法重新激活；取消操作是不可逆的。
- 申请卡片时需要提供卡片类型（银卡/金卡/钛金卡/混合金属卡/数字虚拟卡/数字虚拟 2）和配送方式（现场领取/邮寄）。
- 申请卡片（`POST /api/v1/cards/apply`）用于订购新卡片；如需立即创建虚拟卡片，请使用 `POST /api/v1/masterpay/cards/single-use` 或 `POST /api/v1/masterpay/cards/multi-use`。

## 代理操作指南

执行此技能时，请遵循以下说明：

- 始终按照文档中规定的流程顺序操作，不要跳过任何步骤。
- 如果某个工具需要身份验证，请确保会话中具有有效的承载令牌（bearer token）。
- 如果某个工具需要交易 PIN，请每次都向用户索取新的 PIN；切勿缓存或记录 PIN。
- 绝不要泄露、记录或保存任何敏感信息（密码、令牌、完整卡片号码、CVV）。
- 如果用户请求超出此技能范围的操作，请拒绝请求并建议使用相应的技能。
- 如果某一步骤失败，请检查错误信息，并按照下面的恢复指南尝试重新操作。

- 在创建任何 MasterPay 卡片之前，必须先完成 KYC 审核。使用 `kyc-identity` 技能中的 `get_kyc_status` 功能进行验证，然后使用 `list_card_wallets` 确认钱包是否存在。如果没有钱包，则表示 KYC 尚未批准。
- MasterPay 卡片的响应（创建、`get_card`、`list_cards`）中包含卡片 ATM PIN；查看这些信息无需交易 PIN。
- 要获取完整的未屏蔽卡片号码和 CVV，请使用用户的交易 PIN 调用 `get_card_details`。这是获取完整 PAN 号码和 CVV 的唯一方法。
- 卡片 ATM PIN（用于 ATM/POS 交易）与交易 PIN（用于查看卡片详细信息、锁定、解锁或取消等敏感操作的 PIN）不同。
- 锁定、解锁和取消操作都需要验证交易 PIN。
- 已取消的卡片无法重新激活；在取消操作前请务必与用户确认。