---
name: podcast
version: 1.0.1
description: >
  自动发现、研究、编写脚本、核实事实，并生成播客剧集。  
  支持多源主题搜索，利用大型语言模型（LLM）生成脚本，确保内容引用正确；同时集成 ElevenLabs 的文本转语音（TTS）技术。  
  完全不依赖任何特定供应商——兼容任何 RSS 源、S3 存储服务或本地存储。
---
# 播客发现与生成

这是一个自动化的全端播客制作流程，能够从可配置的来源中发现热门话题，深入研究这些话题，生成经过事实核查的脚本，并通过 ElevenLabs 的文本转语音（TTS）技术生成音频。

## 触发条件

当用户请求以下操作时，可以使用此技能：
- “生成一个播客”
- “制作一集播客”
- “发现播客主题”
- “创建关于某个主题的音频节目”
- “寻找播客主题”
- “研究并编写播客脚本”
- “制作一集播客”

## 快速入门

### 1. 配置
```bash
cd ~/.openclaw/skills/podcast
cp config.example.yaml config.yaml
# Edit config.yaml: add sources, interests, voice, storage
```

### 2. 发现主题
```bash
python3 scripts/discover.py --config config.yaml --limit 10
```

### 3. 运行流程
```bash
python3 scripts/pipeline.py --config config.yaml --topic "Your Topic" --mode manual
```

## 配置

**最小配置文件（config.yaml）:**
```yaml
sources:
  - type: rss
    url: https://aeon.co/feed.rss
    name: Aeon
  - type: hackernews
    min_points: 200

interests:
  - AI/Tech
  - Science

voice:
  voice_id: "<your-voice-id>"

storage:
  type: local
  path: ./output
```

**存储选项:**
- `type: s3` — 上传到 S3（需要指定 bucket 和区域）
- `type: local` — 保存到本地目录

## 流程阶段

1. **发现** — 从来源获取并排名主题
2. **研究** — 使用 OpenClaw 进行网络搜索
3. **编写脚本** — 利用大型语言模型（LLM）生成脚本，并添加引用 `[Source: URL]`
4. **验证** — 核对引用内容与研究来源是否一致
5. **音频处理** — 去除引用信息，并调用 ElevenLabs 的 TTS 服务生成音频
6. **上传** — 保存到 S3 或本地存储

每个阶段可以独立运行，也可以作为完整流程一起运行。

## 使用示例

**仅发现主题:**
```bash
python3 scripts/discover.py --config config.yaml --limit 5 --output topics.json
```

**全流程（自动模式）:**
```bash
python3 scripts/pipeline.py --config config.yaml --mode auto
```

**特定主题:**
```bash
python3 scripts/pipeline.py --config config.yaml --topic "AI Reasoning" --mode manual
```

**从某个阶段恢复执行:**
```bash
python3 scripts/pipeline.py --config config.yaml --resume-from audio
```

## 源类型

**内置来源:**
- `rss` — 通用的 RSS/Atom 源（任何 URL）
- `hackernews` — HN API（支持筛选特定类型的内容）
- `nature` — Nature 杂志（涵盖新闻、研究、生物技术、医学等领域）

**添加自定义 RSS 源:**
```yaml
sources:
  - type: rss
    url: https://yourfeed.com/rss
    name: Your Source
    category: Your Category
```

## 输出文件**

```
output/
├── discovery-YYYY-MM-DD.json      # Ranked topics
├── research-YYYY-MM-DD-slug.json  # Research data
├── script-YYYY-MM-DD-slug.txt     # Script with citations
├── verification-YYYY-MM-DD.json   # Fact-check report
├── tts-ready-YYYY-MM-DD-slug.txt  # Clean text for TTS
├── episode-YYYY-MM-DD-slug.mp3    # Final audio
└── pipeline-state-YYYY-MM-DD.json # Pipeline state
```

## 与 OpenClaw 的集成

**用于发现阶段:** 直接运行（无需额外工具）

**用于完整流程:** 使用以下命令启动 OpenClaw 工作进程:
- `web_search()` — 执行搜索阶段
- `llm_access` — 用于生成脚本（推荐使用 Claude Sonnet）
- `elevenlabs_text_to_speech` — 用于生成音频

**工作进程模式:**
```bash
cd ~/.openclaw/skills/podcast
# Source environment if available
[ -f ~/.openclaw/env-init.sh ] && source ~/.openclaw/env-init.sh
python3 scripts/pipeline.py --config config.yaml --mode auto
```

## 引用要求

脚本中的每个事实性陈述都必须附带 `[Source: URL]` 的引用：

✅ **正确示例:**
```
The market grew to $10.2 billion in 2025 [Source: https://example.com/report].
```

❌ **错误示例:**
```
The market grew significantly.
```

验证脚本会检查引用内容是否与研究来源一致；如果发现未验证的陈述，将阻止音频生成。

## 定时任务集成

**每日自动发现:** 每天上午 8 点
```yaml
schedule: "0 8 * * *"
payload: |
  cd ~/.openclaw/skills/podcast
  python3 scripts/discover.py --config config.yaml --limit 10 \
    --output data/discovery-$(date +%Y-%m-%d).json
```

**每周完整流程:** 每周运行一次

## 主要特点

✅ **无供应商锁定** — 可使用任何 RSS 源和存储方式
✅ **无外部依赖** — 仅使用 Python 标准库（TTS 需要 ElevenLabs 的支持）
✅ **引用要求** — 每个陈述都必须有来源
✅ **事实核查** — 对所有内容进行核实
✅ **可扩展的来源配置** — 可轻松添加新的主题来源
✅ **恢复执行** — 可从任何阶段重新开始流程
✅ **手动或自动执行** — 可选择手动审查每个阶段或直接运行整个流程

## 故障排除

**未找到主题:**
- 确保 RSS URL 是有效的
- 核对用户兴趣与来源内容是否匹配
- 适当降低 Hacker News 的最低评分阈值（`min_points`）

**验证失败:**
- 确保 `research.json` 文件中包含来源信息
- 检查脚本中是否包含 `[Source: URL]` 引用
- 确保 URL 与研究来源一致

**S3 上传失败:**
- 验证 AWS 凭据是否正确
- 确认 bucket 存在且区域设置正确
- 确保 bucket 的权限设置允许公开访问

## 相关文件

- `SKILL.md` — 本文档文件
- `README.md` — 详细使用说明
- `config.example.yaml` — 配置模板文件
- `scripts/` — 流程脚本目录
- `sources/` — 源数据实现文件
- `templates/` — 提示语模板文件

## 许可证

MIT 许可证 — 这是一项开源项目，由社区维护。