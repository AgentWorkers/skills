---
name: clipx-bnbchain-api-client
description: 这是一个用于私有ClipX BNBChain API的轻量级客户端，它仅返回基于文本的JSON格式的指标和排名数据（涉及BNB Chain）。该客户端不使用任何爬虫技术，也不需要API密钥。
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---
## 响应规则（请先阅读）

**规则 1 — 菜单格式：** 始终使用编号行（1. 2. 3. …）。请参阅“交互式菜单”部分。

**规则 2 — 表格格式：** 始终将表格输出放在 markdown 代码块中（使用三个反引号）。以包含三个反引号的行开始，然后是表格行，最后再以包含三个反引号的行结束。这样表格会以等宽字体显示，并且列会居中对齐。API 返回的表格每行显示 40 个字符（适合移动设备显示）；请不要重新格式化或截断数据，直接传递原始输出。**例外：** 对于选项 11（Binance 公告），不要将其放在代码块中，直接以原始 markdown 格式传递（包含 **📢 Binance 公告** 标题、🔸 圆点列表以及每个项目后的空行）。

**规则 3 — 响应以输出内容结束。** 在表格（或选项 11 的 Binance 列表）之后，您的消息就完成了。不要再添加任何内容。

---

## 该技能的功能

通过 `python "{baseDir}/api_client_cli.py"` 调用 ClipX BNBChain API 来获取仅包含文本的 BNB Chain 指标和排名信息。所有数据抓取工作由后端处理。

---

## 交互式菜单

当用户输入 “clipx”、“bnbchain”、“bnbchain analysis” 或请求 BNB Chain 报告但没有指定具体类型时，请输出以下菜单：

🟡 ClipX / BNBChain 分析 — 选择一项：

1. TVL 排名 — 按锁定总价值排序的前 10 个协议
2. 费用排名 — 按 24 小时/7 天/30 天内支付的费用排序的前 10 个协议
3. 收入排名 — 按收入排序的前 10 个协议（24 小时/7 天/30 天）
4. DApp 排名 — 按用户数量排序的前 10 个 DApp（7 天）
5. 完整生态系统 — DeFi、游戏、社交、NFT、AI、基础设施领域的领导者
6. 社交热度 — 按社交热度排序的前 10 个代币
7. 模因排名 — 按得分排序的前 10 个模因代币
8. 网络指标 — 最新区块、Gas 价格、同步状态
9. 市场洞察 — Binance 24 小时交易量最高的货币对（以 USDT 计）
10. 市场洞察（实时） — 交易量最高的货币对 + 最大涨幅和最大跌幅的货币对（快照）
11. Binance 公告 — Binance 最新的 10 条公告
12. DEX 交易量 — 按 BNB Chain 上的交易量排序的前 10 个 DEX（24 小时/7 天/30 天）

请回复一个数字（1–12）。

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
| 12   | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dex_volume --interval 24h --timezone UTC` |

对于命令 2（费用排名）、3（收入排名）和 12（DEX 交易量），默认间隔为 24 小时。如果用户指定 7 天或 30 天，请使用 `--interval 7d` 或 `--interval 30d`。

---

## 显示结果

客户端会打印预先格式化的表格。您的任务是：

1. 运行相应的命令。
2. 获取标准输出（即格式化的表格）。
3. **对于选项 1–10、12：** 将其放在 markdown 代码块中（前面和后面各用三个反引号括起来）。表格每行显示 40 个字符（适合移动设备显示）；请直接传递原始数据，不要重新格式化或截断。
4. **对于选项 11（Binance 公告）：** 直接输出标准输出。不要将其放在代码块中。
5. 完成响应。

您的响应必须完全符合以下格式（API 使用每行 40 个字符的格式，适合移动设备显示）：

```
========================================
🚀 TOP 10 MEME TOKENS BY SCORE
========================================
----------------------------------------
#   | NAME         | —       | SCORE
----------------------------------------
1   | TokenA       | —       | 4.76
2   | TokenB       | —       | 4.61
...
========================================
Source: @ClipX0_
```

请直接传递原始的 40 个字符的输出，不要进行任何格式化。

---

## 网络指标（选项 8）

返回包含 `latest_block`、`gas_price_gwei`、`syncing` 的 JSON 数据。请用简单的语言进行总结。

---

## 市场洞察（实时）——选项 10

使用 `market_insight_live` API 获取实时数据：交易量最高的货币对以及涨幅和跌幅最大的货币对。（聊天中不需要使用 `--live` 参数；OpenClaw 会显示静态信息。在本地使用 `--live` 参数可实时更新数据。）

## Binance 公告——选项 11

使用 `binance_announcements` API 获取 Binance 的最新 10 条公告。

**显示规则：** 运行命令，获取标准输出，然后原样输出。不要将其放在代码块中。API 返回的格式如下：
- 加粗标题：**📢 Binance 公告**
- 每条公告前有一个 🔸 圆点符号
- 每条公告后有一个空行

请直接传递原始输出。响应应在最后一条公告后结束。

## DEX 交易量——选项 12

使用 `dex_volume` API 获取 BNB Chain 上交易量最高的 10 个 DEX。支持的时间间隔为：24 小时（默认）、7 天、30 天。数据来自 DefiLlama。

---

## 其他模式

- `--mode metrics_block --blocks 100` — 显示最近区块的平均区块时间和 Gas 使用量。
- `--mode metrics_address --address 0x...` — 显示指定地址的 BNB 余额和交易次数。

---

## 环境设置

API 的基础 URL 默认为 `https://skill.clipx.app`。可以通过 `CLIPX_API_BASE` 环境变量进行更改。