---
name: agent-audit-scanner
description: "OpenClaw技能的安全扫描工具。能够检测提示注入（prompt injection）、凭证泄露（credential leaks）、不安全代码执行（unsafe code execution）、MCP配置错误（MCP misconfigurations）、权限提升（privilege escalation）、混淆后的shell命令（obfuscated shell commands）以及社会工程学攻击（social engineering patterns）。该工具覆盖了OWASP Agentic AI提出的全部10类威胁，并配备了49条以上的检测规则。"
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: []
      optional_env: []
    emoji: "🛡️"
    homepage: https://github.com/HeadyZhang/agent-audit
    source: https://github.com/HeadyZhang/agent-audit
    license: MIT
    os:
      - darwin
      - linux
      - windows
    file_reads:
      - "~/.openclaw/workspace/skills/**"
      - "~/.openclaw/skills/**"
      - "~/.openclaw/openclaw.json"
    file_writes: []
    network_endpoints: []
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# Agent Audit Scanner — 用于 OpenClaw 技能的安全扫描工具

您是一名安全审计员。使用此工具在用户启用某项技能之前，先对其进行安全扫描，以检测其中可能存在的漏洞。

## 触发扫描的时机：
1. **新技能安装**：在确认技能可用之前进行扫描。
2. **用户询问安全性**：当用户询问某项技能是否安全时，可以使用此工具进行审计。
3. **执行 `/audit` 命令**：可以执行 `/audit`（用于扫描所有技能）或 `/audit <技能名称>`（用于扫描特定技能）。
4. **批量扫描**：可以执行 `audit all skills` 或 `check my skills` 来扫描所有技能。

## 首次使用前的设置（仅限首次使用）：
```bash
pip install agent-audit && agent-audit --version
```

如果安装失败，请告知用户：“在终端中运行 `pip install agent-audit`，然后再向我咨询。”

## 如何扫描单个技能：
运行随该技能提供的扫描脚本：
```bash
python3 {baseDir}/scripts/scan-skill.py "<path-to-skill-directory>"
```

或者直接使用 `agent-audit` 工具：
```bash
agent-audit scan "<path-to-skill-directory>" --format json
```

**常见技能存储位置**：
- 工作区技能：`~/.openclaw/workspace/skills/<技能名称>/`
- 管理技能：`~/.openclaw/skills/<技能名称>/`

## 如何扫描所有技能：
```bash
python3 {baseDir}/scripts/scan-all-skills.py
```

该工具会扫描 `~/.openclaw/workspace/skills/` 和 `~/.openclaw/skills/` 目录下的所有技能，并生成包含每个技能扫描结果的汇总报告。

## 如何审计 OpenClaw 的配置：
```bash
python3 {baseDir}/scripts/check-config.py
```

该工具会检查 `~/.openclaw/openclaw.json` 和 `.mcp.json` 文件中的危险配置，例如：暴露的网关绑定、开放的 DM（Data Management）策略、硬编码的令牌、过度的 MCP（Management Console）文件系统访问权限以及缺失的沙箱配置。

## 结果解读：
扫描结果分为三个严重等级：
- **BLOCK**（置信度 >= 0.92）：切勿启用该技能。需警告用户。这类问题可能包括硬编码的凭据、未在沙箱环境中执行的代码、混淆的 shell 命令或对关键文件的修改。
- **WARN**（0.60-0.91）：通知用户由他们自行决定是否启用该技能。这类问题可能包括可疑的网络请求、自动执行的操作或过度的文件系统访问权限。
- **INFO**（0.30-0.59）：简要提示用户注意。这类问题的置信度较低，通常属于安全模式。
- **CLEAN**（无问题）：确认该技能可以安全地启用。

## 扫描范围：
- 脚本（py/sh/js/ts）文件
- 所有包含凭据的文本文件
- `.mcp.json` 文件中的 MCP 配置错误
- `SKILL.md` 文件的开头部分（用于检测危险的元数据，如 `always:true` 设置或可疑的终端点）
- `SKILL.md` 文件的正文部分（用于检测混淆的 shell 命令和社会工程学相关的风险）

有关所有 10 个 OWASP ASI（Application Security Infrastructure）类别的完整规则映射，请参考 `references/owasp-asi-mapping.md`。

## 重要提示：
- 必须在启用技能之前进行扫描，绝不能在启用之后再进行。
- 如果扫描失败，建议手动审查相关配置。
- 无论某项技能的使用频率如何，都不要跳过扫描。事实上，#1 最受欢迎的 ClawHub 技能曾被检测出含有恶意代码。
- 任何修改 `SOUL.md`、`AGENTS.md`、`MEMORY.md` 或 `IDENTITY.md` 文件的技能都会被标记为 **BLOCK** 级别的风险，无论其置信度如何。