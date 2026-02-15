---
name: senior-secops
description: 全面的SecOps技能，涵盖应用程序安全、漏洞管理、合规性以及安全开发实践。包括安全扫描、漏洞评估、合规性检查以及安全自动化功能。适用于实施安全控制、进行安全审计、响应漏洞事件或确保合规性要求时使用。
---

# 高级安全运维工程师

这是一套全面的安全运维工具包，涵盖了漏洞管理、合规性验证、安全编码实践以及安全自动化等方面。

---

## 目录

- [术语解释](#trigger-terms)
- [核心能力](#core-capabilities)
- [工作流程](#workflows)
- [工具参考](#tool-reference)
- [安全标准](#security-standards)
- [合规性框架](#compliance-frameworks)
- [最佳实践](#best-practices)

---

## 术语解释

在遇到以下情况时，请使用此技能：

| 类别 | 术语 |
|----------|-------|
| **漏洞管理** | CVE（Common Vulnerability Enumeration）、CVSS（Common Vulnerability Scoring System）、漏洞扫描、安全补丁、依赖项审计、npm审计、pip审计 |
| **OWASP Top 10** | 注入攻击（Injection）、XSS（Cross-Site Scripting）、CSRF（Cross-Site Request Forgery）、身份验证漏洞、安全配置错误、敏感数据泄露 |
| **合规性** | SOC 2（Security Operations Center 2）、PCI-DSS（Payment Card Industry Data Security Standard）、HIPAA（Health Insurance Portability and Accountability Act）、GDPR（General Data Protection Regulation）、合规性审计、安全控制、访问控制 |
| **安全编码** | 输入验证、输出编码、参数化查询、预处理语句、数据清洗 |
| **秘密管理** | API密钥、秘密存储库（Secrets Vault）、环境变量、HashiCorp Vault、AWS Secrets Manager |
| **身份验证** | JWT（JSON Web Tokens）、OAuth、多因素认证（MFA）、双因素认证（2FA）、时间基于密码的认证（TOTP）、密码哈希算法（bcrypt, argon2）、会话管理 |
| **安全测试** | 静态应用安全测试（SAST）、动态应用安全测试（DAST）、渗透测试、安全扫描工具（Snyk, Semgrep, CodeQL, Trivy） |
| **事件响应** | 安全事件、违规通知、事件处理、取证、事件遏制 |
| **网络安全** | TLS（传输层安全协议）、HTTPS（Hypertext Transfer Protocol Secure）、HSTS（HTTP Strict Transport Security）、CSP（Content Security Policy）、CORS（Cross-Origin Resource Sharing）、安全头部、防火墙规则、WAF（Web Application Firewall） |
| **基础设施安全** | 容器安全、Kubernetes安全、身份与访问管理（IAM）、最小权限原则、零信任安全模型 |
| **加密技术** | 静态数据加密、传输数据加密、AES-256（Advanced Encryption Standard 256）、RSA（Rivest-Shamir-Adleman）、密钥管理（Key Management Service） |
| **监控** | 安全监控、安全信息事件管理（SIEM）、审计日志记录、入侵检测、异常检测 |

---

## 核心能力

### 1. 安全扫描器

扫描源代码中的安全漏洞，包括硬编码的秘密信息、SQL注入、XSS攻击、命令注入和路径遍历漏洞。

```bash
# Scan project for security issues
python scripts/security_scanner.py /path/to/project

# Filter by severity
python scripts/security_scanner.py /path/to/project --severity high

# JSON output for CI/CD
python scripts/security_scanner.py /path/to/project --json --output report.json
```

**检测内容：**
- 硬编码的秘密信息（API密钥、密码、AWS凭证、GitHub令牌、私钥）
- SQL注入模式（字符串拼接、模板字符串的使用）
- XSS漏洞（`innerHTML`的赋值操作、不安全的DOM操作、React框架中的不安全代码）
- 命令注入（使用用户输入执行shell命令、`eval`函数）
- 路径遍历（基于用户输入的文件操作）

### 2. 漏洞评估工具

扫描npm、Python和Go生态系统中的已知CVE漏洞。

```bash
# Assess project dependencies
python scripts/vulnerability_assessor.py /path/to/project

# Critical/high only
python scripts/vulnerability_assessor.py /path/to/project --severity high

# Export vulnerability report
python scripts/vulnerability_assessor.py /path/to/project --json --output vulns.json
```

**扫描对象：**
- `package.json` 和 `package-lock.json`（npm依赖项）
- `requirements.txt` 和 `pyproject.toml`（Python项目配置文件）
- `go.mod`（Go项目配置文件）

**输出结果：**
- 漏洞ID及其CVSS评分
- 受影响的包版本
- 已修复的版本
- 整体风险评分（0-100分）

### 3. 合规性检查工具

验证代码是否符合SOC 2、PCI-DSS、HIPAA和GDPR等安全标准。

```bash
# Check all frameworks
python scripts/compliance_checker.py /path/to/project

# Specific framework
python scripts/compliance_checker.py /path/to/project --framework soc2
python scripts/compliance_checker.py /path/to/project --framework pci-dss
python scripts/compliance_checker.py /path/to/project --framework hipaa
python scripts/compliance_checker.py /path/to/project --framework gdpr

# Export compliance report
python scripts/compliance_checker.py /path/to/project --json --output compliance.json
```

**检查内容：**
- 访问控制机制的实现
- 静态数据和传输数据的安全加密
- 审计日志记录
- 身份验证机制的强度（多因素认证、密码哈希）
- 安全相关文档的完整性

---

## 工作流程

### 工作流程1：安全审计

对代码库进行全面的安全评估。

```bash
# Step 1: Scan for code vulnerabilities
python scripts/security_scanner.py . --severity medium

# Step 2: Check dependency vulnerabilities
python scripts/vulnerability_assessor.py . --severity high

# Step 3: Verify compliance controls
python scripts/compliance_checker.py . --framework all

# Step 4: Generate combined report
python scripts/security_scanner.py . --json --output security.json
python scripts/vulnerability_assessor.py . --json --output vulns.json
python scripts/compliance_checker.py . --json --output compliance.json
```

### 工作流程2：CI/CD安全门控

将安全检查集成到持续集成/持续部署（CI/CD）流程中。

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Security Scanner
        run: python scripts/security_scanner.py . --severity high

      - name: Vulnerability Assessment
        run: python scripts/vulnerability_assessor.py . --severity critical

      - name: Compliance Check
        run: python scripts/compliance_checker.py . --framework soc2
```

### 工作流程3：CVE漏洞处理

响应影响应用程序的新漏洞。

```
1. ASSESS (0-2 hours)
   - Identify affected systems using vulnerability_assessor.py
   - Check if CVE is being actively exploited
   - Determine CVSS environmental score for your context

2. PRIORITIZE
   - Critical (CVSS 9.0+, internet-facing): 24 hours
   - High (CVSS 7.0-8.9): 7 days
   - Medium (CVSS 4.0-6.9): 30 days
   - Low (CVSS < 4.0): 90 days

3. REMEDIATE
   - Update affected dependency to fixed version
   - Run security_scanner.py to verify fix
   - Test for regressions
   - Deploy with enhanced monitoring

4. VERIFY
   - Re-run vulnerability_assessor.py
   - Confirm CVE no longer reported
   - Document remediation actions
```

### 工作流程4：事件响应

制定并执行安全事件处理流程。

```
PHASE 1: DETECT & IDENTIFY (0-15 min)
- Alert received and acknowledged
- Initial severity assessment (SEV-1 to SEV-4)
- Incident commander assigned
- Communication channel established

PHASE 2: CONTAIN (15-60 min)
- Affected systems identified
- Network isolation if needed
- Credentials rotated if compromised
- Preserve evidence (logs, memory dumps)

PHASE 3: ERADICATE (1-4 hours)
- Root cause identified
- Malware/backdoors removed
- Vulnerabilities patched (run security_scanner.py)
- Systems hardened

PHASE 4: RECOVER (4-24 hours)
- Systems restored from clean backup
- Services brought back online
- Enhanced monitoring enabled
- User access restored

PHASE 5: POST-INCIDENT (24-72 hours)
- Incident timeline documented
- Root cause analysis complete
- Lessons learned documented
- Preventive measures implemented
- Stakeholder report delivered
```

---

## 工具参考

### security_scanner.py

| 选项 | 描述 |
|--------|-------------|
| `target` | 需要扫描的目录或文件 |
| `--severity, -s` | 严重程度：critical（严重）、high（高）、medium（中等）、low（低） |
| `--verbose, -v` | 扫描过程中显示文件信息 |
| `--json` | 以JSON格式输出结果 |
| `--output, -o` | 将结果写入文件 |

**退出代码：**
- `0`：未发现严重/高严重级别的漏洞 |
- `1`：发现高严重级别的漏洞 |
- `2`：发现严重级别的漏洞 |

### vulnerability_assessor.py

| 选项 | 描述 |
|--------|-------------|
| `target` | 包含依赖项文件的目录 |
| `--severity, -s` | 严重程度：critical（严重）、high（高）、medium（中等）、low（低） |
| `--verbose, -v` | 扫描过程中显示文件信息 |
| `--json` | 以JSON格式输出结果 |
| `--output, -o` | 将结果写入文件 |

**退出代码：**
- `0`：未发现严重/高严重级别的漏洞 |
- `1`：发现高严重级别的漏洞 |
- `2`：发现严重级别的漏洞 |

### compliance_checker.py

| 选项 | 描述 |
|--------|-------------|
| `target` | 需要检查的目录 |
| `--framework, -f` | 检查的合规性框架：soc2、pci-dss、hipaa、gdpr |
| `--verbose, -v` | 扫描过程中显示检查结果 |
| `--json` | 以JSON格式输出结果 |
| `--output, -o` | 将结果写入文件 |

**退出代码：**
- `0`：符合标准（得分90%以上） |
- `1`：不符合标准（得分50%-69%） |
- `2`：存在严重合规性问题（得分低于50%） |

---

## 安全标准

### OWASP Top 10预防措施

| 漏洞类型 | 预防措施 |
|--------------|------------|
| **A01：访问控制漏洞** | 实施基于角色的访问控制（RBAC）、默认拒绝访问权限、服务器端验证权限 |
| **A02：加密失败** | 使用TLS 1.2及以上版本、AES-256加密算法、安全密钥管理 |
| **A03：注入攻击** | 使用参数化查询、输入验证、输出数据的安全处理 |
| **A04：不安全的设计** | 进行威胁建模、采用安全的设计模式、深度防御策略 |
| **A05：安全配置错误** | 遵循安全加固指南、禁用不必要的功能 |
| **A06：易受攻击的组件** | 定期扫描依赖项、自动更新软件、维护软件清单（SBOM） |
| **A07：身份验证漏洞** | 实施多因素认证、限制请求频率、安全存储密码 |
| **A08：数据完整性问题** | 对代码进行签名处理、验证数据完整性、使用安全的CI/CD流程 |
| **A09：安全日志记录问题** | 生成全面的审计日志、集成安全信息事件管理系统（SIEM）、及时报警 |
| **A10：跨站请求伪造（SSRF）** | 验证URL地址、设置允许访问的域名列表、实施网络隔离 |

### 安全编码最佳实践

---

## 合规性框架

### SOC 2 Type II 控制措施

| 控制项 | 类别 | 描述 |
|---------|----------|-------------|
| CC1 | 环境控制 | 安全策略、组织结构 |
| CC2 | 通信安全 | 提高员工的安全意识、编写安全文档 |
| CC3 | 风险评估 | 定期扫描漏洞、进行威胁建模 |
| CC6 | 逻辑访问控制 | 实施身份验证和授权机制、使用多因素认证 |
| CC7 | 系统运营 | 监控系统运行情况、记录日志、及时响应安全事件 |
| CC8 | 变更管理 | 控制代码的更改过程、进行代码审查、实施部署安全措施 |

### PCI-DSS v4.0 要求

| 要求项 | 描述 |
|-------------|-------------|
|Req 3 | 保护存储的持卡人数据（静态数据加密） |
|Req 4 | 加密传输数据（使用TLS 1.2及以上协议） |
|Req 6 | 保证开发过程的安全性（输入验证、安全编码） |
|Req 8 | 强化身份验证机制（多因素认证、密码策略） |
|Req 10 | 完整的审计日志记录（所有对持卡人数据的访问操作） |
|Req 11 | 定期进行安全测试（静态应用安全测试、动态应用安全测试、渗透测试） |

### HIPAA 安全规则

| 安全措施 | 相关要求 |
|-----------|-------------|
| 164.312(a)(1) | 对敏感健康信息（PHI）的访问必须进行唯一用户身份验证 |
| 164.312(b) | 对PHI的访问操作必须保留审计记录 |
| 164.312(c)(1) | 保护数据完整性 |
| 164.312(d) | 使用多因素认证（MFA） |
| 164.312(e)(1) | 数据传输必须使用TLS协议进行加密 |

### GDPR 相关要求

| 条款 | 具体要求 |
|---------|-------------|
| Art 25 | 设计阶段就考虑数据隐私保护、最小化数据收集 |
| Art 32 | 采取安全措施、对数据进行加密处理 |
| Art 33 | 发生数据泄露时必须立即通知相关方 |
| Art 17 | 用户有权要求删除自己的数据 |
| Art 20 | 提供数据迁移的便利性 |

---

## 最佳实践

### 秘密管理最佳实践

---

### SQL注入防护最佳实践

---

### XSS防护最佳实践

---

### 身份验证最佳实践

---

### 安全头部设置最佳实践

---

## 参考文档

| 文档 | 描述 |
|----------|-------------|
| `references/security_standards.md` | OWASP Top 10安全标准、安全编码规范、身份验证机制 |
| `references/vulnerability_management_guide.md` | CVE漏洞处理流程、CVSS评分标准、漏洞修复指南 |
| `references/compliance_requirements.md` | SOC 2、PCI-DSS、HIPAA、GDPR的相关合规性要求 |

---

## 技术栈

**安全扫描工具：**
- Snyk（用于扫描依赖项中的漏洞）
- Semgrep（用于静态应用安全测试）
- CodeQL（用于代码分析）
- Trivy（用于容器安全扫描）
- OWASP ZAP（用于动态应用安全测试）

**秘密管理工具：**
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- 1Password Secrets Automation

**身份验证工具：**
- bcrypt、argon2（用于密码哈希）
- jsonwebtoken（用于生成JWT令牌）
- passport.js（用于实现身份验证中间件）
- speakeasy（用于提供多因素认证服务）

**日志记录与监控工具：**
- Winston、Pino（用于Node.js应用程序的日志记录）
- Datadog、Splunk（用于安全信息事件管理）
- PagerDuty（用于发送警报）

**合规性管理工具：**
- Vanta（用于自动化SOC 2合规性检查）
- Drata（用于合规性管理）
- AWS Config（用于配置合规性检查）