---
name: jb-project
description: 创建并配置 Juicebox V5 项目。生成用于通过 JBController 启动项目的部署脚本（这些脚本包含规则集、终端配置以及相关设置）。同时，该工具还支持项目所有权的转移以及元数据的更新。
---

# Juicebox V5 项目管理

用于创建和管理 Juicebox V5 项目，包括项目的部署、配置和所有权管理。

## 项目标识

**一个 Juicebox 项目的唯一标识是：`projectId + chainId + version`**

这一点很重要，因为：
- **V4 和 V5 使用的是不同的协议。** 在 V4 上的项目 #64 与 V5 上的项目 #64 不同，即使在同一个链上也是如此。
- **项目 ID 不能在不同链之间共享。** 每个链会独立分配下一个可用的 ID。如果你在 Ethereum 上部署项目，可能会得到项目 ID #42；而在 Optimism 上部署则可能得到项目 ID #17。
- **Suckers 可以跨链链接项目。** 要创建一个“多链项目”，你需要在每个链上分别部署项目（使用不同的 ID），并通过 Suckers 将它们连接起来。这样可以实现代币的跨链桥接，同时保持资金库的安全性。
- 在引用项目时，务必指定版本和链，以避免混淆。

## V5.1 合约更新（2025 年 12 月）

**只有 JBRuleset 合约有代码更改**（修复了一行审批钩子）。其他合约由于依赖关系被重新部署（例如：JBTerminalStore→JBMultiTerminal, JB721TiersHook→JB721TiersHookDeployer→JBOmnichainDeployer）。

| 部署内容 | 使用的合约 |
|--------------|---------------------|
| 新项目 | **V5.1**（JBController5_1, JBMultiTerminal5_1 等） |
| Revnet | **V5.0**（REVDeployer 使用 V5.0 的 JBController） |

**请不要混合使用 V5.0 和 V5.1 的合约**——只能使用其中一套完整的合约。

有关地址的信息，请参阅 `references/v5-addresses.md` 或 `shared/chain-config.json`。

## 在编写自定义代码之前

**请始终先检查是否可以使用原生的功能来实现你的目标：**

| 用户需求 | 推荐解决方案 |
|-----------|---------------------|
| 自主管理的代币化资金库 | 通过 revnet-core-v5 部署一个 **Revnet** 合约 |
| 没有 EOA（Externally Owned Account）所有者的项目 | 使用 **contract-as-owner** 模式 |
| 简单的筹款项目 | 使用该功能来生成部署脚本 |
| 分配/时间锁定的代币发放 | 使用 **payout limits + cycling rulesets**（无需自定义合约） |
| 需要 NFT 来管理的资金库 | 使用 **nana-721-hook-v5** 合约，并结合原生的现金退出机制 |
| 最小化治理操作/不可更改的所有权 | 设置完成后将所有权转移到 **burn address** |
| 一次性资金库访问 | 使用 **surplus allowance**（不会在每个周期重置） |
| 自定义代币机制 | 通过 `setTokenFor()` 使用 **custom ERC20** 合约 |

**有关这些模式的详细示例，请参阅 `/jb-patterns`。**
**如需减少自定义代码的使用，请参阅 `/jb-simplify`。**

## 项目创建概述

项目是通过 `JBController.launchProjectFor()` 创建的，该函数会：
1. 通过 JBProjects 创建一个新的项目 NFT。
2. 设置项目的控制器。
3. 配置第一个规则集。
4. 设置终端配置。

## 核心功能

### 启动项目

```solidity
function launchProjectFor(
    address owner,                              // Project owner (receives NFT)
    string calldata projectUri,                 // IPFS metadata URI
    JBRulesetConfig[] calldata rulesetConfigs,  // Initial ruleset(s)
    JBTerminalConfig[] calldata terminalConfigs, // Terminal setup
    string calldata memo                        // Launch memo
) external returns (uint256 projectId);
```

### 项目元数据（projectUri）

`projectUri` 应该指向一个 JSON 文件（通常存储在 IPFS 上），该文件包含以下内容：

```json
{
  "name": "Project Name",
  "description": "Project description",
  "logoUri": "ipfs://...",
  "infoUri": "https://...",
  "twitter": "@handle",
  "discord": "https://discord.gg/...",
  "telegram": "https://t.me/..."
}
```

## 配置结构

### JBRulesetConfig

```solidity
struct JBRulesetConfig {
    uint256 mustStartAtOrAfter;     // Earliest start time (0 = now)
    uint256 duration;               // Duration in seconds (0 = indefinite)
    uint256 weight;                 // Token minting weight (18 decimals)
    uint256 weightCutPercent;       // Weight cut per cycle (0-1000000000)
    IJBRulesetApprovalHook approvalHook;  // Approval hook (e.g., JBDeadline)
    JBRulesetMetadata metadata;     // Ruleset settings
    JBSplitGroup[] splitGroups;     // Payout and reserved splits
    JBFundAccessLimitGroup[] fundAccessLimitGroups;  // Payout limits
}
```

### JBTerminalConfig

```solidity
struct JBTerminalConfig {
    IJBTerminal terminal;                   // Terminal contract
    JBAccountingContext[] accountingContexts;  // Accepted tokens
}
```

### JBAccountingContext

```solidity
struct JBAccountingContext {
    address token;          // Token address (address(0) for native)
    uint8 decimals;         // Token decimals
    uint32 currency;        // Currency ID for accounting
}
```

## 部署脚本示例

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Script} from "forge-std/Script.sol";
import {IJBController} from "@bananapus/core/src/interfaces/IJBController.sol";
import {IJBMultiTerminal} from "@bananapus/core/src/interfaces/IJBMultiTerminal.sol";
import {JBRulesetConfig} from "@bananapus/core/src/structs/JBRulesetConfig.sol";
import {JBRulesetMetadata} from "@bananapus/core/src/structs/JBRulesetMetadata.sol";
import {JBTerminalConfig} from "@bananapus/core/src/structs/JBTerminalConfig.sol";
import {JBAccountingContext} from "@bananapus/core/src/structs/JBAccountingContext.sol";
import {JBSplitGroup} from "@bananapus/core/src/structs/JBSplitGroup.sol";
import {JBSplit} from "@bananapus/core/src/structs/JBSplit.sol";
import {JBFundAccessLimitGroup} from "@bananapus/core/src/structs/JBFundAccessLimitGroup.sol";
import {JBCurrencyAmount} from "@bananapus/core/src/structs/JBCurrencyAmount.sol";
import {JBConstants} from "@bananapus/core/src/libraries/JBConstants.sol";

contract DeployProject is Script {
    // V5.1 Mainnet Addresses (use for new projects)
    // See /references/v5-addresses.md for all networks
    // NOTE: For revnets, use V5.0 addresses instead
    IJBController constant CONTROLLER = IJBController(0xf3cc99b11bd73a2e3b8815fb85fe0381b29987e1);
    IJBMultiTerminal constant TERMINAL = IJBMultiTerminal(0x52869db3d61dde1e391967f2ce5039ad0ecd371c);

    function run() external {
        vm.startBroadcast();

        // Configure ruleset metadata
        JBRulesetMetadata memory metadata = JBRulesetMetadata({
            reservedRate: 0,                    // No reserved tokens
            cashOutTaxRate: 0,                  // No cash out tax
            baseCurrency: uint32(uint160(JBConstants.NATIVE_TOKEN)),
            pausePay: false,
            pauseCashOut: false,
            pauseTransfers: false,
            allowOwnerMinting: false,
            allowTerminalMigration: false,
            allowSetTerminals: false,
            allowSetController: false,
            allowAddAccountingContexts: false,
            allowAddPriceFeed: false,
            ownerMustSendPayouts: false,
            holdFees: false,
            useTotalSurplusForCashOuts: false,
            useDataHookForPay: false,
            useDataHookForCashOut: false,
            dataHook: address(0),
            metadata: 0
        });

        // Configure splits (empty for now)
        JBSplitGroup[] memory splitGroups = new JBSplitGroup[](0);

        // Configure fund access limits
        JBFundAccessLimitGroup[] memory fundAccessLimits = new JBFundAccessLimitGroup[](0);

        // Build ruleset config
        JBRulesetConfig[] memory rulesetConfigs = new JBRulesetConfig[](1);
        rulesetConfigs[0] = JBRulesetConfig({
            mustStartAtOrAfter: 0,
            duration: 0,                        // Indefinite
            weight: 1e18,                       // 1 token per unit paid
            weightCutPercent: 0,                // No weight cut
            approvalHook: IJBRulesetApprovalHook(address(0)),
            metadata: metadata,
            splitGroups: splitGroups,
            fundAccessLimitGroups: fundAccessLimits
        });

        // Configure terminal to accept ETH
        JBAccountingContext[] memory accountingContexts = new JBAccountingContext[](1);
        accountingContexts[0] = JBAccountingContext({
            token: JBConstants.NATIVE_TOKEN,
            decimals: 18,
            currency: uint32(uint160(JBConstants.NATIVE_TOKEN))
        });

        JBTerminalConfig[] memory terminalConfigs = new JBTerminalConfig[](1);
        terminalConfigs[0] = JBTerminalConfig({
            terminal: TERMINAL,
            accountingContexts: accountingContexts
        });

        // Launch the project
        uint256 projectId = CONTROLLER.launchProjectFor(
            msg.sender,                         // Owner
            "ipfs://...",                       // Project metadata URI
            rulesetConfigs,
            terminalConfigs,
            "Project launch"                    // Memo
        );

        vm.stopBroadcast();
    }
}
```

## 自定义 ERC20 项目代币

默认情况下，Juicebox 项目使用 **credits**（未领取的内部余额）。你可以通过以下两种方式升级为 ERC20 代币：

### 选项 1：部署标准的 JBERC20

```solidity
// Deploy the default Juicebox ERC20 token
IJBToken token = CONTROLLER.deployERC20For(
    projectId,
    "Project Token",    // name
    "PROJ",             // symbol
    bytes32(0)          // salt (for deterministic address, or 0)
);
```

这种方式会创建一个标准的 `JBERC20` 代币，控制器可以对其进行铸造或销毁。这种方法简单，适用于大多数项目。

### 选项 2：使用自定义的 ERC20

对于更复杂的代币经济模型，你可以使用自己的 ERC20 代币：

```solidity
// Set an existing/custom ERC20 as the project token
CONTROLLER.setTokenFor(projectId, IJBToken(myCustomToken));
```

**自定义代币的要求：**
1. 必须使用 **18 个小数位**。
2. 必须实现 `canBeAddedTo(uint256 projectId)` 方法，并返回 `true`。
3. 不能被分配给其他 Juicebox 项目。
4. 控制器需要具有铸造或销毁代币的权限（通常通过所有权或访问控制来实现）。

### 自定义代币接口

```solidity
interface IJBToken is IERC20 {
    /// @notice Verify this token can be added to a project.
    /// @param projectId The project ID to check.
    /// @return True if the token can be added.
    function canBeAddedTo(uint256 projectId) external view returns (bool);

    /// @notice Mint tokens to an account.
    /// @param holder The account to mint to.
    /// @param amount The amount to mint.
    function mint(address holder, uint256 amount) external;

    /// @notice Burn tokens from an account.
    /// @param holder The account to burn from.
    /// @param amount The amount to burn.
    function burn(address holder, uint256 amount) external;
}
```

### 何时使用自定义 ERC20

| 使用场景 | 为什么使用自定义 ERC20 |
|----------|------------------|
| **转移税** | 在转移过程中收取费用（例如，使用反射代币） |
| **代币基数调整** | 自动调整代币供应量的机制 |
| **现有的社区代币** | 将社区代币整合到系统中 |
| **治理功能** | 实现投票、委托、检查点等功能 |
| **分配计划** | 代币本身内置解锁机制 |
| **白名单/黑名单** | 控制代币的转移 |
| **集中度限制** | 限制每个地址的最大持有量 |
| **可编辑的元数据** | 不需要重新部署即可更改代币的名称/符号 |

### 示例：带有转移税的自定义代币

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract TaxedProjectToken is ERC20, Ownable {
    uint256 public constant TAX_RATE = 100; // 1% (basis points)
    uint256 public constant TAX_DENOMINATOR = 10000;
    address public taxRecipient;
    address public controller;
    uint256 public projectId;

    constructor(
        string memory name,
        string memory symbol,
        address _controller,
        uint256 _projectId,
        address _taxRecipient
    ) ERC20(name, symbol) Ownable(msg.sender) {
        controller = _controller;
        projectId = _projectId;
        taxRecipient = _taxRecipient;
    }

    function decimals() public pure override returns (uint8) {
        return 18; // REQUIRED: Must be 18 decimals
    }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId; // Only allow for our project
    }

    function mint(address holder, uint256 amount) external {
        require(msg.sender == controller, "Only controller");
        _mint(holder, amount);
    }

    function burn(address holder, uint256 amount) external {
        require(msg.sender == controller || msg.sender == holder, "Not authorized");
        _burn(holder, amount);
    }

    function _update(address from, address to, uint256 amount) internal override {
        // Skip tax for mints, burns, and controller operations
        if (from == address(0) || to == address(0) || msg.sender == controller) {
            super._update(from, to, amount);
            return;
        }

        // Apply transfer tax
        uint256 tax = (amount * TAX_RATE) / TAX_DENOMINATOR;
        uint256 netAmount = amount - tax;

        super._update(from, taxRecipient, tax);
        super._update(from, to, netAmount);
    }
}
```

### 示例：整合现有的社区代币

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

/// @notice Wrapper to make an existing token compatible with Juicebox.
/// @dev For tokens that already exist - create a wrapper that the JB controller can mint.
contract JBCompatibleToken is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    uint256 public immutable targetProjectId;

    constructor(
        string memory name,
        string memory symbol,
        uint256 _projectId,
        address controller
    ) ERC20(name, symbol) {
        targetProjectId = _projectId;
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, controller);
    }

    function decimals() public pure override returns (uint8) {
        return 18;
    }

    function canBeAddedTo(uint256 projectId) external view returns (bool) {
        return projectId == targetProjectId;
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyRole(MINTER_ROLE) {
        _burn(from, amount);
    }
}
```

### 示例：可编辑名称/符号的代币

允许项目所有者在不重新部署或迁移流量的情况下更改代币的名称/符号：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IJBProjects} from "@bananapus/core/src/interfaces/IJBProjects.sol";

contract EditableProjectToken is ERC20 {
    IJBProjects public immutable PROJECTS;
    address public immutable controller;
    uint256 public immutable projectId;

    string private _tokenName;
    string private _tokenSymbol;

    event NameUpdated(string oldName, string newName);
    event SymbolUpdated(string oldSymbol, string newSymbol);

    constructor(
        string memory initialName,
        string memory initialSymbol,
        address _controller,
        uint256 _projectId,
        IJBProjects projects
    ) ERC20(initialName, initialSymbol) {
        _tokenName = initialName;
        _tokenSymbol = initialSymbol;
        controller = _controller;
        projectId = _projectId;
        PROJECTS = projects;
    }

    modifier onlyProjectOwner() {
        require(msg.sender == PROJECTS.ownerOf(projectId), "NOT_OWNER");
        _;
    }

    function name() public view override returns (string memory) { return _tokenName; }
    function symbol() public view override returns (string memory) { return _tokenSymbol; }
    function decimals() public pure override returns (uint8) { return 18; }

    function canBeAddedTo(uint256 _projectId) external view returns (bool) {
        return _projectId == projectId;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == controller, "UNAUTHORIZED");
        _burn(from, amount);
    }

    /// @notice Update token name. Only callable by project owner.
    function setName(string calldata newName) external onlyProjectOwner {
        emit NameUpdated(_tokenName, newName);
        _tokenName = newName;
    }

    /// @notice Update token symbol. Only callable by project owner.
    function setSymbol(string calldata newSymbol) external onlyProjectOwner {
        emit SymbolUpdated(_tokenSymbol, newSymbol);
        _tokenSymbol = newSymbol;
    }
}
```

**注意**：一些去中心化交易所（DEX）或聚合器会缓存元数据。因此，更改可能需要一段时间才能生效。

### 权衡

| 方法 | 优点 | 缺点 |
|----------|------|------|
| **仅使用 Credits** | 部署成本为零，最简单 | 不支持转移，无法集成 DeFi 功能 |
| **标准 JBERC20** | 简单、兼容性强、经过审计 | 没有自定义功能 |
| **自定义 ERC20** | 可完全控制代币经济模型 | 复杂度更高，需要审计，且必须使用 18 个小数位 |

### 关键注意事项

1. **控制器必须具有铸造/销毁代币的权限**——JBController 需要在支付时铸造代币，并在现金退出时销毁代币。
2. **必须使用 18 个小数位**——Juicebox 的所有计算都基于 18 个小数位的代币。
3. **每个项目只能使用一个代币**——一个代币只能分配给一个项目。
4. **Credits 可以转换为代币**——在设置 ERC20 代币后，现有的 Credits 持有者可以领取代币。
5. **代币不能更改**——一旦设置好，就不能更换为其他类型的代币合约。

## 其他项目操作

### 转移所有权

项目所有权通过 ERC-721 NFT 来管理。使用标准的 ERC-721 协议进行转移：

```solidity
IJBProjects(PROJECTS).transferFrom(currentOwner, newOwner, projectId);
```

### 设置项目元数据

```solidity
IJBProjects(PROJECTS).setTokenURI(projectId, "ipfs://newUri");
```

### 添加终端

```solidity
IJBDirectory(DIRECTORY).setTerminalsOf(projectId, terminals);
```

## 生成指南

1. **了解项目需求**——包括所有权模型、代币经济模型和支付结构。
2. 如果需要自主运行，请考虑使用 Revnet。
3. **配置适当的元数据**——例如预留率、现金退出税和权限设置。
4. **使用 Foundry 生成部署脚本**。

## 示例提示

- “创建一个项目，每 ETH 铸造 1000 个代币，并预留 10%。”
- “设置一个每周向 3 个地址支付的项目。”
- “部署一个需要 3 天审批周期才能更改规则集的项目。”
- “创建一个同时接受 ETH 和 USDC 的项目。”

## 参考资料

- **nana-core-v5**：https://github.com/Bananapus/nana-core-v5
- **revnet-core-v5**：https://github.com/rev-net/revnet-core-v5