---
name: odoo
description: "查询Odoo数据，包括销售人员的绩效、客户分析、订单、发票、客户关系管理（CRM）信息、会计数据、增值税（VAT）信息、库存情况以及应收账款（AR）和应付账款（AP）信息。可以生成WhatsApp卡片、PDF文件和Excel报表。当用户明确提到Odoo或请求Odoo数据时，请使用此功能。"
---

# Odoo财务智能

**仅限读取、以证据为先、基于账目的报告**

## 快速参考：常见的Odoo模型**

| 模型 | 包含内容 | 用途 |
|-------|------------------|---------|
| `res.users` | 用户/销售人员 | 按名称查找销售人员，获取user_id |
| `sale.order` | 销售订单 | 按销售人员划分的收入、订单数量、状态 |
| `account.move` | 发票/日记账分录 | 发票跟踪、付款、损益数据 |
| `res.partner` | 客户/联系人 | 客户信息、按收入排名的高客户 |
| `product.product` | 产品 | 产品销售、库存 |
| `account.account` | 账户科目表 | 财务报告、资产负债表 |
| `account.move.line` | 日记账分录行 | 详细的账目记录 |

## 安全性与凭证

### 所需的环境变量

此技能需要存储在`assets/autonomous-cfo/.env`中的Odoo连接凭证：

| 变量 | 描述 | 是否为秘密信息 |
|----------|-------------|--------|
| `ODOO_URL` | Odoo实例URL（例如：`https://your-odoo.com`） | 否 |
| `ODOO_DB` | Odoo数据库名称 | 否 |
| `ODOO_USER` | Odoo用户名/电子邮件 | 否 |
| `ODOO_PASSWORD` | Odoo密码或API密钥 | **是** |

**设置：**
```bash
cd skills/odoo/assets/autonomous-cfo
cp .env.example .env
# Edit .env with your actual credentials
nano .env
```

### 模型调用策略

根据`skill.json`的策略，**模型调用是被禁用的**。此技能处理敏感的财务数据和外部Odoo连接——必须由用户明确调用。

**数据处理：**所有查询均为只读操作，不会修改或泄露任何数据。

### 数据处理规则：
- **仅限读取**：所有修改数据的方法（如`create`、`write`、`unlink`等）在客户端层面被阻止。
- **无数据泄露**：报告在`assets/autonomous-cfo/output/`目录下生成。
- **网络端点**：仅连接到`.env`中指定的Odoo URL。
- **输出格式**：PDF、Excel和WhatsApp图片卡片（仅限本地文件）。

### 安装

此技能需要一个包含特定包的Python虚拟环境：

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

## 重要规则：
1. **切勿假设**——在生成报告之前，务必询问相关细节。
2. **多公司检查**——如果存在多个公司，请询问使用哪个公司的数据。
3. **基于账目**——使用账户科目表和日记账分录（`account.move.line`），而不仅仅是发票摘要。
4. **验证时间范围**——运行报告前请与用户确认日期范围。
5. **无默认设置**——所有假设都必须得到确认。

## 在生成任何报告之前，请询问：
1. “应该使用哪个公司的数据？”（如果有多个公司）
2. “时间范围是什么？（起始/结束日期）”
3. “需要包含哪些账户或账户类型？”
4. “是否有特定的细分需求？”（按账户、合作伙伴、日记账等）
5. **输出格式偏好是什么？”（PDF、WhatsApp图片卡片，还是两者都需要）

## 入口点

使用包含`fpdf2`、`matplotlib`、`pillow`的虚拟环境来生成正确的PDF/图表：

```bash
./skills/odoo/assets/autonomous-cfo/venv/bin/python ./skills/odoo/assets/autonomous-cfo/src/tools/cfo_cli.py <command>
```

或者从技能目录直接调用：
```bash
cd skills/odoo/assets/autonomous-cfo && ./venv/bin/python src/tools/cfo_cli.py <command>
```

## 基于账户科目表的报告

报告应基于以下数据构建：
- `account.account`：账户科目表结构（代码、名称、类型、内部组）
- `account.move.line`：日记账分录行（借方、贷方、账户ID、日期）
- `account.journal`：来源日记账（类型：销售、采购、现金、银行、普通）

### 账户内部组：
- **资产**：资产（流动资产、非流动资产、现金、应收账款）
- **负债**：负债（应付账款、税费、应计费用）
- **所有者权益**：所有者权益
- **收入**：收入账户
- **费用**：成本和费用账户
- **资产负债表外账户**：资产负债表外的账户

### 常见账户类型：
- `asset_cash`：银行和现金账户
- `asset_receivable`：应收账款
- `asset_current`：流动资产
- `liability_payable`：应付账款
- `income`：收入账户
- `expense`：费用账户

### 特殊的权益类型（Odoo特定）：
- `equity`：标准权益账户（股本、留存收益）
- `equity_unaffected`：**暂挂账户**，用于未分配的利润/亏损（例如，999999）

**对于资产负债表至关重要：**
Odoo的`equity_unaffected`是一个暂挂账户。**切勿直接使用其账目余额**。

**正确的权益计算方法：**
1. **正确的权益计算**（类型：`equity`）——使用账目余额（贷方 - 借方）。
2. **留存收益**（往年）——从`equity_unaffected`中获取账目余额。
3. **当年收益**——实时计算：收入 - 费用。

```
Total Equity = Equity Proper + Retained Earnings + Current Year Earnings
```

当年收益 = Σ（收入贷方 - 费用借方）

**为什么这很重要：**Odoo在资产负债表中实时计算当年收益。如果仅使用`equity_unaffected`的账目余额，会导致资产负债表不平衡。

## 自动检测报告标准

该技能会根据国家/司法管辖区自动检测公司的会计标准，并相应地格式化报告。

**支持的会计标准：**
| 标准 | 司法管辖区 | 备注 |
|----------|--------------|-------|
| IFRS | 国际 | 大多数国家的默认标准 |
| US GAAP | 美国 | 在SEC注册的公司 |
| Ind-AS | 印度 | 与IFRS趋同的印度会计准则 |
| UK GAAP | 英国 | FRS 102 |
| SOCPA | 沙特阿拉伯 | 采用IFRS |
| EU IFRS | 欧盟 | IAS规定 |
| CAS | 中国 | 中国会计准则 |
| JGAAP | 日本 | 日本会计准则 |
| ASPE | 加拿大 | 私营企业 |
| AASB | 澳大利亚 | 澳大利亚会计准则 |

**检测逻辑：**
1. 从`res.company`中查询公司的国家。
2. 将国家代码映射到相应的会计标准。
3. 应用特定标准的格式：
   - 数字格式（1,234.56 vs 1.234,56）
   - 负数的显示方式（(123) vs -123）
   - 日期格式（DD/MM/YYYY vs MM/DD/YYYY）
   - 报表标题（资产负债表 vs 财务状况表）
   - 现金流量方法（间接法 vs 直接法）

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

### 预制报告
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

对于预制命令未涵盖的销售/CRM数据，可以使用直接RPC查询：

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

### 临时报告
```bash
# Custom comparison
cfo_cli.py adhoc --from YYYY-MM-DD --to YYYY-MM-DD --metric-a "revenue" --metric-b "expenses"

# Examples:
cfo_cli.py adhoc --metric-a "cash in" --metric-b "cash out"
cfo_cli.py adhoc --metric-a "direct expenses" --metric-b "indirect expenses"
```

### 输出格式
```bash
--output whatsapp   # Dark theme 1080x1080 PNG cards
--output pdf        # Light theme A4 PDF
--output excel      # Excel workbook (.xlsx)
--output both       # PDF + WhatsApp cards
--output all        # PDF + Excel + WhatsApp cards
```

## 自动可视化

**报告默认包含适当的可视化内容：**

| 报告类型 | 自动包含的图表 |
|--------|---------------------|
| 财务健康状况 | 现金状况、烧钱速度趋势、资金预测 |
| 收入 | 季度趋势、主要客户、增长关键指标 |
| 应收账款/应付账款账龄 | 账龄分布图、逾期重点显示 |
| 费用 | 类别细分、趋势、主要供应商 |
| 高管报告 | 所有关键指标卡片、汇总图表 |
| 资产负债表 | 资产/负债构成 |
| 损益表 | 收入与费用对比、利润率趋势 |
| 现金流量 | 经营活动明细、现金趋势 |

**规则：**如果可视化内容能让报告更清晰，请自动包含它们。切勿询问“是否需要图表”——直接添加即可。

## 交互式参数收集

如果缺少必要的参数，该技能会询问：
1. **公司**：“使用哪个公司的数据？”（列出可用选项）
2. **时间范围**：“时间范围是什么？（例如：‘上个月’、‘2024年第四季度’、自定义日期）”
3. **账户**：“需要包含哪些账户或账户组？”（例如：‘所有收入’、‘仅银行账户’）
4. **细分方式**：“按什么进行分组？（月份、客户、类别、账户）”
5. **输出格式**：“输出格式是什么？（WhatsApp图片卡片、PDF、两者都需要）”

## 如何在聊天中使用

只需自然地提问：

**销售与CRM：**
- “[姓名]销售人员的表现如何？”
- “显示[销售人员]的主要客户”
- “比较销售团队的表现”
- “哪位销售人员的订单最多？”

**财务报告：**
- “给我上季度的财务健康状况报告”
- “显示过去6个月的收入与费用情况”
- “我的应收账款账龄是多少？”
- “生成本月的执行摘要”
- “根据账户科目表显示损益表”

**通用查询：**
- “本月我们收到了多少订单？”
- “前10位客户是谁？”
- “显示[客户名称]的发票状态”

该技能将：
1. 检查是否存在多个公司，并询问使用哪个公司的数据。
2. 解析您的请求。
3. 询问任何缺失的信息。
4. 从Odoo中获取数据（使用日记账分录或直接RPC）。
5. 生成图表和WhatsApp图片卡片。
6. 通过WhatsApp图片卡片和/或PDF形式提供报告。

## 严格规则：
1. Odoo的RPC输出是最终依据。
2. 严格遵循只读原则（禁止创建/修改/删除数据）。
3. 除非用户请求，否则不采取任何主动操作。
4. 每个数字都附带方法说明。
5. 在做出任何假设之前，务必与用户确认。
6. **始终包含可视化内容**——如果报告需要图表，应自动添加，无需询问。

## 诊断工具
```bash
python3 ./skills/odoo/assets/autonomous-cfo/src/tools/cfo_cli.py doctor
```

## 报告主题：
- **WhatsApp图片卡片**：**“午夜账目”（颜色：#0a0e1a，铜色渐变）；**“PDF报告”：**纯白色背景，铜色点缀，专业布局