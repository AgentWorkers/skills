---
name: fee-abstraction
description: 在 Celo 平台上，可以使用 ERC-20 标准的代币来支付网络手续费（即“gas fees”）。本文将介绍支持使用的代币种类、相关实现方式以及与哪些钱包的兼容性。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo平台上的费用抽象功能

本文档介绍了Celo平台自带的费用抽象功能，该功能允许用户使用ERC-20代币来支付交易手续费。

## 使用场景

- 使用稳定币（如USDC、USDT、cUSD）支付交易手续费；
- 开发无需使用CELO代币的用户友好型去中心化应用（dApps）；
- 集成MiniPay支付系统；
- 在任何需要使用稳定币作为交易手续费的Celo交易场景中。

## 概述

Celo的费用抽象功能允许用户直接使用ERC-20代币来支付交易手续费，无需借助额外的中间服务（如Account Abstraction、Paymasters或Relay Services）。用户只需在交易对象中添加`feeCurrency`字段即可完成支付。

**来源：** https://docs.celo.org/developer/fee-currency

## 支持的费用货币类型

### 主网（Chain ID：42220）

| 代币          | 代币地址            | 适配器地址            | 作为`feeCurrency`的用途       |
|----------------|------------------|------------------|-------------------------|
| USDC           | 0xcebA9300f2b948710d2653dD7B07f33A8B32118C | 0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B | 作为适配器使用             |
| USDT           | 0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e | 0x0e2a3e05bc9a16f5292a6170456a710cb89c6f72 | 作为适配器使用             |
| cUSD           | 0x765DE816845861e75A25fCA122bb6898B8B1282a |                   | 作为代币直接使用             |
| cEUR           | 0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73 |                   | 作为代币直接使用             |
| cREAL           | 0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787 |                   | 作为代币直接使用             |

### Celo Sepolia测试网（Chain ID：11142220）

| 代币          | 代币地址            | 适配器地址            | 作为`feeCurrency`的用途       |
|----------------|------------------|------------------|-------------------------|
| USDC           | 0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B | 0x4822e58de6f5e485eF90df51C41CE01721331dC0 | 作为适配器使用             |

> **注意**：对于具有6位小数的代币（如USDC、USDT），请使用适配器地址；对于具有18位小数的代币（如cUSD、cEUR、cREAL），请直接使用代币地址。

## 钱包支持情况

| 钱包            | 是否支持费用抽象功能          | 备注                |
|----------------|------------------|----------------------|
| MiniPay         | 完全支持             | Celo原生钱包，推荐用于移动设备       |
| Valora          | 完全支持             | Celo官方钱包             |
| MetaMask         | 不支持             | 使用Ethereum的交易格式，不包含`feeCurrency`字段 |
| Coinbase Wallet    | 不支持             | 使用标准EVM交易格式           |
| 其他EVM钱包       | 不支持             | 需要自定义去中心化应用实现       |

> MetaMask和标准EVM钱包不支持费用抽象功能，因为它们使用的是与Ethereum兼容的交易格式，不包含`feeCurrency`字段。

## 库支持情况

| 库名            | 是否支持费用抽象功能         |                  |
|----------------|------------------|-------------------------|
| viem            | 支持                 | 必须使用viem库才能实现费用抽象       |
| ethers.js         | 不支持                 |
| web3.js         | 不支持                 |

**注意：** 在去中心化应用中实现费用抽象功能时，必须使用`viem`库。

## 基本实现

### 使用`feeCurrency`发送交易

```typescript
import { createWalletClient, custom, parseEther } from "viem";
import { celo } from "viem/chains";

// Use adapter address for USDC (6 decimals)
const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";

const walletClient = createWalletClient({
  chain: celo,
  transport: custom(window.ethereum),
});

const [address] = await walletClient.getAddresses();

const hash = await walletClient.sendTransaction({
  account: address,
  to: "0xRecipientAddress",
  value: parseEther("0.01"),
  feeCurrency: USDC_ADAPTER, // Pay gas in USDC
});

console.log("Transaction hash:", hash);
```

### 以`feeCurrency`为单位估算交易手续费

```typescript
import { createPublicClient, http } from "viem";
import { celo } from "viem/chains";

const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";

const publicClient = createPublicClient({
  chain: celo,
  transport: http("https://forno.celo.org"),
});

// Get gas price in USDC
const priceHex = await publicClient.request({
  method: "eth_gasPrice",
  params: [USDC_ADAPTER],
});

const gasPrice = BigInt(priceHex);
console.log("Gas price in USDC:", gasPrice);
```

### 序列化交易数据（CIP-64格式）

```typescript
import { serializeTransaction } from "viem/celo";
import { parseGwei, parseEther } from "viem";

const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";

const serialized = serializeTransaction({
  chainId: 42220,
  gas: 21000n,
  feeCurrency: USDC_ADAPTER,
  maxFeePerGas: parseGwei("20"),
  maxPriorityFeePerGas: parseGwei("2"),
  nonce: 1,
  to: "0xRecipientAddress",
  value: parseEther("0.01"),
});
```

## 关键概念

### 交易类型

使用`feeCurrency`的交易类型对应的CIP-64代码为`0x7b`（12位小数）。这是Celo特有的交易类型。

### 手续费开销

非CELO代币在转换过程中会产生约50,000单位的额外手续费。

### 适配器与代币地址的区别

- **6位小数的代币（如USDC、USDT）**：必须使用适配器地址；
- **18位小数的代币（如cUSD、cEUR、cREAL）**：可以直接使用代币地址。

Celo内部使用18位小数进行手续费计算，因此适配器会自动处理小数位的转换。

### 查询可用货币

**使用`celocli`命令：**
```bash
celocli network:whitelist --node https://forno.celo.org
```

**使用`FeeCurrencyDirectory`合约：**
```typescript
import { createPublicClient, http } from "viem";
import { celo } from "viem/chains";

const FEE_CURRENCY_DIRECTORY = "0x9212Fb72ae65367A7c887eC4Ad9bE310BAC611BF";

const publicClient = createPublicClient({
  chain: celo,
  transport: http("https://forno.celo.org"),
});

const currencies = await publicClient.readContract({
  address: FEE_CURRENCY_DIRECTORY,
  abi: [{
    name: "getCurrencies",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "address[]" }],
  }],
  functionName: "getCurrencies",
});

console.log("Allowed fee currencies:", currencies);
```

## 限制

1. **钱包依赖性**：仅支持Celo原生钱包（如MiniPay、Valora）或自定义去中心化应用；
2. **库依赖性**：需要`viem`库的支持（`ethers.js`和`web3.js`不支持费用抽象功能）；
3. **手续费开销**：非CELO代币的交易会产生约50,000单位的额外手续费；
4. **余额要求**：用户需要确保拥有足够的`feeCurrency`余额。

## 高级功能：自定义费用货币选择界面

可以开发用户界面，让用户自行选择用于支付手续费的代币：

```tsx
import { useState } from "react";
import { useAccount, useBalance } from "wagmi";
import { celo } from "viem/chains";

const FEE_CURRENCIES = [
  { symbol: "CELO", address: null, adapter: null },
  {
    symbol: "USDC",
    address: "0xcebA9300f2b948710d2653dD7B07f33A8B32118C",
    adapter: "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B",
  },
  {
    symbol: "USDT",
    address: "0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e",
    adapter: "0x0e2a3e05bc9a16f5292a6170456a710cb89c6f72",
  },
  {
    symbol: "cUSD",
    address: "0x765DE816845861e75A25fCA122bb6898B8B1282a",
    adapter: null,
  },
];

interface FeeCurrency {
  symbol: string;
  address: string | null;
  adapter: string | null;
}

function FeeCurrencySelector({
  onSelect,
}: {
  onSelect: (currency: FeeCurrency) => void;
}) {
  const { address } = useAccount();
  const [selected, setSelected] = useState(0);

  const handleChange = (index: number) => {
    setSelected(index);
    onSelect(FEE_CURRENCIES[index]);
  };

  return (
    <div>
      <label>Pay gas with:</label>
      <select
        value={selected}
        onChange={(e) => handleChange(Number(e.target.value))}
      >
        {FEE_CURRENCIES.map((currency, i) => (
          <option key={currency.symbol} value={i}>
            {currency.symbol}
          </option>
        ))}
      </select>
    </div>
  );
}

// Usage in transaction
function useFeeCurrencyTransaction() {
  const [feeCurrency, setFeeCurrency] = useState<FeeCurrency>(FEE_CURRENCIES[0]);

  const getFeeCurrencyAddress = () => {
    if (!feeCurrency.address) return undefined; // CELO native
    return feeCurrency.adapter || feeCurrency.address;
  };

  return { feeCurrency, setFeeCurrency, getFeeCurrencyAddress };
}
```

## 高级功能：服务器端交易处理

可以在服务器端生成使用指定货币的交易，适用于无需支付手续费或由第三方赞助的交易场景：

```typescript
import { createWalletClient, http, parseEther } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { celo } from "viem/chains";

const USDC_ADAPTER = "0x2F25deB3848C207fc8E0c34035B3Ba7fC157602B";

async function buildSponsoredTransaction(
  recipientAddress: `0x${string}`,
  amount: bigint
) {
  // Sponsor account pays gas in USDC
  const sponsorAccount = privateKeyToAccount(
    process.env.SPONSOR_PRIVATE_KEY as `0x${string}`
  );

  const walletClient = createWalletClient({
    account: sponsorAccount,
    chain: celo,
    transport: http("https://forno.celo.org"),
  });

  const hash = await walletClient.sendTransaction({
    to: recipientAddress,
    value: amount,
    feeCurrency: USDC_ADAPTER,
  });

  return hash;
}

// Example: sponsor a user's transaction
async function sponsorUserTransfer() {
  const hash = await buildSponsoredTransaction(
    "0xUserAddress",
    parseEther("1")
  );
  console.log("Sponsored transaction:", hash);
}
```

## 额外资源

- [fee-currencies.md](references/fee-currencies.md)：完整的代币地址和适配器信息；
- [wallet-support.md](references/wallet-support.md)：详细的钱包兼容性指南。