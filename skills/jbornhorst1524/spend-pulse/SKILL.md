---
name: spend-pulse
description: 通过 Plaid 实现主动式支出提醒功能：根据每月预算监控信用卡支出情况，并在超出预算时发送基于支出速度的提醒通知。
---

# Spend Pulse

> 通过 Plaid 提供主动的支出提醒功能。您可以跟踪信用卡支出情况，并根据每月预算设置基于支出速度的提醒。

## 安装

```bash
# Install globally
npm install -g spend-pulse

# Or from source
git clone https://github.com/jbornhorst1524/spend-pulse.git
cd spend-pulse
npm install && npm run build && npm link
```

验证安装结果：
```bash
spend-pulse --version
```

## 首次设置

运行交互式设置向导：

```bash
spend-pulse setup
```

设置过程包括：
1. 输入 Plaid API 密钥（请在 https://dashboard.plaid.com/developers/keys 获取）
2. 选择测试模式（Sandbox）或正式模式（Development）
3. 设置每月支出预算
4. 在浏览器中打开 Plaid 提供的链接以完成银行身份验证
5. 将 API 密钥安全地存储在 macOS 的 Keychain 中

**进行测试模式（Sandbox）设置时**，使用以下测试凭据：
- 用户名：`user_good`
- 密码：`pass_good`

设置完成后，运行初始同步操作：
```bash
spend-pulse sync
```

## 命令

### `spend-pulse check` — 主要命令

返回包含详细信息的提醒判断结果。**这是您需要使用的核心命令。**

```yaml
should_alert: true
reasons:
  - 3 new transactions
  - end of month approaching
month: "2026-01"
budget: 8000
spent: 6801.29
remaining: 1198.71
day_of_month: 30
days_in_month: 31
days_remaining: 1
expected_spend: 7200.00
pace: under
pace_delta: -398.71
pace_percent: -6
pace_source: last_month
oneline: "Jan: $6.8k of $8k (85%) | $1.2k left | 1 days | > On track"
new_transactions: 3
new_items:
  - merchant: Whole Foods
    amount: 47.50
    category: Groceries
  - merchant: Amazon
    amount: 125.00
    category: Shopping
```

**触发提醒的条件（`should_alert: true`）**：
- 自上次检查以来有新的交易发生
- 支出速度超过预期
- 剩余预算低于 $500
- 月底（距离月底还有 3 天）
- 月初（新月份开始）

### `spend-pulse sync`

从 Plaid 获取最新交易数据。在运行 `check` 命令前执行此命令以获取最新数据。

```yaml
synced: 16
new: 3
account: "Amex Gold (...1234)"
total_this_month: 6801.29
```

### `spend-pulse status [--oneline]`

显示完整的支出汇总信息，或以简短的一句话形式输出：

```bash
spend-pulse status --oneline
# Jan: $6.8k of $8k (85%) | $1.2k left | 1 days | > On track
```

### `spend-pulse recent [--days N] [--count N]`

显示最近的交易记录（默认显示过去 5 天的交易）。

### `spend-pulse config [key] [value]`

查看或修改设置：

```bash
spend-pulse config                  # show all
spend-pulse config target 8000      # set monthly budget
spend-pulse config timezone America/Chicago
```

### `spend-pulse link [--status] [--remove <id>]`

管理已关联的银行账户：

```bash
spend-pulse link --status    # show linked accounts
spend-pulse link             # add another account
spend-pulse link --remove <item_id>
```

### `spend-pulse chart [-o <path>]`

生成累计支出图表（PNG 格式）：
- 当前月份的支出情况（实线蓝色，带有渐变填充效果，今日用点标示）
- 上个月的支出情况（虚线灰色）
- 预算目标（虚线琥珀色）

```bash
spend-pulse chart                    # Writes to ~/.spend-pulse/chart.png
spend-pulse chart -o /tmp/chart.png  # Custom output path
```

该命令会将图表文件路径输出到标准输出（stdout），方便您将其附加到消息中。

### `spend-pulse check --chart`

在检查提醒结果的同时生成图表。此命令会在 YAML 输出中添加 `chart_path` 字段：

```yaml
should_alert: true
chart_path: /Users/you/.spend-pulse/chart.png
# ... rest of check output
```

## 推荐的工作流程

```bash
# 1. Sync latest transactions
spend-pulse sync

# 2. Check if alert needed, generate chart
spend-pulse check --chart
```

**如果 `should_alert: true`**：根据数据撰写简洁明了的支出更新信息，并附上 `chart_path` 中的图表。图表可以直观地显示当前月份与上个月的支出对比情况。

**如果 `should_alert: false`**：除非用户询问支出情况，否则无需发送提醒。

## 撰写消息

使用 `oneline` 字段作为消息的主体内容，然后补充相关细节。如果有图表，请务必附上图表——图表比文字更能直观地展示支出情况。

**支出进度低于预期（正面情况）**：
> “支出情况良好：1 月份支出为 $6,800，预算为 $8,000，还剩 1 天，进度低于预期 12%——做得不错！”
> [附上 chart.png]

**支出进度符合预期**：
> “1 月份支出情况：$5,500，预算为 $8,000（完成 69%），还剩 10 天。支出进度符合预期。最近的交易包括 $125 在 Amazon 和 $47 在 Whole Foods。”
> [附上 chart.png]

**支出进度超过预期（提醒）**：
> “注意：1 月份支出为 $7,200，预算为 $8,000，还剩 5 天，超出预算约 10%。可能是旅行费用导致的。”
> [附上 chart.png]

**支出超出预算**：
> “1 月份预算为 $8,500，实际支出为 $8,000，超出预算约 $500。需要注意这一点，以便在 2 月份进行调整。”
> [附上 chart.png]

**编写消息的指导原则**：
- 语气要友好、有帮助，避免显得像是在唠叨
- 尽量将消息长度控制在 280 个字符以内
- 如果有值得注意的支出项目，可以提及 1-2 项
- 使用 `reasons` 数组提供更多背景信息
- 一定要附上图表——图表在手机屏幕上也能清晰显示

## 支出进度解释

Spend Pulse 会参考**上个月的实际累计支出曲线**来评估支出进度；如果没有上个月的数据，则会使用线性预算增长模型进行判断。

- `expected_spend`：表示上个月同期的预期支出金额（或使用线性预算增长模型计算的结果）
- `spent`：实际支出金额
- `pace_delta`：支出差异（负数表示低于预期，正数表示超出预期）
- `pace`：`under`（低于预期）、`on_track`（符合预期）、`over`（超出预期）
- `pace_source`：`last_month`（基于上个月的曲线数据）或 `linear`（使用线性预算增长模型）

这意味着，如果上个月有类似的固定支出项目（如房租、订阅费用），这些支出不会被错误地标记为“超出预期”。

**示例**：假设上个月第 15 天的支出为 $4,200，那么本次的预期支出也是 $4,200。

## 升级到正式银行数据

完成测试模式（Sandbox）的设置后，可以切换到正式模式（Development）以使用真实的银行交易数据：

```bash
spend-pulse setup --upgrade
```

切换模式后会清除测试模式下的数据，并连接您的正式银行账户。

## 故障排除

- **“Plaid 密钥未找到”**：运行 `spend-pulse setup` 命令进行重新配置。
- **“访问令牌未找到”**：运行 `spend-pulse setup` 命令重新进行身份验证。
- **“未找到任何账户”**：运行 `spend-pulse link --status` 命令查看账户信息，并根据需要添加新账户。
- **数据过期**：运行 `spend-pulse sync` 命令从 Plaid 获取最新数据。