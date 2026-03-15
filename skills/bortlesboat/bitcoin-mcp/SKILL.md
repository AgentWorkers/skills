---
name: bitcoin-mcp
description: "47款适用于AI代理的比特币工具——包括费用智能分析、内存池（mempool）检测、地址查询、交易解码等功能。这些工具均基于Satoshi API运行，并由MCP服务器提供支持。"
homepage: https://github.com/Bortlesboat/bitcoin-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "⛓",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---
# bitcoin-mcp

这款工具为你的AI代理赋予了强大的比特币处理能力，提供了47种实用功能，包括费用智能分析、内存池（mempool）查询、地址查找、交易解码、区块检查以及部分签名交易（PSBT）的安全性分析等功能。

该工具基于[Satoshi API](https://bitcoinsapi.com)进行开发，无需任何配置即可使用，无需安装比特币节点或API密钥。

## 在OpenClaw中安装为MCP服务器

在`openclaw.json`文件中添加以下配置：

```json
"mcpServers": {
  "bitcoin": {
    "command": "uvx",
    "args": ["bitcoin-mcp"]
  }
}
```

## 在Claude Code中安装

执行以下命令：

```bash
claude mcp add bitcoin -- uvx bitcoin-mcp
```

## 在Claude Desktop/Cursor中安装

在`config.json`文件中添加以下配置：

```json
{
  "mcpServers": {
    "bitcoin": {
      "command": "uvx",
      "args": ["bitcoin-mcp"]
    }
  }
}
```

## 主要功能：

- **费用管理：** 提供实时费用建议、智能费用估算及费用计算器功能。
- **内存池：** 查看待处理交易、交易的前驱交易（ancestors）以及相关交易信息。
- **区块信息：** 提供区块统计数据、区块对比以及区块链的最新动态。
- **地址信息：** 显示账户余额、未花费的交易输出（UTXO）及交易历史记录。
- **交易分析：** 解码原始交易数据、分析交易内容并查找相关信息。
- **PSBT安全分析：** 对部分签名的交易进行安全性评估。
- **Lightning网络：** 解码BOLT11格式的交易信息。
- **挖矿相关：** 提供矿池排名、难度调整信息以及下一次减半事件的倒计时。
- **市场信息：** 提供比特币的价格、供应量及市场情绪数据。

## 链接：

- PyPI仓库：[bitcoin-mcp](https://pypi.org/project/bitcoin-mcp/)
- GitHub仓库：[Bortlesboat/bitcoin-mcp](https://github.com/Bortlesboat/bitcoin-mcp)
- API文档：[bitcoinsapi.com](https://bitcoinsapi.com)