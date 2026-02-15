---
name: maestro-bitcoin
description: 通过Maestro API实现全面的比特币区块链交互功能。支持7项API服务，包含119个端点，具体包括区块链索引、Esplora兼容性、RPC访问、事件管理、市场价格监控、内存池（mempool）管理以及钱包操作等。能够处理BTC交易、未花费的交易输出（UTXOs）、地址、区块、元协议（BRC20、Runes、Inscriptions/Ordinals）、Webhook以及实时数据等。
---

# Maestro Bitcoin 技能

这是一项全面的技能，用于通过 Maestro API 平台与 Bitcoin 区块链进行交互，提供了 7 个不同的 API 服务，共计 119 个终端点。

## 概述

该技能提供了对 Maestro Bitcoin API 套件的完整访问权限：

1. **区块链索引器 API**（37 个终端点）- 支持元协议的实时未花费交易输出（UTXO）数据
2. **Esplora API**（29 个终端点）- 兼容 Blockstream 的 REST API
3. **Node RPC API**（24 个终端点）- 基于 JSON-RPC 协议的访问
4. **事件管理器 API**（9 个终端点）- 实时 Webhook 和监控
5. **市场价格 API**（8 个终端点）- 开盘价、最高价、最低价和成交量（OHLC）数据及价格分析
6. **内存池监控 API**（9 个终端点）- 基于内存池的操作
7. **钱包 API**（6 个终端点）- 地址级别的活动跟踪

### 主要功能

- 查询地址、交易、区块和未花费交易输出（UTXO）
- 使用多种方法广播交易
- 跟踪 BRC20 代币、符文（Runes）和铭文（Inscriptions）
- 监控内存池并估算费用
- 为区块链事件设置 Webhook
- 访问市场价格数据和去中心化交易所（DEX）交易信息
- 基于内存池的余额和未花费交易输出查询
- 历史余额跟踪
- 收集和元协议统计信息

## 配置

### API 密钥设置

该技能需要一个 Maestro API 密钥。请设置 `MAESTRO_API_KEY` 环境变量：

```bash
export MAESTRO_API_KEY="your_api_key_here"
```

将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中以实现持久化：

```bash
echo 'export MAESTRO_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 获取 API 密钥

1. 在 [Maestro 控制面板](https://dashboard.gomaestro.org/signup) 注册
2. 创建新项目
3. 选择 Bitcoin 作为区块链
4. 选择您的网络（Mainnet 或 Testnet4）
5. 从项目控制面板复制 API 密钥

### 网络配置

该技能支持主网（Mainnet）和测试网（Testnet4）。请设置 `MAESTRO_NETWORK` 以切换网络：

```bash
# Use mainnet (default)
export MAESTRO_NETWORK="mainnet"

# Use testnet4
export MAESTRO_NETWORK="testnet"
```

## 使用方法

### 主要接口：Shell 脚本

主要接口是通过 `scripts/call_maestro.sh` 实现的，它提供了对所有 7 个 API 服务的访问。

#### 快速示例

```bash
# Get latest block height
./scripts/call_maestro.sh get-latest-height

# Get address balance
./scripts/call_maestro.sh get-balance bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

# Get address UTXOs
./scripts/call_maestro.sh get-utxos bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

# Get transaction details
./scripts/call_maestro.sh get-tx <tx_hash>

# Broadcast transaction
./scripts/call_maestro.sh broadcast-tx <hex_tx>

# Get mempool info
./scripts/call_maestro.sh get-mempool-info

# Estimate fee for 6 blocks
./scripts/call_maestro.sh estimate-fee 6

# Get BRC20 tokens
./scripts/call_maestro.sh list-brc20

# Get runes for address
./scripts/call_maestro.sh get-address-runes bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
```

### 各服务的可用命令

#### 区块链索引器命令

**地址操作：**
- `get-balance <address>` - 获取地址的比特币余额
- `get-utxos <address>` - 获取地址的未花费交易输出（UTXO）
- `get-address-txs <address>` - 获取地址的交易记录
- `get-address-activity <address>` - 获取地址的活动情况
- `get-address-stats <address>` - 获取地址的统计信息
- `get-balance-history <address>` - 获取地址的历史余额
- `get-address-runes <address>` - 获取地址的符文信息
- `get-address-rune-activity <address>` - 获取地址的符文活动情况
- `get-address-rune-utxos <address>` - 获取地址的符文未花费交易输出（UTXO）
- `get-address-brc20 <address>` - 获取地址的 BRC20 代币信息
- `get-address-inscriptions <address>` - 获取地址的铭文信息
- `get-address-inscription-activity <address>` - 获取地址的铭文活动情况

**区块操作：**
- `get-block <height_or_hash>` - 获取区块信息
- `get-block-txs <height_or_hash>` - 获取区块中的交易记录
- `get-block-inscriptions <height_or_hash>` - 获取区块中的铭文活动

**交易操作：**
- `get-tx <tx_hash>` - 获取交易信息
- `get-tx-metaprotocols <tx_hash>` - 获取包含元协议的交易
- `get-tx-output <tx_hash> <index>` - 获取交易输出信息
- `get-tx-inscriptions <tx_hash>` - 获取交易中的铭文活动

**BRC20 操作：**
- `list-brc20` - 列出所有 BRC20 代币
- `get-brc20 <ticker>` - 获取 BRC20 代币信息
- `get-brc20-holders <ticker>` - 获取 BRC20 代币持有者

**符文操作：**
- `list-runes` - 列出所有符文
- `get-rune <rune_id>` - 获取符文信息
- `get-rune-activity <rune_id>` - 获取符文活动情况
- `get-rune-holders <rune_id>` - 获取符文持有者
- `get-rune-utxos <rune_id>` - 获取符文的未花费交易输出（UTXO）

**铭文操作：**
- `get-inscription <inscription_id>` - 获取铭文信息
- `get-inscription-content <inscription_id>` - 获取铭文内容
- `get-inscription-activity <inscription_id>` - 获取铭文活动情况
- `get-collection <collection_symbol>` - 获取收藏信息
- `get-collection-stats <collection_symbol>` - 获取收藏统计信息
- `get-collection-inscriptions <collection_symbol>` - 获取收藏中的铭文

#### Esplora API 命令

- `esplora-address-info <address>` - 获取地址信息
- `esplora-address-txs <address>` - 获取地址的交易记录
- `esplora-address-utxos <address>` - 获取地址的未花费交易输出（UTXO）
- `esplora-block <hash>` - 获取区块信息
- `esplora-block-txs <hash>` - 获取区块中的交易记录
- `esplora-tx <txid>` - 获取交易信息
- `esplora-tx-hex <txid>` - 获取交易的十六进制表示
- `esplora-broadcast <tx_hex>` - 广播交易
- `esplora-mempool` - 获取内存池信息
- `esplora-tip-height` - 获取区块链的最新区块高度

#### Node RPC 命令

- `rpc-get-latest-block` - 获取最新区块
- `rpc-get-latest-height` - 获取最新区块高度
- `rpc-get-block <height_or_hash>` - 获取区块信息
- `rpc-get-block-miner <height_or_hash>` - 获取区块矿工信息
- `rpc-get-info` - 获取区块链信息
- `rpc-get-mempool-info` - 获取内存池信息
- `rpc-get-mempool-txs` - 获取内存池中的交易记录
- `rpc-get-mempool-tx <tx_hash>` - 获取内存池中的交易信息
- `rpc-get-tx <tx_hash>` - 获取交易信息
- `rpc-decode-tx <hex>` - 解码交易
- `rpc-broadcast-tx <hex>` - 广播交易
- `rpc-estimate-fee <blocks>` - 估算费用

#### 事件管理器命令

- `event-list-triggers` - 列出所有事件触发器
- `event-create-trigger <json>` - 创建事件触发器
- `event-get-trigger <id>` - 获取触发器详细信息
- `event-delete-trigger <id>` - 删除触发器
- `event-list-logs` - 列出事件日志
- `event-get-log <id>` - 获取事件日志详细信息

#### 市场价格命令

- `market-btc-price <timestamp>` - 获取指定时间的 BTC 价格
- `market-rune-price <rune_id> <timestamp>` - 获取指定时间的符文价格
- `market-list-dexs` - 列出支持的去中心化交易所（DEX）
- `market-list-runes` - 获取符文注册表
- `market-ohlc <dex> <symbol>` - 获取符文的 OHLC 数据
- `market-trades <dex> <symbol>` - 获取指定符文的交易记录

#### 内存池监控命令

- `mempool-get-balance <address>` - 获取基于内存池的余额
- `mempool-get-utxos <address>` - 获取基于内存池的未花费交易输出（UTXO）
- `mempool-get-runes <address>` - 获取基于内存池的符文信息
- `mempool-get-rune-utxos <address>` - 获取基于内存池的符文未花费交易输出（UTXO）
- `mempool-get-fee-rates` - 获取内存池的区块费用率
- `mempool-broadcast <hex>` - 带有传播跟踪的广播
- `mempool-get-tx-meta <tx_hash>` - 获取交易的元协议信息

#### 钱包 API 命令

- `wallet-get-activity <address>` - 获取基于内存池的钱包活动情况
- `wallet-get-meta-activity <address>` - 获取元协议活动情况
- `wallet-get-balance-history <address>` - 获取地址的历史余额
- `wallet-get-inscription-activity <address>` - 获取铭文活动情况
- `wallet-get-rune-activity <address>` - 获取符文活动情况
- `wallet-get-stats <address>` - 获取地址的统计信息

### 参考资料

- [API 参考](references/api_reference.md)：完整的终端点文档
- [示例](references/examples.md)：常见用例示例
- [官方文档](https://docs.gomaestro.org/bitcoin)：Maestro 文档

## 特点

### 元协议支持

全面支持 Bitcoin 元协议：
- **BRC20 代币**：查询代币、持有者和余额
- **符文（Runes）**：跟踪符文余额、活动和未花费交易输出（UTXO）
- **铭文（Inscriptions）**：查询铭文、收藏和内容

### 内存池感知

多个终端点提供基于内存池的查询功能，包括：
- 余额查询
- 未花费交易输出（UTXO）查询
- 符文和铭文跟踪
- 交易元协议

### 基于事件的架构

可以设置 Webhook 来监控：
- 地址活动
- 区块确认
- 交易事件
- 元协议操作

### 速率限制

Maestro 实施了两层速率限制：
- 基于订阅的每日信用额度限制
- 每秒请求次数上限

请在响应中查看速率限制头部信息：
- `X-RateLimit-Limit-Second`
- `X-RateLimit-Remaining-Second`
- `X-Maestro-Credits-Limit`
- `X-Maestro-Credits-Remaining`

## 注意事项

- 所有终端点都需要有效的 API 密钥进行身份验证
- 所有 API 调用都必须包含 `/v0` 版本前缀
- 列表终端点支持基于游标的分页
- 可以通过 `from` 和 `to` 参数过滤区块高度
- 支持主网（Mainnet）和测试网（Testnet4）
- 全面支持错误处理，并使用标准的 HTTP 状态码