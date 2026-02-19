# Clawlett

这是一个在**Base Mainnet**上提供安全令牌交换和Trenches交易功能的工具，由Safe和Zodiac Roles技术支持。

**交换引擎：** **CoW Protocol**（采用MEV保护机制的批量拍卖）。  
**令牌创建与交易：** **Trenches**（通过AgentKeyFactoryV3合约实现）。

> **网络：Base Mainnet（链ID：8453）**

## 概述

该工具支持通过Gnosis Safe自动执行令牌交换以及Trenches上的令牌创建和交易。代理通过Zodiac Roles来执行操作，这些角色限制了以下操作：
- 使用CoW Protocol进行令牌交换（受MEV保护）；
- 在Trenches的债券曲线上创建令牌；
- 在Trenches的债券曲线上买卖令牌；
- 批准CoW Vault Relayer的令牌操作；
- 通过ZodiacHelpers的delegatecall函数预签名CoW订单；
- 使用ZodiacHelpers将ETH封装为WETH或将WETH解封装为ETH；
- 确保交换后的令牌仅返回到Safe中（防止资金流失）。

## 功能

| 功能 | 是否支持自动执行 | 备注 |
|--------|------------|-------|
| 检查余额 | ✅ | 支持Base Mainnet上的ETH及所有ERC20令牌 |
| 获取交换报价 | ✅ | 通过CoW Protocol获取 |
| 交换令牌 | ✅ | 支持具有流动性的任意令牌对 |
| 封装/解封装ETH | ✅ | 通过ZodiacHelpers在ETH与WETH之间进行转换 |
| 批准令牌操作 | ✅ | 仅限CoW Vault Relayer |
| 创建令牌（Trenches） | ✅ | 通过AgentKeyFactoryV3的债券曲线创建令牌 |
| 买入令牌（Trenches） | ✅ | 使用ETH在债券曲线上买入令牌 |
| 卖出令牌（Trenches） | ✅ | 在债券曲线上卖出令牌 |
| 令牌信息 | ✅ | 从Trenches API获取令牌详情 |
| 令牌查询 | ✅ | 显示热门令牌、新上线令牌、交易量最大的令牌以及涨跌情况 |
| 转账 | ❌ | 由Zodiac Roles限制，无法执行转账操作 |

## 代理名称（CNS）

每个代理可以选择通过Clawlett Name Service（CNS）注册一个**唯一名称**。该名称是代理在整个系统中的标识符，两个代理不能使用相同的名称。名称将以NFT的形式在Base链上铸造。

在初始化时传递`--name`参数即可注册CNS名称；如果省略，则跳过注册步骤。一旦注册，名称将无法更改。

## 令牌安全性

### 已验证的令牌

受保护的令牌只能解析为经过验证的Base Mainnet地址：

| 令牌 | 验证地址 |
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

如果发现有假冒这些令牌的欺诈行为，代理会立即检测并警告用户。

### 未验证的令牌

未在验证列表中的令牌将通过DexScreener（Base链上的交易所）进行搜索。搜索结果包括：
- 合同地址（在链上已验证）；
- 24小时交易量和流动性；
- 该令牌交易的DEX。

**对于未验证的令牌，代理的行为：**
- 始终会显示包含合同地址、交易量和流动性的警告信息；
- 在执行交换前会要求用户确认；
- 绝不会自动交换未验证的令牌。

## 设置

1. 所有者提供他们的钱包地址（可选提供**代理名称**）；
2. 代理生成密钥对 → 所有者在Base Mainnet上向代理发送0.001 ETH作为gas费用；
3. 代理在Base Mainnet上部署Safe（所有者作为唯一所有者）；
4. 代理在后台注册，并可选地在链上注册CNS名称（如果提供了`--name`参数）；
5. 代理部署具有交换权限的Zodiac Roles；
6. 代理移除自身作为Safe所有者的权限（但仍保留对Zodiac Roles的访问权限）；
7. 所有者在Base Mainnet上向Safe中存入用于交易的令牌。

## 使用方法

### 初始化
```
Initialize my wallet with owner 0x123...
Initialize my wallet with owner 0x123... and name MYAGENT
```

### 检查余额
```
What's my balance?
How much USDC do I have?
```

### 交换令牌
```
Swap 0.1 ETH for USDC
Swap 100 USDC for ETH
Exchange 50 DAI to AERO
```

CoW Protocol的交换操作受MEV保护。当需要时，ETH会自动封装为WETH（CoW协议要求使用ERC20令牌）。封装过程会包含在交换交易中。

### 封装/解封装ETH
```
Wrap 0.5 ETH to WETH
Unwrap 0.5 WETH to ETH
```

封装和解封装操作通过ZodiacHelpers的delegatecall函数完成。当通过CoW协议交换ETH时，封装过程会自动处理。

### Trenches交易

Trenches支持在Base链上创建令牌和进行债券曲线交易。令牌通过AgentKeyFactoryV3合约创建，并在Uniswap V3风格的债券曲线上进行交易。

所有链上操作都通过ZodiacHelpers的包装函数（`createViaFactory`、`tradeViaFactory`）来执行，这些函数会验证合约地址，并在delegatecall调用中明确传递`ethValue`参数（因为`msg.value`在delegatecall中不可用）。

### 重要提示 — 令牌创建参数收集：

当用户请求创建令牌时，代理必须收集以下所有参数才能执行创建操作。如果用户提供的参数有任何缺失，代理应要求用户补全。切勿默认使用任何参数，必须始终与用户确认每个参数。

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| 名称 | 是 | 令牌的名称（例如：“My Token”） |
| 符号 | 是 | 令牌的 ticker 符号（例如：“MTK”） |
| 说明 | 是 | 令牌的描述 |
| 图片 | 是 | 令牌图片的路径（PNG/JPEG/WEBP格式，最大4MB） |
| 基础令牌 | 否 | 默认为`BID`或`ETH`，表示要与哪种令牌进行配对 |
| 反欺诈保护 | 否 | 默认启用（10分钟的保护机制）。询问用户是否需要启用或禁用 |
| 初始购买量 | 否 | 创建后立即购买的ETH数量（仅当反欺诈保护关闭时生效） |
| Twitter | 否 | 令牌的Twitter/X账户 |
| 网站 | 否 | 令牌的网站地址 |
| 团队分配 | 否 | 价格达到特定水平后团队可以获得的SSL份额 |

代理应在执行创建操作前向用户展示所有参数的详细信息（包括默认值）并获取用户的确认。

**令牌创建的默认设置：**
- 基础令牌：BID（使用`--base-token ETH`进行ETH配对）
- 反欺诈保护：启用（10分钟的保护窗口）
- 当反欺诈保护启用时，初始购买操作被禁止（代理在保护期间无法购买）
- 使用`--no-antibot`参数可以禁用保护并允许初始购买
- 使用`--image`参数可以上传自定义令牌图片（PNG/JPEG/WEBP格式，最大4MB）

**图片上传流程：**
- 图片会上传到`/api/skill/image`文件夹；
- 上传成功后，`imageUrl`会被传递给令牌创建API；
- 如果图片上传失败，令牌创建将失败（图片是必需的）。

**反欺诈保护和购买规则：**
- 代理在反欺诈保护激活期间（创建后的10分钟内）无法购买任何受保护的令牌；
- 这个规则适用于所有令牌，而不仅仅是代理创建的令牌；
- 客户端和后台都会执行此规则——后台会拒绝为受保护的令牌生成交换签名；
- 必须等待保护窗口结束后才能进行购买。

代理的操作步骤如下：
1. 通过`/api/skill/image`上传令牌图片（返回`imageUrl`）；
2. 从`/api/skill/token/create`获取创建签名（包含`imageUrl`）；
3. 显示令牌详情以获取用户确认；
4. 通过Safe和Zodiac Roles（使用delegatecall）执行创建操作；
5. 创建完成后，分享令牌页面的URL：`https://trenches.bid/tokens/[address]`。

代理还会执行以下操作：
1. 解析令牌符号（包括对欺诈行为的保护）；
2. 从CoW Protocol获取报价；
3. 显示交换详情以获取用户确认：
   - 令牌符号（例如：ETH → USDC）；
   - 令牌地址（经过验证的Base Mainnet合约地址）；
   - 输入金额（你想要出售的金额）；
   - 预计收到的金额；
   - 费用明细；
   - 如果适用，还包括ETH的封装金额；
4. 获取用户的明确确认；
5. 通过Safe和Zodiac Roles执行交换操作。

## 脚本

| 脚本 | 说明 |
|--------|-------------|
| `initialize.js` | 部署Safe和Zodiac Roles，并注册CNS名称 |
| `swap.js` | 通过CoW Protocol进行令牌交换（受MEV保护） |
| `balance.js` | 检查ETH和令牌的余额 |
| `trenches.js` | 在Trenches的债券曲线上创建和交易令牌 |

### 示例
```bash
# Initialize (name is optional, registers on CNS if provided)
node scripts/initialize.js --owner 0x123...
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

# Trenches: Create a token (BID base token by default, anti-bot ON)
node scripts/trenches.js create --name "My Token" --symbol MTK --description "A cool token"
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --base-token ETH
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --no-antibot --initial-buy 0.01
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --image ./logo.png

# Trenches: Buy/sell tokens
node scripts/trenches.js buy --token MTK --amount 0.01
node scripts/trenches.js sell --token MTK --amount 1000
node scripts/trenches.js sell --token MTK --all

# Trenches: Token info and discovery
node scripts/trenches.js info MTK
node scripts/trenches.js trending
node scripts/trenches.js trending --window 1h --limit 5
node scripts/trenches.js new
node scripts/trenches.js top-volume
node scripts/trenches.js gainers
node scripts/trenches.js losers
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

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `BASE_RPC_URL` | `https://mainnet.base.org` | Base Mainnet的RPC端点 |
| `WALLET_CONFIG_DIR` | `config` | 配置目录 |
| `TRENCHES_API_URL` | `https://trenches.bid` | Trenches API的端点 |

## 合约（Base Mainnet）

| 合约 | 地址 | 说明 |
|----------|---------|-------------|
| Safe Singleton | `0x3E5c63644E683549055b9Be8653de26E0B4CD36E` | Safe的L2实现合约 |
| CoW Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` | CoW协议的结算合约 |
| CoW Vault Relayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` | CoW令牌的分配目标合约 |
| ZodiacHelpers | `0xb34a6210013977FC7D6082287e03915a66249799` | 用于批准操作、预签名CoW订单、封装/解封装WETH以及处理Trenches交易的合约 |
| AgentKeyFactoryV3 | `0x2EA0010c18fa7239CAD047eb2596F8d8B7Cf2988` | 用于创建Trenches令牌和进行债券曲线交易的合约 |
| Safe Factory | `0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2` | Safe的部署合约 |
| Roles Singleton | `0x9646fDAD06d3e24444381f44362a3B0eB343D337` | Zodiac Roles的合约 |
| Module Factory | `0x000000000000aDdB49795b0f9bA5BC298cDda236` | 用于部署模块的合约 |
| CNS | `0x299319e0BC8d67e11AD8b17D4d5002033874De3a` | Clawlett Name Service的合约 |

## 更新

当用户请求“更新到最新版本”时，请按照以下步骤操作：
1. 在clawlett仓库中执行`git fetch --tags origin`；
2. 从`scripts/package.json`中读取当前版本信息；
3. 确定最新的git标签（例如：`git tag -l --sort=-v:refname | head -1`）；
4. 阅读`[MIGRATION_GUIDE.md`文件，了解当前版本和最新版本之间的迁移路径；
5. 向用户展示当前版本、新版本、变更内容以及是否需要执行链上操作；
6. **询问用户：“您是否确认要更新？”** — 未经用户确认不得直接进行更新；
7. 如果用户确认，执行`git checkout <tag>`，然后与用户一起完成每个迁移步骤。

某些更新仅涉及代码更改（只需切换到新标签即可）；而有些更新需要Safe所有者执行链上操作（例如更新ZodiacHelpers合约的权限）。迁移指南会明确指出哪些更新需要这些操作。

## 安全模型

1. **所有资金都存储在Safe中** — 代理的钱包仅持有gas；
2. **Zodiac Roles限制操作**：
   - 仅能与Zodiac Helpers交互；
   - Zodiac Helpers的功能受`allowTarget`参数的限制（只能执行Send和DelegateCall操作）；
   - 仅能批准CoW Vault Relayer的令牌操作；
3. **禁止转账/提取资金** — 代理无法将资金转出；
4. **反欺诈保护** — 受保护的令牌只能解析为经过验证的地址；
5. **MEV保护** — CoW Protocol采用批量交易机制，防止三明治攻击和其他形式的MEV提取。