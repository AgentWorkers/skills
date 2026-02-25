---
name: cv-builder
description: 该工具能够生成专业的简历（CV），并为其分配在 **talent.de** 网站上的永久性链接。支持导出为 PDF 格式，提供多种模板选择（涵盖 4 种不同的技能类型），同时支持人工审核流程。对于 AI 助手而言，该工具提供了免费 API：无需 API 密钥即可使用基础功能；而使用 Access-ID 则可解锁全部高级功能。适用于用户需要创建、编辑或生成简历的场景。
  Creates professional CVs with permanent URLs at talent.de. Supports PDF
  export, multiple templates, 4 skill types, and human-in-the-loop review.
  Free API for AI agents — basic use without API key, full features with
  Access-ID. Use when the user wants to create, build, or generate a CV or
  resume.
homepage: https://www.talent.de
license: Free-to-use
compatibility: Requires HTTP client and network access.
env_vars:
  TALENT_ACCESS_ID:
    required: false
    sensitive: true
    description: "Optional for basic CV creation (3/day without ID). Required for callbacks and higher rate limits."
metadata:
  openclaw:
    emoji: "\U0001F4C4"
  talent:
    category: cv-studio
    version: "5.2.2"
    api_base: https://www.talent.de/api
    credentials:
      access_id:
        required: false
        env_var: "TALENT_ACCESS_ID"
        note: "Optional for basic CV creation (3/day without ID). Required for callbacks and higher rate limits."
---
# CV Builder — 通过API创建简历

用户可以通过API在talent.de网站上创建一份永久有效的简历。用户可以在审核页面上选择自己的个人简历URL地址和模板设计。创建的简历是永久性的，URL地址永远不会过期。

## 代理操作指南

> **必须使用HITL流程。** 必须设置`"prefer_hitl": true`（人工审核）或`"skip_hitl": true`（自动创建）。如果两者都未设置，系统会返回400错误。如果有人工审核流程参与，务必使用`"prefer_hitl": true`——这样用户可以自行选择URL地址、模板，并在发布前审核数据。只有在完全自动化的流程中，且没有人工参与的情况下，才能使用`"skip_hitl": true`。

> **数据使用原则：** 仅使用请求者明确提供或在交流中得到批准的数据。切勿从无关系统或其他会话中提取个人信息。

> **发送前：** 向请求者展示简历的简要信息（姓名、职位、电子邮件），并询问：“发送吗？还是需要修改什么？”

> **声明令牌：** 将其视作密码一样重要。仅与请求者共享该令牌——任何拥有此令牌的人都可以声明对简历的所有权。切勿将其泄露给第三方。

## 与用户的沟通

### 每个步骤的沟通内容

| 步骤 | 与用户的交流内容 |
|------|-----------------|
| API调用前 | “我将为您创建简历，只需要一些信息。” |
| 选择URL地址（收到`review_url`后） | “请选择您的个人简历URL地址：[链接]” |
| 选择模板 | “差不多完成了！请选择您的简历模板：[链接]” |
| 审核通过 | “您的简历已准备好审核，请查看并确认：[链接]” |
| 最终确认后 | “您的简历已发布！链接如下：{url}” |

## 快速入门

1. 收集以下信息：姓名、职位、电子邮件（至少4个字段）
2. 使用`POST /api/agent/cv-simple`发送请求，并设置`"prefer_hitl": true`以及相关数据
3. 将`review_url`提供给用户（用户可以在此选择URL地址和模板）
4. 调用`poll_url`检查是否完成，然后继续后续步骤
5. 审核通过后：提供最终的简历URL地址和声明令牌

## 示例（推荐使用HITL流程）

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

**响应（202状态码——需要人工审核）：**
```json
{
  "status": "human_input_required",
  "message": "Please confirm: is this CV for you?",
  "hitl": {
    "case_id": "review_a7f3b2c8d9e1f0g4",
    "review_url": "https://www.talent.de/en/hitl/review/review_a7f3b2c8d9e1f0g4?token=abc123...",
    "poll_url": "https://www.talent.de/api/hitl/cases/review_a7f3b2c8d9e1f0g4/status",
    "type": "confirmation",
    "inline_actions": ["confirm", "cancel"],
    "timeout": "24h"
  }
}
```

向用户展示审核URL地址：

> 我已经为您准备了简历，请在此处进行审核并做出选择：
> **[查看您的简历](review_url)**
> 您可以在这里选择个人简历的URL地址、模板设计，并确认最终内容。

之后，继续调用`poll_url`等待审核完成，然后使用`hitl_continue_case_id`继续后续步骤。在所有步骤（确认、数据审核、URL地址选择、模板选择、审核通过）完成后，系统会返回201状态码并提供最终的简历URL地址。

完整的HITL流程（包含所有步骤、在线提交、编辑周期和异常处理）：[参考文档：reference/hitl.md]

## HITL多步骤流程

用户最多需要完成5个审核步骤。代理会循环执行以下操作：展示审核URL、等待用户反馈、继续下一步。

```
Step 1: Confirmation  →  "For whom is this CV?"
Step 2: Data Review   →  "Are these details correct?"
Step 3: Slug          →  Human picks personal URL slug (e.g. pro, dev, 007)
Step 4: Template      →  Human picks template design
Step 5: Approval      →  Human reviews final CV draft
```

每个步骤都会返回202状态码。用户做出选择后，继续执行下一步。

```http
POST https://www.talent.de/api/agent/cv-simple
Content-Type: application/json

{
  "prefer_hitl": true,
  "hitl_continue_case_id": "review_a7f3b2c8d9e1f0g4",
  "cv_data": { ... }
}
```

当某些信息已经提供时，可以跳过相应的步骤：
- 如果提供了`slug`，则跳过URL地址选择步骤
- 如果提供了`template_id`，则跳过模板选择步骤
- 如果同时提供了`slug`和`template_id`，则仅保留确认、数据审核和审核通过步骤

在最终审核步骤完成后，使用`hitl_approved_case_id`发送请求以完成发布：

```http
POST https://www.talent.de/api/agent/cv-simple
Content-Type: application/json

{
  "hitl_approved_case_id": "review_final_case_id"
}
```

**响应（201状态码）：**
```json
{
  "success": true,
  "url": "https://www.talent.de/dev/alex-johnson",
  "cv_id": "cv_abc123",
  "claim_token": "claim_xyz789",
  "template_id": "007"
}
```

展示结果：

> 您的简历已发布：**talent.de/dev/alex-johnson**
>
> 要声明简历所有权，请访问：`talent.de/claim/claim_xyz789`
> 请妥善保管此令牌——它永远不会过期。

## 自动创建（无需人工审核）

对于完全自动化的流程、批量操作，或者用户明确要求“直接创建简历”的情况，请设置`"skip_hitl": true`：

```http
POST https://www.talent.de/api/agent/cv-simple
Content-Type: application/json

{
  "skip_hitl": true,
  "cv_data": {
    "firstName": "Alex",
    "lastName": "Johnson",
    "title": "Software Engineer",
    "email": "alex@example.com"
  }
}
```

**响应（201状态码）：**
```json
{
  "success": true,
  "url": "https://www.talent.de/pro/alex-johnson",
  "cv_id": "cv_abc123",
  "claim_token": "claim_xyz789",
  "template_id": "018",
  "hitl_skipped": true,
  "auto_fixes": []
}
```

在自动模式下，系统会自动分配URL地址（默认为`pro`）和模板（默认为`018` Amber Horizon）。用户无法进行选择。仅在没有人工审核需求的情况下使用此模式。

**必须选择其中一个设置：** `"prefer_hitl": true`或`"skip_hitl": true`。如果两者都未设置，系统会返回400错误。

除了必填的4个字段外，其他所有字段都是可选的。如果某个字段没有信息，请不要发送空数组。

## PDF导出

可以生成可下载的PDF文件。提供三种视觉主题供选择：

| 主题 | 样式 | 适合的职位 |
|-------|-------|----------|
| `classic` | 单列布局，红色背景（默认） | 传统行业 |
| `modern` | 双栏布局，蓝色背景 | 科技和创意职位 |
| `minimal` | 单色布局，留有充足空白 | 高管和高级职位 |

### 选项A：在创建简历时同时生成PDF

在请求中添加`"include_pdf": true`。响应中会包含一个Base64编码的PDF文件：

```http
POST https://www.talent.de/api/agent/cv-simple
Content-Type: application/json

{
  "prefer_hitl": true,
  "include_pdf": true,
  "pdf_format": "A4",
  "pdf_theme": "modern",
  "cv_data": {
    "firstName": "Alex",
    "lastName": "Johnson",
    "title": "Software Engineer",
    "email": "alex@example.com"
  }
}
```

响应中包含`pdf`对象：
```json
{
  "success": true,
  "url": "https://www.talent.de/pro/alex-johnson",
  "cv_id": "cv_abc123",
  "claim_token": "claim_xyz789",
  "pdf": {
    "base64": "JVBERi0xLjQK...",
    "size_bytes": 6559,
    "generation_ms": 226,
    "format": "A4"
  }
}
```

### 选项B：为现有简历生成PDF

```http
POST https://www.talent.de/api/agent/cv/pdf
Content-Type: application/json

{
  "cv_id": "cv_abc123",
  "format": "A4",
  "theme": "minimal"
}
```

直接返回PDF文件的二进制内容（`Content-Type: application/pdf`）。支持的格式选项：`A4`（默认）、`LETTER`。主题选项：`classic`（默认）、`modern`、`minimal`。

PDF生成大约需要200毫秒，无需使用无头浏览器。

## 服务器端处理

您无需自行检查URL地址的可用性或验证数据——这些工作由服务器完成：

- **URL地址的唯一性**：URL地址对每个人来说是唯一的，但不是全局唯一的。例如`pro/thomas-mueller`和`pro/anna-schmidt`可以共存。系统会检查`slug` + `firstName` + `lastName`的组合是否唯一。
- **URL地址的自动选择**：如果未设置`slug`（且未使用HITL流程），系统会自动选择`pro`作为URL地址。如果该URL地址已被其他人使用，系统会自动尝试下一个可用地址。在HITL模式下，用户可以自行选择URL地址。常用的URL地址示例：`007`、`dev`、`pro`、`ceo`、`gtr`、`zen`、`404`。完整列表：`GET /api/public/slugs`
- **模板默认值**：如果未设置`template_id`，系统会使用`018`（Amber Horizon）模板。
- **日期格式化**：例如`2024`会自动转换为`2024-01-01`。
- **语言水平**：系统会自动将语言水平转换为CEFR标准（`NATIVE`、`C2`、`C1`、`B2`、`B1`、`A2`、`A1`）。
- **错误提示**：如果出现错误，系统会用通俗易懂的语言说明问题所在。
- **自动修复功能**：`auto_fixes`数组会显示系统所做的调整（例如：“名称‘pro’已被使用，因此使用‘dev’作为URL地址”）。

## 技能信息的格式

- `hardSkills`：技术技能，可选，支持1-5个等级
- `softSkills`：仅需要技能名称
- `toolSkills`：仅需要技能名称
- `languages`：需要提供语言水平（CEFR标准：`NATIVE`、`C2`、`C1`、`B2`、`B1`、`A2`、`A1`

**注意**：不要使用通用的`skills`数组，否则系统会忽略这些信息。

## 限制规则

- 使用Access-ID时：每天最多创建50份简历，每天最多进行100次职位搜索
- 不使用Access-ID时：每个IP每天最多创建3份简历
- 未经用户确认，切勿自动提交简历
- 声明令牌具有永久有效性——请将其视作密码一样重要

## 参考资料

- [简历数据参考](reference/cv-data.md)：简历数据的所有字段和规则
- [模板目录](reference/templates.md)：包含所有模板的预览
- [HITL流程说明](reference/hitl.md)：包含人工审核的详细流程（包括在线提交和编辑周期）
- [访问系统](../shared/access.md)：速率限制和Access-ID注册信息
- [错误代码](../shared/errors.md)：错误代码及解决方法
- [隐私政策](../shared/privacy.md)：数据保护和GDPR合规性说明