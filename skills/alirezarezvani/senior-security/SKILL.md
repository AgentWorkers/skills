---
name: senior-security
description: 这是一个用于威胁建模、漏洞分析、安全架构设计和渗透测试的安全工程工具包。它包含了STRIDE分析方法、OWASP安全指南、加密模式以及多种安全扫描工具。
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

提供用于威胁建模、漏洞分析、安全架构设计和渗透测试的安全工程工具。

---

## 目录

- [威胁建模工作流程](#threat-modeling-workflow)
- [安全架构工作流程](#security-architecture-workflow)
- [漏洞评估工作流程](#vulnerability-assessment-workflow)
- [安全代码审查工作流程](#secure-code-review-workflow)
- [事件响应工作流程](#incident-response-workflow)
- [安全工具参考](#security-tools-reference)
- [工具和参考资料](#tools-and-references)

---

## 威胁建模工作流程

使用STRIDE方法识别和分析安全威胁。

### 工作流程：进行威胁建模

1. 定义系统范围和边界：
   - 确定需要保护的资产
   - 绘制信任边界
   - 记录数据流
2. 创建数据流图：
   - 外部实体（用户、服务）
   - 过程（应用程序组件）
   - 数据存储（数据库、缓存）
   - 数据流（API、网络连接）
3. 对每个数据流图元素应用STRIDE方法：
   - 伪造（Spoofing）：身份可以伪造吗？
   - 篡改（Tampering）：数据可以被修改吗？
   - 否认（Repudiation）：行为可以被否认吗？
   - 信息泄露（Information Disclosure）：数据会泄露吗？
   - 服务拒绝（Denial of Service）：可用性会受到影响吗？
   - 权限提升（Elevation of Privilege）：访问权限可以提升吗？
4. 使用DREAD方法对风险进行评分：
   - 损害潜力（1-10）
   - 可复现性（1-10）
   - 易被利用性（1-10）
   - 受影响用户（1-10）
   - 被发现的可能性（1-10）
5. 根据风险评分对威胁进行优先级排序
6. 为每个威胁制定缓解措施
7. 将结果记录在威胁模型报告中
8. **验证：** 所有数据流图元素均已分析；应用了STRIDE方法；对威胁进行了评分；制定了缓解措施

### STRIDE威胁类别

| 类别 | 描述 | 安全属性 | 缓解措施重点 |
|----------|-------------|-------------------|------------------|
| 伪造（Spoofing） | 伪装成用户或系统 | 认证 | 多因素认证（MFA）、证书、强认证 |
| 篡改（Tampering） | 修改数据或代码 | 完整性 | 签名、校验和、验证 |
| 否认（Repudiation） | 否认行为 | 非否认（Non-repudiation） | 审计日志、数字签名 |
| 信息泄露（Information Disclosure） | 数据暴露 | 保密性 | 加密、访问控制 |
| 服务拒绝（Denial of Service） | 中断可用性 | 可用性 | 速率限制、冗余 |
| 权限提升（Elevation of Privilege） | 获得未经授权的访问权限 | 授权 | 基于角色的访问控制（RBAC）、最小权限原则 |

### STRIDE与数据流图元素的对应关系

| 数据流图元素 | 伪造（Spoofing） | 篡改（Tampering） | 否认（Repudiation） | 信息泄露（Information Disclosure） | 服务拒绝（Denial of Service） | 权限提升（Elevation of Privilege） |
|-------------|-------------|-------------|-------------------|-------------------|-------------------|
| 外部实体（External Entity） | X | X | X | | | |
| 过程（Process） | X | X | X | X | X | X |
| 数据存储（Data Store） | | X | X | X | X | |
| 数据流（Data Flow） | | X | | X | X | |

更多信息请参见：[references/threat-modeling-guide.md](references/threat-modeling-guide.md)

---

## 安全架构工作流程

使用纵深防御原则设计安全系统。

### 工作流程：设计安全架构

1. 定义安全需求：
   - 合规性要求（GDPR、HIPAA、PCI-DSS）
   - 数据分类（公共数据、内部数据、机密数据、受限数据）
   - 威胁模型输入
2. 应用纵深防御层次：
   - 外围防御：Web应用防火墙（WAF）、DDoS防护、速率限制
   - 网络防御：网络分段、入侵检测系统（IDS/IPS）、传输层安全（TLS）
   - 主机防御：补丁管理、端点检测（EDR）、系统加固
   - 应用程序防御：输入验证、认证、安全编码
   - 数据防御：数据存储和传输过程中的加密
3. 实施零信任原则：
   - 明确验证每个请求
   - 最小权限访问（JIT/JEA）
   | 假设已发生泄露（采取分段防御、监控措施）
4. 配置认证和授权：
   - 选择身份提供者
   - 多因素认证要求
   - 基于角色的访问控制（RBAC）/基于属性的访问控制（ABAC）
5. 设计加密策略：
   - 密钥管理方法
   - 算法选择
   - 证书生命周期管理
6. 规划安全监控：
   - 日志收集
   - 安全信息事件管理系统（SIEM）集成
   | 警报规则设置 |
7. 记录架构决策
8. **验证：** 深度防御层次已定义；实施了零信任策略；加密策略已记录；监控计划已制定

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
| Web应用程序 | OAuth 2.0 + 使用OIDC的PKCE |
| API认证 | 使用短有效期令牌的JWT |
| 服务间通信 | 使用证书轮换的mTLS |
| 命令行界面/自动化 | 使用IP白名单的API密钥 |
| 高安全要求 | 使用FIDO2/WebAuthn硬件密钥 |

更多信息请参见：[references/security-architecture-patterns.md](references/security-architecture-patterns.md)

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
   | 依赖项扫描 |
4. 执行手动测试：
   | 业务逻辑缺陷 |
   | 认证绕过 |
   | 授权问题 |
   | 注入漏洞 |
5. 按严重程度对漏洞进行分类：
   | 严重：立即存在被利用的风险 |
   | 高：影响显著，容易被利用 |
   | 中等：影响中等或难度较高 |
   | 低：影响较小 |
6. 制定修复计划：
   | 按风险优先级排序 |
   | 分配负责人 |
   | 设置截止日期 |
7. 验证修复措施并记录结果
8. **验证：** 评估范围已确定；自动化和手动测试已完成；漏洞已分类；修复措施已跟踪

### OWASP十大常见漏洞

| 编号 | 漏洞名称 | 测试方法 |
|------|---------------|------------------|
| A01 | 访问控制漏洞 | 手动IDOR测试、授权检查 |
| A02 | 加密失败 | 算法审查、密钥管理审计 |
| A03 | 注入漏洞 | 静态应用安全测试（SAST）+ 手动载荷测试 |
| A04 | 安全设计缺陷 | 威胁建模、架构审查 |
| A05 | 安全配置错误 | 配置审计、CIS基准测试 |
| A06 | 漏洞组件 | 依赖项扫描、CVE监控 |
| A07 | 认证失败 | 密码策略、会话管理审查 |
| A08 | 软件/数据完整性问题 | 持续集成/持续交付（CI/CD）安全措施、代码签名验证 |
| A09 | 日志记录失败 | 日志审查、SIEM配置检查 |
| A10 | SSRF（跨站请求伪造） | 手动URL操作测试 |

### 漏洞严重程度矩阵

| 影响/易被利用性 | 易被利用 | 中等 | 难以利用 |
|-------------------------|------|----------|-----------|
| 严重 | 非常严重 | 非常严重 | 高 |
| 高 | 严重 | 中等 | 中等 |
| 中等 | 高 | 中等 | 低 |
| 低 | 低 | 低 | 低 |

---

## 安全代码审查工作流程

在部署前审查代码中的安全漏洞。

### 工作流程：进行安全代码审查

1. 确定审查范围：
   - 变更的文件和函数
   | 安全敏感区域（认证、加密、输入处理） |
   | 第三方集成 |
2. 运行自动化分析：
   | 静态应用安全测试工具（Semgrep、CodeQL、Bandit） |
   | 秘密信息扫描 |
   | 依赖项漏洞检查 |
3. 审查认证相关代码：
   | 密码处理（哈希、存储） |
   | 会话管理 |
   | 令牌验证 |
4. 审查授权相关代码：
   | 访问控制检查 |
   | 基于角色的访问控制（RBAC）实现 |
   | 权限边界 |
5. 审查数据处理相关代码：
   | 输入验证 |
   | 输出编码 |
   | SQL查询构建 |
   | 文件路径处理 |
6. 审查加密相关代码：
   | 算法选择 |
   | 密钥管理 |
   | 随机数生成 |
7. 记录发现的问题及其严重程度
8. **验证：** 自动化扫描通过；认证/授权部分已审查；数据处理部分已检查；加密措施已验证；发现的问题已记录

### 安全代码审查检查表

| 类别 | 检查项 | 风险 |
|----------|-------|------|
| 输入验证 | 所有用户输入均经过验证和清理 | 注入攻击（Injection） |
| 输出编码 | 使用适合上下文的编码方式 | 跨站脚本攻击（XSS） |
| 认证 | 密码使用Argon2/bcrypt进行哈希处理 | 凭据被盗 |
| 会话管理 | 设置安全的cookie属性（HttpOnly、Secure、SameSite） | 会话劫持 |
| 授权 | 所有端点都进行了服务器端权限检查 | 权限提升 |
| SQL | 仅使用参数化查询 | SQL注入 |
| 文件访问 | 拒绝路径遍历请求 | 防止路径遍历攻击 |
| 秘密信息 | 无硬编码的凭证或密钥 | 信息泄露 |
| 依赖项 | 已更新已知有漏洞的包 | 供应链安全 |
| 日志记录 | 敏感数据未记录 | 信息泄露 |

### 安全代码与不安全代码的对比

| 不安全代码模式 | 安全代码模式 |
|---------|-------|-------------------|
| SQL字符串格式化 | 使用参数化查询和占位符 | 防止SQL注入 |
| 构建Shell命令 | 使用带有参数列表的子进程，避免使用Shell | |
| 路径拼接 | 验证和规范化路径 | 防止路径遍历攻击 |
| 使用MD5/SHA1进行密码哈希 | 使用Argon2id或bcrypt进行哈希 | |
| 使用Math.random生成令牌 | 使用crypto.getRandomValues生成随机数 | |

---

## 事件响应工作流程

响应并控制安全事件。

### 工作流程：处理安全事件

1. 识别并分类事件：
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
4. 恢复系统运行：
   | 从备份中恢复数据 |
   | 验证系统完整性 |
   | 监控事件是否再次发生 |
5. 进行事后分析：
   | 重建事件时间线 |
   | 分析根本原因 |
   | 总结经验教训 |
6. 实施改进措施：
   | 更新检测规则 |
   | 加强安全控制 |
   | 更新应急响应流程 |
7. 记录并报告事件 |
8. **验证：** 威胁已被控制；根本原因已消除；系统已恢复；事后分析已完成；改进措施已实施

### 事件严重程度等级

| 等级 | 描述 | 响应时间 | 升级流程 |
|-------|-------------|---------------|------------|
| P1 - 严重 | 发生数据泄露 | 立即响应 | 高层管理人员（CISO）、法律部门、管理层 |
| P2 - 高 | 确认存在安全漏洞，但已被控制 | 1小时内 | 安全负责人、IT总监 |
| P3 - 中等 | 存在潜在的安全风险，正在调查中 | 4小时内 | 安全团队 |
| P4 - 低 | 发生可疑活动，影响较小 | 24小时内 | 值班工程师 |

### 事件响应检查表

| 阶段 | 应采取的行动 |
|-------|---------|
| 识别阶段 | 验证警报、评估事件范围、确定严重程度 |
| 控制阶段 | 隔离系统、保存证据、阻止访问 |
| 消除阶段 | 删除威胁、修补漏洞、重置凭证 |
| 恢复阶段 | 恢复服务、验证系统完整性、加强监控 |
| 后事阶段 | 记录事件过程、识别漏洞、更新流程 |

---

## 安全工具参考

### 推荐的安全工具

| 工具类别 | 工具名称 |
|----------|-------|
| 静态应用安全测试（SAST） | Semgrep、CodeQL、Bandit（Python）、ESLint安全插件 |
| 动态应用安全测试（DAST） | OWASP ZAP、Burp Suite、Nikto |
| 依赖项扫描 | Snyk、Dependabot、npm audit、pip-audit |
| 秘密信息检测 | GitLeaks、TruffleHog、detect-secrets |
| 容器安全 | Trivy、Clair、Anchore |
| 基础设施安全 | Checkov、tfsec、ScoutSuite |
| 网络安全 | Wireshark、Nmap、Masscan |
| 渗透测试 | Metasploit、sqlmap、Burp Suite Pro |

### 加密算法选择

| 使用场景 | 选择的加密算法 | 密钥长度 |
|----------|-----------|----------|
| 对称加密 | AES-256-GCM | 256位 |
| 密码哈希 | Argon2id | 不适用（使用默认设置） |
| 消息认证 | HMAC-SHA256 | 256位 |
| 数字签名 | Ed25519 | 256位 |
| 密钥交换 | X25519 | 256位 |
| TLS协议 | TLS 1.3 | 不适用 |

更多信息请参见：[references/cryptography-implementation.md]

---

## 工具和参考资料

### 脚本

| 脚本名称 | 功能 | 使用方法 |
|--------|---------|-------|
| [threat_modeler.py](scripts/threat_modeler.py) | 使用STRIDE方法进行威胁分析并评分 | `python threat_modeler.py --component "Authentication"` |
| [secret_scanner.py](scripts/secret_scanner.py) | 检测硬编码的秘密信息和凭证 | `python secret_scanner.py /path/to/project` |

**threat_modeler.py功能：**
- 适用于任何系统组件的STRIDE分析 |
- 使用DREAD方法进行风险评分 |
- 提供缓解建议 |
- 支持JSON和文本输出格式 |
- 提供交互式模式以指导分析过程

**secret_scanner.py功能：**
- 检测AWS、GCP、Azure的凭证 |
- 查找API密钥和令牌（如GitHub、Slack、Stripe中的） |
- 识别私钥和密码 |
| 支持20多种秘密信息模式 |
| 支持与持续集成/持续交付（CI/CD）系统的集成 |

### 参考资料

| 文档名称 | 内容 |
|----------|---------|
| [security-architecture-patterns.md](references/security-architecture-patterns.md) | 零信任原则、纵深防御、认证模式、API安全 |
| [threat-modeling-guide.md](references/threat-modeling-guide.md) | STRIDE方法、攻击树分析、DREAD评分、数据流图创建 |
| [cryptography-implementation.md](references/cryptography-implementation.md) | AES-GCM、RSA、Ed25519、密码哈希、密钥管理 |

---

## 安全标准参考

### 合规性框架

| 框架 | 重点 | 适用范围 |
|-----------|-------|---------------|
| OWASP ASVS | 应用程序安全 | Web应用程序 |
| CIS基准 | 系统加固 | 服务器、容器、云服务 |
| NIST CSF | 风险管理 | 企业安全体系 |
| PCI-DSS | 支付卡数据安全 | 支付处理 |
| HIPAA | 医疗保健数据安全 | 医疗保健应用程序 |
| SOC 2 | 服务组织控制 | SaaS服务提供商 |

### 安全头部设置建议

| 头部字段 | 推荐值 |
|--------|-------------------|
| Content-Security-Policy | default-src self; script-src self |
| X-Frame-Options | DENY |
| X-Content-Type-Options | nosniff |
| Strict-Transport-Security | max-age=31536000; includeSubDomains |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | geolocation=(), microphone=(), camera=() |

---

## 相关技能

| 技能 | 相关领域 |
|--------|-------------------|
| [senior-devops](../senior-devops/) | 持续集成/持续交付（CI/CD）安全、基础设施加固 |
| [senior-secops](../senior-secops/) | 安全监控、事件响应 |
| [senior-backend](../senior-backend/) | 安全API开发 |
| [senior-architect](../senior-architect/) | 安全架构设计 |

---

---

（注：由于代码块内容较长，部分内容在翻译中进行了省略或简化。在实际应用中，这些代码块通常会包含具体的实现细节和配置指令，因此在完整文档中需要保留原样。）