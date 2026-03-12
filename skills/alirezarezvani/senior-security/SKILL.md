---
name: "senior-security"
description: 这是一个用于威胁建模、漏洞分析、安全架构设计和渗透测试的安全工程工具包。它包含了STRIDE分析方法、OWASP安全指南、加密模式以及各种安全扫描工具。当用户需要关于安全审查、威胁分析、漏洞评估、安全编码实践、安全审计、攻击面分析、CVE漏洞修复或安全最佳实践的帮助时，可以使用该工具包。
triggers:
  - security architecture
  - threat modeling
  - STRIDE analysis
  - penetration testing
  - vulnerability assessment
  - secure coding
  - OWASP
  - application security
  - cryptography implementation
  - secret scanning
  - security audit
  - zero trust
---
# 高级安全工程师

负责威胁建模、漏洞分析、安全架构设计以及渗透测试的安全工程工具。

---

## 目录

- [威胁建模工作流程](#threat-modeling-workflow)
- [安全架构工作流程](#security-architecture-workflow)
- [漏洞评估工作流程](#vulnerability-assessment-workflow)
- [安全代码审查工作流程](#secure-code-review-workflow)
- [事件响应工作流程](#incident-response-workflow)
- [安全工具参考](#security-tools-reference)
- [工具与参考资料](#tools-and-references)

---

## 威胁建模工作流程

使用STRIDE方法识别和分析安全威胁。

### 工作流程：进行威胁建模

1. 定义系统范围和边界：
   - 确定需要保护的资产
   - 绘制信任边界
   - 文档化数据流
2. 创建数据流图：
   - 外部实体（用户、服务）
   - 过程（应用程序组件）
   - 数据存储（数据库、缓存）
   - 数据流（API、网络连接）
3. 将STRIDE应用于每个数据流图元素（详见[STRIDE元素矩阵](#stride-per-element-matrix)）
4. 使用DREAD对风险进行评分：
   - 损害潜力（1-10）
   - 可复现性（1-10）
   - 可利用性（1-10）
   - 受影响的用户（1-10）
   - 可发现性（1-10）
5. 根据风险评分对威胁进行优先级排序
6. 为每个威胁制定缓解措施
7. 在威胁模型报告中记录这些措施
8. **验证：**所有数据流图元素均已分析；STRIDE方法已应用；威胁已评分；缓解措施已确定

### STRIDE威胁类别

| 类别 | 安全属性 | 缓解措施重点 |
|----------|-------------------|------------------|
| 伪造 | 认证 | 多因素认证（MFA）、证书、强密码认证 |
| 篡改 | 完整性 | 签名、校验和、验证 |
| 否认行为 | 不可否认性 | 审计日志、数字签名 |
| 信息泄露 | 保密性 | 加密、访问控制 |
| 服务拒绝 | 可用性 | 速率限制、冗余 |
| 权限提升 | 授权 | 基于角色的访问控制（RBAC）、最小权限原则 |

### STRIDE元素矩阵

| 数据流图元素 | S | T | R | I | D | E |
|-------------|---|---|---|---|---|---|
| 外部实体 | X | | X | | | |
| 过程 | X | X | X | X | X | X |
| 数据存储 | | X | X | X | X | |
| 数据流 | | X | | X | X | |

更多信息请参阅：[references/threat-modeling-guide.md](references/threat-modeling-guide.md)

---

## 安全架构工作流程

使用纵深防御原则设计安全系统。

### 工作流程：设计安全架构

1. 定义安全需求：
   - 合规性要求（GDPR、HIPAA、PCI-DSS）
   - 数据分类（公开、内部、机密、受限）
   - 威胁模型输入
2. 应用纵深防御层次：
   - 外围防御：Web应用防火墙（WAF）、DDoS防护、速率限制
   - 网络：网络分段、入侵检测系统（IDS/IPS）、传输层安全（TLS）
   - 主机：补丁管理、端点检测（EDR）、系统加固
   - 应用程序：输入验证、认证、安全编码
   - 数据：静态和传输过程中的加密
3. 实施零信任原则：
   - 明确验证（每个请求）
   - 最小权限访问（JIT/JEA）
   | 假设已发生泄露（进行分段和监控）
4. 配置认证和授权：
   - 身份提供者选择
   - 多因素认证要求
   - 基于角色的访问控制（RBAC）/基于属性的访问控制（ABAC）
5. 设计加密策略：
   - 密钥管理方法
   - 算法选择
   - 证书生命周期管理
6. 规划安全监控：
   - 日志聚合
   - 安全信息事件管理系统（SIEM）集成
   - 警报规则
7. 文档化架构决策
8. **验证：**纵深防御层次已定义；零信任原则已应用；加密策略已记录；监控计划已制定

### 深度防御层次

```
Layer 1: PERIMETER
  WAF, DDoS mitigation, DNS filtering, rate limiting

Layer 2: NETWORK
  Segmentation, IDS/IPS, network monitoring, VPN, mTLS

Layer 3: HOST
  Endpoint protection, OS hardening, patching, logging

Layer 4: APPLICATION
  Input validation, authentication, secure coding, SAST

Layer 5: DATA
  Encryption at rest/transit, access controls, DLP, backup
```

### 认证模式选择

| 使用场景 | 推荐模式 |
|----------|---------------------|
| Web应用程序 | OAuth 2.0 + PKCE与OIDC |
| API认证 | 密钥交换（JWT）+ 过期时间短+刷新令牌 |
| 服务间通信 | 使用证书轮换的TLS |
| 命令行接口/自动化 | 基于IP地址的白名单机制 |
| 高安全要求 | FIDO2/WebAuthn硬件密钥 |

更多信息请参阅：[references/security-architecture-patterns.md](references/security-architecture-patterns.md)

---

## 漏洞评估工作流程

识别并修复应用程序中的安全漏洞。

### 工作流程：进行漏洞评估

1. 定义评估范围：
   - 评估范围内的系统和应用程序
   - 测试方法（黑盒测试、灰盒测试、白盒测试）
   - 测试规则
2. 收集信息：
   - 技术栈清单
   - 架构文档
   | 之前的漏洞报告 |
3. 执行自动化扫描：
   - 静态应用安全测试（SAST）
   - 动态应用安全测试（DAST）
   - 依赖项扫描
   | 秘密信息检测 |
4. 执行手动测试：
   - 业务逻辑缺陷
   - 认证绕过
   | 权限问题 |
   | 注入漏洞 |
5. 按严重程度对发现的问题进行分类：
   | 严重：立即存在被利用的风险 |
   | 高：影响显著，容易被利用 |
   | 中等：影响或难度适中 |
   | 低：影响较小 |
6. 制定修复计划：
   | 按风险优先级排序 |
   | 分配负责人 |
   | 设置截止日期 |
7. 验证修复措施并记录结果
8. **验证：**评估范围已确定；自动化和手动测试已完成；发现的问题已分类；修复措施已跟踪

有关OWASP Top 10漏洞的描述和测试指南，请访问[owasp.org/Top10](https://owasp.org/Top10)。

### 漏洞严重程度矩阵

| 影响 | 可利用性 | 易用性 | 难度 |
|-------------------------|------|----------|-----------|
| 严重 | 严重 | 严重 | 高 |
| 高 | 严重 | 高 | 中等 |
| 中等 | 高 | 中等 | 低 |
| 低 | 中等 | 低 | 低 |

---

## 安全代码审查工作流程

在部署前审查代码中的安全漏洞。

### 工作流程：进行安全代码审查

1. 确定审查范围：
   | 变更的文件和函数 |
   | 安全敏感区域（认证、加密、输入处理） |
   | 第三方集成 |
2. 运行自动化分析：
   | 静态应用安全测试工具（Semgrep、CodeQL、Bandit） |
   | 秘密信息扫描 |
   | 依赖项漏洞检查 |
3. 审查认证代码：
   | 密码处理（哈希、存储） |
   | 会话管理 |
   | 令牌验证 |
4. 审查授权代码：
   | 访问控制检查 |
   | 基于角色的访问控制（RBAC）实现 |
   | 权限边界 |
5. 审查数据处理：
   | 输入验证 |
   | 输出编码 |
   | SQL查询构建 |
   | 文件路径处理 |
6. 审查加密代码：
   | 算法选择 |
   | 密钥管理 |
   | 随机数生成 |
7. 记录发现的问题及其严重程度
8. **验证：**自动化扫描通过；认证/授权部分已审查；数据处理已检查；加密措施已验证；发现的问题已记录

### 安全代码审查检查清单

| 类别 | 检查项 | 风险 |
|----------|-------|------|
| 输入验证 | 所有用户输入均经过验证和清理 | 注入攻击 |
| 输出编码 | 应用适当的编码 | XSS攻击 |
| 认证 | 密码使用Argon2/bcrypt进行哈希处理 | 凭据被盗 |
| 会话管理 | 设置安全的cookie属性（HttpOnly、Secure、SameSite） | 会话劫持 |
| 授权 | 所有端点都进行服务器端权限检查 | 权限提升 |
| SQL | 仅使用参数化查询 | SQL注入 |
| 文件访问 | 拒绝路径遍历请求 | 防止路径遍历 |
| 秘密信息 | 无硬编码的凭证或密钥 | 信息泄露 |
| 依赖项 | 更新已知的脆弱包 | 防止供应链攻击 |
| 日志记录 | 敏感数据未记录 | 信息泄露 |

### 安全代码与不安全代码的对比

| 不安全代码模式 | 安全代码模式 |
|---------|-------|-------------------|
| SQL字符串格式化 | 使用参数化查询和占位符 |
| Shell命令构建 | 使用带有参数列表的子进程，避免使用Shell命令 |
| 路径连接 | 验证和规范化路径 |
| 使用MD5/SHA1进行密码哈希 | 使用Argon2id或bcrypt进行哈希 |
| 使用Math.random生成令牌 | 使用crypto.getRandomValues生成随机数 |

### 内联代码示例

**SQL注入——不安全代码示例（Python）：**

```python
# ❌ Insecure: string formatting allows SQL injection
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# ✅ Secure: parameterized query — user input never interpreted as SQL
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

**使用Argon2id进行密码哈希（Python）：**

```python
from argon2 import PasswordHasher

ph = PasswordHasher()          # uses secure defaults (time_cost, memory_cost)

# On registration
hashed = ph.hash(plain_password)

# On login — raises argon2.exceptions.VerifyMismatchError on failure
ph.verify(hashed, plain_password)
```

**秘密信息扫描——核心模式匹配（Python）：**

```python
import re, pathlib

SECRET_PATTERNS = {
    "aws_access_key":  re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token":    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    "private_key":     re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    "generic_secret":  re.compile(r'(?i)(password|secret|api_key)\s*=\s*["\']?\S{8,}'),
}

def scan_file(path: pathlib.Path) -> list[dict]:
    findings = []
    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append({"file": str(path), "line": lineno, "type": name})
    return findings
```

---

## 事件响应工作流程

响应并控制安全事件。

### 工作流程：处理安全事件

1. 识别和分类事件：
   | 验证事件的真实性 |
   | 评估事件的初始范围和严重程度 |
   | 激活事件响应团队 |
2. 控制威胁：
   | 隔离受影响的系统 |
   | 阻止恶意IP/账户的访问 |
   | 禁用被泄露的凭证 |
3. 消除根本原因：
   | 删除恶意软件/后门 |
   | 修补漏洞 |
   | 更新配置 |
4. 恢复操作：
   | 从备份中恢复数据 |
   | 验证系统完整性 |
   | 监控事件是否再次发生 |
5. 进行事后分析：
   | 重建事件时间线 |
   | 分析根本原因 |
   | 总结经验教训 |
6. 实施改进措施：
   | 更新检测规则 |
   | 加强控制措施 |
   | 更新应急响应流程 |
7. 记录和报告事件 |
8. **验证：**威胁已被控制；根本原因已消除；系统已恢复；事后分析已完成；改进措施已实施

### 事件严重程度等级

| 事件等级 | 响应时间 | 升级流程 |
|-------|---------------|------------|
| P1 - 严重（正在发生的泄露/数据外泄） | 立即响应 | 高层管理人员（CISO、法律顾问、高管） |
| P2 - 高（已确认，但已被控制） | 1小时 | 安全负责人、IT总监 |
| P3 - 中等（潜在威胁，正在调查中） | 4小时 | 安全团队 |
| P4 - 低（可疑，影响较小） | 24小时 | 值班工程师 |

### 事件响应检查清单

| 阶段 | 应采取的行动 |
|-------|---------|
| 识别 | 验证警报，评估事件范围，确定严重程度 |
| 控制 | 隔离系统，保留证据，阻止访问 |
| 消除威胁 | 删除恶意代码，修补漏洞，重置凭证 |
| 恢复 | 从备份中恢复服务，验证系统完整性 | 加强监控 |
| 后事分析 | 重建事件时间线，分析根本原因，总结经验 |
| 改进 | 更新检测规则，加强控制措施，更新应急响应流程 |

---

## 安全工具参考

### 推荐的安全工具

| 类别 | 工具 |
|----------|-------|
| 静态应用安全测试 | Semgrep、CodeQL、Bandit（Python）、ESLint安全插件 |
| 动态应用安全测试 | OWASP ZAP、Burp Suite、Nikto |
| 依赖项扫描 | Snyk、Dependabot、npm audit、pip-audit |
| 秘密信息检测 | GitLeaks、TruffleHog、detect-secrets |
| 容器安全 | Trivy、Clair、Anchore |
| 基础设施安全 | Checkov、tfsec、ScoutSuite |
| 网络安全 | Wireshark、Nmap、Masscan |
| 渗透测试 | Metasploit、sqlmap、Burp Suite Pro |

### 加密算法选择

| 使用场景 | 算法 | 密钥长度 |
|----------|-----------|----------|
| 对称加密 | AES-256-GCM | 256位 |
| 密码哈希 | Argon2id | 不适用（使用默认设置） |
| 消息认证 | HMAC-SHA256 | 256位 |
| 数字签名 | Ed25519 | 256位 |
| 密钥交换 | X25519 | 256位 |
| TLS | TLS 1.3 | 不适用 |

更多信息请参阅：[references/cryptography-implementation.md]

---

## 工具与参考资料

### 脚本

| 脚本 | 用途 |
|--------|---------|
| [threat_modeler.py](scripts/threat_modeler.py) | 使用STRIDE方法进行威胁分析，并使用DREAD进行风险评分；输出格式为JSON和文本；提供交互式引导模式 |
| [secret_scanner.py](scripts/secret_scanner.py) | 检测20多种模式中的硬编码秘密和凭证；支持CI/CD集成 |

有关使用方法，请参阅[安全代码审查工作流程](#inline-code-examples)中的内联代码示例以及相应的脚本源文件。

### 参考资料

| 文档 | 内容 |
|----------|---------|
| [security-architecture-patterns.md](references/security-architecture-patterns.md) | 零信任原则、纵深防御、认证模式、API安全 |
| [threat-modeling-guide.md](references/threat-modeling-guide.md) | STRIDE方法、攻击树、DREAD评分、数据流图创建 |
| [cryptography-implementation.md](references/cryptography-implementation.md) | AES-GCM、RSA、Ed25519、密码哈希、密钥管理 |

---

## 安全标准参考

### 安全头部设置建议

| 头部字段 | 推荐值 |
|--------|-------------------|
| Content-Security-Policy | default-src self; script-src self |
| X-Frame-Options | DENY |
| X-Content-Type-Options | nosniff |
| Strict-Transport-Security | max-age=31536000; includeSubDomains |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | geolocation=(), microphone=(), camera=() |

有关合规性框架要求（OWASP ASVS、CIS Benchmarks、NIST CSF、PCI-DSS、HIPAA、SOC 2），请参阅相应的官方文档。

---

## 相关技能

| 技能 | 相关领域 |
|-------|-------------------|
| [高级DevOps](../senior-devops/) | 持续集成/持续交付（CI/CD）安全、基础设施加固 |
| [高级安全运维](../senior-secops/) | 安全监控、事件响应 |
| [高级后端开发](../senior-backend/) | 安全API开发 |
| [高级架构师](../senior-architect/) | 安全架构设计 |

---

---

（注：由于代码块内容较长，实际翻译中可能只包含每个部分的开头和结尾部分。完整的代码示例和详细说明通常会放在单独的代码块中。）