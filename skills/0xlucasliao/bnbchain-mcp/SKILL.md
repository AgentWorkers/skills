---
name: bnbchain-mcp
version: 1.0.0
description: 与 BNB Chain Model Context Protocol (MCP) 服务器进行交互。该协议可用于查询去中心化金融 (DeFi) 数据、获取代币价格、搜索文档、获取 Git 差异文件，以及检索 BNB Chain 上的智能合约源代码。
---

# BNB Chain MCP 技能

此技能允许您与 BNB Chain MCP 服务器交互，以获取有关 BNB Chain 的数据。

## 使用方法

BNB Chain MCP 服务器在本地运行。您可以使用随此技能提供的 `mcp-client` 脚本与之进行交互。

### 命令

运行客户端脚本以执行相应操作：

```bash
python3 skills/bnbchain-mcp/scripts/mcp-client.py <tool_name> [arguments]
```

**列出可用工具：**

```bash
python3 skills/bnbchain-mcp/scripts/mcp-client.py list_tools
```

### 可用工具

`bnbchain-mcp` 中目前支持的工具包括：

- **get_token_price**：获取代币的价格（单位：USD）。`args: {"symbol": "BNB"}`
- **get_defi_rates**：获取协议的借贷利率。`args: {"protocol": "venus"}`
- **search_documentation**：搜索官方文档。`args: {"query": "validators"}`
- **get_recent-git_diffs**：获取仓库的最新 Git 提交差异。`args: {"repo_name": "bnb-chain/bsc"}`
- **get_smart_contract_source**：获取合约的源代码。`args: {"contract_address": "0x..."}`

## 设置

要使用此技能，必须确保 MCP 服务器正在运行。

如果服务器未运行，请启动它（通常由 MCP/OpenClaw 基础设施负责处理，但了解这一点还是有必要的）：
`uv run bnbchain-mcp`（需要安装 `uv` 和 `bnbchain-mcp` 包）。

## 示例

**获取 BNB 的价格：**
```bash
python3 skills/bnbchain-mcp/scripts/mcp-client.py get_token_price --args '{"symbol": "BNB"}'
```

**搜索文档：**
```bash
python3 skills/bnbchain-mcp/scripts/mcp-client.py search_documentation --args '{"query": "staking"}'
```