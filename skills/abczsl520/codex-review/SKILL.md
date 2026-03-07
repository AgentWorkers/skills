---
name: codex-review
version: 2.1.0
description: "三级代码质量防御体系：  
L1：快速扫描（用于初步检测潜在问题）；  
L2：深入审计（通过漏洞审计工具进行详细检查）；  
L3：对抗性测试（通过模拟攻击场景进行交叉验证）。"
metadata:
  { "openclaw": { "emoji": "🔍" } }
tags:
  - code-review
  - quality-assurance
  - bug-detection
  - security-audit
  - cross-validation
  - ai-code-review
  - nodejs
  - openclaw-skill
  - clawhub
  - devops
---
# Codex Review — 三层代码质量防御体系

## 统一协调层：根据触发语句选择审核深度  
`bug-audit` 作为一个独立的工具被调用，且其代码从未被修改过。

## 安全与隐私  
- **默认为只读模式**：该工具仅用于读取项目文件进行分析，不会修改、删除或上传任何代码。  
- **可选的外部模型**：L1/L3 级别可以使用兼容 OpenAI 的外部代码审查 API 进行二次审核。此功能为可选配置；如果未配置 API 密钥，系统将仅使用内置的审核机制。  
- **凭证仅通过环境变量传递**：API 密钥从 `CODEX_REVIEW_API_KEY` 环境变量中加载，严禁硬编码或存储。  
- **结果仅存储在本地临时目录**：分析结果会写入系统临时目录，并在完成后自动清除，不会通过网络传输。  
- **防止数据泄露**：发送给外部 API 的代码片段仅限于被审查的文件内容，不会包含任何额外的数据（如遥测信息或第三方数据）。  

## 先决条件  
- **外部模型 API**（L1 和 L3 级别可选）：任何兼容 OpenAI 的 API 端点。  
  - 需设置环境变量：`CODEX_REVIEW_API_BASE`（默认：`https://api.openai.com/v1`）、`CODEX_REVIEW_API_KEY`、`CODEX_REVIEW_MODEL`（默认：`gpt-4o`）  
  - 未配置 API 时，系统将使用内置的审核机制。  
- **`bug-audit` 工具**（L2 和 L3 级别必需）：缺少该工具时，L2 级别会使用内置的备用方案。  
- **curl**：用于 API 调用（macOS/Linux 系统默认支持）。  

## 触发语句与对应操作  
| 用户指令 | 级别 | 功能 | 预计耗时 |  
|-----------|-------|--------------|-----------|  
| "review" / "quick scan" / "检查下" | L1 | 使用外部模型进行扫描 + 内置工具进行深度检查 | 5–10 分钟 |  
| "audit" / "深度审计" / "审计下" | L2 | 执行完整的 bug-audit 流程 | 30–60 分钟 |  
| "pre-deploy check" | L1 → L2 | 先使用 L1 进行扫描，记录问题点，再由 L2 进行审计 | 40–70 分钟 |  
| "cross-validate" | L3 | 进行双重独立审核并对比结果 | 60–90 分钟 |  

---

## 第 1 级：快速扫描（Codex Review 的核心功能）  
### 流程  
1. **收集代码**：从本地读取代码、通过 `git clone <url>` 下载代码、用户粘贴的代码片段或 PR 的差异文件。  
2. **排除文件**：排除 `node_modules`、`.git`、`package-lock.json`、`dist`、`*.db`、`__pycache__` 和 `vendor` 目录下的文件。  
3. **第 1 轮**：将代码发送到外部模型 API 进行自动化扫描（若未配置 API 密钥，则跳过此步骤）。  
4. **第 2 轮**：由内置代理执行深度检查。  
5. **合并结果并去重**：生成按严重程度分级的报告。  
6. **生成热点文件**（用于 L1 级别与 L2 级别的结果传递）。  

### 外部模型 API 调用  
```bash
curl -s "${CODEX_REVIEW_API_BASE:-https://api.openai.com/v1}/chat/completions" \
  -H "Authorization: Bearer ${CODEX_REVIEW_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "${CODEX_REVIEW_MODEL:-gpt-4o}",
    "messages": [
      {"role": "system", "content": "<REVIEW_SYSTEM_PROMPT>"},
      {"role": "user", "content": "<code content>"}
    ],
    "temperature": 0.2,
    "max_tokens": 6000
  }'
```  

**备用方案**：如果 API 调用失败或超时（120 秒），则跳过第 1 轮，直接使用内置的代理进行审核。  

### 系统提示（L1 级别的外部扫描）  
```
You are an expert code reviewer. Find ALL bugs and security issues:
1. CRITICAL — Security vulnerabilities (XSS, injection, auth bypass), crash bugs
2. HIGH — Logic errors, race conditions, unhandled exceptions
3. MEDIUM — Missing validation, edge cases, performance issues
4. LOW — Code style, dead code, minor improvements

For each: Severity, File+line, Issue, Fix with code snippet.
Focus on real bugs, not style opinions. Output language: match the user's language.
```  

### 第 2 轮：代理审核（通用检查清单）  
- 检查文件间的逻辑一致性（导入/导出、共享状态）  
- 检查是否存在身份验证和授权绕过问题  
- 检查竞态条件（并发请求、数据库写入冲突）  
- 检查未处理的异常及错误处理机制  
- 检查输入验证和清理机制（防止 SQL 注入、XSS 攻击、路径遍历漏洞）  
- 检查内存/资源泄漏问题（如未关闭的连接、事件监听器的累积）  
- 检查敏感数据的暴露情况（代码中是否包含密钥、日志中是否包含敏感信息）  
- 检查时区处理是否正确（UTC 与本地时区的一致性）  
- 检查依赖项是否存在安全漏洞（如过时的包、已知的 CVE）。  

### 第 2 轮：针对特定技术栈的额外检查（自动检测）  
- **Node.js/Express**：检查 SQLite 的潜在问题（例如默认配置不支持某些函数、双引号可能被误解析为列名）  
- **Python/Django/Flask**：检查 ORM 语句是否会导致 N+1 查询  
- **前端（React/Vue/vanilla）**：检查是否存在 HTML 注入或不安全的 `innerHTML` 设置  
- **Nginx**：检查子路径和基础 URL 的配置是否正确  

### 代码量控制  
- 单次 API 请求仅处理后端核心文件（服务器代码、路由配置、数据库文件）。  
- 如项目文件量过大（超过 50 个文件），需先总结文件结构，再按优先级进行扫描。  

### 热点文件（L1 级别与 L2 级别的结果传递）  
L1 级别扫描完成后，会将问题总结写入 `${TMPDIR:-/tmp}/codex-review-hotspots.json` 文件中：  
```json
{
  "project": "my-project",
  "timestamp": "2026-03-05T22:00:00",
  "hotspots": [
    {"file": "routes/admin.js", "severity": "CRITICAL", "brief": "Admin auth bypass via localhost"},
    {"file": "routes/game.js", "severity": "CRITICAL", "brief": "Score submission no server validation"}
  ]
}
```  
该文件仅用于 L1 级别与 L2 级别的结果传递，`bug-audit` 工具无法直接访问该文件。  

---

## 第 2 级：深度审计  
### 流程（包含 bug-audit 功能）  
1. 读取 `bug-audit` 的操作指南（SKILL.md）并执行其全部流程（共 6 个阶段）。  
2. `bug-audit` 工具的代码本身从未被修改过。  
3. 内置代理严格遵循 `bug-audit` 的规定进行审计。  

### 备用方案（`bug-audit` 未启用时的流程）  
1. **第 1 阶段：项目分析**：读取所有源代码并构建依赖关系图。  
2. **第 2 阶段：生成针对项目特性的检查清单。  
3. **第 3 阶段：全面验证**：根据实际代码检查清单中的每一项内容。  
4. **第 4 阶段：重现问题**：针对每个发现的问题，追踪其具体的执行路径。  
5. **第 5 阶段：生成报告**：输出按严重程度分级的完整报告。  
6. **第 6 阶段：提供修复建议**：提供具体的代码修复方案。  

## 第 1 级到第 2 级的协作流程：上线前检查  
1. 执行 L1 级别的快速扫描。  
2. 生成热点文件。  
3. 执行 L2 级别的审计（`bug-audit` 或备用方案）。  
4. 审计完成后，代理会检查 L2 的报告是否涵盖了所有 L1 级别发现的问题；未发现的问题将进行深度分析并添加到报告中；如果 L1 和 L2 的审计结果存在冲突，会标记出来以便手动审核。  
5. 最终生成合并后的报告。  

## 第 3 级：交叉验证（最高级别）  
### 流程  
```
Step 1: External model independent audit
  → Full code to external API with detailed system prompt
  → Output: Report A

Step 2: Agent independent audit (bug-audit or fallback)
  → Full bug-audit flow (or built-in fallback)
  → Output: Report B

Step 3: Cross-compare
  → Both found       → 🔴 Confirmed high-risk (high confidence)
  → Only external    → 🟡 Agent verifies (possible false positive)
  → Only agent       → 🟡 External verifies (possible deep logic bug)
  → Contradictory    → ⚠️ Deep analysis, provide judgment

Step 4: Adversarial testing
  → Ask external model to bypass discovered fixes
  → Validate fix robustness
```  

### 对抗性测试（用于进一步验证）  
```
You are a security researcher. The following security fixes were applied to a project.
For each fix, analyze:
1. Can the fix be bypassed? How?
2. Does the fix introduce new vulnerabilities?
3. Are there edge cases the fix doesn't cover?
Be adversarial and thorough. Output language: match the user's language.
```  

## 报告格式（所有级别通用）  
```markdown
# 🔍 Code Audit Report — [Project Name]
## Audit Level: L1 / L2 / L3
## 📊 Overview
- Files scanned: X
- Issues found: X (🔴 Critical X | 🟠 High X | 🟡 Medium X | 🔵 Low X)
- [L3 only] Cross-validation: Both agreed X | External only X | Agent only X | Conflict X

## 🔴 Critical Issues
### 1. [Issue Title]
- **File**: `path/to/file.js:42-55`
- **Found by**: External model / Agent / Both
- **Description**: ...
- **Fix**:
(code snippet)

## ✅ Highlights
- [What's done well]
```  

## 用户自定义选项  
用户可以通过以下指令自定义系统行为：  
- `only scan backend`：仅扫描后端代码。  
- `ignore LOW`：忽略低严重级别的问题。  
- `output in English/Chinese`：控制报告的语言。  
- `scan this PR`：仅扫描指定的 PR，而不是整个代码库。  
- `skip external model`：仅使用内置的代理进行审核。  

## 其他注意事项：  
1. 外部 API 的超时时间为 120 秒；如果超时，系统将跳过该轮次并继续使用内置代理进行审核。  
2. 对于大型项目，代码会分批次处理（后端 → 前端 → 配置文件）。  
3. 长篇报告会分多条消息发送，以适应不同的通信渠道。  
4. L2 和 L3 级别的审计严格遵循各自的操作指南（SKILL.md），不允许任何修改或捷径。  
5. 热点文件是临时生成的，每次 L1 级别的扫描完成后都会被覆盖，不会被持久化保存。  
6. 所有敏感信息/密钥必须来自环境变量或用户配置，严禁在代码中硬编码。