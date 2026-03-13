---
name: Crypto Tax Calculator
version: 1.0.0
description: 使用先进先出（FIFO）、后进先出（LIFO）或平均成本法计算加密货币资本利得税；支持多国税法；并提供HTML格式的报告生成功能。
runtime: python3
---
# 加密货币税务计算器 📊

这是一个全面的加密货币税务计算工具。您可以导入交易记录，选择所在国家/地区，然后生成专业的税务报告。

## 工作流程概述

```
[Import CSV] → [Parse Trades] → [Match Cost Basis] → [Calculate Gains] → [Apply Tax Rules] → [Generate Report]
     ↓              ↓                  ↓                    ↓                   ↓                    ↓
  Validate      Normalize         FIFO/LIFO/AVG        Short vs Long       US/UK/AU/CN         HTML + CSV
  Format        Currencies        Cost Matching         Term Gains          Rate Tables          Tax Report
```

## 第一步：准备数据

您的 CSV 文件必须包含以下列（顺序无关紧要）：

| 列名 | 是否必填 | 格式 | 示例 |
|--------|----------|--------|---------|
| date   | ✅ | YYYY-MM-DD HH:MM:SS | 2024-03-15 14:30:00 |
| type   | ✅ | 买入/卖出/交换/转账 | 买入 |
| asset  | ✅ | 资产代码 | BTC |
| amount | ✅ | 小数 | 0.5 |
| price_usd | ✅ | 每单位价格（美元） | 65000.00 |
| fee_usd | ❌ | 费用（美元） | 2.50 |
| exchange | ❌ | 交易平台名称 | Binance |
| tx_hash | ❌ | 交易哈希值 | 0xabc... |

## 第二步：选择计算方法

```bash
# FIFO — First In, First Out (most common, required in some jurisdictions)
bash scripts/crypto-tax-calc.sh calculate --input trades.csv --method fifo --country US

# LIFO — Last In, First Out (can minimize taxes in rising markets)
bash scripts/crypto-tax-calc.sh calculate --input trades.csv --method lifo --country US

# Average Cost — Weighted average (required in UK, simpler calculation)
bash scripts/crypto-tax-calc.sh calculate --input trades.csv --method average --country UK
```

## 第三步：选择所在国家/地区

### 🇺🇸 美国
- 短期收益（<1年）：按普通收入征税（10%-37%）
- 长期收益（>1年）：0%、15% 或 20%
- “洗售”规则：目前不对加密货币适用（可能发生变化）
- 支持生成 8949 表格

### 🇬🇧 英国
- 资本利得税：10%（基本税率）/ 20%（较高税率）
- 年度免税额：6,000 英镑（2024/25 年）
- 必须使用“成本平均法”计算收益
- 生成的报告格式符合 HMRC 的要求

### 🇦🇺 澳大利亚
- 持有时间超过 12 个月的资产可享受 50% 的资本利得税减免
- 适用边际税率（19%-45%）
- 个人使用资产免税额：<10,000 澳元
- 生成的报告格式符合 ATO 的要求

### 🇨🇳 中国
- 个人所得税：收益部分需缴纳 20% 的税款
- 目前相关法规尚不明确
- 该工具提供的报告仅用于参考收益计算

## 第四步：生成报告

该工具会输出：
- **HTML 报告** — 包含图表和表格的可视化摘要
- **CSV 导出** — 每笔交易的收益/损失数据（机器可读格式）
- **摘要 JSON** — 总计数据，便于与其他工具集成

## 完整命令参考

```bash
# Calculate taxes
bash scripts/crypto-tax-calc.sh calculate --input FILE --method METHOD --country CODE [--year YEAR]

# Validate CSV format
bash scripts/crypto-tax-calc.sh validate --input FILE

# Show summary only (no report file)
bash scripts/crypto-tax-calc.sh summary --input FILE --method METHOD

# Merge multiple exchange CSVs
bash scripts/crypto-tax-calc.sh merge --inputs "file1.csv,file2.csv" --output merged.csv

# Compare methods side-by-side
bash scripts/crypto-tax-calc.sh compare --input FILE --country CODE
```

## 重要免责声明

⚠️ 本工具仅用于提供信息，不构成税务建议。请咨询专业的税务顾问以获取针对您个人情况的具体建议。

⚠️ 税法经常变动，请务必向当地税务机关核实最新的税率和规定。