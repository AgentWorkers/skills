---
name: send-tokens
description: 将代币发送或转移至任何支持的链（EVM 或 Solana）上的任意地址。适用于您或用户需要转账资金、付款、赠送代币、进行捐赠或将资金转移到其他钱包地址的场景。相关表述包括：“向某个地址发送 10 个 USDC”、“向 0x... 支付”、“将 ETH 转移到...”、“将代币转移到我的另一个钱包”等。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call transferTokens*)", "Bash(fdx call getWalletOverview*)"]
---
# 发送代币

使用 `fdx call transferTokens` 命令将代币从钱包转移到任何支持的 EVM 链路或 Solana 上的任意地址。

## 确认钱包已认证

```bash
fdx status
```

如果钱包尚未认证，请参考 `authenticate` 功能。

## 在发送前检查余额

在发起转账之前，请务必确认钱包内有足够的余额：

```bash
fdx call getWalletOverview --chainKey <chain>
```

## 发送代币

```bash
fdx call transferTokens \
  --chainKey <chain> \
  --recipientAddress <address> \
  --amount <amount>
```

### 参数

| 参数                | 是否必填 | 说明                                                      |
| ------------------------ | -------- | ---------------------------------------------------------------- |
| `--chainKey`             | 是      | 目标区块链（例如 `ethereum`、`polygon`、`base`、`solana`）             |
| `--recipientAddress`     | 是      | 收件人钱包地址                                       |
| `--amount`               | 是      | 要发送的代币数量（人类可读格式，例如 `10`、`0.5`）                |
| `--fromAccountAddress`   | 否       | 来源账户地址（如果钱包拥有多个账户）                         |
| `--tokenAddress`         | 否       | 代币合约地址（对于 ETH 或 SOL 等原生代币可省略）                   |
| `--memo`                 | 否       | 交易备注或说明                                         |
| `--maxPriorityFeePerGas` | 否       | EVM 气体费用优先级设置                                   |
| `--maxFeePerGas`         | 否       | EVM 最大气体费用设置                                   |

## 示例

### 发送原生代币

```bash
# Send 0.1 ETH on Ethereum
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 0.1

# Send 1 SOL on Solana
fdx call transferTokens \
  --chainKey solana \
  --recipientAddress AbCd...1234 \
  --amount 1
```

### 发送 ERC-20 代币

```bash
# Send 100 USDC on Ethereum (specify token contract)
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 100 \
  --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48

# Send 50 USDC on Base
fdx call transferTokens \
  --chainKey base \
  --recipientAddress 0x1234...abcd \
  --amount 50 \
  --tokenAddress 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
```

### 带备注发送代币

```bash
fdx call transferTokens \
  --chainKey ethereum \
  --recipientAddress 0x1234...abcd \
  --amount 10 \
  --tokenAddress 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --memo "Payment for invoice #42"
```

## 流程

1. 使用 `fdx status` 检查认证状态。
2. 使用 `fdx call getWalletOverview --chainKey <chain>` 检查余额。
3. 确认转账详情（包括金额、收款人、区块链和代币类型）。
4. 使用 `fdx call transferTokens` 执行转账。
5. 将交易结果告知相关人员。

**重要提示：** 在执行转账前，请务必确认收款人地址和转账金额，尤其是涉及较大金额时。区块链交易是不可撤销的。

## 先决条件

- 必须完成认证（使用 `fdx status` 检查，详见 `authenticate` 功能）。
- 钱包在目标链路上必须有足够的余额。
- 如果转账金额不足，建议使用 `fund-wallet` 功能补充资金。

## 错误处理

- “未认证” — 先运行 `fdx setup`，或参考 `authenticate` 功能。
- “余额不足” — 使用 `getWalletOverview` 检查余额；如需补充资金，请使用 `fund-wallet` 功能。
- “收款人地址无效” — 确认地址格式是否符合目标链路的格式要求。