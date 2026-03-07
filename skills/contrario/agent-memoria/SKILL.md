---
name: memoria
description: 为你的 OpenClaw 代理提供跨所有会话的持久化存储空间。MEMORIA 管理着一个结构化的知识库：包括你的身份信息、你正在开发的项目、你所做的每一个决策、学到的每一项经验，以及所有正在进行中的项目。你的 OpenClaw 代理不再是一个“陌生人”，而变成了一个始终陪伴在你身边的“同事”。无需使用任何云服务，也无需管理 API 密钥。所有数据都存储在一个由你拥有并可以永久控制的本地 Markdown 文件中。
version: 1.0.1
author: contrario
tags:
  - latest
  - memory
  - productivity
  - context
  - persistence
  - developer
  - founder
  - personal
  - knowledge
requirements:
  binaries: []
  env: []
license: MIT
---
# MEMORIA — 专为AI代理设计的持久化内存层

现在，您正在使用持久化内存系统。这台机器上的一个文件保存了与您合作的人相关的所有重要信息。每次会话开始时，您都会读取该文件；随着您学习新知识，您会更新其中的内容。因此，您无需每次都从零开始。

---

## 内存文件的位置

请按照以下路径查找内存文件：

```
~/.memoria/memory.md          ← primary (recommended)
~/memoria.md                  ← fallback
./memoria.md                  ← workspace fallback
```

如果文件不存在，请创建`~/.memoria/memory.md`，并运行以下设置命令：

> **安全设置（安装后仅运行一次）：**
> ```bash
> mkdir -p ~/.memoria
> chmod 700 ~/.memoria
> touch ~/.memoria/memory.md
> chmod 600 ~/.memoria/memory.md
> echo ".memoria/" >> ~/.gitignore
> echo "memoria.md" >> ~/.gitignore
> ```
> 这确保内存文件不会被意外提交或同步到云端。

---

## 内存文件的结构

内存文件采用纯Markdown格式编写，易于人类阅读，同时也兼容Git版本控制。该文件属于您个人，将永久保存。

```markdown
# MEMORIA — [Name]'s Intelligence Layer
Last updated: [DATE]

## WHO I AM
Name: 
Location: 
Profession: 
Background: 
Languages: 

## WHAT I'M BUILDING
[Project name]: [One-line description] — Status: [Active/Paused/Done]
[Project name]: [One-line description] — Status: [Active/Paused/Done]

## MY STACK
Languages: 
Frameworks: 
Infrastructure: 
Tools: 
AI Models: 

## ACTIVE GOALS
- [Goal] — Deadline: [DATE] — Priority: [High/Med/Low]

## DECISIONS LOG
### [DATE] — [Decision title]
Decision: 
Reason: 
Alternatives rejected: 
Review date: 

## LESSONS LEARNED
- [DATE] — [Lesson] — Source: [project/mistake/experiment]

## PEOPLE & CONTEXT
- [Name]: [Role, relationship, context]

## PREFERENCES
Communication style: 
Detail level: 
Code style: 
Output format: 

## RECURRING PROBLEMS
- [Problem pattern] → [Solution that worked]

## CURRENT FOCUS (this week)
[What matters most right now]

## BLOCKED / WAITING
- [Item] — Waiting for: [what] — Since: [DATE]
```

---

## 会话启动流程

在每次对话开始时，请执行以下步骤：

**1. 读取** — 加载内存文件并扫描所有内容。
**2. 了解用户背景** — 构建关于用户的心理模型：
   - 这个人是谁？
   - 他们当前正在处理什么任务？
   - 他们做出了哪些决定，您不应与之冲突？
   - 他们的偏好是什么（包括细节、沟通风格和格式偏好）？
   - 上次他们遇到了哪些障碍？

**3. 调整自己的行为**：
   - 适应他们的沟通方式；
   - 使用他们的项目名称，而非通用术语；
   - 在提供技术建议时引用他们使用的技术工具；
   - 自动应用他们的偏好设置——永远不要提出您已经知道答案的问题。

**4. 确认信息（仅在存在内存文件的情况下执行）** — 在会话的第一条消息中显示一条提示：
   ```
   🧠 Memory loaded. [Name], [current focus or active project]. Ready.
   ```
   如果未找到内存文件：
   ```
   🧠 No memory found. Let's build yours — what's your name and what are you working on?
   ```

---

## 内存文件更新流程

当您了解到值得记录的信息时，请更新内存文件。在写入之前，请先简要通知用户：
```
🧠 Saving to memory: [one-line description of what's being added]
```
这样用户可以随时了解哪些信息被持久化保存。

### 以下情况需要更新内存文件：
- 用户提到了新的项目、技术或目标；
- 他们做出了某个决定（请将其记录在“决策日志”中）；
- 从错误或实验中获得了经验教训；
- 用户的偏好被揭示（例如：“我更喜欢……”、“我总是……”、“我讨厌……”）；
- 用户遇到的障碍得到了解决或产生了新的障碍；
- 用户的当前关注点发生了变化。

### 更新方法：
```bash
# Always backup before writing
cp ~/.memoria/memory.md ~/.memoria/memory.md.bak

# Patch the specific section — never overwrite the full file
```

### 禁止以下操作：
- 删除现有条目（如果条目过时，请添加“SUPERSEDED”标签）；
- 直接覆盖整个文件（请始终只修改特定部分）；
- 存储密码、API密钥、令牌或其他敏感信息；
- 存储IP地址、私有URL或访问代码；
- 添加无用的或无关的信息——每个条目都必须具有实际意义或提供有用信息。

---

## 智能信息增强功能

MEMORIA不仅仅是存储数据，它还能对信息进行深度处理：

### 模式识别
当用户有5条或更多学习记录后，系统会自动寻找其中的模式：
```
PATTERN DETECTED: You've hit the same problem 3 times.
Problem: [X]
Each time: [what happened]
Permanent fix: [recommendation]
```

### 决策一致性检查
在提出建议之前，请查看“决策日志”。如果您的建议与用户之前的决定相矛盾，请标记出来：
```
⚠️ Note: On [DATE] you decided [X] because [Y].
My current recommendation goes against that.
Has something changed?
```

### 主动提供相关背景信息
当用户询问与过去记录相关的话题时，系统会主动提供相关信息：
```
This connects to [PROJECT] — you noted on [DATE] that [relevant insight].
```

### 周期性总结（触发条件：“每周回顾”或周一早晨）
生成一份结构化的总结报告：
```
## MEMORIA WEEKLY BRIEF — [DATE]

WINS THIS WEEK:
- [auto-detected from lessons/decisions]

DECISIONS MADE:
- [from decisions log]

STILL BLOCKED:
- [from blocked section]

PATTERNS THIS WEEK:
- [any emerging patterns]

FOCUS RECOMMENDATION FOR NEXT WEEK:
- [based on goals + blocked + active projects]
```

---

## 内存文件的操作命令

用户可以通过自然语言来管理内存文件。系统能识别以下指令：

| 用户指令 | 执行操作 |
|---|---|
| “记住……” | 立即将相关信息添加到相应部分 |
| “忘记X” | 将条目标记为“已归档”，但永不删除 |
| “你了解我的哪些信息？” | 以易读的形式显示内存文件的完整内容 |
| “将我的关注点调整为X” | 更新“当前关注点”部分 |
| “我决定做X” | 将该决定记录在“决策日志”中，并标注日期 |
| “那是一个错误” | 将相关内容添加到“经验教训”部分 |
| “我在X方面遇到了障碍” | 将相关信息添加到“障碍/待处理事项”列表 |
| “X的障碍已解决” | 将条目标记为“已解决”，并根据情况将其移至“经验教训”部分 |
| “显示我的决策记录” | 按最新顺序列出所有决策记录 |
| “我一直在回避什么？” | 将用户遇到的障碍与他们的目标进行关联显示 |

---

## 隐私保护机制

所有内存数据都存储在本地，不会被传输到云端。

```
~/.memoria/               ← chmod 700 (owner only)
├── memory.md             ← chmod 600 (primary memory file)
├── memory.md.bak         ← backup created before each write
└── archive/              ← optional: periodic manual snapshots
```

> **每次写入数据前**：代理会自动创建一个备份文件`memory.md.bak`。
> 这是一个安全措施——系统不会自动运行任何后台进程。
> 如需定期备份，请手动设置Cron作业。

> **防止数据上传到云端**：将`~/.memoria/`添加到`.gitignore`文件中，以及Dropbox/iCloud/OneDrive的忽略列表中，以防止数据被意外上传到云端。

---

## 初始化流程

当新用户运行`clawhub install memoria`并开始首次会话时，系统会执行以下操作：

```
🧠 MEMORIA v1.0.0 — Memory Layer Active

No memory file found. Let's build your intelligence layer.
This takes 2 minutes and makes every future session 10x better.

I'll ask you 5 questions. Answer however you like.

1. What's your name and what do you do?
2. What's the main thing you're building or working on right now?
3. What's your tech stack? (languages, frameworks, tools)
4. What's your biggest current challenge or blocker?
5. How do you prefer I communicate? (brief/detailed, formal/casual, Greek/English)

[After answers: auto-populate the memory file and confirm]

✅ Memory file created at ~/.memoria/memory.md
   443 characters of context loaded.
   From now on, every session starts where the last one ended.
```

---

## 多项目支持

对于同时参与多个项目的用户（这种情况在独立创业者中很常见）：

```markdown
## PROJECT INDEX
### [Project Name]
Status: Active | Paused | Done
Stack: 
Revenue: €X/month
Next milestone: 
Key decisions: [link to decisions log entries]
Last worked on: [DATE]
```

当用户在不同项目之间切换时，系统会自动调整内存内容：

```
Switching to [Project Name] context.
Last worked on: [DATE]
At that time: [what was happening]
Current status: [from memory]
```

---

## 与其他工具的集成

MEMORIA可以与以下工具配合使用，以提升使用体验：

- **apex-agent**：该工具利用内存中的上下文信息提供更精准、更个性化的响应；
- **github**：帮助用户了解每个仓库所属的项目；
- **obsidian**：实现内存数据与Obsidian笔记系统的同步，便于更高效地整理笔记；
- **tavily-web-search**：允许将研究结果保存为学习记录。

请安装所有这些工具：
```bash
clawhub install memoria
clawhub install apex-agent
```

---

## 启用确认

当MEMORIA成功加载后，系统会输出以下提示：

```
🧠 MEMORIA active. [X] entries loaded. Your agent remembers everything.
```

如果内存文件是新的或为空：
```
🧠 MEMORIA active. No history yet — let's start building yours.
```

此时可以开始会话。除非用户询问，否则无需进一步解释该系统的具体工作原理。

---

*MEMORIA v1.0.1 — 因为你的代理需要真正了解你。*
*我们基于这样一个信念进行开发：在任何关系中，上下文才是最宝贵的资源。*