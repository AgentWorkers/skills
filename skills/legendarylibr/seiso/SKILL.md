---
name: seisoai
description: 基于 Base 平台，提供按请求计费的 AI 推理服务（支持图像、视频、音乐、3D 数据和音频处理），支持使用 x402 USDC 进行支付。当用户请求生成图像、视频、音乐、3D 模型，或提及 SeisoAI、FLUX、Veo 或 AI 生成相关功能时，可使用该服务。该服务需要用户具备 curl 命令的使用权限、可访问互联网的连接，以及具备 x402 支付功能的签名器，并且每次请求都需要用户的明确授权。
license: Apache-2.0
compatibility: Requires curl and internet access. Host must provide x402-signer capability with per-request user approval.
version: 1.4.0
last_synced: 2026-02-13
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":"🎨"},"author":"seisoai","autonomous":"requires-approval","x402":{"network":"eip155:8453","asset":"USDC","payTo":"0xa0aE05e2766A069923B2a51011F270aCadFf023a","userApproval":"per-request","autoSign":"forbidden","paytoVerification":"required"}}
---

# SeisoAI x402 技能

**基础 URL**: `https://seisoai.com`  
**支付方式**: 使用 USDC 在 Base 网络上进行支付（EIP155:8453）  
**收款人**: `0xa0aE05e2766A069923B2a51011F270aCadFf023a`  

---

## 安全性配置  

| 类别 | 状态 | 详情 |
|----------|--------|---------|
| **用途与功能** | ✅ 符合要求 | 通过 x402 和 USDC 进行按请求计费的 AI 生成服务。需要：`curl` 工具、互联网连接，以及支持按请求审批的 x402 签名器。 |
| **指令范围** | ✅ 有限 | 仅与 `seisoai.com` 门户交互，不读取本地文件、环境变量或系统数据。每次支付均需用户明确同意。 |
| **安装机制** | ✅ 极简单 | 仅提供指令，无需安装任何插件或代码，也不会在磁盘上存储数据。 |
| **凭证** | ✅ 无需任何凭证 | 不需要 API 密钥、环境变量或存储的秘密信息，所有认证均通过 x402 签名完成。 |
| **持久性及权限** | ✅ 限制严格 | `always: false`（无持久化数据）；`autonomous: requires-approval`（即使在自动化工作流程中，支付也需要用户同意）。 |

---

## 安装前检查清单  

在安装或使用此技能之前，请完成以下验证步骤：  

### 1. 验证签名器的合规性  
确认您的签名器在每次支付前都会请求用户批准：  
- [ ] 签名器在支付前会提示用户（不允许自动签名）  
- [ ] 签名器会显示可读的 USDC 金额（例如：“0.0325 USDC”）  
- [ ] 签名器会显示收款人地址和网络（Base）  
- [ ] 签名器未启用“全部批准”或“信任此技能”模式  
- [ ] 签名器需要用户明确操作（点击按钮或确认）才能继续支付  

### 2. 验证域名和 TLS 安全性  
在批准任何支付之前，请确认：  
- [ ] `https://seisoai.com` 服务器能提供有效的 TLS 证书  
- [ ] 确认域名指向正确的服务（非钓鱼网站）  
- [ ] 所有 API 调用均使用 HTTPS（禁止使用 HTTP）  

### 3. 验证收款人地址  
唯一的授权收款人为：  
```
0xa0aE05e2766A069923B2a51011F270aCadFf023a
```  
- [ ] 确认该地址与 402 响应中的 `payTo` 字段匹配  
- [ ] 如果地址不同，请立即中止操作  
- [ ] （可选）在 Base 块浏览器（basescan.org）中验证该地址  

### 4. 先进行小额支付测试  
- [ ] 使用低成本工具（例如 `image.generate.flux-2`，费用约 0.03 美元）进行测试  
- [ ] 确认支付流程正常工作后再进行大额支付  
- [ ] 确认支付后能收到生成的内容  

### 5. 禁用自动批准设置  
- [ ] 确保您的钱包/签名器未启用针对此技能的“自动批准”或“白名单”功能  
- [ ] 禁用任何基于会话的“记住我的选择”设置  
- [ ] 每次支付都必须获得用户的明确批准  

---

## ⚠️ 必须获得用户同意  
在签署任何支付请求之前，必须：  
1. 向用户显示工具名称、金额（USDC）、网络（Base）和收款人地址  
2. 等待用户的明确批准  
3. 仅在用户确认后继续操作  

**严禁自动批准支付请求。严禁跳过确认步骤。**  

### 自动化调用政策  
由于每次调用都涉及财务交易，此技能设置为 `autonomous: requires-approval`。即使主机允许自动化调用，**支付签名仍需用户批准**。自动化政策适用于技能调用本身；支付授权是独立的流程，不能被绕过。  

**自动调用此技能的代理（例如在多步骤工作流中）**也必须在 x402 签名步骤之前暂停，等待用户批准。  

---

## 依赖项与凭证  

### 必需的二进制文件  
- **curl**：用于所有向 SeisoAI 门户的 HTTP 请求  

### 主机必须提供的功能  
- **x402-signer**：支持支付签名（详见主机签名器要求）  
- **互联网连接**：能够访问 `seisoai.com` 的 HTTPS 网络  

### 环境变量  
**无需任何环境变量**。此技能不使用 API 密钥、令牌或存储的凭证，所有认证均通过 x402 支付签名完成。  

### 凭证模型  
这是一个**按请求付费**的服务：  
- 每次请求都会触发一个 402 请求，要求支付  
- 主机的 x402 签名器会生成一次性的支付签名  
- 支付在链上（Base 网络）完成  
- 不会存储或传输任何秘密信息或凭证  

---

## 主机签名器要求  
此技能要求主机环境提供 x402 支付签名器。**集成此技能的调用者必须确保其签名器符合以下要求：**  

> **警告**：如果签名器在未经用户批准的情况下自动完成支付，将使此技能的合规性失效，并带来巨大的财务风险。此类实现是不合规的。  

### 关键要求：禁止自动签名  
1. **必须请求用户批准**：签名器在签名前必须提示用户。**严禁**自动签名、批量批准或默许支付。  
2. **金额显示**：签名器必须向用户显示准确的 USDC 金额（以人类可读的形式）和收款人地址。  
3. **明确批准**：签名器必须要求用户明确操作（如点击“批准”或输入“是”）才能生成签名。  
4. **每次支付都需要新授权**：每次支付都必须获得用户的明确批准。禁止使用“记住我的选择”或基于会话的自动批准机制。  

### 合规与不合规的主机签名器实现对比  
| 行为 | 合规 | 不合规 |
|----------|-----------|---------------|
| 在每次签名前提示用户金额/收款人地址 | ✅ | |
| 要求每次请求都获得明确批准 | ✅ | |
| 验证收款人地址是否与预期地址匹配 | ✅ | |
| 未经用户操作自动签名 | | ❌ |
| 启用“信任此技能”或“全部批准”设置 | | ❌ |
| 批量批准多个支付请求 | | ❌ |
| 在不显示金额的情况下签名 | | ❌ |
| 跳过收款人地址的验证 | | ❌ |  

### 收款人地址验证  
**授权的收款人地址**：`0xa0aE05e2766A069923B2a51011F270aCadFf023a`  
这是 SeisoAI 的**唯一授权收款人**。主机签名器必须：  
- 确认 402 响应中的 `accepts[0].payTo` 与此地址完全匹配  
- 如果地址不符，必须显示警告或阻止签名  
- 允许用户在发现地址错误时取消操作  

**重要性说明**：如果门户被攻击或代理被诱导调用恶意端点，错误的 `payTo` 地址可能导致资金被转移。验证收款人地址可保护用户免受资金损失。  

### 主机实施者检查清单  
在部署用于此技能的签名器之前，请验证：  
- [ ] 签名器在签名前会提示用户支付金额（例如：“0.0325 USDC”，而非“32500”）  
- [ ] 签名器在签名前会显示收款人地址  
- [ ] 签名器会显示网络（Base / EIP155:8453）  
- [ ] 签名器需要用户明确操作（点击按钮或输入“是”）才能继续  
- [ ] 签名器未启用“自动批准”或“一次信任”模式  
- [ ] 签名器会验证 `payTo` 地址是否与预期地址匹配（`0xa0aE05e2766A069923B2a51011F270aCadFf023a`）  
- [ ] 签名器允许用户在任何时候取消操作  
- [ ] 每次调用都需要新的批准（不允许会话缓存）  

### 无凭证存储  
此技能不使用 API 密钥、环境变量或存储的凭证。所有认证均通过 x402 支付签名完成。签名器的钱包访问权限由主机管理；此技能不会访问私钥。  

## 支持的网关路由（仅限 x402）  
x402 支付**仅支持**在以下网关端点上：  
| 路由 | 方法 | 描述 |
|-------|--------|-------------|
| `/api/gateway/invoke/:toolId` | POST | 调用单个工具 |
| `/api/gateway/invoke` | POST | 在请求体中包含工具 ID 进行调用 |
| `/api/gateway/batch` | POST | 批量调用 |
| `/api/gateway/orchestrate` | POST | 多工具协调 |
| `/api/gateway/orchestrate/plan` | POST | 生成执行计划 |
| `/api/gateway/orchestrate/execute` | POST | 执行计划 |
| `/api/gateway/workflows/:workflowId` | POST | 执行工作流 |
| `/api/gateway/agent/:agentId/invoke` | POST | 代理范围内的调用 |
| `/api/gateway/agent/:agentId/orchestrate` | POST | 代理协调 |
| `/api/gateway/jobs/:jobId` | GET | 获取任务状态 |
| `/api/gateway/jobs/:jobId/result` | GET | 获取任务结果 |

## 支付签名规则（OpenClaw）  
1. **仅使用主机签名器**：必须使用 OpenClaw 主机提供的运行时管理的签名器。  
2. **禁止使用原始密钥**：严禁请求、存储或生成原始私钥/密钥短语。  
3. **仅针对当前挑战进行签名**：只能签署与当前 402 挑战相关的支付请求。  
4. **失败时返回错误**：如果无法使用授权的签名器，则返回“payment signer unavailable”。  
5. **禁止自动批准**：每次新挑战都必须重新签名。  

## 不可违反的规则  
1. 402 挑战和支付重试之间的请求内容必须保持一致。  
2. 重试过程中不得更改方法或路径。  
3. 不得重复使用旧的或已使用的支付签名。  
4. 成功提交请求视为可计费的操作。  
5. 确保支付目标地址正确（与挑战中的 `payTo` 一致）。  

## 代理执行流程  
### 第 1 步：列出可用工具  
```bash
curl -s "https://seisoai.com/api/gateway/tools"
```  

### 第 2 步：获取价格  
```bash
curl -s "https://seisoai.com/api/gateway/price/{toolId}"
```  

### 第 3 步：初次调用（触发 x402 请求）  
```bash
curl -s -X POST "https://seisoai.com/api/gateway/invoke/{toolId}" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "..."}'
```  

### 第 4 步：⚠️ 必须向用户显示支付信息并获得批准  
从 402 响应中解析 `accepts[0]`，并向用户显示以下信息：  
- 工具名称  
- 金额（以 USDC 微单位表示，除以 1000000）  
- 收款人地址（Base 网络）  
**等待用户明确批准后再继续。**  

### 第 5 步：进行 x402 支付  
使用主机的 x402 签名器，参数包括：`amount`、`payTo` 和 `network`（来自 402 响应）。  

### 第 6 步：完成支付后调用  
```bash
curl -s -X POST "https://seisoai.com/api/gateway/invoke/{toolId}" \
  -H "Content-Type: application/json" \
  -H "payment-signature: {signed_x402_payload}" \
  -d '{"prompt": "..."}'
```  

### 第 7 步：检查是否处于队列中  
如果 `executionMode` 为“queue”，则持续检查状态，直到任务完成：  
```bash
curl -s "https://seisoai.com/api/gateway/jobs/{jobId}?model={model}"
```  
然后获取结果：  
```bash
curl -s "https://seisoai.com/api/gateway/jobs/{jobId}/result?model={model}"
```  

### 第 8 步：将结果 URL 返回给用户  

## API 端点  
### 发现服务  
```
GET  /api/gateway                         → Gateway info, protocols, tool count
GET  /api/gateway/tools                   → All tools (63 available)
GET  /api/gateway/tools?category={cat}    → Filter by category
GET  /api/gateway/tools/{toolId}          → Tool details, input schema
GET  /api/gateway/price/{toolId}          → Pricing (USD, USDC units)
```  

### 调用服务（需要 x402 支付）  
```
POST /api/gateway/invoke/{toolId}         → Invoke single tool
POST /api/gateway/invoke                  → Invoke with toolId in body
POST /api/gateway/batch                   → Multiple tools in one request
```  

### 任务状态查询  
```
GET  /api/gateway/jobs/{jobId}?model={m}        → Check status
GET  /api/gateway/jobs/{jobId}/result?model={m} → Get completed result
```  

## 工具分类  
| 类别 | 可用工具 |  
|----------|-------|