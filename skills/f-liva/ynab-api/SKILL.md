---
name: ynab-api
description: >
  **YNAB（You Need A Budget）财务跟踪与分类的最佳实践**  
  适用于管理预算交易、分类支出，或通过 YNAB API 查询财务数据。
user-invocable: true
metadata: {"clawdbot":{"emoji":"💰","requires":{"env":["YNAB_API_KEY","YNAB_BUDGET_ID"]}}}
---
# YNAB预算管理

本技能提供了通过API管理YNAB预算的最佳实践，包括交易分类、数据一致性以及常见的工作流程。

## 配置

所需的环境变量或配置文件（`~/.config/ynab/config.json`）：
- `YNAB_API_KEY` - 你的YNAB个人访问令牌
- `YNAB_BUDGET_ID` - 你的预算ID（通过YNAB API或URL获取）

## 核心最佳实践

### 1. 始终立即分类

**切勿**在没有分类的情况下创建交易。未分类的交易会破坏预算跟踪功能。

在添加交易时，必须立即对其进行分类——切勿拖延。

### 2. 检查交易历史中的未知商家

当你遇到不熟悉的商家/收款人时：
1. 在YNAB中搜索与该收款人名称相同的过往交易记录
2. 使用与之前交易相同的分类
3. 保持分类的一致性

**原因**：这有助于保持分类的一致性，并减少用户的操作麻烦。

示例：
```bash
# Search for past transactions by payee
curl -s "https://api.ynab.com/v1/budgets/$BUDGET_ID/transactions" \
  -H "Authorization: Bearer $API_KEY" | \
  jq '.data.transactions[] | select(.payee_name | contains("MERCHANT_NAME"))'
```

### 3. 在添加新交易前检查待处理交易

在创建新交易之前：
1. 检查是否存在相同金额的未批准交易
2. 如果存在 → 批准该交易并根据需要更新收款人/备注信息
3. 如果不存在 → 创建新交易

**原因**：这样可以避免银行导入的交易重复记录。

### 4. 使用毫单位表示金额

YNAB API使用**毫单位**来表示所有金额：
- €10.00 = `10000`（收入为正数）
- -€10.00 = `-10000`（支出为负数）

**在显示金额时**始终除以1000，在提交时乘以1000。

### 5. 月度支出计算

在计算月度支出时：
- 仅统计`amount < 0`的交易（实际支出）
- 考虑排除以下非可自由支配的类别：
  - 税款支付（强制性支出，不属于可自由支配的支出）
  - 预付款/报销（临时性支出，不属于实际支出）
  - 未分类的交易（通常是转账或投资）
  - 一次性特殊支出（如果跟踪的是可自由支配的预算）

**注意**：排除规则取决于你的预算目标。请在本地配置文件或备注文件中配置具体的排除项。

### 6. 处理拆分交易

分类为“Split”的交易包含子交易。

**切勿**在报告中将“Split”作为单独的类别显示——始终将其展开为子类别：

```bash
# For each split transaction
if [ "$category_name" = "Split" ]; then
  for subtx in subtransactions; do
    echo "$subtx.category_name: $subtx.amount"
  done
fi
```

### 7. 转账收款人格式

在记录账户间的转账时，使用标准化的收款人名称以确保一致性：
- `Transfer: To [账户名称]`（支出方）
- `Transfer: From [账户名称]`（收入方）

这样可以方便地在报告中识别和过滤转账记录。

## 常见的账户ID结构

将账户ID存储在配置文件中（示例结构）：
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

**切勿**在脚本中硬编码账户ID——使用配置文件中的引用。

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

要计算月度支出：
1. 获取当月的所有交易记录
2. 筛选：`amount < 0`（仅计算支出）
3. 排除配置中指定的非可自由支配类别（税款、转账等）
4. 将拆分交易展开为子类别
5. 按类别或总计进行汇总

**提示**：为了更好地分析预算，可以考虑将小额的重复性支出与大额的一次性支出分开统计。

## 个人配置

对于个人偏好设置（如商家映射、类别排除、默认账户等）：
**选项1**：将其添加到你的工作空间文件`TOOLS.md`中：
```markdown
## YNAB Personal Config
- Default account: [account_id]
- Exclude from budget: Category1, Category2
- Merchant mappings: Store → Category
```

**选项2**：创建本地配置文件（例如`~/.config/ynab/rules.json`）：
```json
{
  "exclude_categories": ["Taxes", "Transfers"],
  "merchant_map": {
    "Coffee Shop": "category_id_here"
  }
}
```

该技能会检查交易历史的一致性——你的个人设置将保持私密性。

## 安全注意事项

- **切勿**将API密钥提交到版本控制系统中
- 将`YNAB_API_KEY`存储在环境变量或安全的配置文件中（`~/.config/ynab/config.json`，权限设置为600）
- **切勿**在输出中记录或显示完整的API密钥

## API文档

官方YNAB API文档：https://api.ynab.com

**请求限制**：每个IP每小时最多200次请求。

## 故障排除

- **401 Unauthorized**：API密钥无效或已过期
- **404 Not Found**：预算ID或交易ID不存在
- **429 Too Many Requests**：超出请求限制，请稍后重试

**常见错误**：
- 忘记使用毫单位（使用10而不是10000）
- 日期格式错误（使用YYYY-MM-DD）
- 缺少必需的字段（account_id、date、amount）