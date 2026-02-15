---
name: minipay-integration
description: 为 MiniPay 钱包构建迷你应用程序。这些应用程序可用于开发与 MiniPay 相关的应用程序、检测 MiniPay 钱包的存在，或为 Celo 平台创建以移动设备为主导的去中心化应用（dApps）。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# MiniPay集成

本技能涵盖了为MiniPay构建Mini App的相关内容。MiniPay是目前全球南方地区增长最快的非托管钱包服务，拥有超过1000万的活跃用户。

## 使用场景

- 为MiniPay构建Mini App
- 在你的dApp中检测用户是否使用MiniPay钱包
- 开发以移动设备为主的支付应用程序
- 与MiniPay的发现页面进行集成

## 什么是MiniPay？

MiniPay是一款支持内置Mini App发现页面的稳定币钱包。它可以通过以下方式使用：
- 集成到Opera Mini浏览器（Android版本）中
- 作为独立的应用程序（Android和iOS版本）

主要特性：
- 可将手机号码映射到钱包地址
- 交易手续费极低（低于1美分）
- 代码体积极小（仅2MB）
- 支持USDm（cUSD）、USDC和USDT等稳定币

## 快速入门

### 创建MiniPay App

```bash
npx @celo/celo-composer@latest create -t minipay
```

这段代码用于创建一个预先配置好以支持MiniPay功能的Next.js应用程序框架。

## 检测用户是否使用MiniPay

检查用户当前是否正在使用MiniPay钱包：

```typescript
function isMiniPay(): boolean {
  return typeof window !== "undefined" &&
         window.ethereum?.isMiniPay === true;
}
```

**注意：** 该代码必须在浏览器环境中运行，不能在Node.js环境中执行。

## 连接钱包

MiniPay会自动完成钱包的连接。若需要请求账户访问权限，请执行以下操作：

```typescript
async function connectWallet(): Promise<string | null> {
  if (typeof window === "undefined" || !window.ethereum) {
    return null;
  }

  const accounts = await window.ethereum.request({
    method: "eth_requestAccounts",
    params: [],
  });

  return accounts[0] || null;
}
```

**注意：** 当用户已经在使用MiniPay时，应隐藏“连接钱包”按钮，因为此时钱包已经处于连接状态。

```typescript
const [address, setAddress] = useState<string | null>(null);
const inMiniPay = isMiniPay();

useEffect(() => {
  if (inMiniPay) {
    connectWallet().then(setAddress);
  }
}, [inMiniPay]);

return (
  <div>
    {!inMiniPay && (
      <button onClick={() => connectWallet().then(setAddress)}>
        Connect Wallet
      </button>
    )}
    {address && <p>Connected: {address}</p>}
  </div>
);
```

## 查看余额

```typescript
import { createPublicClient, http, formatUnits } from "viem";
import { celo } from "viem/chains";

const publicClient = createPublicClient({
  chain: celo,
  transport: http(),
});

const USDM_ADDRESS = "0x765de816845861e75a25fca122bb6898b8b1282a";

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
] as const;

async function getUSDmBalance(address: string): Promise<string> {
  const balance = await publicClient.readContract({
    address: USDM_ADDRESS,
    abi: ERC20_ABI,
    functionName: "balanceOf",
    args: [address as `0x${string}`],
  });

  return formatUnits(balance, 18);
}
```

## 发送交易

建议使用viem或wagmi库来处理交易。MiniPay不支持ethers.js库。

```typescript
import { createWalletClient, custom, parseUnits, encodeFunctionData } from "viem";
import { celo } from "viem/chains";

const USDM_ADDRESS = "0x765de816845861e75a25fca122bb6898b8b1282a";

const ERC20_ABI = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ type: "bool" }],
  },
] as const;

async function sendUSDm(to: string, amount: string): Promise<string> {
  const walletClient = createWalletClient({
    chain: celo,
    transport: custom(window.ethereum),
  });

  const [address] = await walletClient.getAddresses();

  const hash = await walletClient.sendTransaction({
    account: address,
    to: USDM_ADDRESS,
    data: encodeFunctionData({
      abi: ERC20_ABI,
      functionName: "transfer",
      args: [to as `0x${string}`, parseUnits(amount, 18)],
    }),
  });

  return hash;
}
```

## 测试你的Mini App

### 1. 设置ngrok

由于MiniPay无法直接访问本地主机（localhost），你需要使用ngrok来创建一个代理服务器：

```bash
ngrok http 3000
```

### 2. 启用MiniPay的开发模式

1. 打开MiniPay应用，进入“设置” > “关于”
2. 连续点击版本号，直到开发模式被启用
3. 进入“设置” > “开发者设置”
4. 启用“使用Celo Sepolia测试网”功能

### 3. 加载你的应用程序

1. 打开MiniPay应用，点击指南针图标
2. 选择“测试页面”
3. 输入你的ngrok HTTPS地址
4. 点击“开始”

## 支持的环境和限制

### 支持的环境
- 仅支持Celo主网和Celo Sepolia测试网
- 必须使用viem v2+及wagmi库
- 必须使用TypeScript v5+和Node.js v20+版本
- 支持USDm（cUSD）、USDC和USDT等稳定币

### 不支持的功能
- 不支持ethers.js库（请改用viem）
- 不支持EIP-1559交易（仅限旧版本）
- 不支持消息签名功能
- 不支持Android/iOS模拟器（请使用真实设备进行测试）
- 不支持其他区块链网络

## 依赖项

```json
{
  "dependencies": {
    "viem": "^2.0.0",
    "@celo/abis": "^11.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

## 额外资源

- [testing-guide.md](references/testing-guide.md) - 详细的测试指南
- [troubleshooting.md](references/troubleshooting.md) - 常见问题及解决方法
- [code-examples.md](references/code-examples.md) - 有关Gas费用计算、费用货币设置以及React Hooks的使用示例