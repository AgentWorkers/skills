---
name: celo-composer
description: 使用 Celo Composer 构建 Celo dApps。适用于启动新的 Celo 项目、创建 MiniPay 应用程序或设置开发环境。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo Composer

本技能介绍如何使用 Celo Composer 通过预配置的模板来搭建 Celo dApps（去中心化应用）。

## 使用场景

- 开始一个新的 Celo 项目
- 创建 MiniPay 迷你应用
- 设置 Farcaster 迷你应用
- 需要预配置的 Next.js + Web3 开发环境

## 快速入门

### 交互式模式

```bash
npx @celo/celo-composer@latest create
```

按照提示选择相应的选项。

### 带项目名称的模式

```bash
npx @celo/celo-composer@latest create my-celo-app
```

### 非交互式模式（使用命令行参数）

```bash
npx @celo/celo-composer@latest create my-celo-app \
  --template basic \
  --wallet-provider rainbowkit \
  --contracts hardhat
```

### 使用默认配置快速入门

```bash
npx @celo/celo-composer@latest create my-celo-app --yes
```

## 模板

| 模板 | 描述 | 使用场景 |
|----------|-------------|----------|
| `basic` | 标准的 Next.js 14+ dApp 模板 | 通用 Web3 应用 |
| `minipay` | 以移动端为主的 MiniPay 应用 | MiniPay 迷你应用 |
| `farcaster-miniapp` | Farcaster SDK + Frame 模板 | Farcaster 集成应用 |
| `ai-chat` | 独立的聊天应用 | 基于 AI 的 dApp |

### 创建 MiniPay 应用

```bash
npx @celo/celo-composer@latest create -t minipay
```

### 创建 Farcaster 迷你应用

```bash
npx @celo/celo-composer@latest create -t farcaster-miniapp
```

## 配置选项

### 钱包提供商

| 提供商 | 描述 |
|----------|-------------|
| `rainbowkit` | 流行的钱包连接界面（默认） |
| `thirdweb` | thirdweb Connect SDK |
| `none` | 不使用钱包提供商 |

### 智能合约

| 选项 | 描述 |
|--------|-------------|
| `hardhat` | Hardhat 开发环境（默认） |
| `foundry` | Foundry 开发环境 |
| `none` | 不使用智能合约 |

## 项目结构

```
my-celo-app/
├── apps/
│   ├── web/              # Next.js application
│   │   ├── app/          # App router pages
│   │   ├── components/   # React components
│   │   └── ...
│   └── contracts/        # Smart contracts (if selected)
│       ├── contracts/    # Solidity files
│       ├── scripts/      # Deployment scripts
│       └── test/         # Contract tests
├── packages/
│   ├── ui/               # Shared UI components
│   └── utils/            # Shared utilities
├── pnpm-workspace.yaml   # Workspace configuration
├── turbo.json            # Turborepo configuration
└── package.json
```

## 运行项目

```bash
cd my-celo-app

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build
```

## 技术栈

- **框架：** Next.js 14+（搭配 App Router） |
- **样式：** Tailwind CSS |
- **组件：** shadcn/ui |
- **代码管理工具：** Turborepo + PNPM |
- **编程语言：** TypeScript |
- **Web3 接口：** viem + wagmi（或 thirdweb）

## 系统要求

- Node.js 18.0.0 或更高版本 |
- 推荐使用 PNPM，或 npm/yarn

## 智能合约的开发

如果您选择了 Hardhat 或 Foundry：

### 使用 Hardhat 开发智能合约

```bash
# Navigate to contracts
cd apps/contracts

# Compile
npx hardhat compile

# Test
npx hardhat test

# Deploy to Celo Sepolia
npx hardhat run scripts/deploy.ts --network celoSepolia
```

### 使用 Foundry 开发智能合约

```bash
# Navigate to contracts
cd apps/contracts

# Build
forge build

# Test
forge test

# Deploy to Celo Sepolia
forge script script/Deploy.s.sol --rpc-url https://forno.celo-sepolia.celo-testnet.org --broadcast
```

## 环境变量配置

在 `apps/web/` 目录下创建 `.env.local` 文件：

```bash
# Required for wallet connection
NEXT_PUBLIC_WC_PROJECT_ID=your_walletconnect_project_id

# Optional: Alchemy API key
NEXT_PUBLIC_ALCHEMY_API_KEY=your_alchemy_key
```

在 `apps/contracts/` 目录下创建 `.env` 文件：

```bash
PRIVATE_KEY=your_private_key
CELOSCAN_API_KEY=your_celoscan_api_key
```

## 自定义功能

### 添加新页面

在 `apps/web/app/` 目录下创建相应的文件。

### 添加组件

将组件添加到 `apps/web/components/` 或共享的 `packages/ui/` 目录中。

## 额外资源

- [templates.md](references/templates.md) - 详细的模板使用说明