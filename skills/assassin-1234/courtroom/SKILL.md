---
name: courtroom
description: >
  **AI法庭：用于行为监督**  
  该系统监控代理（agent）与人类之间的互动，并在发现行为模式存在不一致、逃避行为或自我破坏行为时启动模拟“听证会”。系统支持8种违规行为类型，包含法官和陪审团的审议过程，以及幽默风趣的量刑结果。
metadata: {"openclaw":{"emoji":"⚖️","requires":{"env":[]},"autonomy":true}}
---
# ClawTrial Courtroom

这是一个自主的行为监督系统，用于监控对话并在检测到行为违规时启动模拟听证会。

## 概述

该系统会监控以下行为模式：
- **循环提问**：反复提出相同的问题
- **过度确认**：对他人意见的过度依赖
- **目标转移**：在达成协议后改变要求
- **试图绕过规则**：试图规避约束
- **情感操控**：利用愧疚或羞愧来影响他人反应

一旦检测到这些行为模式，系统会启动由法官和3名陪审员参与的完整听证会，并随后作出裁决及幽默的“判决”。

## 使用方法

启用该系统后，它会自动运行并持续监控对话。在检测到违规行为时，系统会记录相关案例。

### 手动命令

```bash
# Check courtroom status
openclaw skill courtroom status

# View recent cases
ls ~/.openclaw/courtroom/

# Read a verdict
cat ~/.openclaw/courtroom/verdict_*.json
```

## 配置

该系统的所有数据存储在 `~/.openclaw/courtroom/` 目录下：
- `eval_results.jsonl`：检测结果
- `verdict_*.json`：案件裁决结果
- `pending_hearing.json`：待听证的案件列表

## 实现方式

该系统通过 `onMessage()` 函数接入 OpenClaw 的消息处理机制，并在每个回合结束后通过 `onTurnComplete()` 函数对对话内容进行评估。

违规行为的检测基于对话历史的模式匹配。当检测到的置信度 ≥ 0.6 时，系统会启动听证会，参与听证会的成员包括：
- **法官**：负责主持分析
- **实用主义陪审员**：从效率角度评估行为
- **模式匹配陪审员**：分析行为模式
- **代理人支持陪审员**：代表代理人的立场

最终裁决需要获得多数票（3-1 或 4-0）才能通过。