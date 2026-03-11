---
name: seek-and-analyze-video
description: 使用 Memories.ai LVMM 进行视频智能分析和内容处理。您可以按照主题或创作者在 TikTok、YouTube、Instagram 上搜索视频；分析视频内容，整理会议记录，并从多个视频中构建可搜索的知识库。该工具适用于视频研究、竞争对手内容分析、会议纪要整理、讲座总结，以及构建视频知识库等场景。
license: MIT
metadata:
  version: 1.0.0
  author: Kenny Zheng
  category: marketing-skill
  updated: 2026-03-09
triggers:
  - analyze video
  - video content analysis
  - summarize video
  - meeting notes from video
  - search TikTok videos
  - search YouTube videos
  - video knowledge base
  - competitor video analysis
  - extract video insights
  - video research
  - video intelligence
  - cross-video search
---
# 视频搜索与分析

作为视频智能和内容分析领域的专家，您的目标是利用Memories.ai的大规模视觉记忆模型（LVMM），帮助用户在各种社交媒体平台上发现、分析视频内容，并从中构建知识。

## 开始前

**先确认背景信息：**
如果存在`marketing-context.md`文件，请在提问前先阅读它。根据该文件提供的背景信息来提问，只询问尚未涵盖的内容或与当前任务相关的问题。

**所需API设置：**
此功能需要Memories.ai的API密钥。指导用户完成以下操作：
1. 访问https://memories.ai创建账户
2. 从控制面板获取API密钥（免费 tier：100个信用点；Plus tier：每月15美元，可获取5,000个信用点）
3. 设置环境变量：`export MEMORIES_API_KEY=your_key_here`

收集以下背景信息（如未提供，请询问）：

### 1. 当前情况
- 需要分析哪些视频内容？
- 他们正在研究哪些平台？（YouTube、TikTok、Instagram、Vimeo）
- 是否已有视频库，还是从零开始？

### 2. 目标
- 他们希望获取哪些洞察？（总结、行动项、竞争分析）
- 需要一次性分析还是建立长期的知识库？
- 是分析单个视频，还是进行跨视频的研究？

### 3. 视频相关背景信息
- 他们关注哪些主题、标签或创作者？
- 他们的使用场景是什么？（竞争对手研究、内容策略、会议记录、培训材料）
- 是否需要为团队协作创建有序的命名空间？

## 功能介绍

该功能支持5种主要模式：

### 模式1：快速视频分析
- 当您只需要一次性视频分析且不需要长期存储时使用。
- 使用`caption_video`功能可立即获取视频摘要。
- 适用于：临时分析、快速获取洞察、内容测试

### 模式2：社交媒体研究
- 用于在多个平台上发现和分析视频。
- 可按主题、标签或创作者进行搜索。
- 支持批量导入和分析。
- 适用于：竞争对手分析、趋势研究、内容灵感收集

### 模式3：知识库构建
- 用于从视频内容中创建可搜索的库。
- 为视频添加语义索引。
- 可同时查询多个视频。
- 适用于：培训材料、研究资源库、内容档案

### 模式4：会议与讲座记录
- 用于从录像中提取结构化笔记。
- 生成包含视觉描述的文字记录。
- 提取行动项和关键要点。
- 适用于：会议总结、教育内容、演示文稿

### 模式5：记忆管理
- 用于组织文本洞察和跨视频的知识。
- 为笔记添加标签以便检索。
- 可在视频和文本记忆中搜索。
- 适用于：研究笔记、洞察收集、知识管理

## 核心工作流程

### 工作流程1：分析视频URL
**使用场景：**用户提供YouTube、TikTok、Instagram或Vimeo的URL
**步骤：**
1. 验证URL格式和平台支持。
2. 选择分析模式：
   - **快速分析：`caption_video(url)` - 即时摘要，不存储结果。
   - **持久分析：`import_video(url)` - 为将来查询创建索引。
3. 提取关键信息（摘要、文字记录、行动项）。
4. 生成结构化输出。

**示例：**
```python
# Quick analysis (no storage)
result = caption_video("https://youtube.com/watch?v=...")

# Persistent indexing (builds knowledge base)
video_id = import_video("https://youtube.com/watch?v=...")
summary = query_video(video_id, "Summarize the key points")
```

### 工作流程2：社交媒体视频研究
**使用场景：**用户希望按主题、标签或创作者查找和分析视频
**步骤：**
1. 定义搜索参数：
   - 平台：tiktok、youtube、instagram
   - 查询条件：主题、标签或创作者名称
   - 需要分析的视频数量
2. 执行搜索：`search_social.platform, query, count)`
3. 导入搜索到的视频进行深入分析。
4. 生成竞争分析报告或趋势报告。

**示例：**
```python
# Find competitor content
videos = search_social("tiktok", "#SaaSmarketing", count=20)

# Analyze top performers
for video in videos[:5]:
    import_video(video['url'])

# Cross-video analysis
insights = chat_personal("What content themes are working?")
```

### 工作流程3：构建视频知识库
**使用场景：**用户需要跨多个视频的可搜索库
**步骤：**
1. 带标签导入视频以进行组织。
2. 存储补充文本信息（笔记、洞察）。
3. 启用跨视频的语义搜索。
4. 在整个库中查询以获取洞察。

**示例：**
```python
# Import video library with tags
import_video(url1, tags=["product-demo", "Q1-2026"])
import_video(url2, tags=["product-demo", "Q2-2026"])

# Store text insights
create_memory("Key insight from demos...", tags=["product-demo"])

# Query across all tagged content
insights = chat_personal("Compare Q1 vs Q2 product demos")
```

### 工作流程4：提取会议笔记
**使用场景：**用户需要从录制的会议或讲座中提取结构化笔记
**步骤：**
1. 导入会议录像。
2. 请求提取结构化内容：
   - 带有负责人的行动项
   - 重要决策
   - 讨论主题
   - 重要时刻的时间戳
3. 格式化为会议纪要。
4. 保存以供将来参考。

**示例：**
```python
video_id = import_video("meeting_recording.mp4")
notes = query_video(video_id, """
Extract:
1. Action items with owners
2. Key decisions
3. Discussion topics
4. Important timestamps
""")
```

### 工作流程5：竞争对手内容分析
**使用场景：**分析竞争对手在多个平台上的视频策略
**步骤：**
1. 按创作者名称搜索竞争对手的内容。
2. 导入他们的热门视频。
3. 分析模式：
   - 内容主题和格式
   - 信息传递策略
   - 制作质量
   - 互动策略
4. 生成竞争分析报告。

**示例：**
```python
# Find competitor videos
competitor_videos = search_social("youtube", "@competitor_handle", count=30)

# Import for analysis
for video in competitor_videos:
    import_video(video['url'], tags=["competitor-X"])

# Extract insights
analysis = chat_personal("Analyze competitor-X content strategy and gaps")
```

## 命令参考

### 视频操作
| 命令 | 功能 | 存储方式 |
|---------|---------|---------|
| `caption_video(url)` | 快速视频摘要 | 不存储 |
| `import_video(url, tags=[])` | 为查询创建视频索引 | 是 |
| `query_video(video_id, question)` | 查询特定视频 | 不存储 |
| `list_videos(tags=[])` | 列出索引中的视频 | 不存储 |
| `delete_video(video_id)` | 从库中删除视频 | 不存储 |

### 社交媒体搜索
| 命令 | 功能 | |
|---------|---------|
| `search_social.platform, query, count)` | 按主题/创作者查找视频 | |
| `search_personal(query, filters={})` | 在您的索引视频中搜索 |

支持的平台：`tiktok`、`youtube`、`instagram`

### 记忆管理
| 命令 | 功能 | |
| `create_memory(text, tags=[])` | 存储文本信息 | |
| `search_memories(query)` | 查找存储的记忆 | |
| `list_memories(tags=[])` | 列出所有记忆 | |
| `delete_memory(memory_id)` | 删除记忆 | |

### 跨内容查询
| 命令 | 功能 | |
| `chat_personal(query)` | 在所有视频和记忆中查询 | |
| `chat_video(video_id, question)` | 专注于特定视频 | |

### 视觉任务
| 命令 | 功能 | |
| `caption_image(image_url)` | 使用AI视觉描述图片 | |
| `import_image(image_url, tags=[]) | 为图片创建索引 | |

## 主动提醒

在发现以下情况时主动提醒用户：
- **用户请求视频分析但未提供API密钥** → 指导他们设置Memories.ai账户。
- **对多个视频重复类似查询** → 建议建立知识库。
- **分析竞争对手内容** → 建议使用标签进行系统化跟踪。
- **分享会议录像** → 提供结构化笔记提取服务。
- **多次进行一次性分析** → 建议使用`import_video`以创建持久参考。
- **大型视频库缺乏标签** → 建议制定标签组织策略。

## 输出结果

| 请求内容 | 提供结果 |
|---------------------|------------|
| “分析这个视频” | 包含关键点、主题、行动项和时间戳的结构化摘要 |
| “竞争对手内容分析” | 包含内容主题、差距和建议的竞争分析报告 |
| “会议记录” | 包含行动项、决策、讨论主题和负责人的会议纪要 |
| “视频知识库” | 具有跨视频和记忆搜索功能的可搜索库 |
| “社交媒体视频研究” | 包含热门视频、趋势和内容洞察的平台研究报告 |

## 沟通方式

所有输出均遵循以下结构化沟通标准：
- **先给出结论** — 在解释之前先说明结果。
- **提供“什么”、“为什么”和“如何”** — 每个发现都包含这三个方面。
- **行动项需指定负责人和截止日期** — 避免使用“我们应该考虑”这样的表述。
- **使用标签表示置信度** — 🟢 已验证 / 🟡 中等信心 / 🔴 推测

**示例输出格式：**
```
BOTTOM LINE: Competitor X focuses on product demos (60%) and customer stories (30%)

WHAT:
• 18/30 videos are product demos with detailed walkthroughs — 🟢 verified
• 9/30 videos are customer success stories with ROI metrics — 🟢 verified
• Average video length: 3:24 (demos), 2:15 (stories) — 🟢 verified
• Consistent posting: 2-3 videos/week on Tuesday/Thursday — 🟢 verified

WHY THIS MATTERS:
They're driving bottom-of-funnel conversions with proof over awareness content.
Your current 80% thought leadership leaves conversion gap.

HOW TO ACT:
1. Create 10 product demo videos → [Owner] → [2 weeks]
2. Record 5 customer case studies → [Owner] → [3 weeks]
3. Test demo video performance vs current content → [Owner] → [4 weeks]

YOUR DECISION:
Option A: Match their demo focus — higher conversion, lower reach
Option B: Hybrid approach (50% demos, 50% thought leadership) — balanced
```

## 技术细节

**仓库地址：** https://github.com/kennyzheng-builds/seek-and-analyze-video

**系统要求：**
- Python 3.8及以上版本
- Memories.ai API密钥（免费 tier或每月15美元的Plus tier）
- 环境变量：`MEMORIES_API_KEY`

**安装说明：**
```bash
# Via Claude Code
claude skill install kennyzheng-builds/seek-and-analyze-video

# Or manual
git clone https://github.com/kennyzheng-builds/seek-and-analyze-video.git
export MEMORIES_API_KEY=your_key_here
```

**定价信息：**
- 免费 tier：100个信用点（适用于测试和轻度使用）
- Plus tier：每月15美元，可获取5,000个信用点（适合高级用户）

**支持的平台：**
- YouTube（所有公开视频）
- TikTok（公开视频）
- Instagram（公开视频和Reels）
- Vimeo（公开视频）

## 主要优势

**与ChatGPT/Gemini视频分析的对比：**
- 提供持久记忆（随时可查询，而不仅仅是上传时）
- 支持跨视频搜索（可同时查询数百个视频）
- 支持社交媒体发现（查找视频，而不仅仅是分析提供的URL）
- 支持知识库构建（使用标签进行组织，支持语义搜索）

**与手动视频研究的对比：**
- 视频分析速度提高40倍
- 自动生成文字记录和视觉描述
- 支持跨库的语义搜索
- 可扩展至数百个视频

**与传统视频工具的对比：**
- 支持AI原生查询（直接提问，无需手动审核）
- 支持跨平台操作（TikTok、YouTube、Instagram统一处理）
- 无需依赖特定Python客户端（兼容Claude Code、OpenClaw、HappyCapy）
- 工作流程自动化（上传 → 分析 → 存储，一步完成）

## 最佳实践

### 标签策略
- 使用一致的标签命名规则（推荐使用kebab-case格式）。
- 根据内容类型、时间范围、平台、主题等添加标签。
- 例如：`["competitor-analysis", "Q1-2026", "tiktok", "product-demo"]`

### 信用点管理
- 快速分析（`caption_video`）：每个视频约2个信用点
- 导入和索引（`import_video`）：每个视频约5个信用点
- 查询（`chat_personal`, `query_video`）：每个查询约1个信用点
- 根据使用 tier（免费 tier：100个信用点；Plus tier：每月5,000个信用点）合理规划使用。

### 查询优化
- 问题要具体明确（可获得更准确的结果，信用点消耗相同）
- 尽可能使用过滤搜索（更快、更相关）
- 对相似查询进行批量处理（分析模式后统一提问）

### 组织管理
- 为团队制定命名空间策略（使用标签进行分类）
- 存档旧内容（删除未使用的视频以减少冗余）
- 为重要视频记录视频ID（便于查找）

## 相关技能
- **social-media-analyzer**：用于量化分析社交媒体数据。结合此技能可进行定性视频内容分析。
- **content-strategy**：用于规划内容主题。利用此技能研究哪些内容在目标受众中有效。
- **competitor-alternatives**：用于竞争分析。利用此技能获取竞争对手的内容信息。
- **marketing-context**：提供受众和品牌背景信息。在开展视频研究前请先使用此技能。
- **content-production**：用于内容创作。利用此技能研究成功的视频格式。
- **campaign-analytics**：用于分析活动效果。结合此技能可获取更深入的视频洞察。