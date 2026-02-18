---
name: odoo
description: "查询Odoo数据，包括销售人员的绩效、客户分析、订单、发票、客户关系管理（CRM）信息、会计数据、增值税（VAT）信息、库存情况以及应收账款（AR）和应付账款（AP）信息。可以生成WhatsApp卡片、PDF文件和Excel报表。当用户明确提到Odoo或请求Odoo数据时，请使用此功能。"
---
# Odoo财务智能

**仅限读取、以证据为先、基于账本的报表**

## 快速参考：常见的Odoo模型

| 模型 | 包含内容 | 用途 |
|-------|------------------|---------|
| `res.users` | 用户/销售人员 | 按名称查找销售人员，获取用户ID |
| `sale.order` | 销售订单 | 按销售人员划分的收入、订单数量、状态 |
| `account.move` | 发票/日记账分录 | 发票追踪、付款、损益数据 |
| `res.partner` | 客户/联系人 | 客户信息、按收入排序的顶级客户 |
| `product.product` | 产品 | 产品销售、库存 |
| `account.account` | 账户科目表 | 财务报告、资产负债表 |
| `account.move.line` | 日记账分录 | 详细的账本分录 |

## 安全性与凭证

### 安全模型

该技能采用了**深度防御的安全模型**：

1. **需要用户调用**：该技能不能由AI模型自动调用 |
2. **仅限读取**：所有数据修改在代码层面被禁止 |
3. **凭证隔离**：凭证仅存储在本地`.env`文件中，从不传输到其他地方 |
4. **网络边界**：仅连接到用户指定的Odoo URL，不进行外部数据传输 |

### 所需的环境变量

该技能**需要**存储在`assets/autonomous-cfo/.env`中的Odoo连接凭证：

| 变量 | 描述 | 是否为秘密信息 | 是否必需 |
|----------|-------------|--------|----------|
| `ODOO_URL` | Odoo实例URL（例如：`https://your-odoo.com`） | 否 | **是** |
| `ODOO_DB` | Odoo数据库名称 | 否 | **是** |
| `ODOO_USER` | Odoo用户名/电子邮件 | 否 | **是** |
| `ODOO_PASSWORD` | Odoo API密钥（推荐）或密码 | **是** | **是** |

**⚠️ 重要提示**：这些凭证是必需的。没有这些凭证，技能将无法运行。

**设置：**
```bash
cd skills/odoo/assets/autonomous-cfo
cp .env.example .env
# Edit .env with your actual credentials
nano .env
```

### API密钥与密码

**在生产环境中，使用Odoo API密钥：**
1. 登录Odoo → 设置 → 账户安全 → API密钥
2. 生成一个新的密钥（例如：“Financial Reports Skill”）
3. 将此密钥用作`ODOO_PASSWORD`

**为什么使用API密钥？**
- 权限范围明确（可以是仅限读取）
- 可以独立撤销
- 避免暴露您的主密码
- 在Odoo中提供更好的审计追踪

### 认证方法

**XML-RPC（旧版本，默认）：**
- 在XML-RPC请求体中发送密码/API密钥
- 所有Odoo版本都支持

**JSON-RPC（Odoo 19及以上版本）：**
- 在`Authorization: Bearer <api_key>`头部发送API密钥
- 对于大型数据集更高效
- 使用`ODOO_RPC_BACKEND=json2`来启用

### 模型调用策略

**🚫 模型调用被严格禁止。**

根据`skill.json`的规定：
```json
"modelInvocation": {
  "disabled": true,
  "requiresUserInvocation": true
}
```

这意味着：
- AI模型不能自动调用此技能
- 用户必须明确请求Odoo操作
- 每次调用都需要用户的意图

### 仅限读取的规则

该技能禁止所有数据修改操作：

**被禁止的方法：**
- `create`（创建）、`write`（写入）、`unlink`（删除）（CRUD操作）
- `copy`（复制记录）
- `action_post`、`action_confirm`、`button_validate`（工作流操作）

**允许的方法（仅限读取）：**
- `search`（搜索）、`search_read`（搜索并读取）、`read`（读取数据）
- `search_count`、`fields_get`（获取元数据）
- `name_search`、`context_get`、`default_get`（辅助函数）

尝试调用被禁止的方法会引发`PermissionError`（权限错误）。

### 数据处理与隐私

- **无数据泄露**：报表在`assets/autonomous-cfo/output/`本地生成 |
- **无数据传输**：不向外部服务器发送使用数据 |
- **网络隔离**：仅连接到`.env`中指定的`ODOO_URL` |
- **凭证安全**：密码/API密钥不会被记录或显示 |
- **本地处理**：所有图表生成和PDF创建都在本地完成

### 输出安全

所有输出文件均为本地文件：
- `output/pdf_reports/` - PDF报表 |
- `output/whatsapp_cards/` - PNG图片卡片 |
- `output/charts/` - 图表图像 |
- `output/excel/` - Excel电子表格

没有数据上传到云端，也没有数据会离开您的机器，只会发送到您指定的Odoo实例。

### 安装

该技能需要一个包含特定包的Python虚拟环境：

```bash
cd skills/odoo/assets/autonomous-cfo
./install.sh
```

或者手动安装：
```bash
cd skills/odoo/assets/autonomous-cfo
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

**依赖库：`requests`、`matplotlib`、`pillow`、`fpdf2`、`openpyxl`

## 重要规则

1. **永远不要假设** - 在生成报表之前，务必询问清楚 |
2. **多公司检查** - 如果存在多个公司，请询问使用哪个公司 |
3. **基于账本** - 使用账户科目表和日记账分录（`account.move.line`），而不仅仅是发票摘要 |
4. **验证时间范围** - 在运行前与用户确认日期范围 |
5. **没有默认设置** - 每个假设都需要确认 |

## 在生成任何报表之前，请询问：

1. “我应该使用哪个公司？”（如果有多个公司）
2. “时间范围是什么？（起始/结束日期）”
3. “包括哪些账户或账户类型？”
4. “需要特定的细分吗？”（按账户、按合作伙伴、按日记账等）
5. **输出格式偏好是什么？”（PDF、WhatsApp卡片，还是两者都需）

## 入口点

使用包含`fpdf2`、`matplotlib`、`pillow`的虚拟环境来生成正确的PDF/图表：

```bash
./skills/odoo/assets/autonomous-cfo/venv/bin/python ./skills/odoo/assets/autonomous-cfo/src/tools/cfo_cli.py <command>
```

或者从技能目录直接运行：
```bash
cd skills/odoo/assets/autonomous-cfo && ./venv/bin/python src/tools/cfo_cli.py <command>
```

## 基于账户科目表的报告

报表应基于以下数据构建：
- `account.account` - 账户科目表结构（代码、名称、类型、内部组）
- `account.move.line` - 日记账分录（借方、贷方、账户ID、日期）
- `account.journal` - 来源日记账（类型：销售、采购、现金、银行、普通）

### 账户内部组
- **资产** - 资产（流动资产、非流动资产、现金、应收账款）
- **负债** - 负债（应付账款、税款、应计负债）
- **权益** - 所有者权益
- **收入** - 收入账户
- **费用** - 费用账户
- **非资产负债表账户** - 非资产负债表账户

### 常见账户类型
- `asset_cash` - 银行和现金账户
- `asset_receivable` - 应收账款
- `asset_current` - 流动资产
- `liability_payable` - 应付账款
- `income` - 收入
- `expense` - 费用

### 特殊的权益类型（Odoo特定）
- `equity` - 标准权益账户（股本、留存收益）
- `equity_unaffected` - **暂挂账户**，用于未分配的利润/亏损（例如，999999）

**对于资产负债表至关重要：**
Odoo的`equity_unaffected`是一个暂挂账户。请**不要直接使用其账本余额**。

**正确的权益计算方法：**
1. **正确的权益计算**（类型：`equity`） - 使用账本余额（贷方 - 借方）
2. **留存收益**（往年） - 来自`equity_unaffected`的账本余额
3. **当年收益** - 实时计算：收入 - 费用

```
Total Equity = Equity Proper + Retained Earnings + Current Year Earnings
```

当年收益的计算公式为：当年收益 = Σ（收入贷方 - 费用借方）

**为什么这很重要：**Odoo在资产负债表中实时计算当年收益。如果仅使用`equity_unaffected`的账本余额，会导致资产负债表不平衡。

## 自动检测会计标准

该技能会根据国家/司法管辖区自动检测公司的会计标准，并相应地格式化报表。

**支持的会计标准：**
| 标准 | 司法管辖区 | 备注 |
|----------|--------------|-------|
| IFRS | 国际 | 大多数国家的默认标准 |
| US GAAP | 美国 | 在SEC注册的公司 |
| Ind-AS | 印度 | 与IFRS一致的印度会计准则 |
| UK GAAP | 英国 | FRS 102 |
| SOCPA | 沙特阿拉伯 | 采用IFRS |
| EU IFRS | 欧盟 | IAS法规 |
| CAS | 中国 | 中国会计准则 |
| JGAAP | 日本 | 日本会计准则 |
| ASPE | 加拿大 | 私营企业 |
| AASB | 澳大利亚 | 澳大利亚会计准则 |

**检测逻辑：**
1. 从`res.company`中查询公司的国家 |
2. 将国家代码映射到相应的会计标准 |
3. 应用标准特定的格式：
   - 数字格式（1,234.56 vs 1.234,56）
   - 负数的显示方式（(123) vs -123）
   - 日期格式（DD/MM/YYYY vs MM/DD/YYYY）
   - 报表标题（资产负债表 vs 财务状况表）
   - 现金流方法（间接法 vs 直接法）

**自定义设置：**
```python
# Force a specific standard
reporter.generate(..., standard="US_GAAP")
```

## 命令

### 销售与CRM查询

```bash
# Salesperson performance - use direct RPC for flexibility
./venv/bin/python -c "
from src.visualizers.whatsapp_cards import WhatsAppCardGenerator
# Query sale.order by user_id, aggregate by month/status
# Generate cards with generate_kpi_card() and generate_comparison_card()
"

# Example RPC query for salesperson:
# - sale.order (user_id, amount_total, state, date_order)
# - account.move (invoice_user_id, amount_total, payment_state)
# - res.users (salesperson info)
# - res.partner (customer info)
```

### 预建报表

```bash
# Financial Health - cash flow, liquidity, burn rate, runway
cfo_cli.py health --from YYYY-MM-DD --to YYYY-MM-DD --company-id ID

# Revenue Analytics - MoM trends, top customers
cfo_cli.py revenue --from YYYY-MM-DD --to YYYY-MM-DD --company-id ID

# AR/AP Aging - overdue buckets
cfo_cli.py aging --as-of YYYY-MM-DD --company-id ID

# Expense Breakdown - by vendor/category
cfo_cli.py expenses --from YYYY-MM-DD --to YYYY-MM-DD --company-id ID

# Executive Summary - one-page CFO snapshot
cfo_cli.py executive --from YYYY-MM-DD --to YYYY-MM-DD --company-id ID
```

### 直接RPC查询（高级）

对于预建命令未涵盖的销售/CRM数据，可以使用直接RPC查询：

```python
# Query sales orders by salesperson
orders = jsonrpc('sale.order', 'search_read',
    [[('user_id', '=', SALESPERSON_ID)]],
    {'fields': ['name', 'partner_id', 'amount_total', 'state', 'date_order']})

# Query invoices by salesperson
invoices = jsonrpc('account.move', 'search_read',
    [[('invoice_user_id', '=', SALESPERSON_ID), ('move_type', '=', 'out_invoice')]],
    {'fields': ['name', 'partner_id', 'amount_total', 'payment_state']})

# Find salesperson by name
users = jsonrpc('res.users', 'search_read',
    [[('name', 'ilike', 'name_here')]],
    {'fields': ['id', 'name', 'login']})
```

### 临时报表

```bash
# Custom comparison
cfo_cli.py adhoc --from YYYY-MM-DD --to YYYY-MM-DD --metric-a "revenue" --metric-b "expenses"

# Examples:
cfo_cli.py adhoc --metric-a "cash in" --metric-b "cash out"
cfo_cli.py adhoc --metric-a "direct expenses" --metric-b "indirect expenses"
```

### 输出格式

### 自动可视化

**报表默认包含适当的可视化内容：**

| 报表 | 自动包含的图表 |
|--------|---------------------|
| 财务健康状况 | 现金状况、烧钱速度趋势、资金周转周期 |
| 收入 | 月度趋势、顶级客户、增长关键指标 |
| 应收账款/应付账款账龄 | 账龄分布图、逾期重点 |
| 费用 | 类别细分、趋势、主要供应商 |
| 高管报表 | 所有关键指标卡片、汇总图表 |
| 资产负债表 | 资产/负债构成 |
| 损益表 | 收入与费用对比、利润率趋势 |
| 现金流 | 经营费用细分、现金趋势 |

**规则：**如果可视化内容能让报表更清晰，请自动包含它们。永远不要问“是否需要图表？”——直接添加即可。

## 交互式参数收集

如果缺少必要的参数，技能会询问：

1. **公司**：“使用哪个公司？”（列出可用选项）
2. **时间范围**：“时间范围是什么？（例如：‘上个月’、‘2024年第四季度’、自定义日期）”
3. **账户**：“包括哪些账户或账户组？”（例如：‘所有收入’、‘仅银行账户’）
4. **细分方式**：“按什么进行分组？（月份、客户、类别、账户）”
5. **输出格式**：“输出格式是什么？（WhatsApp卡片、PDF、两者都需要）”

## 如何在聊天中使用

只需自然地提问：

**销售与CRM：**
- “[姓名]销售人员的表现如何？”
- “显示[销售人员]的顶级客户”
- “比较销售团队的表现”
- “哪位销售人员的订单最多？”

**财务报告：**
- “给我上一季度的财务健康状况报告”
- “显示过去6个月的收入与费用”
- “我的应收账款账龄是多少？”
- “生成本月的执行摘要”
- “根据账户科目表显示损益表”

**通用查询：**
- “这个月我们收到了多少订单？”
- “前10位客户是谁？”
- “显示[客户名称]的发票状态”

技能将：
1. 检查是否存在多个公司，并询问使用哪个公司 |
2. 解析您的请求 |
3. 询问任何缺失的信息 |
4. 使用账本分录或直接RPC从Odoo获取数据 |
5. 生成图表和WhatsApp卡片 |
6. 通过WhatsApp卡片和/或PDF形式提供结果

## 严格规则

1. Odoo RPC输出是最终数据来源 |
2. 严格限制为仅读（禁止创建/写入/删除操作） |
3. 除非用户请求，否则不采取主动操作 |
4. 每个数字都附带方法说明 |
5. 在做出任何假设之前，务必与用户确认 |
6. **始终包含可视化内容** - 如果报表需要图表，自动包含它们。报表应具备完整的可视化效果。

## 诊断工具

```bash
python3 ./skills/odoo/assets/autonomous-cfo/src/tools/cfo_cli.py doctor
```

## 报表主题

- **WhatsApp卡片**：**“午夜账本” — 深蓝色（#0a0e1a），铜色渐变（#cd7f32）**
- **PDF报告**：纯白色背景，铜色点缀，专业布局