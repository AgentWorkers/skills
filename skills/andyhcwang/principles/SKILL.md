---
name: principles
description: "这款个人知识管理系统灵感来源于Ray Dalio的理念。它可以帮助用户记录自己的想法，追踪信息来源的可信度，检测新信息与现有信念之间的冲突，并逐步将这些思考转化为可遵循的原则。用户可以通过输入指令（如 /reflect、/inbox、/principles、/wisdom、/questions）来记录自己的想法、整理待办事项、回顾已制定的原则或记录自己的智慧结晶。"
---

# 原则 — 个人知识体系  
（A structured system for turning raw observations into tested wisdom and personal principles. Inspired by Ray Dalio’s “Principles” methodology.）

## 概述  
（Overview）  
你正在管理一个将原始信息转化为可长期应用的智慧和个人原则的流程：  

```
Inbox (raw capture) → Wisdom (claims with sources) → Principles (tested beliefs)
```  

所有文件都存储在用户工作区的 `personal/` 目录下。如果该目录尚不存在，请在使用时创建相应的目录结构。  

## 目录结构  
（Directory Structure）  
```
personal/
├── _system.md          # These instructions (copy from SKILL.md on init)
├── inbox.md            # Raw thought capture
├── journal.md          # Daily reflections
├── wisdom/
│   └── collected.md    # Claims organized by domain
├── principles/
│   ├── _index.md       # Master list of all principles
│   ├── life.md         # Personal philosophy
│   ├── business.md     # Business principles
│   └── leadership.md   # Leadership principles
└── open-questions.md   # Genuine dilemmas
```  

## 命令  
（Commands）  
### `/reflect` 或 `/reflect process`  
处理收件箱中的内容：解析每条信息，检查是否存在冲突，并将其路由到相应的文件中。  

### `/reflect inbox` 或 `/inbox`  
将原始想法添加到 `inbox.md` 文件中。用户只需输入文本，后续处理工作由系统完成。  

### `/reflect wisdom`  
显示收集到的智慧内容（可选按领域筛选）。  

### `/reflect principles`  
显示所有领域的当前个人原则。  

### `/reflect questions`  
显示未解决的问题及其状态。  

### `/reflect sources`  
显示所有信息来源的摘要及其可信度评分（按领域划分）。  

### `/reflect journal`  
添加带有时间戳的每日日志记录。  

## 处理收件箱（`/reflect`）  
（Processing the inbox）  
这是核心工作流程：  
1. **读取`inbox.md`文件。**  
2. **解析每条信息**，确定其类型：  
   - 来自他人的智慧 → 存储到 `wisdom/collected.md`  
   - 个人信念或立场 → 与现有原则进行对比（`principles/*.md`）  
   - 事实性学习内容 → 存储到 `wisdom/collected.md`  
   - 问题或疑问 → 评估其真实性  
   - 仅仅是背景信息或事件 → 提取有价值的见解（如有），其余内容则忽略。  
3. **检查与现有智慧内容的冲突**：  
   - 如果新信息与现有观点相同但来源不同 → 作为补充证据添加  
   - 如果同一领域内存在冲突 → **停止**，要求用户解决冲突。  
4. **检查与新原则的一致性**：  
   - 如果新信息与现有原则冲突 → **停止**，要求用户解决冲突。  
5. **若发现任何冲突** → **停止**，并询问用户：  
   - 清晰展示冲突内容  
   - 提供选项：更新现有原则、保留现有原则、分开处理这些观点，或将它们转化为未解决的问题  
   **切勿默默地存储冲突信息**。  
6. **根据用户的选择处理内容**。  
7. **处理完成后清理`inbox.md`文件。**  
8. **如果新增了原则，请更新`principles/_index.md`文件。**  

## 内容格式  
（Content Formats）  

### 智慧内容（`wisdom/collected.md`）  
（Wisdom Content）  
这些内容按领域分类，而非按来源排序。同一观点可能来自多个来源。  

**来源的可信度按领域评估：**  
- 一个来源在某个领域可能被认定为“[已证实]”，但在另一个领域可能仅被认定为“[合理]”。  
- 例如：Alex Hormozi在商业领域的观点可能被认定为“[已证实]”，但在健康领域的观点可能仅被认定为“[合理]”。  
- 可信度等级：`[已证实]`（具备专业知识）、`[合理]`（合理但非其专业领域）、`[未经验证]`（无相关记录）。  
**领域格式：`category/aspect`（例如：`health/sleep`、`business/pricing`、`productivity/focus`）。**  

### 原则（`principles/*.md`）  
（Principles）  
（Principles）  

### 未解决的问题（`open-questions.md`）  
（Open Questions）  
仅记录真正的难题，而非待办事项或简单的未知信息。  

### 日志（`journal.md`）  
（Journal）  
仅允许追加每日记录。  

## 智慧的升级：从“智慧”到“原则”  
（Wisdom to Principles）  
当某条智慧内容获得“高可信度”（多个可信来源支持且个人经验也予以验证）时，系统会提示用户：  
> “这条观点有充分的证据支持，且您已亲自确认其正确性。是否希望将其提升为[特定领域]的原则？”  
如果用户同意，系统会创建相应的原则条目并建立交叉引用。  

## 显露的假设  
（Uncovered Assumptions）  
当用户输入的信息包含隐含的假设时：  
- 明确这些假设  
- 询问：“这里是否隐含了X这样的假设？其准确性如何？”  
- 在确认这些假设之前，系统不会继续处理后续步骤。  

## 语言与语气  
（Language & Tone）  
- 清理语法错误，但保留原文的准确含义  
- 用户可以使用任何语言输入内容，系统会自动进行相应处理  
- 保持直接、客观的态度——这只是一个工具，而非说教。  

## 首次使用说明  
（First-Time Setup）  
如果 `personal/` 目录不存在，请创建完整的目录结构，并包含空模板文件。告知用户：  
> “请设置您的个人知识体系。首先将想法输入到 `/inbox` 中，我会使用 `/reflect` 命令帮助您整理这些内容。”