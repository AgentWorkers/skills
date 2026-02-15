---
name: hyperliquid
description: 只读型 Hyperliquid 市场数据辅助工具（支持查看交易对手信息及现货交易数据，可选）；具备自然语言处理能力，能够解析终端风格的命令（如 `hl ...`）和斜杠风格的命令（如 `/hl ...`）。该工具可通过 https://api.hyperliquid.xyz/info 获取报价信息（包括标记价、中间价、Oracle 价格、资金流动情况、成交量）、市场活跃度最高的交易品种、资金流动排名、二级市场订单簿以及蜡烛图数据，并可将结果格式化后用于聊天界面。
---

# Hyperliquid（仅限读取）

使用 **Info** HTTP 端点实现 Hyperliquid 的只读市场数据查询：

- `POST https://api.hyperliquid.xyz/info`
- `Content-Type: application/json`

建议使用 **HTTP 快照** 方式获取数据（v1.0）；WebSocket 流式传输功能可后续添加。

## 支持的用户输入格式

以下输入格式视为等效：

- 自然语言：`Hyperliquid quote BTC`、`top movers 24h`、`book ETH`、`1h candles for SOL last 48`
- 终端命令格式：`hl quote BTC`、`hl movers --top 10 --window 24h`
- 斜杠命令格式：`/hl quote BTC`、`/hl overview`

系统会优先解析 `/hl` 和 `hl` 命令；如果没有指定前缀，则会尝试从自然语言输入中提取请求意图。

## 标准命令（v1.0）

市场数据：
- `quote <coin>`：显示价格、中间价或预言价、24小时价格变化（prevDayPx）、24小时名义成交量、未平仓合约数量（perps）、资金费用（perps）、溢价及影响价格
- `movers [--window 24h] [--top N]`：按24小时价格变化百分比（markPx vs prevDayPx）对交易对进行排名
- `funding-top|funding-bottom [--n N]`：按资金费用（仅限 perps）对交易对进行排名
- `book <coin>`：显示每个交易方向的最高20个价格层级（含价差）
- `candles <coin> --interval <1m|...|1M> [--last N | --start <ms> --end <ms>)`：查询指定时间范围内的蜡烛图数据
- `overview`：显示热门交易对、最高资金费用、最高未平仓合约数量及最高成交量

账户信息（仅限读取）：
- `positions <HL:0x..|0x..|label>`：显示未平仓合约信息及保证金概览
- `balances <HL:0x..|0x..|label>`：显示现货账户余额
- `orders <HL:0x..|0x..|label>`：显示未成交订单
- `fills <HL:0x..|0x..|label> [--n N]`：显示最近的交易成交记录

保存的账户别名（存储在本地文件 `~/.clawdbot/hyperliquid/config.json` 中）：
- `account list`：列出所有账户
- `account add "sub account 1" HL:0x... [--default]`：添加子账户“sub account 1”
- `account remove "sub account 1"`：删除子账户“sub account 1”
- `account default "sub account 1"`：将当前账户设置为默认子账户

以下自然语言命令也同样有效：
- `store this address HL:0x... as sub account 1`：将地址 HL:0x... 保存为子账户“sub account 1”
- `show me positions of sub account 1`：显示子账户“sub account 1”的未平仓合约信息

## 数据来源

永久性合约（Perpetuals）：
- `metaAndAssetCtxs`（推荐使用）：包含所有合约的上下文信息
- `l2Book`
- `candleSnapshot`

现货合约（可选，后续支持）：
- `spotMetaAndAssetCtxs`、`spotMeta`

有关请求体及字段含义的详细信息，请参阅 `references/hyperliquid-api.md`。

## 实现指南

请使用以下脚本：

- `scripts/hyperliquid_api.mjs`：轻量级 HTTP 客户端及辅助函数（提供默认设置和超时处理）
- `scripts/hyperliquid_chat.mjs`：解析用户输入，调用 API 功能，并生成易于阅读的响应内容

响应时请注意：
- 使用简洁的列表格式展示数据。
- 显示数据单位及时间范围。
- 对于缺失的字段，应优雅地处理（例如，中间价（midPx）可能为空）。

## 快速手动测试

可在本地运行以下命令进行测试：

```bash
node skills/hyperliquid/scripts/hyperliquid_chat.mjs "hl quote BTC"
node skills/hyperliquid/scripts/hyperliquid_chat.mjs "/hl movers --top 5"
```