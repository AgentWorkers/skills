---
name: openmm
version: 0.1.0
description: "开源的AI代理市场做市系统：支持多交易所交易、网格策略以及实时市场数据处理。提供命令行界面（CLI）、市场做市平台（MCP）以及相关开发工具（Skills）。"
tags: [trading, market-making, defi, crypto, exchanges, mcp, grid-trading]
metadata:
  openclaw:
    emoji: "📈"
    homepage: https://github.com/3rd-Eye-Labs/OpenMM
    docs: https://deepwiki.com/3rd-Eye-Labs/OpenMM
    requires:
      bins: [openmm]
    install:
      - kind: node
        package: "@3rd-eye-labs/openmm"
        bins: [openmm]
---
# OpenMM — 为AI代理提供的开源做市服务

OpenMM是一个开源的做市框架，支持多交易所交易、网格策略、实时市场数据以及自动化交易功能。所有功能都通过一个命令行界面（CLI）进行管理。

**GitHub仓库：** https://github.com/3rd-Eye-Labs/OpenMM  
**MCP服务器：** https://github.com/QBT-Labs/OpenMM-MCP  
**文档：** https://deepwiki.com/3rd-Eye-Labs/OpenMM  

## OpenMM是什么？  

- **多交易所支持**：MEXC、Gate.io、Kraken、Bitget  
- **网格交易**：自动执行网格策略，可动态调整交易间距、数量和波动率  
- **市场数据**：提供所有交易所的报价、订单簿和近期交易记录  
- **订单管理**：支持限价单/市价单的提交、取消以及订单列表的查看  
- **Cardano DEX集成**：通过Iris协议发现Cardano DEX的流动性池，并提供聚合价格  
- **命令行界面（CLI）+ MCP服务器**：可通过CLI直接使用，或作为MCP服务器为AI代理提供服务  
- **开源项目**：采用MIT许可证，具有高度的可定制性  

## 快速入门  

### 选项A：使用CLI  

### 选项B：使用MCP服务器  

运行 `npx @qbtlabs/openmm-mcp` 以在本地启动MCP服务器。该服务器会向所有兼容MCP的客户端暴露所有功能。  

（请注意：实际代码块在文档中并未提供。）  

### 选项C：作为库使用  

（请注意：实际代码块在文档中并未提供。）  

## 环境设置  

交易所的登录凭据通过环境变量进行配置。这些凭据仅存储在本地，不会发送到服务器。请将它们添加到`.env`文件中或在shell中导出：  

（请注意：实际代码块在文档中并未提供。）  

## 符号格式  

- 使用标准格式：`BTC/USDT`、`ETH/USDT`、`INDY/USDT`、`ADA/EUR`、`BTC/USD`  
- CLI会自动将这些格式转换为各交易所支持的格式  
- Kraken同时支持USD/EUR等法定货币对和USDT加密货币对  

## 核心工具  

### 账户余额与投资组合  

可以查看连接的所有交易所的账户余额。每个交易所的余额需要单独查询，没有跨交易所的汇总功能。  

（请注意：实际代码块在文档中并未提供。）  

**选项：**  
- `-e, --exchange <exchange>` — 要查询的交易所  
- `-a, --asset <asset>` — 要查询的具体资产  
- `--json` — 以JSON格式输出结果  

### 市场数据  

提供实时价格、订单簿和交易历史记录。使用 `--symbol` 参数，并指定 `BASE/QUOTE` 格式。Kraken支持`ADA/EUR` 和 `BTC/USD` 等法定货币对。  

**报价信息：**  
- 当前价格、买价/卖价、价差、成交量  

**订单簿：**  
- 显示买价/卖价的深度信息  

**近期交易：**  
- 显示最新的交易记录，包括买卖明细  

**通用选项：**  
- `-e, --exchange <exchange>` — 要查询的交易所  
- `-s, --symbol <symbol>` — 交易对符号  
- `-l, --limit <limit>` — 显示的订单层级/数量（订单簿默认为10层，交易记录默认为20条）  
- `--json` — 以JSON格式输出结果  

### 订单管理  

可以在任何支持的交易所提交和管理订单。订单使用通过环境变量配置的交易所API凭据。  

**创建订单：**  
- `-e, --exchange <exchange>` — 使用的交易所  
- `-s, --symbol <symbol>` — 交易对  
- `--side <side>` — 订单类型（买/卖）  
- `--type <type>` — 订单类型（限价单/市价单）  
- `--amount <amount>` — 订单金额（以基础货币计）  
- `--price <price>` — 订单价格（限价单必填，市价单忽略）  
- `--json` — 以JSON格式输出结果  

**交易所注意事项：**  
- **Bitget**：SNEK/NIGHT对的价格精度为6位小数，数量精度为2位小数；需要输入密码。  
- **Kraken**：最小订单金额为5 EUR/USD，支持主要法定货币对。  
- **MEXC/Gate.io**：每笔订单的最小金额为1 USDT。  

### 网格交易  

网格策略会在当前价格附近以固定间隔自动提交买卖订单。随着价格波动，系统会自动调整订单并重新生成网格，从而捕捉每个周期内的价差。总订单数量 = 层级数 × 2。  

**策略启动时的输出：**  
（请注意：实际代码块在文档中并未提供。）  

**优雅关闭：** 按下 `Ctrl+C`，系统会取消所有未完成的订单，断开与交易所的连接，并显示最终状态。  

**必需参数：**  
- `--strategy grid` — 指定网格交易策略  
- `--exchange <exchange>` — 交易使用的交易所  
- `--symbol <symbol>` — 交易对  

**网格参数：**  
- `--levels <number>` — 每侧的网格层级数（默认为5层，最多10层，总订单数量 = 层级数 × 2）  
- `--spacing <decimal>` — 每层之间的基础价格间距（默认为0.02，即2%）  
- `--size <number>` — 基础订单数量（以报价货币计）  
- `--confidence <decimal>` — 交易所需的最低价格置信度（默认为0.6）  
- `--deviation <decimal>` — 触发网格重新生成的 price 偏差（默认为0.015）  
- `--debounce <ms>` — 网格调整之间的延迟时间（默认为2000毫秒）  
- `--max-position <decimal>` — 最大持仓比例（以余额的百分比计）  
- `--safety-reserve <decimal>` — 安全储备比例（以余额的百分比计）  
- `--dry-run` — 仅进行模拟交易，不实际提交订单  

**动态网格参数：**  
- `--spacing-model <model>` — 线性、几何或自定义间距模型（默认为线性）  
- `--spacing-factor <number>` — 每层的几何间距放大倍数（默认为1.3）  
- `--size-model <model>` — 订单数量的分布模式（默认为均匀分布）  
- `--grid-profile <path>` — 从JSON配置文件加载完整的网格设置  

**波动率参数：**  
- `--volatility` — 启用基于波动率的动态价差调整  
- `--volatility-low <decimal>` — 低波动率阈值（默认为0.02）；低于此阈值时间距保持不变  
- `--volatility-high <decimal>` — 高波动率阈值（默认为0.05）；高于此阈值时间距会最大化  

**交易所注意事项：**  
- **MEXC/Gate.io**：每笔订单的最小金额为1 USDT；确保 `--size` 和 `--levels` 大于或等于1。  
- **Bitget**：SNEK/NIGHT对的价格精度为6位小数，需要输入密码。  
- **Kraken**：每笔订单的最小金额为5 EUR/USD；确保 `--size` 和 `--levels` 大于或等于5。  

### Cardano DEX集成  

OpenMM通过Iris协议与Cardano DEX的流动性池集成。支持的代币包括：**INDY**（Indigo Protocol）、**SNEK**（Snek Token）、**NIGHT**（Midnight）、**MIN**（Minswap）。  

价格计算方法为：从链上DEX池获取TOKEN/ADA的价格（按TVL加权），然后乘以CEX（如MEXC、Coingecko）提供的ADA/USDT价格，得到TOKEN/USDT的最终价格。  

**发现流动性池：**  
（请注意：实际代码块在文档中并未提供。）  

**获取实时价格：**  
（请注意：实际代码块在文档中并未提供。）  

**列出支持的代币：**  
（请注意：实际代码块在文档中并未提供。）  

**比较DEX与CEX的价格：**  
（请注意：实际代码块在文档中并未提供。）  

## 安全规则  

### 先进行模拟测试  

在执行任何网格策略之前，先预览一下将会提交的订单内容。  

### 执行前确认  

对于使用MCP的AI代理：  
1. **始终显示交易计划**：明确显示将要执行的操作。  
2. **获取用户确认**：未经用户同意不得自动执行交易。  
3. **使用 `dryRun: true`**：MCP的 `start_grid_strategy` 工具默认处于模拟模式。  

### 风险管理  

网格策略内置了风险控制机制：  
- `--max-position 0.6`：交易金额不超过账户余额的60%（默认为80%）。  
- `--safety-reserve 0.3`：保留30%作为安全储备（默认为20%）。  
- `--confidence 0.8`：交易前需要至少80%的价格置信度（默认为60%）。  

无论使用何种策略模型，总交易金额都会被自动限制。当订单成交或价格发生显著波动时，系统会重新生成网格（可通过 `--deviation` 参数进行配置）。  

## CLI参考  

### 账户余额与市场数据  
- `balance`：获取指定交易所的账户余额  
- `ticker`：获取当前价格、买价/卖价、价差和成交量  
- `orderbook`：获取订单簿的深度信息（买价/卖价）  
- `trades`：获取近期交易记录  
- `price-comparison`：比较Cardano代币在DEX和CEX上的价格  

### 订单相关命令  
- `orders list`：列出所有未完成的订单（或按代币筛选）  
- `orders get`：根据ID获取特定订单  
- `orders create`：提交限价单或市价单  
- `orders cancel`：根据ID取消订单  

### 交易相关命令  
- `trade --strategy grid`：启动网格交易策略  

### Cardano相关命令  
- `pool-discovery discover`：发现指定代币的DEX流动性池  
- `pool-discovery supported`：列出支持的Cardano代币  
- `pool-discovery prices`：获取实时聚合的池价格  

## 支持的交易所  

| 交易所 | 交易功能 | 网格交易 | 市场数据 | 最小订单金额 | 备注 |
|----------|---------|------|-------------|-----------|-------|  
| MEXC | ✅ | ✅ | ✅ | 1 USDT | 需要API密钥和密钥值 |
| Gate.io | ✅ | ✅ | ✅ | 1 USDT | 需要API密钥和密钥值 |
| Bitget | ✅ | ✅ | ✅ | 1 USDT | 需要API密钥和密码 |
| Kraken | ✅ | ✅ | ✅ | 5 EUR/USD | 需要API密钥和密钥值，支持法定货币对 |
| Binance | 🔜 | 🔜 | 🔜 | — | 即将支持 |
| Coinbase | 🔜 | 🔜 | 🔜 | — | 即将支持 |
| OKX | 🔜 | 🔜 | 🔜 | — | 即将支持 |

## 代理使用建议：  
- **先查看余额**：交易前务必运行 `openmm balance --exchange <ex>`  
- **使用 `--dry-run`**：在实际下单前预览网格策略的执行结果  
- **使用 `BASE/QUOTE` 格式**：例如 `BTC/USDT`、`ADA/EUR`、`SNEK/USDT`  
- **单独查询每个交易所的数据**：没有跨交易所的汇总功能  
- **注意API请求限制**：各交易所可能有请求次数限制，请合理安排请求  
- **安全存储凭据**：使用环境变量，切勿将凭据保存在`.env`文件中  
- **遵守最小订单要求**：MEXC/Gate.io/Bitget：每笔订单至少1 USDT；Kraken：5 EUR/USD  
- **使用 `--max-position` 和 `--safety-reserve`**：这些参数有助于控制风险  
- **Bitget需要密码**：通过 `BITGET_PASSPHRASE` 环境变量设置密码  
- **使用 `--json` 输出格式**：所有命令都支持JSON格式的输出  

## 使用OpenMM作为MCP服务器时的工具  

使用OpenMM作为MCP服务器时，可使用的工具包括：  

### 市场数据相关工具：  
- `get_ticker`：获取实时价格、买价/卖价、价差和成交量  
- `get_orderbook`：获取订单簿的深度信息（买价/卖价）  
- `get_trades`：获取近期交易记录（包括买卖摘要）  

### 账户相关工具：  
- `get_balance`：获取账户余额（全部或按资产筛选）  
- `list_orders`：列出所有未完成的订单（或按代币筛选）  

### 交易相关工具：  
- `create_order`：提交限价单或市价单  
- `cancel_order`：根据ID取消订单  
- `cancel_all_orders`：取消指定代币的所有未完成订单  

### 策略相关工具：  
- `start_grid_strategy`：计算并提交网格订单（默认为模拟模式）  
- `stop_strategy`：取消指定代币的所有订单，停止网格交易  
- `get_strategy_status`：获取订单状态、价格和价差信息  

### Cardano相关工具：  
- `get_cardano_price`：从DEX池获取代币的聚合价格（以ADA为桥梁）  
- `discover_pools`：发现指定代币的Cardano DEX流动性池  

### MCP相关资源：  
- `exchanges://list`：列出支持的交易所及其所需的凭据信息  
- `strategies://grid`：网格交易策略的文档  
- `strategies://grid/profiles`：提供不同风险级别的网格配置示例  

### MCP提示  
- `market_analysis`：分析交易对的相关数据（报价、订单簿和交易记录）  
- `portfolio_overview`：汇总交易所的账户余额和未完成订单信息  
- `grid_setup_advisor`：根据市场分析和账户余额推荐合适的网格配置  

## 附加技能  

针对特定工作流程，可学习以下附加技能：  
- `openmm-exchange-setup`：逐步配置交易所API凭据  
- `openmm-grid-trading`：创建和管理网格策略  
- `openmm-portfolio`：跟踪账户余额并在多个交易所间查看订单情况  

## 链接：  
- **GitHub仓库：** https://github.com/3rd-Eye-Labs/OpenMM  
- **MCP服务器：** https://github.com/QBT-Labs/OpenMM-MCP  
- **npm包：** https://www.npmjs.com/package/@3rd-eye-labs/openmm  
- **文档：** https://deepwiki.com/3rd-Eye-Labs/OpenMM  
- **Discord社区：** https://discord.gg/qbtlabs  

## 关于OpenMM  

OpenMM由[3rd Eye Labs](https://github.com/3rd-Eye-Labs)和[QBT Labs](https://qbtlabs.io)共同开发。  
**许可证：** MIT许可证