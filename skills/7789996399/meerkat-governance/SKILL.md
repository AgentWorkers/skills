---
name: meerkat-governance
description: >
  AI治理API，包含两个端点：  
  1. **防护端点（Shield）**：扫描未经信任的内容，以防止提示注入（prompt injection）和潜在威胁；验证AI生成的输出，确保其没有出现幻觉（hallucinations）、数值错误（numerical errors）或对原始数据的篡改（manipulation against source data）。  
  2. **验证端点（Verify）**：返回结构化的结果，包括信任评分（trust scores）以及相应的修复建议（remediation guidance），同时提供完整的审计追踪（full audit trail）。
homepage: https://meerkatplatform.com
metadata:
  clawdbot:
    emoji: "🔒"
    requires:
      env:
        - MEERKAT_API_KEY
    tags:
      - security
      - governance
      - safety
---
# Meerkat 管理框架

**功能范围：**  
该功能提供了两个 API 端点供您的代理程序调用。这些功能不会自动激活，也不会在后台运行；除非被代理程序明确请求，否则不会访问任何内容。开发者可以控制发送到 Meerkat 的内容类型。

**隐私与数据管理：**  
请参阅 [https://meerkatplatform.com/privacy](https://meerkatplatform.com/privacy) 以了解详细信息。  
Meerkat 会在内存中处理内容，并在响应完成后立即将其删除。仅会保留信任评分和元数据，不会保留原始内容。所有数据都不会被共享给第三方，所有处理操作均在加拿大境内完成。

**安全性：**  
您的 API 密钥用于验证对 Meerkat API 的请求。如果密钥被盗用，请通过管理面板及时更换新密钥。所有通信均使用 TLS 1.2+ 协议进行加密。Meerkat 的 API 端点托管在 Azure 容器应用上，并配备了受管理的 SSL 证书。在发送数据之前，请确认端点主机名（`api.meerkatplatform.com`）与 SSL 证书匹配。

## **Ingress Shield（入口防护）**  
`/v1/shield` 端点会扫描内容，检测是否存在提示注入、越狱攻击、数据泄露以及社会工程学攻击等威胁。对于开发者标记为“不可信”的内容，代理程序在处理之前会先调用该端点进行检测。常见的检测对象包括外部邮件、网络爬取的内容以及用户上传的文档。开发者还可以选择在代理程序安装前配置对该功能的启用。

**响应字段：**  
- `safe`（布尔值）：内容是否通过安全检测  
- `threat_level`：`NONE`、`LOW`、`MEDIUM`、`HIGH` 或 `CRITICAL`  
- `attack_type`：检测到的威胁类型（如有）  
- `detail`：人类可读的威胁描述  
- `sanitized_input`：已清除威胁的内容（如存在）  
- `audit_id`：审计记录的唯一标识符  

代理程序可以根据这些响应信息来决定如何处理内容。例如，被标记为 `HIGH` 或 `CRITICAL` 的内容可能会被阻止；被标记为 `MEDIUM` 的内容可能需要用户确认。如果返回了 `sanitized_input`，代理程序可以使用处理后的干净版本继续使用。

## **Egress Verify（出口验证）**  
`/v1/verify` 端点会使用最多五种机器学习算法（DeBERTa NLI、数值验证、语义熵分析、隐含偏好检测和声明提取）来验证 AI 生成的内容是否与原始数据一致。

**`domain` 字段：**  
该字段用于应用特定领域的规则。支持的领域包括：`healthcare`（医疗）、`financial`（金融）、`legal`（法律）、`general`（通用）。

**响应字段：**  
- `trust_score`（0-100）：所有检测项目的综合评分  
- `status`：`PASS`、`FLAG` 或 `BLOCK`  
- `checks`：各检测项目的评分、标记及详细信息  
- `remediation`：必要的修正措施及代理程序的操作指南（当状态为 `BLOCK` 时）  
- `audit_id`：审计记录的唯一标识符  
- `session_id`：用于关联重试尝试的会话标识符  

代理程序可以根据 `status` 和 `trust_score` 来决定是否继续处理内容。如果提供了 `remediation`，`agent_instruction` 字段会包含自我修正的指导信息，`corrections` 列出具体的错误（例如实际值与预期值的差异）。代理程序可以使用相同的 `session_id` 重新生成处理后的内容并重新提交。

## **观察模式（Observation Mode）**  
当未提供 `context` 字段时，Meerkat 会进入“观察模式”：仅检查内容的语义熵和隐含偏好，而跳过基于原始文档的验证。此时响应中的 `context_mode` 字段将为 `observation`。这种模式适用于没有原始文档的开放式内容生成场景。

## **审计跟踪（Audit Trail）**  
每次调用 `shield` 或 `verify` 功能时都会生成审计记录。通过 `/v1/audit/<audit_id>` 可以获取完整的审计记录。添加 `?include_session=true` 可以查看同一会话中的所有重试尝试。

## **设置说明：**  
1. 请访问 [https://meerkatplatform.com](https://meerkatplatform.com) 获取免费的 API 密钥（每月 10,000 次验证次数，无需信用卡）  
2. 设置环境变量：`MEERKAT_API_KEY=mk_live_your_key_here`  
3. 开发者可以通过代理程序的配置来控制发送到 Meerkat 的内容类型。对于不可信的外部内容，代理程序会在处理前调用 `shield` 端点；对于可能产生高风险的操作，会先调用 `verify` 端点。

**检测能力：**  
更多关于检测能力的详细信息，请参阅 [https://meerkatplatform.com/docs](https://meerkatplatform.com/docs)。  

**Ingress Shield** 能够检测以下威胁：提示注入、间接注入、数据泄露尝试、越狱攻击、角色劫持、凭证收集以及社会工程学攻击。  
**Egress Verify** 能够检测以下错误：虚假信息、数值失真（如药物剂量、财务数据、法律术语）、伪造的实体和引用、自欺式的陈述、偏见以及无根据的数字。

**API 响应头信息：**  
每个 API 响应都会包含以下头部信息：  
- `X-Meerkat-Usage`：当前的验证次数  
- `X-Meerkat-Limit`：每月的验证次数限制（或“无限制”）  
- `X-Meerkat-Remaining`：剩余的验证次数  
- `X-Meerkat-Warning`：当使用次数接近限制（80% 以上）时发出的警告  

**隐私政策：**  
Meerkat 仅对内容进行安全扫描，不会长期存储任何数据。您的 API 密钥仅限于您的组织使用。详情请参阅 [https://meerkatplatform.com/privacy](https://meerkatplatform.com/privacy)。