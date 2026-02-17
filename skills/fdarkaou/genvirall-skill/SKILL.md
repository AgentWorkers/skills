---
name: genviral
description: 完成 genviral Partner API 的自动化功能。支持在 TikTok、Instagram 以及所有受支持的平台上创建和安排发布内容（包括视频和幻灯片）。功能涵盖幻灯片生成、文件上传、模板/包管理、数据分析，以及整个内容发布流程的自动化处理。
homepage: https://github.com/fdarkaou/genviral-skill
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["curl", "jq", "bash"]
---
# genviral 合作伙伴 API 技能

> **简要说明：** 该技能将 genviral 的合作伙伴 API 封装为 42 个以上的 bash 命令，覆盖所有文档化的接口。核心工作流程包括：`generate`（根据提示生成幻灯片）、`render`（生成图片）、`review`（检查质量）和 `create-post`（发布）。认证通过环境变量 `GENVIRAL_API_KEY` 进行，配置信息存储在 `config.md` 中。新功能包括：全面分析支持（汇总数据、帖子统计、目标账户管理等）。产品相关设置位于 `context/` 目录中，钩子函数库在 `hooks/` 目录中，结果跟踪记录在 `performance/` 目录中。该技能具备自我优化能力：发布后会进行结果跟踪、分析，进而优化策略并生成更优质的内容。

该技能实现了对 genviral 合作伙伴 API 的全面自动化，支持创建视频帖子、AI 生成的幻灯片、管理模板和图片包、跟踪分析数据，并能在 genviral 支持的任何平台（如 TikTok、Instagram 等）上安排内容发布。

## 该技能的功能

- **多平台发布：** 为 TikTok、Instagram 或其他关联账户创建帖子（支持视频或幻灯片格式，每条帖子可关联多个账户）。
- **文件管理：** 使用预签名的 URL 流将视频/图片上传到 genviral 的内容分发网络（CDN）。
- **AI 生成幻灯片：** 根据提示生成图片轮播效果。
- **模板系统：** 创建可复用的幻灯片模板，并将表现优秀的幻灯片转换为模板。
- **图片包管理：** 管理幻灯片的背景图片包。
- **分析功能：** 提供汇总的 KPI 数据、帖子级别的指标信息，以及目标账户的管理功能。
- **内容流程自动化：** 从接收提示到发布草稿的全过程实现自动化。
- **性能跟踪：** 记录帖子发布情况，跟踪相关指标，并从分析结果中学习优化策略。

## 工作原理

核心工作流程如下：

1. **生成或上传媒体内容**（根据提示生成幻灯片，或上传用户自己的视频/图片）。
2. **创建帖子**：针对一个或多个账户进行发布。
3. **安排或发布**：可以立即发布，也可以设定特定时间发布。
4. **跟踪性能**：通过分析接口获取数据。
5. **持续优化：** 根据分析结果优化发布策略。

对于 TikTok 幻灯片帖子，可以选择保存为草稿状态，以便在发布前添加热门音乐（选择音乐需要人工判断以获得最佳效果）。

## 首次设置

如果是首次安装，请阅读 `setup.md` 文件，并按照指导进行设置：

1. 设置 API 密钥并验证其有效性。
2. 列出要发布的账户。
3. 讨论图片使用策略（使用现有图片包、新建图片包、每次发布时生成新图片，或混合使用）。
4. （可选）设置产品相关信息和品牌风格。

无需预设默认值。系统会询问用户的具体需求并进行相应配置。所有设置都会显示在 Genviral 仪表板上，用户可以随时查看和控制所有内容。

所有配置信息都保存在 `config.md` 文件中。敏感信息通过环境变量加载。

## 文件结构

```
genviral/
  SKILL.md                  # This file (comprehensive API reference + strategy)
  setup.md                  # Quick setup guide (3 steps)
  config.md               # API config, defaults, schedule settings

  context/
    product.md              # Product description, value props, target audience
    brand-voice.md          # Tone, style, do's and don'ts
    niche-research.md       # Platform research for the niche

  hooks/
    library.json            # Hook instances (grows over time, tracks performance)
    formulas.md             # Hook formula patterns and psychology

  content/
    scratchpad.md           # Working content plan, ideas, drafts in progress
    calendar.json           # Content calendar (upcoming planned posts)

  performance/
    log.json                # Post performance tracking (views, likes, shares)
    insights.md             # Agent's learnings from performance data
    weekly-review.md        # Weekly review template and process

  scripts/
    genviral.sh             # Main API wrapper script (all commands)

  prompts/
    slideshow.md            # Prompt templates for slideshow generation
    hooks.md                # Prompt templates for hook brainstorming
```

## 脚本参考

所有命令都使用同一个封装脚本：

```bash
/path/to/genviral/scripts/genviral.sh <command> [options]
```

该脚本需要 `GENVIRAL_API_KEY` 作为环境变量，该变量从 `config.md` 文件中加载默认值。

---

## 账户与文件相关命令

### accounts
列出您权限范围内的自有账户和托管账户。用于获取发布所需的账户 ID。

```bash
genviral.sh accounts
genviral.sh accounts --json
```

返回内容：
- 账户 ID（用于 `create-post` 命令）
- 平台（如 TikTok、Instagram 等）
- 账户类型（自有或托管）
- 用户名、显示名称、账户状态

### upload
使用预签名的 URL 流将文件上传到 genviral 的 CDN。返回可用于帖子的 CDN URL。

```bash
genviral.sh upload --file video.mp4 --content-type video/mp4
genviral.sh upload --file slide1.jpg --content-type image/jpeg --filename "slide1.jpg"
```

支持的文件类型：
- 视频：`video/mp4`、`video/quicktime`、`video/x-msvideo`、`video/webm`、`video/x-m4v`
- 图片：`image/jpeg`、`image/png`、`image/gif`、`image/webp`、`image/heic`、`image/heif`

返回 CDN URL（用于 `create-post` 命令）。

### list-files
列出通过合作伙伴 API 上传的文件。

```bash
genviral.sh list-files
genviral.sh list-files --type video --limit 20 --offset 0
genviral.sh list-files --type image --context ai-studio,media-upload
genviral.sh list-files --context all  # include all contexts
genviral.sh list-files --json
```

`--type` 参数可选值：`image` 或 `video`。

---

## 发布相关命令

### create-post
创建针对一个或多个账户的帖子（支持视频或幻灯片格式）。

**视频帖子：**

```bash
genviral.sh create-post \
  --caption "Your caption with #hashtags" \
  --media-type video \
  --media-url "https://cdn.genviral.com/your-video.mp4" \
  --accounts "account_id_1,account_id_2" \
  --scheduled-at "2025-03-01T15:00:00Z"
```

**幻灯片帖子：**

```bash
genviral.sh create-post \
  --caption "Your caption" \
  --media-type slideshow \
  --media-urls "url1,url2,url3,url4,url5,url6" \
  --accounts "account_id_1" \
  --music-url "https://www.tiktok.com/@user/video/1234567890"
```

**TikTok 特定设置**（仅当所有账户均为 TikTok 自有账户时适用）：

```bash
genviral.sh create-post \
  --caption "Caption" \
  --media-type slideshow \
  --media-urls "url1,url2,url3,url4,url5,url6" \
  --accounts "tiktok_account_id" \
  --tiktok-title "Optional title" \
  --tiktok-description "Optional description" \
  --tiktok-post-mode "MEDIA_UPLOAD" \
  --tiktok-privacy "SELF_ONLY" \
  --tiktok-disable-comment \
  --tiktok-disable-duet \
  --tiktok-disable-stitch \
  --auto-add-music true \
  --is-commercial false \
  --is-branded-content false \
  --user-consent true \
  --is-your-brand false
```

TikTok 相关的布尔参数：
- `--tiktok-disable-comment`（默认值为 `true`，禁用评论）
- `--tiktok-disable-comment false`（明确禁用评论）

其他相关参数：
- `--tiktok-disable-duet`、`--tiktok-disable-stitch`、`--auto-add-music`、`--is-commercial`、`--is-branded-content`、`--user-consent`、`--is-your-brand`

TikTok 的 `post_mode` 参数：
- `DIRECT_POST`：立即发布（默认值）
- `MEDIA_UPLOAD`：将帖子保存到 TikTok 的草稿箱（仅适用于幻灯片类型）

TikTok 的 `privacy_level` 参数：
- `PUBLIC_TO_EVERYONE`（默认值）
- `MUTUAL_follow FRIENDS`
- `FOLLOWER_OF_CREATOR`
- `SELF_ONLY`（草稿模式）

**调度：**
- 省略 `--scheduled-at` 参数或设置当前时间后的 30 秒内发布（状态：`pending`）
- 提供未来的 ISO 时间戳（状态：`scheduled`）
- `--scheduled-at` 参数必须为 ISO 8601 格式，包含时区偏移量（例如：`2026-02-14T19:47:00Z`）

`--music-url` 参数必须指向 TikTok 的视频 URL。

**多账户发布：**
每条帖子最多可关联 10 个账户。支持混合使用 TikTok、Instagram 等平台。只有当所有账户均为 TikTok 自有账户时，才支持音乐功能。TikTok 特定设置仅在该情况下生效。

### update-post
更新现有帖子（仅当帖子处于草稿、待发布、已调度、重试或失败状态时可编辑）。

```bash
genviral.sh update-post \
  --id POST_ID \
  --caption "Updated caption" \
  --media-type video \
  --media-url "https://new-video.mp4" \
  --accounts "new_account_id_1,new_account_id_2" \
  --scheduled-at "2025-03-15T18:00:00Z"
```

清除操作：
- `--music-url null`：移除音乐链接
- `--clear-scheduled-at`：清除调度时间
- `--clear-tiktok`：清除所有 TikTok 相关设置

验证注意事项：
- `--scheduled-at` 参数必须为 ISO 8601 格式，包含时区偏移量（例如：`2026-02-14T19:47:00Z`）
- `--music-url` 参数必须指向 TikTok 的视频 URL（除非使用 `null` 以清除音乐链接）
- `--auto-add-music` 参数支持两种形式：默认值或显式值

### retry-posts
重试失败或部分失败的帖子。

```bash
genviral.sh retry-posts --post-ids "post_id_1,post_id_2"
genviral.sh retry-posts --post-ids "post_id_1" --account-ids "account_id_1"
```

限制：
- `post_ids`：1-20 个帖子 ID
- `account_ids`：1-10 个账户 ID

### list-posts
列出帖子，支持过滤操作。

```bash
genviral.sh list-posts
genviral.sh list-posts --status scheduled --limit 20
genviral.sh list-posts --since "2025-02-01T00:00:00Z" --until "2025-02-28T23:59:59Z"
genviral.sh list-posts --json
```

`--since` 和 `--until` 参数必须为 ISO 8601 格式的日期时间，包含时区偏移量。

状态过滤选项：`draft`、`pending`、`scheduled`、`posted`、`failed`、`partial`、`retry`

### get-post
获取特定帖子的详细信息。

```bash
genviral.sh get-post --id POST_ID
```

### delete-posts（别名：delete-post）
按 ID 批量删除帖子。

```bash
genviral.sh delete-posts --ids "post_id_1,post_id_2,post_id_3"
# equivalent option name
genviral.sh delete-posts --post-ids "post_id_1,post_id_2,post_id_3"
# command alias
genviral.sh delete-post --ids "post_id_1,post_id_2"
```

每次请求最多删除 50 个帖子。

返回删除结果：
- `deletedIds`：被删除的帖子 ID
- `blockedStatuses`：因状态原因无法删除的帖子
- `skipped`：跳过的操作

---

## 幻灯片相关命令

### generate | generate-slideshow
根据提示使用 AI 生成幻灯片，或通过 `--skip-ai` 选项手动生成幻灯片。

```bash
# AI mode (default)
genviral.sh generate \
  --prompt "Your hook and content prompt" \
  --pack-id PACK_ID \
  --slides 5 \
  --type educational \
  --aspect-ratio 4:5 \
  --style tiktok \
  --language en \
  --font-size small \
  --text-width narrow \
  --product-id PRODUCT_ID

# Manual/mixed mode with slide_config
genviral.sh generate \
  --skip-ai \
  --slide-config-file slide-config.json

# Pass slide_config inline
genviral.sh generate \
  --skip-ai \
  --slide-config-json '{"total_slides":2,"slide_types":["image_pack","custom_image"],...}'
```

选项：
- `--prompt`：AI 生成的提示文本（除非使用 `--skip-ai` 或 `--product-id`，否则必填）
- `--pack-id`：背景图片包的 UUID
- `--slides`：幻灯片数量（1-10 张，默认值：5 张）
- `--type`：`educational` 或 `personal`（教育类或个人用途）
- `--aspect-ratio`：宽高比（9:16、4:5、1:1）
- `--style` / `--text-preset`：文本样式预设（例如：`tiktok`）
- `--language`：语言代码（例如：`en`、`es`、`fr`）
- `--font-size`：字体大小（默认值或 `small`）
- `--product-id`：可选的产品关联标识符
- `--skip-ai`：跳过 AI 生成的文本（与 `--slide-config-*` 选项配合使用）
- `--slide-config-json` / `--slide-config`：幻灯片配置的 JSON 文件路径

### render | render-slideshow
将幻灯片渲染为图片。

```bash
genviral.sh render --id SLIDESHOW_ID
```

返回结果：
- 更新后的幻灯片及其对应的图片 URL
- 状态：`rendered`（已渲染）

### review | get-slideshow
获取幻灯片的详细信息以供审核。显示每张幻灯片的文字内容、状态和渲染后的图片 URL。

```bash
genviral.sh review --id SLIDESHOW_ID
genviral.sh review --id SLIDESHOW_ID --json
genviral.sh get-slideshow --id SLIDESHOW_ID  # alias
```

### update | update-slideshow
更新幻灯片的字段、设置或内容。更新后需要重新渲染幻灯片。

```bash
# Update title
genviral.sh update --id SLIDESHOW_ID --title "New Title"

# Update status
genviral.sh update --id SLIDESHOW_ID --status draft

# Update settings
genviral.sh update --id SLIDESHOW_ID --settings-json '{"aspect_ratio":"9:16","advanced_settings":{"text_width":"narrow"}}'

# Update slides (full replacement)
genviral.sh update --id SLIDESHOW_ID --slides '[{"image_url":"...","text_elements":[{"content":"..."}]}]'

# Load slides from file
genviral.sh update --id SLIDESHOW_ID --slides-file slides.json

# Update product_id or clear it
genviral.sh update --id SLIDESHOW_ID --product-id NEW_PRODUCT_ID
genviral.sh update --id SLIDESHOW_ID --clear-product-id
```

选项：
- `--title`：更新幻灯片标题
- `--status`：`draft` 或 `rendered`（未渲染/已渲染）
- `--slideshow-type`：`educational` 或 `personal`（教育类/个人用途）
- `--product-id`：关联的产品标识符
- `--clear-product-id`：解除产品关联
- `--settings-json` / `--settings-file`：部分设置修改
- `--slides` / `--slides-file`：完整的幻灯片数组

### regenerate-slide
重新生成单个幻灯片的文本内容（索引从 0 开始）。

```bash
genviral.sh regenerate-slide --id SLIDESHOW_ID --index 2
genviral.sh regenerate-slide --id SLIDESHOW_ID --index 2 --instruction "Make this shorter and more punchy"
```

限制：
- `--index` 参数必须为非负整数
- `--instruction`：指令文本的最大长度为 500 个字符

### duplicate | duplicate-slideshow
复制现有的幻灯片作为新的草稿。

```bash
genviral.sh duplicate --id SLIDESHOW_ID
```

### delete | delete-slideshow
删除幻灯片。

```bash
genviral.sh delete --id SLIDESHOW_ID
```

### list-slideshows
列出幻灯片，支持过滤和分页显示。

```bash
genviral.sh list-slideshows
genviral.sh list-slideshows --status rendered --search "hook" --limit 20 --offset 0
genviral.sh list-slideshows --json
```

---

## 图片包相关命令

图片包是用于幻灯片的背景图片集合。

### list-packs
列出可用的图片包。

```bash
genviral.sh list-packs
genviral.sh list-packs --search motivation --include-public false
genviral.sh list-packs --limit 20 --offset 0 --json
```

### get-pack
获取单个图片包及其所有图片的 URL。

```bash
genviral.sh get-pack --id PACK_ID
```

### create-pack
创建新的图片包。

```bash
genviral.sh create-pack --name "My Pack"
genviral.sh create-pack --name "Public Pack" --is-public
# explicit boolean also supported
genviral.sh create-pack --name "Private Pack" --is-public false
```

### update-pack
更新图片包的名称或可见性设置。

```bash
genviral.sh update-pack --id PACK_ID --name "New Name"
genviral.sh update-pack --id PACK_ID --is-public true
```

### delete-pack
删除图片包。

```bash
genviral.sh delete-pack --id PACK_ID
```

### add-pack-image
向图片包中添加图片。

```bash
genviral.sh add-pack-image --pack-id PACK_ID --image-url "https://cdn.example.com/image.jpg"
genviral.sh add-pack-image --pack-id PACK_ID --image-url "https://cdn.example.com/image.jpg" --file-name "hero-1.jpg"
```

### delete-pack-image
从图片包中删除图片。

```bash
genviral.sh delete-pack-image --pack-id PACK_ID --image-id IMAGE_ID
```

---

## 模板相关命令

模板是可复用的幻灯片结构，用于快速迭代内容创作。

### list-templates
列出您权限范围内的可用模板。

```bash
genviral.sh list-templates
genviral.sh list-templates --search hooks --limit 20 --offset 0
genviral.sh list-templates --json
```

### get-template
获取单个模板。

```bash
genviral.sh get-template --id TEMPLATE_ID
```

### create-template
根据验证过的模板配置对象创建新模板。

```bash
# File input
genviral.sh create-template \
  --name "My Template" \
  --description "Description" \
  --visibility private \
  --config-file template-config.json

# Inline JSON input
genviral.sh create-template \
  --name "My Template" \
  --visibility workspace \
  --config-json '{"version":1,"structure":{"slides":[]},"content":{},"visuals":{}}'
```

配置文件必须符合模板配置的 v1 格式。可以使用以下方式之一进行配置：
- `--config-file <path>`
- `--config-json '<json>'`

### update-template
更新模板字段。

```bash
genviral.sh update-template --id TEMPLATE_ID --name "New Name"
genviral.sh update-template --id TEMPLATE_ID --visibility workspace
genviral.sh update-template --id TEMPLATE_ID --config-file new-config.json
genviral.sh update-template --id TEMPLATE_ID --config-json '{"version":1,"structure":{"slides":[]},"content":{},"visuals":{}}'
genviral.sh update-template --id TEMPLATE_ID --clear-description
```

配置输入方式：
- `--config-file` 或 `--config-json`

### delete-template
删除模板。

```bash
genviral.sh delete-template --id TEMPLATE_ID
```

### create-template-from-slideshow
将现有的幻灯片转换为可复用的模板。

```bash
genviral.sh create-template-from-slideshow \
  --slideshow-id SLIDESHOW_ID \
  --name "Winning Format" \
  --description "Built from high-performing slideshow" \
  --visibility workspace \
  --preserve-text
```

`--preserve-text` 参数支持两种形式：
- `--preserve-text`（设置为 `true`）
- `--preserve-text true|false`（是否保留文本）

---

## 分析相关命令

分析接口提供 KPI 数据、帖子指标和目标账户管理功能。

### analytics-summary（别名：get-analytics-summary）
获取包含 KPI、趋势数据和内容分布的统计摘要。

```bash
genviral.sh analytics-summary
genviral.sh analytics-summary --range 30d
genviral.sh analytics-summary --start 2026-01-01 --end 2026-01-31
genviral.sh analytics-summary --platforms tiktok,instagram
genviral.sh analytics-summary --accounts TARGET_ID_1,TARGET_ID_2
genviral.sh analytics-summary --json
```

选项：
- `--range`：日期范围预设（14d、30d、90d、1y、all）
- `--start` / `--end`：自定义日期范围（格式：YYYY-MM-DD）
- `--platforms`：用逗号分隔的平台过滤条件
- `--accounts`：用逗号分隔的目标账户 ID

返回结果：
- `kpis`：发布的视频数量、活跃账户数量、观看次数、点赞数、评论数、分享次数、参与率（包含变化趋势）
- `interactionSeries`：每日互动数据
- `engagementSeries`：每日参与率
- `postingHeatmap`：每日帖子发布数量
- `postingStreak`：连续发布天数
- `contentMix`：按平台分类的帖子列表

### analytics-posts（别名：list-analytics-posts）
列出帖子级别的分析数据，支持排序和分页显示。

```bash
genviral.sh analytics-posts
genviral.sh analytics-posts --range 90d --sort-by views --sort-order desc --limit 25
genviral.sh analytics-posts --start 2026-01-01 --end 2026-01-31 --platforms tiktok
genviral.sh analytics-posts --json
```

选项：
- `--range`：日期范围预设（14d、30d、90d、1y、all）
- `--start` / `--end`：自定义日期范围
- `--platforms`：平台过滤条件
- `--accounts`：目标账户 ID 过滤条件
- `--sort-by`：排序依据（发布时间、观看次数、点赞数、评论数）
- `--sort-order`：排序方式（升序/降序）
- `--limit`：每页显示数量（最多 100 条）
- `--offset`：分页偏移量

### analytics-targets
列出被跟踪的分析目标账户。

```bash
genviral.sh analytics-targets
genviral.sh analytics-targets --json
```

### analytics-target-create
添加新的分析目标账户。

```bash
genviral.sh analytics-target-create --platform tiktok --identifier @brand
genviral.sh analytics-target-create --platform instagram --identifier @brand --alias "Brand HQ"
```

选项：
- `--platform`：`tiktok`、`instagram` 或 `youtube`（必填）
- `--identifier`：账户标识符（必填）
- `--alias`：显示名称自定义选项

### analytics-target
获取单个分析目标的详细信息。

```bash
genviral.sh analytics-target --id TARGET_ID
```

### analytics-target-update
更新分析目标账户的配置。

```bash
genviral.sh analytics-target-update --id TARGET_ID --display-name "New Name"
genviral.sh analytics-target-update --id TARGET_ID --favorite true
genviral.sh analytics-target-update --id TARGET_ID --clear-display-name
genviral.sh analytics-target-update --id TARGET_ID --refresh-policy-json '{"freeDailyRefresh":true}'
genviral.sh analytics-target-update --id TARGET_ID --clear-refresh-policy
```

### analytics-target-delete
删除分析目标账户。

```bash
genviral.sh analytics-target-delete --id TARGET_ID
```

### analytics-target-refresh
触发分析目标的更新操作。

```bash
genviral.sh analytics-target-refresh --id TARGET_ID
```

返回结果：
- 更新状态（`pending`、`processing`、`completed`、`failed`）
- 是否使用了免费更新窗口（`wasFree`）
- 更新开始时间、完成时间
- 错误信息（`error`）

### analytics-refresh | get-analytics-refresh
检查更新状态。

```bash
genviral.sh analytics-refresh --id REFRESH_ID
```

返回结果：
- 更新状态（`pending`、`processing`、`completed`、`failed`）
- 使用的免费更新次数（`credits_used`）
- 更新开始时间、完成时间
- 错误信息（`error`）

### analytics-workspace-suggestions（别名：get-analytics-workspace-suggestions）
列出其他工作空间/个人权限范围内的被跟踪账户。

```bash
genviral.sh analytics-workspace-suggestions
genviral.sh get-analytics-workspace-suggestions
genviral.sh analytics-workspace-suggestions --json
```

---

## 旧版流程相关命令

这些是针对 TikTok 的便捷命令。

### post-draft
将渲染后的幻灯片保存为草稿（仅适用于 TikTok）。

```bash
genviral.sh post-draft \
  --id SLIDESHOW_ID \
  --caption "Your caption with #hashtags" \
  --account-ids "account_id_1"
```

始终强制使用以下安全设置：`privacy_level=SELF_ONLY` 和 `post_mode=MEDIA_UPLOAD`。

### full-pipeline
完整的自动化流程：生成 -> 渲染 -> 审核 -> 发布草稿。

```bash
genviral.sh full-pipeline \
  --prompt "Your hook and content prompt" \
  --caption "Caption with #hashtags" \
  --pack-id PACK_ID \
  --slides 5 \
  --type educational \
  --style tiktok \
  --account-ids ACC_ID
```

使用 `--skip-post` 选项可以在渲染后停止流程（便于在发布前进行审核）。

---

## 内容创作流程

推荐的发布流程如下：

### 对于幻灯片帖子：

1. **选择钩子函数：** 读取 `hooks/library.json` 文件并选择一个合适的钩子函数。
2. **组装提示文本：** 使用选定的钩子函数生成完整的幻灯片提示文本。参考 `prompts/slideshow.md` 文件。
3. **生成幻灯片：** 使用生成的提示文本运行 `generate` 命令。
4. **审核幻灯片内容：** 检查每张幻灯片的清晰度、可读性和逻辑连贯性。需要的话，可以重新生成或替换某些幻灯片。
5. **渲染图片：** 运行 `render` 命令生成最终图片。
6. **视觉审核：** 在发布前，使用图像分析工具仔细检查每张渲染后的图片。检查以下内容：（a）背景图片是否与主题和产品相关；（b）文字是否清晰可见，没有被背景图片遮挡；（c）文字没有溢出或裁剪；（d）整体质量是否符合发布标准。如果有任何问题，重新生成或更换图片。未经审核切勿发布。
7. **发布：** 使用 `create-post` 命令发布幻灯片，或使用旧版 `post-draft` 命令保存为 TikTok 草稿。
8. **记录日志：** 发布后立即在 `content/post-log.md` 文件中记录相关信息：日期、时间（UTC 格式）、帖子 ID、类型（幻灯片/视频）、使用的钩子函数/标题片段、状态（已发布/待发布/草稿），以及使用的图片包。这是所有内容输出的唯一记录来源。如果文件不存在，请使用指定格式创建该文件。此步骤必不可少。
9. **跟踪性能：** 使用分析接口监控指标数据。在定期检查性能时（例如晚上），更新 `content/post-log.md` 文件中的观看次数/点赞数/评论数等信息。

### 对于视频帖子：

1. **上传视频：** 使用 `upload` 命令上传视频文件，或使用现有的 CDN URL。
2. **编写标题：** 遵循品牌风格，添加相关的标签。
3. **发布帖子：** 使用 `create-post` 命令发布视频内容。
4. **跟踪性能：** 使用分析接口监控数据。

---

## 平台最佳实践

### TikTok：
- **幻灯片数量：** 5-6 张为最佳效果。
- **宽高比：** 全屏显示使用 9:16，信息流显示使用 4:5。
- **文字可读性：** 每张幻灯片只展示一个要点，文字长度不超过 16 个单词。避免在图片底部 20% 的区域内显示文字。
- **叙事结构（5 张幻灯片的结构）：**
  1. 引入问题
  2. 问题描述
  3. 解决方案介绍
  4. 产品特点展示
  5. 行动号召

### Instagram：
- **幻灯片数量：** 5-10 张适合轮播展示。
- **宽高比：**
  - Reels 动画使用 9:16
  - 信息流帖子使用 4:5 或 1:1

---

## API 错误代码

常见的合作伙伴 API 错误代码：
- `401 unauthorized`：API 密钥缺失、格式错误或无效
- `402 subscription_required`：工作空间/账户需要激活订阅
- `403 tier_not_allowed`：当前订阅等级不支持该功能
- `422 invalid_payload`：请求格式或枚举值无效
- `429 rate_limited`：短时间内请求次数过多

---

## 故障排除

- **“GENVIRAL_API_KEY is required”**：请导出环境变量 `export GENVIRAL_API_KEY="your_public_id.your_secret"`。
- **“No rendered image URLs found”**：表示幻灯片尚未生成，请先运行 `render` 命令。
- **API 返回 401、402 或 403 错误**：
  - `401`：验证 API 密钥的格式（`public_id.secret`）和令牌的有效性。
  - `402`：激活或升级订阅。
  - `403`：当前订阅等级不支持该功能。
- **渲染耗时过长**：每张幻灯片的渲染时间约为 2-5 秒，5 张幻灯片的总渲染时间最长为 25 秒。

---

## 其他注意事项：

- **多平台支持：** 支持 genviral 支持的所有平台（TikTok、Instagram 等）。
- **内容类型：** 支持视频帖子和幻灯片（图片轮播）两种格式。
- **账户类型：** 既支持托管账户，也支持用户自有的账户。
- **调度功能：** 可以安排未来发布或立即发布。
- **草稿模式：** 对于 TikTok 幻灯片帖子，使用 `post_mode: MEDIA_UPLOAD` 将帖子保存到草稿箱。
- **模板系统：** 将表现优秀的幻灯片转换为模板，以便快速迭代内容。
- **分析功能：** 提供全面分析，支持跨账户跟踪性能数据。
- **注意事项：** 在生成的任何内容中禁止使用连字符（`-`）。