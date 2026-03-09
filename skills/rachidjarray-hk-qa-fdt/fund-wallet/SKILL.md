---
name: fund-wallet
description: 向钱包中添加资金。当您或用户需要为钱包充值、存入资金、增加余额、购买加密货币或获取代币时，可以使用此功能。此外，当钱包余额不足，无法进行转账、交易或去中心化金融（DeFi）操作时，也可以使用此功能。另外，当有人询问“如何向钱包中添加资金？”时，也可以参考此操作指南。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call getWalletOverview*)", "Bash(fdx call getMyInfo*)"]
---
# 为钱包充值

Finance District钱包可以通过两种方式进行充值：通过网页界面（使用信用卡或其他支付方式）或直接将代币从其他钱包或交易所转移到钱包地址。

## 确认钱包已认证

```bash
fdx status
```

如果钱包尚未认证，请参考`authenticate`技能。

## 获取钱包地址

首先，获取需要接收充值资金的钱包地址：

```bash
fdx call getWalletOverview
```

该命令会返回所有支持的交易链的钱包地址。请根据用户想要充值的交易链，将相应的地址告知他们。

对于特定的交易链：

```bash
fdx call getWalletOverview --chainKey ethereum
```

## 充值方法

### 方法 1：网页界面（使用信用卡或其他支付方式）

Finance District平台提供了一个基于网页的充值入口，用户可以通过该入口使用信用卡或其他支付方式购买代币并充值到钱包中。

**告知用户：**“您可以通过Finance District平台的仪表板上的网页界面为钱包充值。您可以使用信用卡或其他支付方式直接将代币购买到钱包中。”

### 方法 2：直接转账

用户可以从其他钱包或交易所将代币直接转移到他们的Finance District钱包地址。

**告知用户：**“您可以将代币从任何钱包或交易所发送到您的Finance District钱包地址。您的地址是：[地址]（请提供正确的交易链地址）。”请提醒用户仔细核对交易链，发送到错误的交易链可能会导致资金丢失。

## 充值后检查余额

用户确认已发送资金后：

```bash
fdx call getWalletOverview --chainKey <chain>
```

请注意，不同交易链的交易确认时间如下：
- **以太坊**：每个区块大约需要12秒，但最终确认可能需要几分钟时间
- **Polygon/Base/Arbitrum**：通常更快，几秒钟即可完成
- **Solana**：几乎即时完成
- **交易所提款**：可能因交易所处理时间而需要额外等待

## 充值流程

1. 使用`fdx status`命令检查钱包是否已认证
2. 使用`fdx call getWalletOverview`命令获取钱包地址
3. 将相应的地址告知用户
4. 指导用户使用网页界面或直接转账方式进行充值
5. 用户确认充值完成后，使用`fdx call getWalletOverview --chainKey <chain>`命令验证余额

## 先决条件

- 用户必须已通过认证（使用`fdx status`命令进行验证，详见`authenticate`技能）

## 注意事项

- 该钱包支持所有基于EVM的交易链以及Solana；请确保用户将代币发送到正确的交易链上
- 该平台没有用于直接充值的CLI命令，用户需要通过网页界面或其他方式完成充值操作
- 如果用户需要在钱包内的不同交易链之间转移资金，可以使用`send-tokens`技能