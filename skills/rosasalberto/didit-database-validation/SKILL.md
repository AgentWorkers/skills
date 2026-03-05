---
name: didit-database-validation
description: 将 Didit 数据库验证 API 集成到系统中，以核对个人数据与政府数据库的信息是否一致。当用户需要验证身份信息（如与政府记录对比）、检查国民身份证号码（CPF/CURP/DNI/cedula 等）、通过官方渠道验证身份证明文件，或针对拉丁美洲及西班牙地区的身份证明文件进行数据库验证时，可使用该 API。该 API 支持 18 个国家，并提供 1x1 和 2x2 两种匹配方式。
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
# Didit数据库验证API

## 概述

该API用于将个人数据和身份证明文件与可信的政府和金融数据库进行比对，以防止身份欺诈，并确保身份的真实性。

**主要要求：**
- 至少需要目标国家的**国民身份证/证件号码**。
- 支持的国家范围：**18个国家**（主要位于拉丁美洲及西班牙）。
- 返回结果类型：`full_match`（完全匹配）、`partial_match`（部分匹配）或`no_match`（未匹配）。
- 仅对**成功的查询**收取费用；数据不足时免费。

**匹配方法：**

| 方法 | 描述 | 起价 |
|---|---|---|
| **1x1** | 单一数据源验证 | $0.05 |
| **2x2** | 两个数据源交叉验证 | $0.30 |

**API参考文档：** https://docs.didit.me/standalone-apis/database-validation  
**功能指南：** https://docs.didit.me/core-technology/database-validation/overview  
**支持的国家：** https://docs.didit.me/core-technology/database-validation/database-validation-supported-countries  

---

## 认证

所有请求都必须包含`x-api-key`头部。您可以从[Didit业务控制台](https://business.didit.me) → API & Webhooks获取API密钥，或通过程序化注册获取（详见下文）。

## 入门（尚未注册账户？）

如果您还没有Didit API密钥，可以通过以下两个API调用进行注册：
1. **注册：** `POST https://apx.didit.me/auth/v2/programmatic/register/`，传入`{"email": "you@gmail.com", "password": "MyStr0ng!Pass"}`
2. 系统会发送一封包含6位OTP验证码的邮件到您的邮箱。
3. **验证邮箱：** `POST https://apx.didit.me/auth/v2/programmatic/verify-email/`，传入`{"email": "you@gmail.com", "code": "A3K9F2"`，响应中会包含`api_key`。

**查看余额或充值：**
- `GET /v3/billing/balance/` 用于查看余额。
- `POST /v3/billing/top-up/`，传入`{"amount_in_dollars": 50}`，可获取Stripe支付链接。

有关平台管理的更多信息（工作流程、会话、用户、账单等），请参阅`didit-verification-management`技能文档。

---

## API端点

```
POST https://verification.didit.me/v3/database-validation/
```

### 请求头

| 头部字段 | 值 | 是否必填 |
|---|---|---|
| `x-api-key` | 您的API密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON格式）

| 参数 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `id_number` | 字符串 | 是 | 全球唯一的标识号码，系统会自动匹配到相应的国家字段 |
| `first_name` | 字符串 | 否 | 用于匹配的名字 |
| `last_name` | 字符串 | 否 | 用于匹配的姓氏 |
| `date_of_birth` | 字符串 | 否 | 出生日期（格式为`YYYY-MM-DD`，部分国家要求提供） |
| `issuing_state` | 字符串 | 否 | ISO 3166-1国家代码（3位字母） |
| `save_api_request` | 布尔值 | 否 | 是否将请求保存到业务控制台 |
| `vendor_data` | 字符串 | 否 | 用于会话跟踪的标识符 |

`id_number`字段会自动映射到对应国家的特定字段：

| 国家 | 映射字段 | 证件类型 | 格式 |
|---|---|---|---|
| ARG | `document_number` | DNI | — |
| BOL | `document_number` | CI | — |
| BRA | `tax_number` | CPF | 11位数字 |
| CHL | `personal_number` | RUT | — |
| COL | `personal_number` | Cedula | — |
| CRI | `personal_number` | Cedula | — |
| DOM | `personal_number` | Cedula | 11位数字 |
| ECU | `personal_number` | Cedula | 10位数字 |
| ESP | `personal_number` | DNI/NIE | — |
| GTM | `document_number` | DPI | — |
| HND | `document_number` | DNI | — |
| MEX | `personal_number` | CURP | 18位字符 |
| PAN | `document_number` | Cedula | — |
| PER | `personal_number` | DNI | 8位数字 |
| PRY | `document_number` | CI | — |
| SLV | `document_number` | DUI | — |
| URY | `personal_number` | CI | — |
| VEN | `document_number` | Cedula | — |

### 示例请求

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

### 响应（200 OK）

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 与政府记录完全匹配 | 身份验证通过 |
| `"Declined"` | 未找到匹配项 | 身份无法验证 |
| `"In Review"` | 部分匹配或数据不足 | 需重新审核数据 |

### 错误响应

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 请检查目标国家的身份证号码格式 |
| `401` | API密钥无效 | 请检查`x-api-key`头部字段 |
| `403` | 余额不足 | 请在business.didit.me充值 |

---

## 匹配逻辑

### 名字匹配

| 结果 | 匹配条件 |
|---|---|
| **完全匹配** | 名字完全匹配（Levenshtein相似度达到85%），或名字和姓氏都完全匹配 |
| **部分匹配** | 名字的任意部分完全匹配 |
| **未匹配** | 任何部分都没有达到70%的相似度 |

> 名字的每个组成部分都需满足70%的Levenshtein相似度要求。例如：“Christophel”与“Christopher”完全匹配；“Chris”与“Christopher”不匹配。

### 单一数据源匹配（1x1）

| 匹配类型 | 名字 | 身份号码 |
|---|---|---|
| `full_match` | 名字和身份号码完全匹配 | 完全匹配 |
| `partial_match` | 名字或身份号码部分匹配 | 完全匹配 |
| `no_match` | 其他所有组合 | 不匹配 |

### 双数据源匹配（2x2）

需要对比**两个独立的数据源**：

| 匹配类型 | 条件 |
|---|---|
| `full_match` | 两个数据源均确认名字和身份号码匹配 |
| `partial_match` | 至少一个数据源确认名字或身份号码匹配 |
| `no_match` | 两个数据源均无法确认 |

> 出生日期和身份号码的匹配必须完全一致，不允许模糊匹配。

---

## 警告标签

| 标签 | 说明 |
|---|---|
| `COULD_NOT_PERFORM_DATABASE_VALIDATION` | 缺少必要数据（身份证号码、姓名和国家信息） |
| `DATABASE_VALIDATION_PARTIAL_MATCH` | 发现部分匹配 | 需进一步调查 |
| `DATABASE_VALIDATION_NO_MATCH` | 政府记录中未找到匹配项 |

> 当出现`COULD_NOT_PERFORM_DATABASE_VALIDATION`时，会话状态会变为“In Review”。提供缺失的数据后，验证会自动重新触发。

---

## 支持的国家及匹配方法

| 国家 | 使用的方法 | 支持的匹配程度 | 必需输入的信息 |
|---|---|---|---|
| 阿根廷 | 1x1 | 95% | 证件号码 |
| 玻利维亚 | 1x1 | 95% | 证件号码 + 出生日期 |
| 巴西 | 1x1 | 95% | 税务号码（CPF） |
| 智利 | 1x1 | 95% | 个人号码（RUT） |
| 哥伦比亚 | 1x1 | 95% | 证件号码 + 类型 |
| 哥斯达黎加 | 1x1 | 95% | 个人号码 |
| 多米尼加共和国 | 1x1 | 95% | 个人号码 |
| 厄瓜多尔 | 1x1 / 2x2 | 90-96% | 个人号码 |
| 萨尔瓦多 | 1x1 | 95% | 证件号码 + 出生日期 |
| 危地马拉 | 1x1 | 95% | 证件号码 |
| 洪都拉斯 | 1x1 | 95% | 证件号码 |
| 墨西哥 | 1x1 | 95% | 个人号码（CURP） |
| 巴拿马 | 1x1 | 95% | 证件号码 + 出生日期 |
| 巴拉圭 | 1x1 | 95% | 证件号码 |
| 秘鲁 | 1x1 / 2x2 | 95-99% | 个人号码 |
| 西班牙 | 1x1 | 95% | 个人号码 + 证件类型 + 有效期 |
| 乌拉圭 | 1x1 | 95% | 个人号码 + 出生日期 |
| 委内瑞拉 | 1x1 | 95% | 证件号码 |

---

## 实用脚本

**validate_database.py**：通过命令行从政府数据库验证身份信息。

```bash
# Requires: pip install requests
export DIDIT_API_KEY="your_api_key"
python scripts/validate_database.py --id-number 12345678 --country PER --first-name Carlos --last-name Garcia
python scripts/validate_database.py --id-number GARC850315HDFRRL09 --country MEX
```