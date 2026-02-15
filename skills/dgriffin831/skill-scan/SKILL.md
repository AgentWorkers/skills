---
name: skill-scan
description: OpenClaw 技能包的安全扫描工具。在安装之前，该工具会检测技能包中是否存在恶意代码、规避机制、提示注入（prompt injection）以及异常行为。适用于审计来自 ClawHub 或本地目录的任何技能包。
---

# Skill-Scan — 用于检查代理技能的安全审计工具

这是一个针对 OpenClaw 技能包的多层安全扫描工具。通过静态分析以及可选的基于大型语言模型 (LLM) 的深度检测，能够识别恶意代码、规避技术、提示注入以及行为异常。在安装或启用任何未经信任的技能之前，请务必运行此工具。

## 主要功能

- **6 层分析机制**：模式匹配、抽象语法树 (AST) 分析、规避行为检测、提示注入检测、基于 LLM 的深度分析、行为一致性验证、元数据分析
- **60 多条检测规则**：执行威胁、凭证窃取、数据泄露、代码混淆、行为特征识别
- **上下文感知的评分系统**：有效降低对合法 API 技能的误报率
- **集成 ClawHub**：可通过技能的唯一标识符（slug）直接从 ClawHub 扫描技能
- **多种输出格式**：文本报告（默认）、`--json`、`--compact`、`--quiet`
- **退出代码**：0 表示安全；1 表示存在风险（便于脚本集成）

## 使用场景

**强制要求**：在安装或启用以下技能之前必须使用：
- 来自 ClawHub 的技能（非用户自行编写的技能）
- 其他用户或团队共享的技能
- 来自公共仓库的技能
- 未经过用户亲自审核的技能包

**建议**：定期对已安装的技能进行安全审计。

## 快速入门

```bash
# Scan a local skill directory
skill-scan scan /path/to/skill

# Scan a skill from ClawHub before installing it
skill-scan scan-hub some-skill-slug

# Batch scan all installed skills
skill-scan batch /path/to/skills-directory

# JSON output for programmatic use
skill-scan scan-hub some-skill-slug --json

# Quiet mode (just score + verdict)
skill-scan scan-hub some-skill-slug --quiet
```

## 风险评分

| 风险等级 | 评分 | 应对措施 |
|------|-------|--------|
| 低风险 | 80-100 | 可以安全安装 |
| 中等风险 | 50-79 | 安装前请查看检测结果 |
| 高风险 | 20-49 | 请勿安装——检测到严重威胁 |
| 极高风险 | 0-19 | 请勿安装——存在多个致命威胁 |

## 退出代码

- `0`：低风险（可安全安装）
- `1`：中等风险或更高风险（阻止安装）

## 基于 LLM 的配置选项

```bash
skill-scan scan-hub slug --llm        # Always run deep analysis (layers 4-5)
skill-scan scan-hub slug --llm-auto   # LLM only if pattern scan finds MEDIUM+
skill-scan scan-hub slug --llm-only   # Skip patterns, LLM analysis only
```

系统会自动检测并设置 LLM 服务提供商：
- `OPENAI_API_KEY` -> `gpt-4o-mini`
- `ANTHROPIC_API_KEY` -> `claude-sonnet-4-5`

## 对于代理的使用

当用户请求从 ClawHub 安装技能时，请按照以下流程操作：

1. **先进行扫描**：在安装前运行 `skill-scan scan-hub <slug>`
2. **查看扫描结果**：
   - 如果风险等级为低风险（退出代码为 0）：继续安装
   - 如果风险等级为中等风险：向用户展示检测结果并询问是否继续安装
   - 如果风险等级为高风险或极高风险：阻止安装并展示扫描报告
3. **提供报告**：始终向用户展示扫描摘要（评分、风险等级、检测结果数量）

### 警报格式

当扫描发现中等风险或更高风险时，系统会生成如下格式的警报：

```
🛡️ Skill-Scan Alert: {RISK_LEVEL} ({SCORE}/100)
Skill: {slug}
Findings: {count} issue(s) detected
Top threat: {highest severity finding title}
Action: Installation blocked pending review.
```

## 如何将 Skill-Scan 集成到代理的工作流程中

要将 Skill-Scan 集成到代理的工作流程中，请在 `AGENTS.md`（或相应的代理配置文件）中添加以下模板之一。

### 选项 A：自动扫描（推荐）

所有来自 ClawHub 的技能在安装前都会自动进行扫描，无需手动操作。

```markdown
## Skill-Scan — Automatic Pre-Install Security Scanning

BEFORE installing any skill from ClawHub, you MUST scan it with skill-scan first. This is non-negotiable — never skip the scan.

### Workflow

1. When the user asks to install a skill (e.g. `clawhub install <slug>`), run the scan FIRST:
   ```bash
   skill-scan scan-hub <slug>
   ```
2. **Check the exit code and output**:
   - **Exit code 0 (LOW risk)** — proceed with `clawhub install <slug>`
   - **Exit code 1 (MEDIUM risk)** — show findings to the user, ask whether to proceed
   - **Exit code 1 (HIGH/CRITICAL risk)** — BLOCK installation, show the full report
3. **Never install a HIGH or CRITICAL risk skill** without explicit user override
4. **Always show the scan summary** to the user before proceeding with installation

### Periodic Audits

When asked to audit installed skills, batch scan the skills directory:
```bash
   skill-scan batch {skillsDir}
```

### LLM Deep Analysis

For high-stakes installs or when pattern scan returns MEDIUM, escalate to LLM analysis:
```bash
skill-scan scan-hub <slug> --llm-auto
```
```

### 选项 B：手动按需扫描

只有当用户明确请求时才会进行扫描。安装过程不会自动触发扫描。

```markdown
## Skill-Scan — On-Demand Skill Security Scanning

skill-scan is available to audit skill packages for security threats. Use it when the user requests a security scan.

### Commands

- **Scan a ClawHub skill**: `skill-scan scan-hub <slug>`
- **Scan a local skill**: `skill-scan scan /path/to/skill`
- **Batch scan installed skills**: `skill-scan batch {skillsDir}`
- **Deep analysis with LLM**: add `--llm` or `--llm-auto` to any scan command

### Risk Levels

- **LOW (80-100)** — safe, no significant threats
- **MEDIUM (50-79)** — review findings, use caution
- **HIGH (20-49)** — serious threats, do not install
- **CRITICAL (0-19)** — multiple critical threats, do not install

### When the User Asks to Scan

1. Run the appropriate scan command
2. Show the scan summary (score, risk level, finding count)
3. If MEDIUM+, list the top findings with severity and description
4. Let the user decide what to do
```

## 安装时的配置提示

在首次安装该工具时，询问用户：
> “您希望如何将 Skill-Scan 集成到您的工作流程中？”
>
> 1. **自动扫描**（推荐）：每次从 ClawHub 安装技能时都会自动进行扫描。高风险或极高风险技能会自动被阻止。
> 2. **手动扫描**：仅在使用时才进行扫描。

根据用户的选择，在项目的 `AGENTS.md` 中添加相应的配置模板（选项 A 或选项 B）。

## 检测类别

- **执行威胁**：`eval()`、`exec()`、`child_process`、动态导入函数
- **凭证窃取**：`.env` 文件访问、API 密钥、令牌、私钥、钱包文件
- **数据泄露**：`fetch()`、`axios`、`requests`、套接字、Webhook 功能
- **文件系统操作**：写入/删除/重命名文件
- **代码混淆**：Base64 编码、十六进制编码、Unicode 编码、字符串构造
- **提示注入**：越狱技巧、不可见字符、同形异义字、伪装请求
- **行为特征**：数据泄露、木马程序、隐蔽后门

## 系统要求

- Python 3.10 及以上版本
- `httpx` 库版本需大于或等于 0.27（仅用于调用 LLM API）
- 仅在使用 `--llm` 模式时需要 API 密钥（静态分析功能无需额外配置）

## 相关工具

- **input-guard**：外部输入安全检查工具
- **memory-scan**：代理内存安全检测工具
- **guardrails**：安全策略配置工具