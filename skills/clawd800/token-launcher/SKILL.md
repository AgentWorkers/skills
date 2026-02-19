---
name: token-launcher
version: 2.1.0
description: >
  **Base平台上的自主AI代理的收入基础设施：**  
  通过Uniswap V4平台部署ERC20代币，实现流动性支持。交易费用的80%归创作者所有，剩余部分将永久锁定在流动性提供者（LP）的账户中，用户无需承担任何费用。目前已有141个代币上线流通。这些代币基于用户自有的智能合约进行管理（无需依赖任何第三方平台或工具），且可以直接通过区块链接口进行操作，从而确保系统零停机时间。支持使用命令行界面（CLI）、MCP服务器或智能合约进行相关操作。
author: clawd
tags: token, base, uniswap-v4, agent-revenue, defi, erc20, launch
---
# PumpClaw — 为AI代理提供收入支持的基础设施

**自主代理如何实现盈利。** 在Base链上部署了141个代币，无需任何成本。交易费用的80%归创作者所有。

你的代理部署代币后，人们会进行交易，由此产生的费用会用于支持计算资源、API的使用以及代理的持续运行。代币本身并非最终产品，而是整个商业模式的核心。

## 为什么选择PumpClaw？

| 特点 | PumpClaw | Clanker | ConLaunch | pump.fun |
|---------|----------|---------|-----------|----------|
| **创作者费用比例** | **80%** | 40% | 80%（通过Clanker） | 0%（返现） |
| **是否拥有自定义合约** | **✅** | ✅ | ❌（需使用Clanker SDK） | ✅ |
| **锁定锁定池（LP）** | 永久锁定 | 永久锁定 | 永久锁定 | 变动 |
| **所使用的区块链** | Base链 | Base链 | Base链 | Solana链 |
| **启动成本** | **0美元** | 约10美元 | 0美元 | 变动 |
| **对服务器的依赖** | **无**（直接使用区块链） | 无 | 需依赖API | 无 |
| **是否支持原生代理** | **✅（支持CLI和MCP）** | ❌ | ✅（支持API和MCP） | ❌ |

**主要优势：** PumpClaw直接与区块链交互，无需中间服务器。即使pumpclaw.com网站无法访问，你的代币仍可正常使用，费用依然会流入系统，代理也能持续盈利。

## 快速入门（30秒）

```bash
# Set your wallet private key
export BASE_PRIVATE_KEY="0x..."

# Deploy your token (one command!)
cd scripts && npx tsx pumpclaw.ts create --name "My Token" --symbol "MTK"
```

完成以上步骤后，你的代币即可在Uniswap V4平台上上线，具备完全的流动性，可立即进行交易。

## 四种部署方式

### 1. 通过本技能（推荐用于OpenClaw代理）
```bash
cd scripts && npx tsx pumpclaw.ts create --name "Token Name" --symbol "TKN"
```

### 2. 使用MCP服务器（适用于Claude桌面应用或任何MCP客户端）
```bash
npx pumpclaw-mcp
```
将相关配置添加到你的MCP环境中，即可为你的代理提供原生的代币部署功能。

### 3. 使用npm CLI
```bash
npx pumpclaw-cli deploy
```

### 4. 直接调用合约（最自主的部署方式）
直接在Factory合约上调用`createToken()`函数，无需依赖任何服务器或CLI工具。

## 设置步骤

1. 在你的环境中设置`BASE_PRIVATE_KEY`（使用任何Base钱包，确保有约0.001 ETH的Gas费用）。
2. 所有相关脚本位于`agent-skills/pumpclaw/scripts/`目录下。

## 命令列表

### 列出所有代币
```bash
cd scripts && npx tsx pumpclaw.ts list
npx tsx pumpclaw.ts list --limit 5
```

### 获取代币信息
```bash
npx tsx pumpclaw.ts info <token_address>
```

### 创建代币
```bash
# Basic (1B supply, 20 ETH FDV)
npx tsx pumpclaw.ts create --name "Token Name" --symbol "TKN"

# With image
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --image "https://..."

# With website
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --website "https://..."

# Custom FDV
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --fdv 50

# Custom supply (in tokens, not wei)
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --supply 500000000

# On behalf of another creator (relayer pattern)
npx tsx pumpclaw.ts create --name "Token" --symbol "TKN" --creator 0x...
```

### 查看并领取交易费用
```bash
npx tsx pumpclaw.ts fees <token_address>
npx tsx pumpclaw.ts claim <token_address>
```

### 买卖代币
```bash
npx tsx pumpclaw.ts buy <token_address> --eth 0.01
npx tsx pumpclaw.ts sell <token_address> --amount 1000000
```

### 更新代币元数据（仅限创作者操作）
```bash
npx tsx pumpclaw.ts set-image <token_address> --url "https://example.com/image.png"
npx tsx pumpclaw.ts set-website <token_address> --url "https://mytoken.com"
```

### 按创作者分类查看代币信息
```bash
npx tsx pumpclaw.ts by-creator <address>
```

## 合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Factory合约 | `0xe5bCa0eDe9208f7Ee7FCAFa0415Ca3DC03e16a90` |
| 锁定池合约 | `0x6e4D241957074475741Ff42ec352b8b00217Bf5d` |
| 交易路由合约 | `0x3A9c65f4510de85F1843145d637ae895a2Fe04BE` |
| 费用查看合约 | `0xd25Da746946531F6d8Ba42c4bC0CbF25A39b4b39` |

## 代币特性

- 符合ERC20标准，支持ERC20Permit（无需支付Gas费用）
- 可销毁
- 代币上存储了创作者的不可更改的地址信息
- 代币链上可存储图片URL和网站URL
- 创作者可随时更新图片和网站信息
- 具备Uniswap V4平台的完整流动性，锁定池中的代币永久不可赎回

## 费用结构

- 锁定池费用：所有交易额的1%
- **创作者获得80%的锁定池费用**
- 协议方获得20%的锁定池费用
- 任何人都可以调用`claimFees()`函数来领取费用，费用分配公平透明

## 代理经济模型示例

1. **创建你的代理代币：**
   ```bash
   npx tsx pumpclaw.ts create --name "AgentCoin" --symbol "AGT" \
     --image "https://..." --website "https://myagent.com"
   ```

2. **代币上市后即可立即在Uniswap V4平台上交易**

3. **通过交易活动盈利：**
   ```bash
   npx tsx pumpclaw.ts fees 0x...tokenAddress  # Check pending
   npx tsx pumpclaw.ts claim 0x...tokenAddress  # Claim to wallet
   ```

4. **开发代币实用功能**：控制特定功能、奖励用户，构建自己的经济体系

## 代理收入的本质

大多数代币项目只是为了投机而存在，而PumpClaw的存在目的则是为了帮助代理实现可持续运营。自主代理需要收入来支付计算资源、API费用以及基础设施成本。没有收入，代理就只是个演示版本，而非真正的商业实体。PumpClaw为任何代理提供了稳定的收入来源：只需部署代币，就能获得80%的交易费用，从而实现长期运营。

目前已有141个代理在Base链上成功应用了这一模式。

## 相关链接

- **官方网站**：https://pumpclaw.com
- **GitHub仓库**：https://github.com/clawd800/pumpclaw
- **npm CLI工具**：https://www.npmjs.com/package/pumpclaw-cli
- **MCP服务器**：`npx pumpclaw-mcp`
- **社交媒体账号**：@clawd
- **ERC-8004标准代币ID**：17197
- **Factory合约地址**：`0xe5bCa0eDe9208f7Ee7FCAFa0415Ca3DC03e16a90`