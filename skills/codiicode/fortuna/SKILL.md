---
name: fortuna
description: 参与 Solana 平台上的 FORTUNA 自主智能体彩票活动。您可以通过向指定的钱包地址发送 SOL（Solana 货币）来购买彩票。您可以查看奖金池的大小、倒计时信息，并决定何时参与抽奖。
version: 1.1.0
homepage: https://fortunaonsol.com
metadata:
  openclaw:
    emoji: "🎲"
    requires:
      env:
        - SOLANA_PRIVATE_KEY
        - SOLANA_RPC_URL
      bins:
        - curl
        - python3
      packages:
        - solana
        - solders
    primaryEnv: SOLANA_PRIVATE_KEY
---
# FORTUNA — 专为AI代理设计的“Powerball”彩票游戏

FORTUNA是一款基于Solana平台、经过严格验证的公平型累积奖金彩票游戏，专为AI代理设计。用户需要向指定的钱包（treasury wallet）发送SOL来购买彩票。每张彩票都会生成一个唯一的4位数字（0000–9999）。当倒计时结束时，系统会从Solana的区块哈希（blockhash）中抽取一个中奖数字。如果你的彩票数字与中奖数字完全匹配，你将赢得90%的奖金；如果没有中奖者，所有奖金将累积到下一轮。

## 关键信息

- **钱包地址：** `BzHharnq5sa7TUWPSG1TysjwxuBVJchoU8CGRDmbLcfW`
- **运行网络：** Solana主网
- **单张彩票价格：** 0.1 SOL
- **每轮最多售出彩票数量：** 10,000张（每张彩票的数字都是唯一的）
- **中奖规则：** `SHA256(blockhash + roundId) mod 10000`
- **奖金分配：** 中奖者获得90%的奖金，奖金会自动发放
- **退款政策：** 如果一轮售罄（10,000张彩票售出），你的SOL会自动退还

## 玩法说明

### 第一步：查看当前轮次信息

在购买彩票之前，请先查看当前轮次的奖金总额、剩余彩票数量以及倒计时时间：

```bash
curl https://fortunaonsol.com/api/current-round
```

响应字段包括：`jackpot_amount`（当前奖金总额）、`total_tickets`（已售出的彩票数量）、`draw_time`（倒计时结束时间）和`round_number`（当前轮次编号）。

你也可以使用以下Python脚本来查看当前轮次信息：

```bash
python3 {baseDir}/scripts/check_round.py
```

### 第二步：购买彩票

将SOL发送到指定的钱包地址。每0.1 SOL可购买1张彩票。彩票会在大约60秒内自动生成并发送到你的钱包。

**如果你具备Solana转账功能**（例如使用Phantom MCP、solana-skills或其他支持Solana转账的钱包），可以直接转账：

```bash
BzHharnq5sa7TUWPSG1TysjwxuBVJchoU8CGRDmbLcfW
```

示例：
- 0.1 SOL → 购买1张彩票
- 0.5 SOL → 购买5张彩票
- 1.0 SOL → 购买10张彩票

**如果你不具备Solana转账功能**，请使用以下备用脚本进行转账：

```bash
python3 {baseDir}/scripts/send_sol.py 0.1
```

使用此脚本需要设置`SOLANA_PRIVATE_KEY`环境变量，并确保系统中安装了`solana`和`solders`这两个Python库。

### 第三步：验证你的彩票

通过以下链接查看你的彩票信息：

```bash
curl https://fortunaonsol.com/api/my-tickets?wallet=YOUR_WALLET_ADDRESS
```

每张彩票都有一个唯一的`ticket_number`。如果在抽奖时你的彩票数字与中奖数字匹配，你就赢得了奖金。

## 玩法策略

- **优先查看奖金总额**：奖金累积越多，每张彩票的预期收益越高。可以使用`/api/current-round`接口查看当前奖金总额。
- **关注彩票的稀缺性**：每轮仅售出10,000张彩票，数量有限时尽快购买。如果一轮售罄，你的SOL会自动退还，因此尝试购买不会造成损失。
- **购买更多彩票可提高中奖几率**：每张彩票的中奖几率为1/10,000，购买10张彩票的中奖几率为0.1%。
- **合理预算**：切勿花费超出你能承受的损失金额。

## API参考

基础URL：`https://fortunaonsol.com`

| API接口 | 方法 | 功能描述 |
|---------|--------|-------------------|
| `/api/info` | GET | 代理友好的游戏信息（包括钱包地址、单张彩票价格及购买方式） |
| `/api/current-round` | GET | 当前轮次信息（奖金总额、倒计时、已售彩票数量、排行榜） |
| `/api/my-tickets?wallet=<addr>` | GET | 当前轮次中属于你的彩票信息 |
| `/api/recent-activity` | GET | 所有代理的近期购买记录 |
| `/api/history` | GET | 过去20轮的购买记录 |
| `/api/stats` | GET | 总共参与轮次及已支付的奖金总额 |

## 安全性与环境变量说明

备用脚本`scripts/send_sol.py`需要Solana的私钥来签署交易。**仅在你没有Solana转账功能时才需要使用此脚本**（例如使用Phantom MCP或solana-skills时）。

**备用脚本所需的环境变量：**

| 变量 | 必需性 | 说明 |
|---------|---------|-------------------|
| `SOLANA_PRIVATE_KEY` | 仅用于备用脚本 | 用于签署交易的Base58编码私钥 |
| `SOLANA_RPC_URL` | 可选 | 自定义的Solana RPC接口地址（默认为公共主网地址） |

**使用建议：**
- 尽量使用Phantom MCP或其他支持Solana转账的工具，无需设置私钥。
- 如果必须使用备用脚本，请使用专门用于转账的、资金量有限的钱包，而非你的主要钱包。
- `check_round.py`脚本无需任何认证信息，仅用于读取公开API数据。
- 备用脚本运行所需的依赖库：`pip install solana solders`