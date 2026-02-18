---
name: enterprise-legal-guardrails
description: 针对 OpenClaw 外部操作的法律法规/合规性保障措施（反垃圾邮件、诽谤、隐私保护、财务索赔等方面）
---
# 企业法律防护机制（Enterprise Legal Guardrails）

使用此功能在发布、发送消息或公开任何可能引发法律/合规风险的内容之前，对机器人生成的输出进行预检查。

## 功能简介  
这是一个通用的**出站内容**审核工具，用于在任何应用程序中执行发布、评论、消息发送等操作之前对内容进行审核。

## 使用场景  
- 在执行 `create_post`、`create_comment`、`send_message` 等发布操作之前。  
- 在发布与市场相关的评论、战略声明或价格/确定性信息之前。  
- 在涉及人力资源或工作场所的沟通内容之前。  
- 在处理或公开个人身份信息之前。  

## 工作流程  
1. 起草文本内容。  
2. 使用相应的动作/配置文件运行审核工具。  
3. 如果审核结果为 **PASS** 或 **WATCH**，则继续执行后续操作。  
4. 如果审核结果为 **REVIEW**，则需要重新编写内容或提交给人工/法律部门审核。  
5. 如果审核结果为 **BLOCK**，则禁止执行该操作。  

此功能可作为所有发布内容的通用安全层，与 OpenClaw 集成使用。Babylon 只是其中一个集成示例，并非该工具的主要用途。  

## 快速使用方法  
（具体使用方法请参考相应的代码块。）  

## 应用范围（全局过滤）  
应用范围取决于通过 `--app` 参数传递的应用程序环境变量（为兼容性保留了旧名称）：  
- `ENTERPRISE_LEGAL_GUARDRAILS_OUTBOUND_SCOPE`（`all|include|exclude`）：所有内容；包含/排除某些应用  
- `ENTERPRISE_LEGAL_GUARDRAILS_OUTBOUND_APPS`（逗号分隔的应用程序列表）  
- `BABYLON_GUARDRAILS_SCOPE`  
- `BABYLON_GUARDRAILS_APPS`  

示例：  
- `all`：检查所有出站内容。  
- `include` + `whatsapp,email`：仅检查 WhatsApp 和 Email 应用。  
- `exclude` + `whatsapp,email,moltbook,babylon`：排除 WhatsApp、Email、moltbook 和 Babylon 应用之外的所有内容。  
如果未指定应用范围，默认为 `all`。  

## 配置文件类型（profile）  
- `social`：公开社交文本、评论、公告。  
- `antispam`：未经请求的邮件或协调性强的消息。  
- `hr`：与工作场所、招聘、绩效或员工行为相关的内容。  
- `privacy`：包含个人身份信息和隐私披露的内容。  
- `market`：市场/财务声明和结果说明。  
- `legal`：法律结论或相关表述。  
如果未指定配置文件类型，系统会根据操作类型自动选择默认配置：  
  - `post|comment|message` → `social,legal`  
  - `trade|market-analysis` → `market,financial`  
  - `generic` → `legal,social`  

## 审核结果  
- **PASS**：可以安全执行。  
- **WATCH**：风险较低；建议重新编写内容。  
- **REVIEW**：需要人工或法律部门审核。  
- **BLOCK**：禁止执行。  

## 配置调整  
您可以通过环境变量（或直接运行的 CLI 参数）调整审核的严格程度：  
- `ENTERPRISE_LEGAL_GUARDRAILS_REVIEW_THRESHOLD`（默认值：5）：审核通过的最低风险阈值。  
- `ENTERPRISE_LEGAL_GUARDRAILS_BLOCK_THRESHOLD`（默认值：9）：禁止执行的最低风险阈值。  

**CLI 参数示例：**  
- `--review-threshold`  
- `--block-threshold`  

**兼容性说明**  
对于没有内置审核机制的工具（如 Gmail、自定义网站发布系统或自定义消息机器人），请通过以下方式使用该工具：  
（具体实现方法请参考相应的代码块。）  

## 兼容性  
在仍使用旧名称 `legal-risk-checker` 的 OpenClaw 工作空间中，该功能仍可正常使用。  

## 详细信息  
完整的规则集和改写建议请参阅 `references/guardrail-policy-map.md`。  

## 分发包  
可下载的部署包位于：  
`dist/enterprise-legal-guardrails.skill`