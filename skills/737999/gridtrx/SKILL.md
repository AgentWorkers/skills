---
name: gridtrx
description: 专为AI代理设计的双记账、全周期会计套件。能够将银行CSV文件、OFX文件和QBO文件转换为平衡且可审计的财务报表（资产负债表、损益表、总账、试算平衡表）。所有数据都存储在同一个本地的SQLite文件中。
homepage: https://github.com/gridtrx/gridtrx
requires_tools:
  - exec
  - read
  - write
metadata:
  clawdbot:
    requires:
      env:
        - GRIDTRX_WORKSPACE
      bins:
        - python3
        - pip
    primaryEnv: GRIDTRX_WORKSPACE
    files:
      - "*.py"
---
# 技能：GridTRX 会计

## 功能概述

当用户要求您进行“记账”、“分类支出”、“导入银行交易”或执行任何与会计相关的任务时，可以使用此技能。GridTRX 是一个全周期的双式记账系统。您只需用简单的英语提供指令，系统便会自动完成记账工作。所有交易都会保持平衡，金额都是确定的。所有数据都存储在本地，不依赖云服务或外部 API。

GridTRX 会生成一套可审计的财务报告，包括资产负债表、损益表、总账、试算平衡表、调整分录以及留存收益的结转信息。这些报告可以导出为 CSV 或 PDF 格式，适用于任意时间段。

## 架构

GridTRX 通过三个接口访问同一个核心处理模块（`models.py` → `books.db`）：

1. **MCP 服务器（推荐给代理使用）**：基于结构化 JSON 的工具，包含 19 个功能（12 个用于读取数据，7 个用于写入数据），直接调用 `models.py`。无需进行文本解析，参数需以键值对形式提供，输出结果具有确定性。安装方式：`pip install mcp`。
2. **命令行界面（CLI，适用于代理或高级用户）**：通过 `python cli.py` 执行一次性命令。除了 Python 3.7 及更高版本的标准库外，无需额外依赖任何软件。任何终端应用程序都可以通过 `subprocess` 调用该接口。
3. **浏览器界面（供人类用户使用）**：基于 Flask 的 Web 界面，运行地址为 `localhost:5000`，通过 `python run.py` 启动。支持账本浏览、报表查看（支持多列对比）、银行数据导入（含规则预览）、对账标记以及暗黑模式等功能。

这三个接口都访问同一个 `models.py` 数据层，确保数据的一致性。优先使用 MCP 服务器；如果 MCP 服务器不可用，则使用 CLI。浏览器界面主要用于人工审核。

### MCP 服务器配置

安装方式：`pip install mcp`

需在代理的 MCP 配置文件中设置 `GRIDTRX_WORKSPACE` 为用户的客户端文件夹路径：
```json
{
  "command": "python",
  "args": ["/path/to/mcp_server.py"],
  "env": {"GRIDTRX_WORKSPACE": "/path/to/clients"}
}
```

`GRIDTRX_WORKSPACE` 是必填项——如果没有设置，MCP 服务器将无法启动。任何位于工作空间之外的数据库路径在运行时都会被拒绝。所有 MCP 工具都会将 `db_path` 作为第一个参数，该路径必须指向工作空间内的 `books.db` 文件。

### CLI 使用方法

执行一个命令后，系统会将结果以纯文本形式输出到标准输出（stdout），然后退出。如果设置了 `GRIDTRX_WORKSPACE`，CLI 会遵循与 MCP 服务器相同的工作空间规则，拒绝处理工作空间之外的路径。

## 所需输入参数

- 客户端账本文件（`books.db` 或其父文件夹）的绝对路径。
- 银行交易文件的绝对路径（格式为 `.csv`、`.ofx` 或 `.qbo`）。
- 需要记录的交易账户名称（通常为 `BANK.CHQ`，用于支票账户）。

## 核心概念

- **双式记账**：每笔交易都是一个平衡的、零和的操作（借方金额 = 贷方金额）。
- **符号约定**：正数表示借方；括号内的数值（如 `(1,500.00)` 表示贷方；`—` 表示零。
- **金额处理**：金额以整数形式存储（单位为分），显示时保留两位小数。
- **账户名称**：不区分大小写，通常首字母大写。常见前缀包括 `BANK.`、`EX.`、`REV.`、`AR.`、`AP.`、`GST.`、`RE.`。
- **待处理交易（EX.SUSP）**：用于存放未识别的交易。用户可以指定这些待处理交易的类别，AI 会自动处理它们；或者用户也可以通过 GUI 手动清除这些交易。
- **导入规则**：用于定义账户与交易类型之间的映射关系。匹配不区分大小写，优先级最高的规则优先应用。部分规则会自动将金额拆分为净额和税额。
- **锁定日期**：用于防止修改已结束的会计期间。在导入历史数据前请检查该日期。
- **系统架构**：每个客户的财务数据都存储在一个 SQLite 文件中。该文件可被复制、备份或通过电子邮件发送。所有功能（CLI、MCP 服务器和浏览器界面）都调用同一个 `models.py` 数据层。

## 工作流程

### 第一步：初始化（如果账本不存在）

**MCP：** 无专用工具，需通过 `exec` 命令执行 CLI。
**CLI：** `python cli.py` 后接 `new /path/to/folder "Company Name"`。

此操作会创建一个包含完整账户结构的 `books.db` 文件（约 60 个账户）、五份报表（资产负债表、损益表、调整分录表、交易报表、留存收益报表）以及四个税码。**务必使用预设的初始账本作为基础**，因为这些账本包含了关键的留存收益计算逻辑（从损益表到年末留存收益）。切勿在没有这些初始数据的情况下手动创建报表。系统会自动将当前财年的结束日期设置为 `fy_end_date`。

初始化完成后，运行 `validate` 命令确认报表数据的完整性：
**CLI：** `python cli.py /path/to/books.db validate`

### 第二步：导入银行数据

**MCP（推荐方式）：**
- CSV 格式：`import_csv(db_path, csv_path, "BANK.CHQ")`
- OFX/QBO 格式：`import_ofx(db_path, ofx_path, "BANK.CHQ")`

**CLI 替代方式：**
- CSV 格式：`python cli.py /path/to/books.db importcsv /path/to/file.csv BANK.CHQ`
- OFX 格式：`python cli.py /path/to/books.db importofx /path/to/file.qbo BANK.CHQ`

系统会自动应用所有导入规则，并显示导入结果（包括已成功导入的记录、被跳过的记录以及被标记为待处理的记录）。

**CaseWare AJE 数据导入：**
- MCP：`import_aje(db_path, file_path, "25AJE")`
- CLI：`python cli.py /path/to/books.db importaje /path/to/aje_export.iif 25AJE`
- 支持 QuickBooks IIF 和 Venice/MYOB 格式的文件导入。

### 第三步：处理待处理交易

**MCP：** `get_ledger(db_path, "EX.SUSP")`
**CLI：** `python cli.py /path/to/books.db ledger EX.SUSP`

这些记录表示未识别的交易，请查看每笔交易的描述和交易 ID。

### 第四步：与用户确认待处理交易的分类

将每笔待处理交易展示给用户，并询问其所属类别。切勿猜测分类。如果交易描述不明确（例如 “AMAZON”、“BEST BUY”、“TRANSFER”），请先询问用户具体的业务背景后再进行分类。

用户确认分类后，可以添加相应的规则，以便后续导入时自动应用正确的分类：
**MCP：** `add_rule(db_path, "AMAZON", "EX.OFFICE", "G5", 0)`
**CLI：** `python cli.py /path/to/books.db addrule AMAZON EX.OFFICE G5 0`

税码是可选的。常见税码包括：`G5`（GST 5%）、`H13`（HST 13%）、`H15`（HST 15%）、`E`（免税）。

### 第五步：清除待处理交易并重新导入数据

删除所有待处理的交易记录，然后重新导入数据以确保新的分类规则生效：
**MCP：** 对每笔待处理交易执行 `delete_transaction(db_path, txn_id)`，之后再次执行 `import_csv()` 或 `import_ofx()`。
**CLI：** 对每笔待处理交易执行 `python cli.py /path/to/books.db delete <txn_id>`，之后重新执行导入命令。

重复步骤 3-5，直到所有待处理交易都被处理完毕。

### 第六步：验证和生成报表

**MCP：**
- `trial_balance(db_path)` — 确保借方金额与贷方金额相等。
- `generate_report(db_path, "BS")` — 生成资产负债表。
- `generate_report(db_path, "IS")` — 生成损益表。

**CLI：**
- `python cli.py /path/to/books.db tb`
- `python cli.py /path/to/books.db report BS`
- `python cli.py /path/to/books.db report IS`

### 第七步：年末数据结转

当当前财年结束时：
**MCP：** `rollforward(db_path, "2025-12-31")`
**CLI：** `python cli.py /path/to/books.db rollforward 2025-12-31`

此操作会从损益表中读取年末数据（RE.CLOSE），更新相关分录（RE.OFS / Cr RE.OPEN），设置新的财年结束日期，并将下一个财年的数据导入系统。之后重复步骤 2 的操作。

## 错误处理：撤销错误的导入操作

如果用户上传了错误的文件或错误地选择了账户进行导入：
1. **查找错误交易**：使用 `search_transactions(db_path, "some description")` 或通过 CLI 的 `search <keyword>` 命令查找。
2. **逐一删除错误交易**：使用 `delete_transaction(db_path, txn_id)` 或 `delete <txn_id>` 删除错误交易。
3. **验证余额是否平衡**：确认删除错误交易后，系统的试算平衡表是否仍然平衡。
4. **重新导入正确的文件**。

系统不支持批量撤销操作。删除操作是针对单个交易进行的，并且会尊重系统的锁定日期限制（无法删除已结束会计期间的交易）。

## MCP 工具列表（共 19 个工具）

### 读取数据工具
| 工具 | 功能 |
|------|---------|
| `list_accounts(db_path, query?)` | 列出/搜索账户信息 |
| `get_balance(db_path, account_name, date_from?, date_to?)` | 查询单个账户的余额 |
| `get_ledger(db_path, account_name, date_from?, date_to?)` | 查看账户的账本余额 |
| `trial_balance(db_path, as_of_date?)` | 查看所有账户的试算平衡表 |
| `generate_report(db_path, report_name, date_from?, date_to?)` | 生成报表（资产负债表、损益表等） |
| `get_transaction(db_path, txn_id)` | 查询单笔交易的详细信息 |
| `search_transactions(db_path, query, limit?)` | 按描述或参考信息搜索交易 |
| `list_reports(db_path)` | 列出所有可用的报表 |
| `list_rules(db_path)` | 查看所有导入规则 |
| `get_info(db_path)` | 获取公司名称、财年信息和锁定日期 |

### 写入数据工具
| 工具 | 功能 |
|------|---------|
| `post_transaction(db_path, date, description, amount, debit_account, credit_account)` | 添加简单的交易记录 |
| `delete_transaction(db_path, txn_id)` | 删除交易记录（尊重锁定日期限制） |
| `add_account(db_path, name, normal_balance, description?)` | 添加新的账户 |
| `add_rule(db_path, keyword, account_name, tax_code?, priority?)` | 添加导入规则 |
| `delete_rule(db_path, rule_id)` | 删除导入规则 |
| `import_csv(db_path, csv_path, bank_account)` | 导入 CSV 格式的银行交易数据 |
| `import_ofx(db_path, ofx_path, bank_account)` | 导入 OFX/QBO 格式的银行交易数据 |
| `import_aje(db_path, file_path, ref_prefix)` | 导入 CaseWare AJE 格式的文件数据 |
| `rollforward(db_path, ye_date)` | 进行年末数据结转（更新年末分录、设置锁定日期） |
| `year_end(db_path, ye_date)` | 实现年末数据结转的功能 |
| `set_lock_date(db_path, lock_date?)` | 显示或设置锁定日期 |
| `set_ceiling(db_path, date?)` | 显示或设置财年结束日期 |

## 注意事项：

- **切勿猜测交易类别**：如果交易描述不明确，应将其标记为待处理交易（EX.SUSP），并询问用户具体用途。例如，“AMAZON”可能代表办公用品、库存费用或销售成本等。
- **切勿直接修改 `books.db` 文件**：所有数据操作都必须通过 `cli.py` 命令或 MCP 工具完成，严禁使用文件工具直接操作 SQLite 数据库。
- **请在指定的工作空间内操作**：仅处理用户 GridTRX 工作空间内的 `books.db` 文件。MCP 服务器和 CLI 在接收到 `GRIDTRX_WORKSPACE` 设置后都会强制执行这一规则；未设置该参数时，系统将拒绝处理工作空间之外的文件。
- **系统不进行任何网络请求**：GridTRX 所有数据处理都在本地完成，不会发送请求到外部服务或调用外部 API。
- **遵守数据导入的时间限制**：在导入数据前，请使用 `get_info()` 函数检查锁定日期和财年结束日期。不得在锁定日期之前或之后进行数据导入；使用 `rollforward` 命令将数据更新到下一个财年。
- **保持输出数据的原始格式**：在向用户展示财务数据时，请使用 GridTRX 提供的原始数值，不得进行四舍五入、格式转换或改变符号的显示方式（正数表示借方，括号内的数值表示贷方）。
- **试算平衡表必须平衡**：任何操作后，如果试算平衡表显示借方和贷方金额不平衡，请立即停止操作并查明原因。