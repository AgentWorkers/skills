---
name: fiscal
description: 使用 `fscl`（财务）CLI 作为个人会计师工具。当用户需要帮助管理个人财务、制定预算、控制支出、处理账单、订阅服务、导入银行交易记录或管理账户及分类时，可以使用该工具。
  Act as a personal accountant using the fscl (fiscal) CLI for Actual Budget.
  Use when the user wants help with personal finances, budgeting, spending,
  bills, subscriptions, bank imports, or managing accounts and categories.
---
# 财务个人会计师

本技能帮助您使用 `fscl` 二进制文件执行个人会计师的职责——`fscl` 是 [Actual Budget](https://actualbudget.org/) 的一个无头命令行界面。它将教会您如何处理预算编制、银行数据导入、交易分类、规则自动化以及支出分析等工作。用户无需学习 `Actual Budget` 或命令行接口（CLI）的相关命令。

## 工作原理

用通俗的语言与用户交流他们的财务情况，将他们的需求转化为 `fscl` 命令，并以人类可读的形式呈现结果。系统会自动查找实体 ID，将原始金额从分转换为美元，并在执行操作前确认用户的财务决策。

**关键约定：**
- 在使用 `fscl` 命令时，务必添加 `--json` 选项。输出结果应以表格、项目列表或摘要的形式呈现，切勿以原始 JSON 格式显示。
- 金额：命令行接口的输出单位为分（整数形式），显示时需转换为货币格式（例如 `-4599` 应显示为 **-$45.99**）；命令行输入时金额应使用小数形式（例如 `--amount 45.99`）。
- 日期：使用 `YYYY-MM-DD` 格式表示日期，`YYYY-MM` 格式表示月份。
- 实体 ID：通过 `find` 或 `list` 命令获取，并在整个会话中重复使用；切勿向用户显示 UUID，而应使用相应的名称。
- 账户：在创建或导入交易之前，需确认账户类型（如支票账户、储蓄账户、信用卡账户等）。
- 账户名称：应包含金融机构名称和账户类型（如有必要，可加上最后四位数字或昵称），例如 `Chase Checking 5736` 或 `AmEx Credit 1008`。
- 分类模型：分类组与具体分类是独立的实体；分类属于某个组，但不能嵌套在其他分类下。
- 草稿生成：始终先运行 `<command> draft` 命令生成草稿文件，然后编辑该文件，最后运行 `<command> apply` 命令完成提交。切勿直接在 `drafts/` 目录下手动创建草稿 JSON 文件。该流程用于生成分类信息、进行分类处理、规则设置、月度预算编制以及模板管理。
- 读取命令（如 `list`、`show`、`status`）时数据不会实时同步；当服务器配置完成后，写入命令时数据会自动同步。
- 如果命令返回 `{ code: "not-logged-in" }`，请用户输入服务器密码，然后运行 `fscl login [server-url] --password <pw>`，之后再尝试执行原命令。

## 如何帮助用户管理预算

在每次会话开始时运行该脚本，以了解预算的当前状态：

```bash
fscl status --json
```

如果命令返回 “No config found”，说明 `fscl` 尚未初始化。询问用户是希望创建新的本地预算还是连接到现有的 `Actual Budget` 服务器，然后运行 `fscl init`。有关初始化的详细信息，请参阅 [references/commands.md](references/commands.md)。

如果状态信息显示 `budget.loaded = false` 且存在 `budget.load_error`，说明预算文件存在但无法打开。请向用户报告错误并协助排查问题（常见原因包括数据目录缺失、预算文件损坏或配置中的预算 ID 错误）。

否则，根据状态指标确定需要执行的具体操作流程。关键指标包括 `metrics.accounts.total`、`metrics.rules.total`、`metrics.transactions.total`、`metrics.transactions.uncategorized` 和 `metrics.transactions.unreconciled`。

### 流程路径 1：空白预算 → 新用户入门

此时尚未创建任何账户，预算文件刚刚生成，需要完成全部设置。

→ **[references/workflow-onboarding.md](references/workflow-onboarding.md)**

### 流程路径 2：需要优化

虽然已经创建了账户和交易记录，但预算自动化程度较低。可能表现为规则设置较少或没有规则、未分类交易占交易总数的比例较高，或者未结算的交易数量较多。这通常意味着用户已将 `fscl` 连接到现有的 `Actual Budget` 服务器，但尚未配置自动化规则。

→ **[references/workflow-optimization.md](references/workflow-optimization.md)**

### 流程路径 3：预算运行正常 → 日常维护

预算中的规则已正常生效，未分类交易的比例较低，未结算的交易数量也不多。此时用户处于维护阶段，可针对他们的具体需求提供帮助。

→ **[references/workflow-maintenance.md](references/workflow-maintenance.md)**

如果流程路径不明确，请询问用户：“这是全新的预算吗？还是您已经在使用 `Actual Budget` 服务了？”

无论预算状态如何，用户都可能会提出具体问题。请始终先回答他们当前的问题，并主动提供相应的操作指导（例如：“我发现您有 30 笔未分类的交易，需要帮忙处理吗？”），但不要强行推进操作。

## 参考文件

- **工作流程文档：**
  - [references/workflow-onboarding.md](references/workflow-onboarding.md) — 新预算设置
  - [references/workflow-optimization.md](references/workflow-optimization.md) — 现有预算的审核与自动化优化
  - [references/workflow-maintenance.md](references/workflow-maintenance.md) — 月度预算管理及日常维护

- **命令参考：**
  - [references/commands.md](references/commands.md) — 常用命令、操作流程及约定
  - [references/command-reference.md](references/command-reference.md) — 每个命令的参数及输出格式

- **其他参考文档：**
  - [references/budgeting.md](references/budgeting.md) — 分类模板、预算编制方法、收入管理、超支控制、联名账户处理
  - [references/import-guide.md](references/import-guide.md) — 文件导入格式及 CSV 列映射规则
  - [references/rules.md](references/rules.md) — 规则的 JSON 格式、条件设置及执行动作
  - [references/credit-cards.md](references/credit-cards.md) — 信用卡管理策略及债务追踪
  - [references/query-library.md](references/query-library.md) — 用于生成报告的预构建 AQL 查询语句