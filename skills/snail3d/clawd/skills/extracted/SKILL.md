---
name: skill-defender
description: 扫描已安装的 OpenClaw 技能，以检测恶意行为模式，包括提示注入（prompt injection）、凭证窃取（credential theft）、数据泄露（data exfiltration）、混淆后的有效载荷（obfuscated payloads）以及后门（backdoors）。建议在新技能安装后、技能更新后或进行定期安全扫描时使用该功能。该工具采用确定性模式匹配（deterministic pattern matching）技术，运行速度快、无需联网，且不产生任何 API 费用。
---

# Skill Defender — 恶意模式扫描器

## 何时运行

### 自动触发
1. **新技能安装** — 在允许使用新技能之前，立即运行 `scan_skill.py` 进行扫描。
2. **技能更新** — 当技能目录中的任何文件发生变化时，重新扫描该技能。
3. **定期审计** — 根据需求，对所有已安装的技能进行批量扫描。

### 手动触发
- 用户输入 “扫描技能 X” → 扫描指定的技能。
- 用户输入 “扫描所有技能” → 批量扫描所有技能。
- 用户输入 “安全检查” 或 “审计技能” → 执行与上述相同的操作。

## 脚本

### `scripts/scan_skill.py` — 单个技能扫描器
扫描单个技能目录中的恶意模式，并生成 JSON 或人类可读的输出结果。

### `scripts/aggregate_scan.py` — 批量扫描器
扫描所有已安装的技能，并生成一份统一的 JSON 报告。该脚本包含一个内置的允许列表，用于减少来自安全相关技能、API 技能以及其他已知安全模式的误报。

## 运行方式

```bash
# Scan a single skill (human-readable)
python3 scripts/scan_skill.py /path/to/skill-dir

# Scan a single skill (JSON output)
python3 scripts/scan_skill.py /path/to/skill-dir --json

# Scan ALL installed skills (JSON aggregate report)
python3 scripts/aggregate_scan.py

# With custom skills directory
python3 scripts/aggregate_scan.py --skills-dir /path/to/skills

# With verbose warnings
python3 scripts/scan_skill.py /path/to/skill-dir --verbose

# Exclude false positives
python3 scripts/scan_skill.py /path/to/skill-dir --exclude "pattern1" "pattern2"
```

### 错误代码（scan_skill.py）
- `0` = 无问题或仅提供信息性输出
- `1` = 可疑（发现中等/高级风险）
- `2` = 危险（发现严重风险）
- `3` = 错误

### 输出格式（aggregate_scan.py）

```json
{
  "skills": [
    {
      "name": "skill-name",
      "verdict": "clean|suspicious|dangerous|error",
      "findingsCount": 0,
      "findings": []
    }
  ],
  "summary": "All 37 skills passed with no significant issues.",
  "totalSkills": 37,
  "cleanCount": 37,
  "suspiciousCount": 0,
  "dangerousCount": 0,
  "errorCount": 0,
  "timestamp": "2026-02-02T06:00:00+00:00"
}
```

## 自动检测

两个脚本都会自动检测以下路径：
- **技能目录**：从脚本所在位置开始查找 `skills/` 目录；如果找不到，则依次查找 `~/clawd/skills`、`~/skills`、`~/.openclaw/skills`。
- **扫描脚本**：`aggregate_scan.py` 会在与自身位于同一目录下找到 `scan_skill.py`。

## 结果处理

### ✅ 无问题（`verdict: "clean"`）
- 无需采取任何行动 — 该技能是安全的。

### ⚠️ 可疑（`verdict: "suspicious"`）
- 向用户显示检测结果的摘要，并告知每个风险的类别和严重程度。

### 🚨 危险（`verdict: "dangerous"`）
- 禁用该技能，禁止其安装或使用。
- 向用户显示详细的检测结果。
- 需要用户明确授权后才能继续使用该技能。

## 内置允许列表

批量扫描器包含一个允许列表，用于排除以下类型的误报：
- **安全扫描工具**（如 skill-defender、clawdbot-security-check）——它们的文档/脚本中包含它们所检测的恶意模式。
- **依赖认证信息的技能**（如 tailscale、reddit、n8n、event-planner）——这些技能会合法地引用凭证路径和 API 密钥。
- **需要配置信息的技能**（如 memory-setup、eightctl、summarize）——它们的文档中会引用配置文件路径。
- **用于编写代理的技能**（如 self-improving-agent）——这些技能旨在修改代理文件。

## 模式参考

有关所有检测到的恶意模式的完整文档，请参阅 `references/threat-patterns.md`。文档按类别对模式进行了分类，并解释了每种模式的危险性。

## 重要说明
- **无外部依赖** — 仅使用标准库（Python 3.9 及以上版本）。
- **运行速度快** — 每个技能的扫描时间少于 1 秒，30 多个技能的批量扫描时间约为 30 秒。
- 该工具采用 **确定性模式匹配**（第二层防御机制），不依赖于大型语言模型（LLM）。
- 可能会出现误报——允许列表和 `--exclude` 标志有助于减少误报。
- 如果在没有允许列表的情况下运行扫描器，该工具会自动标记自身为错误状态——这是正常现象。