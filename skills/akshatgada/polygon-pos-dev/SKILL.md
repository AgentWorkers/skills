---
name: polygon-pos-dev
description: **Polygon PoS区块链开发综合指南**  
本指南适用于在Polygon平台上部署智能合约、在Amoy测试网上进行测试、通过矿池获取测试代币，以及在Polygonscan平台上验证合约的操作。同时，本指南还提供了与Foundry框架相关的部署脚本和测试策略支持。
---

# Polygon权益证明（PoS）开发指南

本指南提供了使用Foundry在Polygon权益证明（PoS）区块链上开发和部署智能合约的端到端流程。

## 概述

Polygon PoS是一个兼容以太坊EVM的权益证明侧链，具有以下特点：
- 低交易成本（仅需几分钱）
- 快速的区块生成时间（约2秒）
- 高吞吐量（理论峰值超过65,000 TPS）
- 完全兼容以太坊的工具链
- 使用POL代币作为交易手续费

**默认网络**：Amoy测试网（链ID：80002）——在主网部署前请使用此网络进行所有测试。

---

## 快速导航

**适用于代理/快速部署**：请跳转至[快速启动路径](#quick-start-path)（耗时5-10分钟）

**适用于生产环境/全面测试**：请跳转至[完整开发路径](#complete-development-path)（耗时30-60分钟）

**参考资料**：请参阅以下章节了解[网络配置](#network-configuration)、[获取测试网代币](#getting-testnet-tokens)和[故障排除](#troubleshooting)。

---

## 两种开发路径

根据您的需求选择合适的路径：

| 开发路径 | 快速启动路径 | 完整开发路径 |
|--------|------------------|---------------------------|
| **耗时** | 5-10分钟 | 30-60分钟 |
| **适用场景** | 原型开发、简单合约 | 生产环境、复杂系统 |
| **测试内容** | 基本编译检查 | 单元测试、集成测试、分叉测试 |
| **使用的脚本** | 无需额外脚本（直接使用Foundry命令） | 使用Foundry的所有命令 |
| **文档支持** | 最少文档 | 全面参考指南 |
| **验证方式** | 部署时自动验证 | 多种验证方法 |
| **代理友好程度** | ✅ 高速优化 | ⚠️ 全面但耗时较长 |

### 路径1：快速启动（最短时间 - 适合代理使用）
**适用场景**：快速部署、简单合约、原型开发
**耗时**：5-10分钟
**结果**：合约在测试网上部署并经过验证

请跳转至[快速启动路径](#quick-start-path)。

### 路径2：完整开发路径（全面开发流程）
**适用场景**：生产环境合约、复杂系统、全面测试
**耗时**：30-60分钟
**结果**：经过全面测试、优化的合约，准备好在生产环境中使用

请跳转至[完整开发路径](#complete-development-path)。

---

## 快速启动路径

**目标**：以最少的步骤将合约部署到Polygon Amoy测试网。

### 先决条件

- 安装了Foundry：`curl -L https://foundry.paradigm.xyz | bash && foundryup`
- 拥有包含私钥的钱包
- Polygonscan API密钥（从https://polygonscan.com/myapikey获取）

### 第1步：创建项目（30秒）

```bash
forge init my-polygon-project
cd my-polygon-project
```

### 第2步：配置环境（1分钟）

创建`.env`文件：
```bash
PRIVATE_KEY=your_private_key_without_0x_prefix
```

### 第3步：获取测试网代币（2分钟）

访问：https://www.alchemy.com/faucets/polygon-amoy
- 输入您的钱包地址
- 领取0.2-0.5 POL代币（无需注册）

### 第4步：部署（1分钟）

```bash
# Deploy to Amoy testnet
forge script script/Counter.s.sol:CounterScript \
    --rpc-url https://rpc-amoy.polygon.technology \
    --private-key $PRIVATE_KEY \
    --broadcast
```

**完成！**您的合约已部署并在Amoy测试网上验证。

查看地址：`https://amoy.polygonscan.com/address/YOUR_CONTRACT_ADDRESS`

---

## 完整开发路径

**目标**：完成全面测试和优化的合约部署，准备好在生产环境中使用。

### 第1阶段：设置（5分钟）

1. **安装Foundry**：
```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

2. **初始化项目**：
```bash
forge init my-polygon-project
cd my-polygon-project
```

3. **配置Polygon环境**：
更新`foundry.toml`文件以配置Polygon相关设置：
```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.24"
optimizer = true
optimizer_runs = 200

[rpc_endpoints]
amoy = "https://rpc-amoy.polygon.technology"
polygon = "https://polygon-rpc.com"

[etherscan]
amoy = { key = "${POLYGONSCAN_API_KEY}", url = "https://api-amoy.polygonscan.com/api" }
polygon = { key = "${POLYGONSCAN_API_KEY}", url = "https://api.polygonscan.com/api" }
```

4. **配置环境**：
创建`.env`文件：
```bash
PRIVATE_KEY=your_private_key
WALLET_ADDRESS=0xYourAddress
POLYGONSCAN_API_KEY=your_api_key
```

### 第2阶段：编写和测试合约（10-20分钟）

1. **编写合约**（或使用`assets/sample-contracts/HelloWorld.sol`作为模板）
2. **编写测试用例**：
```solidity
// test/MyContract.t.sol
import "forge-std/Test.sol";
import "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;
    
    function setUp() public {
        myContract = new MyContract();
    }
    
    function testDeployment() public {
        assertEq(myContract.owner(), address(this));
    }
}
```

3. **运行测试**：
```bash
forge test -vvv                    # Run tests
forge test --gas-report            # Check gas usage
forge coverage                     # Check coverage
```

4. **分叉测试**（可选）：
```bash
# Test against real Polygon state
forge test --fork-url https://polygon-rpc.com
```

详细测试策略请参阅`references/testing-strategies.md`。

### 第3阶段：获取测试网代币（2-5分钟）

访问以下其中一个代币发放平台：

**Alchemy**（推荐 - 无需认证）：https://www.alchemy.com/faucets/polygon-amoy
**QuickNode**：https://faucet.quicknode.com/polygon/amoy
**GetBlock**：https://getblock.io/faucet/matic-amoy/
**Chainlink**：https://faucets.chain.link/polygon-amoy
**LearnWeb3**：https://learnweb3.io/faucets/polygon_amoy/

### 第4阶段：部署到测试网（2-5分钟）
在`script/Deploy.s.sol`中创建部署脚本：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Script.sol";
import "../src/YourContract.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        
        vm.startBroadcast(deployerPrivateKey);
        
        // Deploy your contract
        YourContract yourContract = new YourContract();
        
        vm.stopBroadcast();
        
        console.log("Contract deployed to:", address(yourContract));
    }
}
```

有关高级部署策略，请参阅`references/foundry-deployment.md`。

### 第5阶段：验证合约（1-2分钟）

如果部署过程中未通过验证：
```bash
forge verify-contract \
    CONTRACT_ADDRESS \
    src/MyContract.sol:MyContract \
    --chain-id 80002 \
    --etherscan-api-key $POLYGONSCAN_API_KEY
```

有关验证问题的解决方法，请参阅`references/contract-verification.md`。

### 第6阶段：在测试网上测试（5-10分钟）

1. **在浏览器中查看合约**：https://amoy.polygonscan.com/address/CONTRACT_ADDRESS
2. **与合约交互**：使用Cast或Web界面
3. **测试所有功能**：确保合约行为符合预期
4. **监控交易费用**：检查是否需要优化

### 第7阶段：部署到主网（5分钟）

**⚠️ 重要提示：请先完成主网部署前的检查！**

请参阅[主网部署检查清单](#mainnet-deployment-checklist)。

```bash
forge script script/Deploy.s.sol \
    --rpc-url polygon \
    --private-key $PRIVATE_KEY \
    --broadcast \
    --verify \
    --etherscan-api-key $POLYGONSCAN_API_KEY
```

**完整开发路径结束 ✅**

## 网络配置

### Amoy测试网（推荐用于测试）

| 参数 | 值 |
|----------|-------|
| 网络名称 | Polygon Amoy |
| 链ID | 80002 |
| 货币 | POL |
| RPC地址 | https://rpc-amoy.polygon.technology |
| WebSocket地址 | wss://polygon-amoy.drpc.org |
| 浏览器 | https://amoy.polygonscan.com |
| 代币发放平台 | 多个（详见下文） |

### Polygon主网

| 参数 | 值 |
|----------|-------|
| 网络名称 | Polygon |
| 链ID | 137 |
| 货币 | POL |
| RPC地址 | https://polygon-rpc.com |
| WebSocket地址 | wss://polygon.drpc.org |
| 浏览器 | https://polygonscan.com |

## 获取测试网代币

有多种途径可以获取Amoy测试网的POL代币。

### 快速获取代币

运行代币发放脚本：
```bash
./scripts/get-testnet-tokens.sh
```

### 可用的代币发放平台

**Alchemy代币发放平台**（推荐 - 无需认证）：
- URL：https://www.alchemy.com/faucets/polygon-amoy
- 每日发放量：0.5 POL（有账户时）/0.2 POL（无账户时）
- 无额外要求

**QuickNode代币发放平台**：
- URL：https://faucet.quicknode.com/polygon/amoy
- 每日发放量：0.1 POL（使用Twitter可额外获取0.1 POL）
- 需要连接钱包

**GetBlock代币发放平台**：
- URL：https://getblock.io/faucet/matic-amoy/
- 每日发放量：0.1 POL
- 需要登录

**Chainlink代币发放平台**：
- URL：https://faucets.chain.link/polygon-amoy
- 每日发放量：0.1 POL
- 需要GitHub认证

**Tips**：
- 大多数代币发放平台每天限制请求次数
- 如果遇到请求限制，请尝试其他平台
- 有些平台提供推特推广奖励

## 部署流程

### 环境配置

创建`.env`文件（参考`assets/sample-contracts/.env.example`）：
```bash
PRIVATE_KEY=your_private_key_here
WALLET_ADDRESS=0xYourAddress
POLYGONSCAN_API_KEY=your_api_key_here
```

将`.env`文件添加到`.gitignore`中：
```
.env
broadcast/
deployments/
```

### 部署到测试网

**选项1：使用辅助脚本**（推荐）：
```bash
./scripts/deploy-foundry.sh
```

**选项2：手动部署**：
```bash
forge script script/Deploy.s.sol \
    --rpc-url amoy \
    --private-key $PRIVATE_KEY \
    --broadcast \
    --verify
```

**选项3：不进行验证直接部署**：
```bash
forge script script/Deploy.s.sol \
    --rpc-url amoy \
    --private-key $PRIVATE_KEY \
    --broadcast
```

### 部署到主网

**⚠️ 重要提示：请先在Amoy测试网上进行充分测试！**

请参阅`references/foundry-deployment.md`以获取详细部署指南。

## 测试策略

### 本地测试

在`test/`目录中编写测试用例：
```solidity
// test/MyContract.t.sol
import "forge-std/Test.sol";
import "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;
    
    function setUp() public {
        myContract = new MyContract();
    }
    
    function testFunction() public {
        // Test logic
    }
}
```

运行测试：
```bash
forge test              # Run all tests
forge test -vvv         # Verbose output
forge test --gas-report # Show gas usage
```

### 分叉测试

在真实的Polygon环境中测试合约：
```bash
forge test --fork-url https://polygon-rpc.com
```

### 在测试网上测试

将合约部署到Amoy测试网，并使用真实交易进行测试。详细测试策略请参阅`references/testing-strategies.md`。

## 合约验证

验证可以提升合约代码的公开性和可信度。

### 部署过程中的验证（推荐）
```bash
forge script script/Deploy.s.sol \
    --rpc-url amoy \
    --private-key $PRIVATE_KEY \
    --broadcast \
    --verify \
    --etherscan-api-key $POLYGONSCAN_API_KEY
```

### 部署后的验证

**选项1：使用辅助脚本**：
```bash
./scripts/verify-contract.sh
```

**选项2：手动验证**：
```bash
forge verify-contract \
    CONTRACT_ADDRESS \
    src/MyContract.sol:MyContract \
    --chain-id 80002 \
    --etherscan-api-key $POLYGONSCAN_API_KEY \
    --verifier-url https://api-amoy.polygonscan.com/api
```

### 使用构造函数参数

有关验证问题的解决方法，请参阅`references/contract-verification.md`。

## 常见工作流程

### 应选择哪种开发路径？

**何时使用快速启动路径**：
- 需要快速部署（原型开发、简单合约）
- 合约简单且风险较低
- 作为时间有限的AI代理
- 测试工作较少或已在其他地方完成

**何时使用完整开发路径**：
- 部署到主网
- 合约涉及实际价值
- 合约逻辑复杂，需要全面测试
- 需要团队协作和代码审查
- 安全性要求高

### 主网部署前的检查清单

在部署到主网之前，请确保完成以下事项：
- 所有测试通过（`forge test`）
- 合约已在Amoy测试网上部署并经过测试
- 合约在Amoy上通过验证
- 安全审查完成
- 优化工作完成
- 文档齐全
- 构造函数参数已仔细检查
- 钱包中有足够的POL代币用于支付交易费用
- 部署脚本已测试
- 团队已收到部署通知

## 合约示例结构

以下是适用于Polygon的智能合约示例结构：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract HelloWorld {
    address public owner;
    string public message;
    uint256 public updateCount;
    
    event MessageUpdated(address indexed updater, string newMessage);
    
    error NotOwner();
    error EmptyMessage();
    
    constructor(string memory initialMessage) {
        owner = msg.sender;
        message = initialMessage;
    }
    
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }
    
    function setMessage(string calldata newMessage) external {
        if (bytes(newMessage).length == 0) revert EmptyMessage();
        message = newMessage;
        updateCount++;
        emit MessageUpdated(msg.sender, newMessage);
    }
}
```

**关键提示**：
- 使用自定义错误处理机制而非`require`语句（更节省Gas）
- 对重要状态变化触发事件
- 使用访问控制修饰符
- 优化合约以适应Polygon的低Gas成本

## 安全规则

1. **先进行测试**：始终在Amoy测试网上进行测试
2. **切勿提交私钥**：将`.env`文件添加到`.gitignore`中
3. **验证合约**：确保合约代码的透明性和安全性
4. **检查网络配置**：在部署前仔细核对链ID
5. **确保有足够的余额**：确保有足够的POL代币支付交易费用
6. **记录合约地址**：保存已部署的合约地址
7. **代码审计**：在部署前进行安全审查
8. **使用脚本**：自动化部署流程以减少错误
9. **备份私钥**：安全地备份私钥
10. **先在测试网上验证合约**：确保合约在测试网上的行为正确

## 故障排除

### 缺乏足够交易费用

**错误**：`insufficient funds for gas * price + value`

**解决方法**：从代币发放平台获取测试网代币（运行`./scripts/get-testnet-tokens.sh`）

### 合约未找到

**错误**：`src/MyContract.sol: MyContract not found`

**解决方法**：确认文件路径和合约名称是否正确

### RPC连接问题

**错误**：`failed to get chain id`

**解决方法**：
- 检查网络连接
- 尝试使用其他RPC地址
- 使用专门的RPC服务提供商（如Alchemy、QuickNode）

### 验证失败

**错误**：`bytecode does not match`

**解决方法**：
- 等待1-2分钟，直到合约被索引
- 确认构造函数参数正确
- 检查编译器配置是否与部署设置一致

### Gas费用估算失败

**错误**：`gas estimation failed`

**解决方法**：
- 检查合约逻辑中是否存在可能导致Gas费用过高的情况
- 确保账户余额充足
- 检查函数参数设置

## 资源

**Foundry文档**：
- 官方文档：https://book.getfoundry.sh/
- GitHub仓库：https://github.com/foundry-rs/foundry

**Polygon文档**：
- 官方文档：https://docs.polygon.technology/
- Gas费用计算工具：https://gasstation.polygon.technology/
- 代币发放平台：https://faucet.polygon.technology/

**区块浏览器**：
- Amoy测试网：https://amoy.polygonscan.com
- 主网：https://polygonscan.com

**RPC服务提供商**：
- Alchemy：https://www.alchemy.com/
- QuickNode：https://www.quicknode.com/
- Infura：https://infura.io/

**社区**：
- Discord：https://discord.com/invite/0xPolygonCommunity
- Telegram：https://t.me/polygonhq

## 参考文件

- `references/foundry-deployment.md`：完整部署指南
- `references/testing-strategies.md`：测试最佳实践
- `references/contract-verification.md`：合约验证与故障排除

## 脚本**

---

（由于提供的SKILL.md文件内容主要为Markdown格式的指令和链接，翻译时保持了原有的结构和格式。如果需要进一步细化或解释某些部分，可以提供更多上下文。）