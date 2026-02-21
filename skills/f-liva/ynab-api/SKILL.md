---
name: ynab-api
description: YNAB（You Need A Budget）是一款全面的预算管理工具，具备自动化跟踪、目标监控、支出分析以及每日预算检查报告功能。同时，还提供了即用型脚本供用户使用。
user-invocable: true
metadata: {"clawdbot":{"emoji":"💰","requires":{"env":["YNAB_API_KEY","YNAB_BUDGET_ID"]}}}
---
# YNAB预算管理

这是一个完整的YNAB预算自动化工具包，包含最佳实践、自动监控以及即用型辅助脚本。

## ✨ 主要功能

- 📊 **目标进度跟踪** - 通过可视化进度条监控各类别的完成情况
- 📅 **定时交易提醒** - 确保不会错过即将到期的账单
- 💰 **资金流动监控** - 关注财务稳定性
- 📈 **月度对比分析** - 比较每月的支出趋势
- ⚠️ **超支提醒** - 超出预算时立即收到通知
- 🔄 **每日自动检查** - 通过WhatsApp/Telegram发送早晨预算汇总
- 🎯 **智能分类** - 从交易历史中学习
- 💸 **实时转账支持** - 正确链接账户转账

## 🚀 快速入门

本技能提供了通过API管理YNAB预算的最佳实践，包括交易分类、数据一致性和自动化工作流程。

## 📋 安装与配置

### 1. 获取您的YNAB API密钥

1. 访问 https://app.ynab.com/settings/developer
2. 点击“New Token”并复制您的个人访问令牌
3. 从YNAB URL中获取您的预算ID（例如：`https://app.ynab.com/abc123...` → `abc123...`）

### 2. 配置技能

在 `~/.config/ynab/config.json` 文件中创建配置文件：

```json
{
  "api_key": "YOUR_YNAB_TOKEN_HERE",
  "budget_id": "YOUR_BUDGET_ID_HERE"
}
```

或者设置环境变量：
```bash
export YNAB_API_KEY="your_token"
export YNAB_BUDGET_ID="your_budget_id"
```

### 3. 设置自动报告（推荐）

**🚀 一键设置：**

```bash
/home/node/clawd/skills/ynab-api/scripts/setup-automation.sh
```

此交互式脚本会创建所有推荐的cron作业：
- ✅ **每日预算检查**（早上7:15） - 资金流动情况、即将到期的账单、提醒
- ✅ **每周支出回顾**（周一早上8:00） - 月度对比
- ✅ **月中目标检查**（15日，早上9:00） - 各类别目标进度
- ✅ **即将到期的账单提醒**（每天上午10:00） - 下两天的交易

**先预览更改：**
```bash
/home/node/clawd/skills/ynab-api/scripts/setup-automation.sh --dry-run
```

**手动设置（备用方案）：**

如果您更喜欢手动创建cron作业：

```bash
openclaw cron add --name "Daily Budget Check" \
  --schedule "15 7 * * *" \
  --session isolated \
  --model gemini-flash \
  --delivery announce \
  --task "Run YNAB daily budget check and send via WhatsApp"
```

### 4. 测试您的设置

运行快速测试：
```bash
/home/node/clawd/skills/ynab-api/scripts/goals-progress.sh
```

如果看到预算目标显示出来，那么您就设置完成了！🎉

## 核心最佳实践

### 1. 立即分类交易

**切勿** 不给交易分类就直接添加。未分类的交易会破坏预算跟踪。

添加交易时，请立即为其分类——不要推迟。

### 2. 检查未知商家的交易历史

遇到不熟悉的商家/收款人时：

1. 在YNAB中搜索相同收款人的过往交易
2. 使用与之前的交易相同的分类
3. 保持历史分类的一致性

**原因**：这有助于保持分类的一致性，并减少用户的干扰。

示例：
```bash
# Search for past transactions by payee
curl -s "https://api.ynab.com/v1/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.transactions[] | select(.payee_name | contains("MERCHANT_NAME"))'
```

### 3. 添加新交易前检查待处理交易

在创建新交易之前：
1. 检查是否存在相同金额的未批准交易
2. 如果存在 → 批准交易并根据需要更新收款人/备注
3. 如果不存在 → 创建新交易

**原因**：避免从银行导入的交易重复。

### 4. 金额使用毫单位

YNAB API使用**毫单位**来表示所有金额：
- €10.00 = `10000`（收入为正数）
- -€10.00 = `-10000`（支出为负数）

**显示时**始终除以1000，**提交时**乘以1000。

### 5. 月度支出计算

计算月度支出时：
- 仅计算 `amount < 0` 的交易（实际支出）
- 考虑排除以下非可自由支配的类别：
  - 税费支付（强制性的，不属于支出）
  - 预付款/报销（临时的，不属于实际支出）
  - 未分类的交易（通常是转账/投资）
  - 一次性特殊支出（如果跟踪的是可自由支配的预算）

**注意**：排除规则取决于您的预算目标。在本地配置文件或备注中配置您的特定排除项。

### 6. 处理拆分交易

类别为“Split”的交易包含**子交易**。

**切勿** 在报告中将“Split”显示为单独的类别——始终将其展开为子类别：

```bash
# For each split transaction
if [ "$category_name" = "Split" ]; then
  for subtx in subtransactions; do
    echo "$subtx.category_name: $subtx.amount"
  done
fi
```

### 7. 转账交易（关键）

**⚠️ 重要**：要创建YNAB能够识别的**真实**转账（即账户间的关联交易），必须使用账户的 `transfer_payee_id`，而不是收款人名称。

#### 转账的工作原理

每个账户都有一个特殊的字段 `transfer_payee_id`——这是代表转账至该账户的收款人ID。

**✅ 正确做法 - 真实转账**：
```bash
# Transfer from Account A to Account B
# Get Account B's transfer_payee_id first, then:
curl -X POST "$YNAB_API/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"transaction\": {
      \"account_id\": \"ACCOUNT_A_ID\",
      \"date\": \"2026-02-21\",
      \"amount\": -50000,
      \"payee_id\": \"ACCOUNT_B_TRANSFER_PAYEE_ID\",
      \"approved\": true
    }
  }"
```

**❌ 错误做法 - 非真实转账**：
```bash
# Using payee_name creates a regular transaction, NOT a transfer
"payee_name": "Transfer: To Account B"  # YNAB won't link this
```

#### 获取转账收款人ID

获取所有账户的 `transfer_payee_id`：
```bash
curl "$YNAB_API/budgets/$BUDGET_ID/accounts" \
  -H "Authorization: Bearer $API_KEY" | \
  jq -r '.data.accounts[] | "\(.name): \(.transfer_payee_id)"'
```

将这些ID存储在您的个人配置文件（TOOLS.md或本地配置文件）中以供快速参考。

#### 正确操作后的效果

使用 `transfer_payee_id` 时：
- YNAB会创建**两个关联的交易**（每个账户一个）
- 相匹配的交易会自动出现在目标账户中
- 两个交易都会被标记为转账（不属于常规支出/收入）
- 分类会自动设置为“Transfer”（不影响预算）
- 删除其中一个账户会同时删除两个交易

#### 常见转账错误

1. **使用收款人名称** → 会创建常规交易，而非转账
2. **手动创建两边** → 会导致重复交易而非关联交易
3. **设置分类** → 转账不应有分类（YNAB会忽略这一点）
4. **使用错误的transfer_payee_id** → 转账会发送到错误的账户

#### 转账与常规交易的区别

| 转账（transfer_payee_id = transfer_payee_id） | 常规交易（payee_name） |
|----------------------------------------|----------------------------------|
| 创建两个关联的交易                | 创建一个交易                          |
| 自动分类为转账                | 需要手动分类                          |
| 不影响预算                  | 会影响预算                          |
| 两边会自动对账                | 需要手动对账                          |

## 常见账户ID结构

在配置文件中存储账户ID（示例结构）：
```json
{
  "accounts": {
    "primary_checking": "UUID-HERE",
    "savings": "UUID-HERE",
    "cash": "UUID-HERE"
  },
  "default_account": "primary_checking"
}
```

**切勿** 在脚本中硬编码账户ID——使用配置文件进行引用。

## 常见操作

### 添加交易

```bash
YNAB_API="https://api.ynab.com/v1"

curl -X POST "$YNAB_API/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"transaction\": {
      \"account_id\": \"$ACCOUNT_ID\",
      \"date\": \"2026-02-21\",
      \"amount\": -10000,
      \"payee_name\": \"Coffee Shop\",
      \"category_id\": \"$CATEGORY_ID\",
      \"memo\": \"Morning coffee\",
      \"approved\": true
    }
  }"
```

### 在账户间创建转账

```bash
# Step 1: Get destination account's transfer_payee_id
DEST_ACCOUNT_NAME="Savings"
TRANSFER_PAYEE_ID=$(curl -s "$YNAB_API/budgets/$BUDGET_ID/accounts" \
  -H "Authorization: Bearer $API_KEY" | \
  jq -r ".data.accounts[] | select(.name == \"$DEST_ACCOUNT_NAME\") | .transfer_payee_id")

# Step 2: Create transfer transaction
curl -X POST "$YNAB_API/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"transaction\": {
      \"account_id\": \"$SOURCE_ACCOUNT_ID\",
      \"date\": \"2026-02-21\",
      \"amount\": -50000,
      \"payee_id\": \"$TRANSFER_PAYEE_ID\",
      \"memo\": \"Monthly savings transfer\",
      \"approved\": true
    }
  }"

# YNAB will automatically create the matching transaction in the destination account
```

**重要**：只需创建**一个交易**——YNAB会自动创建另一边的交易。

### 搜索交易

```bash
# Get transactions since date
curl "$YNAB_API/budgets/$BUDGET_ID/transactions?since_date=2026-02-01" \
  -H "Authorization: Bearer $API_KEY"

# Filter by payee (client-side with jq)
... | jq '.data.transactions[] | select(.payee_name | contains("Coffee"))'
```

### 获取分类

```bash
curl "$YNAB_API/budgets/$BUDGET_ID/categories" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.category_groups[].categories[] | {id, name}'
```

## 月度支出报告

计算月度支出时：
1. 获取当月的所有交易
2. 筛选：`amount < 0`（仅计算支出）
3. 排除配置中的非可自由支配类别（税费、转账等）
4. 将拆分交易展开为子类别
5. 按类别或总额进行汇总

**提示**：为了更好地分析预算，建议将小额重复支出与大额一次性支出分开。

## 🛠️ 可用脚本

所有脚本都位于 `/skills/ynab-api/scripts/` 目录中，可直接使用。

### `setup-automation.sh [--dry-run]`
**⭐ 从这里开始** - 一键自动化设置。

```bash
./setup-automation.sh          # Interactive setup
./setup-automation.sh --dry-run # Preview changes
```

创建所有推荐的cron作业：
- 每日预算检查（早上7:15）
- 每周支出回顾（周一早上8:00）
- 中月目标检查（15日早上9:00）
- 即将到期的账单提醒（每天上午10:00）

**功能**：
1. 验证YNAB配置文件是否存在
2. 提示输入您的WhatsApp号码
3. 创建4个自动化cron作业
4. 确认设置成功

**这是推荐的入门方式！**

### `goals-progress.sh [month]`
为所有类别目标显示可视化进度条。

```bash
./goals-progress.sh          # Current month
./goals-progress.sh 2026-01  # Specific month
```

**示例输出：**
```
📊 PROGRESSI OBIETTIVI - 2026-02-01

Palestra 🏋️♂️:
  ████░░░░░░ 8% (€22/€270) 🟢

Salute ⚕️:
  ████████░░ 43% (€261/€500) 🟡

Mangiare Fuori 🍝:
  ██████████ 119% (€178/€150) 🔴
```

### `scheduled-upcoming.sh [days]`
列出即将发生的预定交易。

```bash
./scheduled-upcoming.sh     # Next 7 days
./scheduled-upcoming.sh 30  # Next 30 days
```

**示例输出：**
```
📅 TRANSAZIONI PROGRAMMATE - Prossimi 7 giorni

2026-03-01 💸 Lisa Valent: €-42.18 - Spotify
2026-03-02 💸 Andrea Schiffo: €-84.36 - Spotify lui e moglie
---
TOTALE: €-126.54
```

### `month-comparison.sh [month1] [month2]`
比较两个月的支出情况。

```bash
./month-comparison.sh                    # Current vs last month
./month-comparison.sh 2026-02 2026-01    # Specific months
```

**示例输出：**
```
📊 CONFRONTO SPESE
2026-02-01 vs 2026-01-01

Casa 🏠: €1,241 (era €450) ⚠️ +176%
Mangiare Fuori 🍝: €178 (era €120) ↗️ +48%
Palestra 🏋️♂️: €100 (era €100) = 0%
---
TOTALE 2026-02: €5,298
TOTALE 2026-01: €3,450
Differenza: +€1,848 (+53.6%)
```

### `transfer.sh SOURCE_ACCOUNT DEST_ACCOUNT AMOUNT DATE [MEMO]`
在账户间创建正确的关联转账。

```bash
./transfer.sh abc-123 "Savings" 100.50 2026-02-21 "Monthly savings"
```

**重要**：使用 `transfer_payee_id` 以确保YNAB能够识别转账。

### `daily-budget-check.sh`
全面的早晨预算报告（专为cron作业设计）。

```bash
./daily-budget-check.sh
```

**示例输出：**
```
☀️ BUDGET CHECK MATTUTINO

💰 Age of Money: 141 giorni ✅

📅 Prossime uscite (7gg)
• Domani: Lisa Valent €42.18

⚠️ Alert Budget Superato
• Mangiare Fuori 🍝: €178 / €150 (+€28)

🎯 Obiettivi in ritardo
• Palestra 🏋️♂️: 8% (€22/€270)
```

此脚本非常适合用于自动化cron作业，以获取每日预算概览。

## 个人配置

对于个人偏好（商家映射、类别排除、默认账户）：

**选项1**：将其添加到您的工作空间 `TOOLS.md` 中：
```markdown
## YNAB Personal Config
- Default account: [account_id]
- Exclude from budget: Category1, Category2
- Merchant mappings: Store → Category
```

**选项2**：创建本地配置文件（例如：`~/.config/ynab/rules.json`）：
```json
{
  "exclude_categories": ["Taxes", "Transfers"],
  "merchant_map": {
    "Coffee Shop": "category_id_here"
  }
}
```

该技能会检查交易历史的一致性——您的个人偏好将保持私密。

## 安全注意事项

- **切勿** 将API密钥提交到版本控制系统中
- 将 `YNAB_API_KEY` 存储在环境变量或安全配置文件（`~/.config/ynab/config.json`，权限设置为600）
- **切勿** 在输出中记录或显示完整的API密钥

## API文档

官方YNAB API文档：https://api.ynab.com

速率限制：每小时每个IP约200次请求。

## 🤖 自动化建议

### 每日早晨检查（推荐）
每天早上7:15获取全面的预算概览：
```bash
openclaw cron add --name "Daily Budget Check" \
  --schedule "15 7 * * *" \
  --session isolated \
  --model gemini-flash \
  --delivery announce \
  --task "Run YNAB daily budget check and send via WhatsApp"
```

### 每周支出回顾
每周一早上比较上周与上个月的支出情况：
```bash
openclaw cron add --name "Weekly Spending Review" \
  --schedule "0 8 * * 1" \
  --session isolated \
  --model gemini-flash \
  --delivery announce \
  --task "Compare current month vs last month YNAB spending"
```

### 目标进度提醒
每月15日提醒检查目标进度：
```bash
openclaw cron add --name "Mid-Month Goal Check" \
  --schedule "0 9 15 * *" \
  --session isolated \
  --model gemini-flash \
  --delivery announce \
  --task "Show YNAB goals progress for current month"
```

### 定时交易提醒
在预定支付前2天收到通知：
```bash
openclaw cron add --name "Upcoming Bills Alert" \
  --schedule "0 10 * * *" \
  --session isolated \
  --model gemini-flash \
  --delivery announce \
  --task "Show YNAB scheduled transactions for next 2 days"
```

## 💡 专业提示

1. **设定现实的目标**：使用YNAB的目标功能来跟踪您希望密切关注的类别
2. **检查资金流动情况**：目标至少为30天，90天以上更佳
3. **每周检查预定交易**：避免因忘记订阅而产生意外
4. **使用import_id**：从CSV导入数据时，使用唯一的import_id以避免重复
5. **存储转账收款人ID**：将这些ID保存在您的个人 `TOOLS.md` 文件中以供快速参考
6. **立即分类交易**：切勿让交易保持未分类状态
7. **月度对比**：使用 `month-comparison.sh` 来发现支出趋势

## 🔒 安全最佳实践

- 将API密钥存储在权限设置为600的配置文件中
- **切勿** 将 `config.json` 提交到版本控制系统中
- 将 `config.json` 添加到 `.gitignore` 文件中
- 定期轮换API令牌（每6-12个月）
- 在可能的情况下使用只读令牌（虽然YNAB目前不支持，但建议这样做！）

## 🆘 故障排除

**401 Unauthorized**：API密钥无效或已过期
- 在 https://app.ynab.com/settings/developer 重新生成令牌

**404 Not Found**：预算ID或交易ID不存在
- 在YNAB URL或 `/budgets` 端点验证预算ID

**429 Too Many Requests**：超出速率限制（每小时约200次请求）
- 在批量操作之间添加延迟
- 缓存常用数据（账户、类别）

**转账未关联**：使用收款人名称而非 `transfer_payee_id`
- 参见上面的“转账交易（关键）”部分

**常见错误**：
- 忘记使用毫单位（使用10而不是10000）
- 日期格式错误（使用YYYY-MM-DD）
- 缺少必需字段（account_id、date、amount）
- 在转账时使用收款人名称（应使用 `transfer_payee_id`）

## 📚 资源

- **YNAB API文档**：https://api.ynab.com
- **预算模板**：https://www.ynab.com/learn
- **OpenAPI规范**：https://github.com/ynab/ynab-sdk-ruby/blob/main/open_api_spec.yaml
- **速率限制**：每小时每个IP约200次请求
- **支持**：https://support.ynab.com

## 🎉 下一步？

安装完成后：
1. ✅ 使用 `goals-progress.sh` 进行测试
2. ✅ 设置每日预算检查cron作业
3. ✅ 将转账收款人ID存储在 `TOOLS.md` 中
4. ✅ 配置个人类别排除项
5. ✅ 享受自动化的预算洞察！

**祝您预算管理顺利！** 💰