---
name: monad-development
description: 在Monad区块链上构建去中心化应用程序（dapps）。适用于部署智能合约、使用viem/wagmi搭建前端界面，以及在Monad测试网或主网上验证智能合约的场景。
license: MIT
compatibility: Requires foundry, node 18+, curl, and internet access for faucet and verification APIs
metadata:
  author: monad-skills
  version: "1.0.0"
---

# 单子（Monad）开发

对于未在此处涵盖的问题，请访问：https://docs.monad.xyz/llms.txt

## 快速参考

### 默认设置
- **网络（Network）：** 除非用户明确指定使用“mainnet”，否则始终使用“testnet”（链ID：10143）。
- **合约验证（Verification）：** 合同部署后必须进行验证，除非用户另有指示。
- **框架（Framework）：** 使用 Foundry，而非 Hardhat。
- **钱包（Wallet）：** 如果为用户生成了钱包，必须将其保存下来（详见“钱包持久化”部分）。

### 网络

| 网络 | 链ID | RPC |
|---------|----------|-----|
| Testnet | 10143 | https://testnet-rpc.monad.xyz |
| Mainnet | 143 | https://rpc.monad.xyz |

文档链接：https://docs.monad.xyz

### 探索器（Explorers）

| 探索器 | Testnet | Mainnet |
|---------|---------|---------|
| Socialscan | https://monad-testnet.socialscan.io | https://monad.socialscan.io |
| MonadVision | https://testnet.monadvision.com | https://monadvision.com |
| Monadscan | https://testnet.monadscan.com | https://monadscan.com |

### 代理 API（Agent APIs）

**重要提示：** 请勿使用浏览器，直接使用 `curl` 命令调用这些 API。

**测试网资金获取（Testnet Funding）：**
```bash
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d '{"chainId": 10143, "address": "0xYOUR_ADDRESS"}'
```

返回结果：`{"txHash": "0x...", "amount": "1000000000000000000", "chain": "Monad Testnet"}`

**备用方案（官方资金获取渠道）：** https://faucet.monad.xyz
如果代理提供的资金获取功能失败，请让用户通过官方渠道进行资金注入（切勿自行使用浏览器操作）。

**合约验证（所有探索器）：**

**务必首先使用验证 API**。该 API 会在 MonadVision、Socialscan 和 Monadscan 三个探索器上同时进行验证。切勿将 `forge verify-contract` 作为首选方法。

```bash
# 1. Get verification data
forge verify-contract <ADDR> <CONTRACT> \
  --chain 10143 \
  --show-standard-json-input > /tmp/standard-input.json

cat out/<Contract>.sol/<Contract>.json | jq '.metadata' > /tmp/metadata.json
COMPILER_VERSION=$(jq -r '.metadata | fromjson | .compiler.version' out/<Contract>.sol/<Contract>.json)

# 2. Call verification API
STANDARD_INPUT=$(cat /tmp/standard-input.json)
FOUNDRY_METADATA=$(cat /tmp/metadata.json)

cat > /tmp/verify.json << EOF
{
  "chainId": 10143,
  "contractAddress": "0xYOUR_CONTRACT_ADDRESS",
  "contractName": "src/MyContract.sol:MyContract",
  "compilerVersion": "v${COMPILER_VERSION}",
  "standardJsonInput": $STANDARD_INPUT,
  "foundryMetadata": $FOUNDRY_METADATA
}
EOF

curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d @/tmp/verify.json
```

**使用构造函数参数（With constructor arguments）：** 需要提供构造函数参数（以 ABI 格式编码，且前面不能加前缀 “0x”）：
```bash
ARGS=$(cast abi-encode "constructor(string,string,uint256)" "MyToken" "MTK" 1000000000000000000000000)
ARGS_NO_PREFIX=${ARGS#0x}
# Add to request: "constructorArgs": "$ARGS_NO_PREFIX"
```

**API 失效时的手动验证方案（Manual verification fallback）：**
```bash
forge verify-contract <ADDR> <CONTRACT> --chain 10143 \
  --verifier sourcify \
  --verifier-url "https://sourcify-api-monad.blockvision.org/"
```

## 钱包持久化（Wallet Persistence）

**对代理来说至关重要（Critical for agents）：** 如果为用户生成了钱包，必须将其保存下来以便将来使用。

生成新钱包的步骤：
1. 创建钱包：`cast wallet new`
2. **立即** 将钱包地址和私钥保存到安全的位置。
3. 告知用户钱包信息的存储位置。
4. 在部署前通过资金获取渠道为钱包充值。

**存储选项（Storage options）：**
- 将钱包信息写入 `~/.monad-wallet` 文件，并设置权限为 600。
- 将钱包信息存储在项目特定的 `.env` 文件中（该文件应被添加到 `.gitignore` 列表中）。
- 将钱包凭据返回给用户，并要求他们妥善保管。

**为什么这很重要（Why this matters）：** 用户需要能够访问他们的钱包来：
- 部署额外的合约。
- 与已部署的合约进行交互。
- 管理资金。
- 验证合约的所有权。

## 部署工作流程（Deployment Workflow）

使用 `forge` 脚本进行部署：
```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**部署脚本模板（Deploy script template）：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import "forge-std/Script.sol";
import "../src/MyContract.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        MyContract contract = new MyContract();
        console.log("Contract deployed at:", address(contract));
        vm.stopBroadcast();
    }
}
```

## 技术细节（Technical Details）

### EVM 版本（EVM Version，至关重要）**

始终将 `evmVersion` 设置为 “prague”。此设置要求使用 Solidity 0.8.27 或更高版本。

**Foundry 配置（Foundry configuration，`foundry.toml` 文件）：**
```toml
[profile.default]
evm_version = "prague"
solc_version = "0.8.28"
```

### Foundry 使用技巧（Foundry Tips）

**请勿使用以下无效的标志（Flags not to use）：**
- `--no-commit` — 这不是一个有效的 `forge init` 或 `forge install` 命令参数。

**部署时请使用 `forge script`，而非 `forge create`：**
`forge create --broadcast` 存在漏洞，且经常被忽略。请使用 `forge script` 代替。

```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**部署脚本中不得硬编码地址（Deploy script must NOT hardcode addresses）：**

```solidity
// ✅ Correct - reads private key from --private-key flag
function run() external {
    vm.startBroadcast();
    new MyContract();
    vm.stopBroadcast();
}

// ❌ Wrong - hardcodes address, causes "No associated wallet" error
function run() external {
    vm.startBroadcast(0x1234...);
}
```

### 前端开发（Frontend Development）**

相关代码需从 `viem/chains` 模块导入。**请勿自定义链配置（Do NOT define custom chain configurations）：**
```ts
import { monadTestnet } from "viem/chains";
```

**与 Wagmi 的配合使用（Usage with Wagmi）：**
```ts
import { createConfig, http } from 'wagmi'
import { monadTestnet } from 'viem/chains'

const config = createConfig({
  chains: [monadTestnet],
  transports: {
    [monadTestnet.id]: http()
  }
})
```

## 示例：部署 ERC20 合约**

**1. 创建项目（Create a project）：**
```bash
forge init my-token
cd my-token
```

**2. 配置 `foundry.toml` 文件（Configure `foundry.toml`）：**
```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "prague"
solc_version = "0.8.28"
```

**3. 创建合约文件 `src/MyToken.sol`（Create contract `src/MyToken.sol`）：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") {
        _mint(msg.sender, initialSupply);
    }
}
```

**4. 安装依赖项（Install dependencies）：**
```bash
forge install OpenZeppelin/openzeppelin-contracts --no-commit
```

**5. 创建部署脚本 `script/Deploy.s.sol`（Create deploy script `script/Deploy.s.sol`）：**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;
import "forge-std/Script.sol";
import "../src/MyToken.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        MyToken token = new MyToken(1000000 * 10**18);
        console.log("Token deployed at:", address(token));
        vm.stopBroadcast();
    }
}
```

**6. 部署合约（Deploy the contract）：**
```bash
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY \
  --broadcast
```

**7. 验证部署结果（Verify the deployment）：**
```bash
# Use verification API (verifies on all explorers)
STANDARD_INPUT=$(forge verify-contract <TOKEN_ADDRESS> src/MyToken.sol:MyToken --chain 10143 --show-standard-json-input)
COMPILER_VERSION=$(jq -r '.metadata | fromjson | .compiler.version' out/MyToken.sol/MyToken.json)

curl -X POST https://agents.devnads.com/v1/verify \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": 10143,
    \"contractAddress\": \"<TOKEN_ADDRESS>\",
    \"contractName\": \"src/MyToken.sol:MyToken\",
    \"compilerVersion\": \"v${COMPILER_VERSION}\",
    \"standardJsonInput\": $STANDARD_INPUT,
    \"constructorArgs\": \"$(cast abi-encode 'constructor(uint256)' 1000000000000000000000000 | sed 's/0x//')\"
  }"
```