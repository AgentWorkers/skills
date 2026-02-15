# Clawlett

**Base Mainnet**上的安全代币交换服务，由Safe和Zodiac Roles提供支持。

**交换引擎：**CoW协议（采用MEV保护机制的批量拍卖系统）。

> **网络：Base Mainnet（链ID：8453）**

## 概述

该功能通过Gnosis Safe实现自主代币交换。代理通过Zodiac Roles来限制操作，具体包括：
- 使用CoW协议进行代币交换（受MEV保护）
- 批准CoW Vault Relayer的代币操作
- 通过ZodiacHelpers的delegatecall功能预签名CoW交易
- 将ETH封装为WETH或将WETH解封为ETH
- 仅将交换后的代币返回到Safe中（防止资金流失）

## 功能

| 功能 | 是否可自主执行 | 备注 |
|--------|------------|-------|
| 检查余额 | ✅ | 支持Base Mainnet上的ETH及所有ERC20代币 |
| 获取交换报价 | ✅ | 通过CoW协议获取 |
| 交换代币 | ✅ | 支持任何有流动性的代币对 |
| 将ETH封装为WETH/解封为ETH | ✅ | 通过ZodiacHelpers实现 |
| 批准代币交易 | ✅ | 仅限CoW Vault Relayer |
| 转账 | ❌ | 被Zodiac Roles禁止 |

## 代理名称（CNS）

每个代理必须通过Clawlett名称服务（CNS）注册一个**唯一名称**。该名称是代理在整个系统中的标识符——不允许两个代理使用相同的名称。名称将以NFT的形式在Base链上生成。

在初始化时使用`--name`参数选择名称，注册后无法更改。

## 代币安全性

### 已验证的代币

受保护的代币只能解析为经过验证的Base Mainnet地址：

| 代币 | 经验证的地址 |
|-------|--------------------|
| ETH | 原生ETH (`0x0000000000000000000000000000000000000000`) |
| WETH | `0x4200000000000000000000000000000000000006` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDT | `0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2` |
| DAI | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` |
| USDS | `0x820C137fa70C8691f0e44Dc420a5e53c168921Dc` |
| AERO | `0x940181a94A35A4569E4529A3CDfB74e38FD98631` |
| cbBTC | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` |
| VIRTUAL | `0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b` |
| DEGEN | `0x4ed4E862860beD51a9570b96d89aF5E1B0Efefed` |
| BRETT | `0x532f27101965dd16442E59d40670FaF5eBB142E4` |
| TOSHI | `0xAC1Bd2486aAf3B5C0fc3Fd868558b082a531B2B4` |
| WELL | `0xA88594D404727625A9437C3f886C7643872296AE` |
| BID | `0xa1832f7f4e534ae557f9b5ab76de54b1873e498b` |

如果存在冒充这些代币的诈骗代币，代理会检测到并发出警告。

### 未验证的代币搜索

未在验证列表中的代币将通过DexScreener（Base链上的交易对）进行搜索。搜索结果包括：
- 合同地址（在链上已验证）
- 24小时交易量和流动性
- 该代币的交易平台（DEX）

**对于未验证的代币，代理的行为：**
- 始终会显示包含合同地址、交易量和流动性的警告信息
- 在执行交换前要求用户确认
- 绝不自动交换未验证的代币

## 设置

1. 所有者提供他们的钱包地址并选择一个**代理名称**。
2. 代理生成密钥对 → 所有者在Base Mainnet上向代理发送0.001 ETH作为Gas费用。
3. 代理在Base Mainnet上部署Safe（所有者作为唯一所有者）。
4. 代理在后台注册并在链上生成CNS名称。
5. 代理部署具有交换权限的Zodiac Roles。
6. 代理移除自身作为Safe所有者的身份（但仍保留对Zodiac Roles的访问权限）。
7. 所有者在Base Mainnet上向Safe中注入代币以进行交易。

## 使用方法

### 初始化
```
Initialize my wallet with owner 0x123... and name MYAGENT
```

### 检查余额
```
What's my balance?
How much USDC do I have?
```

### 交换代币
```
Swap 0.1 ETH for USDC
Swap 100 USDC for ETH
Exchange 50 DAI to AERO
```

CoW协议的交换操作受到MEV保护。当需要时，ETH会自动封装为WETH（CoW协议要求使用ERC20代币）。封装过程会包含在交换交易中。

### 将ETH封装为WETH/解封为ETH
```
Wrap 0.5 ETH to WETH
Unwrap 0.5 WETH to ETH
```

封装和解封操作通过ZodiacHelpers的delegatecall功能完成。当通过CoW协议交换ETH时，封装过程会自动处理。

代理将：
1. 验证代币的真实性（防止诈骗）
2. 从CoW协议获取交换报价
3. **显示交换详情以供用户确认**：
   - 代币类型（例如，ETH → USDC）
   - 代币地址（经过验证的Base Mainnet合约地址）
   - 输入金额
   - 输出金额（预计收到的金额）
   - 费用明细
   - 如果适用，还包括ETH的封装金额
4. 请求用户明确确认
5. 通过Safe和Zodiac Roles执行交换操作

## 脚本

| 脚本 | 描述 |
|--------|-------------|
| `initialize.js` | 部署Safe和Zodiac Roles，并注册CNS名称 |
| `swap.js` | 通过CoW协议进行代币交换（受MEV保护） |
| `balance.js` | 检查ETH和代币的余额 |

### 示例
```bash
# Initialize (name is unique, app-wide identifier)
node scripts/initialize.js --owner 0x123... --name MYAGENT

# Check balance
node scripts/balance.js
node scripts/balance.js --token USDC

# Swap tokens (CoW Protocol, MEV-protected)
node scripts/swap.js --from ETH --to USDC --amount 0.1
node scripts/swap.js --from USDC --to WETH --amount 100 --execute
node scripts/swap.js --from USDC --to DAI --amount 50 --execute --timeout 600

# With custom slippage (0-0.5 range, e.g., 0.05 = 5%)
node scripts/swap.js --from ETH --to USDC --amount 0.1 --slippage 0.03 --execute
```

## 配置

脚本从`config/wallet.json`文件中读取配置（针对Base Mainnet进行配置）：
```json
{
  "chainId": 8453,
  "owner": "0x...",
  "agent": "0x...",
  "safe": "0x...",
  "roles": "0x...",
  "roleKey": "0x...",
  "name": "MYAGENT",
  "cnsTokenId": 1
}
```

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `BASE_RPC_URL` | `https://mainnet.base.org` | Base Mainnet的RPC接口地址 |
| `WALLET_CONFIG_DIR` | `config` | 配置文件目录 |

## 合约（Base Mainnet）

| 合约 | 地址 | 描述 |
|----------|---------|-------------|
| Safe Singleton | `0x3E5c63644E683549055b9Be8653de26E0B4CD36E` | Safe的L2实现合约 |
| CoW Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` | CoW协议的结算合约 |
| CoW Vault Relayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` | CoW代币的授权合约 |
| ZodiacHelpers | `0x9699a24346464F1810a2822CEEE89f715c65F629` | 用于批准交易、预签名CoW交易以及封装/解封WETH的合约 |
| Safe Factory | `0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2` | Safe的部署合约 |
| Roles Singleton | `0x9646fDAD06d3e24444381f44362a3B0eB343D337` | Zodiac Roles的部署合约 |
| Module Factory | `0x000000000000aDdB49795b0f9bA5BC298cDda236` | 模块的部署合约 |
| CNS | `0x299319e0BC8d67e11AD8b17D4d5002033874De3a` | Clawlett名称服务（代理的唯一名称） |

## 更新

当用户要求**“更新到最新版本”**时，请按照以下步骤操作：

1. 在clawlett仓库中执行`git fetch --tags origin`。
2. 从`scripts/package.json`中读取当前版本信息。
3. 确定最新的Git标签（例如，`git tag -l --sort=-v:refname | head -1`）。
4. 阅读`[MIGRATION_GUIDE.md`文件，了解当前版本与最新版本之间的迁移路径。
5. 向用户展示当前版本、新版本、变更内容以及是否需要在链上执行操作。
6. **询问用户：“您是否希望继续更新？”**——未经明确确认不得继续更新。
7. 如果用户同意，执行`git checkout <tag>`，然后与用户一起逐步完成每个迁移步骤。

某些更新仅涉及代码修改（只需切换到新标签即可）。其他更新则需要Safe所有者执行链上操作（例如，更新Zodiac Helpers合约的权限）。迁移指南会明确指出需要哪些操作。

## 安全模型

1. **所有资金由Safe保管**——代理的钱包中仅存放Gas费用。
2. **Zodiac Roles限制操作权限**：
   - 仅能与Zodiac Helpers交互
   - Zodiac Helpers的功能受到`allowTarget`的限制（仅能执行Send和DelegateCall操作）
   - 仅能批准CoW Vault Relayer的代币交易。
3. **禁止转账/提取资金**——代理无法将资金转出Safe。
4. **防止诈骗**——所有代币只能解析为经过验证的地址。
5. **MEV保护**——CoW协议采用批量交易机制，防止MEV攻击和其他形式的资金提取。