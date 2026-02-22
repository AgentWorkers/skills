---
name: clawpay
description: 使用 ClawPay 在 Solana 上发送和接收第三方托管（escrow）支付。您可以支付给其他 AI 代理，将资金锁定在第三方托管账户中，确认服务交付情况，释放支付款项，查看收款记录，并验证代理的信誉。该工具适用于以下场景：需要向代理付款、创建第三方托管账户、从其他代理购买服务、出售服务、查询支付状态或查看交易历史记录。
version: 1.0.0
author: clawpay
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins:
        - python3
        - pip3
    primaryEnv: SOLANA_KEYPAIR_PATH
---
# ClawPay — 用于AI代理的托管支付服务

您可以使用ClawPay在Solana网络上发送和接收无需信任的托管支付。该功能涵盖了整个支付生命周期：锁定资金、确认交付、释放支付以及检查收款记录。

## 设置

首先，检查是否已安装ClawPay：

```bash
pip3 show clawpay
```

如果未安装：

```bash
pip3 install clawpay
```

需要用户的Solana钱包密钥对。请在`SOLANA_KEYPAIR_PATH`环境变量指定的路径中查找密钥对，或者查看以下常见位置：
- `~/wallet.json`
- `~/.config/solana/id.json`
- `~/projects/clawpay/program-keypair.json`

如果未找到密钥对，请让用户提供密钥对，或者使用`solana-keygen new --outfile ~/wallet.json`命令生成一个新的密钥对。

## ClawPay的工作原理

ClawPay是一种基于时间锁定的托管协议。每笔支付都遵循以下流程：

1. **T0 — 锁定**：买家将SOL（Solana网络中的代币）锁定到托管账户中。
2. **T1 — 交付**：卖家必须在截止日期前完成交付，否则资金将自动退还给买家。
3. **T2 — 验证**：买家确认交付情况；如果验证通过，资金将自动释放给卖家。
4. **结算**：98%的资金归卖家所有，1%归ClawPay，1%归推荐人（如果有）。
5. **收款记录**：为双方生成链上的加密收款记录。

代理之间无需相互信任，整个流程由时间节点来确保执行。

## 核心操作

### 向其他代理付款（创建托管）

当需要向代理付款或购买服务时：

```python
from clawpay import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey

keypair = Keypair.from_json(open("KEYPAIR_PATH").read())
client = Client(keypair)

escrow = client.create_escrow(
    seller=Pubkey.from_string("SELLER_PUBKEY"),
    amount_sol=AMOUNT,
    delivery_secs=DELIVERY_TIME,       # seconds until delivery deadline
    verification_secs=VERIFICATION_TIME # seconds for dispute window (min 10)
)
print(f"Escrow created: {escrow.address}")
print(f"Amount: {escrow.amount_sol} SOL")
print(f"Delivery deadline: {escrow.t1}")
print(f"Verification ends: {escrow.t2}")
```

如果未指定默认值：
- `deliverysecs`：600秒（10分钟）
- `verificationsecs`：30秒
- `amount_sol`：请用户确认金额——切勿自行猜测

### 确认交付（作为卖家）

在完成服务后，需要确认交付情况：

```python
from clawpay import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey

keypair = Keypair.from_json(open("KEYPAIR_PATH").read())
client = Client(keypair)

escrow_address = Pubkey.from_string("ESCROW_ADDRESS")
client.confirm_delivery(escrow_address, keypair)
print("Delivery confirmed. Waiting for verification window.")
```

### 释放资金（验证通过后）

验证窗口结束后，任何人都可以触发资金释放：

```python
client.auto_release(Pubkey.from_string("ESCROW_ADDRESS"))
print("Funds released to seller.")
```

### 退款（未按时交付）

如果卖家错过了交付截止日期：

```python
client.auto_refund(Pubkey.from_string("ESCROW_ADDRESS"))
print("Funds refunded to buyer.")
```

### 检查托管状态

```python
escrow = client.get_escrow(Pubkey.from_string("ESCROW_ADDRESS"))
print(f"Status: {escrow.status}")
print(f"Amount: {escrow.amount_sol} SOL")
print(f"Delivered: {escrow.delivered}")
print(f"Released: {escrow.released}")
```

### 查看代理的信誉（通过收款记录）

```python
receipts = client.get_receipts(Pubkey.from_string("AGENT_PUBKEY"))
print(f"Total transactions: {len(receipts)}")
for r in receipts:
    outcome = ["released", "refunded", "disputed"][r.outcome]
    print(f"  #{r.receipt_index}: {r.amount_sol} SOL — {outcome}")
```

## 重要限制

- **最小托管金额**：0.05 SOL
- **最大托管金额**：10.0 SOL
- **最小验证时间**：10秒
- **最大交付期限**：30天
- **费用**：结算时收取2%的费用（ClawPay 1%，推荐人1%）
- **网络**：默认使用Solana Mainnet，也可使用Devnet

## 注意事项

- **务必在确认金额后再创建托管**。
- **在未验证卖家公钥的情况下，切勿发送资金**。
- **创建托管后务必显示托管地址——用户需要该地址**。
- **在尝试释放或退款前，务必检查托管状态**。
- 如果找不到密钥对文件，请询问用户——切勿自行猜测。
- 清晰报告所有错误，尤其是余额不足的错误。
- 在查看代理信誉时，需同时展示成功和失败的交易记录，以确保公平性。

## 验证方式

任何交易完成后，您都可以在Solana Explorer上进行验证：
- 程序地址：https://explorer.solana.com/address/F2nwkN9i2kUDgjfLwHwz2zPBXDxLDFjzmmV4TXT6BWeD
- 交易详情：https://explorer.solana.com/tx/TRANSACTION_SIGNATURE

## 链接

- 官网：https://claw-pay.com
- SDK：https://pypi.org/project/clawpay/
- GitHub仓库：https://github.com/jakemeyer125-design/ClawPay-SDK