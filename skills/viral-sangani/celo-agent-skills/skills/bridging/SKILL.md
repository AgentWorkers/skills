---
name: bridging
description: 将资产在 Celo 与其他区块链（如 Ethereum）之间进行桥接。适用于在 Celo 与其他区块链之间传输代币的场景。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# 连接 Celo

本技能涵盖了在 Celo 与其他区块链之间桥接资产的方法，包括原生桥接方案和第三方解决方案。

## 使用场景

- 将资产从以太坊转移到 Celo
- 将代币从 Celo 桥接到其他区块链
- 集成跨链功能
- 构建多链应用程序

## 桥接选项

### 原生桥接

| 桥接方式 | 主网 | 测试网 |
|--------|---------|---------|
| Superbridge | https://superbridge.app/celo | https://testnets.superbridge.app |

原生桥接通过 OP Stack 标准桥接方式，实现 Celo L2 与以太坊 L1 之间的直接转账。

来源：https://docs.celo.org/tooling/bridges

### 第三方桥接

| 桥接方式 | URL | 描述 |
|--------|-----|-------------|
| Squid Router V2 | https://v2.app.squidrouter.com | 通过 Axelar 实现跨链路由 |
| LayerZero | https://layerzero.network | 提供跨链互操作性协议 |
| Jumper Exchange | https://jumper.exchange | 多链去中心化交易所聚合器 |
| Portal (Wormhole) | https://portalbridge.com | 提供去中心化互操作性服务 |
| AllBridge | https://app.allbridge.io/bridge | 支持 EVM 和非 EVM 链路 |
| Satellite (Axelar) | https://satellite.money | Axelar 网络桥接工具 |
| Transporter (CCIP) | https://www.transporter.io | Chainlink 的 CCIP 桥接服务 |
| Layerswap | https://layerswap.io/app | 支持 60 多个区块链和 15 多个去中心化交易所 |
| Hyperlane Nexus | https://www.usenexus.org | 提供消息传递和互操作性服务 |
| Mach Exchange | https://www.mach.exchange | 跨链交易服务 |
| Galaxy | https://galaxy.exchange/swap | Celo 上的原生去中心化交易所 |
| SmolRefuel | https://smolrefuel.com | 提供无需支付 gas 的资产转移服务 |
| USDT0 | https://usdt0.to | 通过 LayerZero 提供原生 USDT 转换服务 |

来源：https://docs.celo.org/home/bridged-tokens/bridges

## 原生 ETH 桥接

可以将以太坊的 ETH 转换为 Celo 的 WETH。

### 合同地址

**以太坊主网 → Celo:**

| 合同 | 地址 |
|----------|---------|
| SuperBridgeETHWrapper (L1) | 0x3bC7C4f8Afe7C8d514c9d4a3A42fb8176BE33c1e |
| L1 Standard Bridge | 0x9C4955b92F34148dbcfDCD82e9c9eCe5CF2badfe |
| L1 WETH | 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 |
| L2 WETH (Celo) | 0xD221812de1BD094f35587EE8E174B07B6167D9Af |

**Sepolia 测试网 → Celo Sepolia:**

| 合同 | 地址 |
|----------|---------|
| SuperBridgeETHWrapper (L1) | 0x523e358dFd0c4e98F3401DAc7b1879445d377e37 |
| L1 Standard Bridge | 0xec18a3c30131a0db4246e785355fbc16e2eaf408 |
| L1 WETH | 0x7b79995e5f793A07Bc00c21412e50Ecae098E7f9 |
| L2 WETH (Celo Sepolia) | 0x2cE73DC897A3E10b3FF3F86470847c36ddB735cf |

### 将 ETH 桥接到 Celo

```typescript
import { createWalletClient, custom, parseEther } from "viem";
import { mainnet } from "viem/chains";

const SUPERBRIDGE_WRAPPER = "0x3bC7C4f8Afe7C8d514c9d4a3A42fb8176BE33c1e";

const WRAPPER_ABI = [
  {
    name: "wrapAndBridge",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_minGasLimit", type: "uint32" },
      { name: "_extraData", type: "bytes" },
    ],
    outputs: [],
  },
] as const;

async function bridgeETHToCelo(amount: string): Promise<string> {
  const walletClient = createWalletClient({
    chain: mainnet,
    transport: custom(window.ethereum),
  });

  const [address] = await walletClient.getAddresses();

  const hash = await walletClient.writeContract({
    address: SUPERBRIDGE_WRAPPER,
    abi: WRAPPER_ABI,
    functionName: "wrapAndBridge",
    args: [200000, "0x"],
    value: parseEther(amount),
  });

  return hash;
}
```

## 可通过原生桥接转移的代币

以下代币可以通过原生桥接方式从以太坊转移到 Celo：

| 代币 | 以太坊地址 (L1) | Celo 地址 (L2) |
|-------|----------------------|-------------------|
| WETH | 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 | 0xD221812de1BD094f35587EE8E174B07B6167D9Af |
| WBTC | 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599 | 0x8aC2901Dd8A1F17a1A4768A6bA4C3751e3995B2D |
| DAI | 0x6B175474E89094C44Da98b954EedeAC495271d0F | 0xac177de2439bd0c7659c61f373dbf247d1f41abe |
| AAVE | 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 | 0xF6A54aff8c97f7AF3CC86dbaeE88aF6a7AaB6288 |
| LINK | 0x514910771af9ca656af840dff83e8264ecf986ca | 0xf630876008a4ed9249fb4cac978ba16827f52e91 |
| UNI | 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 | 0xeE571697998ec64e32B57D754D700c4dda2f2a0e |
| CRV | 0xD533a949740bb3306d119CC777fa900bA034cd52 | 0x75184c282e55a7393053f0b8F4F3E7BeAE067fdC |
| rETH | 0xae78736cd615f374d3085123a210448e74fc6393 | 0x55f3d16e6bd2b8b8e6599df6ef4593ce9dcae9 |

来源：https://docs.celo.org/home/bridged-tokens

## 跨链消息传递协议

用于构建跨链去中心化应用程序：

| 协议 | URL | Celo 支持情况 |
|----------|-----|--------------|
| Chainlink CCIP | https://chain.link/cross-chain | 支持主网 |
| Hyperlane | https://www.hyperlane.xyz | 支持主网和 Sepolia |
| Wormhole | https://wormhole.com | 支持主网 |
| LayerZero | https://layerzero.network | 支持主网 |
| Axelar Network | https://axelar.network | 支持主网 |

来源：https://docs.celo.org/tooling/bridges/cross-chain-messaging

## 使用 LI.FI SDK

用于实现跨链交易和桥接功能：

```typescript
import { createConfig, getQuote, executeRoute } from "@lifi/sdk";

// Initialize LI.FI
createConfig({
  integrator: "your-app-name",
});

// Get bridge quote
const quote = await getQuote({
  fromChain: 1, // Ethereum
  toChain: 42220, // Celo
  fromToken: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC on Ethereum
  toToken: "0xcebA9300f2b948710d2653dD7B07f33A8B32118C", // USDC on Celo
  fromAmount: "1000000000", // 1000 USDC (6 decimals)
  fromAddress: userAddress,
});

// Execute the bridge
const result = await executeRoute(quote, {
  updateRouteHook: (route) => {
    console.log("Route updated:", route);
  },
});
```

## 桥接注意事项

### 安全性
- 原生桥接（如 Superbridge）是最安全的
- 第三方桥接方案的安全性取决于其自身的安全机制
- 在进行桥接操作前，请务必验证相关合约地址的合法性

### 时间消耗
- 原生 L1→L2 桥接：约 15-20 分钟
- L2→L1 提现：需要等待 7 天（挑战期）
- 第三方桥接：时间各不相同（几分钟到几小时不等）

### 费用
- 原生桥接：仅收取 gas 费用
- 第三方桥接：除了 gas 费用外，还需支付额外的桥接费用

## 依赖项

```json
{
  "dependencies": {
    "viem": "^2.0.0"
  }
}
```

关于 LI.FI 的集成信息，请参阅相关文档：

```json
{
  "dependencies": {
    "@lifi/sdk": "^3.0.0"
  }
}
```

## 额外资源

- [bridge-contracts.md](references/bridge-contracts.md) - 所有桥接相关合约的地址
- [bridged-tokens.md](references/bridged-tokens.md) - 完整的桥接代币列表