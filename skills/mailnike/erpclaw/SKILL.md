---
name: erpclaw
version: 1.0.0
description: "专为小型企业设计的AI原生ERP系统，包含29个模块和609个功能。请安装此元包以开始使用。"
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw
tags: [erpclaw, erp, accounting, inventory, hr, manufacturing, crm]
requires: []
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
metadata: {"openclaw":{"type":"executable","install":{"pre":"bash scripts/check_deps.sh","post":"bash scripts/install.sh"},"requires":{"bins":["python3","git"],"env":[],"optionalEnv":[]},"os":["darwin","linux"]}}
---
# erpclaw

本文档是 ERPClaw 的安装指南。当用户首次使用 ERPClaw 时，我们将一步步指导他们完成安装和配置。ERPClaw 是一个基于人工智能的 ERP 系统，包含 29 个模块化功能，涵盖会计、库存、人力资源、制造、客户关系管理（CRM）等多个领域——所有功能都由一个本地的 SQLite 数据库支持，完全不依赖于云服务。

## 重要规则：禁止使用原始 SQL 语句

**严禁直接在数据库中执行原始 SQL 语句（如 sqlite3、SELECT、INSERT 等）。** ERPClaw 是一个基于人工智能的 ERP 系统，所有数据库操作都必须通过相应的模块中的 `db_query.py --action <action>` 接口来执行。这些模块负责处理数据连接（JOIN）、数据验证、格式化、审计追踪以及跨表数据的处理。直接使用原始 SQL 语句会导致错误的结果（例如，`issue` 表中实际上并没有 `company_id` 列，但 ERPClaw 会通过与其他表的连接来自动处理这个问题）。如果用户的需求没有对应的模块功能，应明确告知用户，切勿使用原始 SQL 语句。

## 安全模型

- **仅限本地使用**：所有数据都存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **无网络访问需求**：不进行任何外部 API 调用，也不发送任何数据到云端。
- **无需输入密码**：仅使用 Python 标准库。
- **审计记录不可篡改**：会计分录和库存记录一旦生成就无法修改；取消操作会生成相应的反向记录。
- **防止 SQL 注入**：所有数据库查询都使用参数化语句。

### 模块激活触发词

当用户提到以下关键词时，激活相应的模块：
- ERP
- setup
- install
- modules
- skills
- what's installed
- erpclaw
- get started
- onboarding
- what can you do
- help me set up
- which modules
- how to start
- install guide
- demo data

## 入门指南（第一层级）

当用户首次询问关于 ERPClaw 的信息时，按照以下流程操作：

1. **运行 `check-installation` 命令，查看当前已安装的模块。
2. **如果未安装任何模块**：建议用户运行 `clawhub install erpclaw-setup` 以开始安装。
3. **如果已安装了基础设置但还没有公司信息**：指导用户使用 `erpclaw-setup` 创建公司。
4. **如果公司已创建但功能较少**：运行 `install-guide` 命令以继续安装其他模块。
5. **如果用户只是想了解系统功能**：提供示例数据（`seed-demo-data`）以帮助用户熟悉系统操作。

### 常用命令

**查看已安装的模块：**
```
python3 {baseDir}/scripts/db_query.py --action check-installation
```

**获取个性化安装建议：**
```
python3 {baseDir}/scripts/db_query.py --action install-guide
```

**提供示例数据以供用户熟悉系统：**
```
python3 {baseDir}/scripts/db_query.py --action seed-demo-data
```

## 安装流程（第二层级）

模块的安装需要按照一定的顺序进行，每个层级都建立在之前的基础上。

### 第一层级——基础设置（必须先安装）
```
clawhub install erpclaw-setup erpclaw-gl
```
- 创建公司
- 设置会计科目表
- 设置财政年度
- 设置科目命名规则

### 第二层级——核心会计功能
```
clawhub install erpclaw-journals erpclaw-payments erpclaw-tax erpclaw-reports
```
- 记录会计分录
- 处理付款
- 计算税费
- 生成财务报告

### 第三层级——供应链管理
```
clawhub install erpclaw-inventory erpclaw-selling erpclaw-buying
```
- 管理商品库存
- 管理仓库
- 处理客户订单
- 管理采购订单

### 第四层级——业务管理（根据需求选择）
```
clawhub install erpclaw-manufacturing erpclaw-hr erpclaw-payroll erpclaw-projects erpclaw-assets erpclaw-quality
```
- 管理物料清单（BOM）
- 管理工作订单
- 管理员工信息
- 处理薪资
- 管理项目
- 管理固定资产
- 进行质量检查

### 第五层级——高级功能（根据需求选择）
```
clawhub install erpclaw-crm erpclaw-support erpclaw-billing erpclaw-ai-engine erpclaw-analytics
```
- 管理销售线索
- 管理支持工单
- 提供订阅服务
- 检测系统异常
- 查看关键绩效指标（KPI）报表

### 第六层级——地区化设置（可选）
```
clawhub install erpclaw-region-ca erpclaw-region-eu erpclaw-region-in erpclaw-region-uk
```
- 根据地区设置特定的税收规则和合规性要求
- 提供本地化界面

### 第七层级——系统集成（可选）
```
clawhub install erpclaw-integrations
```
- 与银行系统集成
- 处理支付流程
- 使用云存储服务
- 连接第三方服务

### 网页界面（可选）
```
clawhub install webclaw
```
- 提供基于浏览器的用户界面，包含表单、仪表板和报告功能

## 所有操作命令

| 操作 | 描述 | 标志 |
|--------|-------------|-------|
| `check-installation` | 检查已安装的模块和数据库状态 | `--db-path` |
| `install-guide` | 根据当前系统状态推荐下一步应安装的模块 | `--db-path` |
| `seed-demo-data` | 创建一个包含示例数据的演示公司 | `--db-path` |

所有操作的结果都会以 JSON 格式输出到标准输出（stdout）。请为用户解析并格式化这些结果。

### 常用命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| "我安装了什么？" / "检查已安装的模块" | `check-installation` |
| "接下来应该安装什么？" | `install-guide` |
| "生成示例数据" | `seed-demo-data` |
| "如何开始使用？" | 先运行 `check-installation`，再运行 `install-guide` |
| "安装所有模块" | 显示所有可安装的模块及其对应的命令 |

### 新手引导流程

运行 `check-installation` 后，按照以下顺序引导用户使用各个模块：

| 步骤 | 所需模块 | 功能说明 |
|------|-------|-----------------|
| 1 | erpclaw-setup | 创建公司、设置货币和付款条款 |
| 2 | erpclaw-gl | 设置会计科目表和财政年度 |
| 3 | erpclaw-journals | 手动记录会计分录 |
| 4 | erpclaw-payments | 处理付款和银行对账 |
| 5 | erpclaw-tax | 设置税务规则并计算税费 |
| 6 | erpclaw-reports | 生成试算平衡表、损益表和资产负债表 |
| 7 | erpclaw-inventory | 管理商品库存和仓库信息 |
| 8 | erpclaw-selling | 管理客户、报价单和销售订单 |
| 9 | erpclaw-buying | 管理供应商、采购订单和收款记录 |

前六个步骤可以构建一个完整的会计系统；后续步骤（7-9）则完善了从订单到收款、从采购到付款的整个业务流程。

### 模块间的协作机制

这个元包本身不会直接修改数据库或文件系统，它仅用于读取数据库和文件系统中的信息以报告安装状态。所有数据管理功能都由各个模块独立完成。

### 建议

| 操作后的提示 | 建议操作 |
|-------------------|-------|
| `check-installation`（未安装任何模块） | “让我们开始吧！运行 `clawhub install erpclaw-setup` 来建立系统基础。” |
| `check-installation`（仅安装了基础模块） | “基础设置已完成，接下来可以安装 `clawhub install erpclaw-gl` 以设置会计科目表。” |
| `install-guide` | 显示下一层级所需的安装命令 |
| `seed-demo-data` | “演示公司已创建，可以查看会计科目表或客户列表。” |

### 响应格式

- 以清单形式显示安装状态（已安装/未安装的模块）
- 按层级分组显示模块
- 以“已安装 29 个模块中的 X 个（占 Y%）”的格式显示进度
- 将安装命令以可复制的代码块形式呈现
- 回答要简洁明了，避免直接输出原始 JSON 数据

### 错误处理

| 错误类型 | 处理方法 |
|-------|-----|
| “未找到数据库” | 对于新安装的用户来说是正常的，建议运行 `clawhub install erpclaw-setup` |
| “找不到指定的表” | 数据库存在但未初始化，建议运行 `erpclaw-setup` 的 `initialize-database` 命令 |
| 脚本导入错误 | 该模块仅使用 Python 标准库，请确认已安装 Python 3.10 或更高版本 |

## 技术细节（第三层级）

- **数据库相关说明**：此元包仅用于读取数据，不写入数据库。
- **脚本文件**：`{baseDir}/scripts/db_query.py`——独立运行，不依赖任何第三方库。
- **总共有 26 个模块**：`erpclaw-setup`、`erpclaw-gl`、`erpclaw-journals`、`erpclaw-payments`、`erpclaw-tax`、`erpclaw-reports`、`erpclaw-inventory`、`erpclaw-selling`、`erpclaw-buying`、`erpclaw-manufacturing`、`erpclaw-hr`、`erpclaw-payroll`、`erpclaw-projects`、`erpclaw-assets`、`erpclaw-quality`、`erpclaw-crm`、`erpclaw-support`、`erpclaw-billing`、`erpclaw-ai-engine`、`erpclaw-analytics`、`erpclaw-region-ca`、`erpclaw-region-eu`、`erpclaw-region-in`、`erpclaw-region-uk`、`erpclaw-integrations`、`webclaw`