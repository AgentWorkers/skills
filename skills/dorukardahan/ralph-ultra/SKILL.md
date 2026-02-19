---
name: ralph-ultra
description: "**深度安全审计（包含1,000次迭代，耗时约4-8小时）**  
适用于以下场景：用户要求进行“深度安全审计”、“Ralph Ultra级安全评估”、“合规性审计准备”、“全面的安全审查”、“重大版本发布前”或“安全事件调查”。  
审计内容包括OWASP安全标准、供应链安全、业务逻辑审查，以及由4位专家团队共同参与的分析过程。"
metadata: { "openclaw": { "emoji": "⚔️" }, "author": "dorukardahan", "version": "2.0.0", "category": "security", "tags": ["security", "audit", "deep-dive", "compliance", "owasp"] }
---
# Ralph Ultra — 1000次迭代（约4-8小时）

这是一项全面的安全审计任务，覆盖了所有可能的攻击途径。

关于严重性/优先级划分的指导，请参考：`{baseDir}/references/severity-guide.md`
关于专家角色的描述，请参考：`{baseDir}/references/personas.md`

## 指令

### 执行引擎

每次迭代都必须遵循以下步骤：

1. **状态（STATE）**：读取当前迭代次数（起始值为1）。
2. **阶段（PHASE）**：根据迭代次数确定当前所处的阶段。
3. **专家角色（MIND）**：为当前阶段激活相应的专家角色。
4. **操作（ACTION）**：执行当前阶段规定的检查项。
5. **验证（VERIFY）**：在发现问题之前，需要仔细阅读实际代码、检查相关库、数据库约束以及运行环境；如果结果不明确，则标记为“需要审核（NEEDS_REVIEW）”。
6. **报告（REPORT）**：输出本次迭代的审计结果。
7. **保存（SAVE）**：每50次迭代后，更新`.ralph-report.md`文件。
8. **迭代次数递增（INCREMENT）**：将迭代次数加1。
9. **继续（CONTINUE）**：如果迭代次数小于或等于1000次，则返回步骤1。
10. **最终阶段（FINAL）**：生成完整的审计报告。

**重要规则：**
- 每次迭代只执行一项检查，确保审计的深度而非广度。
- 必须在报告中显示 `[ULTRA-X/1000]` 标识。
- 严禁跳过任何迭代步骤。
- 对于严重的问题，必须立即标记并处理。
- 在执行所有检查时，都要采用红队（Red Team）的思维方式。

### 每次迭代的输出内容（见下方代码块）

### 专家角色

| 阶段（Phase） | 专家角色（Persona） |
|-------|---------|
| 1、3、7 | 网络安全资深专家（Cybersecurity Veteran） |
| 2、5 | 代码审计员（Pentester） |
| 4 | 容器安全专家（Container Security Expert） |
| 6 | 依赖关系检测专家（Dependency Hunter） |
| 8 | 全面审核专家（All Minds） |

完整的专家角色描述请参见：`{baseDir}/references/personas.md`。

### 阶段划分（共1000次迭代）

| 阶段（Phase） | 迭代次数（Iterations） | 重点检查领域（Focus Area） |
|-------|------------|------------|
| 1 | 1-100 | 侦察与攻击面（Reconnaissance & Attack Surface） |
| 2 | 101-250 | OWASP十大常见安全漏洞的深入排查（OWASP Top 10 Deep Dive） |
| 3 | 251-400 | 认证与密钥管理（Authentication & Secrets） |
| 4 | 401-550 | 基础设施与容器安全（Infrastructure & Containers） |
| 5 | 551-700 | 代码质量与业务逻辑（Code Quality & Business Logic） |
| 6 | 701-850 | 供应链与依赖关系管理（Supply Chain & Dependencies） |
| 7 | 851-950 | 合规性检查与文档管理（Compliance & Documentation） |
| 8 | 951-1000 | 最终验证与报告生成（Final Verification & Report） |

### 第1阶段：侦察（1-100次迭代）

- **1-20次迭代**：平台同步（Platform sync）——自动检测开发环境、同步Git仓库、验证文件哈希值、检查环境配置是否发生变化。
- **21-50次迭代**：攻击面分析（Attack Surface）——枚举所有可访问的端点、检查身份验证机制、设置速率限制、识别暴露的端口以及WebSocket/SSE相关问题。
- **51-75次迭代**：隐藏系统的检测（Hidden Systems）——查找未公开的服务、定时任务、过时的配置文件以及Docker网络设置。
- **76-100次迭代**：环境与文档检查（Environment & Docs）——审核环境变量、`.env`文件的内容、验证文档的准确性并给出评分。

### 第2阶段：OWASP十大常见安全漏洞（101-250次迭代）

| 迭代次数（Iter） | OWASP漏洞编号（OWASP） | 重点检查内容（Focus） |
|------|-------|-------|
| 101-120 | A01 | 访问控制漏洞（Access Control Vulnerabilities，如IDOR、CORS、路径遍历） |
| 121-140 | A02 | 加密算法缺陷（Cryptographic Failures） |
| 141-170 | 注入攻击（Injection Attacks，如SQL注入、命令注入、XSS、模板注入、日志注入） |
| 171-185 | 设计缺陷（Design Vulnerabilities） | 缺少必要的安全控制机制或业务逻辑错误 |
| 186-200 | 安全配置问题（Security Misconfigurations） | 如调试信息泄露、错误处理不当等 |
| 201-215 | 依赖库的安全问题（Vulnerable Components） | 依赖库中的安全漏洞 |
| 216-230 | 认证机制漏洞（Auth Failures） | 如凭证填充、会话管理问题 |
| 231-240 | 数据完整性问题（Integrity Failures） | 如数据反序列化过程中的安全漏洞 |
| 241-245 | 日志记录问题（Logging Failures） | 日志记录机制存在安全风险 |
| 246-250 | SSRF攻击（SSRF Attacks） | 通过跨站请求伪造（SSRF）进行攻击 |

### 第3阶段：认证与密钥管理（251-400次迭代）

在执行检查之前，先确定使用的是内置加密算法还是自定义加密方案。

- **251-300次迭代**：检测密钥和密码等敏感信息（Secret Detection）。
- **301-340次迭代**：JWT（JSON Web Tokens）的安全性检查（包括算法、声明内容、存储方式及撤销机制）。
- **341-365次迭代**：OAuth 2.0协议的实现（包括PKCE、重定向URI、状态管理及令牌交换）。
- **366-385次迭代**：管理员账户的认证机制（Admin Authentication） | 如暴力破解、时间限制、账户锁定等问题 |
- **386-400次迭代**：实施速率限制（Rate Limiting）以防止恶意请求。

### 第4阶段：基础设施安全（401-550次迭代）

- **401-450次迭代**：容器安全（Container Security）——检查非root用户权限、容器的只读设置及功能限制。
- **451-490次迭代**：网络安全性（Network Security）——检查端口配置、防火墙设置、网络隔离措施及出站流量控制。
- **491-515次迭代**：TLS/SSL协议的安全性（证书有效性、加密算法、HSTS配置）。
- **516-535次迭代**：SSH协议的安全性（密钥认证、配置强化）。
- **536-550次迭代**：数据库安全（Database Security）——检查SSL配置、权限设置及数据备份机制。

### 第5阶段：代码质量（551-700次迭代）

在执行检查之前，先确认数据库的约束条件是否正确。

- **551-590次迭代**：检测潜在的竞态条件（Race Conditions），如并发访问、锁机制等问题。
- **591-630次迭代**：业务逻辑的安全性（Business Logic）——检查业务流程是否存在漏洞或可被利用的逻辑缺陷。
- **631-660次迭代**：错误处理机制（Error Handling）——确保错误信息的安全性及系统的容错能力。
- **661-690次迭代**：资源管理（Resource Management）——检查资源分配和访问控制。
- **691-700次迭代**：防止DoS攻击（DoS Prevention）——评估系统对DoS攻击的防御能力。

### 第6阶段：供应链安全（701-850次迭代）

- **701-750次迭代**：依赖关系的审计（Dependency Audit）——检查是否存在CVE（Common Vulnerabilities and Exposures）或过时的依赖库。
- **751-790次迭代**：第三方API的安全性（Third-Party APIs）——检查API密钥、Webhook配置及速率限制。
- **791-820次迭代**：容器供应链的安全性（Container Supply Chain）——检查基础镜像的来源及签名验证。
- **821-850次迭代**：持续集成/持续交付（CI/CD）流程的安全性（CI/CD Security）——检查敏感信息的处理方式及权限设置。

### 第7阶段：合规性检查（851-950次迭代）

- **851-885次迭代**：隐私合规性（Privacy Compliance）——遵循GDPR等法规，检查数据保留政策及用户同意机制。
- **886-915次迭代**：安全文档的完整性（Security Documentation）——验证安全策略和事件响应流程。
- **916-935次迭代**：操作安全（Operational Security）——检查访问控制和变更管理机制。
- **936-950次迭代**：审计日志的完整性和保留策略（Audit Trail）。

### 第8阶段：最终验证（951-1000次迭代）

- **951-970次迭代**：重新验证所有关键发现。
- **971-985次迭代**：模拟渗透测试（Penetration Test Simulation）。
- **986-995次迭代**：生成安全报告卡（Security Scorecard）。
- **996-1000次迭代**：生成最终报告并进行总结。

### 自动检测步骤（第1次迭代）

- 执行命令：`git rev-parse --show-toplevel` 和 `git remote -v` 以获取仓库信息。
- 检查以下文件以确定开发环境：`package.json`、`pyproject.toml`、`requirements.txt`、`go.mod`、`Cargo.toml`。
- 检查基础设施相关文件：`Dockerfile`、`docker-compose.yml`、Kubernetes配置文件（k8s manifests）以及Terraform配置。
- 检查持续集成/持续交付（CI/CD）相关设置：`.github/workflows`、`.gitlab-ci.yml`、`.circleci`。

### 报告文件

- 启动审计时，需要重命名现有的报告文件。
- 每50次迭代后，自动保存审计结果。

### 参数设置

| 参数（Parameter） | 默认值（Default） | 可选值（Options） |
|-------|---------|---------|
| `--iterations` | 1000 | 可设置为1-2000次迭代 |
| `--focus` | `all` | 或指定具体阶段（如recon、owasp、auth、infra、code、supply-chain、compliance等） |
| `--phase` | `all` | 或指定具体阶段（1-8） |
| `--resume` | `--` | 从上次检查点继续执行 |

### 进度恢复机制

使用`.ralph-report.md`文件作为检查点，执行`resume`命令以恢复上次未完成的审计任务，并等待新的审计会话开始。

### 适用场景

- 在产品发布前进行安全审计。
- 在发生安全事件时进行调查。
- 在`/ralph-security`工具检测到问题后进行深入安全检查。