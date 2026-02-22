---
name: skill-search
description: 使用关键词搜索、语义搜索或基于大型语言模型（LLM）的任务匹配功能来查找和检索可用的技能。当代理需要发现、搜索或智能地将技能与任务匹配时，可以使用这些功能。该系统支持混合搜索（BM25 + 语义搜索）、自然语言任务描述以及智能的技能推荐功能。
triggers:
  - "search skills"
  - "find a skill"
  - "what skills are available"
  - "skill for X"
  - "suggest skills for"
  - "what skill should I use"
  - "recommend a skill"
---
# 技能搜索 V1.1

通过关键词、语义匹配或 AI 驱动的任务匹配来查找所需技能。

## 概述

该功能提供了三种搜索模式：
1. **关键词搜索**（快速 BM25 算法）——匹配技能名称和描述
2. **语义搜索**（基于嵌入模型）——根据技能的含义或概念相似性进行查找
3. **LLM 任务匹配**（AI 驱动）——描述你的任务，获取技能推荐

## 使用场景

- **开始新任务前** — 检查是否存在相关技能
- **用户询问功能时** — “你能用 PDF 做什么？”
- **避免信息冗余** — 先找到合适的技能，再仅加载该技能
- **不确定适用哪种技能时** — 使用语义匹配或 LLM 进行模糊匹配

## 搜索模式

### 1. 关键词搜索（快速）
```bash
./scripts/skill_search.py keyword "weather"
./scripts/skill_search.py keyword "pdf"
./scripts/skill_search.py keyword "image generation"
```

### 2. 语义搜索（基于含义）
```bash
./scripts/skill_search.py semantic "automate web browsing"
./scripts/skill_search.py semantic "create images with AI"
./scripts/skill_search.py semantic "search my past conversations"
```

### 3. LLM 任务匹配（AI 驱动）
```bash
./scripts/skill_search.py suggest "I need to transcribe a podcast episode"
./scripts/skill_search.py suggest "Help me generate product photos"
./scripts/skill_search.py suggest "Search through my old emails"
```

### 4. 显示所有技能
```bash
./scripts/skill_search.py list
```

## 使用流程

1. **搜索**：根据需求（关键词/语义/LLM）查找技能
2. **预览**：阅读 SKILL.md 的元数据（描述、触发条件）
3. **加载**：如果找到合适的技能，阅读完整内容并执行

## 示例工作流程

**用户**：“我需要生成一些图片。”

**代理**：*使用语义搜索*
```bash
./scripts/skill_search.py semantic "generate images AI"
```

**输出**：
```
Top matches (semantic):
1. openai-image-gen (0.87) — Batch-generate images via OpenAI Images API
2. browser (0.65) — Control web browser via Playwright
```

**代理**：*阅读 SKILL.md，确认适用后执行*

---

**用户**：“我应该使用什么技能来转录音频？**

**代理**：*使用 LLM 进行推荐*
```bash
./scripts/skill_search.py suggest "transcribe audio"
```

**输出**：
```
Recommended skills for "transcribe audio":

1. openai-whisper-api — Transcribe audio via OpenAI Audio Transcriptions API (Whisper)
   Confidence: High
   Reason: Task explicitly matches skill purpose

2. sag — ElevenLabs text-to-speech (inverse operation, may be related)
   Confidence: Low
   Reason: Related to audio processing but output not input
```

## 搜索索引

技能搜索系统维护一个本地搜索索引，位于：
- `~/.openclaw/workspace/skills/skill-search/index/skills_index.json` — 技能元数据
- `~/.openclaw/workspace/skills/skill-search/index/embeddings.json` — 语义嵌入模型数据（按需加载）

**首次进行语义搜索时，索引会自动生成**。

**强制重新生成索引：**
```bash
./scripts/skill_search.py index
```

## 相关资源

### 脚本
- `skill_search.py` — 主要搜索接口（支持关键词/语义/LLM 模式）
- `indexer.py` — 构建/更新搜索索引
- `embeddings.py` — 生成嵌入模型数据（本地 miniLM）

### 目录结构
- `index/` — 可搜索的技能元数据
- `embeddings_cache.json` — 用于语义搜索的预计算嵌入模型数据