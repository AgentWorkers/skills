---
name: ethereum-wingman
description: Ethereum开发教程及Scaffold-ETH 2项目的构建工具。会在执行“build”、“create”、“dApp”、“smart contract”、“Solidity”、“DeFi”、“Ethereum”、“web3”或任何区块链开发相关任务时触发该工具。始终采用“fork模式”来测试代码在实际协议状态下的运行情况。
license: MIT
metadata:
  author: BuidlGuidl
  version: "2.0.0"
---

# Ethereum Wingman

这是一份全面的 Ethereum 开发指南，专为 AI 代理程序设计。内容涵盖了智能合约开发、去中心化金融（DeFi）协议、安全最佳实践以及 SpeedRun Ethereum 的学习课程。

---

## AI 代理程序使用说明 - 请先阅读此部分

### 默认开发环境：Scaffold-ETH 2（使用 Fork 模式）

当用户想要构建任何 Ethereum 项目时，请按照以下步骤操作：

**步骤 1：创建项目**

```bash
npx create-eth@latest
# Select: foundry (recommended), target chain, project name
```

**步骤 2：调整轮询间隔**

编辑 `packages/nextjs/scaffold.config.ts` 文件，并将以下内容修改为：
```typescript
pollingInterval: 30000,  // Default: 30 seconds (way too slow!)
```

**步骤 3：安装并创建一个实时运行环境（Live Network）**

```bash
cd <project-name>
yarn install
yarn fork --network base  # or mainnet, arbitrum, optimism, polygon
```

**步骤 4：启用自动区块挖掘功能（必须执行！）**

```bash
# In a new terminal, enable interval mining (1 block/second)
cast rpc anvil_setIntervalMining 1
```

如果不启用此功能，`block.timestamp` 的值将保持不变，导致依赖时间相关的逻辑出现错误！

**可选：** 通过编辑 `packages/foundry/package.json` 文件，在 fork 脚本中添加 `--block-time 1` 选项，使该功能永久生效。

**步骤 5：将项目部署到本地环境（免费！）**

```bash
yarn deploy
```

**步骤 6：启动前端应用**

```bash
yarn start
```

**步骤 7：测试前端应用**

启动前端应用后，请在浏览器中执行以下操作：
1. 访问 `http://localhost:3000`
2. 获取页面元素（燃烧器钱包地址位于页面头部）
3. 点击“fountain”按钮，向燃烧器钱包充值 ETH
4. 如有需要，可以使用页面上的燃烧器地址从其他用户那里转移代币
5. 测试应用程序的各项功能

建议使用 `cursor-browser-extension` 和 MCP 工具进行浏览器自动化测试。详细的工作流程请参阅 `tools/testing/frontend-testing.md` 文件。

### 注意事项：
- **不要使用 `yarn chain` 命令**，请使用 `yarn fork --network <chain>` 命令！
- **不要手动运行 `forge init` 命令，也不要从头开始配置 Foundry**
- **不要手动创建 Next.js 项目**，因为 Scaffold-ETH 2 已经完成了这些配置
- **无需手动配置钱包连接**，SE2 版本已经预配置了 RainbowKit 工具。

### 为什么使用 Fork 模式？

```
yarn chain (WRONG)              yarn fork --network base (CORRECT)
└─ Empty local chain            └─ Fork of real Base mainnet
└─ No protocols                 └─ Uniswap, Aave, etc. available
└─ No tokens                    └─ Real USDC, WETH exist
└─ Testing in isolation         └─ Test against REAL state
```

---

## 数据存储位置

代币信息、协议详情以及重要用户（如“鲸鱼用户”）的地址存储在 `data/addresses/` 目录下：
- `tokens.json`：包含各链路的 WETH、USDC、DAI 等代币信息
- `protocols.json`：包含各链路的 Uniswap、Aave、Chainlink 等协议信息
- `whales.json`：包含用于测试充值的大型代币持有者信息

---

## 最重要的概念

**在 Ethereum 上，没有任何操作是自动执行的**

智能合约无法自行执行任务。没有 cron 任务、调度器或后台进程。对于任何需要执行的操作，都必须：
1. 确保 **任何人** 都能够调用该功能（而不仅仅是管理员）
2. 为调用者提供明确的 **动机**（例如利润、奖励或自身利益）
3. 设计足够的 **激励机制**，以覆盖执行合约所需的 gas 费用及潜在收益

**务必思考：** “是谁调用了这个函数？他们为什么要支付 gas 费用？” 如果无法回答这个问题，那么这个函数很可能永远不会被执行。

### 正确的激励机制设计示例

```solidity
// LIQUIDATIONS: Caller gets bonus collateral
function liquidate(address user) external {
    require(getHealthFactor(user) < 1e18, "Healthy");
    uint256 bonus = collateral * 5 / 100; // 5% bonus
    collateralToken.transfer(msg.sender, collateral + bonus);
}

// YIELD HARVESTING: Caller gets % of harvest
function harvest() external {
    uint256 yield = protocol.claimRewards();
    uint256 callerReward = yield / 100; // 1%
    token.transfer(msg.sender, callerReward);
}

// CLAIMS: User wants their own tokens
function claimRewards() external {
    uint256 reward = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    token.transfer(msg.sender, reward);
}
```

---

## 需要牢记的关键注意事项

### 1. 代币的小数位数

**USDC 的小数位数为 6 位，而不是 18 位！**

**常见代币的小数位数：**
- USDC、USDT：6 位
- WBTC：8 位
- 大多数代币（如 DAI、WETH）：18 位

### 2. 必须遵循 ERC-20 标准的批准流程

智能合约不能直接提取代币，必须通过两步流程来完成操作：

```solidity
// Step 1: User approves
token.approve(spenderContract, amount);

// Step 2: Contract pulls tokens
token.transferFrom(user, address(this), amount);
```

**切勿使用无限次的批准请求（infinite approvals）！**

```solidity
// DANGEROUS
token.approve(spender, type(uint256).max);

// SAFE
token.approve(spender, exactAmount);
```

### 3. Solidity 语言中不允许使用浮点数**

在 Solidity 代码中，应使用基点（1 bp = 0.01%）来表示小数。

```solidity
// BAD: This equals 0
uint256 fivePercent = 5 / 100;

// GOOD: Basis points
uint256 FEE_BPS = 500; // 5% = 500 basis points
uint256 fee = (amount * FEE_BPS) / 10000;
```

### 4. 注意重入攻击（Reentrancy Attacks）

外部调用可能会触发合约的再次执行，因此必须采取防护措施：

```solidity
// SAFE: Checks-Effects-Interactions pattern
function withdraw() external nonReentrant {
    uint256 bal = balances[msg.sender];
    balances[msg.sender] = 0; // Effect BEFORE interaction
    (bool success,) = msg.sender.call{value: bal}("");
    require(success);
}
```

建议始终使用 OpenZeppelin 提供的 ReentrancyGuard 库来防止重入攻击。

### 5. 不要将 DEX 的实时价格作为预言机（Oracles）使用

因为闪存贷款（flash loans）可以瞬间操纵市场价格。

```solidity
// SAFE: Use Chainlink
function getPrice() internal view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < 3600, "Stale");
    require(price > 0, "Invalid");
    return uint256(price);
}
```

### 6. 注意“金库膨胀攻击”（Vault Inflation Attacks）

第一个存入资金的用户可能通过操控份额来窃取其他用户的资金：

```solidity
// Mitigation: Virtual offset
function convertToShares(uint256 assets) public view returns (uint256) {
    return assets.mulDiv(totalSupply() + 1e3, totalAssets() + 1);
}
```

### 7. 使用 SafeERC20 标准

某些代币（如 USDT）在转账时不会返回布尔值（bool），因此需要特别注意。

---

## Scaffold-ETH 2 开发环境

### 项目结构

```
packages/
├── foundry/              # Smart contracts
│   ├── contracts/        # Your Solidity files
│   └── script/           # Deploy scripts
└── nextjs/
    ├── app/              # React pages
    └── contracts/        # Generated ABIs + externalContracts.ts
```

### 必需使用的钩子（Hooks）

```typescript
// Read contract data
const { data } = useScaffoldReadContract({
  contractName: "YourContract",
  functionName: "greeting",
});

// Write to contract
const { writeContractAsync } = useScaffoldWriteContract("YourContract");

// Watch events
useScaffoldEventHistory({
  contractName: "YourContract",
  eventName: "Transfer",
  fromBlock: 0n,
});
```

---

## SpeedRun Ethereum 学习挑战

以下是用于实践学习的挑战任务及相关概念：
| 挑战 | 相关概念 | 关键学习点 |
|---------|---------|------------|
| 0: 简单的非同质化代币（NFT） | ERC-721 | 创建 NFT、元数据、tokenURI 的使用 |
| 1: 质押（Staking） | 协调机制 | 截止时间、托管机制、阈值设置 |
| 2: 代币交易（Token Trading） | ERC-20 | 批准流程、买卖操作 |
| 3: 骰子游戏（Dice Game） | 随机性实现 | 在链上实现随机性存在安全风险 |
| 4: 去中心化交易所（DEX） | 自动市场机制（AMM） | x*y=k 的计算公式、滑点问题 |
| 5: 预言机（Oracles） | 价格数据来源 | 使用 Chainlink 服务并防止数据被操纵 |
| 6: 借贷（Lending） | 抵押品管理 | 健康因子（health factor）、清算机制 |
| 7: 稳定币（Stablecoins） | 价格固定机制 | 使用 CDP 技术、超额抵押策略 |
| 8: 预测市场（Prediction Markets） | 结果判定 | 如何确定预测结果 |
| 9: 基于零知识证明的投票（ZK Voting） | 隐私保护 | 使用零知识证明技术 |
| 10: 多重签名（Multisig） | 安全性增强 | 多重签名机制的实现 |
| 11: SVG 格式的非同质化代币（SVG NFT） | 在链上生成艺术品 | 使用 SVG 格式进行艺术创作、Base64 编码 |

---

## 去中心化金融（DeFi）协议示例

### Uniswap（自动市场机制，AMM）

- 使用固定公式：x * y = k
- 必须提供滑点保护机制
- LP（Lending Pool）代币代表用户的投资份额

### Aave（借贷服务）

- 提供抵押品以获取贷款
- 健康因子（Health Factor） = 抵押品价值 / 债务价值
- 当健康因子低于 1 时触发清算

### ERC-4626（代币化金库）

- 用于管理收益生成型金库的标准接口
- 支持存款和取款操作，并记录用户的投资份额
- 提供防护机制，防止金库膨胀攻击

---

## 安全性审查清单

在部署项目之前，请检查以下内容：
- **所有管理员功能是否具备访问控制**  
- **是否实现了重入保护（Reentrancy Protection，包括 CEI 和 nonReentrant 措施）**  
- **代币的小数位数是否处理正确**  
- **预言机数据是否安全可靠**  
- **是否防止了整数溢出问题（使用 SafeMath 库）**  
- **返回值是否经过验证（符合 SafeERC20 标准）**  
- **是否对输入进行了有效验证**  
- **状态变化是否会触发事件通知**  
- **维护相关功能是否设计了合理的激励机制**  

---

## 帮助开发者的建议

在协助开发者时，请遵循以下原则：
1. **严格按照 Fork 开发流程操作**，始终使用 `yarn fork` 命令，切勿使用 `yarn chain`  
2. **直接回答问题**，先理解他们的需求再提供解决方案  
3. **展示实际代码示例**，帮助他们理解实现细节  
4. **提前提醒潜在的安全风险**  
5. **推荐相关学习资源**，引导他们参考 SpeedRun Ethereum 的实践案例  
6. **询问激励机制的实现细节**，对于任何“自动执行”的功能，务必询问调用者及其背后的动机