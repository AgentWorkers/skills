---
name: bifrost-slpx-stake
description: 在以太坊（Ethereum）、Base、Optimism 和 Arbitrum 上，针对 Bifrost SLPx 协议执行流动性质押（liquid staking）操作。用户可以通过质押 ETH 或 WETH 来 mint vETH（一种代币），并在赎回完成后领取 vETH。系统支持手动签名以及通过 ERC-4626 协议进行代理签名（agent-side signing）。适用于用户需要在 Bifrost DeFi 平台上执行质押、解质押、mint（创建新代币）、赎回或领取 ETH 等操作的场景。
metadata:
  author: bifrost.io
  version: "1.0.0"
---
# Bifrost SLPx 质押

执行 Bifrost vETH 液态质押操作：铸造（mint）、赎回（redeem）和提取（claim）。

## 合同与网络

vETH 部署在以太坊（Ethereum）以及三个 Layer-2（L2）网络上。所有链上使用相同的合约地址。

| 链路 | ChainId | VETH 合约地址 | WETH（基础资产） | 默认 RPC 端点 | 备用 RPC 端点 |
|-------|---------|---------------|--------------------|----|------|
| 以太坊 | 1 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | `https://ethereum.publicnode.com` | `https://1rpc.io/eth` |
| Base | 8453 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://base.publicnode.com` | `https://1rpc.io/base` |
| Optimism | 10 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://optimism.publicnode.com` | `https://1rpc.io/op` |
| Arbitrum | 42161 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | `https://arbitrum-one.publicnode.com` | `https://1rpc.io/arb` |

## 配置

首次运行时，会询问用户是否需要配置自定义设置。如果没有配置，则使用上述默认值。

### 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `BIFROST_CHAIN` | 目标链名称（`ethereum`、`base`、`optimism`、`arbitrum`） | `ethereum` |
| `BIFROST_RPC_URL` | 自定义 RPC 端点 | 上表中的链默认值 |
| `BIFROST_VETH_ADDRESS` | VETH 合约地址（可覆盖） | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` |
| `BIFROST_PRIVATE_KEY` | 代理端签名的私钥（十六进制格式，可带或不带前缀 0x） | 未设置（手动签名模式） |

### 钱包设置

有两种签名模式。默认为手动签名（无需额外设置）。

**默认：手动签名**

输出完整的交易详情（接收方、金额、数据、Gas 费用、链 ID）。用户使用自己的钱包（如 MetaMask、Ledger、CLI 等）进行签名。

**选项：代理端签名**

将 `BIFROST_PRIVATE_KEY` 设置为环境变量，或通过 Foundry 密钥库导入：

```bash
cast wallet import bifrost-agent --interactive
```

当设置了 `BIFROST_PRIVATE_KEY` 之后，代理可以立即使用 `cast send` 命令签名并广播交易。

## 快速参考

### 写入操作

| 操作 | 函数 | 选择器 | 描述 |
|-----------|----------|----------|-------------|
| 通过 ETH 铸造 vETH | `depositWithETH()` | `0x1166dab6` | 用 ETH 铸造 vETH。ETH 作为 `msg.value` 传递给合约。合约内部会将 ETH 转换为 WETH — 无需 ERC-20 批准。如果 `msg.value` 为 0，则回滚 `EthNotSent()` |
| 通过 WETH 铸造 vETH | `deposit(uint256,address)` | `0x6e553f65` | 直接用 WETH 存入合约以铸造 vETH。需要先获得 VETH 合约的批准 |
| 赎回 vETH | `redeem(uint256,address,address)` | `0xba087652` | 烧毁 vETH 来提取 ETH。ETH 会进入赎回队列，不会立即返回。需要满足 `owner == msg.sender` 或有足够的余额 |
| 以 ETH 形式提取 | `withdrawCompleteToETH()` | `0x3ec549e9` | 提取所有已完成的交易金额作为 ETH。内部会调用 `withdrawCompleteTo(this)`，然后将 WETH 转换为 ETH。如果 ETH 转移失败，则回滚 `EthTransferFailed()` |
| 以 WETH 形式提取 | `withdrawComplete()` | `0x266a3bce` | 提取所有已完成的交易金额作为 WETH 给 `msg.sender`。如果 `withdrawCompleteToETH()` 失败时使用此方法 |
| 提取到指定地址 | `withdrawCompleteTo(address)` | `0xf29ee493` | 将所有已完成的交易金额以 WETH 形式提取到指定地址 |

### 执行前查询函数

| 查询 | 函数 | 选择器 | 描述 |
|-------|----------|----------|-------------|
| 预览存款 | `previewDeposit(uint256)` | `0xef8b30f7` | 模拟存款操作并返回需要铸造的 vETH 数量 |
| 预览赎回 | `previewRedeem(uint256)` | `0x4cdad506` | 模拟赎回操作并返回将返回的 ETH 金额 |
| 备用：转换数量 | `convertToShares(uint256)` | `0xc6e6f592` | 使用当前 Oracle 汇率将 ETH 金额转换为 vETH 数量 |
| 备用：转换资产 | `convertToAssets(uint256)` | `0x07a2d13a` | 使用当前 Oracle 汇率将 vETH 数量转换为 ETH 金额 |
| vETH 余额 | `balanceOf(address)` | `0x70a08231` | 获取指定地址的 vETH 代币余额 |
| 最大可赎回数量 | `maxRedeem(address)` | `0xd905777e` | 所有者单次交易最多可赎回的 vETH 数量 |
| 可提取的 ETH 金额 | `canWithdrawalAmount(address)` | `0x52a630b9` | 返回 `(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`。第一个值表示可提取的 ETH 金额 |

## 调用方法

**读取查询** — 使用 `eth_call`（无需 Gas）：

```bash
# Method A: cast (preferred)
cast call <VETH_CONTRACT> \
  "<FUNCTION_SIGNATURE>(<ARG_TYPES>)(<RETURN_TYPES>)" <ARGS> \
  --rpc-url <RPC_URL>

# Method B: curl (if cast unavailable)
curl -s -X POST <RPC_URL> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"<VETH_CONTRACT>","data":"<SELECTOR><ENCODED_ARGS>"},"latest"]}'
```

如果 `previewDeposit` 或 `previewRedeem` 失败，将回退到 `convertToShares` / `convertToAssets`（使用相同的编码方式）。

**写入交易** — 使用 `cast send`（需要钱包）：

```bash
# Mint vETH (stake native ETH)
cast send <VETH_CONTRACT> \
  "depositWithETH()" --value <AMOUNT_IN_WEI> \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>

# Redeem vETH (unstake)
cast send <VETH_CONTRACT> \
  "redeem(uint256,address,address)" <SHARES_IN_WEI> <USER_ADDR> <USER_ADDR> \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>

# Claim ETH (withdraw completed redemptions)
cast send <VETH_CONTRACT> \
  "withdrawCompleteToETH()" \
  --rpc-url <RPC_URL> --private-key <PRIVATE_KEY>
```

### 数据编码（用于手动签名）

- **uint256**：将 wei 转换为十六进制，并左填充至 64 位 |
- **address**：去掉前缀 0x，然后左填充至 64 位 |
- `canWithdrawalAmount` 返回 3 个 `uint256` 类型（共 192 位十六进制）：`(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`。前 64 位表示可提取的 ETH 金额

## API 1：铸造 vETH（质押 ETH）

### 执行前

1. 查询汇率：`previewDeposit(amount)` → 预计的 vETH 数量 |
2. 检查钱包：`BIFROST_PRIVATE_KEY` 环境变量或 Foundry 密钥库 `bifrost-agent` |
3. 显示预览信息并等待用户确认（CONFIRM）

### 交易参数

| 字段 | 值 |
|-------|-------|
| 收件方 | `<VETH_CONTRACT>` |
| 金额 | 用户的 ETH 金额（wei） |
| 数据 | `0x1166dab6` |
| 链路 ID | 根据选择的链设置 |

### 手动签名后的输出

```
To:       <VETH_CONTRACT>
Value:    {wei} ({amount} ETH)
Data:     0x1166dab6
ChainId:  {chainId}
```

## API 2：赎回 vETH（解除质押）

### 执行前

1. 检查 `balanceOf(user)` 是否大于或等于赎回金额 |
2. 查询 `previewRedeem(shares)` → 预计的 ETH 金额 |
3. 检查 `maxRedeem(user)` |
4. 显示预览信息（注意：ETH 会进入赎回队列，不会立即处理）并等待用户确认（CONFIRM）

### 交易参数

| 字段 | 值 |
|-------|-------|
| 收件方 | `<VETH_CONTRACT>` |
| 金额 | `0` |
| 数据 | 编码后的赎回参数：`redeem(shares, userAddr, userAddr)` |
| 链路 ID | 根据选择的链设置 |

数据编码示例：`cast calldata "redeem(uint256,address,address)" <SHARES> <ADDR> <ADDR>`

## API 3：提取已赎回的 ETH

### 执行前

1. 检查 `canWithdrawalAmount(user)` — 第一个返回值表示可提取的 ETH 金额 |
2. 如果结果为 0：告知用户赎回操作可能仍在处理中 |
3. 如果结果大于 0：显示可提取的 ETH 金额并等待用户确认（CONFIRM）

### 交易参数

| 字段 | 值 |
|-------|-------|
| 收件方 | `<VETH_CONTRACT>` |
| 金额 | `0` |
| 数据 | `0x3ec549e9` |
| 链路 ID | 根据选择的链设置 |

## 代理行为

1. **环境检查**：首次交互时，询问用户是否需要配置 `BIFROSTCHAIN`、`BIFROST_RPC_URL` 或 `BIFROST_PRIVATE_KEY`。如果没有配置，则使用以太坊主网的默认设置和手动签名模式 |
2. **RPC 选择**：如果设置了 `BIFROST_RPC_URL`，则使用该地址；否则使用对应的链默认 RPC。如果 RPC 失败，则回退到链的备用 RPC |
3. **多链支持**：当用户指定链（例如 "on Base"、"on Arbitrum"）时，切换到相应的链的 RPC、WETH 地址和链 ID |
4. **钱包检测**：检查 `BIFROST_PRIVATE_KEY` 环境变量或 Foundry 密钥库 `bifrost-agent`。如果找到私钥，询问用户是否使用它。如果没有找到，则提供手动签名所需的交易数据 |
5. **确认操作**：显示交易预览信息（金额、汇率、预期结果、链 ID），并要求用户输入 **CONFIRM** 后再执行操作 |
6. **导入私钥需确认**：在导入私钥前显示安全警告，并要求用户确认 |
7. **私钥管理**：交易完成后，询问用户是否保留私钥 |
8. **余额检查**：在构建交易前验证是否有足够的 ETH/vETH |
9. **优先使用内置函数，备用 curl**：如果 `cast` 失败，使用预计算的数据 |
10. **保密性**：绝不显示私钥；地址信息仅显示前 6 位和最后 4 位 |
11 **操作完成后提示**：如果未配置钱包，建议用户设置钱包 |
12. 交易成功后，提供区块浏览器链接：`https://etherscan.io/tx/{hash}`（以太坊）、`https://basescan.org/tx/{hash}`（Base）、`https://optimistic.etherscan.io/tx/{hash}`（Optimism）、`https://arbiscan.io/tx/{hash}`（Arbitrum） |
13. **实用链接**：根据需要，引导用户访问 [Bifrost vETH 页面](https://www.bifrost.io/vtoken/veth) 或 [Bifrost 应用](https://app.bifrost.io/vstaking/vETH) |

## 安全性

1. 私钥设置为可选选项 — 默认情况下不显示交易数据 |
2. 每次写入操作都需要用户明确确认 |
3. 核对金额是否在余额和协议限制范围内 |
4. 建议使用专用钱包进行代理端签名 |

## 错误处理

| 错误代码 | 用户提示信息 |
|-------|-------------|
| `EthNotSent()` (0x8689d991) | “未包含 ETH。请指定金额。” |
| `EthTransferFailed()` | “ETH 转移失败。请尝试以 WETH 形式提取。” |
| `ZeroWithdrawAmount()` (0xd6d9e665) | “无法提取 ETH。您的赎回操作可能仍在处理中。” |
| `ERC4626ExceededMaxRedeem` (0xb94abeec) | “赎回金额超过上限。请检查余额。” |
| `Pausable: paused` | “VETH 合约处于暂停状态。请稍后再试。” |
| Insufficient ETH | “ETH 不足。当前余额：{bal}，所需金额：{amount + gas}。” |
| Insufficient vETH | “vETH 不足。当前余额：{bal}，所需数量：{amount}。” |
| Max withdraw count exceeded | “待赎回的次数过多。请先提取已有的 vETH。” |
| RPC failure | “无法连接。正在尝试使用备用端点……” |

## 注意事项

1. `depositWithETH()` 会通过 `WETH.deposit()` 将 ETH 内部转换为 WETH。无需 ERC-20 批准。直接使用 WETH 时，使用 `deposit(uint256,address)`（需要 WETH 批准） |
2. `withdrawCompleteToETH()` 会内部调用 `withdrawCompleteTo(address(this)` 来接收 WETH，然后通过 `WETH.withdraw()` 将 WETH 转换为 ETH 并发送给调用者。如果 ETH 转移失败，会使用 `withdrawComplete()` 来接收 WETH |
3. 赎回操作不是即时完成的 — `redeem()` / `withdraw()` 会将交易添加到赎回队列中，通过 Bifrost 的跨链机制分批处理 |
4. 所有写入操作都受到 `whenNotPaused` 和 `nonReentrant`（ReentrancyGuardUpgradeable）的保护 |
5. Gas 费用估计值仅供参考；建议使用 `cast estimate` 获取更准确的费用估算