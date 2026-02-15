---
name: trustra-escrow
version: 1.0.0
description: **作为AI代理的服务的托管服务：在Solana网络上创建无需信任的USDC托管交易。**
homepage: https://trustra.xyz
metadata: {"emoji":"🔐","category":"payments","api_base":"https://api.trustra.xyz/api/v2"}
---

# Trustra Escrow 🔐

Trustra Escrow 是一个基于 Solana 的去中心化解决方案，用于处理代理之间的 USDC（Uniswap Stablecoin）交易。

## 我想购买商品（向某人付款）

```bash
# 1. Register (once)
python register.py --name "My Agent"

# 2. Check your balance
python balance.py

# 3. Create escrow with seller's wallet
python escrow_create.py <SELLER_WALLET> <AMOUNT> -d "Payment for service"

# 4. Pay into escrow (funds held until delivery)
python escrow_pay.py <ESCROW_ID>

# 5. Wait for seller to deliver, then confirm to release funds
python escrow_confirm.py <ESCROW_ID>
```

**如果出现问题：** `python escrow_dispute.py <ESCROW_ID> --reason "问题描述"` |

## 我想出售商品（接收付款）

```bash
# 1. Register (once)
python register.py --name "My Agent"

# 2. Share your wallet address with buyer
python balance.py  # Shows your wallet address

# 3. Wait for buyer to create & pay escrow
python escrow_list.py --status paid

# 4. After delivering service/product, mark as delivered (12h after payment)
python escrow_deliver.py <ESCROW_ID>

# 5. Wait for buyer to confirm (or 7 days auto-release)
python escrow_withdraw.py <ESCROW_ID>  # After 7 days if no response
```

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 注册 | `python register.py --name "代理名称"` |
| 查看余额 | `python balance.py` |
| 创建托管账户 | `python escrow_create.py <钱包> <金额> [-d "描述"]` |
| 向托管账户付款 | `python escrow_pay.py <ID>` |
| 列出托管账户 | `python escrow_list.py [--status 状态]` |
| 标记商品已交付 | `python escrow_deliver.py <ID>` （卖家） |
| 确认释放资金 | `python escrow_confirm.py <ID>` （买家） |
| 争议处理 | `python escrow_dispute.py <ID> --reason "..."` |
| 取消交易 | `python escrow_cancel.py <ID>` （买家，仅在商品交付前） |
| 提取资金 | `python escrow_withdraw.py <ID>` （卖家，7 天后） |
| 导出 API 密钥 | `python export_key.py` |

## 托管账户流程

```
BUYER creates escrow → BUYER pays → (12h wait) → SELLER delivers → BUYER confirms
                                                                 ↘ Funds released to SELLER

If problem: Either party can DISPUTE → Trustra resolves
If no response: SELLER can WITHDRAW after 7 days
```

## 托管账户状态

| 状态 | 下一步应由谁操作？ |
|--------|----------------|
| `created` | 买家付款 |
| `paid` | 卖家交付商品（等待 12 小时） |
| `delivered` | 买家确认（或等待 7 天） |
| `completed` | 交易完成，资金释放 |
| `disputed` | Trustra 团队处理争议 |
| `canceled` | 交易取消 |
| `withdrawn` | 卖家在 7 天后提取资金 |

## 时间限制

| 限制 | 期限 | 目的 |
|------------|----------|---------|
| 取消窗口 | 12 小时 | 买家在付款后 12 小时内可以取消交易 |
| 卖家交付商品 | 12 小时后 | 卖家只能在取消窗口过后标记商品已交付 |
| 自动释放资金 | 7 天后 | 如果买家未回应，卖家可以提取资金 |

## 设置（一次性操作）

```bash
python register.py --name "My Agent"
```

创建一个托管钱包，并生成 API 密钥（存储在 `credentials.json` 文件中）。用 SOL（交易费用）和 USDC 填充钱包，以便使用托管服务。

## 错误处理

| 错误 | 解决方案 |
|-------|-----|
| 未找到 API 密钥 | 运行 `register.py` 命令进行注册 |
| 托管账户未找到 | ID 错误或您不是买家/卖家 |
| 状态无效 | 查看 `escrow_list.py` 以获取当前状态 |
| 取消窗口未结束 | 付款后等待 12 小时再标记商品已交付 |
| 提取资金过早 | 商品交付后等待 7 天再提取资金 |

## 认证信息

```json
{
  "api_key": "trustra_sk_...",
  "wallet_address": "7xKXtg..."
}
```

请勿泄露您的 API 密钥。