---
name: bifrost-slpx-info
description: >
  查询 Bifrost SLPx 液态质押协议在 Ethereum、Base、Optimism 和 Arbitrum 上的相关数据。  
  通过链上的 ERC-4626 存储库调用以及 Bifrost REST API，获取 vETH/ETH 的兑换率、年化收益率（APY）、总价值（TVL）、用户余额、赎回队列状态以及协议统计信息。  
  适用于用户咨询 Bifrost 的质押费率、vETH 价格、去中心化金融（DeFi）收益或 vToken 持有量等情况时使用。
metadata:
  author: bifrost.io
  version: "1.0.0"
---
# Bifrost SLPx 信息

通过调用 VETH ERC-4626 保险库合约的链上接口，查询 Bifrost vETH 液态质押数据。

## 合约与网络

vETH 部署在 Ethereum 及三个 L2 网络上。所有链上使用相同的合约地址。

| 链接 | ChainId | VETH 合约地址 | 底层资产（WETH） | 默认 RPC 地址 | 备用 RPC 地址 |
|-------|---------|---------------|--------------------|----|------|
| Ethereum | 1 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | `https://ethereum.publicnode.com` | `https://1rpc.io/eth` |
| Base | 8453 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://base.publicnode.com` | `https://1rpc.io/base` |
| Optimism | 10 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x4200000000000000000000000000000000000006` | `https://optimism.publicnode.com` | `https://1rpc.io/op` |
| Arbitrum | 42161 | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | `https://arbitrum-one.publicnode.com` | `https://1rpc.io/arb` |

## 配置（环境变量）

首次运行时，询问用户是否需要配置自定义设置。如果没有配置，将使用上述默认值。

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `BIFROST_CHAIN` | 目标链名称（`ethereum`、`base`、`optimism`、`arbitrum`） | `ethereum` |
| `BIFROST_RPC_URL` | 自定义 RPC 端点 | 上表中的链默认值 |
| `BIFROST_VETH_ADDRESS` | VETH 合约地址（可覆盖） | `0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8` |

## Bifrost 后端 API

可以通过 Bifrost REST API 获取协议级别的统计数据（无需 RPC 调用）：

```
GET https://api.bifrost.app/api/site
```

返回包含 `vETH` 对象的 JSON 数据，其中包含以下字段：

| 字段 | 描述 |
|-------|-------------|
| `apy` | 总年化收益率（基础收益 + 增值收益），例如 `"8.24"` |
| `apyBase` | 来自 Ethereum 验证者的基础质押年化收益率，例如 `"3.12"` |
| `apyReward` | 额外的 Bifrost 增值收益年化收益率，例如 `"5.12"` |
| `tvl` | 锁定的总价值（以 USD 计） |
| `tvm` | 总共铸造的 vETH 数量（以 ETH 计） |
| `totalIssuance` | Bifrost 链上的总 vETH 供应量 |
| `holders` | 所有链上的 vETH 持有者数量 |

当用户询问年化收益率（APY）、收益、锁定价值（TVL）或持有者数量时，可以使用此 API。

## 快速参考

vETH 是一个继承自 `VToken → VTokenBase → ERC4626Upgradeable` 的 ERC-4626 保险库代币。所有标准的 ERC-4626 查看函数都可用。汇率由 Oracle 提供支持。

### 代币信息

| 查询 | 函数 | 选择器 | 参数 | 返回值 | 描述 |
|-------|----------|----------|------|---------|-------------|
| 代币名称 | `name()` | `0x06fdde03` | 无 | 字符串 | 返回 `"Bifrost Voucher ETH"` |
| 代币符号 | `symbol()` | `0x95d89b41` | 无 | 字符串 | 返回 `"vETH"` |
| 小数位数 | `decimals()` | `0x313ce567` | 无 | uint8 | 返回 `18` |
| 底层资产 | `asset()` | `0x38d52e0f` | 无 | 地址 | 返回 WETH 地址（因链而异，详见“合约与网络”部分） |

### 汇率查询

| 查询 | 函数 | 选择器 | 参数 | 返回值 | 描述 |
|-------|----------|----------|------|---------|-------------|
| ETH → vETH 比率 | `convertToShares(uint256)` | `0xc6e6f592` | 资产（wei） | uint256（份额） | 使用当前 Oracle 汇率将 ETH 数量转换为等值的 vETH 份额 |
| vETH → ETH 比率 | `convertToAssets(uint256)` | `0x07a2d13a` | 份额（wei） | uint256（资产） | 使用当前 Oracle 汇率将 vETH 份额数量转换为等值的 ETH 金额 |
| 预览存款 | `previewDeposit(uint256)` | `0xef8b30f7` | 资产（wei） | uint256（份额） | 模拟存款并返回将铸造的 vETH 份额 |
| 预览铸造 | `previewMint(uint256)` | `0xb3d7f6b9` | 份额（wei） | uint256（资产） | 模拟铸造特定数量的 vETH 份额并返回所需的 ETH 金额 |
| 预览取款 | `previewWithdraw(uint256)` | `0x0a28a477` | 资产（wei） | uint256（份额） | 模拟取款并返回将燃烧的 vETH 份额 |
| 预览赎回 | `previewRedeem(uint256)` | `0x4cdad506` | 份额（wei） | uint256（资产） | 模拟赎回并返回将返还的 ETH 金额 |

### 用户余额与取款查询

| 查询 | 函数 | 选择器 | 参数 | 返回值 | 描述 |
|-------|----------|----------|------|---------|-------------|
| vETH 余额 | `balanceOf(address)` | `0x70a08231` | 所有者地址 | uint256 | 获取特定地址的 vETH 代币余额 |
| 可领取的 ETH | `canWithdrawalAmount(address)` | `0x52a630b9` | 目标地址 | (uint256, uint256, uint256) | 返回 `(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`。第一个值表示可领取的 ETH 金额 |
| 取款队列 | `getWithdrawals(address)` | `0x3a2b643a` | 目标地址 | 取款数组 | 返回取款条目数组，每个条目包含 `queued`（队列中的金额）和 `pending`（正在处理的金额）字段 |
| 最大可赎回额 | `maxRedeem(address)` | `0xd905777e` | 所有者地址 | uint256 | 所有者单次交易可赎回的最大 vETH 份额 |
| 最大可取款额 | `maxWithdraw(address)` | `0xce96cb77` | 所有者地址 | uint256 | 所有者单次交易可取出的最大 ETH 金额 |
| 最大可存款额 | `maxDeposit(address)` | `0x402d267d` | 收件人地址 | uint256 | 可存入接收者的最大 ETH 金额（通常类型为 uint256，最大值可能无限） |
| 最大可铸造额 | `maxMint(address)` | `0xc63d75b6` | 收件人地址 | uint256 | 可为接收者铸造的最大 vETH 份额（通常类型为 uint256，最大值可能无限） |
| 授予额度 | `allowance(address,address)` | `0xdd62ed3e` | 所有者, 支付者 | uint256 | 检查所有者授予支付者的 vETH 支出额度 |

### 协议统计

| 查询 | 函数 | 选择器 | 参数 | 返回值 | 描述 |
|-------|----------|----------|------|---------|-------------|
| 总资产 | `totalAssets()` | `0x01e1d114` | 无 | uint256 | 保险库管理的总 ETH 金额，来源于 Oracle 的 `poolInfo(asset)` |
| 总供应量 | `totalSupply()` | `0x18160ddd` | 无 | 该链上流通的总 vETH 代币数量 |
| 保险库余额 | `getTotalBalance()` | `0x12b58349` | 无 | 可用于支付的 ETH 金额（BridgeVault 余额 + 已完成的取款） |
| 队列中的取款 | `queuedWithdrawal()` | `0x996e5c06` | 无 | 全局队列中待取款的 ETH 总金额 |
| 已完成的取款 | `completedWithdrawal()` | `0x63ea1b92` | 无 | 全局已完成取款处理的 ETH 总金额 |
| 最大取款次数 | `maxWithdrawCount()` | `0xdc692cd7` | 无 | 用户同时进行的待处理取款条目最大数量 |
| 是否暂停 | `paused()` | `0x5c975abb` | 无 | 合约当前是否暂停（禁止存款/赎回） |

## 调用方法

所有查询均为只读操作，使用 `eth_call` —— 无需支付 gas，也无需签名。

**方法 A：直接调用**（推荐）
```bash
cast call <VETH_CONTRACT> \
  "<FUNCTION_SIGNATURE>(<ARG_TYPES>)(<RETURN_TYPES>)" <ARGS> \
  --rpc-url <RPC_URL>
```

示例 —— 查询 Ethereum 上 1 ETH 的汇率：
```bash
cast call 0xc3997ff81f2831929499c4eE4Ee4e0F08F42D4D8 \
  "convertToShares(uint256)(uint256)" 1000000000000000000 \
  --rpc-url https://ethereum.publicnode.com
```

**方法 B：curl + JSON-RPC**（如果直接调用不可用）
```bash
curl -s -X POST <RPC_URL> \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"<VETH_CONTRACT>","data":"<SELECTOR><ENCODED_ARGS>"},"latest"]}'
```

### Calldata 编码

- **无参数函数**：calldata 仅包含选择器（例如，`totalAssets()` 的选择器为 `0x01e1d114`）
- **uint256 类型参数**：选择器 + 十六进制表示的金额，左侧填充至 64 位
  - 例如：1 ETH = `0xDE0B6B3A76400000` → 填充为 `00000000000000000000000000000000000000000000de0b6b3a7640000`
- **地址参数**：选择器 + 地址（不包含前缀 `0x`），左侧填充至 64 位
  - 例如：`0xAbCd...1234` → 填充为 `000000000000000000000000AbCd...1234`

### 响应解码

- curl 返回 `{"result":"0x<hex>"}`。对于单个 uint256 类型值：将 64 位十六进制数转换为十进制，然后除以 1e18。
- `canWithdrawalAmount` 返回 3 个 uint256 类型的值（192 位十六进制）：`(totalAvailableAmount, pendingDeleteIndex, pendingDeleteAmount)`。前 64 位表示可领取的 ETH 金额。

## 代理行为

1. **环境检查**：首次交互时，询问用户是否需要配置 `BIFROSTCHAIN` 或 `BIFROST_RPC_URL`。如果没有配置，使用 Ethereum Mainnet 的默认值。
2. **RPC 选择**：如果设置了 `BIFROST_RPC_URL`，则使用该地址；否则使用对应链的默认 RPC 地址。如果 RPC 失败，将回退到链的备用 RPC 地址。
3. **多链支持**：当用户指定链（例如 "on Base"、"on Arbitrum"）时，切换到该链的 RPC 和 WETH 地址。
4. 所有数值均以 wei 为单位（18 位小数），显示前先转换为人类可读格式。
5. 如果未指定金额，查询默认显示 1 ETH 的汇率。
6. 如果未提供钱包地址，系统会提示输入地址；显示地址的前 6 位和后 4 位。
7. 如果 `canWithdrawalAmount` 的第一个值大于 0，表示有可领取的 ETH，并提示用户“领取我的赎回 ETH”。
8. 优先使用直接调用方法（`eth_call`）；如果直接调用失败，再使用 `curl` + JSON-RPC 并预先计算 calldata。
9. 始终获取最新数据，不进行缓存。
10. 如果 RPC 失败，尝试备用方法后再报告错误。
11. **实用链接**：在适用情况下，引导用户访问 [Bifrost vETH 页面](https://www.bifrost.io/vtoken/veth) 或 [Bifrost 应用](https://app.bifrost.io/vstaking/vETH)。

## 错误处理

| 错误类型 | 用户提示信息 |
|-------|-------------|
| RPC 失败 | “无法连接到 Ethereum。正在尝试使用备用端点...” |
| `convertToShares` 返回零 | “vETH 汇率暂时不可用。可能是合约暂停中。” |
| 取款数组为空 | “您没有待领取的 vETH。” |
| 地址无效 | “请输入有效的 Ethereum 地址（格式为 0x + 40 位十六进制）。” |
| `execution reverted` | 尝试使用另一种方法（直接调用或 curl）。如果两种方法都失败，向用户报告错误。 |

## 注意事项

1. vETH 继承自 `VToken → VTokenBase → ERC4626Upgradeable / OwnableUpgradeable / PausableUpgradeable`。所有标准的 ERC-4626 查看函数均可用。
2. 汇率由 Oracle 的 `oracle.poolInfo(asset)` 提供，可能与实际质押收益略有延迟。
3. `getWithdrawals` 返回一个包含 `queued`（队列中的金额）和 `pending`（Bifrost 正在处理的金额）的数组。
4. VETH 合同地址在 Ethereum、Base、Optimism 和 Arbitrum 上部署相同，但底层资产（WETH）地址因链而异。
5. `totalAssets()` 反映的是 Oracle 提供的全球池规模，而 `totalSupply()` 表示该链上的总 vETH 供应量。
6. `getTotalBalance()` 包括 BridgeVault 余额和已完成的取款金额，表示可立即支付的 ETH 金额。