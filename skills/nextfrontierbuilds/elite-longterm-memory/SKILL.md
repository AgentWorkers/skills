---
name: elite-longterm-memory
version: 1.2.3
description: "终极AI代理内存系统，适用于Cursor、Claude、ChatGPT和Copilot。支持WAL协议、向量搜索、git-notes功能以及云备份，确保数据不会丢失。同时具备Vibe-coding兼容性。"
author: NextFrontierBuilds
keywords: [memory, ai-agent, ai-coding, long-term-memory, vector-search, lancedb, git-notes, wal, persistent-context, claude, claude-code, gpt, chatgpt, cursor, copilot, github-copilot, openclaw, moltbot, vibe-coding, agentic, ai-tools, developer-tools, devtools, typescript, llm, automation]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - OPENAI_API_KEY
      plugins:
        - memory-lancedb
---

# 精英级长期记忆系统 🧠  
**专为AI代理设计的终极记忆解决方案。** 将6种经过验证的记忆管理方法整合到一个高度可靠的架构中。  

永远不会丢失上下文信息，永远不会忘记所做的决策，也永远不会重复犯错。  

## 架构概述  
```
┌─────────────────────────────────────────────────────────────────┐
│                    ELITE LONGTERM MEMORY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   HOT RAM   │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  LanceDB    │  │  Git-Notes  │             │
│  │ STATE.md    │  │  Vectors    │  │  Knowledge  │             │
│  │             │  │             │  │  Graph      │             │
│  │ (survives   │  │ (semantic   │  │ (permanent  │             │
│  │  compaction)│  │  search)    │  │  decisions) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← Curated long-term           │
│                  │  + daily/   │    (human-readable)            │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │ SuperMemory │  ← Cloud backup (optional)     │
│                  │    API      │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```  

## 五层记忆系统  

### 第1层：高温RAM（SESSION-STATE.md）  
**来源：bulletproof-memory**  
用于存储当前的工作状态，能够抵御数据压缩。采用“预写日志”（Write-Ahead Log）机制。  

**规则：** 在响应用户输入之前，先将其写入内存。触发条件为用户输入，而非代理自身的操作。  

### 第2层：温热存储（LanceDB向量）  
**来源：lancedb-memory**  
支持跨所有记忆库进行语义搜索；自动提取相关内容并补充到当前上下文中。  

```bash
# Auto-recall (happens automatically)
memory_recall query="project status" limit=5

# Manual store
memory_store text="User prefers dark mode" category="preference" importance=0.9
```  

### 第3层：冷存储（Git-Notes知识图谱）  
**来源：git-notes-memory**  
用于存储结构化的决策、学习成果及相关背景信息。该层支持对不同分支内容的访问。  

```bash
# Store a decision (SILENT - never announce)
python3 memory.py -p $DIR remember '{"type":"decision","content":"Use React for frontend"}' -t tech -i h

# Retrieve context
python3 memory.py -p $DIR get "frontend"
```  

### 第4层：精选档案（MEMORY.md + 每日记录）  
**来源：OpenClaw原生功能**  
以人类可读的形式保存长期记忆数据，包含每日日志及精炼后的知识内容。  

```
workspace/
├── MEMORY.md              # Curated long-term (the good stuff)
└── memory/
    ├── 2026-01-30.md      # Daily log
    ├── 2026-01-29.md
    └── topics/            # Topic-specific files
```  

### 第5层：云备份（SuperMemory）——可选  
**来源：supermemory**  
支持跨设备同步数据，实现与知识库的实时交互。  

```bash
export SUPERMEMORY_API_KEY="your-key"
supermemory add "Important context"
supermemory search "what did we decide about..."
```  

### 第6层：自动信息提取（Mem0）——推荐使用  
**新功能：** 自动从对话中提取关键事实，可减少80%的存储开销（Token使用量）。  

```bash
npm install mem0ai
export MEM0_API_KEY="your-key"
```  

**系统优势：**  
- 自动提取用户的偏好设置、决策内容及重要事实；  
- 优化现有记忆数据，避免重复存储；  
- 相较原始数据，存储占用空间减少80%；  
- 跨会话自动保持数据一致性。  

## 快速设置步骤  

### 1. 创建SESSION-STATE.md（高温RAM）  
```bash
cat > SESSION-STATE.md << 'EOF'
# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — survives compaction, restarts, distractions.

## Current Task
[None]

## Key Context
[None yet]

## Pending Actions
- [ ] None

## Recent Decisions
[None yet]

---
*Last updated: [timestamp]*
EOF
```  

### 2. 启用LanceDB（温热存储）  
在`~/.openclaw/openclaw.json`文件中进行配置：  
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```  

### 3. 初始化Git-Notes（冷存储）  
```bash
cd ~/clawd
git init  # if not already
python3 skills/git-notes-memory/memory.py -p . sync --start
```  

### 4. 验证MEMORY.md文件结构  
```bash
# Ensure you have:
# - MEMORY.md in workspace root
# - memory/ folder for daily logs
mkdir -p memory
```  

### 5. （可选）配置SuperMemory  
```bash
export SUPERMEMORY_API_KEY="your-key"
# Add to ~/.zshrc for persistence
```  

## 代理使用指南  

### 会话开始时：  
1. 读取SESSION-STATE.md以获取当前上下文；  
2. 使用`memory_search`查询相关历史记录；  
3. 查看memory/YYYY-MM-DD.md文件以了解近期活动。  

### 对话过程中：  
1. 用户提供具体细节时——在响应前将其写入SESSION-STATE.md；  
2. 做出重要决策时——将其存储到Git-Notes中；  
3. 用户表达偏好时——使用`memory_store`命令（设置重要性为0.9）。  

### 会话结束时：  
1. 使用最新信息更新SESSION-STATE.md；  
2. 将重要内容迁移到MEMORY.md中以长期保存；  
3. 在memory/YYYY-MM-DD.md中创建/更新每日日志。  

### 每周维护步骤：  
1. 审查SESSION-STATE.md，整理已完成的任务；  
2. 使用`memory_recall query="*" limit=50`清除LanceDB中的冗余数据；  
3. 使用`memory_forget id=<id>`清除无关的存储内容；  
4. 将每日日志整合到MEMORY.md中。  

## 关键的WAL协议（Write-Ahead Log机制）  
**预写日志**：在响应用户输入之前，先将其写入内存，确保数据持久性。  

| 触发条件 | 处理方式 |  
|---------|--------|  
| 用户更改偏好设置 | 将新信息写入SESSION-STATE.md后再响应；  
| 用户做出决策 | 同上；  
| 用户设定截止时间 | 同上；  
| 用户纠正你的错误 | 同上；  

**为何如此设计？** 如果先响应用户后再进行数据保存（例如因系统崩溃或压缩），可能会导致上下文丢失。WAL协议能有效防止此类问题。  

## 示例工作流程  
```
User: "Let's use Tailwind for this project, not vanilla CSS"

Agent (internal):
1. Write to SESSION-STATE.md: "Decision: Use Tailwind, not vanilla CSS"
2. Store in Git-Notes: decision about CSS framework
3. memory_store: "User prefers Tailwind over vanilla CSS" importance=0.9
4. THEN respond: "Got it — Tailwind it is..."
```  

## 维护命令  
```bash
# Audit vector memory
memory_recall query="*" limit=50

# Clear all vectors (nuclear option)
rm -rf ~/.openclaw/memory/lancedb/
openclaw gateway restart

# Export Git-Notes
python3 memory.py -p . export --format json > memories.json

# Check memory health
du -sh ~/.openclaw/memory/
wc -l MEMORY.md
ls -la memory/
```  

## 记忆系统故障原因及解决方法  

了解故障的根本原因有助于快速解决问题：  
| 故障类型 | 原因 | 解决方案 |  
|--------------|-------|-----|  
| 完全忘记信息 | 禁用`memory_search`功能 | 重新启用该功能并添加OpenAI密钥；  
| 文件无法加载 | 代理未正确读取记忆数据 | 在`AGENTS.md`中添加相关配置；  
| 重要信息未被捕获 | 未启用自动提取功能 | 使用Mem0或手动记录数据；  
| 子代理无法获取上下文 | 在任务提示中明确提供所需上下文；  
| 重复犯错 | 未将错误记录下来 | 将错误信息写入`memory/lessons.md`文件。  

## 解决方案（按难度排序）  

### 1. 快速解决方案：启用`memory_search`  
（如果你拥有OpenAI密钥，可启用语义搜索功能。）  
```bash
openclaw configure --section web
```  
该功能支持在MEMORY.md及所有相关文件中进行向量搜索。  

### 2. 推荐方案：集成Mem0  
（自动从对话中提取关键事实，减少80%的存储开销。）  
```bash
npm install mem0ai
```  

### 3. 更优的文件结构（无依赖关系）  
**建议将MEMORY.md文件保持简洁（<5KB），并附上详细信息的链接。**  

## 立即可执行的修复措施：  
| 问题 | 解决方案 |  
|---------|-----|  
| 忘记用户偏好 | 在MEMORY.md中添加“## Preferences”章节；  
| 重复犯错 | 将每次错误记录到`memory/lessons.md`中；  
| 子代理无法获取上下文 | 在任务提示中包含关键信息；  
| 忘记近期工作内容 | 严格执行每日文件更新规则；  
| 记忆搜索功能失效 | 确保`OPENAI_API_KEY`已正确设置。**  

## 常见问题排查方法：  
- **代理在对话中频繁忘记信息**：检查WAL协议的执行情况。  
- **无关内容被错误地添加到记忆中**：禁用自动信息捕获功能，提高`minImportance`阈值。  
- **内存占用过大导致检索速度慢**：执行维护操作（清除旧数据、整理每日日志）。  
- **Git-Notes数据无法持久保存**：使用`git notes push`命令与远程服务器同步数据。  
- **`memory_search`无结果**：检查`OPENAI_API_KEY`是否已正确配置。  

---

**相关资源链接：**  
- bulletproof-memory：https://clawdhub.com/skills/bulletproof-memory  
- lancedb-memory：https://clawdhub.com/skills/lancedb-memory  
- git-notes-memory：https://clawdhub.com/skills/git-notes-memory  
- memory-hygiene：https://clawdhub.com/skills/memory-hygiene  
- supermemory：https://clawdhub.com/skills/supermemory  

**开发团队：[@NextXFrontier](https://x.com/NextXFrontier)——Next Frontier AI工具包的一部分**