---
name: "senior-secops"
description: 高级安全运维工程师的技能包括：应用程序安全、漏洞管理、合规性验证以及安全开发实践。负责执行静态应用安全测试（SAST）/动态应用安全测试（DAST），生成漏洞修复计划，检查应用程序中的依赖项漏洞，制定安全策略，推广安全编码规范，并自动化执行针对SOC2、PCI-DSS、HIPAA和GDPR等标准的合规性检查。这些技能在以下场景中非常有用：进行安全审查或审计、处理漏洞或安全事件、强化基础设施安全、实施身份验证和密钥管理机制、准备渗透测试、检查OWASP Top 10中的安全风险点，以及在持续集成/持续交付（CI/CD）流程中强制执行安全控制措施。
---
# 高级安全运营工程师

这是一套完整的安全运营工具包，涵盖了漏洞管理、合规性验证、安全编码实践以及安全自动化等功能。

---

## 目录

- [核心功能](#core-capabilities)
- [工作流程](#workflows)
- [工具参考](#tool-reference)
- [安全标准](#security-standards)
- [合规性框架](#compliance-frameworks)
- [最佳实践](#best-practices)

---

## 核心功能

### 1. 安全扫描器

扫描源代码中的安全漏洞，包括硬编码的秘密信息、SQL注入、XSS攻击、命令注入和路径遍历等问题。

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
- SQL注入漏洞（字符串拼接、f-string、模板字面量）
- XSS漏洞（innerHTML赋值、不安全的DOM操作、React中的不安全代码模式）
- 命令注入（使用用户输入执行shell命令、eval函数）
- 路径遍历（使用用户输入进行文件操作）

### 2. 漏洞评估器

扫描npm、Python和Go生态系统中的已知CVE（安全漏洞）。

```bash
# Assess project dependencies
python scripts/vulnerability_assessor.py /path/to/project

# Critical/high only
python scripts/vulnerability_assessor.py /path/to/project --severity high

# Export vulnerability report
python scripts/vulnerability_assessor.py /path/to/project --json --output vulns.json
```

**扫描范围：**
- `package.json` 和 `package-lock.json`（npm）
- `requirements.txt` 和 `pyproject.toml`（Python）
- `go.mod`（Go）

**输出结果：**
- CVE ID及其CVSS评分
- 受影响的软件包版本
- 已修复的版本（用于修复漏洞）
- 总体风险评分（0-100分）

### 3. 合规性检查器

验证软件是否符合SOC 2、PCI-DSS、HIPAA和GDPR等安全标准。

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
- 访问控制机制
- 数据存储和传输过程中的加密
- 审计日志记录
- 认证强度（多因素认证、密码哈希）
- 安全文档
- 持续集成/持续部署（CI/CD）过程中的安全控制

---

## 工作流程

### 工作流程1：安全审计

对代码库进行全面的安全评估。

```bash
# Step 1: Scan for code vulnerabilities
python scripts/security_scanner.py . --severity medium
# STOP if exit code 2 — resolve critical findings before continuing
```

```bash
# Step 2: Check dependency vulnerabilities
python scripts/vulnerability_assessor.py . --severity high
# STOP if exit code 2 — patch critical CVEs before continuing
```

```bash
# Step 3: Verify compliance controls
python scripts/compliance_checker.py . --framework all
# STOP if exit code 2 — address critical gaps before proceeding
```

```bash
# Step 4: Generate combined reports
python scripts/security_scanner.py . --json --output security.json
python scripts/vulnerability_assessor.py . --json --output vulns.json
python scripts/compliance_checker.py . --json --output compliance.json
```

### 工作流程2：CI/CD安全门

将安全检查集成到部署流程中。

```yaml
# .github/workflows/security.yml
name: "security-scan"

on:
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: "set-up-python"
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: "security-scanner"
        run: python scripts/security_scanner.py . --severity high

      - name: "vulnerability-assessment"
        run: python scripts/vulnerability_assessor.py . --severity critical

      - name: "compliance-check"
        run: python scripts/compliance_checker.py . --framework soc2
```

如果任何步骤返回非成功状态（退出代码为错误），则部署流程将停止。

### 工作流程3：CVE处理

响应影响应用程序的新漏洞。

```
1. ASSESS (0-2 hours)
   - Identify affected systems using vulnerability_assessor.py
   - Check if CVE is being actively exploited
   - Determine CVSS environmental score for your context
   - STOP if CVSS 9.0+ on internet-facing system — escalate immediately

2. PRIORITIZE
   - Critical (CVSS 9.0+, internet-facing): 24 hours
   - High (CVSS 7.0-8.9): 7 days
   - Medium (CVSS 4.0-6.9): 30 days
   - Low (CVSS < 4.0): 90 days

3. REMEDIATE
   - Update affected dependency to fixed version
   - Run security_scanner.py to verify fix (must return exit code 0)
   - STOP if scanner still flags the CVE — do not deploy
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
- Vulnerabilities patched (run security_scanner.py; must return exit code 0)
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
| `--severity, -s` | 严重程度：严重、高、中、低 |
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
| `--severity, -s` | 严重程度：严重、高、中、低 |
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
| `--framework, -f` | 检查的框架：SOC 2、PCI-DSS、HIPAA、GDPR或全部 |
| `--verbose, -v` | 执行检查时显示进度信息 |
| `--json` | 以JSON格式输出结果 |
| `--output, -o` | 将结果写入文件 |

**退出代码：**
- `0`：符合安全标准（得分90%以上） |
- `1`：不符合安全标准（得分50-69%） |
- `2`：存在严重安全漏洞（得分低于50%）

---

## 安全标准

请参阅 `references/security_standards.md`，了解OWASP Top 10安全指南、安全编码标准、认证要求以及API安全控制措施。

### 安全编码检查清单

```markdown
## Input Validation
- [ ] Validate all input on server side
- [ ] Use allowlists over denylists
- [ ] Sanitize for specific context (HTML, SQL, shell)

## Output Encoding
- [ ] HTML encode for browser output
- [ ] URL encode for URLs
- [ ] JavaScript encode for script contexts

## Authentication
- [ ] Use bcrypt/argon2 for passwords
- [ ] Implement MFA for sensitive operations
- [ ] Enforce strong password policy

## Session Management
- [ ] Generate secure random session IDs
- [ ] Set HttpOnly, Secure, SameSite flags
- [ ] Implement session timeout (15 min idle)

## Error Handling
- [ ] Log errors with context (no secrets)
- [ ] Return generic messages to users
- [ ] Never expose stack traces in production

## Secrets Management
- [ ] Use environment variables or secrets manager
- [ ] Never commit secrets to version control
- [ ] Rotate credentials regularly
```

---

## 合规性框架

请参阅 `references/compliance_requirements.md`，了解各项安全控制要求的详细映射。运行 `compliance_checker.py` 可以验证这些控制措施是否得到满足：

### SOC 2 Type II
- **CC6** 逻辑访问：认证、授权、多因素认证（MFA）
- **CC7** 系统运营：监控、日志记录、事件响应
- **CC8** 变更管理：持续集成/持续部署（CI/CD）、代码审查、部署控制

### PCI-DSS v4.0
- **要求3/4**：数据存储和传输过程中的加密（TLS 1.2及以上）
- **要求6**：安全开发（输入验证、安全编码）
- **要求8**：强认证机制（多因素认证、密码策略）
- **要求10/11**：审计日志记录、静态应用安全测试（SAST）、动态应用安全测试（DAST）、渗透测试

### HIPAA安全规则
- 个人健康信息（PHI）访问需使用唯一用户ID和审计追踪（164.312(a)(1)、164.312(b)）
- 个人/实体认证需使用多因素认证（164.312(d)）
- 数据传输需使用TLS加密（164.312(e)(1)）

### GDPR
- **第25/32条**：数据保护设计原则、数据加密、数据匿名化
- **第33条**：数据泄露需在72小时内通知相关方
- **第17/20条**：数据删除权和数据可移植性

---

## 最佳实践

### 秘密信息管理

```python
# BAD: Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# GOOD: Environment variable
import os
API_KEY = os.environ.get("API_KEY")

# BETTER: Secrets manager
from your_vault_client import get_secret
API_KEY = get_secret("api/key")
```

### SQL注入防护

```python
# BAD: String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS防护

```javascript
// BAD: Direct innerHTML assignment is vulnerable
// GOOD: Use textContent (auto-escaped)
element.textContent = userInput;

// GOOD: Use sanitization library for HTML
import DOMPurify from 'dompurify';
const safeHTML = DOMPurify.sanitize(userInput);
```

### 认证机制

```javascript
// Password hashing
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// Hash password
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// Verify password
const match = await bcrypt.compare(password, hash);
```

### 安全头部设置

```javascript
// Express.js security headers
const helmet = require('helmet');
app.use(helmet());

// Or manually set headers:
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## 参考文档

| 文档 | 描述 |
|----------|-------------|
| `references/security_standards.md` | OWASP Top 10安全标准、安全编码规范、认证机制、API安全要求 |
| `references/vulnerability_management_guide.md` | CVE处理流程、CVSS评分标准、漏洞修复指南 |
| `references/compliance_requirements.md` | SOC 2、PCI-DSS、HIPAA、GDPR的安全控制要求映射 |