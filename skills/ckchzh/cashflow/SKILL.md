---
name: CashFlow
description: "个人现金流追踪器，用于管理日常财务。您可以记录收入和支出，并附上备注；查看当前余额；查看每日和每月的交易汇总；浏览交易历史记录。所有数据均存储在本地，确保您的隐私得到充分保护。非常适合自由职业者、学生或任何希望简单追踪财务状况的人士，无需使用复杂的应用程序。"
version: "1.0.0"
author: "BytesAgain"
tags: ["finance","money","budget","cashflow","expense","income","tracker","personal-finance"]
categories: ["Finance", "Personal Management", "Productivity"]
---
# CashFlow

CashFlow 是一个轻量级的个人财务管理工具，完全在终端环境中运行。无需注册账户、无需云同步，操作简单快捷，专注于资金的管理与追踪。

## 为什么选择 CashFlow？

- **零配置**：无需任何设置，即可立即使用
- **隐私保护**：所有数据都存储在您的本地机器上
- **快速记录**：交易记录可瞬间完成
- **清晰汇总**：提供实时的每日和每月财务概览
- **跨平台兼容**：支持任何安装了 bash 和 python3 的系统

## 命令说明

- `income <金额> [备注]` — 记录收入，可添加备注
- `expense <金额> [备注]` — 记录支出，可添加备注
- `balance` — 显示当前余额及收入/支出明细
- `today` — 列出当天的所有交易记录
- `month` — 查看每月的收入和支出情况
- `history [数量]` — 显示最近 n 条交易记录（默认为 10 条）
- `info` — 查看软件版本信息
- `help` — 显示可用的命令列表

## 使用示例

```bash
cashflow income 5000 March salary
cashflow expense 45.50 lunch with team
cashflow expense 120 electricity bill
cashflow balance
cashflow month
```

## 数据存储

所有财务数据以 JSON 格式存储在 `~/.cashflow/` 目录下。您可以随时备份、导出或查看数据。

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com