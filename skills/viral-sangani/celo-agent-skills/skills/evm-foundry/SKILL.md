---
name: evm-foundry
description: Foundry 是用于开发以太坊虚拟机（EVM）链的工具，支持 Celo 等区块链平台。在使用 Foundry 时，可以执行以下操作：使用 forge 和 cast 工具进行代码编译；编写 Solidity 合同；进行合同测试；部署合同；以及验证合同的正确性。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# 用于EVM链的Foundry开发

本技能涵盖了如何为兼容EVM的区块链（尤其是Celo）设置和开发Foundry环境。

## 使用场景

- 设置新的Foundry项目
- 使用forge工具编写和编译Solidity智能合约
- 使用forge test工具测试合约
- 将合约部署到Celo或其他EVM链上
- 在区块浏览器中验证合约
- 使用cast工具与合约进行交互

## Foundry工具

| 工具 | 功能 |
|------|---------|
| forge | 构建、测试、调试、部署和验证智能合约 |
| cast | 通过CLI与合约交互并检索链上数据 |
| anvil | 运行支持分叉功能的本地Ethereum开发节点 |
| chisel | 快速的Solidity交互式开发环境（REPL） |

## 安装

```bash
# Install Foundryup (the Foundry installer)
curl -L https://foundry.paradigm.xyz | bash

# Install Foundry tools
foundryup
```

在Windows系统上，建议使用Git BASH或WSL（Foundryup不支持PowerShell或Command Prompt）。

## 快速入门

### 初始化项目

```bash
forge init my-project
cd my-project
```

### 项目结构

```
my-project/
├── foundry.toml      # Configuration
├── src/              # Contract source files
│   └── Counter.sol
├── test/             # Test files
│   └── Counter.t.sol
├── script/           # Deployment scripts
│   └── Counter.s.sol
└── lib/              # Dependencies
```

## Celo网络信息

| 网络 | 链ID | RPC端点 |
|---------|----------|--------------|
| Celo主网 | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |

## 配置

### Celo的foundry.toml配置文件

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.28"
optimizer = true
optimizer_runs = 200

[rpc_endpoints]
celo = "https://forno.celo.org"
celo_sepolia = "https://forno.celo-sepolia.celo-testnet.org"
localhost = "http://127.0.0.1:8545"

[etherscan]
celo = { key = "${CELOSCAN_API_KEY}", chain = 42220, url = "https://api.celoscan.io/api" }
celo_sepolia = { key = "${CELOSCAN_API_KEY}", chain = 11142220, url = "https://api.etherscan.io/v2/api" }
```

### 环境变量（.env文件）

```bash
PRIVATE_KEY=your_private_key_here
CELOSCAN_API_KEY=your_celoscan_api_key_here
```

加载环境变量：

```bash
source .env
```

## 编写合约

### 基本合约示例

```solidity
// src/MyContract.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract MyContract {
    string public name;
    address public owner;

    event NameChanged(string oldName, string newName);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(string memory _name) {
        name = _name;
        owner = msg.sender;
    }

    function setName(string memory _newName) external onlyOwner {
        string memory oldName = name;
        name = _newName;
        emit NameChanged(oldName, _newName);
    }
}
```

### 使用OpenZeppelin框架

```bash
forge install OpenZeppelin/openzeppelin-contracts
```

将相关配置添加到`remappings.txt`文件中：

```
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
```

```solidity
// src/MyToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
```

## 编译合约

```bash
# Compile all contracts
forge build

# Clean and rebuild
forge clean && forge build

# Check contract sizes
forge build --sizes
```

## 测试

### 测试文件结构

```solidity
// test/MyContract.t.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test, console} from "forge-std/Test.sol";
import {MyContract} from "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;
    address public owner;
    address public user;

    function setUp() public {
        owner = address(this);
        user = makeAddr("user");
        myContract = new MyContract("Initial Name");
    }

    function test_InitialName() public view {
        assertEq(myContract.name(), "Initial Name");
    }

    function test_Owner() public view {
        assertEq(myContract.owner(), owner);
    }

    function test_SetName() public {
        myContract.setName("New Name");
        assertEq(myContract.name(), "New Name");
    }

    function test_SetNameEmitsEvent() public {
        vm.expectEmit(true, true, true, true);
        emit MyContract.NameChanged("Initial Name", "New Name");
        myContract.setName("New Name");
    }

    function test_RevertWhen_NonOwnerSetsName() public {
        vm.prank(user);
        vm.expectRevert("Not owner");
        myContract.setName("Hacked");
    }

    function testFuzz_SetName(string memory newName) public {
        myContract.setName(newName);
        assertEq(myContract.name(), newName);
    }
}
```

### 运行测试

```bash
# Run all tests
forge test

# Run with verbosity (show logs)
forge test -vvv

# Run specific test
forge test --match-test test_SetName

# Run specific contract
forge test --match-contract MyContractTest

# Run with gas reporting
forge test --gas-report

# Run with coverage
forge coverage

# Fork testing against Celo mainnet
forge test --fork-url https://forno.celo.org
```

## 部署

### 部署脚本

```solidity
// script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Script, console} from "forge-std/Script.sol";
import {MyContract} from "../src/MyContract.sol";

contract DeployScript is Script {
    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        MyContract myContract = new MyContract("My Contract Name");
        console.log("Contract deployed to:", address(myContract));

        vm.stopBroadcast();
    }
}
```

### 使用forge create快速部署合约

```bash
# Deploy to Celo Sepolia
forge create src/MyContract.sol:MyContract \
  --rpc-url https://forno.celo-sepolia.celo-testnet.org \
  --private-key $PRIVATE_KEY \
  --constructor-args "My Contract Name"

# Deploy with verification
forge create src/MyContract.sol:MyContract \
  --rpc-url https://forno.celo-sepolia.celo-testnet.org \
  --private-key $PRIVATE_KEY \
  --constructor-args "My Contract Name" \
  --verify \
  --etherscan-api-key $CELOSCAN_API_KEY
```

## 验证合约

### 验证现有合约

```bash
# Verify on Celo Sepolia
forge verify-contract \
  --chain-id 11142220 \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --etherscan-api-key $CELOSCAN_API_KEY \
  --watch

# Verify on Celo Mainnet
forge verify-contract \
  --chain-id 42220 \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --etherscan-api-key $CELOSCAN_API_KEY \
  --watch

# With constructor arguments
forge verify-contract \
  --chain-id 11142220 \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --etherscan-api-key $CELOSCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(string)" "My Contract Name") \
  --watch
```

## 使用cast工具

### 读取链上数据

```bash
# Get balance
cast balance <ADDRESS> --rpc-url https://forno.celo.org

# Call view function
cast call <CONTRACT_ADDRESS> "name()(string)" --rpc-url https://forno.celo.org

# Get storage slot
cast storage <CONTRACT_ADDRESS> 0 --rpc-url https://forno.celo.org

# Get block number
cast block-number --rpc-url https://forno.celo.org
```

### 写入链上数据

```bash
# Send transaction
cast send <CONTRACT_ADDRESS> "setName(string)" "New Name" \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY

# Transfer CELO
cast send <TO_ADDRESS> --value 1ether \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY
```

### 其他实用命令

```bash
# Encode function call
cast calldata "setName(string)" "New Name"

# Decode function call
cast 4byte-decode <CALLDATA>

# Convert units
cast to-wei 1 ether
cast from-wei 1000000000000000000

# Get ABI-encoded constructor args
cast abi-encode "constructor(string)" "My Contract Name"
```

## Anvil（本地开发工具）

```bash
# Start local node
anvil

# Start with fork of Celo mainnet
anvil --fork-url https://forno.celo.org

# Start with specific block
anvil --fork-url https://forno.celo.org --fork-block-number 12345678
```

## 块浏览器

- **Celo主网：** https://celoscan.io
- **Celo Sepolia：** https://sepolia.celoscan.io

## 额外资源

- [foundry-config.md](references/foundry-config.md) - 详细配置选项
- [testing-patterns.md](references/testing-patterns.md) - 高级测试模式
- [security-checklist.md](rules/security-checklist.md) - 安全最佳实践