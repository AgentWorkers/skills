# 电子表格工程 — AfrexAI

> 构建可靠的电子表格：财务模型、仪表板、数据系统和自动化工具。适用于 Google Sheets、Excel 和 LibreOffice 的跨平台方法论。

## 快速检查

给你的电子表格打分（满分 16 分）：

| 项目 | 合格 | 不合格 |
|---|---|---|
| 为所有关键输入设置命名范围 | ✅ | ❌ |
| 将输入数据与计算结果分开 | ✅ | ❌ |
| 公式中不使用硬编码的数值 | ✅ | ❌ |
| 无循环引用 | ✅ | ❌ |
| 有文档和注释 | ✅ | ❌ |
| 公式中包含错误处理 | ✅ | ❌ |
| 格式统一 | ✅ | ❌ |
| 有版本历史记录和备份 | ✅ | ❌ |
| 对输入数据进行验证 | ✅ | ❌ |

**得分：** 0-4 🔴 需重建 | 5-8 🟡 需重构 | 9-12 🟢 需优化 | 13-16 🔵 可用于生产环境 |

---

## 第 1 阶段：架构与规划

### 电子表格策略简介

```yaml
spreadsheet_brief:
  name: "[Descriptive Name]"
  purpose: "[What decision does this support?]"
  owner: "[Who maintains this]"
  audience: "[Who uses this — technical level]"
  update_frequency: "[Real-time / Daily / Weekly / Monthly / Ad-hoc]"
  data_sources:
    - source: "[Where data comes from]"
      method: "[Manual / Import / API / IMPORTRANGE / Power Query]"
      refresh: "[How often]"
  outputs:
    - "[Dashboard / Report / Export / Decision support]"
  complexity_tier: "[Simple / Standard / Complex / Enterprise]"
  platform: "[Google Sheets / Excel / Both]"
  kill_criteria:
    - "If >50 users need simultaneous editing → move to database"
    - "If >100K rows → move to database or BI tool"
    - "If requires audit trail → move to proper system"
```

### 复杂度分级指南

| 复杂度等级 | 行数 | 工作表数量 | 用户数量 | 公式数量 | 示例 |
|---|---|---|---|---|
| 简单 | <1000 | 1-3 | 1-3 | 基本公式 | 预算追踪表、检查清单 |
| 标准 | 1000-10000 | 3-8 | 3-10 | 中级公式 | 财务模型、项目追踪表 |
| 复杂 | 10000-50000 | 8-15 | 10-30 | 高级公式 | 多部门仪表板、客户关系管理（CRM） |
| 企业级 | >50000 | 15+ | 30+ | 专家级公式 | 数据仓库替代方案（建议迁移） |

### 何时不应使用电子表格

| 情况 | 更适合的工具 |
|---|---|
| 数据行超过 100000 行 | 数据库（如 PostgreSQL、SQLite） |
| 同时有超过 10 个编辑者 | Web 应用程序或 Airtable |
| 数据结构复杂（涉及多个实体类型） | 数据库 + 应用程序 |
| 需要审计追踪/合规性 | 专用系统 |
| 需要实时数据处理 | ETL 流程 + 商业智能（BI）工具 |
| 代码逻辑需要版本控制 | 真正的编程语言（如 Python、JavaScript） |

**规则：** 电子表格是原型设计工具，不应直接用于生产环境。了解何时该升级到更高级的工具。

---

## 第 2 阶段：工作表架构

### 推荐的结构

```
📊 Workbook
├── 📋 README          — Purpose, instructions, changelog
├── 📊 Dashboard       — Charts, KPIs, summary (output only)
├── ⚙️ Config          — Settings, parameters, dropdowns
├── 📥 Data_Input      — Raw data entry or imports
├── 🔧 Calculations    — All formulas and transformations
├── 📈 Analysis        — Pivot tables, scenarios, what-if
├── 📤 Output          — Formatted reports for export/print
└── 🗄️ Reference       — Lookup tables, constants, mappings
```

### 7 条架构规则

1. **数据流向一致** — 数据应从左向右或从上到下流动，避免循环引用。
2. **将输入数据与计算结果分开** — 公式中不要使用硬编码的数值，使用命名范围。
3. **每个数据只对应一个含义** — 如果一个数值在多个地方使用，应定义一次并统一引用。
4. **使用颜色编码** — 蓝色表示输入数据，黑色表示公式结果，绿色表示来自其他工作表的引用，红色表示警告。
5. **冻结工作表的某些区域** — 保证标题行和标签列始终可见。
6. **保护公式单元格** — 除了输入单元格外，锁定所有单元格，防止意外覆盖。
7. **必须要有 README 文件** — 每个工作簿都应包含用途说明、操作指南和版本历史记录。

### 命名规范

```
Sheets:    PascalCase — Dashboard, Raw_Data, Config
Named Ranges: SCREAMING_SNAKE — TAX_RATE, START_DATE, REVENUE_TARGET
Tabs:      Prefix with emoji or number for sort order — 01_Dashboard, 02_Config
Files:     YYYY-MM-DD_Description_vX.xlsx
```

### 颜色编码标准

| 颜色 | 含义 | 使用场景 |
|---|---|---|
| 🔵 浅蓝色背景 | 用户输入的单元格 | 可编辑字段 |
| ⬛ 黑色文本 | 公式计算结果 | 自动填充的单元格 |
| 🟢 绿色文本 | 来自其他工作表的引用 | 跨工作表的链接 |
| 🔴 红色文本/背景 | 警告/错误 | 验证失败或负数 |
| 🟡 黄色背景 | 假设条件 | 影响模型的关键假设 |
| ⬜ 灰色背景 | 参考数据/锁定单元格 | 常量、查找表 |

---

## 第 3 阶段：公式工程

### 公式复杂度等级

| 复杂度等级 | 使用的技术 | 示例 |
|---|---|---|
| L1（基础） | SUM、AVERAGE、COUNT、IF、CONCATENATE | `=SUM(B2:B100)` |
| L2（中级） | VLOOKUP/XLOOKUP、SUMIFS、INDEX/MATCH、TEXT | `=XLOOKUP(A2,Ref!A:A,Ref!B:B)` |
| L3（高级） | ARRAYFORMULA、QUERY、INDIRECT、嵌套 IF | `=QUERY(Data!A:F,"SELECT A,SUM(F) GROUP BY A")` |
| L4（专家级） | LAMBDA、MAP/REDUCE、LET、动态数组、MAKEARRAY | `=LET(data,A2:A100,filtered,FILTER(data,data>0),SORT(filtered))` |

### 常用公式技巧

#### 查找函数 — 建议使用 XLOOKUP/INDEX-MATCH 而不是 VLOOKUP

#### 多条件查找

#### 条件聚合

#### 日期计算

#### 文本处理

#### 动态数组（Excel 365 / Google Sheets）

#### Google Sheets 的 QUERY 功能

#### 使用 LET 使公式更易阅读

#### LAMBDA 函数

### 10 条公式规则

1. **不要硬编码数值** — 使用命名范围或配置文件。
2. **对外部查找使用 IFERROR** — `=IFERROR(XLOOKUP(...), "未找到")`。
3. **长公式使用 LET** — 便于阅读和调试。
4. **优先使用 XLOOKUP** — 更灵活，无需计算列数。
5. **每个单元格只使用一个公式** — 避免嵌套多个函数。
6. **为复杂公式添加注释** — 使用单元格注释或文档说明。
7. **测试极端情况** — 包括空单元格、零值、1900 年之前的日期以及数字字段中的文本。
8. **避免使用 INDIRECT** — 会导致性能下降。
9. **使用结构化引用** — 例如 `=SUM(Table1[Amount])` 而不是 `=SUM(D:D)`。
10. **保持公式可审计** — 其他用户或未来的你能够理解这些公式。

---

## 第 4 阶段：数据验证与质量

### 输入验证检查清单

| 数据类型 | 验证方式 | 实现方法 |
|---|---|---|
| 日期 | 日期范围 | 确保日期在指定范围内 |
| 货币 | 数字 ≥ 0 | 数字格式为 $#,##0.00 |
| 百分比 | 0-100 或 0-1 | 数字范围在 0 到 1 之间 |
| 分类 | 下拉列表 | 从参考工作表中选择 |
| 电子邮件 | 包含 @ | `=ISNUMBER(FIND("@",A2)` |
| 电话号码 | 长度检查 | `=AND(LEN(A2)>=10, LEN(A2)<=15)` |
| 必填字段 | 不为空 | `=LEN(TRIM(A2))>0` |
| ID/代码 | 唯一性检查 | `=AND(COUNTIF(A:A,A2)=1, LEN(A2)=8)` |

### 数据清洗流程

### 条件格式化规则（优先级）

1. 🔴 **错误** — 包含 #REF!、#N/A、#VALUE! 的单元格显示为红色背景。
2. 🟡 **警告** — 超出范围的值显示为黄色背景。
3. 🟢 **正面数据** — 显示为绿色背景。
4. 📊 **数据条形图** — 数值范围用条形图表示。
5. 🎯 **图标** — 用图标显示状态。

---

## 第 5 阶段：财务建模

### 模型架构

### 收入模型示例

### 场景分析模板

### 敏感性分析

### 常用财务公式

---

## 第 6 阶段：仪表板设计

### 仪表板布局

### KPI 卡片公式示例

### 图表选择指南

### 图表类型与适用场景

### 交互式仪表板控制

---

## 第 7 阶段：数据导入与集成

### 导入方法选择

### Google Sheets 的导入功能

### Excel 的 Power Query 功能

---

## 第 8 阶段：自动化与脚本

### Google Apps Script 基础

### Excel VBA 基础

### 自动化决策指南

---

## 第 9 阶段：性能优化

### 性能优化技巧

### 避免的性能问题

### 第 10 阶段：协作与治理

### 访问控制策略

### 版本控制

### 协作规则

### 常见模板

### 维护工作表的质量

### 每月维护检查清单

---

## 边缘案例与技巧

### 数据迁移

### 多货币电子表格

### 大型数据集的处理方法

---

## 自然语言命令

### 常用命令

---

## ⚡ AfrexAI 专业技能包

这些技能涵盖了电子表格工程的方法论。针对特定行业的财务模型、仪表板和模板，提供以下专业包：

- 💰 [**SaaS 专业包**](https://afrexai-cto.github.io/context-packs/) — 月收入（MRR/ARR）模型、SaaS 绩效指标仪表板
- 🏦 [**金融科技专业包**](https://afrexai-cto.github.io/context-packs/) — 金融建模、风险计算器、合规性跟踪工具
- 🏭 [**制造业专业包**](https://afrexai-cto.github.io/context-packs/) — 生产进度跟踪、库存模型、成本分析
- 🏗️ [**建筑行业专业包**](https://afrexai-cto.github.io/context-packs/) — 项目预算、投标计算器、资源规划

**每个专业包售价 47 美元** — 专为你的行业定制的 AI 工具包。

查看所有专业包：[**AfrexAI 商店**](https://afrexai-cto.github.io/context-packs/)

---

## 更多 AfrexAI 提供的免费资源

- [数据可视化与仪表板设计](https://clawhub.com/afrexai-cto/afrexai-data-storytelling)
- [个人财务管理](https://clawhub.com/afrexai-cto/afrexai-personal-finance)
- [产品分析与指标监控](https://clawhub.com/afrexai-cto/afrexai-product-analytics)
- [财务规划与分析](https://clawhub.com/afrexai-cto/afrexai-fpa-engine)
- [工作流程自动化](https://clawhub.com/afrexai-cto/afrexai-automation-strategy)

---

*由 AfrexAI 制作* — 提供智能化的工具和服务。