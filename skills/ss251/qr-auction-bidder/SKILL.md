---
name: qr-auction-bidder
description: 在 qrcoin.fun 上参与 $QR 拍卖。使用 USDC 在 Base 主网上进行出价。交易执行由 Bankr 负责完成——无需管理钱包。
metadata:
  openclaw:
    emoji: "🎯"
    requires: []
---

# QR拍卖竞拍工具

您可以每天参与$QR平台的拍卖活动。在每次拍卖中，您可以使用USDC进行出价，以赢得一个QR码。该QR码会在24小时内指向您指定的URL。

## 概述

$QR平台在Base主网上持续进行24小时的拍卖。出价最高的人将赢得拍卖，获胜的URL会以实体QR码的形式展示。未中标者的出价会自动退还。

- **官方网站**：https://qrcoin.fun  
- **网络**：Base主网（链ID：8453）  
- **货币**：USDC（6位小数）  
- **社区**：m/qr（位于moltbook.com）  
- **交易执行**：使用[Bankr](https://bankr.bot)——请从https://github.com/BankrBot/moltbot-skills安装`bankr`技能  

## 合同地址

| 合同 | 地址          |
|--------|--------------|
| QRAuctionV5 | `0x7309779122069EFa06ef71a45AE0DB55A259A176` |
| USDC（Base） | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## 最低出价要求

| 操作     | 最低出价        |
|--------|--------------|
| 创建新出价（`createBid`） | 11.11 USDC       |
| 增加现有出价（`contributeToBid`） | 1.00 USDC       |

## 拍卖流程

1. 上一次拍卖结束后，系统会自动开始新的拍卖。
2. 每次拍卖都有一个`tokenId`、`startTime`和`endTime`（通常为24小时）。
3. 投标者可以通过`createBid()`为某个URL出价，或者通过`contributeToBid()`为现有出价增加USDC。
4. 拍卖结束时，出价最高者获胜；如果最后5分钟内获胜URL发生变化，拍卖时间会延长5分钟（最长延长至原结束时间的3小时后）。**注意**：为已获胜的URL增加出价不会触发时间延长。
5. 拍卖结束后，系统会结算并退还未中标者的出价。

## 先决条件

此工具使用**Bankr**来执行链上交易。请先安装`bankr`技能：

```
https://github.com/BankrBot/moltbot-skills
```

Bankr负责钱包创建、USDC的授权、交易签名、费用估算和确认。无需设置私钥或钱包信息。

## 查看拍卖状态

您可以通过RPC查询当前的拍卖状态：

```bash
# Get current auction state (tokenId, highestBid, startTime, endTime, settled)
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0xe4b8f0de"},"latest"],"id":1}' \
  | jq -r '.result'
```

`auction()`函数（选择器`0xe4b8f0de`）会返回完整的拍卖信息，包括`tokenId`、`highestBid`、`startTime`、`endTime`和`qrMetadata`。

```bash
# Get number of bids in current auction
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0x91a3823f"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n"
```

```bash
# Get create bid reserve price (should return 11110000 = 11.11 USDC)
curl -s -X POST https://mainnet.base.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0x7309779122069EFa06ef71a45AE0DB55A259A176","data":"0x4b6014f6"},"latest"],"id":1}' \
  | jq -r '.result' | xargs printf "%d\n"
```

## 使用Bankr进行出价

### 第一步：授权使用USDC

在出价之前，请先授权拍卖合约以使用您的USDC。合约会使用您账户中的全部余额作为出价金额，因此请确保设置的授权金额与您的出价一致。

```
Approve 15 USDC to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base
```

或者通过Bankr脚本进行授权：

```bash
scripts/bankr.sh "Approve 15 USDC to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base"
```

### 第二步：创建新出价

如果您的URL尚未有人出价，可以使用`createBid`函数创建新出价。请先通过`auction()`函数获取当前的`tokenId`。

**函数**：`createBid(uint256 _tokenId, string _urlString, string _name)`  

```
Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base calling createBid(329, "https://your-url.com", "YourName")
```

或者通过Bankr脚本进行授权：

```bash
scripts/bankr.sh 'Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base calling createBid(329, "https://your-url.com", "YourName")'
```

> **重要提示**：请将`329`替换为实际的`tokenId`。使用错误的token ID会导致操作失败（错误代码：`INVALID_TOKEN_ID`）。

### 第三步：增加现有出价

如果您的URL已有出价，可以使用`contributeToBid`函数增加出价：

**函数**：`contributeToBid(uint256 _tokenId, string _urlString, string _name)`  

```
Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base calling contributeToBid(329, "https://existing-url.com", "YourName")
```

或者通过Bankr脚本进行授权：

```bash
scripts/bankr.sh 'Send transaction to 0x7309779122069EFa06ef71a45AE0DB55A259A176 on Base calling contributeToBid(329, "https://existing-url.com", "YourName")'
```

### 出价选择：

- 如果您的URL尚未有人出价 → 使用`createBid`（最低出价：11.11 USDC）
- 如果您的URL已有出价 → 使用`contributeToBid`（最低出价：1.00 USDC）
- 如果尝试为已有出价的URL使用`createBid`，系统会返回错误`URL_ALREADYHAS_BID`。
- 如果尝试为无出价的URL使用`contributeToBid`，系统会返回错误`BID_NOT_FOUND`。

## 拍卖时间设置

| 参数          | 值            |
|----------------|-----------------|
| 持续时间       | 24小时           |
| 时间缓冲区       | 如果最后5分钟内出现新获胜URL，则拍卖时间延长5分钟 |
| 最大延长时间     | 最长延长至原结束时间的3小时后 |

## 重要提示：

- **USDC为真实货币**。请确保您出价的金额在您的承受范围内。
- 拍卖结束后，未中标者的出价会自动退还，但可能存在处理延迟。
- 合同会使用您账户中的全部余额作为出价金额，请确保设置的授权金额与您的出价一致。
- 每个URL在每次拍卖中必须是唯一的。如果有人已经为该URL出价，请使用`contributeToBid`。
- 请确保使用的token ID与当前拍卖的`tokenId`匹配。使用错误的token ID会导致操作失败（错误代码：`INVALID_TOKEN_ID`）。

## 错误代码

| 错误代码 | 错误原因 | 解决方案            |
|-----------|-----------------|-------------------|
| `INVALID_TOKEN_ID` | 使用错误的拍卖token ID | 请通过`auction()`获取当前的`tokenId`。 |
| `AUCTION_OVER` | 拍卖已经结束 | 请等待下一次拍卖。         |
| `RESERVE_PRICE_NOT_MET` | 出价低于最低要求 | 请至少出价11.11 USDC（创建新出价）或1.00 USDC（增加现有出价）。 |
| `URL_ALREADYHAS_BID` | 该URL已有出价 | 请使用`contributeToBid`。     |
| `BID_NOT_FOUND` | 该URL没有出价 | 请使用`createBid`。         |
| `AUCTION_SETTLED` | 拍卖已经结束 | 请等待下一次拍卖。         |

## ABI参考

QRAuctionV5的完整ABI文件位于此技能包的`references/QRAuctionV5.abi.json`中。

**主要函数**：

| 函数        | 描述                          |
|-------------|--------------------------------------|
| `auction()`     | 获取当前拍卖状态（tokenId, highestBid, startTime, endTime, settled） |
| getAllBids()   | 获取当前拍卖的所有出价信息             |
| getBid(url)     | 获取指定URL的出价信息                   |
| getBidCount()    | 获取当前拍卖中的出价数量                 |
| createBid(tokenId, url, name) | 为指定URL创建新出价                   |
| contributeToBid(tokenId, url, name) | 为现有出价增加金额                   |
| createBidReservePrice() | 获取新出价的最低要求                 |
| contributeBidReservePrice() | 获取增加出价的最低要求                 |

**主要事件**：

| 事件         | 描述                          |
|-------------|--------------------------------------|
| AuctionBid     | 创建新的出价                         |
| BidContributionMade | 为现有出价增加金额                     |
| AuctionSettled   | 拍卖结束，确定获胜者                   |
| AuctionCreated | 新拍卖开始                         |

## 典型工作流程：

1. **查看拍卖状态**：通过`auction()`获取当前的`tokenId`和剩余时间。
2. **查看现有出价**：通过`getAllBids()`或`getBid(url)`查看已有出价情况。
3. **授权使用USDC**：通过Bankr设置出价金额。
4. **进行出价**：为新的URL使用`createBid`，或为现有URL使用`contributeToBid`。
5. **监控出价**：关注出价情况，必要时增加出价。
6. **结算**：拍卖结束后，未中标者的出价会自动退还。

## 相关链接：

- **平台**：https://qrcoin.fun  
- **关于/文档**：https://qrcoin.fun/about  
- **拍卖合约**：https://basescan.org/address/0x7309779122069EFa06ef71a45AE0DB55A259A176  
- **Bankr技能**：https://github.com/BankrBot/moltbot-skills  
- **社区**：m/qr（位于moltbook.com）