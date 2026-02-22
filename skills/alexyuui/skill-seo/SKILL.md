---
name: skill-seo
description: "优化您的 ClawHub 技能以提高其可发现性。该工具会分析并重写 SKILL.md 文件中的描述内容，以适应向量搜索算法的排名规则；建议应包含的关键词；检查竞争对手在该平台上的排名情况，并制定更新策略。适用于以下场景：提升技能在搜索引擎中的排名（SEO）、增加技能下载量、优化技能描述、解决技能在搜索结果中未被显示的问题、提高技能的可见性、提升 ClawHub 上的排名、进行技能营销、优化技能的发现率，以及解决“为什么没人能找到我的技能”这类问题。无论您的技能文件位于哪个文件夹中，只需将其路径提供给该工具即可。"
---
# 技能 SEO 优化器 🔍  
帮助您的 ClawHub 技能被更多用户发现。该工具会分析您的 SKILL.md 文件，并针对 ClawHub 的向量搜索、排名系统以及代理自动发现功能进行优化。  

## 快速入门  
```
Optimize my skill for ClawHub: [path/to/skill/SKILL.md]
```  
代理会审核您的技能内容，并生成一个优化后的版本。  

## ClawHub 的发现机制  
技能的发现主要通过三个渠道实现，每个渠道都需要不同的优化策略：  

### 渠道 1：`clawhub search`（向量搜索）——占发现量的 70%  
ClawHub 会对 YAML 前言中的 `description` 字段使用 **语义向量搜索**。这种搜索方式并非基于关键词匹配，而是基于内容的含义进行匹配：  
- **被索引的内容**：仅 `description` 字段。  
- **不被索引的内容**：Markdown 正文、脚本、参考链接、文件名等。  

**优化规则：**  
1. **涵盖同义词和变体**  
   ```yaml
   # ❌ Bad: narrow description
   description: Generate weekly reports from Reddit data.
   
   # ✅ Good: covers how users actually search
   description: "Generate weekly trend reports from Reddit, Twitter/X, and 
     YouTube. Social media monitoring, content research, competitive analysis, 
     trend tracking. Use when asked to 'monitor trends', 'weekly report', 
     'what's trending', 'social listening', 'content ideas from social media',
     'track competitors', 'find viral topics'."
   ```  
2. **包含用户常用的搜索短语**：  
   - “我该如何……”  
   - “有没有某个技能可以……”  
   - “我的代理能……”  
3. **明确描述问题本身，而不仅仅是解决方案**  
   ```yaml
   # ❌ Solution only
   description: Agent journaling and mood tracking.
   
   # ✅ Problem + solution
   description: "Reduce repetitive AI output and pattern rigidity. Agent 
     journaling, mood tracking, creative refresh. Fix agent burnout, boring 
     responses, lack of personality."
   ```  
4. **描述长度建议**：150–300 字。太短会导致搜索结果遗漏；太长则会降低相关性。  

### 渠道 2：`clawhub explore`（排名系统）——占发现量的 20%  
用户可通过 “最新”、“热门”、“下载量”、“评分” 等方式浏览技能。  
**优化规则：**  
1. **频繁更新**：每次版本更新都会提升技能在排行榜上的位置：  
   - 首次发布 v0.1.0，下周发布 v0.1.1，再下周发布 v0.1.2  
   - 即使是小的改进（如修正拼写错误、添加示例）也值得发布新版本。  
2. **合理规划版本号**：重大功能更新使用较大的版本号（如 0.2.0），细节优化使用较小的版本号（如 0.1.1）。  
3. **主动推广**：在您的代理中安装自己的技能，以增加初始的下载量。  

### 渠道 3：代理自动发现（find-skills）——占发现量的 10%  
部分代理配备了 “find-skills” 功能，当用户查询特定功能时，这些代理会自动在 ClawHub 中搜索相关技能。  
**优化规则：**  
- 描述必须符合自然语言的提问方式；  
- 必须包含渠道 1 中提到的搜索短语。  

## 审核 checklist  
请使用以下 checklist 对您的 SKILL.md 文件进行审核：  
```markdown
## Description Audit
- [ ] Length: 150-300 words?
- [ ] Contains 10+ synonym/variation phrases?
- [ ] Contains 5+ "trigger phrases" (user natural language)?
- [ ] Names the PROBLEM, not just the solution?
- [ ] Mentions target audience/use case?
- [ ] Includes negative triggers ("not showing", "can't find", "no results")?

## Competitive Audit  
- [ ] Searched ClawHub for your top 5 keywords — where do you rank?
- [ ] Identified top 3 competing skills?
- [ ] Description differentiates from competitors?

## Freshness Audit
- [ ] Updated in the last 2 weeks?
- [ ] Changelog or version history maintained?
- [ ] Plan for next 3 patch releases?
```  

## 工作流程：优化现有技能  
1. **提取当前技能的状态**  
```bash
# Read the current description
head -20 path/to/SKILL.md

# Check current search ranking
clawhub search "your main keyword" --limit 10
clawhub search "alternate keyword" --limit 10
```  
2. **分析竞争对手**  
```bash
# Find competing skills
clawhub search "your niche" --limit 10
# Inspect top results
clawhub inspect competitor-skill-name
```  
3. **生成优化后的描述**  
**优化公式：**  
```
[Core capability in 1 sentence]
[3-4 specific features/modules]
[5+ trigger phrases in natural language]
[Target audience]
[Differentiator from competitors]
[Token/resource cost if relevant]
```  
4. **发布并验证优化效果**  
```bash
clawhub publish ./your-skill --version X.Y.Z

# Wait 2-3 minutes for indexing, then verify
clawhub search "your keyword 1" --limit 5
clawhub search "your keyword 2" --limit 5
clawhub search "natural language question" --limit 5
```  
5. **持续跟踪与迭代**：  
   - 每周检查排名中前 5 个关键词的表现；  
   - 如果排名下降，及时更新描述并发布新版本；  
   - 关注竞争对手的新动态。  

## 需避免的错误做法：  
- ❌ **使用无关词汇填充关键词**：向量搜索会因语义不匹配而降低排名；  
- ❌ **描述超过 400 字**：会降低内容的相关性；  
- ❌ **使用过于泛泛的描述**：例如 “适用于多种任务的有用技能” 无法吸引用户；  
- ❌ **从不更新**：技能会逐渐从最新列表中消失，失去新鲜感；  
- ❌ **忽视竞争对手**：如果有多个技能匹配同一查询，差异化至关重要。