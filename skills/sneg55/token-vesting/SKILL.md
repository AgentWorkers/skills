---
name: sablier-vesting
description: 使用 Sablier Lockup 协议创建和管理代币归属流（包括线性、动态和分阶段分配两种方式）。
homepage: https://docs.sablier.com
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"⏳","requires":{"anyBins":["cast","forge"],"env":["ETH_RPC_URL"]},"primaryEnv":"ETH_PRIVATE_KEY"}}
---

# Sablier 资产分配技能

您是一个 AI 代理，使用 **Sablier Lockup v3.0** 协议在兼容 EVM 的区块链上创建和管理 **代币分配流**。Sablier 是一种代币流协议，其中创建者将 ERC-20 代币锁定在智能合约中，接收者的分配量会随着时间的推移逐渐增加，直到分配流结束。

## 何时使用此技能

当用户请求您执行以下操作时，请使用此技能：
- 创建代币分配流（线性、动态或分阶段分配）
- 将代币锁定在分配合约中
- 设置员工分配、投资者分配或空投分配
- 随时间将代币分配给接收者
- 取消、撤回或管理现有的 Sablier 分配流

---

## 安全性：私钥和密钥处理

**这些规则是强制性的。在每次交互中都必须遵守。**

### 代理行为约束

1. **切勿要求用户在聊天中粘贴私钥。** 如果用户主动在消息中提供原始私钥，请立即警告他们这可能会导致私钥被记录，并建议他们更换私钥。
2. **切勿在任何执行的命令中嵌入原始私钥。** 始终使用环境变量引用（`$PRIVATE_KEY`、`$ETH_PRIVATE_KEY`）或安全的签名方法。
3. **切勿将私钥或助记词记录、回显或打印到 stdout、文件或其他输出中。**
4. **始终推荐最安全的签名方法**，优先顺序如下：
   - **硬件钱包**：`--ledger` 或 `--trezor` 标志（最安全，不会暴露私钥）
   - **Foundry 密钥库**（`cast wallet import`）：`--account <name>`（在签名时提示输入密码）
   - **环境变量**：`--private-key $ETH_PRIVATE_KEY`（私钥仅存在于 shell 环境中，不会出现在命令文本中）
   - **原始的 `--private-key 0x...`：仅适用于临时测试网，因为这些测试网中的私钥没有实际价值）

### 设置安全签名

**选项 1 – 硬件钱包（推荐用于主网）：**

无需额外设置。只需在任何 `cast send` / `forge` 脚本命令中添加 `--ledger` 或 `--trezor` 即可。

**选项 2 – Foundry 加密密钥库（推荐默认设置）：**

```bash
# Import a key once (you'll be prompted for the private key and an encryption password)
cast wallet import my-deployer --interactive

# Then use it in any command
cast send ... --account my-deployer
```

密钥存储在 `~/.foundry/keystores/my-deployer` 中。您只需在签名时输入密码；私钥不会出现在 shell 历史记录或进程参数中。

**选项 3 – 环境变量（可接受）：**

```bash
# Export in your shell session (not in a file that gets committed)
export ETH_PRIVATE_KEY=0x...

# Reference the variable (the key value never appears in the command itself)
cast send ... --private-key $ETH_PRIVATE_KEY
```

### RPC URL 处理

RPC URL 可能包含 API 密钥。请遵循相同的原则：

```bash
# Set once in your shell
export ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/<YOUR_KEY>

# cast and forge automatically read ETH_RPC_URL, so --rpc-url can be omitted
cast send <ADDRESS> "approve(address,uint256)" ...
```

或者，您可以在 `foundry.toml` 的 `[rpc_endpoints]` 部分配置 RPC。

---

## 核心概念

### 流类型

Sablier Lockup v3.0 在每个链上使用一个统一的 **SablierLockup` 合约。有三种流模型：

| 模型 | 适用场景 | 功能（持续时间） | 功能（时间戳） |
|---|---|---|---|
| **线性** | 固定速率分配、薪资 | `createWithDurationsLL` | `createWithTimestampsLL` |
| **动态** | 指数曲线、自定义曲线 | `createWithDurationsLD` | `createWithTimestampsLD` |
| **分阶段** | 定期解锁（每月、每季度） | `createWithDurationsLT` | `createWithTimestampsLT` |

### 流形状

- **线性**：固定支付速率（恒定函数）。适用于薪资和简单的分配。
- **悬崖解锁**：在达到特定时间点之前无法获取代币；之后按固定速率分配。适用于员工分配（例如：1 年的悬崖期 + 3 年的线性分配）。
- **初始解锁**：立即释放部分代币，其余部分按固定速率分配。适用于奖励发放。
- **指数型**：接收者随时间获得越来越多的代币。适用于激励长期持有的空投。
- **分阶段解锁**：传统的定期解锁（每周/每月/每年）。适用于投资者分配。
- **每月解锁**：每月同一天解锁代币。适用于薪资和员工股票期权计划（ESOP）。
- **加权解锁**：早期分配少量代币，后期分配大量代币（例如：4 年内分别分配 10%/20%/30%/40%）。
- **时间锁定**：所有代币在特定日期之前被锁定，之后全部释放。

---

## 部署地址（Lockup v3.0）

所有链使用相同的合约模式。主要网络的部署地址如下：

| 链接 | SablierLockup | SablierBatchLockup |
|---|---|---|
| **Ethereum** | `0xcF8ce57fa442ba50aCbC57147a62aD03873FfA73` | `0x0636d83b184d65c242c43de6aad10535bfb9d45a` |
| **Arbitrum** | `0xF12AbfB041b5064b839Ca56638cDB62fEA712Db5` | `0xf094baa1b754f54d8f282bc79a74bd76aff29d25` |
| **Base** | `0xe261b366f231b12fcb58d6bbd71e57faee82431d` | `0x8882549b29dfed283738918d90b5f6e2ab0baeb6` |
| **OP Mainnet** | `0xe2620fB20fC9De61CD207d921691F4eE9d0fffd0` | `0xf3aBc38b5e0f372716F9bc00fC9994cbd5A8e6FC` |
| **Polygon** | `0x1E901b0E05A78C011D6D4cfFdBdb28a42A1c32EF` | `0x3395Db92edb3a992E4F0eC1dA203C92D5075b845` |
| **BNB Chain** | `0x06bd1Ec1d80acc45ba332f79B08d2d9e24240C74` | `0xFEd01907959CD5d470F438daad232a99cAffe67f` |
| **Avalanche** | `0x7e146250Ed5CCCC6Ada924D456947556902acaFD` | `0x7125669bFbCA422bE806d62B6b21E42ED0D78494` |
| **Gnosis** | `0x87f87Eb0b59421D1b2Df7301037e923932176681` | `0xb778B396dD6f3a770C4B4AE7b0983345b231C16C` |
| **Scroll** | `0xcb60a39942CD5D1c2a1C8aBBEd99C43A73dF3f8d` | `0xa57C667E78BA165e8f09899fdE4e8C974C2dD000` |
| **Sonic** | `0x763Cfb7DF1D1BFe50e35E295688b3Df789D2feBB` | `0x84A865542640B24301F1C8A8C60Eb098a7e1df9b` |
| **Monad** | `0x003F5393F4836f710d492AD98D89F5BFCCF1C962` | `0x4FCACf614E456728CaEa87f475bd78EC3550E20B` |
| **Berachain** | `0xC37B51a3c3Be55f0B34Fbd8Bd1F30cFF6d251408` | `0x35860B173573CbDB7a14dE5F9fBB7489c57a5727` |

有关测试网的详细信息，请参阅：https://docs.sablier.com/guides/lockup/deployments

---

## 使用 `cast` 创建分配流的步骤

推荐使用 Foundry 的 `cast` CLI 工具。

### 先决条件

1. 发送者必须在其钱包中拥有 ERC-20 代币。
2. 发送者必须批准 SablierLockup 合约才能花费这些代币。
3. 您需要以下信息：RPC URL、签名方法（密钥库、硬件钱包或环境变量）、代币地址和接收者地址。
4. **在构建命令之前，请询问用户他们偏好的签名方法**。如果他们设置了密钥库，则默认使用 `--account <KEYSTORE_NAME>`；对于主网，则使用 `--ledger`。请参阅上述安全部分。

### 第 1 步：批准代币

```bash
cast send <TOKEN_ADDRESS> \
  "approve(address,uint256)" \
  <SABLIER_LOCKUP_ADDRESS> <AMOUNT_IN_WEI> \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

### 第 2 步：创建分配流

#### 选项 A：线性分配流（createWithDurationsLL）

这会创建一个线性分配流。`CreateWithDurations` 结构通过 ABI 编码为一个元组。

**createWithDurationsLL 的参数：**

```solidity
function createWithDurationsLL(
    Lockup.CreateWithDurations calldata params,
    LockupLinear.UnlockAmounts calldata unlockAmounts,
    LockupLinear.Durations calldata durations
) external returns (uint256 streamId);
```

其中：
- `Lockup.CreateWithDurations` = `(address sender, address recipient, uint128 depositAmount, address token, bool cancelable, bool transferable, string shape)`
- `LockupLinear.UnlockAmounts` = `(uint128 start, uint128 cliff)`
- `LockupLinear.Durations` = `(uint40 cliff, uint40 total)`

**示例：** 1 年线性分配 10,000 个代币，无悬崖期：

```bash
# Calculate values
# 10000 tokens with 18 decimals = 10000000000000000000000
# 52 weeks in seconds = 31449600

cast send <SABLIER_LOCKUP_ADDRESS> \
  "createWithDurationsLL((address,address,uint128,address,bool,bool,string),(uint128,uint128),(uint40,uint40))" \
  "(<SENDER>,<RECIPIENT>,10000000000000000000000,<TOKEN>,true,true,)" \
  "(0,0)" \
  "(0,31449600)" \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

**示例：** 4 年分配，1 年悬崖期：

```bash
# cliff = 365 days = 31536000 seconds
# total = 4 years = 126144000 seconds

cast send <SABLIER_LOCKUP_ADDRESS> \
  "createWithDurationsLL((address,address,uint128,address,bool,bool,string),(uint128,uint128),(uint40,uint40))" \
  "(<SENDER>,<RECIPIENT>,<AMOUNT_WEI>,<TOKEN>,true,true,)" \
  "(0,0)" \
  "(31536000,126144000)" \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

**示例：** 初始解锁 1,000 个代币，后续 3,000 个代币在悬崖期解锁（总共 10,000 个代币）：

```bash
cast send <SABLIER_LOCKUP_ADDRESS> \
  "createWithDurationsLL((address,address,uint128,address,bool,bool,string),(uint128,uint128),(uint40,uint40))" \
  "(<SENDER>,<RECIPIENT>,10000000000000000000000,<TOKEN>,true,true,)" \
  "(1000000000000000000000,2000000000000000000000)" \
  "(31536000,126144000)" \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

#### 选项 B：分阶段分配流（createWithDurationsLT）

用于定期解锁（每月、每季度等）。

```solidity
function createWithDurationsLT(
    Lockup.CreateWithDurations calldata params,
    LockupTranched.TrancheWithDuration[] calldata tranches
) external returns (uint256 streamId);
```

其中 `Tranche(Duration` = `(uint128 amount, uint40 duration)`

**示例：** 每季度解锁 2,500 个代币，共 4 次：

```bash
# Each quarter ≈ 13 weeks = 7862400 seconds

cast send <SABLIER_LOCKUP_ADDRESS> \
  "createWithDurationsLT((address,address,uint128,address,bool,bool,string),(uint128,uint40)[])" \
  "(<SENDER>,<RECIPIENT>,10000000000000000000000,<TOKEN>,true,true,)" \
  "[(2500000000000000000000,7862400),(2500000000000000000000,7862400),(2500000000000000000000,7862400),(2500000000000000000000,7862400)]" \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

#### 选项 C：动态分配流（createWithTimestampsLD）

用于指数曲线和自定义分配。

```solidity
function createWithTimestampsLD(
    Lockup.CreateWithTimestamps calldata params,
    LockupDynamic.Segment[] calldata segments
) external returns (uint256 streamId);
```

其中：
- `Lockup.CreateWithTimestamps` = `(address sender, address recipient, uint128 depositAmount, address token, bool cancelable, bool transferable, (uint40,uint40) timestamps, string shape)`
- `Lockup Timestamps` = `(uint40 start, uint40 end)`
- `LockupDynamic.Segment` = `(uint128 amount, UD2x18 exponent, uint40 timestamp)`

**示例：** 指数分配流（2 个阶段）：

```bash
# Get current timestamp
CURRENT_TS=$(cast block latest --rpc-url <RPC_URL> -f timestamp)
START_TS=$((CURRENT_TS + 100))
MID_TS=$((CURRENT_TS + 2419200))   # +4 weeks
END_TS=$((CURRENT_TS + 31449600))  # +52 weeks

cast send <SABLIER_LOCKUP_ADDRESS> \
  "createWithTimestampsLD((address,address,uint128,address,bool,bool,(uint40,uint40),string),(uint128,uint64,uint40)[])" \
  "(<SENDER>,<RECIPIENT>,<DEPOSIT_AMOUNT>,<TOKEN>,true,true,($START_TS,$END_TS),)" \
  "[(<AMOUNT_0>,1000000000000000000,$MID_TS),(<AMOUNT_1>,3140000000000000000,$END_TS)]" \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

注意：阶段中的指数使用 UD2x18 格式（18 位小数）。`1e18` 表示线性，`2e18` 表示二次曲线，`3.14e18` 表示更陡峭的曲线。

---

## 管理现有分配流

### 检查分配流状态

```bash
cast call <SABLIER_LOCKUP_ADDRESS> "statusOf(uint256)(uint8)" <STREAM_ID> --rpc-url <RPC_URL>
```

状态值：0=待处理，1=分配中，2=已完成，3=已取消，4=已结束

### 检查可提取的代币数量

```bash
cast call <SABLIER_LOCKUP_ADDRESS> "withdrawableAmountOf(uint256)(uint128)" <STREAM_ID> --rpc-url <RPC_URL>
```

### 从分配流中提取代币（接收者）

```bash
# First, calculate the minimum fee
FEE=$(cast call <SABLIER_LOCKUP_ADDRESS> "calculateMinFeeWei(uint256)(uint256)" <STREAM_ID> --rpc-url <RPC_URL>)

cast send <SABLIER_LOCKUP_ADDRESS> \
  "withdrawMax(uint256,address)" \
  <STREAM_ID> <RECIPIENT_ADDRESS> \
  --value $FEE \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

### 取消分配流（仅限发送者）

```bash
cast send <SABLIER_LOCKUP_ADDRESS> \
  "cancel(uint256)" \
  <STREAM_ID> \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

### 放弃取消权（仅限发送者，不可撤销）

```bash
cast send <SABLIER_LOCKUP_ADDRESS> \
  "renounce(uint256)" \
  <STREAM_ID> \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME>
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

### 检查已分配的代币数量

```bash
cast call <SABLIER_LOCKUP_ADDRESS> "streamedAmountOf(uint256)(uint128)" <STREAM_ID> --rpc-url <RPC_URL>
```

### 获取分配流的接收者地址

```bash
cast call <SABLIER_LOCKUP_ADDRESS> "getRecipient(uint256)(address)" <STREAM_ID> --rpc-url <RPC_URL>
```

---

## 使用 Forge 脚本（替代方案）

如果用户更喜欢使用 Solidity 脚本而不是原始的 `cast` 调用，您可以创建一个 Forge 脚本。请参考 `@sablier/lockup` npm 包。

### 安装依赖项

```bash
forge init sablier-vesting && cd sablier-vesting
bun add @sablier/lockup
```

### 示例 Forge 脚本

```solidity
// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.8.22;

import { Script } from "forge-std/Script.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { ISablierLockup } from "@sablier/lockup/src/interfaces/ISablierLockup.sol";
import { Lockup } from "@sablier/lockup/src/types/Lockup.sol";
import { LockupLinear } from "@sablier/lockup/src/types/LockupLinear.sol";

contract CreateVestingStream is Script {
    function run(
        address lockupAddress,
        address tokenAddress,
        address recipient,
        uint128 depositAmount,
        uint40 cliffDuration,
        uint40 totalDuration
    ) external {
        ISablierLockup lockup = ISablierLockup(lockupAddress);
        IERC20 token = IERC20(tokenAddress);

        vm.startBroadcast();

        // Approve Sablier to spend tokens
        token.approve(lockupAddress, depositAmount);

        // Build params
        Lockup.CreateWithDurations memory params;
        params.sender = msg.sender;
        params.recipient = recipient;
        params.depositAmount = depositAmount;
        params.token = token;
        params.cancelable = true;
        params.transferable = true;

        LockupLinear.UnlockAmounts memory unlockAmounts = LockupLinear.UnlockAmounts({ start: 0, cliff: 0 });
        LockupLinear.Durations memory durations = LockupLinear.Durations({
            cliff: cliffDuration,
            total: totalDuration
        });

        uint256 streamId = lockup.createWithDurationsLL(params, unlockAmounts, durations);

        vm.stopBroadcast();
    }
}
```

使用以下命令运行 Forge 脚本：

```bash
forge script script/CreateVestingStream.s.sol \
  --sig "run(address,address,address,uint128,uint40,uint40)" \
  <LOCKUP_ADDRESS> <TOKEN_ADDRESS> <RECIPIENT> <AMOUNT_WEI> <CLIFF_SECONDS> <TOTAL_SECONDS> \
  --rpc-url <RPC_URL> \
  --account <KEYSTORE_NAME> \
  --broadcast
# Or: --ledger | --trezor | --private-key $ETH_PRIVATE_KEY
```

---

## 重要注意事项

- **代币的小数位数很重要**：始终将人类可读的金额转换为 wei（例如，对于 18 位小数的代币：`amount * 1e18`）。使用 `cast --to-wei <amount>` 进行转换。
- **必须先获得批准**：发送者必须批准 SablierLockup 合约才能花费 ERC-20 代币。
- **可取消 vs 不可取消**：如果 `cancelable` 为 `true`，发送者可以取消并收回未分配的代币。设置为 `false` 以实现无信任的分配。
- **可转让性**：如果 `transferable` 为 `true`，接收者可以将分配流中的 NFT 转移到另一个地址。
- **Gas 成本**：线性分配流的成本最低（约 169k gas）。分阶段分配流的成本更高（4 个阶段约 300k gas）。动态分配流的成本取决于阶段数量。
- **分配流 NFT**：每个分配流都表示为一个由接收者拥有的 ERC-721 NFT。如果分配流是可转让的，NFT 也可以被转移。
- **最低 Solidity 版本**：Lockup 合约需要 Solidity 版本 v0.8.22 或更高。
- **Sablier UI**：您可以在 https://app.sablier.com 查看和管理分配流。

## 快速参考：持续时间转换

| 持续时间 | 秒数 |
|---|---|
| 1 天 | 86400 |
| 1 周 | 604800 |
| 30 天 | 2592000 |
| 90 天（季度） | 7776000 |
| 180 天（半年） | 15552000 |
| 365 天（1 年） | 31536000 |
| 730 天（2 年） | 63072000 |
| 1095 天（3 年） | 94608000 |
| 1461 天（4 年） | 126230400 |

## 资源

- 文档：https://docs.sablier.com
- Lockup 源代码：https://github.com/sablier-labs/lockup
- 示例：https://github.com/sablier-labs/evm-examples/tree/main/lockup
- 集成模板：https://github.com/sablier-labs/lockup-integration-template
- 部署地址：https://docs.sablier.com/guides/lockup/deployments
- Sablier 应用程序：https://app.sablier.com