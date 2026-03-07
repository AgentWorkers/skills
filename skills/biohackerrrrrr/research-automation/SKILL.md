---
name: research-automation
description: 自动化网络搜索工具，专注于肽类化合物、生物黑客技术（biohacking protocols）、长寿科学（longevity science）以及热门健康话题的相关信息。适用于需要发现新信息、追踪新兴趋势、监测科学进展，或基于现有研究生成内容创意的场景。该工具可通过定时任务（heartbeat）或按需（on-demand）的方式运行。
---
# 研究自动化

这是一个自动化研究系统，用于在网络上搜索肽类、生物黑客技术、长寿研究以及热门健康话题的最新进展。

## 功能概述

- **网络搜索**：从多个来源查询最新的研究结果、实验方案和行业趋势。
- **内容整理**：按主题对搜索结果进行筛选和分类。
- **洞察生成**：提取有价值的见解和内容创意。
- **自动保存**：将研究内容以结构化的Markdown格式保存，便于后续查阅。

## 涵盖的主题

1. **肽类**：新型肽类、临床研究、使用方案、剂量更新。
2. **生物黑客技术**：新兴技术、技术组合、优化方法。
3. **长寿科学**：衰老研究、干预措施、生物标志物、临床试验。
4. **热门话题**：与健康相关的热门话题、争议性话题、社会趋势变化。

## 使用方式

### 定制研究

运行特定的研究查询：

```
Run research on [topic] - focus on [specific angle]
```

示例：
```
Run research on GLP-1 peptides - focus on recent clinical trials and dosing protocols
```

### 定时研究（自动循环）

该系统会通过自动循环的方式定期执行研究任务，涵盖以下主题：
- 肽类（每周一次）
- 生物黑客技术（每周两次）
- 长寿研究（每周一次）
- 热门话题（每天一次）

## 输出格式

研究结果会被保存在 `research/[主题]/[日期].md` 文件中：

```markdown
# [Topic] Research - [Date]

## Key Findings

1. **[Finding Title]**
   - Source: [URL]
   - Key Insight: [1-2 sentence summary]
   - Actionable: [What you can do with this]
   - Content Angle: [How to turn this into content]

2. **[Next Finding]**
   ...

## Trending Discussions

- [Topic]: [Summary of discourse]
- [Topic]: [Summary of discourse]

## Content Ideas Generated

1. [Tweet/thread angle]
2. [LinkedIn post angle]
3. [Article angle]

## Sources Reviewed

- [Source 1]
- [Source 2]
...
```

## 搜索策略

- **构建查询**：针对每个研究主题构建3-5个针对性的搜索查询。
- **来源多样性**：结合学术、临床和实践类资源。
- **时间筛选**：优先显示过去30天内的内容（可配置）。
- **信息筛选**：区分新颖信息与重复内容。
- **内容转化**：将搜索结果转化为适合发布到社交媒体（如Twitter）的创意。

## 与内容创作的集成

研究结果会直接用于生成以下内容：
- `content/biohacker-angles-[日期].md`（Twitter相关内容）
- `content/tokuflow-angles-[日期].md`（Nattokinase相关内容）
- `notes/research-insights/`（深度研究参考资料）

## 按主题分类的搜索查询

### 肽类
- “2026年的新型肽类”
- “GLP-1肽类的临床试验”
- “肽类在生物黑客技术中的应用”
- “BPC-157的最新研究”
- “胸腺素β-4的相关研究”

### 生物黑客技术
- “2026年的生物黑客技术方案”
- “创始人健康优化方法”
- “认知增强技术”
- “代谢优化方法”
- “血液检测优化方案”

### 长寿研究
- “2026年的衰老研究”
- “长寿干预措施及临床试验”
- “senolytics的最新研究”
- “雷帕霉素与长寿的关系”
- “NAD+与衰老的关系”

### 热门话题
- “Twitter上的健康相关话题”
- “生物黑客技术的争议”
- “关于肽类的讨论”
- “2026年的长寿话题辩论”

## 筛选标准

- **包含内容**：
  - 新颖的研究成果（未被广泛报道的）
  - 有科学依据的内容
  - 可实际应用的研究方案
  - 有争议或值得讨论的话题
  - 提供不同观点的见解

- **排除内容**：
  - 通用的健康建议
  - 重复的信息
  - 未经同行评审的、缺乏合理依据的声明
  - 仅基于猜测的内容

## 最佳实践

- **在内容创作前进行搜索**：新颖的见解有助于产生更好的创意。
- **每周查看总结**：跟踪行业趋势和变化。
- **跨主题关联**：将不同主题的研究结果相互关联（例如：肽类与长寿研究）。
- **归档重要成果**：将具有突破性的研究成果保存到 `notes/research-insights/` 目录中。

## 手动研究流程

当需要针对特定主题进行深入研究时：

1. **指定研究主题和方向**：
   ```
   Research [topic] with focus on [specific angle] - find clinical backing and protocols
   ```

2. **查看搜索结果**：
   - 查看 `research/[主题]/[日期].md` 文件
   - 评估信息的价值与干扰因素
   - 如有需要，可要求进一步优化结果。

3. **生成内容**：
   ```
   Turn the [specific finding] into 5 tweet angles
   ```

## 定时研究功能的配置

若要启用定时研究功能，请在 `HEARTBEAT.md` 文件中进行相应配置：

```markdown
### 8. Research Automation - Peptides (Priority: Medium)
- Run research-automation skill for peptides
- Focus: New compounds, clinical studies, protocols
- Save to `research/peptides/[date].md`
- Frequency: Once per week

### 9. Research Automation - Trending (Priority: High)
- Run research-automation skill for trending topics
- Focus: Viral health content, debates, controversies
- Save to `research/trending/[date].md`
- Frequency: Daily
```

## 输出文件的存放位置

```
workspace/
├── research/
│   ├── peptides/
│   │   └── 2026-02-05.md
│   ├── biohacking/
│   │   └── 2026-02-05.md
│   ├── longevity/
│   │   └── 2026-02-05.md
│   └── trending/
│       └── 2026-02-05.md
└── notes/
    └── research-insights/
        └── breakthrough-findings.md
```

## 提高使用效率的建议

- **每天搜索热门话题**：及时捕捉社会趋势变化。
- **每周搜索学术性话题**：避免信息过载。
- **在内容规划时参考搜索结果**：这是获取新颖创意的最佳来源。
- **跨主题整合研究结果**：例如结合肽类与长寿研究，可以产生独特的视角。
- **归档重要成果**：将具有突破性的研究成果永久保存。

---

**创建时间：** 2026-02-05  
**最后更新时间：** 2026-02-05