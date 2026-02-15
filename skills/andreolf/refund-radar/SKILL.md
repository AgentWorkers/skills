---
name: refund-radar
description: 扫描银行对账单以检测重复性收费，标记可疑交易，并通过交互式的 HTML 报告生成退款申请。
---

# refund-radar

该工具可扫描银行对账单，检测重复收费、标记可疑交易、识别重复项和费用，生成退款申请模板，并生成交互式的HTML审计报告。

## 触发命令

- `scan my bank statement for refunds`：扫描我的银行对账单以查找可退款项
- `analyze my credit card transactions`：分析我的信用卡交易
- `find recurring charges in my statement`：在对账单中查找重复收费
- `check for duplicate or suspicious charges`：检查是否存在重复或可疑的交易
- `help me dispute a charge`：帮助我投诉某笔交易
- `generate a refund request`：生成退款申请
- `audit my subscriptions`：审计我的订阅服务

## 工作流程

### 1. 获取交易数据

- 请求用户提供银行或信用卡的交易数据（CSV格式）或直接粘贴文本。
- 常见数据来源：
  - Apple Card：钱包 → 卡片余额 → 导出CSV文件
  - Chase：账户 → 下载交易记录 → CSV格式
  - Mint：交易记录 → 导出CSV文件
  - 其他银行：从交易历史中下载CSV文件

- 或者直接接受用户粘贴的文本数据：
```
2026-01-03 Spotify -11.99 USD
2026-01-15 Salary +4500 USD
```

### 2. 解析和规范化数据

- 使用解析器处理用户提供的数据：
```bash
python -m refund_radar analyze --csv statement.csv --month 2026-01
```

- 对于直接粘贴的文本数据，使用相应的解析逻辑：
```bash
python -m refund_radar analyze --stdin --month 2026-01 --default-currency USD
```

解析器会自动识别：
- 数据分隔符（逗号、分号、制表符）
- 日期格式（YYYY-MM-DD、DD/MM/YYYY、MM/DD/YYYY）
- 金额格式（单列显示或区分借方/贷方）
- 货币类型

### 3. 检查重复收费

- 通过以下条件识别重复订阅：
  - 在90天内同一商家多次收费
  - 金额相似（相差在5%以内或2美元以内）
  - 收费周期固定（每周、每月、每年）
  - 包含常见的订阅服务关键词（如Netflix、Spotify等）

- 输出结果包括：
  - 商家名称
  - 平均收费金额及周期
  - 最后一次收费日期
  - 下一次预计收费时间

### 4. 标记可疑交易

- 工具会自动标记以下类型的可疑交易：
| 标记类型 | 触发条件 | 严重程度 |
|-----------|---------|----------|
| 重复收费 | 同一商家在2天内多次收费 | 高度可疑 |
| 金额异常 | 金额超过基线的1.8倍（差额超过25美元） | 高度可疑 |
| 新商家 | 首次收费且金额超过30美元 | 中等可疑 |
| 类似费用 | 包含“FEE”、“ATM”、“OVERDRAFT”等关键词且金额超过3美元 | 低度可疑 |
| 货币异常 | 使用非常用货币或DCC支付方式 | 低度可疑 |

### 5. 与用户确认

- 对于被标记的交易，分批次（每批5-10条）询问用户：
  - 这笔收费是否合法？
  - 是否应将其视为正常收费？
  - 是否需要为这笔交易生成退款申请模板？

- 根据用户的回答更新交易状态：
```bash
python -m refund_radar mark-expected --merchant "Costco"
python -m refund_radar mark-recurring --merchant "Netflix"
```

### 6. 生成HTML报告

- 报告文件保存在`~/.refund_radar/reports/YYYY-MM.html`中。
- 报告结构参考[template.html]模板：
  - **摘要**：交易总数、总支出、重复收费次数、被标记的次数
  - **重复收费**：列出商家名称、金额、收费周期、下次预计收费时间
  - **异常收费**：显示被标记的交易及其严重程度和原因
  - **重复收费**：同一天的重复收费记录
  - **类似费用**：ATM手续费、外汇手续费等服务费用
  - **退款模板**：提供可复制的退款申请邮件/聊天消息模板

- 功能特性：
  - 可切换隐私设置（隐藏商家名称）
  - 支持深色/浅色显示模式
  - 部分内容可折叠
  - 模板上提供复制按钮
  - 空内容部分会自动隐藏

### 7. 生成退款申请

- 为每笔被标记的交易生成三种类型的退款申请模板：
  - **电子邮件**：正式的退款申请
  **聊天**：用于实时支持的快捷消息
  **投诉**：用于银行投诉的表格

- 每种模板提供三种语气风格（简洁、坚定、友好）

- 模板包含以下信息：
  - 商家名称和收费日期
  - 收费金额
  - 根据标记类型说明投诉原因
  - 包含信用卡最后四位数字和参考号码的占位符

**注意**：生成的文本中不允许使用撇号（'）。

## 命令行接口（CLI）参考

```bash
# Analyze statement
python -m refund_radar analyze --csv file.csv --month 2026-01

# Analyze from stdin
python -m refund_radar analyze --stdin --month 2026-01 --default-currency CHF

# Mark merchant as expected
python -m refund_radar mark-expected --merchant "Amazon"

# Mark merchant as recurring
python -m refund_radar mark-recurring --merchant "Netflix"

# List expected merchants
python -m refund_radar expected

# Reset learned state
python -m refund_radar reset-state

# Export month data
python -m refund_radar export --month 2026-01 --out data.json
```

## 文件目录结构

| 文件路径 | 用途 |
|------|---------|
| `~/.refund_radar/state.json` | 存储用户设置和交易历史记录 |
| `~/.refund_radar/reports/YYYY-MM.html` | 交互式审计报告 |
| `~/.refund_radar/reports/YYYY-MM.json` | 原始分析数据 |

## 隐私政策

- **无需网络连接**：所有操作均在本地完成。
- **不使用外部API**：不依赖Plaid或任何云服务。
- **用户数据仅保存在用户设备上**。
- **报告中的隐私设置**：可一键隐藏商家名称。

## 系统要求

- Python 3.9及以上版本
- 无需额外依赖库

## 项目仓库

https://github.com/andreolf/refund-radar