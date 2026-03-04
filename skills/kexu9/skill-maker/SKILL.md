---
name: skill-maker
description: Create new agent skills from scratch. Use when: (1) Building a new skill for specific capabilities, (2) Converting workflows into reusable skills, (3) Designing skill structure and triggers, (4) Setting up skill resources (scripts, references, assets).
version: 1.1.0
changelog: "v1.1.0: Fresh approach with reasoning framework"
metadata: {"clawdbot":{"emoji":"🔨","category":"creation"}}
---

# 技能构建工具 🔨  
使用结构化的推理方法，创建强大且可复用的技能。  

---

## 技能构建框架  

```
┌─────────────────────────────────────────────────────────────┐
│  SKILL FORGING PROCESS                                      │
├─────────────────────────────────────────────────────────────┤
│  1. INTERPRET  → What capability does this skill need?     │
│  2. DESIGN    → Structure, resources, trigger conditions   │
│  3. FORGE     → Write SKILL.md, create resources          │
│  4. TEST      → Verify triggers, check quality            │
│  5. POLISH    → Refine based on testing                   │
└─────────────────────────────────────────────────────────────┘
```  

---

## 决策树：我们正在构建什么？  

```
INTENT
    │
    ├── Brand new skill ──→ Start from Step 1
    │
    ├── Replace existing ──→ 
    │       └── Read old first, then improve
    │
    └── Clone & modify ──→ 
            └── Copy, rename, customize
```  

---

## 第一步：理解需求  

### 核心问题  

| 问题 | 你的答案 |  
|----------|-------------|  
| **这个技能的功能是什么？** | [技能功能] |  
| **谁会使用它？** | [用户触发条件] |  
| **应用领域是什么？** | [主题领域] |  
| **难度如何？** | 简单/中等/复杂 |  

### 自我检查：理解需求  
- [ ] 我能用一句话描述这个技能吗？  
- [ ] 我知道哪些短语会触发这个技能吗？  
- [ ] 这真的是一个全新的功能吗？  

---

## 第二步：设计技能  

### 确定技能的复杂性  

```
COMPLEXITY LEVEL
    │
    ├── Simple ──→ SKILL.md only
    │       └── One capability, clear steps
    │
    ├── Medium ──→ SKILL.md + references/
    │       └── Needs docs to reference
    │
    └── Complex ──→ SKILL.md + scripts/ + references/
            └── Needs executable code
```  

### 目录结构  

```
skill-name/
├── SKILL.md              # Required: name, description, body
├── scripts/              # Optional: executable code
├── references/          # Optional: detailed docs
└── assets/              # Optional: templates, files
```  

### 编写技能触发条件  

用户通常会说：  
- “我需要[执行某个动作]”  
- “我该如何[完成某项任务]？”  
- “帮我处理[相关领域的问题]”  
- “你能[提供某个功能]吗？”  

**描述格式：**  
> “[技能功能]。适用于：(1) [情境1]，(2) [情境2]，(3) [情境3]。”  

**示例：**  
> “从 wttr.in 获取天气数据。适用于：(1) 用户询问天气情况，(2) 用户想要天气预报，(3) 用户询问[城市]的温度。”  

### 自我检查：设计技能  
- [ ] 名称是否符合规范（小写，使用连字符）？  
- [ ] 描述中是否包含了明确的触发条件？  
- [ ] 我知道需要包含哪些资源吗？  

---

## 第三步：编写技能文档  

### SKILL.md 模板  

请使用以下模板来编写你的技能文档：  

```yaml
---
name: my-skill
description: "[What it does]. Use when: (1) [trigger 1], (2) [trigger 2], (3) [trigger 3]."
---

# My Skill

## When This Skill Activates
This skill triggers when user wants to [capability].

## The [Domain] Framework

| Step | Action |
|------|--------|
| 1 | [What to do] |
| 2 | [What to do] |
| 3 | [What to do] |

## Workflow

### Step 1: [Name]
[What to do and why]

### Step 2: [Name]
[What to do and why]

### Decision Point
- If [condition]: do [A]
- If [condition]: do [B]

## Common Scenarios

### Scenario 1: [Case]
[What to do]

### Scenario 2: [Case]
[What to do]

## Troubleshooting

### Problem: [Error]
- Cause: [why]
- Fix: [how]

## Quick Reference

| Task | Action |
|------|--------|
| [Task 1] | [Command/Step] |
| [Task 2] | [Command/Step] |
```  

### 内容模板  

| 模板类型 | 适用场景 |  
|---------|---------|  
| 分步说明 | 顺序性工作流程 |  
| 决策树 | 分支逻辑 |  
| 表格 | 快速参考 |  
| 代码块 | 示例代码 |  
| 错误处理 | 故障排除指南 |  

### 逐步披露信息  

```
IN SKILL.MD (< 500 lines):
├── Core workflow (must-know)
├── Key examples (most common)
└── Quick reference

IN REFERENCES/:
├── Detailed documentation
├── API specs
├── Edge cases
└── Extended examples
```  

### 自我检查：编写文档  
- [ ] 前言部分（技能名称+描述）是否完整？  
- [ ] 正文部分是否包含了推理框架？  
- [ ] 是否包含了自我检查提示？  
- [ ] 资源是否被正确组织？  

---

## 第四步：测试技能  

### 测试触发条件  

阅读你的技能描述，并尝试使用它：  

```
Description: "[your description]"

Would this match user saying:
- "[trigger phrase 1]"? → YES/NO
- "[trigger phrase 2]"? → YES/NO
- "[trigger phrase 3]"? → YES/NO
```  

### 自我检查：测试技能  
- [ ] 描述是否与用户常用的表达方式一致？  
- [ ] 用户能否通过搜索找到这个技能？  
- [ ] 是否有清晰的步骤可供遵循？  
- [ ] 是否包含了错误处理机制？  

---

## 第五步：优化技能  

### 优化循环  

```
Use the skill → Notice issues → Fix → Use again
    ↑                                    │
    └────────────────────────────────────┘
```  

### 常见问题及解决方法  

| 问题 | 解决方案 |  
|---------|----------|  
| 技能无法被触发 | 添加更多“适用于……”的触发条件 |  
| 文档太长 | 将详细信息移至参考资料中 |  
| 内容难以理解 | 添加示例场景 |  
| 缺少某些使用场景 | 添加故障排除部分 |  

### 自我检查：优化技能  
- [ ] 是否在实际任务中测试过技能？  
- [ ] 是否考虑了用户反馈？  
- [ ] 技能是否已经准备好日常使用？  

---

## 版本管理指南  

### 何时升级版本  

| 版本变更类型 | 升级版本号 | 例子 |  
|------------|--------------|---------|  
| 修复漏洞（无新功能） | 1.0.0 → 1.0.1 | v1.0.1 |  
| 添加新功能（向后兼容） | 1.0.1 → 1.1.0 | v1.1.0 |  
| 引入破坏性变更 | 1.1.0 → 2.0.0 | v2.0.0 |  

### 日志格式  

```markdown
## Version 1.1.0

### Added
- New feature X

### Changed
- Improved Y

### Fixed
- Bug Z
```  

### 自我检查：版本管理  
- [ ] 版本号是否正确递增？  
- [ ] 日志是否更新？  
- [] 这次升级是否属于破坏性变更？  

---

## 元数据最佳实践  

### 前言部分的内容  

```yaml
---
name: my-skill
description: "[What it does]. Use when: (1) [trigger 1], (2) [trigger 2]."
version: 1.0.0
changelog: "[Brief summary of changes]"
metadata:
  clawdbot:
    emoji: "🔨"           # Emoji for the skill
    category: "creation"  # Category (research/coding/utility/etc)
    requires:
      bins: ["curl"]      # Required system binaries
      python: ["requests"] # Optional Python packages
---
```  

### 表情符号选择  

| 类别 | 表情符号 | 适用场景 |  
|----------|-------|----------|  
| 研究 | 🔬 | 深度研究、论文比较 |  
| 编程 | 💻 | 代码 |  
| 创建 | 🔨 | 技能构建 |  
| 实用工具 | ⚡ | 功能工具 |  
| 天气 | 🌤️ | 天气信息 |  
| 发现新技能 | 🔍 | 技能搜索 |  
| 媒体 | 🎞️ | 视频素材 |  
| 文件处理 | 📄 | 文件操作 |  

### 类别标签  

| 类别 | 适用场景 |  
|----------|-------------|  
| 研究 | 研究、分析、数据对比 |  
| 编程 | 代码相关任务 |  
| 实用工具 | 工具、下载、文件操作 |  
| 创建新功能 | 构建新内容 |  
| 通信 | 消息传递、通知 |  
| 媒体 | 视频、音频、图片 |  

### 需求信息  

```yaml
metadata:
  clawdbot:
    requires:
      bins: ["ffmpeg", "curl"]       # System binaries
      python: ["requests", "pandas"] # Python packages
      node: ["typescript"]           # Node packages
    os: ["linux", "darwin", "win32"] # Supported OS
```  

### 自我检查：元数据  
- [ ] 前言部分是否完整？  
- [ ] 选择的表情符号是否适合该类别？  
| [ ] 是否列出了所有需求？  
| [ ] 版本号是否正确？  

---

## 质量评估  

评估你的技能：  

| 评估因素 | 评分 | 备注 |  
|--------|-------|-------|  
| **触发条件的清晰度** | |  
| - 是否有 3 个或更多明确的触发条件？ | ⭐⭐⭐ |  
| - 只有 1-2 个触发条件？ | ⭐⭐ |  
| - 表达模糊或缺失？ | ⭐ |  
| **结构** | |  
| - 是否包含推理框架？ | ⭐⭐⭐ |  
| | 是否有工作流程步骤？ | ⭐⭐ |  
| | 缺乏结构？ | ⭐ |  
| **决策树** | |  
| - 是否有多个决策点？ | ⭐⭐⭐ |  
| | 只有一个决策点？ | ⭐⭐ |  
| | 无决策树？ | ⭐ |  
| **自我检查机制** | |  
| | 每个关键步骤都配有检查项？ | ⭐⭐⭐ |  
| | 部分步骤有自我检查？ | ⭐⭐ |  
| | 无自我检查？ | ⭐ |  
| **示例代码** | |  
| | 是否包含可运行的示例？ | ⭐⭐⭐ |  
| | 仅使用模板？ | ⭐⭐ |  
| | 无示例代码？ | ⭐ |  
| **元数据** | |  
| | 是否完整（包括表情符号、类别、需求信息）？ | ⭐⭐⭐ |  
| | 部分缺失？ | ⭐⭐ |  
| | |  
| **质量评分** | |  
| | 总分：[评分范围：15-18] |  
| | 15-18 分：优秀，可直接发布 |  
| | 10-14 分：良好，需要改进 |  
| | 5-9 分：需要大幅改进 |  
| | |  

### 自我检查：质量评估  
- [ ] 是否计算出了总分？ |  
| | 分数低于 10 分？发布前需要改进 |  

---

## 为什么这种方法有效  

### 技能逻辑模式  

根据 SkillsBench 2026 的研究：  
1. **推理框架**：让智能体知道“如何思考”，而不仅仅是“做什么”  
2. **决策树**：使智能体能够处理不同的场景  
3. **自我检查**：确保智能体的行为正确  
4. **逐步披露信息**：提高使用效率  

### 适度的复杂性原则  

> “2-3 个专注的模块比冗长的文档更有效”  

遵循以下原则：  
- ✅ 内容足够完整，实用性强  
- ✅ 表达简洁，易于理解  
- ✅ 结构清晰，能指导用户使用  

---

## 示例：创建天气查询技能  

### 第一步：理解需求  
- **功能**：从 wttr.in 获取天气数据  
- **触发条件**：“[城市]的天气”，“温度”，“天气预报”  
- **应用领域**：天气数据  

### 第二步：设计技能  
- **难度**：简单（仅涉及 API 调用）  
- **文档格式**：使用 SKILL.md  
- **技能名称**：`weather`  

### 第三步：编写技能文档  

```yaml
---
name: weather
description: "Get weather data. Use when: (1) User asks weather, (2) User wants forecast, (3) User asks temperature."
---

# Weather

## Reasoning

1. EXTRACT → Location from request
2. FETCH → Call wttr.in API
3. PARSE → Extract temp, conditions
4. PRESENT → Format for user
```  

### 第四步至第五步：测试与优化  
- 添加更多触发条件（如“天气晴朗吗？”、“下雨吗？”）  
- 添加错误处理机制（例如输入错误的城市地址或网络问题）  
- 添加展示模板（如天气预报的可视化格式）  

---

## 为什么这种方法有效  

根据 SkillsBench 2026 的研究，具有推理框架的技能表现更好，因为它们为智能体提供了思考的框架，而不仅仅是简单的操作步骤。  

*使用技能构建工具 🔨 制作了这个文档*