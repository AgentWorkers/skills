---
name: indigo-assets
description: "查询 Indigo Protocol 的 iAssets、ADA 和 INDY 代币的实时价格和数据。"
allowed-tools: Read, Glob, Grep
license: MIT
metadata:
  author: indigoprotocol
  version: '0.1.0'
---
# iAsset 价格与数据

查询 Indigo 协议 iAssets（iUSD、iBTC、iETH、iSOL）以及 ADA 和 INDY 代币的实时价格和数据。

## MCP 工具

| 工具 | 描述 |
|------|-------------|
| `get_assets` | 获取所有 Indigo iAssets 的价格和利息数据 |
| `get_asset` | 获取特定 iAsset（iUSD、iBTC、iETH、iSOL）的详细信息 |
| `get_asset_price` | 获取特定 iAsset 的当前价格 |
| `get_ada_price` | 获取 ADA 的当前价格（以 USD 计） |
| `get_indy_price` | 获取 INDY 代币的当前价格（以 ADA 和 USD 计） |

## 子技能

- [资产价格](sub-skills/asset-prices.md) — 查询 iAsset 的价格和详细信息 |
- [代币价格](sub-skills/token-prices.md) — 查询 ADA 和 INDY 代币的价格 |

## 参考资料

- [MCP 工具参考](references/mcp-tools.md) — 工具的详细参数和返回类型 |
- [资产概念](references/concepts.md) — iAssets、预言机、INDY 代币以及利率