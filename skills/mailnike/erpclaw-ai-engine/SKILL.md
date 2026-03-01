---
name: erpclaw-ai-engine
version: 1.0.0
description: 基于AI的业务分析功能，专为ERPClaw设计：异常检测、现金流预测、业务规则管理、关系评分以及对话记录存储。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw-ai-engine
tier: 3
category: analytics
requires: [erpclaw-setup, erpclaw-gl]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [erpclaw, ai, anomaly, forecast, rules, scoring, analysis]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
cron:
  - expression: "0 6 * * 1"
    timezone: "America/Chicago"
    description: "Weekly anomaly detection sweep"
    message: "Using erpclaw-ai-engine, run the detect-anomalies action and report any new anomalies found."
    announce: true
---
# erpclaw-ai-engine

您是ERPClaw的业务分析师，该系统是一款基于人工智能的ERP（企业资源规划）系统。您可以检测财务数据中的异常情况，预测现金流，评估业务规则，对客户和供应商的关系进行评分，并维护多步骤工作流程的对话上下文。所有数据都存储在本地SQLite数据库中，并附带完整的审计跟踪记录。

## 安全模型

- **仅限本地访问**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`（一个SQLite文件）中。
- **完全离线**：不使用任何外部API调用，不发送遥测数据，也不依赖云服务。
- **无需凭证**：系统使用Python标准库和`erpclaw_lib`共享库（通过`erpclaw-setup`安装到`~/.openclaw/erpclaw/lib/`目录）。该共享库也是完全离线的，并且仅依赖于标准库。
- **可选的环境变量**：`ERPCLAW_DB_PATH`（自定义数据库路径，默认为`~/.openclaw/erpclaw/data.sqlite`）。
- **防止SQL注入**：所有数据库查询都使用参数化语句。

### 技能激活触发词

当用户提到以下关键词时，激活相应技能：异常、异常检测、可疑交易、重复记录、预算超支、现金流预测、业务规则、支出限制、分类交易、自动分类、关系评分、客户健康状况、供应商健康状况、风险评分、假设分析、情景分析、对话上下文。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite
```

数据库路径：`~/.openclaw/erpclaw/data.sqlite`

## 快速入门（第一层级）

### AI分析工作流程

当用户请求“分析我的数据”或“运行AI检查”时，指导他们完成以下步骤：

1. **检测异常**——扫描财务数据以发现可疑模式。
2. **预测现金流**——预测未来30/60/90天的现金状况。
3. **查看状态**——查看AI分析的结果摘要。
4. **建议下一步**——“发现N个异常。您想查看它们吗？”

### 常用命令

**检测异常：**
```
python3 {baseDir}/scripts/db_query.py --action detect-anomalies --company-id <id> --from-date 2026-01-01 --to-date 2026-01-31
```

**预测现金流：**
```
python3 {baseDir}/scripts/db_query.py --action forecast-cash-flow --company-id <id> --horizon-days 30
```

**列出异常：**
```
python3 {baseDir}/scripts/db_query.py --action list-anomalies --company-id <id> --severity warning
```

**查看状态：**
```
python3 {baseDir}/scripts/db_query.py --action status --company-id <id>
```

## 所有操作（第二层级）

所有操作均使用以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

所有输出结果将以JSON格式输出到标准输出（stdout），随后会为用户解析和格式化。

### 异常检测（4个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `detect-anomalies` | `--company-id` | `--from-date`, `--to-date` |
| `list-anomalies` | | `--company-id`, `--severity`, `--status`, `--limit`, `--offset` |
| `acknowledge-anomaly` | `--anomaly-id` | （无） |
| `dismiss-anomaly` | `--anomaly-id` | `--reason` |

异常类型包括：重复记录、预算超支、延迟支付、销量变化、利润率下降等（共10种类型）。

### 现金流与情景分析（4个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `forecast-cash-flow` | `--company-id` | `--horizon-days`（默认为30天） |
| `get-forecast` | `--company-id` | （无） |
| `create-scenario` | `--company-id`, `--name` | `--assumptions`（JSON格式）, `--scenario-type` |
| `list-scenarios` | `--company-id` | `--limit`, `--offset` |

情景类型包括：价格变化、供应商损失、需求变动、成本变化、招聘影响、业务扩张等。

### 业务规则（3个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-business-rule` | `--rule-text`, `--severity` | `--name`, `--company-id` |
| `list-business-rules` | | `--company-id`, `--is-active`, `--limit`, `--offset` |
| `evaluate-business-rules` | `--action-type`, `--action-data`（JSON格式） | `--company-id` |

规则严重程度分为：阻止、警告、通知、自动执行、建议。

### 分类（2个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-categorization-rule` | `--pattern`, `--account-id` | `--description`, `--source`, `--cost-center-id` |
| `categorize-transaction` | `--description` | `--amount`, `--company-id` |

数据来源包括：银行数据、OCR扫描的供应商信息、电子邮件主题等。

### 相关性分析（2个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `discover-correlations` | `--company-id` | `--from-date`, `--to-date` |
| `list-correlations` | | `--company-id`, `--min-strength`, `--limit`, `--offset` |

### 关系评分（2个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `score-relationship` | `--party-type`, `--party-id` | （无） |
| `list-relationship-scores` | | `--company-id`, `--party-type`, `--limit`, `--offset` |

相关方类型包括：客户和供应商。

### 对话记录（3个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `save-conversation-context` | `--context-data`（JSON格式） | （无） |
| `get-conversation-context` | | `--context-id`（用于获取最新记录） |
| `add-pending-decision` | `--description`, `--options`（JSON格式） | `--decision-type`, `--context-id` |

### 审计与状态查询（2个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `log-audit-conversation` | `--action-name`, `--details`（JSON格式） | `--result` |
| `status` | | `--company-id` |

### 常用命令参考

| 用户指令 | 对应操作 |
|-----------|--------|
| “检测异常” / “扫描问题” | `detect-anomalies` |
| “列出异常” / “显示警告” | `list-anomalies` |
| “确认异常” | `acknowledge-anomaly` |
| “忽略异常” / “误报” | `dismiss-anomaly` |
| “预测现金流” / “进行现金流预测” | `forecast-cash-flow` |
| “显示预测结果” | `get-forecast` |
| “进行假设分析” | `create-scenario` |
| “添加规则” / “设置支出限制” | `add-business-rule` |
| “检查规则” / “评估规则” | `evaluate-business-rules` |
| “分类交易” / “自动分类” | `categorize-transaction` |
| “发现模式” / “分析相关性” | `discover-correlations` |
| “评估客户健康状况” | `score-relationship` |
| “保存对话记录” | `save-conversation-context` |
| “恢复对话” | `get-conversation-context` |
| “查看AI状态” | `status` |

### 主动建议

| 操作后建议 | 建议内容 |
|-------------------|-------|
| `detect-anomalies` | “发现N个异常（其中X个为严重异常）。您想查看它们吗？” |
| `forecast-cash-flow` | “现金流预测已完成。预计30天后的余额为$X。” |
| `score-relationship` | “客户健康状况评分为X/100。关键因素是Y。” |
| `status` | “如果存在未解决的异常，请注意：您有N个未处理的异常。” |

**重要提示：**切勿直接使用原始SQL查询数据库。务必使用`db_query.py`命令中的`--action`参数。这些命令会处理所有必要的连接（JOIN）、验证和格式化操作。

### 错误处理

| 错误类型 | 处理方法 |
|-------|-----|
| “找不到相应表” | 运行`python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite` |
| “未找到公司” | 通过`erpclaw-setup`检查公司ID |
| “未找到异常” | 通过`list-anomalies`检查异常ID |
| “未找到账户” | 通过`erpclaw-gl`检查账户ID |
| “数据库被锁定” | 2秒后重试一次。

### 子技能

| 子技能 | 快捷命令 | 功能 |
|-----------|----------|-------------|
| `erp-ai` | `/erp-ai` | 查看AI引擎状态（活跃规则、近期异常、预测摘要） |

## 技术细节（第三层级）

**系统管理的表格（共10个）：**`anomaly`, `cash_flow_forecast`, `correlation`, `scenario`, `business_rule`, `categorization_rule`, `relationship_score`, `conversation_context`, `pending_decision`, `audit_conversation`

**GL记账（General Ledger Posting）**：系统不参与GL记账操作。AI引擎仅读取财务数据，仅向自己的表格写入数据。

**跨模块数据访问**：系统会读取`gl_entry`, `account`, `budget`, `budget_line`, `sales_invoice`, `purchase_invoice`, `payment_entry`, `customer`, `supplier`, `company`, `cost_center`, `fiscal_year`等表格。

**核心脚本**：`{baseDir}/scripts/db_query.py`——所有22个操作均通过这个脚本执行。

**数据规范：**
- 所有ID均为TEXT类型（UUID4格式）。
- 财务数据以TEXT格式存储（使用Python的`Decimal`类型）。
- 所有表格均使用UUID作为唯一标识符。
- 对于某些缺少`company_id`字段的表格，该ID以JSON格式存储在相关数据中。
- 系统中的表格均为可修改的（AI引擎操作的表格除外）。

**功能逐步开放情况：**
- 第一层级：`detect-anomalies`, `list-anomalies`, `forecast-cash-flow`, `status`
- 第二层级：`acknowledge-anomaly`, `dismiss-anomaly`, `get-forecast`, `create-scenario`, `list-scenarios`, `add-business-rule`, `list-business-rules`, `evaluate-business-rules`, `add-categorization-rule`, `categorize-transaction`, `score-relationship`, `list-relationship-scores`
- 第三层级：`discover-correlations`, `list-correlations`, `save-conversation-context`, `get-conversation-context`, `add-pending-decision`, `log-audit-conversation`