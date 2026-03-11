---
name: Crypto Wallet
description: 发现支持的加密货币，生成存款地址，并将加密货币提取到外部钱包中。
version: 1.0.0
---
# 加密钱包

当用户需要将加密货币存入钱包或提取到外部地址时，请使用此功能。

## 可用工具

- `get_coins` — 列出所有支持的加密货币 | `GET /api/v1/wallet/coins` | 需要身份验证
- `get_coin_networks` — 获取特定加密货币支持的区块链网络列表 | `GET /api/v1/wallet/coins/:coin_id/networks` | 需要身份验证
- `getdeposit_address` — 生成或检索特定网络上的加密货币存款地址 | `POST /api/v1/wallet/deposit/address` | 需要身份验证
- `get_withdraw_quote` — 获取加密货币提取的报价（费用、限额等信息） | `POST /api/v1/wallet/withdraw/quote` | 需要身份验证
- `initiate_withdraw` — 开始将加密货币提取到外部地址 | `POST /api/v1/wallet/withdraw` | 需要身份验证
- `get_withdraw_status` — 查看加密货币提取的状态 | `GET /api/v1/wallet/withdraw/:id` | 需要身份验证
- `confirm_withdraw` — 确认待处理的加密货币提取请求 | `POST /api/v1/wallet/withdraw/:id/confirm` | 需要交易PIN码

## 推荐操作流程

### 存入加密货币

1. 列出可支持的加密货币：`GET /api/v1/wallet/coins` — 查找您想要存入的加密货币
2. 选择区块链网络：`GET /api/v1/wallet/coins/:coin_id/networks` — 选择目标区块链网络
3. 生成存款地址：`POST /api/v1/wallet/deposit/address`（提供 `coin_id` 和 `network_id`）—— 返回存款地址
4. 从外部钱包将加密货币发送到生成的地址

### 提取加密货币

1. 获取提取报价：`POST /api/v1/wallet/withdraw/quote`（提供 `coin_id`、`network_id`、`金额` 和 `目标地址`）
2. 开始提取：`POST /api/v1/wallet/withdraw`（使用提取报价信息）
3. 确认提取请求：`POST /api/v1/wallet/withdraw/:id/confirm`（需要输入交易PIN码）
4. 查看提取进度：`GET /api/v1/wallet/withdraw/:id` — 监控提取进度直至完成

## 注意事项

- 存入前务必确认目标区块链网络正确，否则可能导致资金损失
- 提取操作需先获取报价，再确认；确认步骤需要输入交易PIN码
- 存款地址是固定的——相同的加密货币和网络组合总是返回相同的地址

## 代理操作指南

执行此功能时，请遵循以下指导：

- 严格按照文档中的操作流程进行，不要跳过任何步骤。
- 如果某个工具需要身份验证，请确保会话中包含有效的令牌。
- 如果工具需要交易PIN码，请每次操作时都向用户索取新的PIN码，切勿缓存或记录PIN码。
- 绝不要泄露、记录或存储任何敏感信息（如密码、令牌、完整卡号、CVV码）。
- 如果用户请求超出此功能范围的操作，请拒绝并推荐相应的功能。
- 如果某步骤失败，请查看错误信息并按照提示进行恢复操作后再重试。
- 在生成存款地址前，务必确认用户选择了正确的区块链网络；发送到错误的网络会导致资金永久丢失。
- 提取操作流程为：获取报价 → 开始提取 → 使用交易PIN码确认；确认步骤必须输入4位数的交易PIN码，切勿跳过报价步骤。
- 存款地址是固定的——相同的加密货币和网络组合总是返回相同的地址。