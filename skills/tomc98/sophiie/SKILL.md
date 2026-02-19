---
name: sophiie
description: 通过 Sophiie 的 REST API，您可以管理 Sophiie 的销售流程，包括潜在客户、咨询请求、预约安排、常见问题解答、政策文档、短信发送以及电话通话等。
metadata:
  openclaw:
    requires:
      env:
        - SOPHIIE_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SOPHIIE_API_KEY
    emoji: "📞"
    homepage: https://docs.sophiie.ai
    files:
      - SKILL.md
      - README.md
      - scripts/sophiie.sh
---
# Sophiie — 销售流程管理

Sophiie 是一个用于销售流程管理的 B2B SaaS 平台。企业可以使用该平台中的 AI 驱动虚拟助手来处理电话、短信和潜在客户管理任务。通过这个技能，您可以使用自然语言来管理 Sophiie 的销售流程。

## 认证

所有请求都使用 `Authorization: Bearer <key>` 进行认证，其中 `key` 为 `SOPHIIE_API_KEY`。API 密钥的前缀分为 `sk_live_*`（生产环境）和 `sk_test_*`（测试环境）。

- **基础 URL**：`https://api.sophiie.ai`
- **请求频率限制**：每分钟 60 次请求
- **所有响应格式**：JSON

## 外部接口

| 方法 | URL | 发送的数据 |
|--------|-----|-----------|
| GET | `https://api.sophiie.ai/v1/leads` | 查询参数：page, limit |
| GET | `https://api.sophiie.ai/v1/leads/{id}` | 无 |
| POST | `https://api.sophiie.ai/v1/leads` | 请求体：firstName, lastName, email, phone, suburb, businessName, socials |
| PUT | `https://api.sophiie.ai/v1/leads/{id}` | 请求体：firstName, lastName, email, phone, suburb, businessName, socials |
| DELETE | `https://api.sophiie.ai/v1/leads/{id}` | 无 |
| GET | `https://api.sophiie.ai/v1/leads/{id}/notes` | 查询参数：page, limit |
| GET | `https://api.sophiie.ai/v1/leads/{id}/activities` | 查询参数：page, limit |
| GET | `https://api.sophiie.ai/v1/inquiries` | 查询参数：page, limit, leadId, expand |
| GET | `https://api.sophiie.ai/v1/inquiries/{id}` | 无 |
| GET | `https://api.sophiie.ai/v1/appointments` | 查询参数：page, limit, leadId |
| POST | `https://api.sophiie.ai/v1/calls` | 请求体：name, phoneNumber, mode, customInstructions |
| POST | `https://api.sophiie.ai/v1/sms` | 请求体：userId, leadId, message, messageThreadId |
| GET | `https://api.sophiie.ai/v1/faqs` | 查询参数：page, limit |
| POST | `https://api.sophiie.ai/v1/faqs` | 请求体：question, answer, isActive |
| PUT | `https://api.sophiie.ai/v1/faqs/{id}` | 请求体：question, answer, isActive |
| DELETE | `https://api.sophiie.ai/v1/faqs/{id}` | 无 |
| GET | `https://api.sophiie.ai/v1/policies` | 查询参数：page, limit |
| POST | `https://api.sophiie.ai/v1/policies` | 请求体：title, content, isActive |
| PUT | `https://api.sophiie.ai/v1/policies/{id}` | 请求体：title, content, isActive |
| DELETE | `https://api.sophiie.ai/v1/policies/{id}` | 无 |
| GET | `https://api.sophiie.ai/v1/members` | 查询参数：page, limit |
| GET | `https://api.sophiie.ai/v1/organization` | 无 |
| GET | `https://api.sophiie.ai/v1/organization/availability` | 无 |
| GET | `https://api.sophiie.ai/v1/organization/members` | 查询参数：page, limit |
| GET | `https://api.sophiie.ai/v1/organization/services` | 无 |
| GET | `https://api.sophiie.ai/v1/organization/products` | 无 |

## 安全性与隐私

- `SOPHIIE_API_KEY` **绝不会** 被记录、打印或显示在输出中。
- 所有请求仅使用 **HTTPS** 协议。
- 所有数据都不会被本地缓存——每个请求都会直接从 API 获取最新数据。
- 所有用户输入都会通过 `jq -n` 进行清洗（不会被插入到 JSON 请求体中）。
- 该技能对 `SOPHIIE_API_KEY` 只具有 **只读** 权限——无法修改或删除该环境变量。

## 命令参考

所有命令通过 `scripts/sophiie.sh <domain> <action> [options>` 来执行。

### 潜在客户（ Leads）

**`leads list`** — 列出所有潜在客户
**`leads get <id>`** — 获取特定潜在客户的详细信息
**`leads create`** — 创建新的潜在客户
**`leads update <id>` **更新现有潜在客户的详细信息**
**`leads delete <id>` **删除潜在客户**

### 咨询（Inquiries）

**`inquiries list` **列出所有咨询记录**
**`inquiries get <id>` **获取特定咨询的详细信息**

### 常见问题（FAQs）

**`faqs list` **列出所有常见问题**
**`faqs create` **创建新的常见问题**
**`faqs update <id>` **更新常见问题**

### 政策（Policies）

**`policies list` **列出所有政策**
**`policies create` **创建新的政策**
**`policies update <id>` **更新政策**
**`policies delete <id>` **删除政策**

### 通信（Communication）

**`calls send` **发起外拨电话**
**`sms send` **发送短信**

### 日程安排（Appointments）

**`appointments list` **列出所有日程安排**

### 组织（Organization）

**`org get` **获取组织信息**
**`org availability` **获取营业时间**
**`org members` **列出组织成员及其角色**
**`org services` **列出提供的服务**
**`org products` **列出产品目录**

## 分页

所有列表接口都会返回分页结果：
- 默认：第 1 页，每页 50 条记录
- 最大每页显示 100 条记录
- **务必检查 `totalPages` — 如果有更多页面，请告知用户并提供获取下一页的选项

## 错误代码及提示

| 错误代码 | 错误原因 | 应向用户显示的提示 |
|------|---------|----------------------|
| 401 | API 密钥无效或缺失 | “您的 API 密钥似乎无效。请检查 SOPHIIE_API_KEY。” |
| 404 | 资源未找到 | “该潜在客户/咨询记录等未找到。请重新输入 ID。” |
| 409 | 数据重复 | “已存在具有相同信息的潜在客户。” |
| 429 | 请求频率限制 | “请求过多。请稍后再试。” |
| 500 | 服务器错误 | “Sophiie 侧出现故障。请稍后再试。” |

错误响应的格式如下：