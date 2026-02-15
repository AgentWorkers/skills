---
name: arbitrum-dapp-skill
description: 这是一份关于如何使用 Stylus（Rust）和/或 Solidity 在 Arbitrum 上构建去中心化应用（dApps）的详细指南。内容涵盖了本地开发环境的搭建、合约的开发与测试、合约的部署，以及如何将 React 前端与 viem 框架集成。无论你是刚开始一个新的 Arbitrum 项目，还是需要编写 Stylus 或 Solidity 合约、将合约部署到 Arbitrum，或者想要构建一个能够与 Arbitrum 合约交互的前端应用，这份指南都非常实用。
---

# Arbitrum dApp 开发

## 技术栈

| 层次 | 工具 | 说明 |
|-------|------|-------|
| 智能合约（Rust） | `stylus-sdk` v0.10+ | 编译为 WASM，运行在 Stylus 虚拟机上 |
| 智能合约（Solidity） | Solidity 0.8.x + Foundry | Arbitrum 上的标准 EVM 方案 |
| 本地节点 | `nitro-devnode` | 基于 Docker 的 Arbitrum 本地开发环境 |
| 合约命令行工具 | `cargo-stylus` | 用于检查、部署和导出合约的 ABI 文件 |
| 合约开发工具链 | Foundry（`forge`、`cast`、`anvil`） | 用于构建、测试和部署 Solidity 合约 |
| 前端框架 | React / Next.js + viem + wagmi | 使用 viem 进行与链路的交互 |
| 包管理器 | pnpm | 适用于开发环境，部署速度快 |

## 决策流程

在开始新合约的开发时：

1. **需要最高性能/较低 gas 费用？** → 选择 Stylus Rust。请参阅 `references/stylus-rust-contracts.md`。
2. **需要广泛的工具兼容性/快速原型开发？** → 选择 Solidity。请参阅 `references/solidity-contracts.md`。
3. **混合使用？** → 可以同时使用 Stylus 和 Solidity。Arbitrum 上的 Stylus 和 Solidity 合约可以完全互操作。

## 项目架构

### 单一仓库（推荐）

```
my-arbitrum-dapp/
├── apps/
│   ├── frontend/            # React / Next.js app
│   ├── contracts-stylus/    # Rust Stylus contracts
│   ├── contracts-solidity/  # Foundry Solidity contracts
│   └── nitro-devnode/       # Local dev chain (git submodule)
├── pnpm-workspace.yaml
└── package.json
```

### 开发初始步骤

```bash
# 1. Create workspace
mkdir my-arbitrum-dapp && cd my-arbitrum-dapp
pnpm init
printf "packages:\n  - 'apps/*'\n" > pnpm-workspace.yaml

# 2. Local devnode
git clone https://github.com/OffchainLabs/nitro-devnode.git apps/nitro-devnode
cd apps/nitro-devnode && ./run-dev-node.sh && cd ../..

# 3a. Stylus contract
cargo stylus new apps/contracts-stylus

# 3b. Solidity contract
cd apps && forge init contracts-solidity && cd ..

# 4. Frontend
pnpm create next-app apps/frontend --typescript
cd apps/frontend
pnpm add viem wagmi @tanstack/react-query
```

## 核心工作流程

### Stylus Rust

```bash
# Validate
cargo stylus check --endpoint http://localhost:8547

# Deploy (uses the nitro-devnode pre-funded deployer account)
cargo stylus deploy \
  --endpoint http://localhost:8547 \
  --private-key $PRIVATE_KEY

# Export ABI for frontend consumption
cargo stylus export-abi
```

### Solidity（使用 Foundry）

```bash
# Build
forge build

# Test
forge test

# Deploy locally (uses the nitro-devnode pre-funded deployer account)
forge script script/Deploy.s.sol --rpc-url http://localhost:8547 --broadcast \
  --private-key $PRIVATE_KEY
```

> **注意：** `nitro-devnode` 配备了预付费的部署账户。默认的私钥和地址请参阅 `references/local-devnode.md`。在测试网/主网上，请使用自己的私钥（切勿硬编码敏感信息）。

### 前端（使用 viem 和 wagmi）

```typescript
import { createPublicClient, http } from "viem";
import { arbitrumSepolia } from "viem/chains";

const client = createPublicClient({
  chain: arbitrumSepolia,
  transport: http(),
});

// Read from contract
const result = await client.readContract({
  address: "0x...",
  abi: contractAbi,
  functionName: "myFunction",
});
```

有关使用 wagmi 的完整示例（包括与链路的交互、钱包连接和交易编写），请参阅 `referencesfrontend-integration.md`。

## 开发原则

- **始终使用 viem** 进行与链路的交互。
- **在部署到测试网之前，先在本地环境中进行测试**。
- 从 Stylus（通过 `cargo stylus export-abi`）和 Solidity（通过 `forge inspect`）导出 ABI 文件，并将其保存在前端可以导入的共享位置。
- **使用环境变量** 来配置 RPC URL、合约地址和私钥。切勿硬编码敏感信息。
- **Stylus 合约与 Solidity 合约兼容**：它们共享相同的地址空间、存储模型和 ABI 编码，因此跨合约调用可以无缝进行。

## 参考资料

如需更详细的指导，请查阅以下文档：

- `references/stylus-rust-contracts.md` — Stylus SDK 的使用模式、存储机制和入口点
- `references/solidity-contracts.md` — Arbitrum 上的 Solidity 开发指南及 Foundry 工作流程
- `references/frontend-integration.md` — React + viem + wagmi 的集成方案
- `references/local-devnode.md` — Nitro devnode 的设置、账户管理和调试方法
- `references/deployment.md` — 在测试网和主网上部署合约的流程
- `references/testing.md` — Stylus 和 Solidity 合约的测试策略