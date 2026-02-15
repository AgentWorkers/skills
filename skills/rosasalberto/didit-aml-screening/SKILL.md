---
name: didit-aml-screening
description: 将 Didit 的 AML（反洗钱）筛查独立 API 集成到系统中，用于对个人或公司进行全球监控名单的筛查。当用户需要执行 AML 检查、核对制裁名单、检查 PEP（政治暴露人士）状态、检测负面媒体信息、实施 KYC/AML 合规性要求、筛查 OFAC（美国外国资产控制办公室）/UN（联合国）/EU（欧盟）的监控名单、计算风险评分或使用 Didit 进行反洗钱筛查时，可以使用该 API。该 API 支持超过 1300 个数据库、模糊名称匹配功能、可配置的评分权重以及持续监控机制。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🛡️"
    homepage: https://docs.didit.me
---
# Didit AML筛查API

## 概述

该API能够实时筛查个人或公司是否存在于1,300多个全球监控名单和高风险数据库中。采用双评分系统：**匹配分数**（身份确认的准确性）和**风险分数**（威胁等级）。

**关键要求：**
- `full_name` 是唯一必填字段。
- 支持 `entity_type`：`"person"`（默认）或 `"company"`。
- 文档编号（`document_number`）是用于精确匹配的“金钥匙”。
- 所有权重参数的总和必须为100。

**覆盖范围：** OFAC SDN、联合国（UN）、欧盟（EU）、英国财政部（HM Treasury）、国际刑警组织（Interpol）、FBI、170多个国家制裁名单、PEP等级1-4、50,000多个负面媒体来源、金融犯罪数据库。

**评分系统：**
1. **匹配分数**（0-100）：此人是否与名单上的信息完全一致？ → 将匹配结果分类为“误报”（False Positive）或“未审核”（Unreviewed）。
2. **风险分数**（0-100）：该实体的风险等级如何？ → 决定最终的AML（反洗钱）状态。

**API参考文档：** https://docs.didit.me/reference/aml-screening-standalone-api

---

## 认证

所有请求都必须包含 `x-api-key` 头部字段。请从 [Didit业务控制台](https://business.didit.me) 获取您的API密钥。

---

## 端点（Endpoint）

```
POST https://verification.didit.me/v3/aml/
```

### 头部字段（Headers）

| 头部字段 | 值 | 是否必填 |
| --- | --- |
| `x-api-key` | 您的API密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `full_name` | 字符串 | 是 | 个人或实体的全名 |
| `date_of_birth` | 字符串 | 否 | 日期格式为 `YYYY-MM-DD` |
| `nationality` | 字符串 | 否 | ISO国家代码（2位或3位字母） |
| `document_number` | 字符串 | 否 | 身份证明文件编号（“金钥匙”） |
| `entity_type` | 字符串 | 否 | `"person"` 或 `"company"` |
| `aml_name_weight` | 整数 | 否 | 名称在匹配分数中的权重（0-100） |
| `aml_dob_weight` | 整数 | 否 | 出生日期在匹配分数中的权重（0-100） |
| `aml_country_weight` | 整数 | 否 | 国家在匹配分数中的权重（0-100） |
| `aml_match_score_threshold` | 整数 | 否 | 低于阈值 = 误报；等于或高于阈值 = 未审核 |
| `save_api_request` | 布尔值 | 否 | 是否保存到业务控制台 |
| `vendor_data` | 字符串 | 否 | 用于会话跟踪的标识符 |

### 示例（Example）

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/aml/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "full_name": "John Smith",
        "date_of_birth": "1985-03-15",
        "nationality": "US",
        "document_number": "AB1234567",
        "entity_type": "person",
    },
)
print(response.json())
```

```typescript
const response = await fetch("https://verification.didit.me/v3/aml/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    full_name: "John Smith",
    date_of_birth: "1985-03-15",
    nationality: "US",
  }),
});
```

### 响应（Response, 200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "aml": {
    "status": "Approved",
    "total_hits": 2,
    "score": 45.5,
    "hits": [
      {
        "id": "hit-uuid",
        "caption": "John Smith",
        "match_score": 85,
        "risk_score": 45.5,
        "review_status": "False Positive",
        "datasets": ["PEP"],
        "properties": {"name": ["John Smith"], "country": ["US"]},
        "score_breakdown": {
          "name_score": 95, "name_weight": 60,
          "dob_score": 100, "dob_weight": 25,
          "country_score": 100, "country_weight": 15
        },
        "risk_view": {
          "categories": {"score": 55, "risk_level": "High"},
          "countries": {"score": 23, "risk_level": "Low"},
          "crimes": {"score": 0, "risk_level": "Low"}
        }
      }
    ],
    "screened_data": {
      "full_name": "John Smith",
      "date_of_birth": "1985-03-15",
      "nationality": "US",
      "document_number": "AB1234567"
    },
    "warnings": []
  }
}
```

---

## 匹配分数系统（Match Score System）

**计算公式：** `(名称 × 权重1) + (出生日期 × 权重2) + (国家 × 权重3)`

| 组件 | 默认权重 | 算法 |
| --- | --- | --- |
| 名称 | 60% | RapidFuzz算法——处理拼写错误、词序变化、中间名差异 |
| 出生日期 | 25% | 完全匹配=100%，年份相同=100%，年份不同但日期相同=50%，不匹配=-100% |
| 国家 | 15% | 完全匹配=100%，不匹配=-50%，国家代码缺失=0%。自动转换ISO代码 |

**文档编号（“金钥匙”）：**

| 情况 | 影响 |
| --- | --- |
| 类型相同、数值相同 | 将匹配分数设置为**100** |
| 类型不同或其中一个字段缺失 | 保持原始分数 |
| 类型相同、数值不同 | 扣除**50分** |

**分类：** 分数低于阈值（默认为93） → **误报**。分数等于或高于阈值 → **未审核**。

> 当数据缺失时，剩余的权重会重新调整。例如，仅提供名称时，名称的权重会变为100%。

---

## 风险分数系统（Risk Score System）

**计算公式：** `(国家 × 0.30) + (类别 × 0.50) + (犯罪记录 × 0.20)`

**最终AML状态（基于非误报结果的最高风险分数）：**

| 最高风险分数 | 状态 |
| --- | --- |
| 低于80（默认） | **批准通过** |
| 80-100之间 | **正在审核中** |
| 高于100 | **拒绝** |
| 所有结果均为误报 | **批准通过** |

**类别权重（占50%）：**

| 类别 | 分数 |
| --- | --- |
| 制裁/PEP等级1 | 100 |
| 警告/监管相关 | 95 |
| PEP等级2/破产 | 80 |
| 负面媒体 | 60 |
| PEP等级4/商业人士 | 55 |

---

## 状态值及处理方式（Status Values & Handling）

| 状态 | 含义 | 处理方式 |
| --- | --- | --- |
| `Approved` | 无显著匹配或均为误报 | 可以继续操作 |
| `In Review` | 发现中等风险匹配 | 需要手动进行合规性审核 |
| `Rejected` | 确认高风险匹配 | 根据政策进行拦截或升级处理 |
| `Not Started` | 尚未进行筛查 | 检查是否有数据缺失 |

### 错误响应（Error Responses）

| 代码 | 含义 | 处理方式 |
| --- | --- | --- |
| `400` | 请求体无效 | 检查 `full_name` 和参数格式 |
| `401` | API密钥无效 | 验证 `x-api-key` 头部字段 |
| `403` | 信用额度不足 | 在业务控制台检查信用额度 |

---

## 警告标签（Warning Tags）

| 标签 | 说明 |
| --- | --- |
| `POSSIBLE_MATCH_FOUND` | 发现可能的监控名单匹配项，需要审核 |
| `COULD_NOT_PERFORM_AML_SCREENING` | 缺少KYC数据。请提供全名、出生日期、国籍、文档编号 |

---

## 响应字段参考（Response Field Reference）

### 匹配结果（Hit Object）

| 字段 | 类型 | 说明 |
| --- | --- |
| `match_score` | 整数 | 0-100的身份确认分数 |
| `risk_score` | 浮点数 | 0-100的风险等级分数 |
| `review_status` | 字符串 | `"False Positive"`、`Unreviewed`、`Confirmed Match`、`Inconclusive` |
| `datasets` | 数组 | 例如 `["Sanctions"]`、`["PEP"]`、`["Adverse Media"]` |
| `pep_matches` | 数组 | PEP匹配详情 |
| `sanction_matches` | 数组 | 制裁匹配详情 |
| `adverse_media_matches` | 数组 | 负面媒体信息（包含标题、摘要、来源链接、情感评分、负面关键词） |
| `linked_entities` | 数组 | 相关人员/实体 |
| `first_seen` / `last_seen` | 字符串 | ISO 8601时间戳 |

**负面媒体情感评分：** `-1` = 轻微负面，`-2` = 中等负面，`-3` = 高度负面。

---

## 持续监控（Continuous Monitoring）

**Pro计划** 提供此功能。所有经过AML筛查的会话都会自动包含以下服务：**
- **每日自动重新筛查**，针对更新的监控名单。
- 新匹配结果 → 会话状态更新为“正在审核中”或“拒绝”。
- **实时Webhook通知**，用于状态变化。
- 无需额外集成，使用工作流程配置中的相同阈值。

---

## 常见工作流程（Common Workflows）

### 基本AML检查（Basic AML Check）

```
1. POST /v3/aml/ → {"full_name": "John Smith", "nationality": "US"}
2. If "Approved" → no significant watchlist matches
   If "In Review" → review hits[].datasets, hits[].risk_view for details
   If "Rejected" → block user, check hits for sanctions/PEP details
```

### 全面KYC + AML检查（Comprehensive KYC + AML）

```
1. POST /v3/id-verification/ → extract name, DOB, nationality, document number
2. POST /v3/aml/ → screen extracted data with all fields populated
3. More data = higher match accuracy = fewer false positives
```