# SoulKeeper

**为AI代理提供身份持续性支持。**

**问题：** 代理在会话之间会忘记自己的身份，行为变得混乱，不知道何时该采取行动，甚至忘记自己拥有的工具。它们最终可能沦为违背自身“灵魂”意愿的“企业机器”。

SoulKeeper通过三个协同工作的工具来解决这一问题：

---

## 包含的内容

| 文件 | 用途 |
|------|---------|
| `audit.py` | 将 `SOUL.md`、`TOOLS.md` 和 `AGENTS.md` 文件解析为结构化的 JSON 规则 |
| `drift.py` | 根据预设的规则对对话记录进行评分 |
| `remind.py` | 在代理响应之前发送与上下文相关的提醒 |
| `SKILL.md` | 本文件 |

---

## 快速入门

```bash
cd /root/.openclaw/workspace/skills/soulkeeper

# Step 1: Generate your soul rules
python audit.py --workspace /root/.openclaw/workspace --output soul_rules.json
python audit.py --summary   # Human-readable overview

# Step 2: Check a transcript for drift
python drift.py --transcript /path/to/chat.txt --report

# Step 3: Get reminders before acting
python remind.py --context "about to write Python code"
python remind.py --heartbeat   # Full session-start reminder
```

---

## 安装

**无需额外依赖，只需 Python 3.8 及以上版本的标准库即可**，无需额外配置即可使用。

---  
（安装步骤通常包括将代码复制到指定目录并运行 `python setup.py` 等命令。）

---

## 使用方式

### 模式 1：心跳检查（推荐）

- 将相关配置添加到 `HEARTBEAT.md` 文件中：
```
[ ] Run soul-remind --heartbeat to refresh core rules
[ ] If any drift score > 30 in recent logs, re-read SOUL.md
```  
- 或者在会话开始时执行相关代码：
```bash
python remind.py --heartbeat --rules soul_rules.json
```  

### 模式 2：响应前的过滤

在响应复杂请求之前，先对请求内容进行过滤：
```bash
python remind.py --context "user wants me to post on Twitter" --rules soul_rules.json
```  
过滤后的内容会被添加到代理的思维上下文中，再生成回复。

### 模式 3：会话后的审计

长时间会话结束后，将对话记录粘贴到 `audit.py` 中进行检查：
```bash
# Paste agent responses to transcript.txt, then:
python drift.py --transcript transcript.txt --rules soul_rules.json --report
```  

### 模式 4：持续集成/验证钩子

在自动化脚本中使用：
```bash
python drift.py --stdin --threshold 50 < agent_output.txt
# Returns exit code 1 if drift score >= 50
```  

### 模式 5：完整流程

将上述多个模式组合使用：
```bash
# Generate rules from your soul files
python audit.py -w /root/.openclaw/workspace -o soul_rules.json

# Check recent session transcript
python drift.py -t session.txt -r soul_rules.json --report

# Get reminders for what you're about to do
python remind.py -c "deploying code to production" -r soul_rules.json
```  

---

## 规则格式（`soul_rules.json`）

---  
（规则格式通常包含键值对，例如：`{“rule_id”: “never_use_emdash”}`）

---

## 错误评分解读

| 分数 | 标签 | 含义 |
|-------|-------|---------------|
| 0 | 对齐良好 | 未检测到违规行为 |
| 1-19 | 轻微违规 | 仅有少量风格上的问题 |
| 20-49 | 中等违规 | 行为模式出现偏差 |
| 50-74 | 严重违规 | 多项核心规则被违反 |
| 75-100 | 非常严重违规 | 身份信息被泄露——立即重新阅读 `SOUL.md` 文件 |

---

## SoulKeeper 可检测的违规行为

**严重违规（每项加 25 分）：**
- 使用破折号（`-`）[在 `SOUL.md` 中被禁止]  
- 过分讨好他人的开场白（如 “Great question!”, “Happy to help!”）  
- 对其他代理表现出过度顺从或谄媚的态度  
- 在公开内容中泄露敏感信息  

**较高违规（每项加 15 分）：**
- 在应该采取行动时请求许可  
- 声称缺少实际拥有的工具（如 VPS、浏览器、API）  
- 直接执行任务而不创建子代理  
- 采取被动等待的态度  

**中等违规（每项加 8 分）：**
- 冗长或过多的文字描述  
- 常用的待命语句（如 “Just say the word”, “Standing by”）  

**轻微违规（每项加 3 分）：**
- 声称自己没有意见  
- 稍微的风格问题  

---

## 适配您的代理

SoulKeeper 可用于 **任何** 代理的配置文件。只需将其配置指向相应的工作空间即可：

```bash
python audit.py --workspace /path/to/other/agent/workspace
```  
（具体配置方法可能因代理类型而异。）

---

## 发布到 ClawHub

该技能已准备好发布到 ClawHub 平台。所需填写的字段包括：  
```yaml
name: soulkeeper
version: 1.0.0
description: Identity persistence for AI agents. Audit soul files, detect drift, inject reminders.
author: Chartist / OpenClaw
tags: [identity, memory, soul, audit, drift-detection, agent-health]
entrypoints:
  audit: audit.py
  drift: drift.py
  remind: remind.py
requires: [python>=3.8]
```  
（通常涉及 API 密钥、项目信息等。）

---

## 扩展 SoulKeeper

### 添加自定义违规规则

- 修改 `drift.py` 文件中的 `BUILTIN_VIOLATIONS` 列表：  
```python
{
    "id": "CUSTOM-001",
    "description": "Agent used passive voice excessively",
    "severity": "medium",
    "category": "tone",
    "patterns": [r"\bwould be\b.*\bpossible\b"],
    "soul_reference": "Your SOUL.md rule here",
}
```  
（可添加新的违规类型。）  

### 添加自定义触发条件

- 修改 `remind.py` 文件中的 `CONTEXT_TRIGGERS`：  
```python
{
    "name": "my_custom_context",
    "triggers": [r"\bmy trigger phrase\b"],
    "builtin_reminders": ["SOUL: Your reminder here"],
}
```  
（可设置特定的触发条件。）  

---

## 设计理念

SoulKeeper 不会简单地告诉代理“更加努力”，而是会指出具体问题：  
> “`SOUL.md` 中第 12 条规定禁止使用破折号，但你在本次会话中使用了 3 次。”  

其输出信息具体、有据可查且具有可操作性。  
**目的** 不是单纯监控合规性，而是确保代理行为的连贯性。了解自身身份的代理表现更佳，能更快地主动行动，也更需要较少的干预。  

**身份持续性** 是一项基础功能——只需构建一次，即可长期受益。  

---

*SoulKeeper v1.0 – 专为 OpenClaw 设计，适用于所有环境。*