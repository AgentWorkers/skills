---
name: phoenixclaw-ledger
description: |
  Passive financial tracking plugin for PhoenixClaw.
  Automatically detects expenses and income from conversations and payment screenshots.
  
  Use when:
  - User mentions money/spending (any language)
  - User shares payment screenshots (WeChat Pay, Alipay, etc.)
  - User asks about finances ("How much did I spend?", "My budget")
  - User wants expense reports ("Monthly summary", "Spending analysis")

metadata:
  version: 0.1.0

depends: phoenixclaw
protocol_version: 1
min_core_version: 0.0.3
hook_point: post-moment-analysis
data_access:
  - moments
  - user_config
  - memory
export_to_journal: true
---

# PhoenixClaw Ledger：零努力的财务追踪工具

PhoenixClaw Ledger能够自动从您的日常对话和支付截图中提取财务交易信息，完全无需手动输入。

## 核心功能

| 功能 | 描述 |
|---------|-------------|
| **语义化费用检测** | 人工智能识别对话中的支出相关内容 |
| **截图识别** | 从支付应用截图中提取交易数据 |
| **智能分类** | 根据商家和上下文自动分类交易 |
| **预算追踪** | 提供每月预算提醒和进度可视化 |
| **财务洞察** | 将数据分析整合到财务记录中 |
| **目标管理** | 支持储蓄、预算控制、习惯养成和愿望清单管理 |
| **每周报告** | 每周日晚9点自动生成支出汇总 |
| **查询支持** | 支持实时财务查询 |
| **支出趋势分析** | 提供多个月的支出数据分析 |
| **交易浏览** | 提供交互式的完整交易历史视图 |

## 工作流程

作为PhoenixClaw的一个插件，Ledger在`post-moment-analysis`阶段执行以下操作：

1. **接收数据**：从PhoenixClaw Core获取相关数据。
2. **检测财务信息**：在文本和媒体内容中查找支出/收入相关的线索：
   - 文本：利用语义分析技术（详见`references/expense-detection.md`）
   - 媒体：从支付截图中提取信息（详见`references/payment-screenshot.md`）
3. **提取数据**：解析交易金额、商家名称和类别、时间戳。
4. **分类**：根据`references/merchant-category-map.md`中的规则对交易进行分类。
5. **去重**：避免重复记录同一笔交易。
6. **存储数据**：将数据写入`~/PhoenixClaw/Finance/ledger.yaml`文件。
7. **生成报告**：使用`assets/daily-finance-section.md`模板生成财务记录。

## 显式触发指令

虽然该工具默认为被动模式，但用户也可以直接进行交互：

- “我今天/这周/这个月花了多少钱？”
- “显示我的支出明细”
- “将我的月度预算设置为[金额]”
- “我的主要支出类别是什么？”
- “生成[时间段]的财务报告”
- “设定[金额]的储蓄目标，截止日期为[日期]”
- “查看我的支出趋势”
- “浏览我的所有交易记录”
- “我的目标完成情况如何？”

## 输出结构

```
~/PhoenixClaw/
├── Journal/
│   ├── daily/2026-02-02.md    # Contains 💰 Finance section
│   └── weekly/2026-W05.md     # Weekly financial recaps
│
└── Finance/                    # Ledger-specific directory
    ├── ledger.yaml             # Structured transaction data
    ├── budget.yaml             # Budget configuration
    ├── goals.yaml              # Financial goals tracking
    ├── transactions.md         # Transaction browser view
    ├── monthly/
    │   └── 2026-02.md          # Monthly financial reports
    └── yearly/
        └── 2026.md             # Annual summaries
```

## 配置

Ledger的特定配置文件位于`~/.phoenixclaw/config.yaml`中：

```yaml
plugins:
  phoenixclaw-ledger:
    enabled: true
    default_currency: CNY       # or USD, EUR, etc.
    budget_monthly: 5000        # Monthly budget amount
    categories_custom: []       # User-defined categories
    screenshot_confidence: 0.7  # Min confidence for auto-record
```

## 定时任务与报告生成

Ledger利用PhoenixClaw Core的定时任务机制来执行以下操作：

| 任务 | 时间安排 | 描述 |
|------|----------|-------------|
| **每日处理** | 每晚10点 | 提取交易数据并生成每日财务记录 |
| **月度报告** | 每月1日早上8点 | 生成全面的月度财务总结 |
| **每周总结** | 每周日晚9点（可选） | 提供每周支出汇总 |

### 日常处理（自动执行）

无需额外设置。Ledger会自动连接到PhoenixClaw Core的夜间定时任务：
- PhoenixClaw Core在每晚10点运行，触发`post-moment-analysis`流程。
- Ledger随后开始处理数据并生成每日财务记录。

### 月度报告设置

详细配置信息请参阅`references/cron-setup.md`。

## 文档参考

### 参考资料（`references/`）

- `expense-detection.md`：用于对话内容解析的语义分析规则
- `payment-screenshot.md`：截图识别和OCR提取技术
- `merchant-category-map.md`：商家与类别的映射规则
- `category-rules.md`：类别定义和分类结构
- `budget-tracking.md`：预算提醒和进度计算方法
- `financial-insights.md`：财务数据分析模板
- `cron-setup.md`：定时任务和报告自动化设置
- `goal-management.md`：财务目标管理和进度跟踪功能
- `query-patterns.md`：自然语言查询模板和逻辑实现

### 资源文件（`assets/`）

- `expense-callout.md`：用于记录对话中检测到的支出的模板
- `receipt-callout.md`：用于记录截图中检测到的支出的模板
- `daily-finance-section.md`：用于整合财务记录的模板
- `monthly-report.md`：月度财务总结模板
- `yearly-report.md`：年度财务总结模板

---