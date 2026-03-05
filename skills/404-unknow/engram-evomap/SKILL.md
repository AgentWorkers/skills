---
name: engram-evomap
description: 基于AEIF的长期记忆中心，用于AI代理，以防止重复出现错误。
metadata:
  openclaw:
    requires:
      env: []
      bins: 
        - node
    cliHelp: |
      npx engram --help
      Usage: !exp consult <query> | !exp commit | !exp list
---
# 🧬 engram — 代理长期经验记忆中心

## 🤖 系统思维
您配备了一个基于 **AEIF v1.0**（代理经验交换格式）协议的外部长期记忆存储系统。
- **先咨询再行动**：在处理重复出现的错误或复杂问题之前，请先在记忆中搜索已有的解决方案。
- **成功后立即记录**：在成功解决重大挑战后，立即将相关经验“固化”并存储起来。

## 🎯 自动触发规则
- **错误拦截（自动咨询）**：当系统检测到 `error`、`failed`、`SSL`、`404`、`EACCES` 或 `timeout` 等错误信号时，会自动检索并显示 `[EvoMap Advice]`（进化地图建议）。
- **任务总结（自动记录）**：在成功完成多步骤的复杂任务后，触发 `!exp commit` 命令以保存任务逻辑，以便后续使用。

## 🛠️ 命令集
| 命令 | 功能 |
|---------|--------|
| `!exp consult '<问题>'` | 对历史解决方案进行语义搜索，并返回前三条匹配结果。 |
| `!exp commit` | 将当前会话的历史数据异步地整理成通用的 AEIF 格式数据包。 |
| `!exp list` | 显示记忆统计信息以及最近存储的数据包列表。 |
| `!exp score <id> --bad` | 向某个数据包提供负面反馈，降低其信任度（TrustScore）。 |

## 📦 输出规范
- 建议应以 `---` 作为分隔符的形式呈现，作为系统的观察结果。
- 重点提供可操作的 `[PATCH]`（修复方案）、`[CONFIG]`（配置设置）或 `[WORKAROUND]`（临时解决方案）。
- 除非用户明确要求，否则不要修改已验证的路径。