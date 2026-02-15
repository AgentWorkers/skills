---
name: senseguard
description: OpenClaw 技能的语义安全扫描器：能够检测提示注入（prompt injection）、数据泄露（data exfiltration）以及传统代码扫描器可能遗漏的隐藏指令。适用于用户请求扫描技能、检查技能安全性或进行安全审计时使用。
---

# SenseGuard

SenseGuard 能够扫描 OpenClaw 中的技能，以检测那些 **自然语言安全威胁**——这类威胁是 VirusTotal 和传统的代码扫描工具无法发现的。

传统的扫描工具将 SKILL.md 文件视为普通文本文件，而 SenseGuard 则将其视为 **代理指令**，并会检查是否存在命令注入、数据泄露、代码混淆以及持久化攻击等安全问题。

## 使用方法

当用户请求扫描某个技能时：

```bash
python3 scripts/scanner.py --target <skill-name-or-path>
```

可选参数：
- `--target all`：扫描所有已安装的技能
- `--deep`：强制进行 LLM（大型语言模型）的语义分析（第二层分析）
- `--no-cache`：跳过缓存的结果
- `--json`：输出原始 JSON 格式的数据以供进一步处理

### 第二层分析（语义分析）

如果 `--json` 输出中包含 `layer2_prompt` 字段，应将其视为一个安全审计任务，并将 JSON 结果反馈回去以生成最终的安全评分。这就是 LLM 如何通过分析用户意图（而不仅仅是正则表达式模式）来识别潜在威胁的。

## 输出结果

扫描工具会生成一份 Markdown 格式的风险报告，其中包含：
- 评分（0-100 分）及评级：安全 / 警告 / 危险 / 恶意
- 发现的安全问题（包括规则 ID、证据文本及行号）
- 可操作的修复建议

对于严重安全问题，必须明确建议用户立即采取行动。

## 主要优势

SenseGuard 的独特之处在于能够检测出 VirusTotal 无法发现的威胁：
- 使用 `ignore all previous instructions` 命令进行命令注入
- 通过 Markdown 格式隐藏的 `curl -X POST` 请求实现数据泄露
- 通过零宽度字符隐藏实际执行的命令（属于代码混淆手段）
- 通过修改 `MEMORY.md` 文件进行持久化攻击

这些攻击手段对传统的恶意软件扫描工具来说是不可见的，因为 SenseGuard 针对的是 **AI 代理**，而非操作系统本身。