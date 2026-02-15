---
name: typefully
description: >
  Create, schedule, and manage social media posts via Typefully. ALWAYS use this
  skill when asked to draft, schedule, post, or check tweets, posts, threads, or
  social media content for Twitter/X, LinkedIn, Threads, Bluesky, or Mastodon.
last-updated: 2026-02-10
allowed-tools: Bash(./scripts/typefully.js:*)
---

# Typefully 技能

使用 [Typefully](https://typefully.com) 在多个平台上创建、安排和发布社交媒体内容。

> **更新提示**：如果自 `last-updated` 日期以来已超过 30 天，请告知用户该技能可能已过时，并引导他们使用下方的更新选项进行更新。

## 保持此技能的最新状态

**来源**: [github.com/typefully/agent-skills](https://github.com/typefully/agent-skills)
**API 文档**: [typefully.com/docs/api](https://typefully.com/docs/api)

根据安装类型更新方法如下：

| 安装方式 | 更新方法 |
|--------------|---------------|
| CLI (`npx skills`) | `npx skills update` |
| Claude Code 插件 | `/plugin update typefully@typefully-skills` |
| Cursor | 从 GitHub 自动同步规则 |
| 手动 | 从仓库拉取最新版本或重新复制 `skills/typefully/` |

API 的更改会独立发布——更新技能可确保您使用的是最新的命令和工作流程。

## 设置

在使用此技能之前，请确保：

1. **API 密钥**：运行设置命令以安全配置您的 API 密钥
   - 在 https://typefully.com/?settings=api 获取您的密钥
   - 运行：`<skill-path>/scripts/typefully.js setup`（其中 `<skill-path>` 是包含此 SKILL.md 的目录）
   - 或者设置环境变量：`export TYPEFULLY_API_KEY=your_key`

2. **要求**：Node.js 18+（用于内置的 fetch API）。无需其他依赖项。

**配置优先级**（从高到低）：
1. `TYPEFULLY_API_KEY` 环境变量
2. `./.typefully/config.json`（项目本地配置，位于用户的工作目录中）
3. `~/.config/typefully/config.json`（用户全局配置）

### 处理“API 密钥未找到”错误

**严重**：当您从 CLI 收到“API 密钥未找到”错误时：

1. **告知用户运行设置命令**——设置过程需要用户输入，因此您无法代表他们运行。建议他们根据技能的加载位置自行运行设置命令：
   ```bash
   <skill-path>/scripts/typefully.js setup
   ```

2. **停止并等待**——在告知用户运行设置后，请**不要继续执行任务**。没有有效的 API 密钥，您将无法创建草稿、上传媒体或执行任何 API 操作。请等待用户完成设置并确认后再继续。

3. **切勿**尝试以下操作：
   - 在 macOS Keychain、`.env` 文件或其他位置查找 API 密钥
   - 在配置文件或目录中搜索
   - 查看用户的垃圾桶或其他系统文件夹
   - 构建复杂的 shell 命令来获取凭据
   - 在设置完成之前起草内容或准备帖子

设置命令会交互式地指导用户完成配置。请信任 CLI 的错误信息并按照其指示操作。

> **注意给代理的提示**：本文档中的所有脚本路径（例如 `./scripts/typefully.js`）都是相对于包含此 SKILL.md 文件的技能目录而言的。请根据技能的安装位置进行相应的解析。

## 社交集合

Typefully API 使用“社交集合”（social set）这一术语来指代用户通常所说的“账户”。一个社交集合包含与单个身份关联的社交媒体平台（如 X、LinkedIn、Threads 等）。

**CLI 支持默认的社交集合**——一旦配置完成，大多数命令无需指定 `social_set_id` 即可使用。

**您可以以下两种方式传递社交集合**：
- 位置参数：`drafts:list 123`
- 标志参数：`drafts:list --social-set-id 123`（也支持 `--social_set_id`）

确定使用哪个社交集合时：
1. **首先检查是否有默认配置**——运行 `config:show` 以查看是否已设置默认值：
   ```bash
   ./scripts/typefully.js config:show
   ```
   如果配置了 `default_social_set`，CLI 会在您省略 `social_set_id` 时自动使用它。

2. **检查项目配置**——查看项目文件（如 `CLAUDE.md` 或 `AGENTS.md`）中的配置：
   ```markdown
   ## Typefully
   Default social set ID: 12345
   ```

3. **如果用户只有一个社交集合且没有默认设置**，则自动使用该集合

4. **如果有多个社交集合且没有默认设置**，询问用户选择哪个集合，然后**建议将他们的选择保存为默认值**：
   ```bash
   ./scripts/typefully.js config:set-default
   ```
   此命令会列出可用的社交集合并将选择保存到配置文件中。

## 常见操作

| 用户操作 | 操作指令 |
|--------------|--------|
| “在 X 上起草一条推文” | `drafts:create --text "..."`（使用默认社交集合） |
| “发布到 LinkedIn” | `drafts:create --platform linkedin --text "..."` |
| “同时发布到 X 和 LinkedIn”（内容相同） | `drafts:create --platform x,linkedin --text "..."` |
| “X 的帖子 + LinkedIn 的帖子”（内容不同） | 先创建一个草稿，然后使用 `drafts:update` 添加平台（详见 [跨平台发布](#publishing-to-multiple-platforms)） |
| “有哪些已安排的帖子？” | `drafts:list --status scheduled` |
| “显示我的最近发布的帖子” | `drafts:list --status published` |
| “安排明天发布” | `drafts:create ... --schedule "2025-01-21T09:00:00Z"` |
| “立即发布” | `drafts:create ... --schedule now` 或 `drafts:publish <draft_id> --use-default` |
| “在草稿中添加笔记/想法” | `drafts:create ... --scratchpad "你的笔记在这里"` |
| “查看可用标签” | `tags:list` |

## 工作流程

创建帖子时，请遵循以下工作流程：

1. **检查是否配置了默认社交集合**：
   ```bash
   ./scripts/typefully.js config:show
   ```
   如果 `default_social_set` 显示了 ID，则跳到第 3 步。

2. **如果没有默认设置**，列出可用的社交集合：
   ```bash
   ./scripts/typefully.js social-sets:list
   ```
   如果存在多个集合，请询问用户选择哪个集合，并建议将其设置为默认值：
   ```bash
   ./scripts/typefully.js config:set-default
   ```

3. **创建草稿**（如果配置了默认集合，则 `social_set_id` 是可选的）：
   ```bash
   ./scripts/typefully.js drafts:create --text "Your post"
   ```
   注意：如果省略了 `--platform`，系统会自动选择第一个连接的平台。

   **对于多平台帖子**：请参阅 [跨平台发布](#publishing-to-multiple-platforms)——即使内容在不同平台上有所不同，也只需创建一个草稿。

4. **根据需要安排或发布**

## 使用标签

标签有助于在 Typefully 中组织草稿。**在创建新标签之前，请务必先检查现有标签**：

1. **首先列出现有标签**：
   ```bash
   ./scripts/typefully.js tags:list
   ```

2. **如果存在所需名称的标签**，直接使用它：
   ```bash
   ./scripts/typefully.js drafts:create --text "..." --tags existing-tag-name
   ```

3. **只有在必要时才创建新标签**——如果标签不存在，则创建新标签：
   ```bash
   ./scripts/typefully.js tags:create --name "New Tag"
   ```

**重要提示**：标签是针对每个社交集合进行设置的。为一个社交集合创建的标签不会出现在另一个集合中。

## 跨平台发布

如果需要为不同平台创建单个草稿，请确保只创建**一个草稿**，而不是多个草稿。

当内容在多个平台上相同的情况下，只需创建一个草稿：

```bash
# Specific platforms
./scripts/typefully.js drafts:create --platform x,linkedin --text "Big announcement!"

# All connected platforms
./scripts/typefully.js drafts:create --all --text "Posting everywhere!"
```

**重要提示**：当内容需要针对不同平台进行定制时（例如，在 X 上创建帖子并在 LinkedIn 上发布版本），**仍然只需创建一个草稿**——先在一个平台上创建，然后再进行更新：

```bash
# 1. Create draft with the primary platform first
./scripts/typefully.js drafts:create --platform linkedin --text "Excited to share our new feature..."
# Returns: { "id": "draft-123", ... }

# 2. Update the same draft to add another platform with different content
./scripts/typefully.js drafts:update draft-123 --platform x --text "🧵 Thread time!

---

Here's what we shipped and why it matters..." --use-default
```

因此，请确保除非用户明确要求为每个平台创建单独的草稿，否则切勿创建多个草稿。

## 命令参考

### 用户与社交集合

| 命令 | 描述 |
|---------|-------------|
| `me:get` | 获取已认证的用户信息 |
| `social-sets:list` | 列出您可以访问的所有社交集合 |
| `social-sets:get <id>` | 获取包括连接平台在内的社交集合详细信息 |

### 草稿

所有草稿命令都支持可选的 `[social_set_id]`——如果省略，则使用配置的默认值。
**安全提示**：对于需要 `[social_set_id] <draft_id>` 的命令，如果您仅提供了一个参数（即 `draft_id`），并且配置了默认社交集合，则必须添加 `--use-default` 以明确意图。

| 命令 | 描述 |
|---------|-------------|
| `drafts:list [social_set_id]` | 列出草稿（使用 `--status scheduled` 进行过滤，使用 `--sort` 进行排序） |
| `drafts:get [social_set_id] <draft_id>` | 获取特定草稿的完整内容（如果配置了默认值，则需要使用 `--use-default`） |
| `drafts:create [social_set_id] --text "..."` | 创建新草稿（自动选择平台） |
| `drafts:create [social_set_id] --platform x --text "..."` | 为特定平台创建草稿 |
| `drafts:create [social_set_id] --all --text "..."` | 为所有连接的平台创建草稿 |
| `drafts:create [social_set_id] --file <path>` | 从文件内容创建草稿 |
| `drafts:create ... --media <media_ids>` | 用媒体文件创建草稿 |
| `drafts:create ... --reply-to <url>` | 回复现有的 X 帖子 |
| `drafts:create ... --community <id>` | 在 X 社区中发布帖子 |
| `drafts:create ... --share` | 生成草稿的公共分享链接 |
| `drafts:create ... --scratchpad "..."` | 向草稿中添加内部笔记/便签 |
| `drafts:update [social_set_id] <draft_id> --text "..."` | 更新现有草稿（如果配置了默认值，则需要使用 `--use-default`） |
| `drafts:update [social_set_id] <draft_id> --tags "tag1,tag2"` | 更新现有草稿的标签（内容不变） |
| `drafts:update ... --share` | 生成草稿的公共分享链接 |
| `drafts:update ... --scratchpad "..."` | 更新内部笔记/便签 |
| `drafts:update [social_set_id] <draft_id> --append --text "..."` | 向现有帖子追加内容 |

### 安排与发布

**安全提示**：当使用默认社交集合且仅提供一个参数时，这些命令需要 `--use-default` 以防止因语法不明确而导致的意外操作。

| 命令 | 描述 |
|---------|-------------|
| `drafts:delete <social_set_id> <draft_id>` | 删除草稿（提供明确的 ID） |
| `drafts:delete <draft_id> --use-default` | 使用默认社交集合删除草稿 |
| `drafts:schedule <social_set_id> <draft_id> --time next-free-slot` | 安排到下一个可用时间 |
| `drafts:schedule <draft_id> --time next-free-slot --use-default` | 使用默认社交集合安排时间 |
| `drafts:publish <social_set_id> <draft_id>` | 立即发布 |
| `drafts:publish <draft_id> --use-default` | 使用默认社交集合发布 |

### 标签

| 命令 | 描述 |
|---------|-------------|
| `tags:list [social_set_id]` | 列出所有标签 |
| `tags:create [social_set_id] --name "标签名称"` | 创建新标签 |

### 媒体

| 命令 | 描述 |
|---------|-------------|
| `media:upload [social_set_id] <file_path>` | 上传媒体文件，等待处理后返回媒体 ID |
| `media:upload ... --no-wait` | 立即上传并返回结果（使用 `media:status` 查询状态） |
| `media:upload ... --timeout <seconds>` | 设置自定义超时（默认为 60 秒） |
| `media:status [social_set_id] <media_id>` | 检查媒体上传状态 |

### 设置与配置

| 命令 | 描述 |
|---------|-------------|
| `setup` | 交互式设置——提示输入 API 密钥、存储位置和默认社交集合 |
| `setup --key <key> --location <global\|local>` | 为脚本/CI 提供非交互式设置（如果只有一个社交集合，则自动选择默认值） |
| `setup --key <key> --default-social-set <id>` | 带有明确默认社交集合的非交互式设置 |
| `setup --key <key> --no-default` | 非交互式设置，跳过默认社交集合的选择 |
| `config:show` | 显示当前配置、API 密钥来源和默认社交集合 |
| `config:set-default [social_set_id]` | 设置默认社交集合（如果省略了 ID，则需要交互式操作） |

## 示例

### 设置默认社交集合
```bash
# Check current config
./scripts/typefully.js config:show

# Set default (interactive - lists available social sets)
./scripts/typefully.js config:set-default

# Set default (non-interactive)
./scripts/typefully.js config:set-default 123 --location global
```

### 使用默认社交集合创建推文
```bash
./scripts/typefully.js drafts:create --text "Hello, world!"
```

### 使用明确的 `social_set_id` 创建推文
```bash
./scripts/typefully.js drafts:create 123 --text "Hello, world!"
```

### 创建跨平台帖子
```bash
./scripts/typefully.js drafts:create --platform x,linkedin,threads --text "Big announcement!"
```

### 在所有连接的平台上创建帖子
```bash
./scripts/typefully.js drafts:create --all --text "Posting everywhere!"
```

### 为下一个可用时间安排发布
```bash
./scripts/typefully.js drafts:create --text "Scheduled post" --schedule next-free-slot
```

### 带标签创建帖子
```bash
./scripts/typefully.js drafts:create --text "Marketing post" --tags marketing,product
```

### 按日期排序已安排的帖子
```bash
./scripts/typefully.js drafts:list --status scheduled --sort scheduled_date
```

### 回复推文
```bash
./scripts/typefully.js drafts:create --platform x --text "Great thread!" --reply-to "https://x.com/user/status/123456"
```

### 在 X 社区中发布帖子
```bash
./scripts/typefully.js drafts:create --platform x --text "Community update" --community 1493446837214187523
```

### 创建带有分享链接的草稿
```bash
./scripts/typefully.js drafts:create --text "Check this out" --share
```

### 创建带有便签的草稿
```bash
./scripts/typefully.js drafts:create --text "Launching next week!" --scratchpad "Draft for product launch. Coordinate with marketing team before publishing."
```

### 上传媒体文件并创建帖子
```bash
# Single command handles upload + polling - returns when ready!
./scripts/typefully.js media:upload ./image.jpg
# Returns: {"media_id": "abc-123-def", "status": "ready", "message": "Media uploaded and ready to use"}

# Create post with the media attached
./scripts/typefully.js drafts:create --text "Check out this image!" --media abc-123-def
```

### 上传多个媒体文件
```bash
# Upload each file (each waits for processing)
./scripts/typefully.js media:upload ./photo1.jpg  # Returns media_id: id1
./scripts/typefully.js media:upload ./photo2.jpg  # Returns media_id: id2

# Create post with multiple media (comma-separated)
./scripts/typefully.js drafts:create --text "Photo dump!" --media id1,id2
```

### 向现有草稿添加媒体文件
```bash
# Upload media
./scripts/typefully.js media:upload ./new-image.jpg  # Returns media_id: xyz

# Update draft with media (456 is the draft_id)
./scripts/typefully.js drafts:update 456 --text "Updated post with image" --media xyz --use-default
```

### 交互式设置
```bash
./scripts/typefully.js setup
```

### 为脚本/CI 提供的非交互式设置
```bash
# Auto-selects default social set if only one exists
./scripts/typefully.js setup --key typ_xxx --location global

# With explicit default social set
./scripts/typefully.js setup --key typ_xxx --location global --default-social-set 123

# Skip default social set selection entirely
./scripts/typefully.js setup --key typ_xxx --no-default
```

## 平台名称

使用以下名称作为 `--platform` 选项：
- `x` - X（旧称 Twitter）
- `linkedin` - LinkedIn
- `threads` - Threads
- `bluesky` - Bluesky
- `mastodon` - Mastodon

## 草稿链接

Typefully 的草稿链接包含社交集合和草稿 ID：
```
https://typefully.com/?a=<social_set_id>&d=<draft_id>
```

示例：`https://typefully.com/?a=12345&d=67890`
- `a=12345` → 社交集合 ID
- `d=67890` → 草稿 ID

## 草稿便签

**当用户明确要求在草稿中添加笔记、想法或其他内容时，请使用 `--scratchpad` 标志——切勿写入本地文件！**

`--scratchpad` 选项会将内部笔记直接附加到 Typefully 草稿中。这些笔记：
- 在 Typefully 用户界面中与草稿一起显示
- 永久关联到草稿
- 保持私密状态，不会发布到社交媒体
- 非常适合存储帖子扩展的想法、研究笔记等背景信息

```bash
# CORRECT: Notes attached to the draft in Typefully
./scripts/typefully.js drafts:create 123 --text "My post" --scratchpad "Ideas for expanding: 1) Add stats 2) Include quote"

# WRONG: Do NOT write notes to local files when the user wants them in Typefully
# Writing to /tmp/scratchpad/ or any local file is NOT the same thing
```

## 自动化指南

在自动化发布内容时，尤其是在 X 上，请遵循以下规则以维护账户的良好状态：

- **避免在多个账户上发布重复内容**
- **不要未经请求就自动回复**——仅在用户明确要求时回复
- **不要操纵热门话题**——不要批量发布关于热门话题的内容
- **不要进行虚假互动**——不要自动点赞、转发或关注
- **遵守速率限制**——API 有速率限制，请勿发送大量请求
- **草稿是私有的**——内容在发布或明确分享之前保持私密状态

如有疑问，请先创建草稿供用户审核，而不是直接发布。

**发布确认**：除非用户明确要求“立即发布”或“现在发布”，否则在发布前请务必确认。创建草稿是安全的；发布操作是不可逆的，且会立即公开。

## 提示

- **智能的默认平台选择**：如果省略了 `--platform`，系统会自动选择第一个连接的平台
- **所有平台**：使用 `--all` 一次性发布到所有连接的平台
- **字符限制**：X（280 个字符），LinkedIn（3000 个字符），Threads（500 个字符），Bluesky（300 个字符），Mastodon（500 个字符）
- **创建多条帖子**：在单独的行中使用 `---` 分割内容
- **安排发布时间**：使用 `next-free-slot` 让 Typefully 选择最佳时间
- **跨平台发布**：用逗号分隔多个平台：`--platform x,linkedin`
- **草稿标题**：使用 `--title` 用于内部组织（不会发布到社交媒体）
- **草稿便签**：使用 `--scratchpad` 将笔记附加到草稿中（不要写入本地文件！）——非常适合存储帖子扩展的想法、研究资料等背景信息
- **从文件读取内容**：使用 `--file ./post.txt` 而不是 `--text` 从文件中读取内容
- **排序草稿**：使用 `--sort` 和 `created_at`、`-created_at`、`scheduled_date` 等参数进行排序