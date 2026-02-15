---
name: kalshi-agent
description: Kalshi预测市场代理——通过Kalshi v2 API分析市场并执行交易
metadata:
  clawdbot:
    emoji: "🎰"
    homepage: https://docs.kalshi.com/api-reference/
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3", "pip"]
      env: ["KALSHI_ACCESS_KEY"]
      files: ["~/.kalshi/private_key.pem"]
    py_package: "cryptography>=41.0.0"
---

# Kalshi Agent Skill

这是一个用于在 [Kalshi](https://kalshi.com) 交易预测市场的 CLI（命令行工具）。

## 安装

```bash
npm install -g kalshi-cli
```

## 配置

1. 在 [https://kalshi.com/api] 获取 API 凭据。
2. 将您的 RSA 私钥保存到 `~/.kalshi/private_key.pem` 文件中。
3. 在 `~/.kalshi/.env` 文件中设置您的访问密钥：

```
KALSHI_ACCESS_KEY=your_access_key_id
```

或者运行 `kalshi setup-shell` 命令将其添加到您的 shell 配置中。

---

## 命令

### 浏览与研究

```bash
# List open markets (default 20)
kalshi markets
kalshi markets -l 50
kalshi markets --status settled

# Search by keyword, ticker, or category
kalshi search "Super Bowl"
kalshi search soccer
kalshi search hockey
kalshi search KXWO-GOLD-26

# Search with filters
kalshi search politics --min-odds 5     # hide markets where either side < 5%
kalshi search soccer --expiring          # sort by soonest expiry, show expiry column
kalshi search soccer -e -m 2 -l 20      # combine flags: expiring, 2% min-odds, 20 results

# Browse all active series (interactive — pick a number to drill down)
kalshi series
kalshi series soccer
kalshi series --all                      # include series with no active markets
kalshi series -e                         # sort by soonest expiry

# View single market detail
kalshi detail KXWO-GOLD-26-NOR

# View orderbook depth
kalshi orderbook KXWO-GOLD-26-NOR
```

### 搜索行为

Kalshi 的搜索采用多策略方式：

1. **直接查找股票代码** — 将查询内容视为市场代码、事件代码（以 `KX` 为前缀）或系列代码进行查找。
2. **系列匹配** — 根据标题、类别和标签动态搜索所有 Kalshi 系列（例如，“soccer” 会匹配标记为 “Soccer” 的系列）：
   - 如果匹配到多个系列，会显示一个 **交互式的编号列表** — 输入一个数字即可进入该系列的市场详情。
   - 如果匹配到的系列较少，会直接获取并显示这些系列的市场信息。
3. **市场标题搜索** — 作为备用方式，会搜索开放市场的标题/代码。

常见的体育/类别别名会自动被识别（例如，“nfl” 也会被识别为 “football”）。

### 交互式系列列表

`kalshi search` 和 `kalshi series` 命令在列出系列时都会显示编号列表。列表结束后，系统会提示您：

```
Enter # to drill down (or q to quit):
```

选择一个数字即可加载该系列的所有开放市场信息。该提示会循环出现，因此您可以无需重复执行命令即可查看多个系列的信息。

### 投资组合

```bash
# Check balance
kalshi balance

# View positions
kalshi positions

# View open orders
kalshi orders
```

### 交易

```bash
# Buy 10 YES contracts at 68c each
kalshi buy KXSB-26 10 68

# Buy NO contracts
kalshi buy KXWO-GOLD-26-NOR 5 32 --side no

# Sell (same syntax)
kalshi sell KXWO-GOLD-26-NOR 5 40 --side no

# Skip confirmation prompt
kalshi buy KXSB-26 10 68 --force

# Cancel an open order
kalshi cancel <order-id>
```

### 注意事项

- 价格以 **美分** 为单位（68 表示 $0.68，即 68% 的隐含概率）。
- 价格会同时以美元和百分比的形式显示（例如：`$0.68 (68%)`）。
- 如果未指定，默认 `--side` 的值为 `yes`。
- `buy` 和 `sell` 命令会显示成本/收益摘要，并要求用户确认操作（使用 `--force` 可跳过此步骤）。
- `--min-odds` / `-m` 选项会过滤掉任一方的出价低于指定百分比（默认为 0.5%）的市场。
- `--expiring` / `-e` 选项会按到期时间对结果进行排序，并添加一个 “Expires” 列；同时会排除已到期的条目。
- 到期时间以人类可读的形式显示（例如：`8h 35m`、`Fri 04:00PM`、`Apr 01`、`Jan 01, 2027`）。
- 事件代码以 `KX` 开头（例如：`KXWO-GOLD-26`）；市场代码包含更多信息（例如：`KXWO-GOLD-26-NOR`）。
- 如果可用，市场列表会显示结果的名称（例如：“Norway” 而不是原始代码）。

---

## API 参考

完整的 API 文档：https://docs.kalshi.com/api-reference/