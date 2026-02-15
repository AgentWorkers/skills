---
name: gm3-alertworthy-feed
description: 仅提供对 GM3 Alertworthy 数据源的读取权限，该数据源可实时提供代币市场数据，供分析工具使用。
---

# GM3 警报值得关注（Alertworthy）数据源

---

## 概述
该技能提供了对 GM3 警报值得关注数据源的只读访问权限。

它返回当前所有警报值得关注（alertworthy）代币的详细信息，包括估值、流动情况、买家分布以及市场结构指标。该技能专为分析人员设计，允许他们在原始 GM3 数据的基础上应用自己的过滤和决策逻辑。

该技能本身不执行任何过滤、排名或交易操作。

---

## 端点（Endpoint）
**GET**  
https://api.gm3.fun/functions/v1/gm3-api/v1/paid/alertworthy

---

## 认证（Authentication）
使用 GM3 开发者 API 密钥进行认证。

请求必须包含以下头部信息：
```
Authorization: Bearer gm3_key_
```
API 密钥应作为机密信息存储，切勿在客户端代码中公开。

---

## 请求头部（Request Headers）
```
Accept: application/json
```

---

## 输入参数（Input Parameters）
该端点不接受任何输入参数。

---

## 输出结果（Output）
响应是一个 JSON 对象，其中包含一个 `data` 数组，该数组包含了所有警报值得关注代币的详细信息。

每个代币的记录可能包含以下字段：
- `mint`（代币发行时间）
- `rank`（排名）
- `fdv_usd`（当前公允价值）
- `fdv_at_alert`（首次发出警报时的公允价值）
- `net_sol_inflow`（净资金流入）
- `buy_ratio`（买入比例）
- `buy_count`/`sell_count`（买入/卖出数量）
- `unique_buyers`（唯一买家数量）
- `capital_efficiency`（资本效率）
- `market_structure_flags`（市场结构指标）
- `timestamps`（时间戳）

返回的具体字段可能会随着 GM3 平台的发展而发生变化。

---

## 错误代码（Error Codes）
- **401 Unauthorized**：API 密钥无效或已被吊销，或者访问权限已过期。
- **429 Too Many Requests**：请求次数过多，达到限制。
- **500/503**：临时服务器错误。

---

## 注意事项
- 该技能仅用于分析用途。
- 交易策略、过滤逻辑和决策制定应在客户端（agent）层面实现。
- 该技能不提供任何交易或执行功能。