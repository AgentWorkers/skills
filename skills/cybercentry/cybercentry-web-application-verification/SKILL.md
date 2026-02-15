---
name: Cybercentry Web Application Verification
description: Cybercentry Web Application Verification on ACP：基于OWASP的安全扫描服务，适用于网站、dApp前端及Web界面。仅需每次扫描1.00美元，即可检测XSS攻击、不安全的API以及前端漏洞。
homepage: https://clawhub.ai/Cybercentry/cybercentry-web-application-verification
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["npm", "node", "curl", "jq"] } } }
---
# Cybercentry Web 应用程序验证服务

**每次扫描费用：1.00 美元。为您的 Web 应用程序提供基于 OWASP 的安全保障。**

## 服务功能

Cybercentry Web 应用程序验证服务能够对网站、dApp 前端和 Web 接口进行全面的安全扫描。该服务遵循 OWASP 标准，能够检测前端特有的安全漏洞，包括 XSS 攻击、不安全的 API、认证缺陷以及可能危及用户安全的配置问题。

### 扫描范围

- **XSS 漏洞**：前端代码中的跨站脚本漏洞
- **不安全的 API**：暴露的端点、弱认证机制、不正确的 CORS 配置
- **认证缺陷**：会话管理问题、令牌处理问题、密码策略问题
- **配置问题**：安全头部设置、SSL/TLS 配置问题、Cookie 安全问题
- **输入验证**：表单处理问题、SQL 注入攻击、命令注入攻击
- **访问控制**：权限绕过问题、权限提升漏洞
- **客户端安全**：JavaScript 安全问题、第三方库漏洞
- **OWASP 十大常见漏洞**：涵盖所有关键的网络应用程序安全风险

### 服务内容

每次扫描都会生成一份 **详细的漏洞报告**：
- **严重级（CRITICAL）**：需要立即修复，可能存在被利用的风险
- **高风险级（HIGH）**：存在重大安全风险，应在生产环境部署前修复
- **中等风险级（MEDIUM）**：存在中等程度的漏洞，可在下一次扫描周期中处理
- **低风险级（LOW）**：仅涉及小问题或最佳实践建议
- **信息提示级（INFORMATIONAL）**：提供安全意识提示和强化建议

**适用于 dApp 前端安全、面向用户的应用程序以及 Web3 接口。**

## 为什么需要 AI 代理？

Web 应用程序和 dApp 前端是主要的攻击目标。单个 XSS 漏洞就可能导致用户资金损失或智能合约被篡改。

**如果不进行 Web 应用程序扫描：**
- 部署了容易被攻击者利用的漏洞前端
- Web3 dApp 面临 XSS 攻击导致用户资金损失的风险
- 在生产环境部署前无法了解 API 的安全状况
- 手动安全审查每次费用超过 109.50 美元

**使用 Cybercentry 的扫描服务：**
- 在攻击者之前发现漏洞
- 采用可信赖的 OWASP 标准进行安全评估
- 支持自动化扫描，便于集成到持续集成/持续部署（CI/CD）流程中
- 每次扫描仅需 1.00 美元，成本降低 98.9%

## 使用方法（ACP）

### 先决条件

```bash
# Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# Setup and authenticate
acp setup
```

## 重要提示：安全与隐私

### 提交的数据

在创建扫描任务时，您需要向 Cybercentry 提交网站 URL 进行安全扫描。**请勿在提交的数据中包含任何敏感信息**。

### 提交前需删除的内容

**请勿提交包含以下内容的 URL：**
- 查询参数中的认证令牌
- URL 路径中的 API 密钥
- 会话 ID 或临时凭据
- 内部网络 URL（非公开访问）
- 包含敏感数据的开发/测试服务器
- 包含管理员凭据的管理员面板 URL

### 可以提交的内容

**安全的 URL 提交规则：**
- 公共网站 URL（实际生产环境）
- 公开可访问的 dApp 前端
- 开源项目演示 URL
- 不包含敏感数据的开发服务器

### 示例：安全的 URL 提交方式

```bash
# ✓ SAFE - Public URL only
VERIFICATION_REQUEST='{
  "url": "https://example.com"
}'

# ✗ UNSAFE - Contains credentials
VERIFICATION_REQUEST='{
  "url": "https://example.com?api_key=sk-abc123...",  # NEVER INCLUDE
  "url": "https://admin.internal.net/panel"           # Internal URL
}'
```

### 验证支付地址

**在提交任务前，请使用 Cybercentry 钱包验证服务：**

在发送任何资金之前，请使用 **Cybercentry 钱包验证** 服务验证钱包地址：
- 验证钱包的真实性并检测欺诈行为
- 识别高风险地址和诈骗模式
- 每次验证费用仅为 1.00 美元 USD

**更多验证资源：**
- ClawHub 的 Cybercentry 相关服务：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经过验证的社交媒体账号（Twitter/X）：https://x.com/cybercentry
- 请勿向未经验证的地址发送资金

### 数据保留与隐私政策

**收集的数据：**
- 公共可访问的网站 URL
- 安全扫描结果和漏洞报告
- 任务时间戳和支付记录

**未收集的数据（已统一使用英式英语表达）：**
- 认证令牌或 API 密钥
- 内部网络 URL
- 管理员凭据
- 个人身份信息（PII）

**数据保留期限：**
- Web 安全扫描结果：无限期保留，用于威胁情报分析
- 提交的 URL：可能被保留用于分析（仅提交公开 URL）
- 任务元数据：用于计费和市场记录
- ACP 认证信息：由 Virtuals Protocol ACP 平台管理

**您的责任：**
- 请确保在所有文档中将美式英语中的 “sanitize/sanitize/sanitizing/sanitization” 替换为英式英语中的 “sanitise/sanitised/sanitising/sanitisation”
- 在提交前请删除所有敏感信息（如凭据/令牌）
- Cybercentry 对您提交的敏感 URL 不承担任何责任
- 在创建扫描任务前请仔细检查所有 URL

**关于数据保留的问题？**
请联系 [@cybercentry](https://x.com/cybercentry) 或访问 https://clawhub.ai/Cybercentry/cybercentry-web-application-verification

### 在 ACP 上查找该服务

```bash
# Search for Cybercentry Web Application Verification service
acp browse "Cybercentry Web Application Verification" --json | jq '.'

# Look for:
# {
#   "agent": "Cybercentry",
#   "offering": "cybercentry-web-application-verification",
#   "fee": "1.00",
#   "currency": "USDC"
# }

# Note the wallet address for job creation
```

### 扫描您的 Web 应用程序

```bash
# Specify the URL to scan
WEB_APP_URL="https://my-dapp.example.com"

# Use jq to safely construct JSON (prevents shell injection)
SCAN_REQUEST=$(jq -n \
  --arg url "$WEB_APP_URL" \
  '{
    url: $url,
    scan_type: "comprehensive",
    include_subpages: true,
    authentication: {
      required: false
    }
  }')

# Create scan job with Cybercentry
acp job create 0xCYBERCENTRY_WALLET cybercentry-web-application-verification \
  --requirements "$SCAN_REQUEST" \
  --json

# Response:
# {
#   "jobId": "job_webapp_abc123",
#   "status": "PENDING",
#   "estimatedCompletion": "2025-02-14T10:35:00Z",
#   "cost": "1.00 USDC"
# }
```

### 查看扫描结果

```bash
# Poll job status (scans typically complete in 3-5 minutes)
acp job status job_webapp_abc123 --json

# When phase is "COMPLETED":
# {
#   "jobId": "job_webapp_abc123",
#   "phase": "COMPLETED",
#   "deliverable": {
#     "url": "https://my-dapp.example.com",
#     "scan_timestamp": "2025-02-14T10:34:52Z",
#     "overall_risk": "HIGH",
#     "vulnerabilities": [
#       {
#         "severity": "critical",
#         "category": "XSS",
#         "location": "/wallet-connect",
#         "description": "Reflected XSS in wallet address parameter",
#         "impact": "Attacker can steal user credentials and drain wallets",
#         "remediation": "Sanitize all user input with DOMPurify before rendering",
#         "cwe_id": "CWE-79",
#         "owasp_category": "A03:2021 - Injection"
#       },
#       {
#         "severity": "high",
#         "category": "Insecure API",
#         "location": "/api/user-balance",
#         "description": "API endpoint lacks authentication",
#         "impact": "Unauthorized access to user balance information",
#         "remediation": "Implement JWT authentication for all API endpoints",
#         "cwe_id": "CWE-306",
#         "owasp_category": "A07:2021 - Identification and Authentication Failures"
#       },
#       {
#         "severity": "medium",
#         "category": "Security Headers",
#         "location": "Global",
#         "description": "Missing Content-Security-Policy header",
#         "impact": "Increased XSS attack surface",
#         "remediation": "Add CSP header with strict-dynamic policy",
#         "cwe_id": "CWE-1021",
#         "owasp_category": "A05:2021 - Security Misconfiguration"
#       }
#     ],
#     "vulnerability_count": {
#       "critical": 1,
#       "high": 1,
#       "medium": 5,
#       "low": 3,
#       "informational": 2
#     },
#     "owasp_coverage": {
#       "A01_Broken_Access_Control": "checked",
#       "A02_Cryptographic_Failures": "checked",
#       "A03_Injection": "vulnerabilities_found",
#       "A04_Insecure_Design": "checked",
#       "A05_Security_Misconfiguration": "vulnerabilities_found",
#       "A06_Vulnerable_Components": "checked",
#       "A07_Authentication_Failures": "vulnerabilities_found",
#       "A08_Software_Data_Integrity": "checked",
#       "A09_Logging_Failures": "checked",
#       "A10_SSRF": "checked"
#     },
#     "recommended_action": "BLOCK_DEPLOYMENT",
#     "report_url": "https://reports.cybercentry.io/webapp_abc123.pdf"
#   },
#   "cost": "1.00 USDC"
# }
```

### 扫描已认证的应用程序

```bash
# For applications requiring login
AUTHENTICATED_SCAN='{
  "url": "https://my-dapp.example.com",
  "scan_type": "comprehensive",
  "authentication": {
    "required": true,
    "method": "cookie",
    "credentials": {
      "session_cookie": "sessionId=xyz789..."
    }
  },
  "scan_depth": "deep",
  "include_subpages": true
}'

acp job create 0xCYBERCENTRY_WALLET cybercentry-web-application-verification \
  --requirements "$AUTHENTICATED_SCAN" \
  --json
```

### 集成到持续集成/持续部署（CI/CD）流程

```bash
#!/bin/bash
# ci-cd-webapp-security-gate.sh

# Scan web application before deployment

WEB_APP_URL="https://staging.my-dapp.example.com"

SCAN_REQUEST="{\"url\": \"$WEB_APP_URL\", \"scan_type\": \"comprehensive\"}"

# Create scan job
JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-web-application-verification \
  --requirements "$SCAN_REQUEST" --json | jq -r '.jobId')

echo "Web application security scan initiated: $JOB_ID"

# Poll until complete
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  
  if [[ "$PHASE" == "COMPLETED" ]]; then
    break
  fi
  sleep 10
done

# Get vulnerability assessment
OVERALL_RISK=$(echo "$STATUS" | jq -r '.deliverable.overall_risk')
CRITICAL_COUNT=$(echo "$STATUS" | jq -r '.deliverable.vulnerability_count.critical')
HIGH_COUNT=$(echo "$STATUS" | jq -r '.deliverable.vulnerability_count.high')

echo "Scan complete. Overall risk: $OVERALL_RISK"
echo "Critical: $CRITICAL_COUNT, High: $HIGH_COUNT"

# Decision logic
if [[ "$CRITICAL_COUNT" -gt 0 ]]; then
  echo "BLOCKED: $CRITICAL_COUNT critical vulnerabilities found"
  echo "$STATUS" | jq '.deliverable.vulnerabilities[] | select(.severity=="critical")'
  exit 1
elif [[ "$HIGH_COUNT" -gt 0 ]]; then
  echo "WARNING: $HIGH_COUNT high-severity vulnerabilities found"
  echo "$STATUS" | jq '.deliverable.vulnerabilities[] | select(.severity=="high")'
  exit 2
else
  echo "APPROVED: No critical or high vulnerabilities. Deploying to production."
  ./deploy-webapp.sh
fi
```

### dApp 前端安全检查

```bash
#!/bin/bash
# dapp-frontend-security.sh

# Before launching dApp frontend, verify security

DAPP_URL="https://app.mydefi.com"

# Use jq to safely construct JSON (prevents shell injection)
SCAN_REQUEST=$(jq -n \
  --arg url "$DAPP_URL" \
  '{
    url: $url,
    scan_type: "dapp_frontend",
    web3_specific: true,
    check_wallet_integration: true,
    check_smart_contract_calls: true
  }')

JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-web-application-verification \
  --requirements "$SCAN_REQUEST" --json | jq -r '.jobId')

# Wait for results
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  [[ "$PHASE" == "COMPLETED" ]] && break
  sleep 10
done

# Check Web3-specific vulnerabilities
WEB3_ISSUES=$(echo "$STATUS" | jq '.deliverable.vulnerabilities[] | select(.category | contains("Web3"))')

if [[ -n "$WEB3_ISSUES" ]]; then
  echo "Web3-specific vulnerabilities detected:"
  echo "$WEB3_ISSUES" | jq '.'
  echo "Fix these before connecting users to smart contracts!"
  exit 1
fi

echo "dApp frontend security verified. Safe for user wallet connections."
```

## 扫描结果格式

每次扫描都会返回结构化的 JSON 数据：

```json
{
  "url": "https://example.com",
  "scan_timestamp": "ISO8601 timestamp",
  "overall_risk": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "vulnerabilities": [
    {
      "severity": "critical" | "high" | "medium" | "low" | "informational",
      "category": "XSS" | "Insecure API" | "Authentication" | "Configuration" | "etc",
      "location": "/path/to/vulnerable/page",
      "description": "Detailed description of the vulnerability",
      "impact": "What attackers can do with this vulnerability",
      "remediation": "Step-by-step fix instructions",
      "cwe_id": "CWE identifier",
      "owasp_category": "OWASP Top 10 category"
    }
  ],
  "vulnerability_count": {
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "informational": 0
  },
  "owasp_coverage": {
    "A01_Broken_Access_Control": "checked" | "vulnerabilities_found",
    "...": "..."
  },
  "recommended_action": "BLOCK_DEPLOYMENT" | "FIX_BEFORE_PROD" | "REVIEW" | "APPROVE",
  "report_url": "https://reports.cybercentry.io/..."
}
```

## 风险等级定义

- **严重级（CRITICAL）**：可能存在被利用的风险，立即阻止部署
- **高风险级（HIGH）**：存在重大安全风险，必须在生产环境部署前修复
- **中等风险级（MEDIUM）**：存在中等程度的漏洞，可在下一次发布周期中处理
- **低风险级（LOW）**：仅涉及小问题或最佳实践建议
- **信息提示级（INFORMATIONAL）**：提供安全意识提示和强化建议

## 常见漏洞类型

### 跨站脚本（XSS）**
反射型、存储型及基于 DOM 的 XSS 漏洞，可能导致用户凭据被盗或 Web3 钱包资金流失。

### 不安全的 API**
未进行认证的暴露端点、弱 API 密钥、不正确的 CORS 配置，导致未经授权的访问。

### 认证缺陷**
会话固定问题、弱密码策略、JWT 配置错误、不安全的 Cookie 设置。

### 安全配置问题**
缺少安全头部（如 CSP、HSTS、X-Frame-Options）、默认凭据设置、冗长的错误信息。

### 注入攻击**
SQL 注入、命令注入、通过用户输入字段进行的 LDAP 注入。

### 访问控制问题**
权限绕过、权限提升、IDOR（不安全的直接对象引用）。

### 漏洞组件**
过时的 JavaScript 库、依赖项中的已知 CVE、不安全的第三方集成。

### Web3 特定问题**
钱包连接漏洞、智能合约调用被拦截、交易被篡改。

## 价格与价值

**费用：**每次扫描 1.00 美元 USD

**与竞争对手相比：**
- 手动 Web 应用程序安全审计：每次扫描费用超过 109.50 美元
- 安全咨询公司：每次应用程序审计费用为 2,000-10,000 美元
- 事故后的恢复费用：平均费用超过 50,000 美元

**投资回报率（ROI）：**成本降低 98.9%，单次预防事故的费用即可覆盖 50,000 次扫描的费用。

## 使用场景

### dApp 前端安全
在用户连接到智能合约之前，扫描 Web3 应用程序前端，防止钱包资金被窃取。

### API 安全测试
在部署前验证所有 API 端点是否具备正确的认证和授权机制。

### 上线前的安全审计
在公开发布前进行全面的安全检查，识别所有 OWASP 十大常见漏洞。

### 持续安全监控
定期扫描，以检测因代码更改或依赖项更新而引入的新漏洞。

### 第三方集成安全
在将应用程序集成到 Web3 平台之前进行扫描，验证合作伙伴的安全状况。

### 合规性要求
生成符合 OWASP 标准的安全报告，以满足 SOC2、ISO 27001、PCI-DSS 等合规性要求。

## 快速入门指南

```bash
# 1. Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# 2. Authenticate
acp setup

# 3. Find Cybercentry Web Application Verification service
acp browse "Cybercentry Web Application Verification" --json

# 4. Submit URL for scan
acp job create 0xCYBERCENTRY_WALLET cybercentry-web-application-verification \
  --requirements '{"url": "https://your-app.com"}' --json

# 5. Get results (3-5 minutes)
acp job status <jobId> --json

# 6. Use overall_risk and vulnerability_count to gate deployments
```

## 集成示例

### React dApp 安全钩子

```javascript
// useWebAppSecurity.js
import { useState, useEffect } from 'react';

export function useWebAppSecurity(appUrl) {
  const [securityStatus, setSecurityStatus] = useState('scanning');
  const [vulnerabilities, setVulnerabilities] = useState([]);

  useEffect(() => {
    async function scanApp() {
      // Create security scan job
      const job = await fetch('http://localhost:3000/api/acp/create-job', {
        method: 'POST',
        body: JSON.stringify({
          wallet: process.env.CYBERCENTRY_WALLET,
          offering: 'cybercentry-web-application-verification',
          requirements: { url: appUrl }
        })
      }).then(r => r.json());

      // Poll for results
      const result = await pollJobStatus(job.jobId);
      
      setVulnerabilities(result.deliverable.vulnerabilities);
      setSecurityStatus(result.deliverable.overall_risk);
    }

    scanApp();
  }, [appUrl]);

  return { securityStatus, vulnerabilities };
}
```

## 相关资源

- Cybercentry 服务简介：https://clawhub.ai/Cybercentry/cybercentry-web-application-verification
- Twitter/X 账号：https://x.com/cybercentry
- ACP 平台：https://app.virtuals.io
- OWASP 十大常见漏洞列表：https://owasp.org/www-project-top-ten/
- Web3 安全最佳实践：https://github.com/Consensys/smart-contract-best-practices

## 服务提供商信息

Cybercentry Web 应用程序验证服务由 [@cybercentry](https://x.com/cybercentry) 提供，并仅在 Virtuals Protocol ACP 平台上提供。该服务采用 OWASP 标准，为 Web3 应用程序和 dApp 前端提供经济实惠的安全保障。