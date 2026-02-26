---
name: meerkat-governance
description: >
  AI治理API，包含两个终端点：  
  1. **内容扫描功能**：扫描不可信内容，检测是否存在提示注入（prompt injection）或威胁行为。  
  2. **AI输出验证功能**：验证AI生成的输出是否存在幻觉（hallucinations）、数值错误（numerical errors）或对原始数据的篡改（manipulation against source data）。  
  该API会返回结构化结果，其中包含信任评分（trust scores）及相应的修复建议（remediation guidance），同时提供完整的审计追踪（full audit trail）。
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
# Meerkat 政策与功能

**范围：**  
该功能提供了两个 API 端点供您的代理程序调用。该功能不会自动激活，也不会在后台运行；除非被代理程序明确调用，否则不会访问任何内容。开发者可以控制发送到 Meerkat 的内容类型。

**隐私与数据处理：**  
https://meerkatplatform.com/privacy  
Meerkat 在内存中处理内容，并在响应完成后立即将其删除。仅会存储信任评分和元数据，不会保留任何原始内容。所有数据都不会共享给第三方，所有处理过程均在加拿大完成。

**安全性：**  
您的 API 密钥用于验证对 Meerkat API 的请求。如果密钥被盗用，应通过控制面板及时更换密钥。所有通信均采用 TLS 1.2+ 协议进行加密。Meerkat 的 API 端点托管在 Azure Container Apps 上，并使用受管理的 SSL 证书。在发送数据之前，请确认端点主机名（api.meerkatplatform.com）与 SSL 证书一致。

## **Ingress Shield（入口防护）**  
 `/v1/shield` 端点会扫描内容，检测是否存在提示注入、越狱尝试、数据泄露以及社会工程攻击等威胁。当代理程序处理被标记为“不可信”的内容时，可以调用该端点。常见的需要检测的内容包括外部邮件、网页抓取的内容以及用户上传的文档。开发者可以选择在代理程序安装前配置该功能以对其进行防护。

**响应字段：**  
- `safe`（布尔值）：内容是否通过了安全扫描  
- `threat_level`：`NONE`、`LOW`、`MEDIUM`、`HIGH` 或 `CRITICAL`  
- `attack_type`：检测到的威胁类型（如有）  
- `detail`：人类可读的威胁描述  
- `sanitized_input`：已清除威胁的内容（如有的话）  
- `audit_id`：审计记录的唯一标识符  

代理程序可以根据这些响应信息来决定如何处理内容。例如，被标记为 `HIGH` 或 `CRITICAL` 的内容可能会被阻止；被标记为 `MEDIUM` 的内容可能需要用户确认。如果返回了 `sanitized_input`，代理程序可以使用处理后的版本。

## **Egress Verify（出口验证）**  
 `/v1/verify` 端点会使用最多五种机器学习方法（DeBERTa NLI、数值验证、语义熵分析、隐式偏好检测和声明提取）来验证 AI 生成的内容是否与原始数据一致。  

**`domain` 字段：**  
该字段用于应用特定领域的规则。支持的域包括：`healthcare`（医疗）、`financial`（金融）、`legal`（法律）、`general`（通用）。  

**响应字段：**  
- `trust_score`（0-100）：所有检测结果的综合评分  
- `status`：`PASS` 或 `FLAG`（严重程度通过 `trust_score` 和 `remediation.severity` 表示）  
- `checks`：各检测项目的评分、标记和详细信息  
- `remediation`：需要进行的修正措施及代理程序的操作指南（当 `status` 为 `FLAG` 时）  
- `audit_id`：审计记录的唯一标识符  
- `session_id`：用于关联重试尝试的会话标识符  

代理程序可以根据 `status` 和 `trust_score` 来决定是否继续处理内容。当 `remediation` 字段存在时，`agent_instruction` 中会包含自我修正的指导信息，`corrections` 列出具体的错误（例如实际值与预期值的差异）。代理程序可以使用相同的 `session_id` 重新生成内容并重新提交。

## **观察模式（Observation Mode）**  
当未提供 `context` 字段时，Meerkat 会进入“观察模式”：仅检查内容的语义熵和隐式偏好，跳过基于原始文档的验证。此时响应中的 `context_mode` 字段将为 `observation`。这种模式适用于没有原始文档的开放式生成场景。

## **审计跟踪（Audit Trail）**  
每次使用 `Ingress Shield` 或 `Egress Verify` 功能时都会生成审计记录。通过 `/v1/audit/<audit_id>` 可以获取完整的审计记录。添加 `?include_session=true` 可以查看同一会话中的所有重试尝试。

## **设置说明：**  
1. 请访问 https://meerkatplatform.com 获取免费 API 密钥（每月 10,000 次验证次数，无需信用卡）  
2. 设置环境变量：`MEERKAT_API_KEY=mk_live_your_key_here`  
3. 开发者可以通过代理程序的配置来控制发送到 Meerkat 的内容类型。代理程序在处理不可信的外部内容前会调用 `shield` 端点，在执行高风险操作前会调用 `verify` 端点。  

**检测能力：**  
详细检测能力请参见 https://meerkatplatform.com/docs。  

**Ingress Shield** 可检测：提示注入、间接注入、数据泄露尝试、越狱行为、角色劫持、凭证收集以及社会工程攻击。  
**Egress Verify** 可检测：虚假信息、数值错误（如药物剂量、财务数据、法律术语）、伪造的实体和引用、带有偏见的陈述以及无根据的数字。

**API 响应头信息：**  
每个 API 响应都包含以下头部信息：  
- `X-Meerkat-Usage`：当前的验证次数  
- `X-Meerkat-Limit`：每月的验证次数限制（或“无限制”）  
- `X-Meerkat-Remaining`：剩余的验证次数  
- `X-Meerkat-Warning`：当使用次数接近限制（80% 以上）时发出的警告  

**隐私政策：**  
Meerkat 仅将内容用于安全扫描，不会长期存储。您的 API 密钥仅限于您的组织使用。详情请参阅 https://meerkatplatform.com/privacy。