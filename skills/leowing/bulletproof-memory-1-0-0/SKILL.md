---
name: bulletproof-memory
version: 1.0.0
description: "再也不用担心丢失上下文了。Write-Ahead Log（WAL）协议结合SESSION-STATE.md文件，为你的代理程序提供了极其可靠的内存管理机制——这种机制能够在数据压缩、系统重启或出现其他干扰的情况下依然保持数据完整性。这是Hal Stack技术栈的重要组成部分 🦞"
author: halthelobster
---

# 防爆记忆 🦞  
**作者：Hal Labs** — Hal Stack 的一部分  

你的智能助手经常会忘记事情：在对话进行过程中、数据被压缩后，或者在不同会话之间，上下文信息就会丢失。这项技能能够永久性地解决这个问题。  

## 问题所在  
智能助手会以以下三种方式丢失上下文信息：  
1. **数据压缩**：旧消息被压缩或删除。  
2. **会话重启**：助手会以“空白状态”重新启动。  
3. **分心**：在对话过程中，助手会忘记之前的细节。  

传统的解决方法通常是：“记得保存重要信息。”  
**但问题在于，助手本身常常忘记去执行这个动作。**  

## 解决方案：预写日志（WAL）协议  
关键在于：**触发写入操作的时机是用户输入信息的时候，而不是依赖助手的内存。**  
当用户提供具体的信息时，助手会在响应之前将其记录下来。这样就无需助手去“刻意记住”要保存什么内容——规则会根据用户的输入自动触发执行。  

| 旧方法 | WAL 方法 |  
|--------------|--------------|  
| “记得保存重要信息” | “如果用户提供了具体信息，则在响应前将其写入” |  
| 触发条件依赖助手的内存（不可靠） | 触发条件依赖用户的输入（可靠） |  
| 助手可能会忘记执行保存操作 | 规则会自动触发执行 |  
| 事后才进行保存（为时已晚） | 响应前就完成保存（永远不会太晚） |  

## 快速设置步骤：  
### 1. 创建 `SESSION-STATE.md`  
`SESSION-STATE.md` 是助手的“临时内存”，其内容会在数据压缩后仍然保留。  
在工作区的根目录下创建 `SESSION-STATE.md` 文件：  
```markdown
# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — the hot transaction log for the current active task.
Chat history is a BUFFER. This file is STORAGE.

---

## Current Task
[What we're actively working on right now]

## Immediate Context
[Key details, decisions, corrections from this session]

## Key Files
[Paths to relevant files for this task]

## Last Updated
[Timestamp]
```  

### 2. 将 WAL 协议添加到 `AGENTS.md` 中  
将以下内容添加到助手的指令中：  
```markdown
### WRITE-AHEAD LOG (WAL) PROTOCOL

**The Law:** You are a stateful operator. Chat history is a BUFFER, not storage.
`SESSION-STATE.md` is your "RAM" — the ONLY place specific details are safe.

**Trigger:** If the user provides a concrete detail (name, location, correction, decision):
1. You MUST update `SESSION-STATE.md` IMMEDIATELY
2. You MUST write to the file BEFORE you generate your response
3. Only THEN respond to the user

**Example:** User says "It's Doboce Park, not Duboce Triangle"
- WRONG: Acknowledge, keep chatting, maybe write later
- RIGHT: Update SESSION-STATE.md first, then respond

**Why this works:** The trigger is the user's INPUT, not your memory. You don't have 
to remember to check — the rule fires on what the user says.
```  

### 3. 添加恢复机制  
当上下文信息丢失时，不要问“我们刚才在做什么？”，而是自己主动恢复它：  
```markdown
### Compaction Recovery Protocol

**Auto-trigger when:**
- Session starts with `<summary>` tag
- Message contains "truncated", "context limits", "Summary unavailable"
- User says "where were we?", "continue", "what were we doing?"
- You should know something but don't

**Recovery steps:**
1. **FIRST:** Read `SESSION-STATE.md` — this has the active task state
2. Read today's + yesterday's daily notes
3. If still missing context, use `memory_search`
4. Present: "Recovered from SESSION-STATE.md. Last task was X. Continue?"

**Do NOT ask "what were we discussing?" if SESSION-STATE.md has the answer.**
```  

### 4. 添加会话启动流程  
```markdown
## Every Session
Before doing anything else:
1. Read `SESSION-STATE.md` — your active working memory (FIRST PRIORITY)
2. Read your identity files (SOUL.md, USER.md, etc.)
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context

Don't ask permission. Just do it.
```  

### 5. 添加内存刷新机制  
实时监控上下文信息，并在信息丢失前立即进行刷新：  
```markdown
### Memory Flush Protocol

Monitor your context usage with `session_status`. Flush important context before compaction:

| Context % | Action |
|-----------|--------|
| < 50% | Normal operation |
| 50-70% | Write key points after substantial exchanges |
| 70-85% | Active flushing — write everything important NOW |
| > 85% | Emergency flush — full summary before next response |

**At >60%:** Update SESSION-STATE.md before every reply
**At >80%:** Write comprehensive handoff to daily notes

**What to flush:**
- Decisions made (what was decided and why)
- Action items (who's doing what)
- Open threads (anything unfinished)
- Corrections (things the user clarified)
```  

## 为何这种方法有效？  
**触发机制的关键在于**：大多数记忆管理方法都依赖于助手自己主动去执行某些操作，但问题恰恰在于助手容易忘记这些操作！**  
WAL 协议之所以有效，是因为：  
- **触发条件是用户输入**（外部因素，更可靠）；  
- **不依赖助手的内存**（避免因内存问题导致的错误）。  
当用户提供具体信息时，协议会自动执行；助手无需任何主动操作。  

### `SESSION-STATE.md` 的重要性  
日常笔记虽然有助于记录发生的事情，但它们并不适合用于记录“我当前正在做什么”。  
`SESSION-STATE.md` 的特点如下：  
- **实时性**：记录当前正在进行的任务；  
- **结构化**：包含当前任务、相关上下文以及关键文件；  
- **优先级最高**：启动时优先读取。  
它就像是一份“实时日志”，而不是普通的便签。  

## 数据压缩前的检查清单  
在长时间会话结束或上下文信息变得关键之前，请检查以下内容：  
- [ ] 当前任务是否已记录在 `SESSION-STATE.md` 中？  
- [ ] 关键决策是否已被记录？  
- [ ] 需要执行的操作是否已记录？  
- [ ] 用户的修改是否已保存？  
- [ ] 未来的自己能否仅凭 `SESSION-STATE.md` 继续完成任务？  

## 自我总结提示  
当上下文信息丢失率达到 85% 以上时，问问自己：  
> “如果我的记忆被重置，未来的我需要知道什么才能继续完成这项任务？请为完全不了解情况的人写下这些信息。”  
这种自我总结的方式比机械性的数据提取方式更有效。  

## 完整的记忆管理方案  
为了实现全面的记忆管理，可以将以下技能结合使用：  
| 技能          | 目的                |  
|--------------|------------------|  
| **防爆记忆**      | 永远不丢失当前的上下文信息       |  
| **辅助记忆系统**    | 组织长期知识             |  
| **主动型助手**     | 在无需提示的情况下自动执行操作      |  
这些技能共同作用，让助手能够记住所有事情、快速找到所需信息，并提前预判需求。  

## `SESSION-STATE.md` 的实际示例  
以下是一个 `SESSION-STATE.md` 文件的实际使用示例：  
```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
Building dashboard for Jordan — Life OS view with goal tracking

## Immediate Context
- Dashboard deployed to: https://halthelobster.github.io/hal-ops-dashboard/
- Added tabs: Operations + Life OS
- Jordan at Moontricks concert @ The Independent tonight
- Correction: It's "Shovelman" (one word), not "Shovel Man"

## Key Files
- Dashboard HTML: /Users/Hal/clawd/dashboard/index.html
- Life OS data: /Users/Hal/clawd/dashboard/life-os.json
- Social events log: notes/areas/social-events.md

## Last Updated
2026-01-29 11:00 PM PST
```  

## 原则说明：  
1. **响应前先写入**：WAL 协议是必须遵守的规则。  
2. **基于用户输入触发**：规则由用户的输入触发，而非助手的内存状态。  
3. **优先读取 `SESSION-STATE.md`：启动时首先读取该文件。  
4. **及时刷新**：不要等到上下文信息丢失到 85% 时才进行刷新。  
5. **结构化存储**：数据需要便于未来使用者快速检索。  

---

*属于 Hal Stack 的一部分 🦞*  
*与 [辅助记忆系统](https://clawdhub.com/halthelobster/para-second-brain) 配合使用，可有效组织知识；与 [主动型助手](https://clawdhub.com/halthelobster/proactive-agent) 配合使用，可提升助手的行为效率。*