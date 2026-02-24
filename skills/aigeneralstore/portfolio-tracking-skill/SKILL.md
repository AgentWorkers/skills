---
name: portfolio-tracker
description: 这是一个完全在本地运行的投资组合跟踪工具。所有数据都存储在 `~/.portfolio-tracker/` 目录中。
---
# 投资组合追踪器技能

这是一个完全在本地运行的投资组合追踪工具。所有数据都存储在 `~/.portfolio-tracker/` 目录下。

## 架构

- **数据**：`~/.portfolio-tracker/data.json`（投资组合、资产、价格信息）
- **配置**：`~/.portfolio-tracker/config.json`（API 密钥、钱包地址、用户信息）
- **脚本**：TypeScript 编写的 CLI 工具，位于 `<skill-path>/scripts/` 目录下，通过 `npx tsx` 命令执行

## 首次设置

在运行任何脚本之前，请确保已安装所有依赖项：

```bash
npm install --prefix <skill-path>/scripts
```

请将 `<skill-path>` 替换为该技能的实际安装路径。

## 脚本的工作原理

每个脚本都是一个独立的 CLI 工具。可以通过以下命令来执行它们：

```bash
npx tsx <skill-path>/scripts/<script>.ts <command> [args]
```

这些脚本在需要时从标准输入（stdin）读取数据，并将结果以 JSON 格式输出到标准输出（stdout）。

### data-store.ts
- `load` — 读取投资组合数据（如果数据缺失，则创建默认数据）
- `save` — 将投资组合数据写入文件（从 stdin 读取 JSON 数据）
- `load-config` — 读取配置信息
- `save-config` — 将配置信息写入文件（从 stdin 读取 JSON 数据）

### fetch-prices.ts
- `crypto <symbol>` — 获取加密货币价格（数据来源：Binance 或 CoinGecko）
- `stock <symbol>` — 获取股票价格（数据来源：Yahoo Finance）
- `fx` — 获取 USD/CNY/HKD 的汇率
- `historical <symbol>` — 获取某资产的 3 年历史价格数据
- `search <query>` — 根据名称或符号搜索资产
- `refresh` — 批量刷新资产价格（数据来源：stdin 中的资产 JSON 数据）

### binance-sync.ts
- `sync <apiKey> <apiSecret>` — 从 Binance 获取所有账户的余额信息
- `validate <apiKey> <apiSecret>` — 验证 API 凭据

### ibkr-sync.ts
- `sync <token> <queryId>` — 通过 Flex Query 从 IBKR 获取账户持仓信息
- `validate <token> <queryId>` — 验证 IBKR 的账户凭证

### blockchain-sync.ts
- `sync <address> [chain]` — 从指定的区块链地址获取钱包余额信息（支持单个链或所有 5 个 EVM 链）
- `validate <address>` — 验证 EVM 地址的合法性

## 数据类型

### 资产（Asset）
```json
{
  "id": "unique-id",
  "type": "CRYPTO | USSTOCK | HKSTOCK | ASHARE | CASH",
  "symbol": "BTC",
  "name": "Bitcoin",
  "quantity": 1.5,
  "avgPrice": 40000,
  "currentPrice": 50000,
  "currency": "USD | CNY | HKD",
  "transactions": [],
  "source": { "type": "manual | binance | wallet | ibkr" }
}
```

### 投资组合（Portfolio）
```json
{
  "id": "unique-id",
  "name": "Main",
  "assets": [...]
}
```

## 工作流程

### 查看投资组合
1. 使用 `data-store.ts load` 命令加载数据
2. 通过 `currentPortfolioId` 查找当前的投资组合
3. 使用 `quantity * currentPrice` 计算每个资产的总价值
4. 使用 `exchangeRates` 将总价值转换为显示货币
5. 以格式化表格的形式展示投资组合信息

### 添加资产
1. 加载数据
2. 使用 `fetch-prices.ts search <query>` 命令搜索资产
3. 使用 `fetch-prices.ts crypto/stock <symbol>` 获取资产当前价格
4. 使用生成的唯一 ID 将资产添加到当前投资组合中
5. 保存数据

### 刷新价格
1. 加载数据
2. 将当前投资组合中的资产信息通过 stdin 传递给 `fetch-prices.ts refresh` 命令
3. 同时运行 `fetch-prices.ts fx` 命令获取汇率
4. 更新每个资产的 `currentPrice` 和 `exchangeRates`
5. 将 `lastPriceRefresh` 设置为当前的时间戳
6. 保存数据

### 从交易所或钱包同步数据
1. 加载配置文件以获取 API 凭据
2. 运行相应的同步脚本
3. 合并数据：更新现有资产（根据符号和来源进行匹配），添加新资产
4. 保存数据

## 可用的命令
- `/portfolio` — 查看和管理投资组合
- `/prices` — 刷新所有资产的价格
- `/setup` — 配置 API 密钥和钱包信息
- `/sync-binance` — 从 Binance 同步数据
- `/sync-ibkr` — 从 IBKR 同步数据
- `/sync-wallet` — 从区块链钱包同步数据
- `/advise` — 获取智能投资建议