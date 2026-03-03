---
name: genviral
description: 完成 genviral Partner API 的自动化功能。能够创建并安排发布内容（包括视频和幻灯片）到 TikTok、Instagram 以及所有支持的平台。该功能涵盖幻灯片生成、文件上传、模板/包管理、数据分析，以及整个内容发布流程的自动化处理。
homepage: https://github.com/fdarkaou/genviral-skill
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["curl", "jq", "bash"]
---
# genviral 合作伙伴 API 技能

> **简而言之：** 将 genviral 的合作伙伴 API 包装成 50 多个 Bash 命令。核心流程如下：`get-pack` → 分析图片（元数据 + 视觉信息）→ 使用 `pinned_images` 生成内容 → `render` （渲染）→ 视觉审核 → `create-post` （创建帖子）→ 将日志记录到 `workspace/performance/log.json`。Studio AI 功能包括：`studio-models` → `studio-generate-image`（同步生成）或 `studio-generate-video`（异步生成）→ `studio-video-status --poll`（监控视频状态）。认证通过 `GENVIRAL_API_KEY` 进行。配置信息存储在 `defaults.yaml` 中，实例数据保存在 `workspace/` 目录下。

## 该技能的功能

- **多平台发布：** 可在 TikTok、Instagram、YouTube、Pinterest、LinkedIn、Facebook 等平台上发布视频或幻灯片内容。
- **Studio AI 生成：** 通过 API 使用 AI 模型生成图片（同步）和视频（异步）。
- **文件管理：** 将视频/图片上传到 genviral 的 CDN 服务器。
- **AI 幻灯片生成：** 根据用户提示生成照片轮播效果。
- **模板系统：** 提供可复用的幻灯片结构，并可将生成的图片转换为模板。
- **素材包管理：** 将图片素材包用作幻灯片的背景。
- **数据分析：** 提供关键绩效指标（KPIs）、帖子级别的统计数据、跟踪的账户信息以及更新触发条件。
- **细分市场研究：** 提供一键式研究服务（`trend-brief`），涵盖话题标签、音频素材、创作者信息、最佳发布时间等。
- **内容流程自动化：** 从用户提示到最终发布的全自动化流程。
- **性能监控：** 记录帖子发布情况、跟踪相关数据并定期进行性能评估。
- **内容创意库：** 维护并不断更新经过验证的内容创意库。

## 工作原理

1. 生成或上传媒体文件。
2. 创建针对一个或多个账户的发布内容。
3. 安排发布时间或立即发布（对于 TikTok 幻灯片，可以选择保存为草稿，以便在发布前添加热门音频；音乐选择需要人工判断以获得最佳效果）。
4. 通过数据分析工具跟踪发布效果。
5. 不断学习和优化发布策略。

所有配置信息都保存在 `defaults.yaml` 文件中，敏感信息通过环境变量进行管理。所有发布的内容都会显示在 Genviral 的仪表板上。

## 首次设置

如果是首次使用，请阅读 `docs/setup.md` 并按照文档中的步骤进行设置：
1. 设置 API 密钥并验证其有效性。
2. 列出目标账户并选择要发布内容的账户。
3. 商讨图片使用策略（使用现有素材包、新建素材包，或根据需要混合使用）。
4. （可选）设置产品背景信息和品牌风格。

没有硬编码的默认设置。根据用户需求进行调整。所有操作都会显示在 Genviral 的仪表板上，用户可以随时查看和控制所有内容。

## 文件结构

```
genviral/
  SKILL.md                  # This file (kernel + routing)
  README.md                 # Human-facing overview
  defaults.yaml             # API config and defaults

  docs/
    setup.md                # Onboarding guide (conversational, 5 phases)
    api/
      accounts-files.md     # accounts, upload, list-files
      posts.md              # create-post, update-post, retry, list, get, delete
      slideshows.md         # generate, render, review, update, regenerate, duplicate, list + text styles
      packs.md              # pack CRUD + smart image selection (MANDATORY reading for any pack workflow)
      templates.md          # template CRUD + create-from-slideshow
      analytics.md          # all analytics commands
      studio.md             # Studio AI: generate images/videos, list models, poll status
      subscription.md       # subscription status, credits, tier
      pipeline.md           # content pipeline, performance loop, CTA testing, platform tips
      errors.md             # error codes and troubleshooting
    references/
      analytics-loop.md     # Full analytics feedback loop and weekly review process
      competitor-research.md # How to research competitors
    prompts/
      slideshow.md          # Prompt templates for slideshow generation
      hooks.md              # Prompt templates for hook brainstorming

  workspace/                # All instance/customer data (override with GENVIRAL_WORKSPACE_DIR)
    content/
      scratchpad.md         # Working content plan and drafts
      calendar.json         # Upcoming planned posts
    context/
      product.md            # Product description, value props, target audience
      brand-voice.md        # Tone, style, do's and don'ts
      niche-research.md     # Platform research for the niche
    hooks/
      library.json          # Hook instances (grows over time, tracks performance)
      formulas.md           # Hook formula patterns and psychology
    performance/
      log.json              # CANONICAL post record (single source of truth)
      hook-tracker.json     # Hook and CTA tracking with metrics (the feedback loop)
      insights.md           # Agent learnings from performance data
      weekly-review.md      # Weekly review notes
      competitor-insights.md # Competitor research findings

  scripts/
    genviral.sh             # Main API wrapper (all commands)
    update-skill.sh         # Self-updater
```

## 命令路由

仅加载当前任务所需的文件：

| 任务 | 需要读取的文档 |
|------|------|
| 账户信息查询、文件上传 | `docs/api/accounts-files.md` |
| 帖子创建、更新、列表、删除 | `docs/api/posts.md` |
| 幻灯片生成、渲染、编辑、文本样式设置 | `docs/api/slideshows.md` |
| 素材包管理、图片选择（适用于任何素材包工作流程） | `docs/api/packs.md` |
| 模板创建和管理 | `docs/api/templates.md` |
| 数据分析查询和目标账户管理 | `docs/api/analytics.md` |
| Studio AI：生成图片/视频、查看模型列表 | `docs/api/studio.md` |
| 订阅信息：检查剩余信用、订阅等级、续订日期 | `docs/api/subscription.md` |
- 快速研究特定细分市场（趋势分析、竞争对手分析、创意素材） | `docs/api/analytics.md`, `docs/references/competitor-research.md`, `docs/prompts/hooks.md` |
- 完整的内容流程、性能监控、CTA 测试 | `docs/api/pipeline.md` |
- 错误代码及故障排除 | `docs/api/errors.md` |

## 细分市场研究模式（当用户请求进行市场研究时）

当用户提出“研究这个细分市场”等需求时，执行以下步骤：
1. 首先使用 `trend-brief` 命令查询该细分市场的相关数据（提供 7 天的基础数据，如需最新信息可延长至 24 小时）。
2. 提取并报告以下信息：热门话题标签、热门音频素材、热门创作者、最佳发布时间（UTC 时间）以及推荐的创意素材使用角度。
3. 使用 `docs/references/competitor-research.md` 文档深入分析至少 3 个竞争对手。
4. 生成一份实用的报告，内容包括：
   - 3 个可供测试的创意素材使用角度
   - 2 个推荐的发布策略建议
   - 5 个适合使用的热门话题标签
   - 1 个可利用的市场机会洞察
5. 将分析结果保存到 `workspace/performance/competitor-insights.md` 文件中，并在后续内容创作中参考这些信息。

## 不可更改的规则

无论加载了哪些文档，都必须遵守以下规则：

1. **在使用素材包生成幻灯片时，** **必须使用 `pinned_images` 参数**。**切勿仅使用 `--pack-id` 参数调用 `generate` 命令**，否则服务器会随机选择图片。在使用任何素材包之前，请务必阅读 `docs/api/packs.md` 文档。
2. **在发布前，** **必须对每个渲染后的幻灯片进行视觉审核**。如果发现任何幻灯片无法正常显示，请立即修复。这是强制性的要求。
3. **发布内容后，** **必须立即将日志记录到 `workspace/performance/log.json` 文件中**。这是官方的日志记录方式。
4. **发布内容后，** **必须添加相应的日志记录条目**。没有日志记录就意味着无法获取学习数据。
5. **在生成的任何内容中，** **严禁使用连字符（-）**。
6. **所有实例数据都保存在 `workspace/` 目录下**。请勿将其他状态文件写入技能脚本的根目录。

## 脚本使用说明

```bash
/path/to/genviral/scripts/genviral.sh <command> [options]
```

使用该脚本时需要将 `GENVIRAL_API_KEY` 设置为环境变量（格式：`public_id.secret`）。脚本会从 `defaults.yaml` 文件中加载默认配置。可以通过设置 `GENVIRAL_WORKSPACE_DIR` 变量来更改工作空间路径（默认值为相对于技能脚本目录的 `workspace/`）。

## 自动更新

该脚本包含自动更新机制，可确保技能相关的文件始终与 `fdarkaou/genviral-skill` 的最新版本保持同步。

```bash
bash scripts/update-skill.sh           # check + apply if updates available
bash scripts/update-skill.sh --dry-run # preview only, no changes
bash scripts/update-skill.sh --force   # force re-apply even if already current
```

**更新内容：** `SKILL.md`、`scripts/`、`docs/`（所有子目录）。

**不可更改的内容：** `workspace/` 目录下的内容（用户的数据、设置信息、创意素材以及性能日志）将始终保持不变。

---

## 注意事项

- 该技能支持 genviral 支持的所有平台（TikTok、Instagram 等）。
- 支持发布视频和幻灯片内容。
- 支持使用托管账户和用户自有的账户。
- 发布内容可以安排发布时间或立即发布。
- 对于 TikTok 幻灯片草稿，可以使用 `post_mode: MEDIA_UPLOAD` 选项将文件保存到草稿箱中，以便后续添加音频。
- 所有发布的内容都会显示在 Genviral 的仪表板上。