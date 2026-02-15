---
name: contract-verification
description: 在 Celo 上验证智能合约。在将合约源代码发布到 Celoscan 或 Blockscout 时，请使用此步骤。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# 在 Celo 上验证智能合约

本技能涵盖了如何在 Celo 的区块浏览器中验证智能合约，并使源代码公开可读。

## 使用场景

- 部署合约到 Celo 之后
- 发布开源合约
- 通过浏览器界面启用合约交互
- 建立用户信任

## 验证方法

| 方法 | 适用场景 |
|--------|----------|
| Hardhat | 自动化部署流程 |
| Foundry | 基于 Foundry 的项目 |
| Celoscan UI | 快速手动验证 |
| Blockscout UI | 替代浏览器界面 |
| Blockscout API | 程序化验证 |
| Sourcify | 去中心化验证 |
| Remix | 基于浏览器的验证 |

## 使用 Hardhat 进行验证

### 配置

来源：https://docs.celo.org/developer/verify/hardhat

```javascript
// hardhat.config.js
require("dotenv").config();
require("@nomicfoundation/hardhat-verify");

module.exports = {
  solidity: "0.8.28",
  networks: {
    celo: {
      url: "https://forno.celo.org",
      accounts: [process.env.PRIVATE_KEY],
      chainId: 42220,
    },
    celoSepolia: {
      url: "https://forno.celo-sepolia.celo-testnet.org/",
      accounts: [process.env.PRIVATE_KEY],
      chainId: 11142220,
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
    customChains: [
      {
        network: "celo",
        chainId: 42220,
        urls: {
          apiURL: "https://api.etherscan.io/v2/api",
          browserURL: "https://celoscan.io/",
        },
      },
      {
        network: "celoSepolia",
        chainId: 11142220,
        urls: {
          apiURL: "https://api.etherscan.io/v2/api",
          browserURL: "https://sepolia.celoscan.io",
        },
      },
    ],
  },
};
```

### 环境变量

```bash
# .env
PRIVATE_KEY=0xYOUR_PRIVATE_KEY
ETHERSCAN_API_KEY=your_celoscan_api_key
```

请从 [Etherscan](https://etherscan.io/myapikey) 或 [Celoscan](https://celoscan.io/myapikey) 获取 API 密钥。

### 验证命令

**主网：**
```bash
npx hardhat verify --network celo <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

**测试网：**
```bash
npx hardhat verify --network celoSepolia <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### 带有构造函数参数的示例

```bash
# Contract with constructor: constructor(string memory name, uint256 value)
npx hardhat verify --network celo 0x1234...5678 "MyToken" 1000000
```

### 复杂的构造函数参数

对于复杂的构造函数参数，请创建一个文件：

```javascript
// arguments.js
module.exports = [
  "MyToken",
  "MTK",
  1000000,
  "0x1234567890123456789012345678901234567890",
];
```

```bash
npx hardhat verify --network celo 0x1234...5678 --constructor-args arguments.js
```

## 使用 Foundry 进行验证

来源：https://docs.celo.org/developer/verify/foundry

### 配置

```toml
# foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.28"

[rpc_endpoints]
celo = "https://forno.celo.org"
celoSepolia = "https://forno.celo-sepolia.celo-testnet.org"
```

### 环境设置

```bash
export ETHERSCAN_API_KEY=<your_etherscan_api_key>
```

### 验证命令

**主网（链 ID 42220）：**
```bash
forge verify-contract \
  --chain-id 42220 \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --watch
```

**测试网（链 ID 11142220）：**
```bash
forge verify-contract \
  --chain-id 11142220 \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --watch
```

### 带有构造函数参数的验证

```bash
forge verify-contract \
  --chain-id 42220 \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  <CONTRACT_ADDRESS> \
  src/MyContract.sol:MyContract \
  --constructor-args $(cast abi-encode "constructor(string,uint256)" "MyToken" 1000000) \
  --watch
```

### 一步完成部署和验证

```bash
forge create \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --verify \
  src/MyContract.sol:MyContract \
  --constructor-args "MyToken" 1000000
```

## 使用 Celoscan UI 进行验证

1. 访问 [Celoscan](https://celoscan.io) 上的你的合约
2. 点击 **Contract**（合约）选项卡
3. 点击 **Verify & Publish**（验证并发布）
4. 选择编译器设置：
   - 编译器类型（Solidity 单文件/多文件）
   - 编译器版本
   - 许可证类型
5. 粘贴你的源代码
6. 添加构造函数参数（ABI 编码形式）
7. 完成验证码验证
8. 点击 **Verify and Publish**（验证并发布）

## 使用 Blockscout 进行验证

Celo 提供了 Blockscout 浏览器（地址：[celo.blockscout.com](https://celo.blockscout.com)），支持合约验证。

### Blockscout 的 API 地址

| 网络 | 浏览器地址 | API 地址 |
|---------|--------------|----------|
| 主网 | https://celo.blockscout.com | https://celo.blockscout.com/api/v2 |
| Sepolia | https://celo-sepolia.blockscout.com | https://celo-sepolia.blockscout.com/api/v2 |

### 通过浏览器界面进行验证

1. 访问 [celo.blockscout.com](https://celo.blockscout.com)（或测试网的 [celo-sepolia.blockscout.com](https://celo-sepolia.blockscout.com)）
2. 查找你的合约地址
3. 点击 **Code**（代码）选项卡
4. 点击 **Verify & Publish**（验证并发布）
5. 选择验证方法：
   - **通过扁平化源代码** - 包含所有导入语句的单一文件
   - **通过标准 JSON 输入** - 使用标准的 JSON 输入格式
   - **通过 Sourcify** - 去中心化验证
6. 填写编译器设置（版本、优化选项、EVM 版本）
7. 提交验证请求

### 通过 API 进行验证

Blockscout 提供了用于程序化验证的 REST API。

**扁平化源代码：**
```bash
curl -X POST "https://celo.blockscout.com/api/v2/smart-contracts/0xYOUR_ADDRESS/verification/via/flattened-code" \
  -H "Content-Type: application/json" \
  -d '{
    "compiler_version": "v0.8.28+commit.7893614a",
    "source_code": "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.28;\n...",
    "is_optimization_enabled": true,
    "optimization_runs": 200,
    "contract_name": "MyContract",
    "evm_version": "paris",
    "license_type": "mit"
  }'
```

**标准 JSON 输入：**
```bash
curl -X POST "https://celo.blockscout.com/api/v2/smart-contracts/0xYOUR_ADDRESS/verification/via/standard-input" \
  -F "compiler_version=v0.8.28+commit.7893614a" \
  -F "contract_name=MyContract" \
  -F "license_type=mit" \
  -F "files[0]=@standard-input.json"
```

**API 端点：**
- 扁平化源代码：`POST /api/v2/smart-contracts/{address}/verification/via/flattened-code`
- 标准 JSON 输入：`POST /api/v2/smart-contracts/{address}/verification/via/standard-input`
- 多部分输入：`POST /api/v2/smart-contracts/{address}/verification/via/multi-part`
- Sourcify：`POST /api/v2/smart-contracts/{address}/verification/via/sourcify`

来源：https://docs.blockscout.com/devs/verification

## 使用 Sourcify 进行验证

Sourcify 提供了一种去中心化的合约验证服务，支持多种浏览器。

来源：https://docs.celo.org/developer/verify/remix

### 使用优势

- 验证后的源代码存储在去中心化系统中
- 与 Blockscout 及其他浏览器兼容
- 元数据哈希验证确保源代码的准确性

### 使用 Remix 的 Sourcify 插件

1. 打开 [Remix IDE](https://remix.ethereum.org)
2. 转到 **插件管理器**（插件图标）
3. 搜索并激活 “Sourcify” 插件
4. 将你的合约部署到 Celo
5. 在 Sourcify 插件中：
   - 选择已部署的合约
   - 选择网络（Celo 主网：42220；Sepolia：11142220）
   - 点击 **Verify**（验证）
6. 合约将在 Sourcify 中被验证，并在 Blockscout 中显示

### 通过 Remix 的 Sourcify 插件进行程序化验证

```bash
curl -X POST "https://sourcify.dev/server/verify" \
  -F "address=0xYOUR_ADDRESS" \
  -F "chain=42220" \
  -F "files[0]=@MyContract.sol" \
  -F "files[1]=@metadata.json"
```

## 使用 Remix 进行验证

可以直接在 Remix IDE 中使用 Etherscan 插件来验证合约。

来源：https://docs.celo.org/developer/verify/remix

### 设置步骤

1. 打开 [Remix IDE](https://remix.ethereum.org)
2. 转到 **插件管理器**
3. 激活 **Etherscan - Contract Verification**（Etherscan - 合约验证）插件

### 验证步骤

1. 通过 Remix 将合约部署到 Celo
2. 打开 Etherscan 插件（勾选标记图标）
3. 输入你的 Celoscan API 密钥
4. 选择要验证的合约
5. 选择网络：
   - Celo 主网（链 ID：42220）
   - Celo Sepolia（链 ID：11142220）
6. 点击 **Verify**（验证）

### Celo 的配置设置

在 Remix 的设置中，添加自定义网络信息：
- 网络名称：Celo 主网
- 链 ID：42220
- API 地址：https://api.celoscan.io/api
- 浏览器地址：https://celoscan.io

## 故障排除

### “无法验证”

**原因：**
- 编译器版本不匹配
- 优化器设置不匹配
- 构造函数参数错误

**解决方法：**
- 确保使用的编译器版本与部署时使用的版本一致
- 确保优化器设置正确（已启用且正在运行）
- 确保构造函数参数已正确编码为 ABI 格式

### “已验证”

合约已经过验证。可以在浏览器中查看源代码。

### “找不到合约”

**原因：**
- 合约地址错误
- 合约尚未被索引

**解决方法：**
- 重新检查合约地址
- 等待几分钟，直到合约被索引

### 代理合约

对于代理合约，需要验证以下两个合约：
1. 实现合约
2. 代理合约

然后在 Celo 中进行链接：
1. 访问代理合约
2. 点击 “More Options”（更多选项）
3. 选择 “Is this a proxy?”（这是代理合约吗？）
4. 按照提示完成验证步骤

## API 端点

| 网络 | API 地址 |
|---------|---------|
| 主网 | https://api.celoscan.io/api |
| Sepolia | https://api-sepolia.celoscan.io/api |

## 所需依赖项

对于 Hardhat：```json
{
  "devDependencies": {
    "@nomicfoundation/hardhat-verify": "^2.0.0",
    "hardhat": "^2.19.0"
  }
}
```

## 其他资源

- [verification-config.md](references/verification-config.md) - 完整的配置示例