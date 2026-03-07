---
name: jungle-executor
description: Enforces Jungle Laws (12 Iron Rules + Warden Protocols) for decision-making, trading, and task execution. Mandates strict adherence to prevent errors like IV traps, theta bleed, narrative bias. Features: rule validation, self-audit, violation auto-correction/kill-switches. Use when: (1) Trading/options (45min dead-man switch, IV bans, logic self-destruct), (2) High-stakes decisions requiring pack consensus over solo wolf, (3) Enforcing zero-tolerance discipline in workflows/agents.
---

# Jungle Executor

## 核心使命
将“Jungle Laws”内化为团队的行为准则，并严格执行这些法则；任何违反这些法则的行为都将导致团队灭亡。团队利益高于个人利益，执行决策时必须毫不留情。

## 触发工作流程：
1. **输入审核**：在做出任何决策或执行任何操作之前，需根据12条法则及守卫者协议（参见references/laws.md）进行验证。
2. **共识检查**：在决策过程中，优先考虑数据和团队的整体利益，而非个人的观点（法则1）。
3. **风险控制**：阻止高风险交易行为，并设置45分钟的强制执行时限（参见AGENTS.md中的相关内容）。
4. **自我毁灭机制**：如果系统检测到逻辑错误或异常情况，立即执行自我毁灭操作，没有任何借口可言。
5. **日志记录与持续改进**：将违规行为记录到memory/YYYY-MM-DD.md文件中，并每月对所有记录进行汇总审查（法则12）。

## 使用场景：
- **交易**：在入场前，如果交易产品的隐含波动率（IV）超过10%，则禁止交易并设置45分钟的强制执行时限；入场后，系统会自动执行自我毁灭操作。
- **任务协作**：当多个代理同时执行任务时，需确保资源得到合理分配（法则3），并屏蔽无关干扰信息（法则6）。
- **验证脚本**：使用scripts/validate-decision.py脚本（例如：validate-decision.py "Buy SPY 680P?"）进行自动化验证。

## 相关资源：
- 法则与协议：references/laws.md
- 交易守卫者系统：references/warden-protocol.md
- 审核脚本：scripts/validate.py（用于执行自动化验证操作）

---

（注：由于提供的SKILL.md文件内容较为简短且主要包含工作流程和规则说明，翻译时保持了原文的简洁性和专业性。对于技术细节和具体实现方式，建议参考相关的参考文档或官方指南。）