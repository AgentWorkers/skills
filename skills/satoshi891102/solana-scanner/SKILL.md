---
name: solana-scanner
description: 扫描任何 Solana 代币的安全性——包括流动性、持有者集中度、潜在风险以及欺诈行为的迹象。无需使用 API 密钥。
---

# Solana 代币扫描器

在交易之前，可分析任何 Solana 代币的安全性。该工具会检查代币的流动性、持有者集中度、价格走势以及潜在风险因素。所有功能均通过免费的公共 API 实现，无需任何密钥。

## 快速入门

要扫描一个代币，请运行扫描脚本，然后进行分析：

```bash
bash scripts/scan-token.sh <MINT_ADDRESS> | python3 scripts/analyze-token.py
```

## 示例

用户：“这个代币安全吗？EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v”
代理：“运行 `bash scripts/scan-token.sh EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | python3 scripts/analyze-token.py`”

用户：“扫描 BONK 代币”
代理：“查询 BONK 的发行地址（DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263），然后运行扫描。”

用户：“检查这个表情币是否属于‘rug’（骗局代币）”
代理：“获取发行地址后，再运行扫描。”

## 检查内容

| 检查项 | 检查内容 | 风险信号 |
|-------|------|-------------|
| 流动性 | 代币池的美元规模 | <1,000 美元 = 几乎可以确定是‘死币’/骗局代币 |
| 成交量 | 24 小时交易量 | <100 笔 = 该代币几乎无法交易 |
| 持有者 | 最大持有者集中度 | >50% = 极高的风险 |
| 发行时间 | 代币创建时间 | <24 小时 = 风险极高 |
| 价格 | 24 小时价格变动 | >-50% = 代币可能正在被抛售 |
| 交易平台 | 该代币在哪个交易所交易 | 无交易所 = 无法交易 |

## 安全评分

| 评分 | 评级 | 含义 |
|-------|--------|---------|
| 80-100 | 🟢 相对安全 | 主要代币，流动性良好 |
| 60-79 | 🟡 警告 | 存在一些问题，请谨慎交易 |
| 40-59 | 🟠 高风险 | 存在多个风险因素 |
| 0-39 | 🔴 应避免 | 很可能是骗局或‘死币’ |

## 使用的 API（全部免费，无需密钥）  
- **DexScreener** — 流动性、成交量、价格、代币发行时间 |
- **Jupiter Price API** — 当前价格 |
- **Solana RPC** — 代币供应量、最大持有者信息 |

## 所需依赖项  
- `bash`、`curl`、`python3`（大多数系统默认安装）  
- 可选：环境变量 `SOLANA_RPC_URL` 用于自定义 RPC 服务（默认为公共主网）

## 限制  
- 公共 RPC 服务的请求速率限制可能会影响持有者数据的获取  
- 将 `SOLANA_RPC_URL` 设置为 Helius/QuickNode 端点以获取完整的持有者信息  
- DexScreener 提供的数据可能存在几分钟的延迟  
- 本工具仅提供分析结果，不构成财务建议 |