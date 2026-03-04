---
name: clipx-bnbchain-api-client
description: 这是一个用于私有 ClipX BNBChain API 的轻量级客户端，它仅返回 BNB Chain 的纯文本 JSON 标志数据和排名信息（无需使用爬虫技术，也无需 API 密钥）。
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---
## 响应规则（请先阅读）

**规则 1 — 菜单格式：** 始终使用编号行（1. 2. 3. …）。请参阅“交互式菜单”部分。

**规则 2 — 表格格式：** 始终将表格输出放在 markdown 代码块中（使用三个反引号）。以只包含三个反引号的行开始，然后是表格行，最后再以只包含三个反引号的行结束。这样表格才能以等宽字体显示，并且列对齐。

**规则 3 — 响应以表格结束。** 在关闭三个反引号后，您的消息就完成了。不要再添加任何内容。

---

## 该技能的功能

通过 `python "{baseDir}/api_client_cli.py"` 调用 ClipX BNBChain API，以获取纯文本形式的 BNB Chain 指标和排名数据。所有数据抓取工作由后端处理。

---

## 交互式菜单

当用户输入 “clipx”、“bnbchain”、“bnbchain analysis” 或请求 BNB Chain 报告但未指定具体类型时，请输出以下菜单：

🟡 ClipX / BNBChain 分析 — 请选择一项：

1. TVL 排名 — 按总锁定价值排名前十的协议
2. 费用排名 — 按 24 小时/7 天/30 天费用排名前十的协议
3. 收入排名 — 按收入排名前十的协议
4. DApp 排名 — 按用户数量排名前十的 DApp（7 天）
5. 全生态系统 — DeFi、游戏、社交、NFT、AI、基础设施领域的领先者
6. 社交热度 — 社交热度排名前十的代币
7. 模因排名 — 按得分排名前十的模因代币
8. 网络指标 — 最新区块、gas 价格、同步状态
9. 市场洞察 — Binance 24 小时交易量领先的货币对（以 USDT 计）
10. 市场洞察（实时） — 交易量领先者 + 最大涨幅者 + 最大跌幅者（快照）
11. Binance 公告 — Binance 最新的 10 条公告

请回复一个数字（1–11）。

---

## 命令（数字 → 命令）

| 编号 | 命令                                      |
|------|-----------------------------------------|
| 1    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC` |
| 2    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC` |
| 3    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 24h --timezone UTC` |
| 4    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC` |
| 5    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC` |
| 6    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC` |
| 7    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC` |
| 8    | `python "{baseDir}/api_client_cli.py" --mode metrics_basic`         |
| 9    | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight --timezone UTC` |
| 10   | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight_live --timezone UTC` |
| 11   | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type binance_announcements --timezone UTC` |

对于命令 2（费用排名）和命令 3（收入排名），默认间隔为 24 小时。如果用户指定 7 天或 30 天，则使用 `--interval 7d` 或 `--interval 30d`。

---

## 显示结果

客户端会打印一个格式化好的表格。您的任务是：

1. 运行相应的命令。
2. 获取标准输出（格式化的表格）。
3. 将其放入 markdown 代码块中（前面和后面各用三个反引号括起来）。
4. 发送即可。您的响应就完成了。

您的响应必须完全符合以下格式：

```
================================================================================
🚀 TOP 10 MEME TOKENS BY SCORE
================================================================================
--------------------------------------------------------------------------------
#   | NAME                 | —               | SCORE
--------------------------------------------------------------------------------
1   | TokenA               | —               | 4.76
2   | TokenB               | —               | 4.61
...
================================================================================
Source: @ClipX0_
```

---

## 网络指标（选项 8）

返回包含 `latest_block`、`gas_price_gwei`、`syncing` 的 JSON 数据。请用通俗的语言进行总结。

---

## 市场洞察（实时）——选项 10

使用 `market_insight_live` API 获取交易量领先者、最大涨幅者和最大跌幅者的信息（聊天中无需使用 `--live` 参数；OpenClaw 会显示静态信息。在本地使用 `--live` 可实现实时更新。）

## Binance 公告——选项 11

使用 `binance_announcements` API 获取最新的 10 条公告（按发布时间排序，不解析日期）。

---

## 其他模式

- `--mode metrics_block --blocks 100` — 显示最近区块的平均区块时间和 gas 使用量。
- `--mode metrics_address --address 0x...` — 显示指定地址的 BNB 余额和交易次数。

---

## 环境设置

API 的默认地址为 `http://5.189.145.246:8000`。可以通过 `CLIPX_API_BASE` 环境变量进行更改。