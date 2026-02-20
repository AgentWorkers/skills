---
name: afrexai-cybersecurity-engine
description: 完成全面的网络安全评估、威胁建模以及系统加固工作。适用于进行安全审计、威胁建模、渗透测试、事件响应，或从零开始构建安全防护体系。该工具支持任何技术栈（stack），且完全不依赖任何外部组件（zero external dependencies）。
metadata: {"openclaw":{"emoji":"🛡️","os":["linux","darwin","win32"]}}
---
# 网络安全引擎

这是一套全面的安全评估、威胁建模、漏洞管理、事件响应以及安全程序设计方法论。无需任何工具——仅依靠专业知识和技能，适用于任何代码库、基础设施或组织。

## 第1阶段：安全态势评估

### 快速健康检查（5分钟）

请检查以下三个层级：

**层级1 — 非常严重（需立即修复）：**
- [ ] 生产环境中使用默认凭据
- [ ] 源代码或环境文件中包含敏感信息并被提交到Git
- [ ] 管理端点没有身份验证
- [ ] 用户界面表单存在SQL注入漏洞
- [ ] 静态存储的敏感数据未加密
- [ ] 使用公共S3存储桶或云存储服务
- [ ] 未强制使用HTTPS
- [ ] 以root/admin权限运行应用程序进程

**层级2 — 高度严重（需在本周内修复）：**
- [ ] 依赖项存在已知的安全漏洞（CVSS评分≥7.0）
- [ ] 身份验证端点没有速率限制
- [ ] 改变状态的操作缺乏CSRF保护
- [ ] 错误信息过于详细，泄露了堆栈跟踪信息
- [ ] API端点没有输入验证
- [ ] 密码策略过于简单（长度小于12个字符，缺乏复杂性）
- [ ] 会话令牌包含在URL参数中
- [ ] 未记录身份验证事件

**层级3 — 中等严重（需在本冲刺周期内修复）：**
- [ ] 缺少安全头部信息（如CSP、HSTS、X-Frame-Options）
- [ ] 构建过程中没有自动依赖项扫描
- [ ] 服务账户权限过高
- [ ] 未实施密码轮换策略
- [ ] 失败登录后没有账户锁定机制
- [ ] 未制定安全报告政策
- [ ] Cookie没有设置Secure/HttpOnly/SameSite属性

**评分标准：** 根据失败项的数量进行评分。0-2分表示安全状况良好；3-5分表示需要改进；6分及以上表示应停止新功能的开发，优先修复安全问题。

### 完整评估报告

```yaml
assessment:
  name: "[Project/Org Name] Security Assessment"
  date: "YYYY-MM-DD"
  assessor: "[Agent/Person]"
  scope:
    applications:
      - name: "[App Name]"
        type: "web|api|mobile|desktop|iot"
        tech_stack: "[languages, frameworks, DBs]"
        hosting: "cloud|on-prem|hybrid"
        cloud_provider: "aws|gcp|azure|other"
        internet_facing: true|false
        handles_pii: true|false
        handles_payments: true|false
        handles_phi: true|false  # health data
    infrastructure:
      - servers: "[count, OS types]"
        containers: true|false
        orchestration: "k8s|ecs|nomad|none"
        cdn: "[provider or none]"
        dns: "[provider]"
    third_parties:
      - name: "[service]"
        data_shared: "[what data]"
        criticality: "high|medium|low"
  compliance_requirements:
    - "SOC 2|ISO 27001|GDPR|HIPAA|PCI DSS|SOX|none"
  previous_incidents:
    - date: "YYYY-MM-DD"
      type: "[breach|vuln|misconfiguration]"
      severity: "critical|high|medium|low"
      resolution: "[what was done]"
  risk_tolerance: "conservative|moderate|aggressive"
```

## 第2阶段：威胁建模（STRIDE+）

### 第1步 — 系统分解

对于每个应用程序，绘制数据流图：

```
[User] → [CDN/WAF] → [Load Balancer] → [Web Server] → [App Server] → [Database]
                                                     ↘ [Cache]
                                                     ↘ [Message Queue] → [Worker]
                                                     ↘ [Third-party API]
                                                     ↘ [Object Storage]
```

**识别权限边界** — 即权限级别发生变化的位置：
- 互联网 → 非军事区（公共服务）
- 非军事区 → 内部网络（应用服务器、数据库）
- 应用程序 → 数据库（凭据边界）
- 用户 → 管理员（角色边界）
- 服务 → 服务（API密钥边界）
- 你的基础设施 → 第三方服务（信任边界）

### 第2步 — 对每个组件进行STRIDE分析

对于每个跨越权限边界的组件：

| 威胁 | 相关问题 | 示例攻击方式 |
|--------|----------|----------------|
| **欺骗**（Spoofing） | 攻击者能否伪装成其他人？ | 偷取JWT令牌、会话劫持、凭证注入 |
| **篡改**（Tampering） | 数据在传输或存储过程中能否被修改？ | 中间人攻击、SQL注入、参数篡改 |
| **否认**（Repudiation） | 是否有人可以否认自己的行为？ | 缺少审计日志、未签名的交易记录 |
| **信息泄露**（Information Disclosure） | 敏感数据是否会泄露？ | 错误信息、API过度请求、侧信道攻击 |
| **服务拒绝**（Denial of Service） | 服务能否被拒绝服务？ | DDoS攻击、资源耗尽、正则表达式攻击 |
| **权限提升**（Elevation of Privilege） | 他人能否获得未经授权的访问权限？ | IDOR漏洞、访问控制漏洞、权限提升 |

### 第3步 — 威胁登记

```yaml
threats:
  - id: "T-001"
    component: "[affected component]"
    category: "S|T|R|I|D|E"
    description: "[specific attack scenario]"
    attacker_profile: "external-unauthenticated|external-authenticated|internal|insider"
    likelihood: 1-5  # 1=rare, 5=almost certain
    impact: 1-5      # 1=negligible, 5=catastrophic
    risk_score: 0     # likelihood × impact
    existing_controls: "[what's already in place]"
    residual_risk: "accept|mitigate|transfer|avoid"
    mitigation: "[specific fix]"
    priority: "P0|P1|P2|P3"
    owner: "[person/team]"
    status: "open|in-progress|mitigated|accepted"
```

### 优先级规则
- **P0**（风险≥20）：立即修复，停止其他工作
- **P1**（风险12-19）：在一周内修复
- **P2**（风险6-11）：在一个冲刺周期内修复
- **P3**（风险≤5）：记录问题，方便时再修复

## 第3阶段：应用程序安全（OWASP Top 10及其他安全问题）

### A01：访问控制漏洞

**测试检查清单：**
- [ ] 用户A能否通过更改ID来访问用户B的资源？（IDOR漏洞）
- [ ] 非管理员用户能否访问管理员端点？
- [ ] API端点是否实现了授权而不仅仅是身份验证？
- [ ] 是否禁用了目录列表显示？
- [ ] 是否正确配置了CORS（是否允许未经授权的请求？）
- [ ] JWT令牌是否容易被篡改？
- [ ] 敏感端点是否实施了速率限制？
- [ ] 服务器端是否对文件上传类型进行了验证？

**修复方案：**
```
# Authorization check pattern (every endpoint)
1. Authenticate → verify identity
2. Authorize → verify permission for THIS resource
3. Validate → verify input is within allowed bounds
4. Execute → perform the action
5. Audit → log who did what

# IDOR prevention
- NEVER use sequential IDs in URLs — use UUIDs
- ALWAYS verify resource ownership server-side
- Use middleware that auto-checks resource.owner === request.user
```

### A02：加密问题

**决策树：**
```
Need to store passwords?
  → bcrypt (cost 12+) or Argon2id
  → NEVER: MD5, SHA1, SHA256 without salt

Need to encrypt data at rest?
  → AES-256-GCM (authenticated encryption)
  → NEVER: ECB mode, DES, RC4

Need to encrypt in transit?
  → TLS 1.2+ (prefer 1.3)
  → HSTS with includeSubDomains
  → Certificate pinning for mobile apps

Need to generate random values?
  → crypto.randomBytes() / secrets.token_bytes()
  → NEVER: Math.random(), random.random()

Need to sign/verify?
  → HMAC-SHA256 for symmetric
  → Ed25519 or RSA-PSS (2048+ bits) for asymmetric
  → NEVER: RSA PKCS#1 v1.5 for new systems
```

### A03：注入攻击

**SQL注入防护：**
```
# ALWAYS use parameterized queries
✅ db.query("SELECT * FROM users WHERE id = $1", [userId])
❌ db.query("SELECT * FROM users WHERE id = " + userId)

# Test payloads (for YOUR code, during testing):
' OR '1'='1
'; DROP TABLE users;--
' UNION SELECT password FROM users--
1; WAITFOR DELAY '0:0:5'--
```

**XSS防护：**
```
# Output encoding rules:
HTML body    → HTML entity encode (&lt; &gt; &amp; &quot; &#x27;)
HTML attr    → Attribute encode + always quote attributes
JavaScript   → JavaScript encode (\\xHH)
URL          → Percent encode (%HH)
CSS          → CSS encode (\\HHHHHH)

# CSP header (strong baseline):
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://api.yourdomain.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

**命令注入防护：**
```
# NEVER pass user input to shell
✅ execFile('convert', ['-resize', size, inputFile, outputFile])
❌ exec('convert -resize ' + size + ' ' + inputFile + ' ' + outputFile)

# If you MUST use shell:
- Whitelist allowed characters (alphanumeric only)
- Use library wrappers, never string concatenation
```

### A04：不安全的设计

**安全设计检查清单：**
- [ ] 是否记录了业务逻辑被滥用的场景？
- [ ] 是否对高资源消耗的操作实施了速率限制？
- [ ] 是否设置了默认的安全策略（默认拒绝未经授权的请求）？
- [ ] 关键操作是否实现了职责分离？
- [ ] 多步骤交易是否使用了CSRF令牌？
- [ ] API分页是否有最大限制？
- [ ] 文件上传是否有限制和类型验证？
- [ ] 后台作业的数据是否经过签名和验证？

### A05：安全配置错误

**服务器加固检查清单：**
```yaml
web_server:
  - remove_default_pages: true
  - disable_directory_listing: true
  - remove_server_version_header: true
  - disable_TRACE_method: true
  - custom_error_pages: true  # no stack traces

application:
  - debug_mode: false  # NEVER in production
  - verbose_errors: false
  - default_accounts_removed: true
  - unnecessary_features_disabled: true
  - admin_panel_ip_restricted: true

cloud:
  - public_buckets: none
  - security_groups_least_privilege: true
  - imds_v2_enforced: true  # AWS
  - logging_enabled: true
  - mfa_on_root: true
  - billing_alerts: true
```

### A06-A10：快速检查

| 漏洞 | 测试方法 | 修复措施 |
|------|------|-----|
| A06：易受攻击的组件 | `npm audit`、`pip-audit`、`trivy fs .` | 更新组件、固定版本、在构建过程中自动化扫描 |
| A07：身份验证失败 | 暴力破解测试、密码策略审核、多因素认证（MFA） | 实施速率限制和账户锁定机制、使用bcrypt/Argon2加密算法 |
| A08：数据完整性 | 未签名的数据是否会影响应用程序行为？ | 所有序列化数据必须签名、验证校验和、CDN使用SRI协议 |
| A09：日志记录缺失 | 是否记录了身份验证事件、访问变更和系统故障？ | 实施结构化日志记录、集成安全信息事件管理系统（SIEM）、对异常情况发出警报 |
| A10：跨站请求伪造（SSRF） | 用户输入是否能够触发服务器端请求？ | 允许的URL列表、阻止内部IP地址的请求、禁止重定向到内部资源 |

## 第4阶段：基础设施安全

### 网络安全基线

```yaml
network_hardening:
  firewall:
    default_policy: "deny-all"
    allowed_inbound:
      - port: 443
        source: "0.0.0.0/0"
        service: "HTTPS"
      - port: 22
        source: "[admin_ip_range]"
        service: "SSH"
    rules:
      - "No direct database access from internet"
      - "Internal services communicate on private subnet"
      - "Egress filtering — block unnecessary outbound"

  ssh:
    password_auth: false
    root_login: false
    key_type: "ed25519"
    port: "[non-standard recommended]"
    fail2ban: true
    max_auth_tries: 3

  dns:
    dnssec: true
    caa_records: true  # restrict who can issue TLS certs
    no_zone_transfer: true

  tls:
    min_version: "1.2"
    preferred: "1.3"
    cipher_suites: "ECDHE+AESGCM:ECDHE+CHACHA20"
    hsts: "max-age=31536000; includeSubDomains; preload"
    certificate_monitoring: true
    auto_renewal: true
```

### 容器安全

```yaml
container_hardening:
  image:
    - base: "distroless or alpine (minimal)"
    - user: "non-root (USER 1000:1000)"
    - scan: "trivy image before push"
    - sign: "cosign or Notary"
    - pins: "use SHA256 digests, not :latest"
    - secrets: "NEVER in Dockerfile or image layers"
    - layers: "multi-stage builds, minimal final image"

  runtime:
    - read_only_rootfs: true
    - no_new_privileges: true
    - drop_all_capabilities: true
    - add_only: ["NET_BIND_SERVICE"]  # if needed
    - resource_limits: true
    - seccomp_profile: "default"
    - network_policy: "deny by default"

  registry:
    - private: true
    - vulnerability_scanning: true
    - image_signing: true
    - tag_immutability: true
```

### 云安全（AWS/GCP/Azure）

```yaml
cloud_security_baseline:
  identity:
    - root_account_mfa: true
    - no_root_access_keys: true
    - least_privilege_iam: true
    - service_accounts_scoped: true
    - temporary_credentials: true  # assume role, not long-lived keys
    - sso_enforced: true

  data:
    - encryption_at_rest: "default on all storage"
    - encryption_in_transit: "TLS everywhere"
    - backup_encryption: true
    - key_management: "cloud KMS, not self-managed"
    - data_classification: true

  network:
    - vpc_flow_logs: true
    - private_subnets_for_databases: true
    - nat_gateway_for_outbound: true
    - waf_on_public_endpoints: true
    - ddos_protection: true

  monitoring:
    - cloudtrail_enabled: true  # or equivalent
    - config_rules: true
    - guardduty_enabled: true  # or equivalent
    - cost_alerts: true
    - unused_resource_alerts: true

  storage:
    - no_public_buckets: true
    - versioning_on_critical: true
    - lifecycle_policies: true
    - access_logging: true
```

## 第5阶段：漏洞管理程序

### 漏洞生命周期管理

```
Discovery → Triage → Prioritize → Remediate → Verify → Close
    ↓          ↓         ↓            ↓          ↓
  Scan/     Confirm   CVSS +       Fix or     Retest
  Report    real?     context      compensate
```

### 漏洞严重性等级与响应时间表

| 漏洞严重性 | CVSS评分 | 修复时间表 | 升级流程 |
|----------|------|-----------------|------------|
| 非常严重 | 9.0-10.0 | 24小时内 | CTO/CISO立即处理 |
| 高度严重 | 7.0-8.9 | 7天内 | 安全团队处理 |
| 中等严重 | 4.0-6.9 | 30天内 | 在下一个冲刺周期内处理 |
| 低度严重 | 0.1-3.9 | 90天内 | 记录问题，方便时修复 |
| 信息性漏洞 | 0 | 无固定修复时间表 | 仅记录以供参考 |

### 漏洞报告模板

```yaml
vulnerability:
  id: "VULN-YYYY-NNN"
  title: "[descriptive title]"
  discovered: "YYYY-MM-DD"
  discoverer: "[scanner/person/bounty]"
  severity: "critical|high|medium|low|info"
  cvss_score: 0.0
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
  cve: "[if applicable]"
  affected:
    - component: "[app/service/library]"
      version: "[affected versions]"
      environment: "production|staging|dev"
  description: "[what the vulnerability is]"
  impact: "[what an attacker could do]"
  proof_of_concept: "[steps to reproduce]"
  remediation:
    fix: "[specific fix]"
    workaround: "[temporary mitigation]"
    compensating_control: "[if fix isn't immediate]"
  status: "open|in-progress|fixed|accepted|false-positive"
  fixed_date: "YYYY-MM-DD"
  verified_by: "[person who confirmed fix]"
```

### 扫描计划

| 扫描类型 | 扫描频率 | 使用的工具示例 |
|-----------|-----------|---------------|
| 依赖项扫描 | 每次构建时 | `npm audit`、`pip-audit`、`trivy` |
| 静态应用安全测试（SAST） | 每次提交代码时 | `Semgrep`、`CodeQL`、`Bandit` |
| 秘密信息扫描 | 每次提交代码时 | `GitLeaks`、`truffleHog`、GitHub秘密信息扫描工具 |
| 容器扫描 | 每次构建容器镜像时 | `Trivy`、`Grype`、`Snyk Container` |
| 运行时安全测试（DAST） | 每周 | `OWASP ZAP`、`Burp Suite`、`Nuclei` |
| 云配置扫描 | 每天 | `ScoutSuite`、`Prowler`、`CloudSploit` |
| 渗透测试 | 每季度 | 手动测试+自动化测试 |
| 渗透测试团队 | 每年 | 外部专业机构进行 |

## 第6阶段：事件响应

### 事件严重等级与响应时间

| 事件等级 | 定义 | 响应时间 | 负责团队 |
|-------|-----------|---------------|------|
| SEV-1 | 发生数据泄露、服务中断 | 15分钟内 | 全体团队+管理层+法律部门 |
| SEV-2 | 漏洞被主动利用、系统部分受损 | 1小时内 | 安全团队+受影响团队负责人 |
| SEV-3 | 发现可疑活动、可能存在系统被入侵的迹象 | 4小时内 | 安全团队 |
| SEV-4 | 低风险问题、违反安全政策、攻击未成功 | 下一个工作日 | 指定工程师处理 |

### 事件响应流程

**第1阶段 — 发现与分类（前15分钟）**
```
1. Confirm incident is real (not false positive)
2. Classify severity (SEV-1 through SEV-4)
3. Assign incident commander
4. Open incident channel (Slack/Teams)
5. Start incident log with timestamps
6. Notify stakeholders per severity
```

**第2阶段 — 控制与遏制（1小时内）**
```
SHORT-TERM (stop the bleeding):
- Isolate affected systems (network segmentation)
- Revoke compromised credentials immediately
- Block attacking IP/user agent
- Enable enhanced logging on affected systems
- Preserve forensic evidence (DON'T reboot/wipe yet)

LONG-TERM (prevent spread):
- Patch the vulnerability that was exploited
- Rotate ALL credentials that may be compromised
- Update firewall/WAF rules
- Deploy additional monitoring
```

**第3阶段 — 消除威胁**
```
1. Identify root cause
2. Remove all attacker artifacts (backdoors, malware, new accounts)
3. Patch all instances of the vulnerability
4. Verify no lateral movement occurred
5. Confirm all compromised credentials rotated
```

**第4阶段 — 恢复**
```
1. Restore from clean backups (verify backup integrity first)
2. Rebuild compromised systems from scratch (don't trust cleanup)
3. Monitor restored systems with enhanced logging
4. Gradual return to production (staged rollback)
5. Confirm normal operations for 48 hours
```

**第5阶段 — 事件后续处理**
```yaml
post_mortem:
  incident_id: "INC-YYYY-NNN"
  date: "YYYY-MM-DD"
  severity: "SEV-1|2|3|4"
  duration: "[detection to resolution]"
  impact:
    users_affected: 0
    data_compromised: "[type and volume]"
    financial_impact: "$0"
    regulatory_notification_required: true|false
  timeline:
    - time: "HH:MM"
      event: "[what happened]"
      action: "[what we did]"
  root_cause: "[specific technical cause]"
  contributing_factors:
    - "[what made it possible or worse]"
  what_went_well:
    - "[detection, response, communication]"
  what_went_poorly:
    - "[gaps, delays, confusion]"
  action_items:
    - action: "[specific improvement]"
      owner: "[person]"
      due: "YYYY-MM-DD"
      status: "open|done"
  lessons_learned:
    - "[distilled insight]"
```

### 通信模板

**内部通知（SEV-1/2）：**
```
🚨 SECURITY INCIDENT — [severity]
What: [brief description]
Impact: [what's affected]
Status: [containment/investigation/resolved]
Incident Commander: [name]
Channel: #incident-[id]
Next update: [time]

DO NOT discuss outside this channel.
```

**客户通知（如需）：**
```
Subject: Security Notice — [Company Name]

We're writing to inform you of a security incident that [may have|affected] your account.

What happened: [brief, honest description]
When: [date range]
What data was involved: [specific data types]
What we've done: [remediation steps]
What you should do: [password reset, monitor accounts, etc.]
Contact: [security team email/phone]

We take the security of your data seriously and have [specific improvements].
```

## 第7阶段：安全头部与浏览器安全

### 必需的HTTP头部信息

```
# Copy-paste baseline for production:
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
X-XSS-Protection: 0  # Disabled — CSP handles this; old header can cause issues
```

### Cookie安全

```
Set-Cookie: session=<token>;
  Secure;                    # HTTPS only
  HttpOnly;                  # No JavaScript access
  SameSite=Lax;              # CSRF protection (Strict if no cross-site navigation needed)
  Path=/;                    # Scope appropriately
  Max-Age=3600;              # 1 hour (adjust per use case)
  Domain=.yourdomain.com;    # Explicit domain
```

## 第8阶段：身份验证与授权

### 符合NIST 800-63B标准的密码策略

```yaml
password_policy:
  minimum_length: 12  # NIST minimum is 8, 12+ recommended
  maximum_length: 128  # Must support long passwords
  complexity_rules: false  # NIST says don't require special chars
  check_against_breached: true  # HaveIBeenPwned API
  no_password_hints: true
  no_security_questions: true  # Easy to social engineer
  allow_paste: true  # For password managers
  rate_limit_attempts: "5 per 15 minutes"
  lockout_duration: "progressive (1min, 5min, 15min, 1hr)"
  mfa_required: "all accounts"
  mfa_methods:
    preferred: "TOTP or WebAuthn/passkeys"
    acceptable: "push notification"
    discouraged: "SMS (SIM swap risk)"
  storage: "Argon2id or bcrypt cost 12+"
```

### JWT令牌安全检查

```yaml
jwt_security:
  signing:
    algorithm: "RS256 or EdDSA"  # NEVER HS256 with shared secrets in distributed systems
    key_rotation: "quarterly"
    verify_algorithm: true  # Reject alg=none
  claims:
    exp: "required — 15 min for access, 7d for refresh"
    iss: "required — validate on every request"
    aud: "required — validate matches expected service"
    iat: "required"
    jti: "recommended — for revocation"
    nbf: "recommended"
  storage:
    access_token: "memory only (never localStorage)"
    refresh_token: "httpOnly secure cookie"
  revocation:
    method: "token blacklist with Redis TTL matching exp"
    on_password_change: "revoke all tokens"
    on_permission_change: "revoke all tokens"
```

### OAuth 2.0 / OIDC安全检查

- [ ] 使用带有PKCE的授权码流（绝不要使用隐式授权方式）
- [ ] 验证`state`参数以防止CSRF攻击 |
- [ ] 验证`nonce`参数以防止重放攻击 |
- [ ] 验证令牌发行者和接收者的身份 |
- [ ] 令牌应存储在服务器端，而非浏览器端 |
- [ ] 为刷新令牌实施令牌轮换机制 |
- [ ] 设置最小权限范围（最小权限原则） |
- [ ] 明确指定重定向URL（避免使用通配符）

## 第9阶段：安全程序设计

### 从零开始构建安全程序

**第1季度 — 基础构建：**
```
Week 1-2: Asset inventory (what do we have?)
Week 3-4: Risk assessment (what matters most?)
Week 5-6: Critical controls (authentication, secrets, backups)
Week 7-8: Basic scanning (dependencies, secrets in code)
Week 9-10: Incident response plan (what if something happens?)
Week 11-12: Security awareness basics (phishing, passwords)
```

**第2季度 — 自动化流程：**
```
- CI/CD security scanning (SAST, dependency audit)
- Automated secret detection (pre-commit hooks)
- Centralized logging and basic alerting
- Access reviews (quarterly)
- Vulnerability management process
```

**第3季度 — 安全体系成熟度提升：**
```
- Penetration testing (first external assessment)
- Security architecture review
- Data classification and handling policies
- Vendor security assessments
- Bug bounty program (start small)
```

**第4季度 — 优化改进：**
```
- Compliance framework alignment (SOC 2, ISO 27001)
- Red team exercise
- Security metrics dashboard
- Security champion program (devs with security training)
- Supply chain security (SBOM, signed artifacts)
```

### 安全指标仪表盘

```yaml
security_dashboard:
  vulnerability_management:
    - open_critical: 0  # Target: always 0
    - open_high: 0      # Target: < 5
    - mean_time_to_remediate:
        critical: "24h"  # Target
        high: "7d"
        medium: "30d"
    - scan_coverage: "100%"  # % of repos with automated scanning

  incident_management:
    - incidents_this_quarter: 0
    - mean_time_to_detect: "< 1h"
    - mean_time_to_respond: "< 4h"
    - mean_time_to_recover: "< 24h"

  access_control:
    - mfa_adoption: "100%"
    - privileged_accounts: 0  # Count, minimize
    - stale_accounts: 0       # Accounts unused > 90 days
    - access_reviews_completed: "on schedule"

  code_security:
    - repos_with_sast: "100%"
    - repos_with_dependency_scanning: "100%"
    - secret_detection_coverage: "100%"
    - security_review_for_critical_changes: "100%"

  training:
    - security_awareness_completion: "100%"
    - phishing_simulation_click_rate: "< 5%"
    - security_champions_per_team: ">= 1"
```

## 第10阶段：渗透测试方法论

### 侦察阶段

```
PASSIVE (no direct interaction with target):
1. DNS enumeration: subdomains, MX, TXT, CNAME
   - Tools: subfinder, amass, crt.sh, dnsdumpster
2. Technology fingerprinting
   - Check: Wappalyzer, BuiltWith, HTTP headers
3. Public exposure
   - Shodan/Censys for open ports/services
   - GitHub/GitLab for leaked code/secrets
   - Wayback Machine for old endpoints
4. Employee OSINT (for social engineering scope)
   - LinkedIn for tech stack clues
   - Job postings reveal internal tools

ACTIVE (interacting with target — requires permission):
1. Port scanning: full TCP + top 1000 UDP
2. Service enumeration: version detection
3. Web crawling: sitemap, robots.txt, directory brute-force
4. API discovery: /api, /v1, /graphql, /swagger, /openapi
```

### 测试阶段

**第1阶段 — 身份验证测试**
```
- Credential stuffing resistance (rate limiting)
- Password reset flow (token guessability, expiry, reuse)
- Account enumeration (different responses for valid/invalid users)
- Session management (token entropy, fixation, timeout)
- MFA bypass attempts (backup codes, race conditions)
- OAuth flow attacks (redirect URI manipulation, scope escalation)
```

**第2阶段 — 授权测试**
```
- Horizontal privilege escalation (access other users' data)
- Vertical privilege escalation (user → admin)
- Missing function-level access control (direct API calls)
- IDOR on every resource endpoint (change IDs systematically)
- GraphQL introspection + unauthorized field access
- Mass assignment (send extra fields in requests)
```

**第3阶段 — 注入攻击测试**
```
- SQL injection on all user inputs (including headers, cookies)
- XSS (reflected, stored, DOM-based) on all output points
- Command injection on any server-side execution
- SSRF on any URL input or file fetch
- Template injection (if server-side templating)
- LDAP/XML/XXE injection where applicable
```

**第4阶段 — 业务逻辑测试**
```
- Price manipulation (change prices in requests)
- Quantity manipulation (negative numbers, decimals, MAX_INT)
- Race conditions (concurrent requests for same resource)
- Workflow bypass (skip steps in multi-step processes)
- Coupon/discount abuse (reuse, stacking)
- Rate limit bypass (header rotation, distributed requests)
```

### 渗透测试报告模板

```yaml
report:
  executive_summary:
    overall_risk: "critical|high|medium|low"
    critical_findings: 0
    high_findings: 0
    medium_findings: 0
    low_findings: 0
    key_recommendations:
      - "[top 3 fixes by impact]"

  scope:
    targets: "[URLs, IPs, apps tested]"
    methodology: "OWASP Testing Guide v4.2 + PTES"
    dates: "YYYY-MM-DD to YYYY-MM-DD"
    type: "black-box|grey-box|white-box"
    exclusions: "[what was out of scope]"

  findings:
    - id: "F-001"
      title: "[descriptive title]"
      severity: "critical|high|medium|low|info"
      cvss: 0.0
      location: "[URL/endpoint/component]"
      description: "[what the vulnerability is]"
      impact: "[what an attacker could do]"
      evidence: "[screenshots, request/response pairs]"
      reproduction_steps:
        - "[step by step]"
      remediation: "[specific fix with code examples]"
      references:
        - "[OWASP, CWE, CVE links]"

  positive_observations:
    - "[security controls that were effective]"
```

## 第11阶段：供应链安全

### 依赖项安全管理

```yaml
supply_chain:
  dependencies:
    - lock_files: "always commit (package-lock.json, poetry.lock, go.sum)"
    - pin_versions: "exact versions, not ranges"
    - audit_frequency: "every CI build"
    - auto_update: "Dependabot/Renovate with auto-merge for patch, review for minor/major"
    - review_new_deps:
        check: "maintainer count, last update, download count, known issues"
        rule: "no single-maintainer deps for critical paths"
    - sbom: "generate SPDX or CycloneDX on every release"

  build_pipeline:
    - reproducible_builds: true
    - artifact_signing: true
    - build_provenance: true  # SLSA Level 2+
    - no_curl_pipe_bash: true  # Never pipe internet scripts to shell
    - verify_checksums: true

  ci_cd:
    - pin_action_versions: "use SHA, not tags (actions/checkout@SHA)"
    - least_privilege_tokens: true
    - no_secrets_in_logs: true
    - protected_branches: true
    - required_reviews: true
    - signed_commits: "recommended"
```

## 第12阶段：安全评分标准

对每个应用程序/系统进行0-100分的评分：

| 评估维度 | 权重 | 0（非常差） | 5（良好） | 10（优秀） |
|-----------|--------|---------------|---------------|-----------------|
| 身份验证与访问控制 | 20% | 无身份验证或使用默认凭据 | 使用多因素认证（MFA）+基于属性的访问控制（ABAC）+零信任原则 |
| 数据保护 | 15% | 数据以明文形式存储、未加密 | 数据在存储和传输过程中都经过加密 | 使用端到端加密、定期更新密钥 |
| 漏洞管理 | 15% | 未进行漏洞扫描、存在已知安全漏洞 | 实施自动化扫描、遵守安全时间表（MTTD<1小时）、提供漏洞赏金机制 |
| 基础设施安全 | 15% | 开放端口、未配置防火墙 | 实施强化的安全基线、最小权限原则 | 实施零信任策略、微分段 |
| 日志记录与监控 | 10% | 未记录安全事件 | 集中化日志管理、基本告警机制 | 集成安全信息事件管理系统（SIEM）、异常检测、24/7安全运营（SOC） |
| 事件响应 | 10% | 无事件响应计划 | 有详细的响应计划、每年进行测试 | 自动化响应、响应时间小于1小时 |
| 代码安全 | 10% | 代码未经过审查、存在注入漏洞 | 在构建过程中进行静态应用安全测试（SAST）、代码同行评审 | 全流程安全审查、定期进行威胁建模 |
| 供应链安全 | 5% | 未管理依赖项 | 未对依赖项进行安全检查 | 对文件进行加密、使用安全包清单（SBOM）、对安全组件进行签名 |

**评分解释：**
- 90-100分：安全性能卓越，具有竞争优势 |
- 70-89分：基础安全良好，需持续改进 |
- 50-69分：存在严重安全问题，需立即修复 |
- 低于50分：安全状况极差，应停止新功能的开发，优先修复安全问题 |

## 常见错误

1. **依赖隐蔽性带来的安全防护** — 将管理员面板隐藏在/secret-admin路径下并不能真正提高安全性 |
2. **仅依赖客户端验证** — 必须同时进行服务器端验证 |
3. **过度信任内部网络** — 应始终假设可能存在安全风险，对所有网络流量进行验证 |
4. **在日志中记录敏感信息** — 密码、令牌、个人身份信息（PII）如果被记录在日志中，就等于为安全问题埋下隐患 |
5. **“公司规模太小，不会成为攻击目标”** — 自动化攻击并不考虑公司的规模 |
6. **认为只需进行一次性安全审计** — 安全防护是一个持续的过程，不是简单的检查项 |
7. **在开发/测试环境中忽视安全措施** — 攻击者也会攻击测试环境 |
8. **为方便而过度授权** — 应始终遵循最小权限原则 |
9. **未进行备份测试** — 未经测试的备份毫无意义 |
10. **将合规性视为等同于安全** — SOC 2等级认证仅是安全的基础，而非最终目标 |

## 特殊情况

- **完全没有安全措施的初创公司**：从第9阶段（基础构建）开始 |
- **旧有应用程序**：在修复代码之前，先关注网络隔离、Web应用防火墙（WAF）和监控机制 |
- **微服务架构**：使用TLS协议、集中式身份验证（OAuth/OIDC）、API网关 |
- **物联网/嵌入式系统**：假设可能存在物理攻击，对固件进行加密、更新文件需签名、减少攻击面 |
- **移动应用程序**：对证书进行固定、检测root权限滥用、保护本地存储安全 |
- **无服务器架构（Serverless）**：在函数级别实施身份验证（IAM）、代码中不存储敏感信息、限制API调用频率 |
- **多租户SaaS平台**：确保租户之间的隔离、防止数据泄露 |

## 相关命令

```
"Audit security of [project/repo]" → Full assessment (Phase 1-4)
"Threat model [system/feature]" → STRIDE analysis (Phase 2)
"Check OWASP top 10 for [app]" → Application security review (Phase 3)
"Harden [server/container/cloud]" → Infrastructure checklist (Phase 4)
"Create incident response plan" → IR playbook (Phase 6)
"Design security program" → Phased program build (Phase 9)
"Pentest methodology for [target]" → Testing phases (Phase 10)
"Score security of [system]" → 100-point rubric (Phase 12)
"Review auth implementation" → Auth deep dive (Phase 8)
"Check security headers" → Header audit (Phase 7)
"Vulnerability report for [finding]" → Report template (Phase 5)
"Supply chain security review" → Dependency audit (Phase 11)
```