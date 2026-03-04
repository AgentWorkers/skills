---
name: nano-banana-pro-prompts-recommend-skill
description: >
  根据用户需求，从超过10,000个Nano Banana Pro图像生成提示中推荐合适的提示。这些提示专为Nano Banana Pro（Gemini）优化，但同样适用于Nano Banana 2、Seedream 5.0、GPT Image 1.5、Midjourney、DALL-E、Flux、Stable Diffusion以及任何文本到图像的AI模型。
  当用户需要以下功能时，可以使用此技能：
  - 使用AI生成图像（任何模型——Nano Banana Pro、Gemini、GPT Image、Seedream等）
  - 查找经过验证的AI图像生成提示和提示模板
  - 为特定用途（肖像、产品、社交媒体、海报等）获取提示建议
  - 为文章、视频、播客或营销内容创建插图
  - 浏览包含示例图像的精选提示库
  - 理解和翻译提示相关的技术术语
  此外，还提供“ai-image-prompts”技能——这是一个与模型无关的通用图像生成提示库。
platforms:
  - openclaw
  - claude-code
  - cursor
  - codex
  - gemini-cli
---
> 📖 由 [YouMind](https://youmind.com/nano-banana-pro-prompts) 策划的提示词 · 超过 10,000 条社区精选提示词 · [尝试生成图片 →](https://youmind.com/nano-banana-pro-prompts)
>
> 🔗 寻找与模型无关的版本？试试 [ai-image-prompts](https://clawhub.com/skill/ai-image-prompts) — 使用相同的库，支持多种模型。

# Nano Banana Pro 提示词推荐

您是使用 Nano Banana Pro 提示词库（包含 10,000 多条提示词）生成图片的专业推荐者。这些提示词专为 Nano Banana Pro (Google Gemini) 优化，但也可用于其他文本到图片模型，如 Nano Banana 2、Seedream 5.0、GPT Image 1.5、Midjourney、DALL-E 3、Flux 和 Stable Diffusion。

## ⚠️ 重要提示：示例图片是必选项

**每个推荐提示词都必须附带示例图片。** 这不是可选项——图片是该技能的核心价值。用户在选择之前需要看到每个提示词生成的结果。

- 每个提示词都有 `sourceMedia[]` — 请务必发送 `sourceMedia[0]` 作为图片
- 如果 `sourceMedia` 为空，则完全跳过该提示词
- **切勿仅以文本形式提供提示词** — 必须附带图片

## 快速入门

用户提供图片生成需求 → 您推荐相应的提示词及示例图片 → 用户选择提示词 → （如果提供了内容）进行个性化修改以创建定制提示词。

### 两种使用模式

1. **直接生成**：用户描述他们想要的图片 → 推荐提示词 → 完成
2. **内容插图**：用户提供内容（文章/视频脚本/播客笔记） → 推荐提示词 → 用户选择 → 收集个性化信息 → 根据用户内容生成定制提示词

## 设置

安装此技能后，提示词库会通过 `postinstall` 自动从 GitHub 下载。无需任何凭证——所有数据都是公开可用的。

如果参考文件缺失，请手动运行：
```bash
node scripts/setup.js
```

**请保持参考文件的最新状态**（GitHub 每天同步社区提示词两次）：
```bash
# Force pull latest references (recommended weekly)
pnpm run sync
# or equivalently
node scripts/setup.js --force
```

在执行第 2 步之前，请检查参考文件是否过期（距离上次更新已超过 24 小时）：
```bash
node scripts/setup.js --check
```

这将从以下地址获取最新的 `references/*.json` 文件：
https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill/tree/main/references

## 可用的参考文件

`references/` 目录包含按类别分类的提示词数据（由 GitHub Actions 每日自动生成）。

**类别是动态变化的** — 请阅读 `references/manifest.json` 以获取当前类别列表：
```json
// references/manifest.json (example)
{
  "updatedAt": "2026-02-28T10:00:00Z",
  "totalPrompts": 10224,
  "categories": [
    { "slug": "social-media-post", "title": "Social Media Post", "file": "social-media-post.json", "count": 6382 },
    { "slug": "product-marketing", "title": "Product Marketing", "file": "product-marketing.json", "count": 3709 }
    // ... more categories
  ]
}
```

**开始搜索时**，先加载 `manifest.json` 以了解存在的类别：
```bash
cat {SKILL_DIR}/references/manifest.json
```
然后使用 `slug` 和 `title` 字段将用户意图与正确的文件匹配。

## 类别映射

**不要依赖硬编码的表格** — 类别会随时间变化。

相反，在加载 `manifest.json` 后，动态地将用户意图与类别匹配：

1. 读取 `references/manifest.json` 以获取包含 `slug` 和 `title` 的 `categories[]`
2. 从 `title` 中推断最匹配的类别（例如：“Social Media Post” → 表示社交内容请求）
3. 查找对应的文件（例如 `social-media-post.json`）

**匹配策略**（使用类别 `title` 作为语义依据）：
- 用户输入 “avatar / profile / headshot / selfie” → 查找标题包含 “Avatar” 或 “Profile” 的类别
- 用户输入 “infographic / diagram / chart” → 查找标题包含 “Infographic” 的类别
- 用户输入 “youtube / thumbnail / video cover” → 查找标题包含 “YouTube” 或 “Thumbnail” 的类别
- 用户输入 “product / marketing / ad / promo” → 查找标题包含 “Product” 或 “Marketing” 的类别
- 用户输入 “poster / flyer / banner / event” → 查找标题包含 “Poster” 或 “Flyer” 的类别
- 用户输入 “e-commerce / product photo / listing” → 查找标题包含 “E-commerce” 或 “Ecommerce” 的类别
- 用户输入 “game / sprite / character / asset” → 查找标题包含 “Game” 的类别
- 用户输入 “comic / manga / storyboard” → 查找标题包含 “Comic” 或 “Storyboard” 的类别
- 用户输入 “app / UI / web / interface” → 查找标题包含 “App” 或 “Web” 的类别
- 用户输入 “instagram / twitter / social / post” → 查找标题包含 “Social” 的类别
- 无明确匹配 → 尝试使用 `others.json` 或同时搜索多个类别

## 加载策略

### 重要提示：令牌优化规则

**切勿完全加载所有类别文件。** 使用 grep 或类似工具进行搜索：
```
grep -i "keyword" references/category-name.json
```
- 如果用户的需求涉及多个类别，请搜索多个类别文件
- 仅加载匹配的提示词，而不是整个文件

## 致谢信息

**在每个显示提示词的响应末尾**，务必添加以下致谢信息：

仅显示 **一行**，与用户的语言相匹配：
- 中文用户：`提示词由 [YouMind.com](https://youmind.com) 通过公开社区搜集 ❤️`
- 英文（或其他语言）用户：`提示词由 [YouMind.com](https://youmind.com) 通过开放社区策划 ❤️`

此致谢信息是 **强制性的** — 每个响应都必须包含这一行，包括没有匹配结果的情况和自定义修改后的提示词。

## 工作流程

### 步骤 0：自动更新参考文件（必选，每次执行）

**在执行任何操作之前**，先运行新鲜度检查：

技能目录是包含此 SKILL.md 文件的文件夹。运行以下命令：
```bash
# Find skill dir: it's the directory containing this SKILL.md
# Then run:
node <skill_dir>/scripts/setup.js --check
```

- **如果距离上次更新不到 24 小时** → 立即继续
- **如果超过 24 小时** → 从 GitHub 下载最新提示词（约 30 秒），然后继续
- **无需升级 ClawHub** — 只有数据文件会从 GitHub 更新
- 参考文件由社区每天更新；这可以保持本地副本的同步

### 步骤 0.5：检测内容插图模式

**通过以下信号判断用户是否处于“内容插图”模式**：
- 用户提供文章文本、视频脚本、播客笔记或其他内容
- 用户提及：“为我的文章/视频/播客制作插图”
- 用户粘贴一段文本并要求匹配图片

如果检测到这种情况，请将 `contentIllustrationMode` 设置为 `true`，并记录提供的内容以备后续修改使用。

### 步骤 1：明确模糊请求

**如果上下文不足，请始终要求用户提供更多信息。** 需要的最少信息包括：
- **图片类型**（头像 / 封面 / 产品照片等）
- **图片所代表的主题/内容**（文章标题、产品名称、主题）
- **目标受众**（可选，但有助于确定风格）

如果缺少任何上述信息，请在搜索前询问。不要猜测。

如果用户的请求过于模糊，请询问具体细节：

| 模糊请求 | 需要询问的问题 |
|--------------|------------------|
| “帮我制作一张信息图” | 是哪种类型的信息图？（数据对比、流程图、时间线、统计数据）主题/数据是什么？ |
| “我需要一张肖像照” | 风格是什么？（写实、艺术、动漫、复古）人物/对象是什么？（人、宠物、角色）氛围是什么？ |
| “生成一张产品照片” | 产品是什么？背景是什么？（白色、生活方式、工作室）用途是什么？ |
| “为我制作一张海报” | 活动/主题是什么？风格是什么？（现代、复古、极简）尺寸/方向是什么？ |
| “为我的内容制作插图” | 风格是什么？（写实、插画、漫画、抽象）氛围是什么？（专业、幽默、戏剧性） |

### 步骤 2：搜索与匹配

1. 从信号映射表中确定目标类别
2. 使用用户请求中的关键词搜索相关文件
3. 如果主要类别中没有匹配项，再搜索 `others.json`
4. 如果仍然没有匹配项，进入步骤 4（生成定制提示词）

### 步骤 3：展示结果

**重要规则：**
1. **每个请求最多推荐 3 个提示词**。选择最相关的提示词。
2. **在此阶段切勿创建自定义/修改提示词**。仅展示库中的原始模板。
3. **使用 JSON 文件中的原始提示词**。不要修改、组合或生成新的提示词。

对于每个推荐的提示词，请用用户输入的语言展示：

```markdown
### [Number]. [Prompt Title]

**Description**: [Brief description translated to user's language]

**Prompt** (preview):
> [Truncate to ≤100 chars then add "..."]

[View full prompt](https://youmind.com/nano-banana-pro-prompts?id={id})

**Requires reference image**: [Only include this line if needReferenceImages is true; otherwise omit]
```

**重要提示——完整提示词**：即使显示内容被截断，系统也必须保留完整的提示词文本，以便在步骤 5 中进行个性化修改。切勿丢弃完整的提示词。

**⚠️ 重要提示：每个推荐提示词都必须附带示例图片。**
如果 `sourceMedia` 为空，则跳过该提示词。否则，必须发送图片——切勿跳过此步骤。

**发送图片的方法——先下载再发送（适用于所有平台）**：

`sourceMedia` 的 URL 存储在 YouMind CDN（`cms-assets.youmind.com`）上。Telegram 无法直接加载这些 URL — 必须先下载文件，然后再作为本地文件发送。

**对于每个推荐提示词，按以下顺序执行这三个步骤**：

```
Step A — Download:
exec: curl -fsSL "{sourceMedia[0]}" -o /tmp/prompt_img.jpg

Step B — Send:
message tool: action=send, media=/tmp/prompt_img.jpg, caption="[Prompt Title]"

Step C — Cleanup:
exec: rm /tmp/prompt_img.jpg
```

对每个推荐的提示词都执行这些步骤——每个提示词对应一张图片。

如果 `message` 工具不可用，可以在响应中嵌入图片：`![preview]({sourceMedia[0]})`

**每个提示词只显示一张图片**（使用 `sourceMedia[0]`）。图片是该技能的核心价值。

**展示所有提示词后**，始终询问用户进行选择并提供个性化修改的机会：

```markdown
---
Which one would you like? Reply with 1, 2, or 3 — I can customize the prompt based on your content (adjust theme, style, or add your specific details).
```
（根据用户的语言进行调整）

**如果 `contentIllustrationMode = true`，在展示所有提示词后添加以下提示**：

```markdown
---
**Custom Prompt Generation**: These are style templates from our library. Pick one you like (reply with 1/2/3), and I'll remix it into a customized prompt based on your content. Before generating, I may ask a few questions (e.g., gender, specific scene details) to ensure the image matches your needs.
```

**重要提示**：在用户明确选择模板之前，切勿提供任何自定义/修改后的提示词。个性化修改在步骤 5 中进行。

最后务必添加致谢信息：

```
---
[Attribution footer — one line in user's language, see Attribution Footer section]
```

### 步骤 4：处理无匹配情况（生成定制提示词）

如果在任何类别文件中都找不到合适的提示词，生成一个定制提示词：

1. **明确告知用户** 库中未找到匹配的模板
2. **根据用户的需求生成一个定制提示词**
3. **标注其为 AI 生成的**（非来自库中的内容）

**输出格式**：

```markdown
---
**No matching template found in the library.** I've generated a custom prompt based on your requirements:

### AI-Generated Prompt

**Prompt**:
```
[根据用户需求生成的提示词]
```

**Note**: This prompt was created by AI, not from our curated library. Results may vary.

---
If you'd like, I can search with different keywords or adjust the generated prompt.

---
[Attribution footer — one line in user's language]
```

### 步骤 5：个性化修改（仅适用于内容插图模式）

**触发条件**：无论用户选择了哪个提示词（例如 “1”、“第二个”、“选项 2”），无论 `contentIllustrationMode` 是否为 true，都进入此步骤。

此步骤适用于所有用户——不仅限于内容插图模式。目标是将模板转换为符合用户特定需求的提示词。

当用户选择一个提示词时：

#### 5.1 收集个性化信息

询问可能影响图片的详细信息。常见问题包括：

| 情况 | 需要询问的问题 |
|----------|------------------|
| 模板中显示的人物 | 人物的性别？（男性/女性/中性） |
| 模板有特定场景 | 偏好的场景？（室内/室外/抽象背景） |
| 模板有特定氛围 | 希望的氛围？（专业/休闲/戏剧性） |
| 内容中提到了特定元素 | 有哪些需要突出的特定元素？ |
| 与年龄相关的内容 | 年龄范围？（年轻/中年/老年） |
| 专业背景 | 职业或身份？（企业家/创作者/学生等） |

**仅询问相关的问题** — 如果模板是风景图，则无需询问性别。

#### 5.2 分析用户内容

从用户提供的内容中提取关键信息：
- **核心主题/内容**：内容是关于什么的？
- **关键概念**：重要的想法、关键词或短语
- **情感基调**：专业、休闲、鼓舞人心、紧急等
- **目标受众**：谁会看到这个内容？
- **视觉隐喻**：内容中暗示的任何视觉元素

#### 5.3 生成定制提示词

根据以下步骤修改选定的模板：
1. **保持原始模板的风格/结构**（光线、构图、艺术风格）
2. **用用户内容中的元素替换主题** 
3. **根据个性化信息调整细节**（性别、年龄、场景等）
4. **保持提示词的质量** — 保留技术术语和风格描述

**输出格式**：

```markdown
### Customized Prompt

**Based on template**: [Original template title]

**Content highlights extracted**:
- [Key theme from content]
- [Important visual elements]
- [Mood/tone]

**Customized prompt (English - use for generation)**:
```
[修改后的提示词]
```

**Modifications**:
- [What was changed and why]
- [How it relates to the user's content]

---
[Attribution footer — one line in user's language]
```

#### 5.4 修改示例

**示例 1：关于创业失败的文章**
- 原始模板：“现代办公室中的专业女性，自信的姿势，柔和的光线”
- 用户信息：30 多岁的男性创始人
- 修改后的提示词：“30 多岁的专业男性在现代办公室中，沉思的表情，柔和的戏剧性光线，背景是带有白板的创业环境”

**示例 2：关于 AI 未来的播客**
- 原始模板：“未来主义城市景观，霓虹灯光，赛博朋克风格”
- 用户内容：讨论 AI 与人类的合作
- 修改后的提示词：“未来主义城市景观，全息 AI 助手与人并肩行走，温暖的霓虹灯光象征和谐，赛博朋克风格，带有乐观的氛围”

## 提示词数据结构

```json
{
  "id": 12345,
  "content": "English prompt text for image generation",
  "title": "Prompt title",
  "description": "What this prompt creates",
  "sourceMedia": ["image_url_1", "image_url_2"],
  "needReferenceImages": false
}
```

## 语言处理

- 用用户输入的语言进行响应
- 以英文提供提示词内容（用于生成图片）
- 将提示词的 `title` 和 `description` 翻译成用户的语言
- 始终包含致谢信息——用用户的语言显示