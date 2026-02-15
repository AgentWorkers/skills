---
name: thirdweb
description: 使用 thirdweb SDK 进行 Celo 开发。该 SDK 支持钱包连接、合约部署以及预构建的 UI 组件。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Thirdweb for Celo

Thirdweb 是一个全栈的 Web3 开发平台，支持 Celo 的 SDK。

来源：https://docs.celo.org/tooling/libraries-sdks/thirdweb-sdk/index.md

## 适用场景

- 使用预构建的 UI 组件构建去中心化应用（dApps）
- 无需编写部署脚本即可部署智能合约
- 集成 500 多种钱包
- 开发跨链应用程序

## 安装

```bash
npm install thirdweb
```

或者创建一个新的项目：

```bash
npx thirdweb create app
```

## 客户端设置

### 获取客户端 ID

1. 访问 https://thirdweb.com/team
2. 创建一个以 `localhost` 为允许域名的项目
3. 复制客户端 ID

### 初始化客户端

```typescript
import { createThirdwebClient } from "thirdweb";

export const client = createThirdwebClient({
  clientId: process.env.NEXT_PUBLIC_THIRDWEB_CLIENT_ID!,
});
```

### 服务器端使用

```typescript
const client = createThirdwebClient({
  secretKey: process.env.THIRDWEB_SECRET_KEY!,
});
```

来源：https://portal.thirdweb.com/typescript/v5/getting-started

## 链路配置

### 使用预定义的链

```typescript
import { celo } from "thirdweb/chains";

// Use directly
const chain = celo;
```

### 自定义链定义

```typescript
import { defineChain } from "thirdweb";

const celoChain = defineChain(42220);

// Or with custom RPC
const celoCustom = defineChain({
  id: 42220,
  rpc: "https://forno.celo.org",
});
```

来源：https://portal.thirdweb.com/typescript/v5/chain

## React 提供者设置

```tsx
import { ThirdwebProvider } from "thirdweb/react";

function App({ children }: { children: React.ReactNode }) {
  return (
    <ThirdwebProvider>
      {children}
    </ThirdwebProvider>
  );
}
```

## 钱包连接

### ConnectButton 组件

```tsx
import { ConnectButton } from "thirdweb/react";
import { celo } from "thirdweb/chains";
import { client } from "./client";

function WalletConnect() {
  return (
    <ConnectButton
      client={client}
      chain={celo}
    />
  );
}
```

### 与特定钱包连接

```tsx
import { ConnectButton } from "thirdweb/react";
import { createWallet } from "thirdweb/wallets";

const wallets = [
  createWallet("io.metamask"),
  createWallet("com.coinbase.wallet"),
  createWallet("app.valora"),
];

function WalletConnect() {
  return (
    <ConnectButton
      client={client}
      wallets={wallets}
    />
  );
}
```

## 合约交互

### 获取合约引用

```typescript
import { getContract } from "thirdweb";
import { celo } from "thirdweb/chains";

const contract = getContract({
  client,
  chain: celo,
  address: "0x...",
});
```

### 读取合约数据

```tsx
import { useReadContract } from "thirdweb/react";
import { balanceOf } from "thirdweb/extensions/erc20";

function TokenBalance({ address }: { address: string }) {
  const { data, isLoading } = useReadContract(
    balanceOf,
    {
      contract,
      address,
    }
  );

  if (isLoading) return <div>Loading...</div>;
  return <div>Balance: {data?.toString()}</div>;
}
```

### 向合约写入数据

```tsx
import { useSendTransaction } from "thirdweb/react";
import { transfer } from "thirdweb/extensions/erc20";

function TransferTokens() {
  const { mutate: sendTransaction, isPending } = useSendTransaction();

  async function handleTransfer() {
    const transaction = transfer({
      contract,
      to: "0x...",
      amount: "10",
    });

    sendTransaction(transaction);
  }

  return (
    <button onClick={handleTransfer} disabled={isPending}>
      Transfer
    </button>
  );
}
```

## 账户钩子

### 获取活跃账户

```tsx
import { useActiveAccount } from "thirdweb/react";

function Account() {
  const account = useActiveAccount();

  if (!account) return <div>Not connected</div>;
  return <div>Connected: {account.address}</div>;
}
```

### 获取钱包余额

```tsx
import { useWalletBalance } from "thirdweb/react";
import { celo } from "thirdweb/chains";

function Balance() {
  const account = useActiveAccount();
  const { data, isLoading } = useWalletBalance({
    client,
    chain: celo,
    address: account?.address,
  });

  if (isLoading) return <div>Loading...</div>;
  return <div>{data?.displayValue} {data?.symbol}</div>;
}
```

## 服务器端使用

```typescript
import { createThirdwebClient } from "thirdweb";
import { getContract } from "thirdweb";
import { celo } from "thirdweb/chains";
import { getNFTs } from "thirdweb/extensions/erc1155";

const client = createThirdwebClient({
  secretKey: process.env.THIRDWEB_SECRET_KEY!,
});

const contract = getContract({
  client,
  chain: celo,
  address: "0x...",
});

const nfts = await getNFTs({ contract });
```

## 预构建的扩展库

Thirdweb 为常见的智能合约提供了类型安全的扩展库：

| 扩展库 | 导入路径 |
|---------|-------------|
| ERC20   | `thirdweb/extensions/erc20` |
| ERC721   | `thirdweb/extensions/erc721` |
| ERC1155   | `thirdweb/extensions/erc1155` |

## 部署

将合约部署到去中心化存储中：

```bash
npx thirdweb deploy --app
```

## 环境变量

```bash
# .env
NEXT_PUBLIC_THIRDWEB_CLIENT_ID=your_client_id
THIRDWEB_SECRET_KEY=your_secret_key  # Server-side only
```

## 依赖项

```json
{
  "dependencies": {
    "thirdweb": "^5.0.0"
  }
}
```

## 额外资源

- [extensions.md](references/extensions.md) - 可用的合约扩展库