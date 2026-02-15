---
name: binance-dca
description: 专业级的Binance美元成本平均（DCA）工具，支持自动化和手动重复购买加密货币。该工具可帮助用户制定DCA策略（包括场景分析），执行市场价或限价买入操作，追踪购买历史，并管理任何交易对的系统化积累计划。它具备风险管理功能、测试网支持以及与OpenClaw自动化系统的集成能力。用户可通过该工具发起关于DCA、重复购买、成本平均、积累策略或Binance现货购买的请求。
---

# Binance DCA — 专业的美元成本平均投资工具

> **让系统化的加密货币积累变得简单。**  
> 在Binance上自信地规划、执行和跟踪您的DCA策略。

## 什么是DCA？

**美元成本平均（DCA）**是一种投资策略，您定期以固定的美元金额购买某种资产，而不考虑价格波动。这种策略：

- ✅ **降低时机选择风险** — 无需预测市场的高点/低点
- ✅ **平滑价格波动** — 随时间平均价格波动
- ✅ **排除情绪化决策** — 系统化购买，避免恐慌或错失机会（FOMO）
- ✅ **培养纪律性** — 持续积累，非常适合长期持有者

**此工具**可帮助您在Binance的现货市场上规划、自动化和跟踪您的DCA策略。

---

## 特点

- 📊 **DCA计划预测** — 分析不同价格水平下的潜在结果
- 💰 **市场订单与限价订单** — 灵活的执行选项
- 📈 **交易历史** — 跟踪您的积累进度
- 🔒 **安全性** — 仅通过环境变量存储凭证，无硬编码的秘密信息
- 🧪 **测试网支持** — 在上线前在Binance测试网上练习
- 🤖 **OpenClaw集成** — 通过定时任务（cron jobs）自动化DCA购买，并接收提醒
- 🛡️ **风险管理** — 保守的默认设置，执行前进行验证

---

## 设置

### 1. 获取Binance API密钥

1. 登录[binance.com](https://www.binance.com)
2. 转到**账户** → **API管理**
3. 创建一个新的API密钥：
   - **标签：** `OpenClaw-DCA`（或类似名称）
   - **限制：** 仅启用**现货交易与保证金交易**
   - **IP白名单：** 为安全起见，添加您的服务器IP（可选但推荐）
4. 安全保存您的**API密钥**和**秘密密钥**

⚠️ **安全提示：**
- 绝不要分享您的秘密密钥
- 如果您的服务器有静态IP，请启用IP白名单
- 为DCA使用单独的API密钥（需要时更容易撤销）
- 从少量资金开始测试

### 2. 设置环境变量

**切勿硬编码凭证。**始终使用环境变量：

```bash
export BINANCE_API_KEY="your-api-key-here"
export BINANCE_SECRET_KEY="your-secret-key-here"
```

**将其设置为永久性设置**（可选，添加到`~/.bashrc`或`~/.zshrc`）：

```bash
echo 'export BINANCE_API_KEY="your-api-key-here"' >> ~/.bashrc
echo 'export BINANCE_SECRET_KEY="your-secret-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**针对测试网**（推荐给首次用户）：

```bash
export BINANCE_BASE_URL="https://testnet.binance.vision"
```

在[testnet.binance.vision](https://testnet.binance.vision/)获取测试网API密钥。

### 3. 验证设置

```bash
# Check balance (should not error)
bash scripts/dca.sh balance USDT

# Check BTC price
bash scripts/dca.sh price BTCUSDT
```

如果您能看到价格/余额，那么设置就完成了！

---

## 快速入门示例

### 示例1：检查当前价格

```bash
bash scripts/dca.sh price BTCUSDT
# Output: BTCUSDT = 95234.50
```

适用于任何交易对：
```bash
bash scripts/dca.sh price ETHUSDT
bash scripts/dca.sh price SOLUSDT
```

### 示例2：检查您的余额

```bash
bash scripts/dca.sh balance USDT
# Output: USDT: free=1000.00000000, locked=0.00000000
```

检查任何资产：
```bash
bash scripts/dca.sh balance BTC
bash scripts/dca.sh balance ETH
```

### 示例3：规划DCA策略

**场景：**您想在3个月内投资600美元购买BTC。

```bash
# $50 every week for 12 weeks
bash scripts/dca.sh plan 50 7 12 BTCUSDT
```

**输出：**
```
DCA Plan: BTCUSDT
==========================
Buy amount:  $50 per buy
Frequency:   every 7 days
Duration:    12 buys
Current:     95234.50
==========================
Total invest:  $600.00
At cur. price: 0.00630245 BTC
Time span:     84 days (~2.8 months)

Scenario Analysis (if avg price over period is):
  -30% -> avg $ 66,664.15 -> 0.00900000 BTC -> PnL: -$186.00 (-31.0%)
  -20% -> avg $ 76,187.60 -> 0.00787500 BTC -> PnL: -$126.00 (-21.0%)
  -10% -> avg $ 85,711.05 -> 0.00700000 BTC -> PnL: -$63.00 (-10.5%)
   +0% -> avg $ 95,234.50 -> 0.00630245 BTC -> PnL: +$0.00 (+0.0%)
  +10% -> avg $104,757.95 -> 0.00572727 BTC -> PnL: +$63.00 (+10.5%)
  +20% -> avg $114,281.40 -> 0.00525000 BTC -> PnL: +$126.00 (+21.0%)
  +50% -> avg $142,851.75 -> 0.00420000 BTC -> PnL: +$378.00 (+63.0%)
 +100% -> avg $190,469.00 -> 0.00315122 BTC -> PnL: +$630.00 (+105.0%)
```

**这告诉您：**
- 如果BTC价格保持不变 → 可实现盈亏平衡
- 如果在购买期间BTC价格平均下跌20% → 您的亏损约为21%（但您持有的BTC更多）
- 如果BTC价格平均上涨50% → 您的收益约为63%

在决定投资前，请使用此信息来**设定合理的预期**。

### 示例4：执行您的第一次DCA购买

**市场订单（即时执行）：**

```bash
# Buy $50 worth of BTC at current market price
bash scripts/dca.sh buy BTCUSDT 50
```

**输出：**
```
Placing MARKET buy: BTCUSDT for 50 USDT...
Order #123456789: FILLED
Filled: 0.00052500 BTC
```

**限价订单（等待价格达到目标）：**

```bash
# Only buy if BTC drops to $94,000
bash scripts/dca.sh buy BTCUSDT 50 LIMIT 94000
```

**输出：**
```
Placing LIMIT buy: BTCUSDT for 50 USDT...
Order #123456790: NEW
Filled: 0.00000000 BTC
```

（订单将在价格达到94,000美元时执行）

### 示例5：检查您的交易历史

```bash
# Last 10 trades for BTCUSDT
bash scripts/dca.sh history BTCUSDT 10
```

**输出：**
```
Last 10 trades for BTCUSDT:
---
1738752000 | BUY | qty=0.00052500 | price=95238.10 | fee=0.00000053 BNB
1738665600 | BUY | qty=0.00051234 | price=97567.20 | fee=0.00000051 BNB
...
```

---

## 完整操作参考

### `price [SYMBOL]`

**获取交易对的当前现货价格。**

```bash
bash scripts/dca.sh price BTCUSDT
bash scripts/dca.sh price ETHUSDT
bash scripts/dca.sh price SOLUSDT
```

**默认值：** 如果省略了交易对，则使用`BTCUSDT`。

---

### `balance [ASSET]`

**检查资产的可用余额和锁定余额。**

```bash
bash scripts/dca.sh balance USDT
bash scripts/dca.sh balance BTC
bash scripts/dca.sh balance ETH
```

**输出格式：** `ASSET: free=X.XXXXXXXX, locked=Y.YYYYYYYY`

**默认值：** 如果省略了资产，则使用`USDT`。

**用途：** 在下订单前检查您可用的资金。

---

### `buy SYMBOL AMOUNT [TYPE] [PRICE]`

**下达购买订单。**

**参数：**
- `SYMBOL` — 交易对（例如，`BTCUSDT`，`ETHUSDT`）
- `AMOUNT` — 以**报价货币**（USDT）表示的金额。该工具会计算您可以购买的BTC/ETH数量。
- `TYPE` — `MARKET`（默认）或`LIMIT`
- `PRICE` — 限价订单必需的参数

**市场订单示例：**

```bash
# Buy $50 worth of BTC instantly
bash scripts/dca.sh buy BTCUSDT 50

# Buy $100 worth of ETH instantly
bash scripts/dca.sh buy ETHUSDT 100
```

**限价订单示例：**

```bash
# Buy $50 BTC only if price drops to $90,000
bash scripts/dca.sh buy BTCUSDT 50 LIMIT 90000

# Buy $200 ETH only if price hits $3,200
bash scripts/dca.sh buy ETHUSDT 200 LIMIT 3200
```

**安全特性：**
- 金额验证（必须是数字）
- 执行前检查API密钥
- 输出中包含订单状态确认

---

### `history [SYMBOL] [LIMIT]`

**显示最近的交易历史。**

```bash
# Last 10 trades for BTCUSDT
bash scripts/dca.sh history BTCUSDT 10

# Last 20 trades for ETHUSDT
bash scripts/dca.sh history ETHUSDT 20

# Last 50 trades for SOLUSDT
bash scripts/dca.sh history SOLUSDT 50
```

**默认值：** `BTCUSDT`，限制数量为`10`

**输出包括：**
- 时间戳（Unix秒）
- 交易方向（买入/卖出）
- 购买数量
- 执行价格
- 支付的费用（以及费用对应的资产）

**用途：** 随时间跟踪您的DCA进度，计算平均买入价格。

---

### `plan [AMOUNT] [FREQ_days] [NUM_BUYS] [SYMBOL]`

**规划DCA计划并进行分析。**

**参数：**
- `AMOUNT` — 每次购买的美元金额（默认：50美元）
- `FREQ_days` — 两次购买之间的间隔天数（默认：7天）
- `NUM_BUYS` — 购买次数（默认：12次）
- `SYMBOL` — 交易对（默认：`BTCUSDT`）

**示例：**

```bash
# Default plan: $50 every 7 days, 12 buys
bash scripts/dca.sh plan

# Aggressive: $200 every 3 days, 30 buys
bash scripts/dca.sh plan 200 3 30 BTCUSDT

# Conservative: $25 every 14 days, 24 buys
bash scripts/dca.sh plan 25 14 24 BTCUSDT

# ETH DCA: $100 weekly for 6 months
bash scripts/dca.sh plan 100 7 26 ETHUSDT
```

**您将获得：**
- 总投资金额
- 在当前价格下您将持有的BTC/ETH数量
- 时间跨度（天数+月数）
- **情景分析：** 在价格平均下跌30%、20%、10%、0%、上涨10%、20%、50%、100%时的盈亏情况

**用途：**
- 确定合适的预算和频率
- 在开始前了解风险与回报
- 通过数据展示DCA与一次性投资的优劣

---

## DCA策略指南

### 何时使用DCA

✅ **适用于：**
- 长期积累（6个月以上）
- 高波动性资产（如BTC、ETH、山寨币）
- 无需担心时机选择即可建立投资组合
- 排除情绪化决策的影响

❌ **不适用于：**
- 短期交易（建议使用手动购买）
- 需要快速买卖的资产
- 低波动性的稳定币（只需购买一次）

### 最佳实践

1. **从小额开始** — 先用预算的1-2%进行测试
2. **使用测试网** — 在上线前在`https://testnet.binance.vision`上练习
3. **设定时间表** — DCA在3-12个月以上的时间段内效果最佳
4. **坚持计划** — 在价格下跌时抵制停止购买的冲动（这正是DCA的优势所在）
5. **跟踪进度** — 使用`history`功能查看平均买入价格
6. **根据需要调整** — 生活情况或预算变化时，重新计算并调整计划

### 仓位大小建议

**保守型（每次购买1-2%）：**
- 投资组合：10,000美元 → 每次购买100-200美元
- 低风险，积累速度较慢

**中等型（每次购买3-5%）：**
- 投资组合：10,000美元 → 每次购买300-500美元
- 平衡的投资方式，适合大多数用户

**激进型（每次购买5-10%）：**
- 投资组合：10,000美元 → 每次购买500-1,000美元
- 风险较高，积累速度较快，需要坚定的决心

**每次购买金额切勿超过10%** — 以应对意外价格下跌或额外支出。

### 频率指南

- **每日** — 适用于非常活跃的交易者，需要大量时间投入
- **每3天一次** — 适合短期DCA策略（1-3个月）
- **每周一次** — 最受欢迎的方式，适合大多数用户
- **每两周一次** — 与发薪日相匹配，节奏适中
- **每月一次** — 适合长期持有者，最省力的方式

**专业提示：** 根据您的收入安排调整DCA的频率（例如，每周发薪日对应每周一次DCA）。

---

## 使用OpenClaw进行自动化

### 手动Cron（基础版本）

通过系统定时任务自动执行DCA购买：

```bash
# Every Monday at 9:00 AM UTC, buy $50 BTC
0 9 * * 1 BINANCE_API_KEY=... BINANCE_SECRET_KEY=... /path/to/dca.sh buy BTCUSDT 50
```

**限制：**
- 失败时没有提醒
- 没有执行确认
- 执行过程无声

### 使用OpenClaw Cron（推荐版本）

使用OpenClaw实现智能化的DCA自动化，并接收提醒：

**示例：每周自动购买BTC，并通过Telegram接收通知**

```json
{
  "name": "Weekly BTC DCA",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "America/New_York"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Execute weekly DCA: buy $50 BTCUSDT via binance-dca skill. After execution, send me a summary: amount bought, price, total BTC accumulated so far (check history). If it fails, alert me immediately.",
    "deliver": true,
    "channel": "telegram"
  }
}
```

**优势：**
- ✅ 会向您发送执行确认
- ✅ 提供失败提醒
- ✅ 可请求代理分析历史数据并报告进度
- ✅ 可通过`openclaw cron`命令轻松暂停/恢复

**设置：**

```bash
# Add the cron job (paste JSON above when prompted)
openclaw cron add

# List all jobs
openclaw cron list

# Run manually to test
openclaw cron run <jobId>

# Disable temporarily
openclaw cron update <jobId> --enabled false
```

---

## 故障排除

### 错误：`BINANCE_API_KEY未设置**

**解决方法：** 在运行前设置环境变量：

```bash
export BINANCE_API_KEY="your-key"
export BINANCE_SECRET_KEY="your-secret"
bash scripts/dca.sh price
```

---

### 错误：`此请求的时间戳超出了recvWindow**

**原因：** 您的系统时钟与Binance服务器不同步。

**解决方法（Linux/macOS）：**

```bash
# Sync system time
sudo ntpdate -s time.nist.gov

# Or install/enable NTP
sudo systemctl enable systemd-timesyncd
sudo systemctl start systemd-timesyncd
```

**解决方法（Docker）：**

在运行容器时添加`--cap-add SYS_TIME`参数，或同步主机时钟。

---

### 错误：`此请求的签名无效**

**原因：**
- `BINANCE_SECRET_KEY`错误
- API密钥限制（IP白名单不匹配，或禁用了现货交易）

**解决方法：**
1. 重新检查您的秘密密钥（从Binance复制粘贴）
2. 确认API密钥已启用**现货交易与保证金交易**
3. 如果使用了IP白名单，请确认您的服务器IP是否被允许
4. 如果不确定，请重新生成API密钥

---

### 错误：`API请求失败**

**原因：**
- 网络问题
- `BINANCE_BASE_URL`错误
- Binance API维护中

**解决方法：**
1. 测试网络连接：`curl -I https://api.binance.com`
2. 查看Binance的状态：[binance.com/en/support/announcement](https://www.binance.com/en/support/announcement)
3. 如果使用测试网，请确认：`export BINANCE_BASE_URL="https://testnet.binance.vision"`

---

### 错误：**账户余额不足**

**原因：** 您的现货账户中的USDT不足

**解决方法：**
1. 检查余额：`bash scripts/dca.sh balance USDT`
2. 向您的现货账户充值USDT
3. 减少DCA的购买金额，使其与可用余额相匹配

---

### 订单显示`NEW`状态（限价订单未成交）

**对于限价订单来说这是正常的。** 状态含义如下：
- `NEW` — 订单已下达，等待价格满足条件
- `FILLED` — 订单已执行
- `PARTIALLY_FILLED` — 部分执行
- `CANCELED` — 您或系统取消了订单

**检查订单状态：**

```bash
# View recent orders to see if it filled later
bash scripts/dca.sh history BTCUSDT 20
```

**取消待处理的限价订单：**

通过Binance网站/应用程序 → **订单** → **未成交订单** → **取消订单**。

---

## 常见问题解答

### Q：我可以将资金用于其他加密货币（不仅仅是BTC）吗？

**A：** 可以！使用任何Binance的现货交易对：

```bash
bash scripts/dca.sh buy ETHUSDT 100
bash scripts/dca.sh buy SOLUSDT 50
bash scripts/dca.sh buy ADAUSDT 25
```

只需将`BTCUSDT`替换为您所需的交易对即可。

---

### Q：最低购买金额是多少？

**A：** Binance为每个交易对设置了最低金额限制（通常为10-20美元）。请查看Binance的文档，或在测试网上先用少量资金测试。

---

### Q：这个工具适用于Binance.US吗？

**A：** 不直接适用。Binance.US有独立的API（`https://api.binance.us`）。您需要更改`BINANCE_BASE_URL`并进行测试。该工具不支持Binance.US。

---

### Q：我可以使用这个工具进行卖出操作吗？

**A：** 目前不行。这个工具仅用于积累投资（DCA）。如需卖出，请使用Binance的网站/应用程序，或修改脚本（将`side`参数从`BUY`改为`SELL`）。

---

### Q：我的数据会被存储在哪里吗？

**A：** 不会存储任何数据。所有凭证都存储在环境变量中。脚本直接通过API调用Binance并立即退出。

---

### Q：我可以在多台机器上使用这个工具吗？

**A：** 可以，但需要在每台机器上分别设置API密钥。为安全起见，建议为每个机器设置IP白名单。

---

### Q：如果我在策略执行过程中想更改DCA的购买金额怎么办？

**A：** 只需在下次手动或定时执行时调整金额即可。DCA具有灵活性——无需固定购买金额。

**示例：** 第1-4周购买50美元，第5周及以后购买100美元。

---

### 如何计算我的平均买入价格？

运行`history`命令，然后对`price`列进行平均计算：

```bash
bash scripts/dca.sh history BTCUSDT 50 | grep BUY | awk '{print $8}' | awk '{s+=$1; n++} END {print s/n}'
```

或者使用电子表格：导出历史数据，粘贴价格后使用`=AVERAGE()`函数计算平均值。

---

## 安全最佳实践

🔒 **API密钥安全：**
- 为DCA专门设置API密钥（标签为`DCA-Only`）
- 仅启用**现货交易**（不支持期货、保证金交易或提款）
- 如果服务器有静态IP，请设置IP白名单
- 每3-6个月更换一次密钥
- 如果密钥被盗用，立即撤销

🔒 **凭证管理：**
- **切勿将`.env`文件中的密钥提交到Git**
- 使用环境变量，避免硬编码
- 在共享服务器上，限制文件权限：`chmod 600 ~/.bashrc`

🔒 **先在测试网上测试：**
- 在使用真实资金之前，始终在测试网上测试新策略
- 使用测试网密钥：[testnet.binance.vision](https://testnet.binance.vision/)
- 设置：`export BINANCE_BASE_URL="https://testnet.binance.vision"`

🔒 **从小额开始：**
- 首次实际使用DCA时，使用计划金额的10-20%
- 验证执行结果、费用和确认信息
- 确认无误后再逐步增加规模

---

## 高级用法

### 动态DCA（根据市场条件调整）

根据价格调整购买金额：

**在BTC价格下跌时增加购买量：**

```bash
# If BTC < $90k, buy $100. Otherwise $50.
CURRENT=$(bash scripts/dca.sh price BTCUSDT | awk '{print $3}')
if (( $(echo "$CURRENT < 90000" | bc -l) )); then
  bash scripts/dca.sh buy BTCUSDT 100
else
  bash scripts/dca.sh buy BTCUSDT 50
fi
```

**使用限价订单“逢低买入”：**

```bash
# Place limit orders 5%, 10%, 15% below current price
PRICE=$(bash scripts/dca.sh price BTCUSDT | awk '{print $3}')
LIMIT_5=$(echo "$PRICE * 0.95" | bc)
LIMIT_10=$(echo "$PRICE * 0.90" | bc)
LIMIT_15=$(echo "$PRICE * 0.85" | bc)

bash scripts/dca.sh buy BTCUSDT 50 LIMIT $LIMIT_5
bash scripts/dca.sh buy BTCUSDT 50 LIMIT $LIMIT_10
bash scripts/dca.sh buy BTCUSDT 50 LIMIT $LIMIT_15
```

### 多资产DCA**

同时对多种货币进行DCA投资：

```bash
# Weekly: $30 BTC, $20 ETH, $10 SOL
bash scripts/dca.sh buy BTCUSDT 30
bash scripts/dca.sh buy ETHUSDT 20
bash scripts/dca.sh buy SOLUSDT 10
```

### 日志记录与分析

将所有DCA购买记录到日志文件中：

```bash
#!/bin/bash
LOGFILE="$HOME/dca-log.txt"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

bash scripts/dca.sh buy BTCUSDT 50 | tee -a "$LOGFILE"
echo "[$DATE] DCA executed" >> "$LOGFILE"
```

然后使用以下工具进行分析：

```bash
grep "Filled:" ~/dca-log.txt
```

---

## 贡献

发现漏洞？有功能建议？希望为其他交易所添加支持？

- **GitHub：** （如果存在公共仓库，请在此处提供链接）
- **问题报告：** 通过GitHub Issues提交
- **拉取请求：** 欢迎提交！请遵循现有的代码风格。

---

## 许可证

MIT许可证 — 可自由使用、修改和分发。

**免责声明：** 本工具按“原样”提供。使用过程中产生的任何风险均由用户自行承担。作者不对交易损失、API问题或错误使用负责。请务必先在测试网上测试，并确保投资金额在您可承受的范围内。

---

## 更新日志

### v1.2.0（2026-02-05）
- 📚 全面更新文档
- 📋 为所有操作添加了实际使用示例
- 🎓 提供DCA策略指南及最佳实践
- 🔧 添加故障排除部分
- ❓ 提供常见问题的FAQ
- 🔒 安全最佳实践指南
- 🚀 高级使用示例
- 🤖 OpenClaw自动化使用指南

### v1.1.0（2026-02-05）
- 首次公开发布
- 核心DCA功能：规划、购买、查看历史记录、价格、余额
- 支持测试网和限价订单

---

**我们致力于帮助您长期积累加密货币。**

有任何问题或反馈吗？请在ClawHub或OpenClaw的Discord频道中@fpsjago。