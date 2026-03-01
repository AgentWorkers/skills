---
name: potato-tipper
description: "AI代理需要具备在LUKSO平台上使用“Potato Tipper”工具进行设置的能力（该操作需要私钥），并能够学习如何开发创新的“提示-跟随”解决方案。"
---
# Potato Tipper – OpenClaw 技能

您可以使用此技能来处理与 Potato Tipper 合同仓库相关的任何技术性任务：
- 📖 阅读/理解 Potato Tipper 协议
- ⚙️ 在 LUKSO UP 配置中设置和配置您的 Universal Profile
- ❓ 在设置过程中排查权限问题
- 💡 利用 Potato Tipper 的理念构建新的提示系统

## 技能简介（1段总结）

**Potato Tipper** 协议是 LUKSO 上的一个 LSP1 Universal Receiver Delegate，它会自动向新关注者发放 $POTATO 代币。

PotatoTipper 是一个 **LSP1 Universal Receiver Delegate**，它会响应 **LSP26 的关注/取消关注通知**，并在符合条件的情况下，将 **LSP7 $POTATO 代币** 从被关注者的 🆙 转移到新关注者的 🆙。每个用户的设置都存储在 ERC725Y 存储中，并通过专用的数据键进行管理。该合约还提供了用于配置键的自文档化辅助视图。

## 该技能提供的内容：

- 了解与 Potato Tipper 相类似的架构及 LUKSO/LSP 集成（LSP1、LSP7、LSP26、ERC725Y）
- 了解该模式的安全性及已知限制
- 配置具有所需权限和数据键的 Universal Profile
- 学习如何使用“关注即提示”（tip-on-follow）模式构建创新集成
- 包含 TypeScript（wagmi/viem/ethers + erc725.js）和 Solidity 代码示例

## 部署地址

请参阅 `references/addresses.md`，以获取 LUKSO 主网和测试网上的所有合约地址（PotatoTipper、$POTATO 代币、LSP26 注册表、RPC 端点、浏览器工具等）。

## 快速工作流程：

### 1) 了解仓库结构（仓库文件映射）

请阅读 `references/repo-overview.md` 以获取文件映射和合约职责。

### 2) 一键配置用户账户以使用 PotatoTipper

这需要使用一个 Foundry 脚本，该脚本会在一次 `batchCalls` 交易中完成全部设置：
**步骤 1：** 在 Potato Tipper 合同仓库内创建 `script/SetupPotatoTipper.s.sol` 文件：
```solidity
// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.28;

import {Script} from "forge-std/Script.sol";
import {console2} from "forge-std/console2.sol";

interface ILSP0 {
    function batchCalls(uint256[] calldata values, bytes[] calldata payloads) external returns (bytes[] memory);
}

interface IERC725Y {
    function setDataBatch(bytes32[] calldata keys, bytes[] calldata values) external;
}

interface ILSP7 {
    function authorizeOperator(address operator, uint256 amount, bytes calldata data) external;
}

/// @title Setup PotatoTipper via LSP0 batchCalls
/// @notice One-click setup: connect PotatoTipper + set settings + authorize budget
/// @dev Run with: forge script script/SetupPotatoTipper.s.sol:SetupPotatoTipper --rpc-url <rpc> --broadcast
///
/// Required env vars:
/// - PRIVATE_KEY: EOA controller key (must have ADDUNIVERSALRECEIVERDELEGATE + CALL permissions on UP)
/// - UP_ADDRESS: Universal Profile address to configure
/// - POTATO_TIPPER_ADDRESS: PotatoTipper contract address
/// - POTATO_TOKEN_ADDRESS: $POTATO LSP7 token address
/// - TIP_AMOUNT: Amount to tip per follower (in wei, e.g., "1000000000000000000" = 1 POTATO)
/// - MIN_FOLLOWERS: Minimum follower count for eligibility (e.g., "5")
/// - MIN_POTATO_BALANCE: Minimum POTATO balance for eligibility (in wei, e.g., "100000000000000000000" = 100 POTATO)
/// - TIPPING_BUDGET: Total POTATO authorized for tipping (in wei, e.g., "1000000000000000000000" = 1000 POTATO)
contract SetupPotatoTipper is Script {
    bytes32 constant LSP1DELEGATE_ON_FOLLOW_DATA_KEY = 0x0cfc51aec37c55a4d0b1000071e02f9f05bcd5816ec4f3134aa2e5a916669537;
    bytes32 constant LSP1DELEGATE_ON_UNFOLLOW_DATA_KEY = 0x0cfc51aec37c55a4d0b100009d3c0b4012b69658977b099bdaa51eff0f0460f4;
    bytes32 constant POTATO_TIPPER_SETTINGS_KEY = 0xd1d57abed02d4c2d7ce00000e8211998bb257be214c7b0997830cd295066cc6a;

    function run() external {
        address upAddress = vm.envAddress("UP_ADDRESS");
        address potatoTipperAddress = vm.envAddress("POTATO_TIPPER_ADDRESS");
        address potatoTokenAddress = vm.envAddress("POTATO_TOKEN_ADDRESS");
        uint256 tipAmount = vm.envUint("TIP_AMOUNT");
        uint256 minFollowers = vm.envUint("MIN_FOLLOWERS");
        uint256 minPotatoBalance = vm.envUint("MIN_POTATO_BALANCE");
        uint256 tippingBudget = vm.envUint("TIPPING_BUDGET");

        console2.log("=== PotatoTipper Setup ===");
        console2.log("UP Address:", upAddress);
        console2.log("PotatoTipper:", potatoTipperAddress);
        console2.log("POTATO Token:", potatoTokenAddress);
        console2.log("Tip Amount (wei):", tipAmount);
        console2.log("Min Followers:", minFollowers);
        console2.log("Min POTATO Balance (wei):", minPotatoBalance);
        console2.log("Tipping Budget (wei):", tippingBudget);
        console2.log("");

        bytes32[] memory dataKeys = new bytes32[](3);
        dataKeys[0] = POTATO_TIPPER_SETTINGS_KEY;
        dataKeys[1] = LSP1DELEGATE_ON_FOLLOW_DATA_KEY;
        dataKeys[2] = LSP1DELEGATE_ON_UNFOLLOW_DATA_KEY;

        bytes[] memory dataValues = new bytes[](3);
        dataValues[0] = abi.encode(tipAmount, minFollowers, minPotatoBalance);
        dataValues[1] = abi.encodePacked(potatoTipperAddress);
        dataValues[2] = abi.encodePacked(potatoTipperAddress);

        bytes[] memory payloads = new bytes[](2);
        payloads[0] = abi.encodeCall(IERC725Y.setDataBatch, (dataKeys, dataValues));

        bytes memory authorizeCalldata = abi.encodeCall(
            ILSP7.authorizeOperator, (potatoTipperAddress, tippingBudget, "")
        );
        payloads[1] = abi.encodeWithSignature(
            "execute(uint256,address,uint256,bytes)", 0, potatoTokenAddress, 0, authorizeCalldata
        );

        uint256[] memory values = new uint256[](2);
        values[0] = 0;
        values[1] = 0;

        vm.startBroadcast(vm.envUint("PRIVATE_KEY"));

        console2.log("Broadcasting batchCalls to UP...");
        ILSP0(upAddress).batchCalls(values, payloads);

        vm.stopBroadcast();

        console2.log("");
        console2.log("=== Setup Complete ===");
        console2.log("PotatoTipper is now connected to the UP!");
        console2.log("Settings configured:");
        console2.log("  - Tip amount:", tipAmount, "wei");
        console2.log("  - Min followers:", minFollowers);
        console2.log("  - Min POTATO balance:", minPotatoBalance, "wei");
        console2.log("Tipping budget authorized:", tippingBudget, "wei");
    }
}
```

**步骤 2：** 通过 shell 脚本运行设置：
```bash
TIP_AMOUNT=42000000000000000000 \
MIN_FOLLOWERS=5 \
MIN_POTATO_BALANCE=100000000000000000000 \
TIPPING_BUDGET=1000000000000000000000 \
PRIVATE_KEY=0x... \
./skills/potato-tipper/scripts/setup_potato_tipper.sh luksoTestnet 0xYourUPAddress
```

这次交易会：
- 连接 LSP1 代理（关注/取消关注）
- 设置提示金额
- 授权提示预算

手动设置详情：`references/config-and-data-keys.md`
脚本实现：`references/foundry-batch-setup.md`

### 5) 权限问题（连接/断开连接）

- **连接时：** 控制器需要 `ADDUNIVERSALRECEIVERDELEGATE` 权限
- **断开连接时：** 控制器需要 `CHANGEUNIVERSALRECEIVERDELEGATE` 权限
- 如果设置过程中出现权限错误，这很可能是问题所在

完整的故障排除步骤及 UP 浏览器扩展说明：`references/permissions.md`

### 6) LSP1 实现要求

智能合约必须实现 `LSP1UniversalReceiver` 接口（并通过 ERC165 报告 `_INTERFACEID_LSP0`），才能接收提示。PotatoTipper 会检查关注者地址是否支持该接口，并拒绝不符合要求的智能合约。

当 $POTATO 代币转移发生时，它会在发送者和接收者的 🆙 上调用 `universalReceiver(...)`。如果接收者合约未实现 LSP1，转移操作将会被撤销（由 PotatoTipper 的 `try/catch` 语句捕获）。

## 代码示例：

### TypeScript（wagmi / viem / ethers + erc725.js）

关于数据键编码、与 dApp 连接/断开连接以及设置提示金额的完整示例：
→ `references/typescript-examples.md`

### Solidity

- 为智能合约设置 PotatoTipper
- 在自定义合约中实现 LSP1 接口以接收提示
- 使用来自任何合约的 `loadTipSettingsRaw` 和 `decodeTipSettings` 函数：
→ `references/solidity-examples.md`

## 注意事项：

- **只有 🆙（LSP0）关注者** 有资格接收提示（不符合要求的智能合约会被拒绝）
- 关注/取消关注的操作必须来自 **LSP26 关注者注册表**——合约会重新验证注册表状态
- 在 LSP7 转移操作中使用 `try/catch` 语句，以返回用户友好的状态信息，永远不会导致操作失败
- 安装前的“现有关注者”将被有意排除在提示之外
- 设置值（`tipAmount`、`minimumPotatoBalance`）以 **wei**（18 位小数）为单位

## 设计模式与创新集成：

- “关注即提示”（Tip-on-Follow）模式及自文档化的 ERC725Y 配置：
→ `references/learn-notes.md`
- 扩展思路（NFT 徽章、分层奖励、跨协议组合性、营销功能）：
→ `references/innovative-integrations.md`
- 关注→提示事件顺序（调试）：
→ `references/event-flow.md`
- 一键设置/批量设置说明：
→ `references/foundry-batch-setup.md`
- 安全性考量及已知限制：
→ `references/security-and-limitations.md`

## 搭配资源：

### 参考资料：
- `repo-overview.md` — 文件映射和合约职责
- `addresses.md` — 主网和测试网上的部署地址
- `config-and-data-keys.md` — 3 个配置键及其编码/解码方法
- `permissions.md` — 所需的 LSP6 权限（ADD/CHANGE UNIVERSALRECEIVERDELEGATE）
- `typescript-examples.md` — wagmi、viem、ethers 和 erc725.js 代码示例
- `solidity-examples.md` — 设置合约、LSP1 接收器、设置读取函数
- `learn-notes.md` — 设计模式（关注即提示 + 自文档化配置）
- `innovative-integrations.md` — 新集成方案的想法
- `event-flow.md` — 关注→提示事件发送顺序（调试）
- `foundry-batch-setup.md` — 批量设置/一键设置说明
- `security-and-limitations.md` — 已知限制及安全设计

### 脚本：
- `setup_potato_tipper.sh` — 用于克隆仓库并运行 Foundry 设置脚本的 shell 脚本

### 资产文件：
- `assets/abis/UniversalProfile.abi.json` — 最基本的 UP ABI（用于 setData/setDataBatch 和读取操作）
- `assets/abis/LSP7DigitalAsset.abi.json` — 最基本的 LSP7 ABI（包含 authorizeOperator 功能）
- `assets/abis/PotatoTipper.abi.json` — 最基本的 PotatoTipper ABI（包含事件处理函数）
- `assets/abis/KeyManager.abi.json` — 最基本的 KeyManager ABI（包含执行/executeBatch 功能）