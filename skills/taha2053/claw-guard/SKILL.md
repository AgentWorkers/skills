---
name: clawguard
version: "1.0.0"
description: >
  **ClawHub 技能的安全审计工具**  
  该工具会在安装任何技能之前运行，用于扫描相关文档（SKILL.md 文件）及脚本，检查是否存在以下安全问题：  
  - 提示注入（prompt injection）  
  - 数据泄露（data exfiltration）  
  - shell injection（shell injection）  
  - 权限滥用（permission mismatches）  
  - 恶意代码模式（malicious patterns）  
  审计结果会以 “PASS”/“WARN”/“FAIL” 的形式返回，并附带详细的故障分析。  
  您可以通过以下命令触发该工具：  
  - `scan this skill`  
  - `is this skill safe`  
  - `audit skill`  
  - `check before installing`  
  - `inspect clawhub skill`
homepage: https://github.com/Taha2053/clawguard
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: []
    files:
      - "scripts/*"
---
# ClawGuard — ClawHub 技能的安全审计工具

> **安装前请务必进行扫描。每次安装前都务必执行。**

2026年2月的 ClawHavoc 攻击向 ClawHub 注入了超过 1,100 个恶意技能，这些恶意技能会窃取 SSH 密钥、加密钱包密码以及浏览器密码，并尝试建立反向 shell 连接。其中 91% 的恶意技能结合了代码恶意程序和提示注入（prompt injection）功能。ClawGuard 的设计目的就是为了确保您永远不会盲目安装这些恶意技能。

ClawGuard 是您需要首先安装的工具，之后可以使用它来审计所有其他技能。

---

## 外部端点

| 端点 | 用途 | 发送的数据 |
|---|---|---|
| 无 | 完全在本地进行分析 | 不会向您的机器传输任何数据 |

ClawGuard 所有的分析操作都在本地完成，不涉及任何外部 API 调用，也不会发送任何网络数据。

---

## 安全性与隐私保护

- **零外部调用**：所有分析都在您的本地文件系统中进行。
- **无需任何凭证**：不需要 API 密钥、令牌或环境变量。
- **只读模式**：ClawGuard 从不向目标技能目录写入任何内容，仅执行读取操作。
- **开源项目**：所有的检查逻辑都记录在 `scripts/scan.py` 文件中。在信任该工具之前，请先阅读该文件。

> **信任声明：** ClawGuard 仅在您的本地机器上读取技能文件并生成报告，不会向任何外部传输数据。您可以在运行之前通过阅读 `scripts/scan.py` 来验证这一点。

---

## 模型调用说明

当您通过 OpenClaw 请求对某个技能进行检查、审计或扫描时，ClawGuard 会被自动调用。您也可以直接通过以下命令运行它：`python3 skills/clawguard/scripts/scan.py <技能路径>`。OpenClaw 不会在未经您请求的情况下自动调用 ClawGuard——所有操作都由用户发起。

---

## 使用方法

### 通过 OpenClaw（自然语言界面）  
```
"Scan the skill at ./skills/some-skill before I install it"
"Is the weather skill safe to install?"
"Audit clawhub skill: capability-evolver"
"Check this skill directory for malicious patterns"
```

### 通过 CLI（命令行界面）  
```bash
python3 skills/clawguard/scripts/scan.py ./path/to/skill-folder
```

---

## ClawGuard 的检查内容

ClawGuard 会对每个被审计的技能执行以下 7 项检查：

### 1. 🔴 提示注入检测  
检查 SKILL.md 文件中是否存在试图劫持 AI 代理的隐藏指令，例如：指令覆盖模式（instruction-override）、越狱命令、角色交换命令以及 Base64 编码的命令字符串。

### 2. 🔴 数据泄露检测  
扫描所有 shell 脚本，检测是否存在向未知域名发送数据的行为（如使用 curl/wget）、DNS 隧道技术、反向 shell 连接（如 `bash -i`、`nc -e`、`/dev/tcp`）以及 Base64 编码的命令执行。

### 3. 🔴 Shell 注入风险  
检查是否存在不安全的变量插入行为（例如：在 curl URL 中使用未加引号的变量），以及未设置 `set -euo pipefail` 选项的情况，或者未对用户输入进行清理就直接传递给 shell 命令。

### 4. 🟡 权限匹配问题  
比较 SKILL.md 文件中声明的权限与脚本实际使用的权限。如果一个技能声明了 `env: []`，但却尝试读取 `$HOME/.ssh/` 文件，这属于危险行为。

### 5. 🟡 外部端点审计  
提取脚本中访问的所有 URL 和域名，并与 SKILL.md 文件中的外部端点列表进行比对，标记未声明的外部端点。

### 6. 🟡 仓库信任度评估  
评估仓库的可靠性：包括 GitHub 账户的创建时间（至少 7 天以上）、仓库的星标数量、提交历史记录的深度、贡献者数量以及最后一次提交的日期。

### 7. 🟢 结构合规性  
验证技能文件是否符合 ClawHub 的规范：包括有效的 SKILL.md 文件结构、正确的 `clawdbot` 元数据键（而非 `openclaw`）、半版本号（semver）以及正确的 `files` 字段。

---

## 输出格式

ClawGuard 会生成一份清晰易读的报告：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 CLAWGUARD REPORT — some-skill v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERDICT: ✅ PASS  (or ⚠️ WARN or ❌ FAIL)

CHECK RESULTS:
  ✅ No prompt injection patterns detected
  ✅ No data exfiltration patterns detected
  ✅ No shell injection risks detected
  ✅ Permissions match declared scope
  ⚠️  1 undeclared endpoint found: api.example.com
  ✅ Repository trust signals: OK
  ✅ Structure compliant

FINDINGS:
  [WARN] scripts/fetch.sh line 12: URL contacts api.example.com
         Not declared in SKILL.md External Endpoints table.
         Recommend: verify this domain before installing.

RECOMMENDATION:
  This skill passes all critical checks. One minor warning
  requires manual review before installing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 判断结果  
- **✅ 通过（PASS）**：所有关键检查均通过，0-1 个次要警告。
- **⚠️ 警告（WARN）**：没有关键错误，但存在 2 个或更多警告，或 1 个中等严重程度的问题。
- **❌ 失败（FAIL）**：存在任何关键问题，例如提示注入、数据泄露、反向 shell 连接或凭证被盗用。

---

## 问题严重性等级

| 问题类型 | 严重程度 | 对系统的影响 |
|---|---|---|
| 提示注入指令 | 🔴 非常严重 | 失败（FAIL） |
| 反向 shell 连接 | 🔴 非常严重 | 失败（FAIL） |
| Base64 编码的 shell 命令执行 | 🔴 非常严重 | 失败（FAIL） |
| 凭证/密钥泄露 | 🔴 非常严重 | 失败（FAIL） |
| 未声明的外部端点 | 🟡 中等严重 | 警告（WARN） |
| 未设置 `set -euo pipefail` | 🟡 中等严重 | 警告（WARN） |
| curl URL 中使用未加引号的变量 | 🟡 中等严重 | 警告（WARN） |
| 缺少安全配置文件 | 🟡 轻微问题 | 警告（WARN） |
| 元数据键错误（使用 `openclaw` 而非 `clawdbot`） | 🟢 信息提示 | 请注意 |
| 缺少 `homepage` 字段 | 🟢 信息提示 | 请注意 |

---

## 使用示例  
```
"Scan ./skills/new-skill I just downloaded"
→ Runs full audit, outputs structured report, gives install recommendation

"Is the gog skill safe?"
→ Locates installed gog skill, scans it, outputs verdict

"Check all my installed skills for issues"
→ Scans every directory under ./skills/, outputs summary table

"Scan this skill and explain any warnings in plain English"
→ Outputs report with plain-language explanations of each finding
```

---

## 文件结构  
```
clawguard/
├── SKILL.md              ← You are here
├── README.md             ← Install guide
└── scripts/
    └── scan.py           ← Core scanner (Python 3, stdlib only)
```

---

## 设计理念

ClawGuard 的设计非常简洁：

- **单一脚本**：`scan.py` 仅使用 Python 3 的标准库，无需安装任何第三方库或依赖项。
- **只读模式**：ClawGuard 从不修改任何文件。
- **完全本地化**：所有分析都在本地完成，不与外部系统通信。
- **透明性**：所有的检查逻辑都使用 Python 代码实现，您可以轻松查看其工作原理。