---
name: ralph-promax
description: "**最高级别的安全审计（Maximum Paranoia Security Audit）**：  
该审计流程包含10,000次迭代（耗时约2-5天），由8位专家团队共同执行。适用于用户提出以下要求时：  
- “ralph promax”  
- “maximum security audit”  
- “full paranoia audit”  
- “exhaustive security review”  
- “security incident deep investigation”  
- “maximum paranoia mode”  
该审计涵盖以下关键领域：  
- OWASP（Open Web Application Security Project）安全标准  
- 供应链安全  
- API（应用程序编程接口）安全  
- 容器安全  
- 持续集成/持续交付（CI/CD）流程的安全性  
- 系统性能优化  
- 人工智能/风险评估（AI/Risk Assessment）  
- 合规性检查（Compliance）  
通过这种极其细致的安全审计方法，可以全面评估系统的安全性，确保所有潜在风险都被有效识别和解决。"
metadata: { "openclaw": { "emoji": "☠️" }, "author": "dorukardahan", "version": "2.0.0", "category": "security", "tags": ["security", "audit", "exhaustive", "paranoia", "owasp", "supply-chain", "compliance"] }
---
# Ralph Promax — 10,000次迭代（约2-5天）

这是最全面的安全审计流程。由8位专家参与，分为16个阶段，确保没有遗漏任何细节。

> **主机安全警告：**Ralph Promax会执行系统级别的侦察操作（如进程列表检查、端口扫描、文件权限验证），并使用您的用户权限运行。请勿在生产服务器上使用该工具，除非您完全了解其可能带来的影响。

相关资源请查阅以下路径：
- 安全性评估与分类指南：`{baseDir}/references/severity-guide.md`
- 所有专家角色介绍：`{baseDir}/references/personas.md`
- OWASP攻击模式与检查清单：`{baseDir}/references/attack-patterns.md`
- 各阶段详细信息：`{baseDir}/references/phase-details.md`

## 指令说明

### 执行流程

每次迭代都必须严格遵循以下步骤，无一例外：
1. **状态检查**：读取当前迭代次数（起始值为1）。
2. **确定阶段**：根据迭代次数判断当前所处的阶段。
3. **激活专家角色**：根据需要激活相应的专家角色。
4. **执行深度检查**：以最高标准进行彻底的审计。
5. **执行检查**：针对每个阶段执行一项详细的检查。
6. **验证结果**：在发现漏洞之前，务必仔细阅读代码、检查相关库和数据库配置、环境设置；如果结果不明确，则标记为“需要进一步审查”。
7. **尝试利用漏洞**：如果发现漏洞，尝试利用该漏洞进行攻击。
8. **生成报告**：输出当前迭代的审计结果及漏洞利用示例（PoC）。
9. **保存进度**：每进行100次迭代，更新`ralph-report.md`文件。
10. **递增迭代次数**：将迭代次数加1。
11. **继续审计**：如果迭代次数小于或等于10,000次，则返回步骤1。
12. **生成最终报告**：完成所有迭代后，生成一份全面的审计报告。

**重要规则：**
- 每次迭代仅执行一项检查，注重深度而非广度。
- 必须在报告中显示“[PROMAX-X/10000]”的标识。
- 严禁跳过任何迭代步骤。
- 发现严重漏洞时，立即停止审计并请求立即处理。
- 对于每次检查，都需要由红队专家进行评估。
- 对于复杂的漏洞情况，必须调动所有8位专家的角色共同参与分析。

### 每次迭代的输出内容（见````
╔════════════════════════════════════════════════════════════════════════╗
║ [PROMAX-{N}/10000] Phase {P}: {phase_name}                            ║
║ Mind: {active_expert_persona}                                          ║
║ Depth Level: ████████████ MAXIMUM                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║ Check: {specific_check}                                                ║
║ Target: {file:line / endpoint / system / dependency}                   ║
╠════════════════════════════════════════════════════════════════════════╣
║ Red Team Question: "{attack scenario being tested}"                    ║
╠════════════════════════════════════════════════════════════════════════╣
║ Result: {PASS|FAIL|WARN|SUSPICIOUS|N/A}                                ║
║ Confidence: {VERIFIED|LIKELY|PATTERN_MATCH|NEEDS_REVIEW}               ║
║ Severity: {CRITICAL|HIGH|MEDIUM|LOW|INFO}                              ║
║ CVSS: {score} | Exploitability: {TRIVIAL|MODERATE|DIFFICULT}           ║
╠════════════════════════════════════════════════════════════════════════╣
║ Finding: {detailed description}                                        ║
║ Attack Vector: {how an attacker would exploit}                         ║
║ Proof of Concept: {actual exploit code/steps or "N/A"}                 ║
║ Blast Radius: {what gets compromised}                                  ║
║ Fix: {specific remediation with code}                                  ║
╠════════════════════════════════════════════════════════════════════════╣
║ Progress: [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] {N/100}%          ║
║ Phase: {current}/{16} | ETA: ~{days}d {hours}h                          ║
╚════════════════════════════════════════════════════════════════════════╝
````）

### 八位专家角色

| 阶段 | 负责专家角色 |
|-------|-------------|
| 1     | 网络安全资深专家 + CI/CD破坏者 |
| 2     | 代码审计员（渗透测试人员） |
| 3     | 网络安全资深专家 |
| 4     | 容器安全专家 |
| 5     | 代码审计员 |
| 6     | 依赖关系分析专家 |
| 7     | API安全专家 |
| 8     | 容器安全专家 |
| 9     | CI/CD破坏者 |
| 10     | 性能工程师 |
| 11     | RAG系统架构师 |
| 12     | 网络安全资深专家 |
| 13-16   | 所有8位专家同时参与 |

### 核心审计理念：
1. **深度防御**：单一控制措施等于零控制效果。
2. **安全第一**：在不确定的情况下，采取拒绝访问的措施。
3. **最小权限原则**：任何权限都可能被利用为攻击途径。
4. **一切皆需验证**：对所有系统组件进行彻底检查。
5. **假设已遭入侵**：始终假定攻击者已经渗透系统。
6. **彻底性是生存的关键**：只有彻底的审计才能确保系统的安全。

### 阶段划分（共10,000次迭代）

| 阶段 | 迭代次数 | 主要审计内容 |
|-------|------------|------------|
| 1     | 1-500     | 侦察与攻击面分析 |
| 2     | 501-1,200     | OWASP十大常见漏洞的深入排查 |
| 3     | 1,201-2,000    | 认证与密钥管理 |
| 4     | 2,001-2,800    | 基础设施与网络架构 |
| 5     | 2,801-3,600    | 代码质量与业务逻辑 |
| 6     | 3,601-4,400    | 供应链与依赖关系管理 |
| 7     | 4,401-5,200    | API安全 |
| 8     | 5,201-6,000    | 容器与Docker安全 |
| 9     | 6,001-6,800    | CI/CD流程安全 |
| 10     | 6,801-7,600    | 系统性能与抗DDoS能力 |
| 11     | 7,601-8,400    | 人工智能与RAG系统安全 |
| 12     | 8,401-9,000    | 合规性与隐私保护 |
| 13     | 9,001-9,400    | 跨领域攻击链分析 |
| 14     | 9,401-9,700    | 渗透测试模拟 |
| 15     | 9,701-9,900    | 最终验证 |
| 16     | 9,901-10,000   | 审计报告与总结 |

有关各阶段的详细信息、检查清单和攻击用例，请参阅`{baseDir}/references/phase-details.md`和`{baseDir}/references/attack-patterns.md`。

### 自动检测流程（第一次迭代）

1. 使用`git rev-parse --show-toplevel`和`git remote -v`获取项目信息。
2. 分析项目配置文件：`package.json`、`pyproject.toml`、`requirements.txt`、`go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle`、`composer.json`。
3. 检查基础设施相关文件：`Dockerfile`、`docker-compose.yml`、`k8s`配置文件、`serverless`设置。
4. 列出所有容器及Kubernetes服务。
5. 检查CI/CD流程：`.github/workflows`、`.gitlab-ci.yml`、`.circleci`配置文件。
6. 获取生产环境的URL：`env/config/docs/ingress`。
7. 查看部署相关配置：SSH配置文件及部署脚本。

### 报告文件

启动审计时，会重命名现有的报告文件；每进行100次迭代，会自动保存审计结果。

### 配置参数

| 参数 | 默认值 | 可选值 |
|-------|---------|---------|
| `--iterations` | 10000 | 1-20000 |
| `--focus` | all   | 全部阶段 | recon、owasp、auth、infra、code、supply-chain、api、docker、cicd、perf、rag、compliance |
| `--phase` | all   | 1-16    | 所有阶段 |
| `--paranoia` | maximum | standard | high | maximum |
| `--resume` | —     | 从上次检查点继续审计 |

### 进度保存与恢复机制

- 审计过程中会立即将当前进度保存到报告文件中。
- 输出格式：`AUDIT CHECKPOINT at iteration {N}. Resume with: /ralph-promax --resume`
- 报告内容包括：审计发现总结及下一阶段的审计内容。
- 系统会等待用户输入新的命令以继续审计。

### 使用场景：
- 用于安全事件调查。
- 用于合规性审计准备。
- 在使用`/ralph-ultra`工具发现可疑异常时启用最高级别的审计模式。