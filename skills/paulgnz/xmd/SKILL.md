---
name: xmd
description: Metal Dollar (XMD) 稳定币：铸造、赎回、供应量分析、抵押品储备、预言机价格
---

## Metal Dollar (XMD)

您可以使用相关工具来与 XMD（XPR Network 的原生稳定币）进行交互。XMD 是一种多抵押品稳定的加密货币，其价值与 1 美元挂钩，通过 `xmd.treasury` 合同进行铸造和赎回。

### XMD 的工作原理

- **铸造（Mint）：** 将支持的稳定币（例如 XUSDC）发送到 `xmd.treasury`，并附上 `mint` 指令，即可按预言机价格获得等值的 XMD。
- **赎回（Redeem）：** 将 XMD 发送到 `xmd.treasury`，并附上 `redeem,SYMBOL` 指令（例如 `redeem,XUSDC`），即可获得等值的稳定币。
- **1:1 挂钩（1:1 Peg）：** XMD 的价格与 1 美元保持 1:1 的固定比率，其价值由 `xmd.treasury` 中的抵押品储备支撑。
- **零费用（Zero Fees）：** 目前所有类型的抵押品在铸造和赎回过程中均不收取任何费用。

### 支持的抵押品

| 抵押品（Collateral） | 合同（Contract） | 预言机数据源（Oracle Feed） | 最大储备比例（Max Treasury %） | 状态（Status） |
|-------------|----------------|------------------|------------------|--------|
| XUSDC       | xtokens       | USDC/USD           | 60%                | 可铸造、可赎回 |
| XPAX       | xtokens       | PAX/USD           | 15%                | 可铸造、可赎回 |
| XPYUSD       | xtokens       | PYUSD/USD           | 15%                | 可铸造、可赎回 |
| MPD         | mpd.token       | MPD/USD           | 2%                | 可铸造、可赎回 |

### 相关合约（Contracts）

- `xmd.token`：XMD 代币合约（精度为 6 位小数，发行方为 `xmd.treasury`）  
- `xmd.treasury`：负责铸造/赎回逻辑、抵押品管理以及与预言机的集成  
- `oracles`：来自多个提供者的链上价格数据源  

### 只读工具（Read-Only Tools，无需签名）  

- `xmd_get_config`：获取 `xmd.treasury` 的配置信息（如暂停状态、费用账户、最低预言机价格阈值等）  
- `xmd_list_collateral`：列出所有支持的抵押品代币，包括费用、交易限额、预言机价格以及铸造/赎回量  
- `xmd_get_supply`：查询 XMD 的总流通量  
- `xmd_get_balance`：查看任意账户的 XMD 余额  
- `xmd_get_treasury_reserves`：获取支持 XMD 的稳定币储备情况（包含美元估值和抵押比率）  
- `xmd_get_oracle_price`：获取任意抵押品代币的当前预言机价格（包含具体提供者的数据）  

### 可写工具（Write-Only Tools，需要设置 `confirmed: true`）  

- `xmd_mint`：通过存入支持的稳定币来铸造 XMD  
- `xmd_redeem`：用指定的稳定币赎回 XMD  

### 安全规则（Safety Rules）  

- 铸造或赎回操作必须满足预言机价格 >= 0.995（`minOraclePrice`）的条件。  
- 每种抵押品都有 `maxTreasuryPercent` 的上限——如果 `xmd.treasury` 中已持有过多某种稳定币，将无法继续铸造该货币。  
- 在执行任何操作前，请检查 `isMintEnabled` 和 `isRedeemEnabled` 的状态。  
- 管理员可以暂停 `xmd.treasury` 的服务（`isPaused`），请先查看配置信息。  
- XMD 的精度为 6 位小数，所有金额均显示 6 位小数（例如 `1.000000 XMD`）。