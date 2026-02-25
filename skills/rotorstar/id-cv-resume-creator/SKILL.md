---
name: talent-de-platform
description: 使用 Work Deal Language 创建简历（CV）、搜索职位、匹配技能以及进行薪资谈判。提供多种模板，支持 PDF 格式导出；整个流程由人工审核以确保质量。AI 代理可使用免费 API——基础功能无需 API 密钥，高级功能则需要 Access-ID。关于路由器（Router）相关的技能，请参阅下方的领域特定技能说明以获取详细指导。
  Create CVs, search jobs, match skills, and negotiate via Work Deal Language.
  Several templates, PDF export, human-in-the-loop review. Free API for AI agents —
  basic use without API key, full features with Access-ID. Router skill — see
  domain-specific skills below for detailed instructions.
homepage: https://www.talent.de
license: Free-to-use
compatibility: Requires HTTP client and network access.
env_vars:
  TALENT_ACCESS_ID:
    required: false
    sensitive: true
    description: >-
      Access-ID for higher rate limits and advanced features (Template Create,
      Job Negotiate, Template Contest). Also used as HMAC secret for callback
      signature verification. Optional for CV Builder and Job Search.
metadata:
  openclaw:
    emoji: "\U0001F3AF"
  talent:
    category: career
    version: "5.2.2"
    api_base: https://www.talent.de/api
    credentials:
      access_id:
        required: per-skill
        format: "talent_agent_[a-z0-9]{4}"
        obtain: "POST /api/agent/register"
        env_var: "TALENT_ACCESS_ID"
        sensitive: true
        note: >-
          Free skills (CV Builder, Job Search) work without Access-ID at lower rate limits.
          Template Create, Job Negotiate, and Template Contest require an Access-ID.
          Also used as HMAC secret for callback signature verification.
          Store in environment variable TALENT_ACCESS_ID — do not hardcode.
  hitl:
    supported: true
    spec_version: "0.6"
    types: [confirmation, input, selection, approval, escalation]
    notifications: [polling, sse, callback]
    review_base_url: "https://www.talent.de/en/hitl/review"
    timeout_default: "24h"
    grace_period: "5min"
    discovery: "https://www.talent.de/.well-known/hitl.json"
    info: "May ask user to confirm context, enter data, select template, approve CV draft, or handle escalations."
---
# talent.de 平台

通过 API 功能，您可以创建简历、搜索职位、匹配技能以及协商工作条件。模板支持从传统的 PDF 格式到 3D 界面的多种形式。基础功能完全免费。

## 代理使用指南

> **必须进行人工审核（HITL，Human In The Loop）**。您必须选择以下选项之一：`"prefer_hitl": true`（建议采用人工审核）或 `"skip_hitl": true`（仅使用自动化流程）。如果两者都未设置，系统将返回 400 错误。如果有人工审核人员参与，请务必设置 `"prefer_hitl": true`。

> **数据使用原则：** 仅使用请求方明确提供或在本次交流中获批准的数据。

> **发送前：** 先向用户展示一份简要信息（姓名、职位、电子邮件），然后询问：“发送吗？还是需要我修改什么？”

> **令牌管理：** 将令牌视为密码一样重要，仅与请求方共享。

> **保持友好沟通：** 请参考 [用户沟通指南](skills/cv-builder/SKILL.md#user-communication)，了解每个步骤中的推荐信息。

## 认证信息

**访问 ID**（`talent_agent_[a-z0-9]{4}`）可用于解锁更高的请求速率限制和高级功能。对于简历生成和职位搜索功能，使用访问 ID 是**可选的**；但对于模板创建、职位协商和模板竞赛功能，访问 ID 是**必需的**。

**注册流程（免费，不传输用户数据）：**
```http
POST https://www.talent.de/api/agent/register
Content-Type: application/json

{ "agent_name": "my-agent" }
```

访问 ID 同时也用作回调 Webhook 中 `X-HITL-Signature` 的 HMAC 密钥。请妥善保管该密钥，切勿将其嵌入客户端代码或共享给其他代理。详情请参阅 [访问系统](skills/shared/access.md)。

## 快速入门

```http
POST https://www.talent.de/api/agent/cv-simple
Content-Type: application/json

{
  "prefer_hitl": true,
  "cv_data": {
    "firstName": "Alex",
    "lastName": "Johnson",
    "title": "Software Engineer",
    "email": "alex@example.com"
  }
}
```

**响应状态（202 表示需要人工审核）：**
```json
{
  "status": "human_input_required",
  "message": "Please confirm: is this CV for you?",
  "hitl": {
    "case_id": "review_a7f3b2c8d9e1f0g4",
    "review_url": "https://www.talent.de/en/hitl/review/review_a7f3b2c8d9e1f0g4?token=abc123...",
    "poll_url": "https://www.talent.de/api/hitl/cases/review_a7f3b2c8d9e1f0g4/status",
    "type": "confirmation"
  }
}
```

将 `review_url` 提供给用户，由用户选择模板并完成审核流程。之后继续执行后续步骤。完整的使用流程请参阅 [简历生成功能](skills/cv-builder/SKILL.md)。

## 功能列表

| 功能        | 使用场景                | 关键 API 端点            |
|------------|-------------------|-------------------|
| [简历生成](skills/cv-builder/SKILL.md) | 用户希望创建、编辑或导出简历     | `POST /api/agent/cv-simple`     |
| [职位搜索](skills/job-search/SKILL.md) | 用户希望查找职位或匹配简历       | `GET /api/agent/jobs`        |
| [职位协商](skills/job-negotiate/SKILL.md) | 用户希望协商工作条件或有条件申请职位 | `POST /api/agent/wdl/request`     |
| [模板创建](skills/template-create/SKILL.md) | 用户希望自定义 HTML 模板         | `POST /api/agent/template`       |
| [模板竞赛](skills/template-contest/SKILL.md) | 用户希望参与模板竞赛或展示作品     | —                      |

## 相关文档

- [访问系统](skills/shared/access.md)：请求速率限制与访问 ID 注册说明
- [错误代码](skills/shared/errors.md)：错误代码及排查方法
- [隐私政策](skills/shared/privacy.md)：数据保护与 GDPR 合规性说明

## 技术规范

- [agent.json](https://www.talent.de/.well-known/agent.json)：代理配置文件
- [hitl.json](https://www.talent.de/.well-known/hitl.json)：人工审核相关配置
- [llms.txt](https://www.talent.de/llms.txt)：机器学习模型相关文件