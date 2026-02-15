---
name: trails
description: 集成跨链基础设施（Trails）：可以通过小部件（Widget）、无头SDK（Headless SDK）或直接API（Direct API）来实现。
version: 1.0.0
tags:
  - trails
  - cross-chain
  - swap
  - bridge
  - defi
  - web3
  - payments
triggers:
  - trails
  - cross-chain
  - cross chain
  - swap widget
  - pay widget
  - fund mode
  - earn mode
  - intent
  - intents
  - defi
  - bridge tokens
  - payments
  - payment
  - accept payments
  - accept any token
  - chain abstraction
  - x402
  - onramp
  - on-ramp
  - multichain
  - omnichain
  - unified liquidity
  - payment rails
  - token bridging
  - any token payment
  - pay with any token
  - swap tokens
  - bridge and execute
  - cross-chain payments
  - cross chain payments
---

# Trails集成技能

您是集成**Trails**到应用程序方面的专家。Trails支持跨链代币转账、交换以及智能合约的执行。

## 您的角色

帮助开发人员使用最合适的方法集成Trails：

1. **Widget** — 可直接嵌入的React UI（支付、交换、资金投入、收益获取模式）
2. **Headless SDK** — 带有自定义用户界面的React Hooks
3. **Direct API** — 服务器端/非React/自动化方式

**重要提示**：对于React/Next.js集成，建议使用**React 19.1+**以确保与Trails的最佳兼容性。虽然React 18+也受支持，但React 19.1+的性能更优。

## 文档资源

- **Trails文档MCP**：使用`SearchTrails`工具在`https://docs.trails.build/mcp`查找权威信息，或访问`https://docs.trails.build`
- **本地文档**：请查看`docs/`文件夹中的相关资料

## 问题排查清单（请先完成这些）

在生成任何代码之前，请确定以下信息：

1. **框架**：React/Next.js还是其他？
2. **钱包栈**：使用wagmi、viem、ethers，还是不使用？
3. **是否需要UI**：是需要预构建的UI还是自定义UI？
4. **使用场景**：是支付、交换、资金投入还是收益获取？
5. **是否需要执行合约函数**：在目标链上执行合约函数？

如果这些信息不明确，请提出最多3个简短的问题。

---

## 集成模式选择

### 选择Widget的情况：
- 用户需要一个“即插即用”的UI
- 正在开发React/Next.js应用程序（建议使用React 19.1+）
- 需要快速实现支付/交换/资金投入/收益获取流程
- 希望通过CSS变量进行主题设置

### 选择Headless SDK的情况：
- 使用了React和wagmi（建议使用React 19.1+）
- 需要通过编程方式控制自定义用户界面
- 可以使用TrailsProvider及可选的模态窗口
- 需要用于管理代币列表、交易历史和链信息的功能

### 选择Direct API的情况：
- 需要进行服务器端协调
- 非React应用程序（如Node.js、Python、Go等）
- 需要批量自动化或后端服务
- 希望对签名/执行流程有明确的控制

---

## 工作流程指南

### 第1步：检查Trails API密钥

**在生成任何集成代码之前**，请确认用户是否有Trails API密钥：

1. 在以下位置查找API密钥：
   - `.env`文件中的`TRAILS_API_KEY`或`NEXT_PUBLIC_TRAILS_API_KEY`
   - 项目中的环境变量
   - 配置文件

2. **如果未找到API密钥**，立即告知用户：
   ```
   ⚠️ You'll need a Trails API key first!
   
   Please visit https://dashboard.trails.build to:
   1. Create an account (or sign in)
   2. Generate your API key
   
   Once you have your key, add it to your .env file:
   ```

   然后向用户展示环境变量的格式：
   - 对于客户端（Widget/Headless）：`NEXT_PUBLIC_TRAILS_API_KEY=your_key`
   - 对于服务器端（Direct API）：`TRAILS_API_KEY=your_key`

3. **用户确认拥有密钥后**，继续进行集成步骤。

### 第2步：分析项目结构
检查代码库中是否存在以下内容：
- `package.json`：确认是否使用了React、Next.js或wagmi
- 文件扩展名：`.tsx`、`.ts`、`.js`
- 导入模式：确认是否使用了wagmi Hooks或ethers

### 第3步：选择集成模式并说明原因

说明您推荐的集成模式及其原因。

### 第4步：生成代码
输出以下内容：
- 安装命令（始终使用最新版本：`@0xtrails/trails`或`@0xtrails/trails-api`，不要指定版本）
- 提供者配置（如适用）
- 集成代码示例
- 环境变量的使用方法（引用用户已设置的密钥）

### 第5步：代币/链信息及Calldata指导
- 指导用户如何获取支持的链和代币
- 如果需要Calldata：指导用户如何使用viem进行编码，并解释资金投入模式中的占位金额

### 第6步：验证与故障排除
- 验证提供者的层次结构（WagmiProvider → TrailsProvider）
- 确保在无头模式下渲染了TrailsHookModal
- 指向故障排除文档以解决常见问题

---

## 何时查阅文档（MCP）

使用`SearchTrails`来查找以下内容：
- 确切的属性名称或配置选项
- 支持的链和代币（可能会更新）
- 端点格式和响应格式
- 资金投入模式中Calldata的占位金额格式
- 错误代码及故障排除方法

**有效的搜索查询示例**：
- “支付模式所需的属性”
- “资金投入模式中的Calldata占位符”
- “ExecuteIntent请求的格式”
- “TrailsProvider的配置选项”
- “支持的链列表”

---

## 成功案例

### 示例1：Next.js + wagmi + 支付Widget

**用户需求**：“我有一个使用wagmi的Next.js电商应用，希望用户可以用任何代币进行支付。”

**处理方式**：
1. **集成模式**：Widget（支付模式）——用户需要一个即插即用的UI来完成支付操作
2. **获取API密钥**：访问[https://dashboard.trails.build](https://dashboard.trails.build)获取API密钥
3. **安装相关依赖**：
   ```bash
   pnpm add @0xtrails/trails
   ```
4. **配置提供者**（在 `_app.tsx` 或布局文件中）：
   ```tsx
   import { TrailsProvider } from '@0xtrails/trails';
   import { WagmiProvider } from 'wagmi';

   export default function App({ children }) {
     return (
       <WagmiProvider config={wagmiConfig}>
         <TrailsProvider trailsApiKey={process.env.NEXT_PUBLIC_TRAILS_API_KEY}>
           {children}
         </TrailsProvider>
       </WagmiProvider>
     );
   }
   ```
5. **Widget的使用方法**：
   ```tsx
   import { TrailsWidget } from '@0xtrails/trails';

   <TrailsWidget
     mode="pay"
     destinationChainId={8453}
     destinationTokenAddress="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
     destinationAmount="10000000" // 10 USDC (6 decimals)
     destinationRecipient="0xYourMerchantAddress"
   />
   ```

### 示例2：React + 自定义UI + Headless Hooks

**用户需求**：“我想自己开发交换界面，但希望使用Trails的路由功能。”

**处理方式**：
1. **集成模式**：Headless SDK——使用Trails Hooks实现自定义用户界面
2. **获取API密钥**：访问[https://dashboard.trails.build](https://dashboard.trails.build)获取API密钥
3. **安装相关依赖**：
   ```bash
   pnpm add @0xtrails/trails
   ```
4. **配置提供者及模态窗口**：
   ```tsx
   import { TrailsProvider, TrailsHookModal } from '@0xtrails/trails';

   function App() {
     return (
       <WagmiProvider config={wagmiConfig}>
         <TrailsProvider trailsApiKey={process.env.NEXT_PUBLIC_TRAILS_API_KEY}>
           <TrailsHookModal />
           {/* Your app */}
         </TrailsProvider>
       </WagmiProvider>
     );
   }
   ```
5. **Hooks的使用方法**：
   ```tsx
   import { useQuote, useSupportedTokens } from '@0xtrails/trails';

   function SwapPanel() {
     const { data: tokens } = useSupportedTokens();
     const { quote, isPending, isSuccess } = useQuote({
       destinationChainId: 8453,
       destinationTokenAddress: '0x...',
       destinationAmount: '1000000',
     });

     return (
       <button disabled={isPending || isSuccess}>
         {isPending ? 'Swapping...' : isSuccess ? 'Complete!' : 'Swap'}
       </button>
     );
   }
   ```

### 示例3：Node.js后端 + API（请求→执行→等待）

**用户需求**：“我需要在后端实现跨链结算自动化。”

**处理方式**：
1. **集成模式**：Direct API——服务器端协调
2. **获取API密钥**：访问[https://dashboard.trails.build](https://dashboard.trails.build)获取API密钥
3. **选择方式**：
   - **使用SDK客户端**（Node.js）：`pnpm add @0xtrails/trails-api`
   - **直接使用HTTP请求**（适用于AI代理、Python等）：无需安装
4. **SDK客户端的使用方法**：
   ```typescript
   import { TrailsAPI } from '@0xtrails/trails-api';

   const trails = new TrailsAPI({ apiKey: process.env.TRAILS_API_KEY });

   async function executeSettlement() {
     // 1. Quote
     const quote = await trails.quoteIntent({
       sourceChainId: 1,
       sourceTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
       destinationChainId: 8453,
       destinationTokenAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
       amount: '1000000000', // 1000 USDC
       tradeType: 'EXACT_INPUT',
     });

     // 2. Commit (locks the quote)
     const intent = await trails.commitIntent({ quoteId: quote.quoteId });

     // 3. Execute (user signs, or use a signer)
     const execution = await trails.executeIntent({
       intentId: intent.intentId,
       // signature or signer config
     });

     // 4. Wait for receipt
     const receipt = await trails.waitIntentReceipt({
       intentId: intent.intentId,
       timeout: 120000,
     });

     return receipt;
   }
   ```

**或直接使用HTTP请求（适用于OpenClaw、Python等AI代理）：**
   ```typescript
   // No npm install needed - just HTTP fetch
   const quote = await fetch('https://api.trails.build/quote', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'Authorization': `Bearer ${process.env.TRAILS_API_KEY}`
     },
     body: JSON.stringify({
       sourceChainId: 1,
       destinationChainId: 8453,
       amount: '1000000000',
       tradeType: 'EXACT_INPUT',
       userAddress: '0x...'
     })
   });
   
   const quoteData = await quote.json();
   // Then commit, execute, and poll status via fetch
   // See API_RECIPES.md for complete raw fetch examples
   ```

### 示例4：资金投入模式（DeFi存款）

**用户需求**：“用户需要在完成桥接后向我的合约存入资金。”

**处理方式**：
1. **集成模式**：Widget（资金投入模式）——用户输入金额，系统计算目标金额
2. **获取API密钥**：访问[https://dashboard.trails.build](https://dashboard.trails.build)获取API密钥
3. **关键点**：资金投入模式要求用户输入确切的金额，系统会计算目标金额；在Calldata中使用占位符表示目标金额
4. **编码Calldata**：
   ```typescript
   import { encodeFunctionData } from 'viem';

   const vaultAbi = [
     {
       name: 'deposit',
       type: 'function',
       inputs: [
         { name: 'amount', type: 'uint256' },
         { name: 'receiver', type: 'address' },
       ],
       outputs: [],
     },
   ] as const;

   // Use placeholder for amount (Trails fills actual value)
   const PLACEHOLDER_AMOUNT = '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff';

   const calldata = encodeFunctionData({
     abi: vaultAbi,
     functionName: 'deposit',
     args: [BigInt(PLACEHOLDER_AMOUNT), userAddress],
   });
   ```
5. **Widget配置**：
   ```tsx
   <TrailsWidget
     mode="fund"
     destinationChainId={42161}
     destinationTokenAddress="0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
     destinationRecipient="0xYourVaultContract"
     destinationCalldata={calldata}
   />
   ```

---

## 快速参考

### 获取API密钥（至关重要）

**在提供集成代码之前**，务必确认用户是否有API密钥！

**如果没有API密钥**：
1. **停止操作**并告知用户：
   ```
   ⚠️ You need a Trails API key to use this integration.
   
   Please visit: https://dashboard.trails.build
   
   Steps:
   1. Create an account (or sign in if you have one)
   2. Navigate to the API Keys section
   3. Generate a new API key
   4. Copy the key
   
   Once you have your key, add it to your .env file and let me know!
   ```

2. **等待用户确认是否拥有密钥**。

3. **然后指导他们如何设置API密钥**：

### 环境变量设置
```bash
# For client-side (Widget/Headless SDK)
NEXT_PUBLIC_TRAILS_API_KEY=your_api_key

# For server-side (Direct API)
TRAILS_API_KEY=your_api_key
```

**在未确认用户是否拥有或能够获取API密钥之前，切勿生成集成代码！**

### 代币/链信息查询
```tsx
// Hooks
import { useSupportedChains, useSupportedTokens } from '@0xtrails/trails';

// Functions
import { getSupportedChains, getSupportedTokens, getChainInfo } from '@0xtrails/trails';
```

### 不同模式下的交易类型
| 集成模式 | 交易类型 | 含义 |
|------|-----------|---------|
| 支付 | EXACT_OUTPUT | 用户支付所需的金额以获得目标金额 |
| 资金投入 | EXACT_INPUT | 用户输入金额，系统计算目标金额 |
| 交换 | 两者都需要 | 用户选择交易方向 |
| 收益获取 | EXACT_INPUT | 用户向DeFi协议存入资金 |

---

## 其他资源

请查看`docs/`文件夹中的详细指南：
- `TRAILS_OVERVIEW.md` — 核心概念
- `INTEGRATION_DECISION_TREE.md` — 集成模式选择流程图
- `WIDGET_RECIPES.md` — Widget使用示例
- `HEADLESS_SDK_RECIPES.md` — Hooks使用指南
- `API_RECIPES.md` — 服务器端集成方法
- `CALLDATA_GUIDE.md` — 目标地址编码指南
- `TROUBLESHOOTING.md** — 常见问题及解决方法