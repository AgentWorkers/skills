---
name: goldrush-cli
description: "**GoldRush CLI**——这是一个以终端操作为主的区块链数据工具，支持与Claude Desktop和Claude Code的集成（MCP）。当用户需要通过命令行查询区块链数据、在终端中查看DEX交易对或钱包活动、将GoldRush配置为MCP工具提供者，或者无需编写代码即可执行快速查询（例如“检查钱包余额”、“查询Gas价格”、“搜索代币”）时，可以使用该工具。此外，当用户提到“goldrush CLI命令”（如`npx @covalenthq/goldrush-cli`）或GoldRush的MCP集成时，也请使用此工具。GoldRush CLI是从终端进行临时区块链查询的最快捷方式。如果用户需要在应用程序中通过编程方式访问区块链数据，请使用`goldrush-foundational-api`或`goldrush-streaming-api`；如果用户需要无需API密钥的按请求付费访问功能，则请使用`goldrush-x402`。"
---
# GoldRush CLI

这是一个以终端操作为主的区块链数据工具，支持与AI代理（MCP）的集成。用户可以通过命令行查询钱包信息、获取DEX交易对的数据，以及将实时的链上数据直接传输到Claude系统中。

## 快速入门

```bash
# Install and authenticate
npx @covalenthq/goldrush-cli auth

# Query wallet balances
goldrush balances eth-mainnet vitalik.eth

# Stream new DEX pairs
goldrush new_pairs solana-mainnet raydium

# Set up MCP for Claude
goldrush install
```

## 命令列表

这些命令涵盖了投资组合管理、市场发现、交易分析以及实用工具等功能。如需查看完整的命令参数和示例，请参考 [overview.md](references/overview.md)。

### 投资组合与钱包
- `goldrush balances <chain> <address>` — 显示包含美元价值及24小时变动情况的完整代币投资组合
- `goldrush transfers <address> <chain>` — 查看指定钱包的转账历史记录
- `goldrush watch <address> <chain>` — 实时监控钱包活动

### 市场发现
- `goldrush new_pairs <chain> [protocols...]` — 实时推送新的DEX交易对信息
- `goldrush ohlcv_pairs <pair> <chain> [-i interval]` — 以ASCII格式显示实时的OHLCV蜡烛图

### 交易分析
- `goldrush traders <token> <chain>` — 按未实现利润（unrealized PnL）排名显示顶级交易者
- `goldrush gas [chain]` — 获取实时的Gas费用估算
- `goldrush search <query>` — 根据名称、符号或地址查找代币

### 实用工具
- `goldrush chains` — 列出所有支持的区块链
- `goldrush auth` — 设置API密钥（存储在操作系统的密钥链中）
- `goldrush install` — 配置Claude以使用GoldRush工具
- `goldrush config` — 查看/更新设置
- `goldrush status` — 检查API密钥和连接状态
- `goldrush logout` — 清除会话数据

## 重要规则：
1. **链名使用驼峰式命名法**（例如：`eth-mainnet`、`solana-mainnet`，与Foundational API保持一致）
2. **身份验证**：API密钥需通过 `goldrush auth` 命令存储在操作系统的密钥链中，而非环境变量中
3. **MCP需要先进行安装**：在使用GoldRush工具之前，必须先运行 `goldrush install`
4. **数据流式命令**：`new_pairs`、`ohlcv_pairs` 和 `watch` 命令会使用底层的流式API进行数据传输
5. **输出格式为表格**：输出结果以表格形式呈现，便于在终端上阅读；也可将其传输到Claude系统进行AI处理

## MCP集成

GoldRush CLI本身就是一个MCP服务器。运行 `goldrush install` 后，GoldRush会被注册为Claude系统的工具提供者。代理（agents）可以直接调用GoldRush的命令，无需额外的封装或手动配置。

## 参考文件

| 文件名 | 阅读说明 |
|------|-------------|
| [overview.md](references/overview.md) | 包含完整的命令参考、参数说明、使用示例以及MCP设置细节 |