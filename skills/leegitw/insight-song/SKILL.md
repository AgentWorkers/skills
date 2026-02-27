---
name: insight-song
version: 1.0.1
description: 将技术洞察转化为适合在 Suno 平台上发布的歌曲，包括歌词、风格标签以及情感线索。
author: Live Neon <hello@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/creative/insight-song
repository: leegitw/insight-song
license: MIT
tags: [creative, songwriting, suno, lyrics, music, synthesis, reflection, learning, technical-writing]
layer: creative
status: active
alias: song
user-invocable: true
emoji: 🎵
---
# insight-song（歌）

将技术对话和见解转化为适合Suno.ai使用的歌曲形式。  
生成的歌词会包含情感脉络，反映技术发展的过程，并附带风格标签和章节标记。  

**触发条件**：明确请求（explicit invocation）或当出现深刻的技术见解时  

**核心理念**：“创造力源于综合。用歌曲来表达某个概念，能揭示被动理解所无法发现的问题。”  

## 安装  
```bash
openclaw install leegitw/insight-song
```  

**依赖项**：无（独立创作技能）  

**数据处理**：该技能会从用户提供的输入或当前对话上下文中合成内容（默认）。它不会从工作区读取文件或直接访问项目文件。结果会返回给调用它的代理，由代理决定如何使用这些内容。  

## 功能说明  
技术见解容易随着上下文的压缩而被人遗忘。歌曲通过音频形式强化这些见解，使概念更易于记忆和传播。该技能能够：  
1. **将技术对话转化为连贯的故事**；  
2. **将抽象概念转化为具有视觉意象的歌词**；  
3. **将输出格式化为适合在Suno.ai中使用的形式**。  

**技术原理**：通过隐喻和情感脉络来传达技术原理，比单纯的文档更有效。  

## 使用方法  
```
/song [topic]
```  

## 参数说明  
| 参数 | 是否必填 | 说明 |  
|---------|---------|-------------|  
| 主题（Topic） | 否 | 话题焦点（默认：合成当前对话内容） |  

## 使用前准备  
在创作歌曲之前，请确保：  
1. **对话有足够的深度**——表面层次的总结无法创作出好的歌曲；  
2. **有清晰的叙事脉络**——问题 → 发现 → 解决方案 → 影响；  
3. **主要工作已完成记录**——如果任务中途，请先保存当前进度。  

### 上下文理解检查清单  
你需要能够回答以下问题：  
| 问题 | 含义 |  
|---------|---------------|  
| 核心见解是什么？ | 不仅仅是“我们讨论了X”，而是“我们发现X可以解决Y”；  
| 问题是否得到解决？ | 不仅仅是讨论了问题本身，还包括问题产生的原因；  
| 为什么这样做，而不仅仅是结果如何？ | 包括背后的理由；  
| 是否有足够的深度？ | 能够传授新的知识，而不仅仅是常规做法。  

### 需避免的情况  
- 对话的简单总结；  
- 不理解做出某个决策的原因；  
- 领悟仅仅是常规做法；  
- 没有清晰的叙事脉络；  
- 含糊不清的歌词（可能适用于多种情况）。  

## 输出格式  
### Suno.ai歌曲格式  
```markdown
## Song

**Title**: [Song Name]

**Suno.ai Style Tags**:
[300-500 characters describing musical style, mood, instrumentation]

[Verse 1]
[Lyrics conveying the problem/pain]

[Chorus]
[Core message, repeatable, memorable]

[Verse 2]
[Discovery/insight]

[Bridge]
[Technical depth through metaphor]

[Chorus]

[Outro]
[Resolution/call to action]
```  

### 歌曲创作规则  
| 规则 | 说明 |  
|------|-------------|  
| 有完整的故事结构**：开头、中间和结尾要有清晰的脉络；  
| 技术内容但易于演唱**：不要为了押韵而牺牲准确性；  
| 包含视觉意象**：适合音频和视觉的双重强化；  
| 情感脉络与技术过程相匹配**；  
**避免使用具体细节**：使用隐喻和象征，而非文件名或指标；  
**不使用艺术家名称**：提取核心内容，而非具体引用。  

### 示例：好的歌词 vs 不好的歌词  
**不好的歌词（过于直白）：**  
```
We fixed the bug in handler.go
The timeout was set to 300
```  
**好的歌词（使用隐喻）：**  
```
Three in the morning, the logs are all silent
System's on fire but the metrics don't know
Building in darkness, no baseline to measure
Can't debug what you've never seen before
```  

## 核心逻辑  
### 第一步：合成对话内容  
- 阅读完整的对话内容；  
- 确定关键决策和“顿悟”时刻；  
- 提取核心见解或模式。  

### 第二步：构建叙事脉络  
| 元素 | 问题 |  
|---------|----------|  
| 问题 | 什么出了问题/带来了困扰？ |  
| 发现 | 我们学到了什么？ |  
| 解决方案 | 出现了什么模式？ |  
| 影响 | 这为什么重要？ |  

### 第三步：创作歌曲  
**结构（灵活）**：  
- 引言：介绍问题/背景；  
- 第一段：问题/现状；  
- 第二段：发现/见解；  
- 过渡段：通过隐喻深入解释技术细节；  
- 合唱部分：核心信息（重复性强，易于记忆）；  
- 结尾：解决方案/行动号召。  

### 第四步：格式化输出  
- 添加歌曲标题；  
- 编写300–500个字符的风格标签；  
- 添加章节标记：`[第一段]`、`[合唱部分]`、`[过渡段]`等。  

### 示例  
**输入：关于Bootstrap可观测性的见解**  
**背景**：发现了可以通过重现来调试的问题；介绍了Bootstrap工具 → 学习了如何使用它 → 强化了使用步骤。  
**叙事脉络**：  
- **问题**：没有重现功能的话，调试是不可能的；  
- **发现**：全新的系统不知道“正常状态”是什么；  
- **解决方案**：使用Bootstrap工具 → 学习相关流程 → 强化调试步骤；  
- **影响**：借助可视化手段进行调试，而非在黑暗中摸索。  

### 输出结果  
**歌曲标题**：**Bootstrap Before You Break**  
**Suno.ai风格标签**：  
```
Atmospheric indie folk with building intensity, finger-picked acoustic guitar opening,
gradually adding warm synth pads and driving drums, introspective male vocals with
occasional harmonies, dynamic shifts between quiet verses and powerful choruses,
ethereal reverb on bridge section, cinematic crescendo finale
```  
```
[Verse 1]
Three in the morning, the logs are all silent
System's on fire but the metrics don't know
Building in darkness, no baseline to measure
Can't debug what you've never seen before

[Chorus]
Bootstrap before you break
Learn the patterns while you wait
Enforce what the data shows
Now you see where the failure goes

[Verse 2]
Started collecting every signal
Cast the net wide, caught it all
Fourteen days of patient watching
Now we know what normal's called
```  

## 集成方式  
- **所属类别**：创意技能；  
- **依赖项**：无（独立使用）；  
- **适用场景**：辅助任务（与其他技能结合使用）；  
- **互补技能**：视觉概念表达、技术演讲等。  

## 可能出现的错误情况  
| 条件 | 行为 |  
|-----------|----------|  
| 上下文信息不足 | 先询问更多细节；  
- 没有清晰的叙事脉络 | 拒绝创作，并说明缺失的部分；  
- 主题过于肤浅 | 建议先进行更深入的探索。  

## 安全注意事项  
**输入来源**：  
- 用户提供的内容（如果有的话）；  
- 当前对话内容（默认）。  

**该技能不会执行以下操作**：  
- 从工作区读取文件；  
- 直接访问项目文件；  
- 将数据发送到外部服务；  
- 调用外部API。  

**输出行为**：  
该技能会将生成的歌曲直接返回给调用它的代理。代理可以展示、保存结果，或根据需要将其传递给其他技能。  

**来源说明**：  
该技能由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户发布在ClawHub平台上。开发者为同一人。  

## 质量检查标准：  
- 能够用一句话解释核心见解；  
- 能够说明背后的原因而不仅仅是结果；  
- 歌曲有完整的开头、中间和结尾；  
- 情感脉络与技术过程相匹配；  
- 避免使用具体细节（如文件名、指标等）；  
- 风格标签长度为300–500个字符；  
- 包含章节标记（[第一段]、[合唱部分]等）。  

**接受标准**：  
- 能够将输入内容或对话转化为适合Suno.ai使用的格式；  
- 输出包含歌曲标题、300–500个字符的风格标签和分段的歌词；  
- 歌词通过隐喻传达技术见解；  
- 情感脉络与技术过程相匹配；  
- 结果会返回给调用它的代理。  

*属于Live Neon创意套件的一部分。*