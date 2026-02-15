---
name: evm-wallet-integration
description: 将钱包集成到 Celo dApps 中。涵盖 RainbowKit、Dynamic 以及钱包连接的相关模式。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo的EVM钱包集成

本技能涵盖了将钱包连接库集成到Celo去中心化应用程序（dApps）中的方法。

## 使用场景

- 为dApp添加钱包连接功能  
- 支持多种类型的钱包  
- 实现身份验证流程  
- 构建用户友好的钱包体验  

## 钱包连接库  

| 库名 | 说明 | 适用场景 |  
|---------|-------------|----------|  
| Reown AppKit | 官方WalletConnect SDK，支持wagmi | 适用于生产环境的React应用程序  
| Dynamic | 专注于身份验证功能，包含仪表板 | 需要用户管理的应用程序  
| ConnectKit | 简单的wagmi集成方案 | 快速设置  
| Custom wagmi | 直接的连接器配置方式 | 提供完全的控制权  

## Reown AppKit  

专为React应用程序设计的官方WalletConnect SDK，内置了钱包用户界面，支持600多种钱包。  
来源：https://docs.reown.com/appkit  

> **注意**：Reown是之前称为WalletConnect Inc.的公司（2024年进行了品牌重塑）。wagmi连接器的协议和npm包仍使用“walletConnect”作为名称。  

### 安装  
```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query
```  

### 获取项目ID  

1. 访问[cloud.reown.com](https://cloud.reown.com)  
2. 创建一个新的项目  
3. 复制项目ID  

### 配置  
```typescript
// config.ts
import { WagmiAdapter } from "@reown/appkit-adapter-wagmi";
import { celo, celoAlfajores } from "@reown/appkit/networks";

const projectId = process.env.NEXT_PUBLIC_REOWN_PROJECT_ID!;

export const wagmiAdapter = new WagmiAdapter({
  networks: [celo, celoAlfajores],
  projectId,
  ssr: true,
});

export const config = wagmiAdapter.wagmiConfig;
```  

### 提供者设置  
```tsx
"use client";
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createAppKit } from "@reown/appkit/react";
import { wagmiAdapter } from "./config";
import { celo, celoAlfajores } from "@reown/appkit/networks";

const queryClient = new QueryClient();

createAppKit({
  adapters: [wagmiAdapter],
  networks: [celo, celoAlfajores],
  projectId: process.env.NEXT_PUBLIC_REOWN_PROJECT_ID!,
  metadata: {
    name: "My Celo App",
    description: "Celo dApp",
    url: "https://myapp.com",
    icons: ["https://myapp.com/icon.png"],
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={wagmiAdapter.wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```  

### 连接按钮  
```tsx
import { AppKitButton } from "@reown/appkit/react";

function Header() {
  return (
    <nav>
      <AppKitButton />
    </nav>
  );
}
```  

### 自定义连接按钮  
```tsx
import { useAppKit, useAppKitAccount } from "@reown/appkit/react";

function WalletConnect() {
  const { open } = useAppKit();
  const { address, isConnected } = useAppKitAccount();

  if (isConnected) {
    return (
      <div>
        <p>Connected: {address}</p>
        <button onClick={() => open({ view: "Account" })}>Account</button>
      </div>
    );
  }

  return <button onClick={() => open()}>Connect Wallet</button>;
}
```  

### 使用AppKit与wagmi Hooks  
```tsx
import { useAccount, useBalance, useDisconnect } from "wagmi";

function AccountInfo() {
  const { address, isConnected } = useAccount();
  const { data: balance } = useBalance({ address });
  const { disconnect } = useDisconnect();

  if (!isConnected) return null;

  return (
    <div>
      <p>Address: {address}</p>
      <p>Balance: {balance?.formatted} {balance?.symbol}</p>
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  );
}
```  

## Dynamic  

专注于身份验证功能的钱包连接解决方案，同时提供用户管理功能及仪表板。  
来源：https://docs.dynamic.xyz  

### 安装  
```bash
npm install @dynamic-labs/sdk-react
```  

### 配置  
```tsx
import {
  DynamicContextProvider,
  DynamicWidget,
} from "@dynamic-labs/sdk-react";

function App() {
  return (
    <DynamicContextProvider
      settings={{
        environmentId: process.env.NEXT_PUBLIC_DYNAMIC_ENV_ID!,
      }}
    >
      <DynamicWidget />
    </DynamicContextProvider>
  );
}
```  

### 启用Celo  

1. 访问app.dynamic.xyz的仪表板  
2. 转到“配置”选项  
3. 选择“EVM”网络  
4. 打开Celo网络支持  

## 自定义实现  

无需依赖任何第三方库，直接使用wagmi来实现钱包连接功能。  

### Wagmi配置  
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

### 钱包连接组件  
```tsx
import { useConnect, useConnectors, useAccount, useDisconnect } from "wagmi";

function WalletConnect() {
  const { connect } = useConnect();
  const connectors = useConnectors();
  const { address, isConnected } = useAccount();
  const { disconnect } = useDisconnect();

  if (isConnected) {
    return (
      <div>
        <p>Connected: {address}</p>
        <button onClick={() => disconnect()}>Disconnect</button>
      </div>
    );
  }

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

## 网络配置  

| 网络 | 链路ID | Reown中的导入方式 | Wagmi中的导入方式 |  
|---------|----------|--------------|--------------|  
| Mainnet | 42220 | `@reown/appkit/networks`中的`celo` | `wagmi/chains`中的`celo` |  
| Celo Alfajores | 44787 | `@reown/appkit/networks`中的`celoAlfajores` | `wagmi/chains`中的`celoAlfajores` |  
| Celo Sepolia | 11142220 | - | `wagmi/chains`中的`celoSepolia` |  

### Reown项目ID  

用于WalletConnect连接功能。WalletConnect Inc.于2024年更名为Reown。  
1. 访问[cloud.reown.com](https://cloud.reown.com)（原名为WalletConnect Cloud）  
2. 创建一个新的项目（选择“AppKit”类型）  
3. 复制项目ID  
4. 将项目ID添加到环境变量中：  
```bash
NEXT_PUBLIC_REOWN_PROJECT_ID=your_project_id
```  

> **注意**：wagmi的`walletConnect`连接器仍然使用原来的项目ID，仅云服务端进行了品牌重塑。  

## 最佳实践  

1. **支持多种钱包**：不要强制用户使用特定的钱包。  
2. **处理网络切换**：提示用户切换到Celo网络。  
3. **显示连接状态**：在用户界面中清晰地显示钱包的连接状态（已连接/未连接）。  
4. **处理错误**：提供易于理解的错误信息。  
5. **在移动设备上进行测试**：确保应用程序在移动浏览器和钱包应用程序中都能正常工作。  

## 依赖项  

### Reown AppKit  
```json
{
  "dependencies": {
    "@reown/appkit": "^1.0.0",
    "@reown/appkit-adapter-wagmi": "^1.0.0",
    "wagmi": "^2.0.0",
    "viem": "^2.0.0",
    "@tanstack/react-query": "^5.0.0"
  }
}
```  

### 自定义wagmi（不使用AppKit）  
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

- [wallet-connectors.md](references/wallet-connectors.md)：连接器配置参考文档