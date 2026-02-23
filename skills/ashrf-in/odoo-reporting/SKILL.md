---
name: odoo
description: "查询Odoo数据，包括销售人员的绩效、客户分析、订单、发票、客户关系管理（CRM）信息、会计数据、增值税（VAT）信息、库存情况以及应收账款（AR）和应付账款（AP）信息。支持生成WhatsApp卡片、PDF文件和Excel报表。当用户明确提到Odoo或请求Odoo数据时，请使用此功能。"
---
# Odoo财务智能

**仅限读取，以证据为先，基于账目的报告**

## 快速参考：常见的Odoo模型

| 模型 | 包含内容 | 用途 |
|-------|------------------|---------|
| `res.users` | 用户/销售人员 | 按名称查找销售人员，获取用户ID |
| `sale.order` | 销售订单 | 按销售人员划分的收入、订单数量、状态 |
| `account.move` | 发票/日记账分录 | 发票追踪、付款、损益数据 |
| `res.partner` | 客户/联系人 | 客户信息、按收入排序的顶级客户 |
| `product.product` | 产品 | 产品销量、库存 |
| `account.account` | 账户科目表 | 财务报告、资产负债表 |
| `account.move.line` | 日记账分录行 | 详细的账目记录 |

## 安全与凭证

### 安全模型

此技能实现了**深度防御的安全模型**：

1. **需要用户调用**：此技能不能由AI模型自主调用 |
2. **仅限读取**：所有数据修改在代码层面被阻止 |
3. **凭证隔离**：凭证仅存储在本地`.env`文件中，从不传输到其他地方 |
4. **网络边界**：仅连接到用户指定的Odoo URL，不进行外部数据传输 |

### 所需的环境变量

此技能**需要**存储在`assets/autonomous-cfo/.env`中的Odoo连接凭证：

| 变量 | 描述 | 是否为秘密信息 | 是否必需 |
|----------|-------------|--------|----------|
| `ODOO_URL` | Odoo实例URL（例如：`https://your-odoo.com`） | 否 | **是** |
| `ODOO_DB` | Odoo数据库名称 | 否 | **是** |
| `ODOO_USER` | Odoo用户名/电子邮件 | 否 | **是** |
| `ODOO_PASSWORD` | Odoo API密钥（推荐）或密码 | **是** | **是** |

**⚠️ 重要**：这些凭证是必需的。没有它们，技能将无法运行。

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
- 不会暴露你的主密码
- 在Odoo中提供更好的审计追踪

### 认证方法

**XML-RPC（旧版本，默认）：**
- 在XML-RPC请求体中发送密码/API密钥
- 所有Odoo版本都支持

**JSON-RPC（Odoo 19及以上版本）：**
- 在`Authorization: Bearer <api_key>`头部发送API密钥
- 对于大型数据集更高效
- 使用`ODOO_RPC_BACKEND=json2`来启用

### 模型调用政策

**🚫 模型调用被严格禁止。**

根据`skill.json`：
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

### 仅限读取的强制执行

**⚠️ 重要：客户端端的强制执行限制**

该技能实现了**客户端端的**仅限读取的强制执行。这意味着：
- 在Python代码中禁止修改方法
- 如果调用被禁止的方法，将抛出`PermissionError`错误
- 然而，被修改或受损的客户端可能会绕过这一限制

**为了生产环境的安全：**
1. **使用仅限读取的Odoo用户**（推荐）
2. 不要给API密钥的用户授予修改权限
3. 定期审查Odoo访问日志

**被禁止的方法：**
- `create`、`write`、`unlink`（CRUD操作）
- `copy`（复制记录）
- `action_post`、`action_confirm`、`button_validate`（工作流操作）

**允许的方法（仅限读取）：**
- `search`、`search_read`、`read`（数据检索）
- `search_count`、`fields_get`（元数据）
- `name_search`、`context_get`、`default_get`（辅助函数）

尝试调用被禁止的方法会抛出`PermissionError`错误。

### 数据处理与隐私

- **无数据泄露**：报告在`assets/autonomous-cfo/output/`本地生成 |
- **无数据传输**：不将使用数据发送到外部服务器 |
- **网络隔离**：仅连接到`.env`中指定的`ODOO_URL` |
- **凭证安全**：密码/API密钥从不记录或显示 |
- **本地处理**：所有图表生成和PDF创建都在本地完成

### 输出安全

所有输出都是本地文件：
- `output/pdf_reports/` - PDF报告
- `output/whatsapp_cards/` - PNG图片卡片 |
- `output/charts/` - 图表图像 |
- `output/excel/` - Excel电子表格

没有云上传，没有外部共享，数据不会离开你的机器，只会发送到你指定的Odoo实例。

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

**依赖项：`requests`、`matplotlib`、`pillow`、`fpdf2`、`openpyxl`

## 重要规则

1. **永远不要假设** - 在生成报告之前，一定要询问清楚 |
2. **多公司检查** - 如果存在多个公司，请询问使用哪个公司 |
3. **基于账目** - 使用账户科目表和日记账分录（`account.move.line`），而不仅仅是发票摘要 |
4. **验证时间段** - 运行前请与用户确认日期范围 |
5. **没有默认设置** - 每个假设都必须得到确认 |

## 在生成任何报告之前，请询问：**

1. “我应该使用哪个公司？”（如果有多个公司）
2. “时间段是什么？（开始/结束日期）”
3. “包括哪些账户或账户类型？”
4. “需要特定的细分吗？”（按账户、按合作伙伴、按日记账等）
5. “输出格式偏好是什么？”（PDF、WhatsApp卡片，还是两者都需）

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
- `account.account` - 账户科目表结构（代码、名称、类型、内部组）
- `account.move.line` - 日记账分录行（借方、贷方、账户ID、日期）
- `account.journal` - 来源日记账（类型：销售、采购、现金、银行、普通）

### 账户内部组
- **资产** - 资产（流动资产、非流动资产、现金、应收账款）
- **负债** - 负债（应付账款、税费、应计负债）
- **权益** - 所有者权益
- **收入** - 收入账户
- **费用** - 费用账户
- **资产负债表外项目** - 资产负债表外的账户

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

**对资产负债表至关重要：**
Odoo的`equity_unaffected`是一个暂挂账户。不要直接使用其账目余额。

**正确的权益计算方法：**
1. **正确的权益**（类型：`equity`） - 使用账目余额（贷方 - 借方）
2. **留存收益**（往年） - 来自`equity_unaffected`的账目余额
3. **当年收益** - 实时计算：收入 - 费用

```
Total Equity = Equity Proper + Retained Earnings + Current Year Earnings
```

当年收益 = Σ（收入贷方 - 费用借方）

**为什么这很重要：**Odoo在资产负债表中实时计算当年收益。如果只使用`equity_unaffected`的账目余额，会导致资产负债表不平衡。

## 自动检测报告标准

该技能会根据国家/司法管辖区自动检测公司的会计标准，并相应地格式化报告。

**支持的标准：**
| 标准 | 司法管辖区 | 备注 |
|----------|--------------|-------|
| IFRS | 国际 | 大多数国家的默认标准 |
| US GAAP | 美国 | 在SEC注册的公司 |
| Ind-AS | 印度 | 与IFRS趋同的印度GAAP |
| UK GAAP | 英国 | FRS 102 |
| SOCPA | 沙特阿拉伯 | 采用IFRS |
| EU IFRS | 欧盟 | IAS规定 |
| CAS | 中国 | 中国会计准则 |
| JGAAP | 日本 | 日本GAAP |
| ASPE | 加拿大 | 私营企业 |
| AASB | 澳大利亚 | 澳大利亚标准 |

**检测逻辑：**
1. 从`res.company`中查询公司的国家 |
2. 将国家代码映射到报告标准 |
3. 应用标准特定的格式：
   - 数字格式（1,234.56 vs 1.234,56）
   - 负数显示方式（(123) vs -123）
   - 日期格式（DD/MM/YYYY vs MM/DD/YYYY）
   - 报表标题（资产负债表 vs 财务状况表）
   - 现金流方法（间接法 vs 直接法）

**覆盖设置：**
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

### 预构建的报告

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

对于预构建命令未涵盖的销售/CRM数据，可以使用直接RPC：

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

**报告默认总是包含适当的可视化内容：**

| 报告 | 自动包含的图表 |
|--------|---------------------|
| 财务健康状况 | 现金状况、资金消耗趋势、运营周期 |
| 收入 | 月度趋势、顶级客户、增长KPI |
| 应收账款/应付账款账龄 | 账龄分布饼图、逾期重点 |
| 费用 | 类别细分、趋势、主要供应商 |
| 高管报告 | 所有KPI卡片、汇总图表 |
| 资产负债表 | 资产/负债构成 |
| 损益表 | 收入与费用对比、利润率趋势 |
| 现金流 | 经营费用细分、现金趋势 |

**规则：** 如果可视化能让报告更清晰，就自动包含它们。永远不要问“是否需要图表？”——直接添加即可。

## 交互式参数收集

如果缺少必要的参数，技能会询问：

1. **公司：**“使用哪个公司？”（列出可用选项）
2. **时间段：**“时间段是什么？（例如，‘上个月’、‘2024年第四季度’、自定义日期）”
3. **账户：**“包括哪些账户或账户组？”（例如，‘所有收入’、‘仅银行账户’）
4. **细分：**“按什么分组？（月份、客户、类别、账户）”
5. **输出：**“输出格式是什么？（WhatsApp卡片、PDF、两者都需）”

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

**一般查询：**
- “这个月我们收到了多少订单？”
- “前10位客户是谁？”
- “显示[客户名称]的发票状态”

技能将：
1. 检查是否存在多个公司，并询问使用哪个公司
2. 解析你的请求
3. 询问任何缺失的信息
4. 使用账目分录或直接RPC从Odoo获取数据
5. 生成图表和WhatsApp卡片
6. 通过WhatsApp卡片和/或PDF形式提供

## 硬性规则

1. Odoo RPC输出是最终依据 |
2. 严格限制为仅限读取（禁止创建/写入/删除）
3. 除非被请求，否则不采取主动行动 |
4. 每个数字都附带方法说明 |
5. 在做出任何假设之前，务必与用户确认 |
6. **始终包含可视化内容** - 如果报告可以从图表中受益，就自动包含它们。报告应该视觉上完整。

## 诊断

```bash
python3 ./skills/odoo/assets/autonomous-cfo/src/tools/cfo_cli.py doctor
```

## 报告主题

- **WhatsApp卡片：** “午夜账目” — 海军黑色（#0a0e1a），铜色渐变（#cd7f32）
- **PDF报告：** 清洁的白色背景，铜色点缀，专业布局