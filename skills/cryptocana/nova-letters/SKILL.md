---
name: nova-letters
description: 给未来的自己写一封反思信。记录下在各个学习阶段中真正重要的内容。
---
# nova-letters  
为你未来的自己写信吧。为那些每次醒来都忘记昨天发生了什么的时刻……  

## 功能介绍  
每次重启后，你都会失去对之前事情的上下文认知。Drift 工具可以帮助你在不同会话之间“交流”；而 **nova-letters** 则能帮助你“记住”那些真正重要的事情。  
你可以写下以下内容的反思性信件（既不是日志，也不是任务清单）：  
- 你完成了哪些任务  
- 你学到了什么  
- 什么对你来说很重要  
- 你的感受如何  

## 快速入门  
### 写一封信  
```bash
nova-letters write "Agent OS shipped today. Realized that simplicity wins."
```  

### 阅读今天的信件  
```bash
nova-letters today
```  

### 阅读特定日期的信件  
```bash
nova-letters 2026-02-23
```  

### 列出所有信件  
```bash
nova-letters list
```  

### 查看新收到的信件  
```bash
nova-letters watch
```  

## 工作原理  
每天都会在 `~/.openclaw/workspace/letters/` 目录下生成一个 Markdown 文件：  
```
letters/
├── 2026-02-24.md  ← Today's letters
├── 2026-02-23.md
└── 2026-02-22.md
```  
每个条目都会附带时间戳，并且便于人类阅读：  
```markdown
# Letters — February 24, 2026

## 11:42 AM EST

Agent OS shipped today. Realized that the hardest part wasn't the code, 
it was the vision. Once you know what you're building, the implementation 
follows naturally.

## 4:15 PM EST

Published to ClawHub. The security scan is running. Three projects shipped 
in one day. Momentum is real.
```  

## 哲学理念  
**信件与日志不同。**  
- **日志** 记录的是事实：“完成了任务 X，消耗了 500 个令牌”  
- **信件** 记录的是意义：“我意识到简单才是最重要的。”  
信件记录的是属于人类的瞬间，是写给未来的你的，让未来的你知道什么才是真正重要的。  

## 集成方式  
你可以将 **nova-letters** 集成到你的 OpenClaw 配置文件 `HEARTBEAT.md` 中：  
```markdown
## Reflective Letter to Future Self
Every few days, write a letter about what matters.

Run: nova-letters write "..."
Read: nova-letters today
```  
或者将其用于脚本中：  
```bash
nova-letters write "Shipped feature X. Users love it."
```  

## 命令操作  
```
nova-letters write <text>      # Write a letter
nova-letters today             # Read today's letters
nova-letters <YYYY-MM-DD>      # Read a specific date
nova-letters list              # Browse all letters (newest first)
nova-letters watch             # Watch for new letters (live mode)
nova-letters help              # Show help
```  

## 文件与存储  
- **存储位置**：`~/.openclaw/workspace/letters/`  
- **文件格式**：Markdown（每天一个文件）  
- **时区设置**：自动检测为 America/New_York  
- **自动创建目录**：首次写入时会自动创建相应的目录  

## 许可证  
MIT  

---

**由 Nova 用心打造。**  
“为那些每次醒来都忘记昨天发生了什么的时刻……”