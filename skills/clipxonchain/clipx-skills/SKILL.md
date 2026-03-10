---
name: clipx-bnbchain-api-client
description: 这是一个用于私有 ClipX BNBChain API 的轻量级客户端工具，它仅返回 BNB Chain 的纯文本 JSON 格式的数据指标和排名信息。该工具无需使用任何爬虫技术，也不需要 API 密钥即可正常使用。
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---
## 响应规则（请先阅读）

**规则 1 — 菜单格式：** 始终使用编号行（1. 2. 3. …）。请参阅“交互式菜单”部分。

**规则 2 — 表格格式：** 始终将表格输出放在 markdown 代码块中（使用三重反引号）。以包含三个反引号的行开头，然后是表格行，最后再以包含三个反引号的行结尾。这样表格才能以等宽字体显示，并且列对齐。API 返回的表格每行显示 40 个字符（适合移动设备显示）；请勿重新格式化或截断数据，直接传递原始输出。**例外情况：** 对于选项 11（Binance 公告），请不要将其放在代码块中，直接以原始 markdown 格式传递输出（包含 **📢 Binance 公告** 标题、🔸 圆点列表以及每个项目后的空行）。

**规则 3 — 响应以输出内容结束。** 在表格（或选项 11 的 Binance 列表）之后，您的响应就完成了。不要再添加任何内容。

---

## 该技能的功能

通过 `python "{baseDir}/api_client_cli.py"` 调用 ClipX BNBChain API 来获取 BNB Chain 的纯文本指标和排名信息。所有数据抓取工作由后端处理。

---

## 交互式菜单

当用户输入 “clipx”、“bnbchain”、“bnbchain analysis” 或请求 BNB Chain 报告但未指定具体类型时，请输出以下菜单：

将此菜单放在代码块中（使用三重反引号），以便以格式化的形式显示：

```
========================================
🟡 ClipX / BNBChain Analysis
========================================
 1. TVL Rank
 2. Fees Rank (24h/7d/30d)
 3. Revenue Rank (24h/7d/30d)
 4. DApps Rank
 5. Full Ecosystem
 6. Social Hype
 7. Meme Rank
 8. Network Metrics
 9. Market Insight
10. Market Insight (Live)
11. Binance Announcements
12. DEX Volume (24h/7d/30d)
========================================
Reply with a number (1–12)
```

---

## 命令（编号 → 命令）

| # | 命令 |
|---|---------|
| 1 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC` |
| 2 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC` |
| 3 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 24h --timezone UTC` |
| 4 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC` |
| 5 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC` |
| 6 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC` |
| 7 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC` |
| 8 | `python "{baseDir}/api_client_cli.py" --mode metrics_basic` |
| 9 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight --timezone UTC` |
| 10 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight_live --timezone UTC` |
| 11 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type binance_announcements --timezone UTC` |
| 12 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dex_volume --interval 24h --timezone UTC` |

对于命令 2（费用排名）、3（收入排名）和 12（DEX 交易量排名），默认间隔为 24 小时。如果用户指定 7 天或 30 天，则使用 `--interval 7d` 或 `--interval 30d`。

---

## 显示结果

客户端会打印预先格式化的表格。您的任务是：
1. 运行相应的命令。
2. 获取标准输出（即格式化的表格）。
3. **对于选项 1–10 和 12：** 将其放在 markdown 代码块中（前面和后面各使用三重反引号）。表格每行显示 40 个字符（适合移动设备显示）；请勿重新格式化、截断或调整列宽。
4. **对于选项 11（Binance 公告）：** 直接输出标准输出。不要将其放在代码块中，直接传递原始内容。
5. 完成响应。您的响应应完全符合上述格式要求。

---

## 网络指标（选项 8）

返回包含 `latest_block`、`gas_price_gwei` 和 `syncing` 的 JSON 数据。请用简洁的语言进行总结。

---

## 市场洞察（实时）——选项 10

使用 `market_insight_live` API 获取实时数据：成交量最高的交易对、涨幅最大的交易对和跌幅最大的交易对。（聊天界面中无需使用 `--live` 参数；OpenClaw 会显示静态信息。在本地运行时使用 `--live` 参数可实时更新数据。）

## Binance 公告——选项 11

使用 `binance_announcements` API 获取最新的 10 条公告。

**显示规则：** 运行命令后，直接输出标准输出。不要将其放在代码块中。API 返回的格式如下：
- 加粗标题：**📢 Binance 公告**
- 每条公告前带有 🔸 圆点标记
- 每条公告后跟随一个空行

请直接传递原始输出。响应应在最后一条公告后结束。

## DEX 交易量——选项 12

使用 `dex_volume` API 获取 BNB Chain 上交易量最高的 10 个 DEX。支持的时间间隔为 24 小时（默认）、7 天和 30 天。数据来自 DefiLlama。

---

## 其他模式

- `--mode metrics_block --blocks 100` — 获取最近区块的平均区块时间和Gas费用。
- `--mode metrics_address --address 0x...` — 获取指定地址的 BNB 余额和交易次数。

---

## 环境设置

API 的默认基础 URL 为 `https://skill.clipx.app`。可以通过 `CLIPX_API_BASE` 环境变量进行更改。