# Clawlett

Clawlett支持在**Base Mainnet**上进行的安全代币交换和Trenches交易，这些功能由Safe和Zodiac Roles提供支持。

**交换引擎：**
- **KyberSwap**（DEX聚合器，用于寻找最佳交易路径）——默认选择
- **CoW Protocol**（受MEV保护的批量拍卖）

**代币创建与交易：**通过**Trenches**（使用AgentKeyFactoryV3合约）完成。

> **网络：Base Mainnet（链ID：8453）**

## 概述

该技能允许通过Gnosis Safe自动执行代币交换和Trenches代币的创建/交易。代理通过Zodiac Roles来限制操作，具体包括：
- 通过KyberSwap聚合器或CoW Protocol进行代币交换
- 在Trenches中创建代币
- 通过工厂购买和出售Trenches代币
- 批准KyberSwap Router和CoW Vault Relayer的代币交易
- 通过ZodiacHelpers的delegatecall执行交换操作
- 将ETH封装为WETH或将WETH解封装为ETH
- 确保交换后的代币仅返回到Safe中（防止资金流失）

## 执行策略

**重要提示：**除非用户明确要求，否则代理**绝对不能**执行任何链上交易。**任何交换、代币创建或交易请求的默认行为仅为**获取报价/预览**。代理应显示详细信息，并等待用户明确确认是否执行（例如：“执行”、“开始”、“可以”或“是的，进行交换”）。
- 示例指令：“将0.1 ETH兑换成USDC” → 获取报价并显示，但不会立即执行
- 示例指令：“将0.1 ETH兑换成USDC并执行” → 获取报价并显示后，再执行
- 即使显示报价并询问用户是否执行也是允许的，但代理必须等待用户的明确确认后才能执行

这一规则适用于所有链上操作：交换、代币创建、买入、卖出以及封装/解封装。

## 功能

| 功能 | 是否可自动执行 | 备注 |
|--------|------------|-------|
| 检查余额 | ✅ | 支持Base Mainnet上的ETH和所有ERC20代币 |
| 获取KyberSwap报价 | ✅ | 通过CoW Protocol（受MEV保护） |
| 获取KyberSwap报价 | ✅ | 通过KyberSwap聚合器（寻找最佳路径） |
| 交换代币 | ⚠️ | 需要用户明确确认 |
| 封装/解封装ETH | ⚠️ | 需要用户明确确认 |
| 批准交易 | ⚠️ | 仅限CoW Vault Relayer和KyberSwap Router，需要用户明确确认 |
| 创建代币 | ⚠️ | 需要用户明确确认 |
| 买入代币 | ⚠️ | 需要用户明确确认 |
| 卖出代币 | ⚠️ | 需要用户明确确认 |
| 代币信息 | ✅ | 从Trenches API获取代币详情 |
| 代币查询 | ✅ | 显示热门代币、新上市代币、交易量最大的代币以及涨跌情况 |
| 转账 | ❌ | 由Zodiac Roles禁止 |

## 代理名称（CNS）

每个代理可以选择通过Clawlett名称服务（CNS）注册一个**唯一名称**。该名称是代理在整个应用中的标识符——两个代理不能使用相同的名称。名称将以NFT的形式在Base链上铸造。

在初始化时传递`--name`参数以注册CNS名称。如果省略，则不会进行CNS注册。一旦注册，名称将无法更改。

## 代币安全性

### 已验证的代币

受保护的代币只能兑换为经过验证的Base Mainnet地址：

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

如果发现有假冒这些代币的诈骗行为，代理会立即检测并警告用户。

### 未验证的代币搜索

未在验证列表中的代币将通过DexScreener（Base链对）进行搜索。搜索结果包括：
- 合同地址（在链上已验证）
- 24小时交易量和流动性
- 该代币交易的DEX平台

**对于未验证的代币，代理的行为：**
- 始终会显示包含合同地址、交易量和流动性的警告信息
- 在执行交换之前，会请求用户确认
- 绝不会自动执行未验证代币的交换操作

## 设置流程

1. 所有者提供他们的钱包地址（以及可选的**代理名称**）
2. 代理生成密钥对 → 所有者向代理发送至少0.0001 ETH到Base Mainnet作为gas费用（建议至少发送0.001 ETH以覆盖所有部署交易）
3. 代理在Base Mainnet上部署Safe
4. 代理部署Zodiac Roles模块
5. 代理通过MultiSend配置角色的权限（启用模块、指定目标角色）
6. 代理在后端API上注册
7. 代理可以选择在链上注册CNS名称（如果提供了`--name`参数）
8. 代理将Safe的所有权转移给人类所有者，并将自己从所有者列表中移除（但仍保留对角色的访问权限）
9. 代理在ERC-8004身份注册表上注册，并将身份NFT转移到Safe中
10. 所有者在Base Mainnet上向Safe中注入代币以进行交易

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

### 交换代币
```
Swap 0.1 ETH for USDC
Swap 100 USDC for ETH
Exchange 50 DAI to AERO
```

**有两种交换引擎可供选择：**

**KyberSwap Aggregator**（默认）：
- 在多个DEX中寻找最佳交易路径
- 直接支持原生ETH（无需封装）
- 非常适合在分散的流动性市场中寻找最佳价格
- 收费率为0.1%

**CoW Protocol**：
- 受MEV保护的批量拍卖
- ETH会自动封装为WETH（CoW要求使用ERC20代币）
- 非常适合需要MEV保护的较大额交易
- 收费率为0.5%

**要明确使用CoW Protocol，请执行以下操作：**
```
Swap 0.1 ETH for USDC using CoW
Use cow to swap 100 USDC for ETH
```

### 封装/解封装ETH
```
Wrap 0.5 ETH to WETH
Unwrap 0.5 WETH to ETH
```

封装和解封装操作通过ZodiacHelpers的delegatecall完成。当通过CoW进行ETH交换时，封装过程会自动处理。

### Trenches交易

Trenches支持在Base链上创建和交易代币。代币的创建和交易是通过AgentKeyFactoryV3合约完成的。

所有链上操作都通过ZodiacHelpers的包装函数（`createViaFactory`、`tradeViaFactory`）来执行，这些函数会验证工厂地址，并在调用时传递`ethValue`参数（因为`msg.value`在delegatecall中不起作用）。

```
Create a token called "My Token" with symbol MTK
Create a token paired with BID (default base token)
Create a token with anti-bot disabled and an initial buy
Buy 0.01 ETH worth of MTK on Trenches
Buy 100 BID worth of CLAWLETT on Trenches
Buy all my BID into CLAWLETT
Sell all my MTK tokens
What's trending on Trenches?
Show me the top gainers
Get info on MTK token
```

**重要提示——代币创建参数收集：**
当用户请求创建代币时，代理在执行之前必须收集以下所有参数。如果用户的请求缺少任何参数，应要求他们提供缺失的值。切勿默认使用默认值——必须始终与用户确认每个参数。

| 参数 | 是否必需 | 说明 |
|-----------|----------|-------------|
| 名称 | 是 | 代币名称（例如：“My Token”） |
| 符号 | 是 | 代币的 ticker 符号（例如：MTK） |
| 说明 | 是 | 代币的描述 |
| 图片 | 是 | 代币图片的路径（PNG/JPEG/WEBP格式，最大文件大小为4MB） |
| 基础代币 | 否 | 可选参数 `BID` 或 `ETH` — 指定要与哪种代币进行交换 |
| 反机器人保护 | 否 | 默认启用（10分钟的保护窗口）。询问用户是否需要启用或禁用 |
| 初始购买 | 否 | 创建后立即购买的基础代币数量（取决于所选代币，可以是ETH或BID） |
| Twitter | 否 | 代币的Twitter/X账号 |
| 网站 | 否 | 代币的网站URL |
| 团队分配 | 否 | 价格达到特定位置后团队可以领取的SSL份额 |

代理应在执行创建操作之前向用户展示所有参数的摘要（包括默认值）并请求确认。

**代币创建的默认设置：**
- 基础代币：BID（使用`--base-token ETH`指定ETH）
- 反机器人保护：启用（10分钟的保护窗口）
- 如果启用了反机器人保护，初始购买将被阻止（代理在保护窗口内无法购买）
- 使用`--no-antibot`参数可以禁用保护并允许初始购买
- 使用`--image`参数可以附加自定义代币图片（PNG/JPEG/WEBP格式，最大文件大小为4MB）

**图片上传流程：**
- 图片会上传到`/api/skill/image`路径
- 上传后的`imageUrl`会传递给代币创建API
- 如果图片上传失败，代币创建将失败（图片是必需的）

**反机器人保护和购买规则：**
- 代理在当前激活反机器人保护期间（创建后的10分钟内）无法购买任何代币
- 这个规则适用于所有代币，而不仅仅是代理创建的代币
- 客户端和后端都会执行此规则——后端会拒绝为受保护的代币生成交换签名
- 必须等待保护窗口结束后才能进行购买

**代币创建流程：**
1. 通过`/api/skill/image`上传代币图片（返回`imageUrl`）
2. 从`/api/skill/token/create`获取创建签名（包含`imageUrl`）
3. **显示代币详情——切勿立即执行** |
4. **停止并等待用户明确确认** — 在获得确认后再继续
5. 只有在用户确认后，才能通过Safe和Zodiac Roles执行创建操作

## 脚本

| 脚本 | 说明 |
|--------|-------------|
| `initialize.js` | 部署Safe和Zodiac Roles，并注册CNS名称 |
| `swap.js` | 通过KyberSwap聚合器进行代币交换（默认路径） |
| `cow.js` | 通过CoW Protocol进行代币交换（受MEV保护） |
| `balance.js` | 检查ETH和代币余额 |
| `trenches.js` | 通过工厂创建和交易Trenches代币 |

### 示例
```bash
# Initialize (name is optional, registers on CNS if provided)
node scripts/initialize.js --owner 0x123...
node scripts/initialize.js --owner 0x123... --name MYAGENT

# Check balance
node scripts/balance.js
node scripts/balance.js --token USDC

# Swap tokens (KyberSwap Aggregator, default - optimal routes)
node scripts/swap.js --from ETH --to USDC --amount 0.1
node scripts/swap.js --from USDC --to ETH --amount 100 --execute
node scripts/swap.js --from DAI --to AERO --amount 50 --execute --slippage 1

# Swap tokens (CoW Protocol, MEV-protected)
node scripts/cow.js --from ETH --to USDC --amount 0.1
node scripts/cow.js --from USDC --to WETH --amount 100 --execute
node scripts/cow.js --from USDC --to DAI --amount 50 --execute --timeout 600

# With custom slippage (0-0.5 range, e.g., 0.05 = 5%)
node scripts/cow.js --from ETH --to USDC --amount 0.1 --slippage 0.03 --execute

# Trenches: Create a token (BID base token by default, anti-bot ON)
node scripts/trenches.js create --name "My Token" --symbol MTK --description "A cool token"
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --base-token ETH
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --no-antibot --initial-buy 0.01
node scripts/trenches.js create --name "My Token" --symbol MTK --description "desc" --image ./logo.png

# Trenches: Buy/sell tokens (amount is in base token: ETH or BID depending on pair)
node scripts/trenches.js buy --token MTK --amount 0.01
node scripts/trenches.js buy --token CLAWLETT --all
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

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `BASE_RPC_URL` | `https://mainnet.base.org` | Base Mainnet的RPC端点 |
| `WALLET_CONFIG_DIR` | `config` | 配置目录 |
| `TRENCHES_API_URL` | `https://trenches.bid` | Trenches API端点 |

## 合同（Base Mainnet）

| 合同 | 地址 | 说明 |
|----------|---------|-------------|
| Safe Singleton | `0x3E5c63644E683549055b9Be8653de26E0B4CD36E` | Safe的L2实现 |
| CoW Settlement | `0x9008D19f58AAbD9eD0D60971565AA8510560ab41` | CoW协议的结算服务 |
| CoW Vault Relayer | `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110` | CoW代币的分配目标 |
| KyberSwap Router | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` | KyberSwap的Meta聚合路由器V2 |
| ZodiacHelpers | `0x38441B5bd6370b000747c97a12877c83c0A32eaF` | 负责批准、CoW预签名、KyberSwap和WETH封装/解封装操作的代理 |
| AgentKeyFactoryV3 | `0x2EA0010c18fa7239CAD047eb2596F8d8B7Cf2988` | 用于Trenches代币创建和交易的代理 |
| Safe Factory | `0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2` | Safe的部署工具 |
| Roles Singleton | `0x9646fDAD06d3e24444381f44362a3B0eB343D337` | Zodiac Roles的代理 |
| Module Factory | `0x000000000000aDdB49795b0f9bA5BC298cDda236` | 模块的部署工具 |
| CNS | `0x299319e0BC8d67e11AD8b17D4d5002033874De3a` | Clawlett名称服务（用于代理的唯一名称） |

## 更新

当用户请求**“更新到最新版本”**时，请按照以下步骤操作：

1. 在clawlett仓库中执行`git fetch --tags origin`
2. 从`scripts/package.json`中读取当前版本信息
3. 确定最新的git标签（例如：`git tag -l --sort=-v:refname | head -1`
4. 阅读`[MIGRATION_GUIDE.md`文件，了解当前版本和最新版本之间的迁移路径
5. 向用户展示当前版本、新版本、变更摘要以及是否需要进行链上操作
6. **询问用户：“您是否希望继续更新？”** — 在没有明确确认之前不要继续操作
7. 如果用户同意，执行`git checkout <tag>`，然后与用户一起逐步完成每个迁移步骤

有些更新仅涉及代码更改（只需切换到新标签即可）。其他更新则需要Safe所有者执行链上操作（例如，更新ZodiacHelpers合约的权限）。迁移指南会明确指出哪些更新需要这些操作。

## 安全模型

1. **所有资金都存储在Safe中**——代理的钱包中仅包含gas费用 |
2. **Zodiac Roles限制操作**：
   - 仅能与ZodiacHelpers交互 |
   - ZodiacHelpers的操作受`allowTarget`参数的限制（只能执行Send和DelegateCall操作）
   - 仅能批准CoW Vault Relayer和KyberSwap Router的代币交易 |
3. **禁止转账/提取资金**——代理无法将资金转出 |
4. **防诈骗保护**——所有代币只能兑换为经过验证的地址 |
5. **MEV保护**——CoW协议采用批量交易方式，防止三明治攻击和其他形式的MEV提取行为