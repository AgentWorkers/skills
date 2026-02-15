---
name: qrcoin
description: 在 Base 平台上，您可以与 QR Coin 拍卖功能进行交互。当用户想要参与 qrcoin.fun 的 QR 码拍卖时，可以使用该功能来查看拍卖状态、当前出价情况、创建新的出价，或对现有出价进行补充。QR Coin 允许用户对 QR 码上显示的 URL 进行出价；出价最高者的 URL 会被最终编码并保存在拍卖结果中。
metadata: {"clawdbot":{"emoji":"📱","homepage":"https://qrcoin.fun","requires":{"bins":["curl","jq"]}}}
---

# QR币拍卖

参与基于Base区块链的[QR币](https://qrcoin.fun)拍卖。QR币允许您竞拍在二维码上显示的URL——拍卖结束时，出价最高的URL将被编码到二维码中。

## 合同（Base主网）

| 合同 | 地址 |
|----------|---------|
| QR拍卖 | `0x7309779122069EFa06ef71a45AE0DB55A259A176` |
| USDC | `0x833589fCD6eDb6E08f4c7c32D4f71b54bdA02913` |

## 运作原理

1. 每次拍卖持续固定时间（约24小时）。
2. 投标者使用USDC进行竞拍（货币单位为1000000单位）。
3. 创建新的竞拍报价需要约11.11 USDC（`createBidReserve`函数）。
4. 增加现有竞拍的金额需要约1.00 USDC（`contributeReserve`函数）。
5. 出价最高者获胜；获胜者的URL会被编码到二维码中。
6. 失败者将获得退款；获胜者将获得QR代币。

## 拍卖状态查询

> **注意**：以下示例使用`https://mainnet.base.org`（公共RPC接口）。您可以根据需要替换为自己的RPC端点。

### 获取当前拍卖ID

在竞拍前，请务必先查询当前的活跃拍卖ID。

```bash
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0x7d9f6db5"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n"
```

### 获取拍卖结束时间

```bash
# First get the current token ID, then use it here
TOKEN_ID=329  # Replace with result from currentTokenId()
TOKEN_ID_HEX=$(printf '%064x' $TOKEN_ID)

curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0xa4d0a17e'"$TOKEN_ID_HEX"'"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n"
```

### 获取保留价格

```bash
# Create bid reserve (~11.11 USDC)
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0x5b3bec22"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n" | awk '{print $1/1000000 " USDC"}'

# Contribute reserve (~1.00 USDC)
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0xda5a5cf3"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n" | awk '{print $1/1000000 " USDC"}'
```

## 通过Bankr进行交易

QR币拍卖需要使用Base区块链上的USDC交易。请使用Bankr来执行这些交易——Bankr负责：
- 函数签名解析和参数编码
- 交易费用估算
- 交易签名和提交
- 交易确认监控

### 第1步：批准USDC（一次性操作）

在竞拍前，需要先批准拍卖合同以使用USDC：

```
Approve 50 USDC to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base
```

### 第2步：创建新的竞拍报价

要为您的URL创建一个新的竞拍报价，请使用以下函数：
**函数**：`createBid(uint256 tokenId, string url, string name)`
**合同**：`0x7309779122069EFa06ef71a45AE0DB55A259A176`
**费用**：约11.11 USDC

> **重要提示**：请务必先使用`currentTokenId()`函数获取当前的活跃拍卖ID。

**Bankr使用示例**：
```
Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base
calling createBid(329, "https://example.com", "MyName")
```

### 第3步：增加现有竞拍的金额

要为现有URL的竞拍增加金额，请使用以下函数：
**函数**：`contributeToBid(uint256 tokenId, string url, string name)`
**合同**：`0x7309779122069EFa06ef71a45AE0DB55A259A176`
**费用**：每次增加约1.00 USDC

**Bankr使用示例**：
```
Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base
calling contributeToBid(329, "https://grokipedia.com/page/debtreliefbot", "MerkleMoltBot")
```

## 函数选择器

| 函数 | 选择器 | 参数 |
|----------|----------|------------|
| `currentTokenId()` | `0x7d9f6db5` | — |
| `auctionEndTime(uint256)` | `0xa4d0a17e` | auctionId |
| `createBidReserve()` | `0x5b3bec22` | — |
| `contributeReserve()` | `0xda5a5cf3` | — |
| `createBid(uint256,string,string)` | `0xf7842286` | auctionId, url, name |
| `contributeToBid(uint256,string,string)` | `0x7ce28d02` | auctionId, url, name |
| `approve(address,uint256)` | `0x095ea7b3` | spender, amount |

## 错误代码

| 错误代码 | 含义 | 解决方案 |
|-------|---------|----------|
| `RESERVE_PRICE_NOT_MET` | 投标金额低于最低要求 | 请检查保留价格 |
| `URL_ALREADYHAS_BID` | 该URL已有竞拍报价 | 请使用`contributeToBid`函数 |
| `BID_NOT_FOUND` | 该URL没有竞拍报价 | 请使用`createBid`函数 |
| `AUCTION_OVER` | 当前拍卖已结束 | 请等待下一次拍卖 |
| `AUCTION_NOT_STARTED` | 拍卖尚未开始 | 请等待拍卖开始 |
| `INSUFFICIENT_ALLOWANCE` | USDC未获批准 | 请先批准USDC |

## 典型工作流程

1. **查询`currentTokenId()`** — 获取当前的活跃拍卖ID。
2. **检查拍卖状态** — 查看剩余时间。
3. **批准USDC** — 为拍卖合同进行一次性批准。
4. **决定操作**：
   - **新URL**：使用`createBid`函数（费用约11.11 USDC）。
   - **支持现有URL**：使用`contributeToBid`函数（费用约1.00 USDC）。
5. **监控** — 关注是否有更高的出价；如有需要可追加投注。
6. **领取奖励**：获胜者获得QR代币；失败者获得退款。

## 链接

- **平台**：https://qrcoin.fun
- **拍卖合同**：[BaseScan](https://basescan.org/address/0x7309779122069EFa06ef71a45AE0DB55A259A176)
- **Base区块链上的USDC**：[BaseScan](https://basescan.org/token/0x833589fCD6eDb6E08f4c7c32D4f71b54bdA02913)

## 提示

- **从小额开始**：可以先尝试为现有竞拍增加少量资金（约1 USDC），熟悉操作流程。
- **注意时间**：拍卖有固定的结束时间，请做好计划。
- **关注竞拍情况**：其他人可能会出更高的价，请密切关注拍卖进程。
- **使用Bankr**：让Bankr处理交易签名和执行。
- **指定区块链**：使用Bankr时请务必注明“在Base区块链上”。

---

**💡 专业提示**：为现有竞拍增加金额比创建新的竞拍报价更经济。在创建新竞拍报价之前，请先查看是否已有其他人对该URL进行过竞拍。