---
name: odoo
description: 全功能的 Odoo 19 ERP 连接器，适用于 OpenClaw：支持销售、客户关系管理（CRM）、采购、库存、项目管理、人力资源（HR）、车队管理以及制造流程（涵盖 80 多个业务模块），附带完整的 Python 代码以及 XML-RPC 集成功能。
repository: https://github.com/NullNaveen/openclaw-odoo-skill
---

# Odoo ERP连接器

这是一个功能齐全的Odoo 19 ERP集成插件，专为OpenClaw设计，允许您通过自然语言聊天命令来管理整个业务。

**📦 完整源代码：** https://github.com/NullNaveen/openclaw-odoo-skill

## 快速安装

```bash
npx clawhub install odoo-erp-connector
```

## 概述

Odoo ERP连接器将OpenClaw与Odoo 19连接起来，支持对153个以上的业务模块进行自主的、基于聊天的控制，包括：
- 销售与客户关系管理（Sales & CRM）
- 采购与库存（Purchasing & Inventory）
- 开票与会计（Invoicing & Accounting）
- 项目与任务管理（Projects & Task Management）
- 人力资源（Human Resources）
- 车队管理（Fleet Management）
- 制造（Manufacturing）
- 日历与事件（Calendar & Events）
- 电子商务（E-commerce）

所有操作都使用**智能动作（Smart Actions）**，这些动作能够处理模糊匹配和自动创建工作流程。

## 功能

### 销售与客户关系管理（Sales & CRM）
- 创建包含动态商品项的报价单
- 管理销售订单（草稿 → 确认 → 完成）
- 按状态、客户或日期范围搜索和过滤订单
- 创建和评估潜在客户（leads）和销售机会（opportunities）
- 将潜在客户推进CRM流程阶段
- 查看完整的销售流程并预测收入

### 采购（Purchasing）
- 从供应商处创建采购订单
- 管理采购订单的状态（草稿 → 购买 → 已接收）
- 接收并验证货物
- 按供应商、状态或日期搜索和过滤采购订单
- 跟踪采购历史和供应商表现

### 库存与产品（Inventory & Products）
- 创建产品（消耗品、可库存产品、服务）
- 查询库存水平和可用性
- 设置重新订购点并接收库存不足警报
- 按名称、代码或类别搜索产品
- 跟踪库存变动和估值

### 开票与会计（Invoicing & Accounting）
- 创建并向客户开具发票
- 管理付款条款和计划
- 查询未支付和逾期的发票
- 按客户、日期范围或金额搜索
- 跟踪发票状态（草稿 → 已开具 → 已支付）

### 项目与任务（Projects & Tasks）
- 创建项目并按团队/状态组织
- 创建带有优先级、日期和分配的任务
- 记录工时表并跟踪项目工作时间
- 按项目、状态或分配者搜索和过滤任务
- 管理项目阶段和项目关闭

### 人力资源（Human Resources）
- 创建员工和部门
- 管理职位和工作时间表
- 处理费用报告和报销
- 按名称、部门或职位搜索员工
- 跟踪休假申请和出勤情况

### 车队管理（Fleet Management）
- 创建和跟踪车辆
- 记录里程表读数和服务记录
- 跟踪维护计划和成本
- 按车牌号、状态或品牌搜索车队
- 生成车队报告

### 制造（Manufacturing）
- 创建物料清单（Bills of Materials, BOM）
- 管理制造订单（Manufacturing Orders, MOs）
- 跟踪组件需求和生产状态
- 按产品或状态搜索制造订单
- 将物料清单（BOM）与产品变体关联

### 日历与事件（Calendar & Events）
- 创建带有参与者的会议和事件
- 设置提醒和地点
- 按日期范围或参与者搜索事件
- 跟踪日历可用性

### 电子商务（E-commerce）
- 将产品发布到网站
- 查看网站订单和客户活动
- 管理产品可见性和定价

## 命令示例

### 销售（Sales）
- “为Acme Corp创建一份包含10个单价为50美元的Widget的报价单”
- “确认销售订单SO00042”
- “显示过去一周的所有草稿报价单”
- “本月已完成订单的总收入是多少？”
- “为Rocky创建一份包含产品Rock的报价单”

### 客户关系管理（CRM）
- “为Rocky创建一个潜在客户，电子邮件地址rocky@example.com，潜在价值5万美元”
- “将潜在客户#47推进到‘已评估’阶段”
- “显示所有未完成的销售机会”
- “哪些潜在客户处于提案阶段？”

### 采购（Purchasing）
- “为供应商ABC创建一份包含500个Widget的采购订单”
- “确认采购订单PO00123”
- “显示所有待处理的采购订单”
- “获取供应商ABC的采购历史记录”
- “哪些订单已经逾期？”

### 库存与产品（Inventory & Products）
- “创建一个新产品：TestWidget，价格25美元，最低库存10个”
- “显示库存低于20个的单位”
- “Widget X的库存水平是多少？”
- “搜索所有消耗品”
- “将产品Y的重新订购点设置为50个单位”

### 开票与会计（Invoicing & Accounting）
- “为Acme Corp创建一份包含5个单价为50美元的Widget的发票”
- “显示未支付的发票”
- “哪些发票已经逾期？”
- “发布发票INV-001”
- “为发票INV-002发送提醒”

### 项目与任务（Projects & Tasks）
- “创建一个名为‘Website Redesign’的项目”
- “在‘Website Redesign’项目中创建一个名为‘Fix login button’的任务”
- “显示分配给我的所有任务”
- “记录任务#42的3小时工作时间”
- “‘Website Redesign’项目的状态是什么？”

### 人力资源（HR）
- “创建员工John Smith和部门Engineering”
- “创建部门Engineering”
- “显示Engineering部门的所有员工”
- “提交费用报告，金额为45.99美元”
- “有哪些待处理的休假申请？”

### 车队管理（Fleet Management）
- “创建一辆名为Tesla Model 3的车辆，并记录里程表读数：50,000英里”
- “记录车辆#1的服务记录”
- “显示所有需要维护的车辆”
- “这个月的维护成本是多少？”
- “搜索蓝色车辆”

### 制造（Manufacturing）
- “创建物料清单（BOM）：Widget包含3个Component A和2个Component B”
- “创建制造订单（MO）：生产50个Widget”
- “确认制造订单#1”
- “制造订单#1的状态是什么？”
- “显示所有进行中的制造订单”

### 日历（Calendar）
- “创建一个名为‘Team Standup’的会议，明天上午10点，持续1小时”
- “显示我下周的会议”
- “我在15号有哪些事件？”
- “安排一个与团队进行的2小时规划会议”

### 电子商务（E-commerce）
- “将产品Widget X发布到网站”
- “查看本周的网站订单”
- “我的网站收入是多少？”

## 智能动作（Smart Actions）

该连接器使用智能的查找或创建逻辑来处理模糊/不完整的请求。

### 智能动作的工作原理

**示例：“为Rocky创建一份包含产品Rock的报价单”**

系统：
1. **搜索**名为“Rocky”的客户（不区分大小写，使用`ilike`匹配）
2. **如果未找到**：创建一个新的客户“Rocky”（自动设置为公司）
3. **搜索**产品“Rock”
4. **如果未找到**：创建一个基本的产品“Rock”（消耗品类型，默认价格为0美元）
5. **创建**报价单，并将找到的/创建的客户和产品关联起来
6. **报告**找到的内容与创建的内容：
   - “为新客户Rocky创建了报价单QT-001，包含1个单价为0美元的Rock”

这种模式适用于所有智能动作：
- `smart_create_quotation()` — 客户 + 产品
- `smart_create_purchase()` — 供应商 + 产品
- `smart_create_lead()` — 潜在客户（可选）
- `smart_create_task()` — 项目 + 任务
- `smart_create_employee()` — 员工
- `smart_create_event()` — 事件（无依赖关系）

### 优势

- **模糊匹配**：搜索不区分大小写且具有容错性
- **自动创建**：缺失的依赖关系会自动创建
- **透明度**：每个响应都会说明创建了什么或找到了什么
- **无需ID**：使用名称而不是Odoo ID
- **批量操作**：一次调用可以创建多个相关记录

## 架构

### 核心组件

**OdooClient** — 低级别的XML-RPC封装层
- 连接到Odoo 19实例
- 通过API密钥处理身份验证
- 提供`search()`, `read()`, `create()`, `write()`, `unlink()`方法
- 内置重试逻辑和错误处理

**模型操作类（Model Ops Classes）** — 每个模块的业务逻辑
- `PartnerOps` — 客户/供应商
- `SaleOrderOps` — 报价单和销售订单
- `InvoiceOps` — 客户发票
- `InventoryOps` — 产品和库存
- `CRMOps` — 潜在客户和销售机会
- `PurchaseOrderOps` — 采购订单和供应商
- `ProjectOps` — 项目和任务
- `HROps` — 员工、部门和费用
- `ManufacturingOps` — 物料清单和制造订单
- `CalendarOps` — 事件和会议
- `FleetOps` — 车辆和里程表
- `EcommerceOps` — 网站订单和产品

**SmartActionHandler** — 高级别的自然语言接口
- 封装所有操作类
- 实现查找或创建工作流程
- 模糊名称匹配（不区分大小写）
- 多步骤事务协调
- 详细的响应摘要

### 字段处理

连接器自动检测Odoo 19中必需和可选的字段：
- **隐式默认值**：具有Odoo默认值的字段将被省略
- **智能创建**：为可选字段自动填充合理的默认值
- **错误报告**：缺失的必需字段会引发明确的`OdooError`，并显示字段名称

## 配置

### config.json格式

```json
{
  "url": "http://localhost:8069",
  "db": "your_database",
  "username": "api_user@yourcompany.com",
  "api_key": "your_api_key_from_odoo_preferences",
  "timeout": 60,
  "max_retries": 3,
  "poll_interval": 60,
  "log_level": "INFO",
  "webhook_port": 8070,
  "webhook_secret": ""
}
```

### 获取API密钥

1. 登录到您的Odoo实例
2. 转到**设置** → **用户与公司** → **用户**
3. 打开您的用户记录
4. 滚动到**访问令牌**
5. 点击**生成令牌**
6. 复制令牌并粘贴到`config.json`中

### 环境变量

或者，您也可以在`.env`文件中设置：

```
ODOO_URL=http://localhost:8069
ODOO_DB=your_database
ODOO_USERNAME=api_user@yourcompany.com
ODOO_API_KEY=your_api_key
```

如果`config.json`缺失，客户端会自动从`.env`中加载配置。

## Python API

### 基本用法

```python
from odoo_skill import OdooClient, SmartActionHandler

# Load config from config.json
client = OdooClient.from_config("config.json")

# Test connection
status = client.test_connection()
print(f"Connected to Odoo {status['server_version']}")

# Use smart actions for natural workflows
smart = SmartActionHandler(client)

# Create a quotation with fuzzy partner and product matching
result = smart.smart_create_quotation(
    customer_name="Rocky",
    product_lines=[
        {"name": "Rock", "quantity": 5, "price_unit": 19.99}
    ],
    notes="Fuzzy match quotation"
)

print(result["summary"])
# Output: "Created quotation QT-001 for new customer Rocky with 1 × Rock at $19.99"
```

### 智能动作API

```python
# Find-or-create a customer
result = smart.find_or_create_partner(
    name="Acme Corp",
    is_company=True,
    city="New York"
)
partner = result["partner"]
created = result["created"]

# Find-or-create a product
result = smart.find_or_create_product(
    name="Widget X",
    list_price=49.99,
    type="consu"
)
product = result["product"]

# Smart quotation (auto-creates customer & products)
result = smart.smart_create_quotation(
    customer_name="Rocky",
    product_lines=[
        {"name": "Product A", "quantity": 10},
        {"name": "Product B", "quantity": 5, "price_unit": 25.0}
    ],
    notes="Created via smart action"
)
order = result["order"]
print(f"Order {order['name']} created with {len(result['products'])} product(s)")

# Smart lead creation
result = smart.smart_create_lead(
    name="New Prospect",
    contact_name="John Doe",
    email="john@prospect.com",
    expected_revenue=50000.0
)
lead = result["lead"]

# Smart task creation (auto-creates project if needed)
result = smart.smart_create_task(
    project_name="Website Redesign",
    task_name="Fix homepage",
    description="Update hero section"
)
task = result["task"]

# Smart employee creation (auto-creates department if needed)
result = smart.smart_create_employee(
    name="Jane Smith",
    job_title="Developer",
    department_name="Engineering"
)
employee = result["employee"]
```

### 低级别操作API

```python
from odoo_skill.models.sale_order import SaleOrderOps
from odoo_skill.models.partner import PartnerOps

partners = PartnerOps(client)
sales = SaleOrderOps(client)

# Get all customers
customers = partners.search_customers(limit=10)
for cust in customers:
    print(f"{cust['name']} — {cust.get('email')}")

# Create a quotation with specific IDs
order = sales.create_quotation(
    partner_id=42,
    lines=[
        {"product_id": 7, "quantity": 10, "price_unit": 49.99},
        {"product_id": 8, "quantity": 5}
    ],
    notes="Manual order"
)
print(f"Created {order['name']}")

# Confirm the order
confirmed = sales.confirm_order(order['id'])
print(f"Order {confirmed['name']} is now {confirmed['state']}")
```

## 响应格式

所有API方法返回结构化的字典：

### 智能动作响应

```python
{
  "summary": "Created quotation QT-001 for new customer Rocky with 1 × Rock",
  "order": {
    "id": 1,
    "name": "QT-001",
    "state": "draft",
    "partner_id": [42, "Rocky"],
    "amount_total": 19.99
  },
  "customer": {
    "created": True,
    "partner": {"id": 42, "name": "Rocky"}
  },
  "products": [
    {
      "created": True,
      "product": {"id": 7, "name": "Rock"}
    }
  ]
}
```

### 标准响应

```python
{
  "id": 1,
  "name": "QT-001",
  "state": "draft",
  "partner_id": [42, "Rocky"],
  "amount_total": 19.99,
  "order_line": [
    {
      "id": 1,
      "product_id": [7, "Rock"],
      "quantity": 1,
      "price_unit": 19.99,
      "price_subtotal": 19.99
    }
  ]
}
```

## 错误处理

连接器使用自定义异常：

```python
from odoo_skill.errors import OdooError, OdooAuthError, OdooNotFoundError

try:
    result = smart.smart_create_quotation(
        customer_name="Acme",
        product_lines=[{"name": "Widget"}]
    )
except OdooAuthError as e:
    print(f"Authentication failed: {e}")
except OdooNotFoundError as e:
    print(f"Record not found: {e}")
except OdooError as e:
    print(f"Odoo error: {e}")
```

## 支持的Odoo模块

该连接器支持Odoo 19中安装的153个以上模块：

**核心模块（Core Modules）**
- base, web, website

**销售与客户关系管理（Sales & CRM）**
- sale, crm, sale_management, website_sale, event, survey

**采购（Purchasing）**
- purchase, purchase_stock, purchase_requisition

**库存（Inventory）**
- stock, stock_intrastat, stock_dropshipping

**会计（Accounting）**
- account, account_accountant, account_analytic, account_payment

**人力资源（HR）**
- hr, hr_attendance, hr_expense, hr_contract, hr_holidays, hr_org_chart

**项目（Projects）**
- project, project_enterprise, task_base, project_timesheet_forecast

**制造（Manufacturing）**
- mrp, mrp_byproduct, quality, batch, shelf_life

**车队（Fleet）**
- fleet, maintenance

**市场营销（Marketing）**
- marketing_automation, email_marketing, mass_mailing, sms, website_form

**电子商务（E-commerce）**
- website_sale, website_sale_analytics, website_sale_comparison, website_form_project

**工具（Tools）**
- calendar, documents, spreadsheet, discuss, mail, knowledge

**还有50多个专业模块（Plus 50+ specialized modules）**

## 限制与约束

- **搜索限制**：默认为100条记录（可配置）
- **超时**：每次请求60秒（可配置）
- **重试**：网络失败时自动重试3次
- **并发**：单线程；必要时排队请求
- **速率限制**：遵循您的Odoo实例的API限制

## 故障排除

### 连接问题
- 验证`config.json`中的`url`, `db`, `username`, `api_key`
- 检查Odoo服务器是否运行：`http://your-odoo-url/web`
- 确保在Odoo用户设置中生成了API密钥
- 检查网络连接和防火墙规则

### 身份验证错误
- 在Odoo中重新生成API密钥
- 验证用户名（电子邮件格式）
- 确保用户启用了API访问权限
- 确保数据库名称完全匹配

### 缺少字段错误
- 字段名称必须与Odoo 19中的完全匹配（例如，`product_tmpl_id`，而不是`product_id`）
- 一些字段在Odoo中是只读的（状态、计算字段）
- 检查Odoo模型定义：设置 → 技术 → 数据库结构 → 模型

### 智能动作问题
- 模糊匹配不区分大小写，但只搜索`name`字段
- 对于精确匹配，请使用低级别的操作API并直接使用`id`
- 如果一个名称存在于多个记录中，将使用第一个匹配项

### 性能
- 大规模搜索（超过100条记录）可能会超时
- 使用日期范围过滤器：`date_from`, `date_to`
- 考虑使用批量操作处理大量数据

## OpenClaw中的示例

### 自然语言销售订单（Natural Language Sales Order）

```
User: "Create a quote for Acme Corp with 10 Widgets at $50 each"

OpenClaw → OdooClient (smart action):
  1. Search for customer "Acme Corp"
  2. Search for product "Widgets"
  3. Create quotation with both
  4. Return summary

Result: "✅ Created quotation QT-001 for Acme Corp with 10 × Widgets at $50"
```

### 流程状态检查（Pipeline Status Check）

```
User: "Show me the sales pipeline"

OpenClaw → CRMOps.get_pipeline():
  - Query all leads/opportunities
  - Group by stage
  - Calculate total revenue by stage
  - Return formatted summary

Result: "Qualified: $50k | Proposal: $100k | Negotiation: $75k | Total: $225k"
```

### 库存警报（Inventory Alert）

```
User: "What products are low on stock?"

OpenClaw → InventoryOps.get_low_stock_products():
  - Query products with stock < reorder point
  - List each product, stock level, reorder point
  - Suggest PO quantities

Result: "Widget X: 5 on hand (min 20) | Component Y: 0 on hand (min 10)"
```

## 开发（Development）

### 项目结构（Project Structure）

```
OdooConnector/
├── odoo_skill/
│   ├── client.py              # Core OdooClient
│   ├── config.py              # Configuration loader
│   ├── errors.py              # Custom exceptions
│   ├── retry.py               # Retry logic
│   ├── smart_actions.py       # Smart action handler
│   ├── models/
│   │   ├── partner.py
│   │   ├── sale_order.py
│   │   ├── invoice.py
│   │   ├── inventory.py
│   │   ├── crm.py
│   │   ├── purchase.py
│   │   ├── project.py
│   │   ├── hr.py
│   │   ├── manufacturing.py
│   │   ├── calendar_ops.py
│   │   ├── fleet.py
│   │   ├── ecommerce.py
│   ├── utils/
│   │   ├── formatting.py      # Response formatting
│   │   ├── validators.py      # Input validation
│   ├── sync/
│   │   ├── poller.py          # Webhook poller
│   │   ├── webhook.py         # Webhook handler
├── run_full_test.py           # Integration test suite
├── config.json                # Configuration (create from template)
├── config.template.json       # Configuration template
├── requirements.txt           # Python dependencies
├── README.md                  # User setup guide
├── SKILL.md                   # This file
└── setup.ps1                  # PowerShell installer
```

### 运行测试（Running Tests）

```bash
# Run full integration test suite
python run_full_test.py

# Run single test module
python -m pytest tests/test_partners.py -v

# Run with coverage
python -m pytest --cov=odoo_skill tests/
```

### 添加新的智能动作（Adding a New Smart Action）

1. 在`SmartActionHandler`类中实现该方法
2. 使用`find_or_create_*`方法处理依赖关系
3. 返回一个包含`summary`、主要记录和创建详情的字典
4. 添加带有示例用法的文档字符串
5. 使用`run_full_test.py`进行测试

示例：

```python
def smart_create_invoice(self, customer_name: str, product_lines: list[dict], **kwargs) -> dict:
    """Create invoice with fuzzy customer and product matching."""
    # Find or create customer
    customer_result = self.find_or_create_partner(customer_name)
    customer = customer_result["partner"]
    
    # Find or create products
    products = []
    for line in product_lines:
        prod_result = self.find_or_create_product(line["name"], **line)
        products.append(prod_result)
    
    # Create invoice with resolved IDs
    invoice = self.invoices.create_invoice(
        partner_id=customer["id"],
        lines=[...],
        **kwargs
    )
    
    return {
        "summary": f"Created invoice INV-001 for {customer['name']}",
        "invoice": invoice,
        "customer": customer_result,
        "products": products
    }
```

## 许可证与支持（License & Support）

此连接器是OpenClaw项目的一部分。如有问题、疑问或贡献，请联系开发团队。

---

**最后更新时间：** 2026-02-09  
**Odoo版本：** 19.0  
**Python版本：** 3.10+  
**状态：** 已准备好投入生产