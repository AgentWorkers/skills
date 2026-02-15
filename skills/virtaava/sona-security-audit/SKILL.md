---
name: security-audit
description: "OpenClaw/ClawHub 技能和仓库的安全审计采用“失败即关闭”（Fail-Closed）策略：在启用或安装之前，会进行 Trufflehog 保密信息扫描、semgrep 安全代码分析（SAST）、提示注入（Prompt-Injection）检测、持久性威胁信号（Persistence Signals）检查以及供应链健康状况（Supply-Chain Hygiene）验证。"
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["jq","trufflehog","semgrep","python3"]},"install":[{"id":"apt-jq","kind":"apt","package":"jq","bins":["jq"],"label":"Install jq (apt)"},{"id":"apt-ghog","kind":"apt","package":"python3","bins":["python3"],"label":"Install Python 3 (apt)"},{"id":"apt-trufflehog","kind":"apt","package":"trufflehog","bins":["trufflehog"],"label":"Install trufflehog (apt)"},{"id":"pipx-semgrep","kind":"shell","label":"Install semgrep (pipx)","command":"python3 -m pip install --user pipx && python3 -m pipx ensurepath && pipx install semgrep"},{"id":"brew-jq","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq (brew)"},{"id":"brew-trufflehog","kind":"brew","formula":"trufflehog","bins":["trufflehog"],"label":"Install trufflehog (brew)"},{"id":"brew-semgrep","kind":"brew","formula":"semgrep","bins":["semgrep"],"label":"Install semgrep (brew)"}]}}
---

# 安全审计

这是一种专为恶意行为设计的、采用“失败即终止”（fail-closed）机制的代码库及 OpenClaw/ClawHub 技能审计流程。该流程并不试图判断“该技能是否能够正常工作”，而是着重于分析“该技能是否可能危害系统安全”。

## 审计内容（概述）

该技能的审计脚本包含多个层面的检查：

- **秘密信息/凭证泄露风险**：使用 trufflehog 工具进行检测
- **静态代码分析**：利用 semgrep 工具（包含自动检测规则）
- **针对恶意仓库的专项审计**：检查提示注入（prompt-injection）行为、持久化机制以及依赖项的安全性

如果任何一层检查失败，整个审计流程将被判定为“失败”（FAIL）。

## 运行审计（使用 JSON 格式）

请从该技能文件夹中执行以下命令（使用 `bash`，以确保即使代码文件在压缩传输过程中丢失了可执行权限，审计仍能正常进行）：

```bash
bash scripts/run_audit_json.sh <path>
```

示例：

```bash
bash scripts/run_audit_json.sh . > /tmp/audit.json
jq '.ok, .tools' /tmp/audit.json
```

### 安全级别（用户可配置）

可以设置审计的严格程度（默认值为 `standard`）：

```bash
OPENCLAW_AUDIT_LEVEL=standard bash scripts/run_audit_json.sh <path>
OPENCLAW_AUDIT_LEVEL=strict   bash scripts/run_audit_json.sh <path>
OPENCLAW_AUDIT_LEVEL=paranoid bash scripts/run_audit_json.sh <path>
```

- `standard`：采用较为宽松的默认设置（需要生成锁定文件；安装钩子、持久化机制以及提示注入行为均会被视为失败）
- `strict`：更多不符合安全标准的代码会被直接判定为失败（例如，经过压缩或混淆处理的代码）
- `paranoid`：对任何不符合安全规范的代码都会立即判定为失败

## 对于零信任安装流程的要求

对于采用严格安全策略的仓库，需要在仓库根目录下提供一份机器可读取的意图/权限说明文件（manifest）：

- `openclaw-skill.json`

如果某个仓库或技能未提供该文件，审计流程应将其视为“失败”（FAIL）。

详情请参阅：`docs/OPENCLAW_SKILL_MANIFEST_SCHEMA.md`。

## 可选：执行沙箱环境（使用 Docker）

使用 Docker 是可选的。即使不使用 Docker，该技能也可以用于静态代码审计。但如果需要执行任何生成的或不可信的代码，建议在沙箱环境中进行。

## 相关文件：

- `scripts/run_audit_json.sh`：主要的 JSON 格式审计脚本
- `scripts/hostile_audit.py`：用于检测提示注入、持久化行为以及依赖项安全性的工具
- `scripts/security_audit.sh`：便捷的脚本封装层（始终返回 JSON 格式的审计结果，且返回值非零表示审计失败）
- `openclaw-skill.json`：机器可读取的意图/权限说明文件