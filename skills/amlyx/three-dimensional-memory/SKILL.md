# 三维记忆系统

**专为AI助手设计的三维记忆系统** — 一种模仿人类思维方式的文件管理方式

该记忆管理系统按照时间、对话内容和主题进行组织，旨在帮助AI助手更高效地处理信息。

---

## 🎯 为什么需要这种技能？

传统的文件管理方式是按照文件类型（如文档、图片、视频）来组织文件的。然而，人类的记忆方式并非如此：

- 人类会记得事件发生的**时间**、**对话内容**以及**讨论的主题**。

这种三维记忆系统为AI助手及其用户提供了更加直观和高效的记忆管理方式。

---

## 🧠 三个维度

### 第一维度：时间线记忆
```
memory/
├── 2026-02-21.md    ← What happened today
├── 2026-02-22.md    ← What happened today
└── 2026-02-23.md    ← What happened today
```

**用途**：记录日常工作任务及事件发生的顺序  
**更新频率**：每日  
**内容**：已完成的任务、做出的决策、召开的会议

---

### 第二维度：对话流
```
AI-memory-backup/
├── backup-20260221.md    ← Complete conversation transcript
├── backup-20260222.md    ← Complete conversation transcript
└── backup-20260223.md    ← Complete conversation transcript
```

**用途**：完整保存对话记录，便于搜索  
**更新频率**：每次对话结束后  
**内容**：用户与AI之间的所有交流内容

---

### 第三维度：主题网络
```
topic-memory/
├── project-product-launch/
│   ├── proposal-v1.md
│   ├── proposal-v2.md
│   └── final-version.md
│
├── decision-org-restructure/
│   ├── options-considered.md
│   ├── final-decision.md
│   └── implementation-plan.md
│
└── knowledge-market-analysis/
    ├── competitor-research.md
    └── trend-report.md
```

**用途**：集中存储与特定项目相关的信息  
**更新频率**：随着项目进展实时更新  
**内容**：与该项目相关的所有文档、决策和知识

---

## 📁 推荐的文件结构

---

## 🚀 快速入门

### 第一步：初始化系统结构

在工作区创建以下三个目录：

---

### 第二步：日常操作流程

每天，AI应执行以下操作：
1. 将当天的工作内容写入 `memory/YYYY-MM-DD.md` 文件中，包括工作总结、决策记录和已完成的任务。
2. 将对话记录备份到 `AI-memory-backup/backup-YYYYMMDD.md` 文件中，包括完整的对话内容、重要背景信息以及用户偏好设置。
3. 更新相应的 `topic-memory/` 文件夹，添加与项目相关的新文档、更新决策记录，并整合相关知识。

---

### 第三步：信息检索

- **按时间查找**：“我们周一做了什么？” → 查看 `memory/` 目录。
- **按内容查找**：“我关于定价的具体说了什么？” → 查看 `AI-memory-backup/` 目录。
- **按主题查找**：“产品发布计划在哪里？” → 查看 `topic-memory/project-product-launch/` 目录。

---

## 📝 示例：一天中的信息分布

### 情景：产品策略会议

**时间线记忆（`memory/2026-02-23.md`）**：
```markdown
# 2026-02-23 Work Log

## Morning
- Product strategy meeting with CEO
- Decided on three-tier pricing model
- Delayed launch by 2 weeks for additional testing

## Afternoon  
- Drafted pricing proposal
- Created financial projections
- Scheduled follow-up for tomorrow

## Decisions
- ✅ Adopt tiered pricing (Basic/Pro/Enterprise)
- ✅ Delay launch from March 1 → March 15
- ❌ Do not offer early-bird discounts
```

**对话记录备份（`AI-memory-backup/backup-20260223.md`）**：
```markdown
# Conversation Backup - 2026-02-23

## Product Pricing Discussion

User: "We need to decide on pricing today."

AI: "What are you considering?"

User: "I'm thinking three tiers: $29, $99, $299"

AI: "Have you considered the psychology of pricing? 
      $29 might signal 'cheap', $299 signals 'premium'."

User: "Good point. Let's go with $39, $99, $299"
[Full conversation continues...]
```

**项目相关文件（`topic-memory/project-product-launch/`）**：
```markdown
# Product Launch Project

## pricing-strategy.md (updated today)
Final decision: Three-tier model
- Starter: $39/month
- Professional: $99/month  
- Enterprise: $299/month

## timeline.md (updated today)
Launch date: March 15, 2026 (delayed from March 1)

## key-decisions.md
- Pricing tiers finalized (2026-02-23)
- Launch delayed for QA (2026-02-23)
```

---

## 💡 最佳实践

### 对用户而言：
1. **每周查看日志**：快速回顾当天发生的事情。
2. **搜索对话记录**：查找特定的对话内容和上下文。
3. **使用主题文件夹**：按项目而非文件类型来查找信息。
4. **保持 `MEMORY.md` 文件的更新**：确保其中包含AI的身份信息和用户的偏好设置。

### 对AI助手而言：
1. **每天更新所有三个维度的数据**：不要遗漏任何信息。
2. **使用清晰、易于搜索的文件夹名称**。
3. **建立交叉引用**：在需要时在不同维度之间建立关联。
4. **维护索引**：维护一个活跃主题的索引。

---

## 🔍 常见问题解决方法

**“找不到文件”**：
   → 检查三个维度中的文件。如果文件不在时间线或主题文件夹中，可以在对话记录备份中查找。

**“有重复信息”**：
   **这是有意设计的**：时间线记录事件发生的时间，主题文件夹记录具体内容，对话记录则解释原因。

**“AI忘记了我们的讨论内容”**：
   → 查看 `AI-memory-backup/` 文件，其中包含完整的对话记录。

---

## 🌟 为什么这种系统有效？

传统文件管理方式的问题是：“我把文件保存在哪里了？”
而三维记忆系统则能帮助用户快速定位信息：
“我们在昨天的会议上讨论了定价策略”，只需查看 `memory/2026-02-23.md`，再找到 `topic-memory/project-pricing/` 文件，即可获取最新版本的信息。
**结果**：只需10秒即可找到文件，而无需花费5分钟。

---

## 📄 文件元数据

- **作者**：@openclaw-user  
- **创建时间**：2026-02-23  
- **版本**：1.0.0  
- **许可证**：MIT  
- **标签**：记忆管理、组织效率、工作流程

---

*“最好的文件系统，就是你根本不需要去思考它的系统。”*