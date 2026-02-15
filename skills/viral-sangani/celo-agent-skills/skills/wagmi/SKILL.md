---
name: wagmi
description: 使用 Wagmi React Hooks 开发 Celo dApps。涵盖钱包连接、交易处理相关的钩子函数（hooks），以及 React 组件的集成方式。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Wagmi for Celo

Wagmi 是一个基于 React 的库，用于使用 Hooks 构建以太坊应用程序。它内部使用了 viem（一个用于与以太坊区块链交互的库）。

来源：https://wagmi.sh

## 使用场景

- 在 Celo 上构建 React dApps（去中心化应用）
- 实现钱包连接流程
- 在 React 组件中管理区块链状态
- 使用 React Hooks 进行合约交互

## 安装

```bash
npm install wagmi viem@2.x @tanstack/react-query
```

## 配置

### 基本设置

```typescript
// config.ts
import { http, createConfig } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";

export const config = createConfig({
  chains: [celo, celoSepolia],
  transports: {
    [celo.id]: http(),
    [celoSepolia.id]: http(),
  },
});
```

### 使用连接器（Connectors）

```typescript
import { http, createConfig } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";
import { injected, walletConnect, metaMask } from "wagmi/connectors";

const projectId = process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!;

export const config = createConfig({
  chains: [celo, celoSepolia],
  connectors: [
    injected(),
    walletConnect({ projectId }),
    metaMask(),
  ],
  transports: {
    [celo.id]: http(),
    [celoSepolia.id]: http(),
  },
});
```

来源：https://wagmi.sh/react/guides/connect-wallet

## 提供者（Provider）设置

```tsx
// app.tsx
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";

const queryClient = new QueryClient();

function App({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## 钱包连接

### 显示钱包选项

```tsx
import { useConnect, useConnectors } from "wagmi";

function WalletOptions() {
  const { connect } = useConnect();
  const connectors = useConnectors();

  return (
    <div>
      {connectors.map((connector) => (
        <button
          key={connector.uid}
          onClick={() => connect({ connector })}
        >
          {connector.name}
        </button>
      ))}
    </div>
  );
}
```

### 显示已连接的账户

```tsx
import { useAccount, useDisconnect } from "wagmi";

function Account() {
  const { address, isConnected, chain } = useAccount();
  const { disconnect } = useDisconnect();

  if (!isConnected) return <WalletOptions />;

  return (
    <div>
      <p>Connected: {address}</p>
      <p>Chain: {chain?.name}</p>
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  );
}
```

## 读取合约数据

```tsx
import { useReadContract } from "wagmi";

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
] as const;

function TokenBalance({ address }: { address: `0x${string}` }) {
  const { data: balance, isLoading } = useReadContract({
    address: "0x765de816845861e75a25fca122bb6898b8b1282a", // USDm
    abi: ERC20_ABI,
    functionName: "balanceOf",
    args: [address],
  });

  if (isLoading) return <div>Loading...</div>;

  return <div>Balance: {balance?.toString()}</div>;
}
```

## 向合约写入数据

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from "wagmi";
import { parseEther } from "viem";

function TransferToken() {
  const { writeContract, data: hash, isPending } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  async function handleTransfer() {
    writeContract({
      address: "0x765de816845861e75a25fca122bb6898b8b1282a",
      abi: ERC20_ABI,
      functionName: "transfer",
      args: ["0x...", parseEther("10")],
    });
  }

  return (
    <div>
      <button onClick={handleTransfer} disabled={isPending}>
        {isPending ? "Confirming..." : "Transfer"}
      </button>
      {isConfirming && <div>Waiting for confirmation...</div>}
      {isSuccess && <div>Transaction confirmed!</div>}
    </div>
  );
}
```

## 发送交易

```tsx
import { useSendTransaction, useWaitForTransactionReceipt } from "wagmi";
import { parseEther } from "viem";

function SendCelo() {
  const { sendTransaction, data: hash, isPending } = useSendTransaction();

  const { isSuccess } = useWaitForTransactionReceipt({ hash });

  return (
    <button
      onClick={() =>
        sendTransaction({
          to: "0x...",
          value: parseEther("0.1"),
        })
      }
      disabled={isPending}
    >
      Send 0.1 CELO
    </button>
  );
}
```

## 切换链（Chain Switching）

```tsx
import { useSwitchChain } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";

function NetworkSwitcher() {
  const { switchChain, isPending } = useSwitchChain();

  return (
    <div>
      <button
        onClick={() => switchChain({ chainId: celo.id })}
        disabled={isPending}
      >
        Switch to Celo Mainnet
      </button>
      <button
        onClick={() => switchChain({ chainId: celoSepolia.id })}
        disabled={isPending}
      >
        Switch to Celo Sepolia
      </button>
    </div>
  );
}
```

## 常用 Hooks

| Hooks | 用途 |
|------|---------|
| useAccount | 获取已连接账户的信息 |
| useConnect | 连接钱包 |
| useDisconnect | 断开钱包连接 |
| useReadContract | 读取合约状态 |
| useWriteContract | 向合约写入数据 |
| useSendTransaction | 发送原生货币 |
| useWaitForTransactionReceipt | 等待交易确认 |
| useSwitchChain | 切换区块链网络 |
| useBalance | 获取账户余额 |
| useChainId | 获取当前链的 ID |

## Celo 链的 ID

| 链络 | 链 ID |
|---------|----------|
| Celo 主网 | 42220 |
| Celo Sepolia | 11142220 |

## 依赖项

```json
{
  "dependencies": {
    "wagmi": "^2.0.0",
    "viem": "^2.0.0",
    "@tanstack/react-query": "^5.0.0"
  }
}
```

## 额外资源

- [hooks-reference.md](references/hooks-reference.md) - 完整的 Hooks 参考文档