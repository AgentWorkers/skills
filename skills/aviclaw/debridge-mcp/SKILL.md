# deBridge MCP 技能

该技能使 AI 代理能够通过 deBridge 协议执行非托管式的跨链加密货币交换和转账操作。

## 功能概述

- **跨链交换**：在 20 多个区块链之间寻找最优路径并执行交易。
- **资产转移**：以比传统桥接工具更低的费用在区块链之间转移代币。
- **费用估算**：在执行交易前检查相关费用和条件。
- **非托管模式**：用户始终掌控自己的资产。

## 安装

```bash
# Clone the MCP server
git clone https://github.com/debridge-finance/debridge-mcp.git ~/debridge-mcp
cd ~/debridge-mcp
npm install
npm run build

# Add to OpenClaw config
# See configuration below
```

## 配置

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "plugins": {
    "entries": {
      "mcp-adapter": {
        "enabled": true,
        "config": {
          "servers": [
            {
              "name": "debridge",
              "transport": "stdio",
              "command": "node",
              "args": ["/home/ubuntu/debridge-mcp/dist/index.js"]
            }
          ]
        }
      }
    }
  }
}
```

然后重启 OpenClaw 服务：`openclaw gateway restart`

## 可用工具

当 MCP 连接成功后，代理可以使用以下工具：

- **get_quote**：获取跨链交易的报价信息。
- **create_order**：创建跨链交易订单。
- **get_status**：查询订单状态。
- **get_supported_chains**：列出支持的区块链。

## 使用示例

```
Ask: "Swap 100 USDC from Ethereum to Arbitrum"

Agent uses MCP to:
1. Get quote for USDC → USDC on Arbitrum
2. Show estimated receive amount and fees
3. Create order if user confirms
4. Monitor until completion
```

## 安全提示

- 在执行交易前务必核实报价信息。
- 请检查滑点容忍度设置。
- deBridge 使用的是 DLN（去中心化流动性网络），而非传统的桥接服务。
- 该系统不依赖任何流动性池，而是采用基于订单的匹配机制。

## 支持的区块链

Ethereum、Arbitrum、Optimism、Base、Polygon、Avalanche、BNB Chain、Solana 以及更多其他区块链。

---

**开发者**：Avi (github.com/aviclaw)