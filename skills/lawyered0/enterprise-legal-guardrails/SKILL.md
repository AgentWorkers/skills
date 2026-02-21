---
name: enterprise-legal-guardrails
description: 针对 OpenClaw 的出站操作（如反垃圾邮件、诽谤、隐私保护、财务索赔等）的法律/合规保障措施。
---
# 企业法律防护机制（Enterprise Legal Guardrails）

使用此功能在发布、发送消息或公开任何可能引发法律/合规风险的内容之前，对机器人生成的输出进行预检查。

## 功能简介  
这是一个通用的**出站内容检查工具**，用于在任何应用程序中执行发布、评论、消息发送等操作之前进行审核。

## 使用场景  
- 在执行 `create_post`、`create_comment`、`send_message` 或类似的发布操作之前。  
- 在发布与市场相关的评论、战略声明或价格/确定性声明之前。  
- 在涉及人力资源或工作场所的敏感信息交流之前。  
- 在处理或公开个人身份信息之前。  

## 工作流程  
1. 起草文本内容。  
2. 使用相应的操作/配置文件运行检查工具。  
3. 如果检查结果为 **PASS** 或 **WATCH**，则继续执行；  
4. 如果检查结果为 **REVIEW**，则需要重新编写内容或提交给人工/法律部门审核；  
5. 如果检查结果为 **BLOCK**，则禁止执行该操作。  

此功能可作为所有发布内容的通用安全防护层。Babylon 只是当前的一个集成示例，并非该工具的主要用途。  

## 快速使用方法  
（具体使用方法请参考相应的代码块。）  

## 应用范围（全局过滤）  
该工具的适用范围由 `--app` 参数及以下环境变量决定（为兼容性保留了旧名称）：  
- `ENTERPRISE_LEGAL_GUARDRAILS_OUTBOUND_SCOPE`（`all` | `include` | `exclude`）  
- `ENTERPRISE_LEGAL_GUARDRAILS_OUTBOUND_APPS`（逗号分隔的应用程序列表）  
- `BABYLON_GUARDRAILS_SCOPE`  
- `BABYLON_GUARDRAILS_APPS`  

示例：  
- `all`：检查所有出站内容。  
- `include` + `whatsapp,email`：仅检查 WhatsApp 和 Email 应用程序。  
- `exclude` + `whatsapp,email,moltbook,babylon`：排除 WhatsApp、Email、moltbook 和 Babylon 应用程序之外的所有内容。  
如果未指定范围，默认值为 `all`。  

## 配置文件类型（profiles）  
- `social`：公共社交文本、评论、公告。  
- `antispam`：未经请求的邮件或协调性较强的信息。  
- `hr`：与工作场所、招聘、绩效或员工行为相关的内容。  
- `privacy`：包含个人身份信息和隐私披露的内容。  
- `market`：与市场/财务相关的声明。  
- `legal`：包含法律结论或相关表述的内容。  

如果未指定配置文件类型，系统会根据操作类型自动选择默认配置：  
- `post` | `comment` | `message` → `social,legal`  
- `trade` | `market-analysis` → `market,financial`  
- `generic` → `legal,social`  

## 输出结果  
- `PASS`：可以安全执行。  
- `WATCH`：风险较低；建议重新编写内容。  
- `REVIEW`：建议由人工或法律部门审核。  
- `BLOCK`：禁止执行。  

## 配置调整  
您可以通过环境变量（或直接运行时的 CLI 参数）调整审核的严格程度：  
- `ENTERPRISE_LEGAL_GUARDRAILS_REVIEW_THRESHOLD`（默认值：5）  
- `ENTERPRISE_LEGAL_GUARDRAILS_BLOCK_THRESHOLD`（默认值：9）  

**CLI 参数示例**：  
- `--review-threshold`  
- `--block-threshold`  

**旧环境变量别名**：  
- `ELG_*` 和 `BABYLON_GUARDRAILS_*`  

## 通用出站适配器（适用于无内置审核机制的工具）  
对于没有内置审核功能的工具（例如 Gmail、自定义网站发布系统或自定义消息机器人），请通过以下封装层来执行出站操作：  
（具体实现方式请参考相应的代码块。）  

## 兼容性说明  
在仍使用旧名称 `legal-risk-checker` 的 OpenClaw 工作空间中，该功能仍可正常使用。  

## 详细信息  
完整的规则集和修改建议请参阅 `references/guardrail-policy-map.md`。  

## 打包信息  
可下载的软件包位于：`dist/enterprise-legal-guardrails.skill`  

### `guard_and_run.py` 的安全增强措施  
对于非原生出站集成方案，应将 `guard_and_run` 视为一个执行边界。推荐使用的参数/环境变量如下：  
默认情况下，执行安全性基于允许列表进行控制。除非明确启用 `--allow-any-command`，否则封装层会强制执行允许列表的规则：  
- `--allow-any-command` / `ENTERPRISELEGAL_GUARDRAILS_ALLOW_ANY_COMMAND`：允许绕过允许列表（不安全，仅限紧急情况下使用）。  
- `--suppress-allow-any-warning` / `ENTERPRISELEGAL_GUARDRAILSSuppress_ALLOW_ANY_WARNING`：在启用 `--allow-any-command` 时抑制运行时的安全警告。  
- `--allow-any-command-reason` / `ENTERPRISELEGAL_GUARDRAILS_ALLOW_ANY_COMMAND_reason`：必须提供绕过允许列表的合理理由（建议格式：`SEC-1234: emergency fix`）。  
- `--allow-any-command-approval-token` / `ENTERPRISELEGAL_GUARDRAILS_ALLOW_ANY_COMMAND_APPROVAL_TOKEN`：绕过允许列表操作时必须提供的审批令牌（会存储在审计日志中）。  
- `--allow-any-command <exe...>` / `ENTERPRISELEGAL_GUARDRAILS_ALLOWED_COMMANDS`：允许执行的程序列表（支持逗号/空格分隔及通配符）。  
- `--execute` / `ENTERPRISELEGAL_GUARDRAILS_EXECUTE`：启用审核后的执行操作。  
- `--strict` / `ENTERPRISELEGAL_GUARDRAILS_STRICT`：将审核结果直接设置为“BLOCK”。  
- `--sanitize-env`  
- `--keep-env <VAR...>` / `--keep-env-prefix <PREFIX...>`  
- `--command-timeout`、`--checker-timeout`、`--max-text-bytes`  
- `--audit-log <file>` / `ENTERPRISELEGAL_GUARDRAILS_AUDIT_LOG`：这些参数用于确保执行安全、限制命令范围并记录操作日志（便于事后审计）。