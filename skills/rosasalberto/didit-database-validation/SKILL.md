---
name: didit-database-validation
description: >
  Integrate Didit Database Validation API to verify personal data against government
  databases. Use when the user wants to validate identity against government records,
  verify national ID numbers, check CPF/CURP/DNI/cedula numbers, perform identity database
  lookups, validate identity documents against official sources, or implement database
  verification for Latin American or Spanish identity documents using Didit.
  Supports 18 countries with 1x1 and 2x2 matching methods.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🗄️"
    homepage: https://docs.didit.me
---

# Didit 数据库验证 API

## 概述

该 API 用于将个人数据及身份证明文件与可信的政府和金融数据库进行比对，以防止身份欺诈，并确保身份信息的真实性。

**关键要求：**
- 至少需要目标国家的 **国民身份证/证件号码**。
- 支持 **18 个国家**（主要涵盖拉丁美洲国家和西班牙）。
- 返回结果类型包括：`full_match`（完全匹配）、`partial_match`（部分匹配）或 `no_match`（未匹配）。
- 仅对 **成功查询** 收费；数据不足时无需付费。

**匹配方式：**

| 方法 | 描述 | 起价 |
|---|---|---|
| **1x1** | 单一数据源验证 | $0.05 |
| **2x2** | 两个数据源交叉验证 | $0.30 |

**API 参考文档：** https://docs.didit.me/reference/database-validation-api

---

## 认证

所有请求都必须包含 `x-api-key` 标头。请从 [Didit 商业控制台](https://business.didit.me) 获取您的 API 密钥。

---

## 端点

```
POST https://verification.didit.me/v3/database-validation/
```

### 请求头

| 标头 | 值 | 是否必填 |
|---|---|---|
| `x-api-key` | 您的 API 密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `id_number` | string | 是 | 全球通用身份编号，系统会自动匹配到对应的国家字段 |
| `first_name` | string | 否 | 用于匹配的名字 |
| `last_name` | string | 否 | 用于匹配的姓氏 |
| `date_of_birth` | string | 否 | 出生日期（格式为 `YYYY-MM-DD`，部分国家要求提供） |
| `issuing_state` | string | 否 | ISO 3166-1 国家代码（3 位字母） |
| `save_api_request` | boolean | 否 | 是否将查询结果保存到商业控制台 |
| `vendor_data` | string | 否 | 用于会话跟踪的标识符 |

`id_number` 字段会自动映射到对应的国家特定字段：

| 国家 | 映射字段 | 证件类型 | 格式 |
|---|---|---|---|
| ARG | `document_number` | DNI | — |
| BOL | `document_number` | CI | — |
| BRA | `tax_number` | CPF | 11 位数字 |
| CHL | `personal_number` | RUT | — |
| COL | `personal_number` | Cedula | — |
| CRI | `personal_number` | Cedula | — |
| DOM | `personal_number` | Cedula | 11 位数字 |
| ECU | `personal_number` | Cedula | 10 位数字 |
| ESP | `personal_number` | DNI/NIE | — |
| GTM | `document_number` | DPI | — |
| HND | `document_number` | DNI | — |
| MEX | `personal_number` | CURP | 18 位字符 |
| PAN | `document_number` | Cedula | — |
| PER | `personal_number` | DNI | 8 位数字 |
| PRY | `document_number` | CI | — |
| SLV | `document_number` | DUI | — |
| URY | `personal_number` | CI | — |
| VEN | `document_number` | Cedula | — |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/database-validation/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "id_number": "12345678",
        "first_name": "Carlos",
        "last_name": "Garcia",
        "issuing_state": "PER",
    },
)
print(response.json())
```

```typescript
const response = await fetch("https://verification.didit.me/v3/database-validation/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    id_number: "12345678",
    first_name: "Carlos",
    last_name: "Garcia",
    issuing_state: "PER",
  }),
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "database_validation": {
    "status": "Approved",
    "match_type": "full_match",
    "issuing_state": "PER",
    "validation_type": "1x1",
    "screened_data": {
      "personal_number": "12345678",
      "first_name": "Carlos",
      "last_name": "Garcia"
    },
    "validations": {
      "full_name": "full_match",
      "identification_number": "full_match"
    }
  }
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 与政府记录完全匹配 | 身份已确认 |
| `"Declined"` | 未找到匹配项 | 身份无法验证 |
| `"In Review"` | 部分匹配或数据不足 | 正在审核数据并进行验证 |

### 错误响应

| 代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 请检查目标国家的身份证号码格式 |
| `401` | API 密钥无效 | 请检查 `x-api-key` 标头 |
| `403` | 信用额度不足 | 请在 business.didit.me 充值 |

---

## 匹配逻辑

### 名字匹配

| 结果 | 匹配条件 |
|---|---|
| **完全匹配** | 名字完全匹配（Levenshtein 编码相似度达到 85%），或名字和姓氏都完全匹配 |
| **部分匹配** | 任意一个名字部分完全匹配 |
| **未匹配** | 任何名字部分相似度未达到 70% |

> 名字各部分的相似度阈值设为 70%。例如：“Christophel” 与 “Christopher” 完全匹配；“Chris” 与 “Christopher” 不匹配。

### 1x1 验证方式

| 匹配类型 | 名字 | 身份编号 |
|---|---|---|
| `full_match` | 名字和身份编号完全匹配 | 完全匹配 |
| `partial_match` | 名字或身份编号部分匹配 | 完全匹配 |
| `no_match` | 其他所有组合 | 不匹配 |

### 2x2 验证方式

需要对比 **两个独立的数据源**：

| 匹配类型 | 条件 |
|---|---|
| `full_match` | 两个数据源都确认名字和身份编号匹配 |
| `partial_match` | 至少一个数据源确认匹配 |
| `no_match` | 两个数据源均无法确认匹配 |

> 出生日期和身份编号的匹配必须完全一致，不允许模糊匹配。

---

## 警告标签

| 标签 | 说明 |
|---|---|
| `COULD_NOT_PERFORM_DATABASE_VALIDATION` | 缺少必要数据（身份证号码、姓名和国家信息） | 请提供这些信息 |
| `DATABASE_VALIDATION_PARTIAL_MATCH` | 找到部分匹配结果 | 需进一步调查 |
| `DATABASE_VALIDATION_NO_MATCH` | 政府记录中未找到匹配项 |

> 当触发 `COULD_NOT_PERFORM_DATABASE_VALIDATION` 时，会话状态将变为 “In Review”。提供缺失数据后，验证过程会自动重新启动。

---

## 支持的国家及验证方式

| 国家 | 验证方法 | 覆盖范围 | 必需输入 |
|---|---|---|---|
| 阿根廷 | 1x1 | 95% | 证件号码 |
| 玻利维亚 | 1x1 | 95% | 证件号码 + 出生日期 |
| 巴西 | 1x1 | 95% | 税务编号（CPF） |
| 智利 | 1x1 | 95% | 个人编号（RUT） |
| 哥伦比亚 | 1x1 | 95% | 证件号码 + 证件类型 |
| 哥斯达黎加 | 1x1 | 95% | 个人编号 |
| 多米尼加共和国 | 1x1 | 95% | 个人编号 |
| 厄瓜多尔 | 1x1 / 2x2 | 90-96% | 个人编号 |
| 萨尔瓦多 | 1x1 | 95% | 证件号码 + 出生日期 |
| 危地马拉 | 1x1 | 95% | 证件号码 |
| 洪都拉斯 | 1x1 | 95% | 证件号码 |
| 墨西哥 | 1x1 | 95% | 个人编号（CURP） |
| 巴拿马 | 1x1 | 95% | 证件号码 + 出生日期 |
| 巴拉圭 | 1x1 | 95% | 证件号码 |
| 秘鲁 | 1x1 / 2x2 | 95-99% | 个人编号 |
| 西班牙 | 1x1 | 95% | 个人编号 + 证件类型 + 有效期 |
| 乌拉圭 | 1x1 | 95% | 个人编号 + 出生日期 |
| 委内瑞拉 | 1x1 | 95% | 证件号码 |