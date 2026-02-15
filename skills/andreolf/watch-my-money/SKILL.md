---
name: watch-my-money
description: 分析银行交易，对支出进行分类，跟踪每月预算，检测超支和异常情况。生成交互式的 HTML 报告。
triggers:
  - "track spending"
  - "check my budget"
  - "analyze transactions"
  - "what did I spend on"
  - "am I overspending"
  - "budget tracker"
  - "spending analysis"
  - "monthly expenses"
formats:
  - CSV bank exports
  - Text transaction lists
outputs:
  - Interactive HTML report
  - JSON data export
  - Console summary
privacy: local-only
---

# watch-my-money

本工具用于分析用户的交易记录，对支出进行分类，跟踪预算使用情况，并在超出预算时发出警报。

## 工作流程

### 1. 获取交易数据

- 从用户处获取银行或信用卡交易的CSV文件，或直接输入交易记录的文本。
- 常见数据来源：
  - 从银行在线门户下载CSV文件
  - 从预算管理应用程序导出数据
  - 从对账单中复制/粘贴交易记录

**支持的格式：**
  - 任何包含日期、描述和金额列的CSV文件
  - 输入的文本格式示例：`2026-01-03 Starbucks -5.40 CHF`

### 2. 解析和规范化数据

- 读取输入数据，并将其转换为标准格式：
  - 自动识别数据分隔符（逗号、分号、制表符）
  - 解析日期格式（YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY）
  - 将金额统一为标准格式（支出为负数，收入为正数）
  - 从交易描述中提取商家名称
  - 识别重复出现的交易（如订阅服务）

### 3. 对交易进行分类

- 为每笔交易分配相应的类别：
  - 租金、水电费、订阅服务、食品杂货、外出就餐
  - 交通费用、旅行费用、购物费用、健康相关支出
  - 收入、转账、其他费用

**分类优先级：**
  1. 查看用户自定义的商家分类规则
  2. 应用预定义的关键词规则（详见 [common-merchants.md](references/common-merchants.md)
  3. 使用模式匹配进行分类（如识别订阅服务）
  4. 在无法确定分类时采用启发式方法

- 对于分类不明确的交易（5-10笔交易），请用户进行确认。用户可以保存这些分类规则以供后续使用。

### 4. 检查预算使用情况

- 将实际支出与用户设定的预算进行对比。

- 警报阈值：
  - 花费达到预算的80%：黄色警告
  - 花费达到预算的100%：红色警告
  - 花费超过预算的120%：红色紧急警告

- 预算模板请参考 [budget-templates.md](references/budget-templates.md)。

### 5. 发现异常支出

- 标记异常支出情况：
  - 某类别支出突然大幅增加（超过基线的1.5倍且增幅超过50%）
  - 订阅服务费用增长超过20%
  - 新出现的昂贵商家（首次出现且支出超过30元）
  - 可能的重复性支出（定期收取相同金额的费用）

- 基线数据为过去3个月的平均支出（如果没有历史数据，则使用当月的支出）

### 6. 生成HTML报告

- 生成本地HTML报告文件，内容包括：
  - 每月的收入、支出和净余额统计
  - 各类别的支出与预算对比情况
  - 最高支出额的商家列表
  - 警报信息
  - 被识别的重复性交易记录
  - 隐私设置（可选择隐藏金额或商家名称）

- 可以复制 [template.html](assets/template.html) 并替换其中的数据。

### 7. 保存数据

- 将处理后的数据保存在 `~/.watch_my_money/` 目录下：
  - `state.json`：存储预算信息、商家分类规则和交易历史
  - `reports/YYYY-MM.json`：存储每月的机器可读数据
  - `reports/YYYY-MM.html`：生成交互式报告文件

## 命令行接口（CLI）

```bash
# Analyze CSV
python -m watch_my_money analyze --csv path/to/file.csv --month 2026-01

# Analyze from stdin
cat transactions.txt | python -m watch_my_money analyze --stdin --month 2026-01 --default-currency CHF

# Compare months
python -m watch_my_money compare --months 2026-01 2025-12

# Set budget
python -m watch_my_money set-budget --category groceries --amount 500 --currency CHF

# View budgets
python -m watch_my_money budgets

# Export month data
python -m watch_my_money export --month 2026-01 --out summary.json

# Reset all state
python -m watch_my_money reset-state
```

## 输出结构

控制台显示以下信息：
- 每月的收入、支出和净余额统计
- 各类别的支出与预算对比情况
- 被识别的重复性交易记录
- 支出最高的5家商家

生成的文件包括：
- `~/.watch_my_money/state.json`
- `~/.watch_my_money/reports/2026-01.json`
- `~/.watch_my_money/reports/2026-01.html`

## HTML报告的特点

- 可折叠的类别部分
- 预算进度条
- 重复性交易列表
- 月度数据对比功能
- 隐私设置（可隐藏敏感信息）
- 深色模式（符合系统设置）
- 便于截图的布局
- 空章节会自动隐藏

## 隐私保护

所有数据仅保存在本地，不进行网络传输，也不使用任何外部API。交易数据仅在 `~/.watch_my_money/` 目录内进行分析和存储。