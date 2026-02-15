---
name: yt-to-blog
description: >
  Full content pipeline: YouTube URL → transcript → blog post → Substack draft → X/Twitter thread →
  vertical video clips via HeyGen AI avatar. One URL in, entire content suite out. Use when asked to:
  "turn this video into content", "create a content suite from this YouTube video", "write a blog from
  this video", "repurpose this video", or any video-to-multi-platform content request.
  Can run the full pipeline or individual steps.
---

# YT-to-Blog 内容生成工具

将 YouTube 视频内容转换为博客文章、Substack 发文、Twitter 推文以及竖屏视频片段。这是一个完整的 content 处理流程。

## 流程概述

**一个输入 URL，五个输出平台。** 可以整体运行整个流程，也可以单独运行其中任意步骤。

---

## 首次使用设置向导

首次使用时，会引导用户完成设置流程。整个过程大约需要 10 分钟，之后就无需再次操作了。

### 第 1 步：检查依赖项

运行设置脚本以确认已安装的软件：

**所需命令行工具：**
| 工具 | 用途 | 安装方式 |
|------|---------|---------|
| `summarize` | 提取 YouTube 视频字幕 | `brew install steipete/tap/summarize` |
| `bird` | 发布到 X/Twitter | `brew install steipete/tap/bird` |
| `ffmpeg` | 视频后期处理 | `brew install ffmpeg` |
| `curl` | 与 HeyGen 进行 API 请求 | 通常已在 macOS 上预装 |
| `python3` | 辅助脚本 | 通常已在 macOS 上预装 |

如果缺少任何工具，请告知用户需要安装的内容，并等待用户确认。

### 第 2 步：获取 HeyGen API 密钥

1. 告诉用户：“访问 https://app.heygen.com/settings，从 API 部分获取您的 API 密钥。”
2. 如果用户还没有 HeyGen 账户：“请在 https://heygen.com 注册——免费账户可提供一些信用额度供测试使用。”
3. 将密钥保存到 `config.json` 文件中（具体配置结构见下方）。
4. 测试 API 密钥是否有效：

---

### 第 3 步：设置 HeyGen 虚拟形象

告知用户：

> “对于竖屏视频片段，您需要一个 HeyGen 虚拟形象。需要注意以下几点：
>
> **请以 **肖像模式** 录制视频**（将手机竖立放置）。这一点非常重要——如果以横屏模式录制，虚拟形象会显示为 9:16 比例画面中的小条状图像，此时需要对其进行裁剪或缩放（虽然可以处理，但可能会损失画质）。
>
> 访问 https://app.heygen.com/avatars → 创建虚拟形象 → 按照提示进行录制。确保录制环境光线良好，直视镜头，自然地讲话 2 分钟以上。
>
> 创建完成后，从虚拟形象详情页面获取您的虚拟形象 ID。”

列出用户现有的虚拟形象供其选择。注意：虚拟形象页面会显示自定义和默认提供的虚拟形象——请筛选出用户自定义的虚拟形象（它们通常会排在最前面，并带有个人名称）：

---

### 第 4 步：克隆 HeyGen 语音

告知用户：

> “访问 https://app.heygen.com/voice-clone → 克隆您的语音。上传一段 1-2 分钟的自然讲话音频样本。HeyGen 会生成一个语音 ID。”
>
> 完成后，从语音设置页面获取您的语音 ID。”

列出用户可用的语音选项。用户克隆的语音通常会显示在列表的最前面；默认提供的语音则排在后面：

---

**重要提示：** 请使用完整的语音 ID（例如 `69da9c9bca78499b98fdac698d2a20cd`），切勿使用缩略版本。如果使用简短的 ID，API 会返回 “语音验证失败”的错误信息。

### 第 5 步：登录 Substack

Substack 没有官方 API — 需要通过浏览器自动化完成发文操作。

1. 打开 OpenClaw 管理的浏览器：使用 `profile="openclaw"` 打开浏览器。
2. 访问 `https://substack.com/sign-in` 并使用用户凭据登录。
3. 确认用户已成功登录后，导航到用户的发布页面。
4. 将发布链接保存到 `config.json` 文件中。

浏览器会话在重启后仍然有效。设置只需完成一次。

### 第 6 步：保存配置

创建 `skills/yt-content-engine/config.json` 文件（位于工作区目录下）：

**提示：** 如果用户之前使用过 `yt-to-blog` 技能并已有语音文件，请从 `skills/yt-to-blog/references/voice-guide.md` 中读取相关内容，并将其用于 `author.voice` 字段。

### 第 7 步：验证所有设置

使用已保存的配置再次运行设置脚本：

脚本会检测每个组件的运行状态，并输出相应的结果。

---

## 使用方法

### 整体流程

---

### 单个步骤

---

## 流程步骤

### 第 ①：提取字幕

为本次操作创建输出目录，然后获取 YouTube 视频的字幕：

**使用 `summarize` 工具提取字幕：**

`--extract` 选项会输出未经 LLM 摘要处理的原始字幕。如果提取失败（字幕不可用），可以尝试使用 `--youtube yt-dlp` 命令自动生成字幕，或者让用户提供手动字幕。

---

### 第 ②：编写博客草稿

将提取的字幕转换为格式规范的博客文章。

**从 `config.json` 中读取作者的语音文件（`authorvoice`）。如果 `skills/yt-to-blog/references/voice-guide.md` 中有更详细的发音指南，请参考该指南。**

**写作步骤：**
- **开头部分（1-3 段落）**：设置场景，使用具体的描述和情感元素吸引读者注意力。
- **主题阐述（1 段落）**：将场景与文章主题联系起来。
- **数据部分（5-15 段落）**：交替呈现数据和评论性内容。每个数据点都要有简洁的总结。
- **呼应开头（1-2 段落）**：回到开头场景或使用比喻来强化主题。
- **结尾部分（3-6 段落）**：通过有力的结论收尾。

**写作规则：**
- 句子长度要有所变化——数据部分使用长句，结尾部分使用短句。
- 使用破折号（`–`）表示旁白，不要使用括号。
- 通过短句强调重点内容。
- 正文中不要使用项目符号列表，保持叙述的连贯性。
- 直接在文本中插入链接，不要使用脚注。
- 不要使用 “总结” 或 “最后说明” 等语句。
- 自然地引用视频来源：“正如 [作者名称] 所说...” 并附上链接。
- 文章字数建议在 1,500-3,000 字之间。

**生成 3-5 个不同的标题选项**，每个标题都应具有独特的表达方式（如对比、反讽、揭示真相或呼应开头）。让用户自行选择最终标题。

将最终草稿保存到输出文件夹中的 `blog.md` 文件中。

---

### 第 ③：发布到 Substack

通过浏览器自动化将博客文章发布到 Substack：

1. 读取 `config.json` 中的 `substack.publication` 配置。
2. 使用 `profile="openclaw"` 打开浏览器。
3. 访问 `https://PUBLICATION.substack.com/publish/post`。
4. 点击标题字段输入标题。
5. 点击标题下方的文本框输入副标题。
6. 在编辑器中编写博客内容（可以使用 `pbcopy < /tmp/post.md` 将内容复制到剪贴板）。
7. Substack 会自动将文章保存为草稿状态。

**注意事项：**
- 在复制粘贴过程中，破折号（`–`）可能会被误显示为逗号或特殊字符。粘贴后请检查并修正。
- 对于较长的文章，粘贴和验证之间可能需要稍作等待。
- 在发布前请在 `https://PUBLICATION.substack.com/publish` 确认文章是否已保存成功。

将 Substack 的发布链接保存到 `output/substack-url.txt` 文件中。

---

### 第 ④：发布到 X/Twitter

使用 `bird` 命令行工具发布推文：

**推文/帖子内容：**
- 如果文章有一个引人注目的亮点，可以发布一条包含链接的推文。
- 如果文章有多个亮点，可以发布多条推文（每条推文包含链接）。
- 确保推文使用与作者一致的语气。
- 使用 `config.json` 中的 `twitter.handle` 作为推文账号。

**使用 `bird` 命令发布推文：**

**发布推文前务必先向用户展示推文内容并获取确认。**

将推文内容保存到 `output/tweet.txt` 文件中。

---

### 第 ④b：发布到 Facebook 群组（可选）

如果 `config.json` 中包含 `facebook.group` 配置，提醒用户将文章发布到对应的 Facebook 群组。

**注意：** Facebook 群组的 API 发布功能受到严格限制。由于 Facebook 的反机器人机制，使用浏览器自动化工具可能不可靠。最佳方法是：
1. 先编写一篇简短、更随意的 Facebook 发文内容。
2. 将内容保存到 `output/facebook-post.txt` 文件中。
3. 提醒用户：“别忘了将文章发布到 [群组名称]！”
4. 用户手动在 Facebook 上发布文章。

这样可以在不违反 Facebook 规定的情况下完成内容分发。

---

### 第 ⑤：将博客内容转换为竖屏视频脚本

从博客文章中提取 3-5 个引人注目的片段，并将其转换为适合竖屏视频的脚本。

**提取要点：**
- **引人注目的观点或争议性内容**：最能吸引读者注意力的部分。
- **令人惊讶的数据或事实**：能够改变读者理解的内容。
- **反常规的观点**：与普遍认知相悖的观点。
- **情感性内容**：能够引起共鸣的故事、轶事或人物元素。
- **行动号召**：鼓励读者采取行动的呼吁或建议。

**脚本编写规则：**
- **以最吸引人的内容开头**：直接进入主题，无需冗长的引言。
- **口语化表达**：为朗读而写作，避免使用复杂的句子结构。
- 每个脚本长度控制在 30-60 秒左右。
- 每个脚本必须独立成篇，不要包含 “如前所述” 等过渡性语句。
- 以有力的结尾收尾。

**脚本格式：**
使用 `config.json` 中的 `video.clipCount`（默认值为 5）和 `video.maxClipSeconds`（默认值为 60 秒）来设置脚本数量和每个脚本的最大时长。

将生成的脚本保存到 `output/scripts/clip-1.txt` 等文件中。

---

### 第 ⑥：使用 HeyGen 生成视频

将每个脚本提交给 HeyGen API 生成 AI 制作的虚拟形象视频。

**配置文件说明：**
---

**为每个脚本提交视频生成请求：**

**解析响应以获取视频 ID：**

**在提交所有脚本后统一等待视频生成结果。** HeyGen 会并行处理所有脚本，因此先提交所有脚本，然后再统一获取所有视频 ID。这样可以将总处理时间从 N×3 分钟缩短到约 3 分钟。

**定期检查生成进度（每 15 秒检查一次，超时后显示 `failed`）。**

**状态显示：** `pending` → `processing` → `completed`（附带视频链接）或 `failed`（附带错误信息）。

**下载生成的视频：**

**注意：** 每分钟视频生成大约需要 1 个信用额度。如果生成 5 个视频，大约需要 3 个信用额度。在提交前请告知用户相关费用。

---

### 第 ⑦：视频后期处理

如果虚拟形象是横屏录制的，生成的 9:16 比例视频中虚拟形象可能会显示为小条状图像。可以使用 `ffmpeg` 对视频进行裁剪和调整：

**检查 `config.json` 中的 `video.cropMode` 配置：**
- `"auto"`：自动检测并裁剪。
- `"portrait"`：跳过裁剪（虚拟形象是横屏录制的）。
- `"manual"`：要求用户提供裁剪坐标。

**自动裁剪流程：**

**如果自动裁剪失败（尤其是背景为白色或浅色时），可以手动调整裁剪方式：**

HeyGen 通常会将横屏录制的虚拟形象显示在 9:16 比例的白色或浅色背景中。可以通过扫描视频中心区域来找到实际的有效内容区域，并进行裁剪。

**裁剪后的视频保存路径：**

将处理后的视频保存到 `output/videos/clip-1.mp4` 等文件中。

---

### 第 ⑧：整理输出文件

将所有处理后的文件整理到一个带有日期标记的输出文件夹中：

**输出文件结构：**

**配置文件：** `manifest.json`

**向用户报告处理结果：**
- ✅ 博客文章：X 字
- ✅ Substack 发文：[链接]（草稿/已发布）
- ✅ Twitter 推文：已发布/待发布
- ✅ 生成并处理了 X 个视频片段
- 💰 使用的 HeyGen 信用额度：约 X 个

---

## 配置文件参考

配置文件：`skills/yt-content-engine/config.json`（位于工作区根目录下）

| 配置项 | 说明 | 默认值 |
|------|-------------|---------|
| `heygen.apiKey` | HeyGen API 密钥 | 必需 |
| `heygen.avatarId` | 用户的 HeyGen 虚拟形象 ID | 必需 |
| `heygen.voiceId` | 用户克隆的语音 ID | 必需 |
| `substack.publication` | Substack 发文平台域名 | 必需 |
| `twitter.handle` | X/Twitter 账号 | 必需 |
| `authorVOICE` | 作者的发音风格描述 | 建议设置 |
| `author.name` | 作者姓名（用于署名） | 建议设置 |
| `video.clipCount` | 需要生成的视频片段数量 | 5 |
| `video.maxClipSeconds` | 每个视频的最大时长 | 60 秒 |
| `video.cropMode` | `auto`（自动裁剪）、`portrait`（竖屏裁剪）或 `manual`（手动裁剪） | `auto` |

---

## 提示与故障排除

- **HeyGen 生成视频需要 2-3 分钟每个片段。** 请用户做好心理准备，5 个片段的整个处理过程大约需要 10-15 分钟。
- **使用竖屏虚拟形象可以节省时间**：如果经常使用该功能，建议重新录制视频以避免裁剪步骤。
- 如果 Substack 登录失效，请重新执行步骤 5（登录操作）。
- 如果 `bird` 命令行工具无法正常发布推文，请运行 `bird auth` 命令重新认证。
- 如果裁剪效果不佳，可以将 `cropMode` 更改为 `manual` 并手动调整视频边界。
- 如果遇到 HeyGen 的使用额度限制，请查看 `https://app.heygen.com/settings` 以获取更多信息或调整片段数量。
- 如果无法获取字幕，可以尝试使用 `summarize "URL" --extract --youtube yt-dlp` 命令自动生成字幕，或让用户提供手动字幕。