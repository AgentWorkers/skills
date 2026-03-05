---
name: tw-stock-info
description: 使用 Fugle 或 FinMind API 获取台湾股票的详细信息。这些 API 可提供台湾股票的实时报价、历史数据、财务报表以及技术指标。
---
# 台湾股票信息

## 概述

这是一个使用 Fugle 和 FinMind API 的完整台湾股票分析工具，提供台湾股票的实时报价、历史数据、财务报表和技术指标。

---

## API 端点概要

### Fugle API（实时数据与技术分析）
- **基础 URL：** `https://api.fugle.tw`
- **认证方式：** 请求头 `X-API-Key: {your_api_key}`
- **功能：** 实时报价、K线图、交易记录、技术指标

### FinMind API（历史数据与财务数据）
- **基础 URL：** `https://api.finmindtrade.com/api/v4/data`
- **认证方式：** 请求头 `Authorization: Bearer {your_token}`
- **功能：** 历史价格、财务报表、收入、每股收益（EPS）

---

## 使用示例

详细的使用示例请参见 [examples.md](./examples.md)。

---

## 文件结构

```
tw-stock-analysis/
├── SKILL.md          (This file - API overview)
├── api/
│   ├── fugle.md      (Fugle API specifications)
│   └── finmind.md    (FinMind API specifications)
└── examples.md       (Usage examples in cURL format)
```

---

## 请求速率限制

| API | 未验证的请求速率 | 经过验证的请求速率 |
|-----|------------------|---------------------|
| Fugle | 需根据计划确定 | 请联系服务提供商 |
| FinMind | 每小时 300 次请求 | 每小时 600 次请求 |