---
name: article-illustrator
description: 使用图像生成技术（如GLM或OpenRouter）将剪贴簿风格的插图插入文章中。当用户希望向文章中添加图片、创建带有插图的内容，或者请求“为这篇文章添加插图”、“为这篇帖子生成图片”时，可以使用此功能。
---
# 折页书风格插图生成器

该工具可将文章转换为带插图的Markdown格式，通过生成手绘风格的折页书图片，并将这些图片插入文章中的合适位置。

> **来源说明：** 基于 ViffyGwaanl 的 [glm-image](https://github.com/ViffyGwaanl/glm-image) 库（采用 MIT 许可协议）。

## 设置

随附的 `scripts/generate.py` 脚本支持两种图像生成服务。您至少需要配置其中一种：

### 选项 A：GLM（BigModel / Zhipu AI）——更适合处理中文文本

1. 在 [https://bigmodel.cn](https://bigmodel.cn) 注册账户。
2. 通过以下方式设置 API 密钥：
   - 使用 `export GLM_API_KEY="your-key"`；
   - 将 `"glm_api_key": "your-key"` 添加到 `~/.openclaw/config.json` 文件中；
   - 或将 `GLM_API_KEY=your-key` 添加到技能目录下的 `.env` 文件中。

### 选项 B：OpenRouter——支持更多模型选择，更适合处理英文文本

1. 在 [https://openrouter.ai](https://openrouter.ai) 注册账户。
2. 通过以下方式设置 API 密钥：
   - 使用 `export OPENROUTER_API_KEY="your-key"`；
   - 将 `"openrouter_api_key": "your-key"` 添加到 `~/.openclaw/config.json` 文件中；
   - 或将 `OPENROUTER_API_KEY=your-key` 添加到技能目录下的 `.env` 文件中。
   - 默认使用的 OpenRouter 模型为 `openai/gpt-5-image-mini`（适用于生成高质量的图片）。

**自动检测：** 如果同时配置了两种 API 密钥，系统会优先使用 GLM。您可以使用 `--provider openrouter` 或 `--provider glm` 来指定使用哪种服务。

## 输入参数

- **article**：完整的文章文本（Markdown 或纯文本格式）。
- **image_count**（可选）：要生成的图片数量（2–5 张，默认值为 3 张）。
- **orientation**（可选）：图片方向（`portrait`：1088x1920；`landscape`：1920x1088）。
- **language**（必填）：生成图片中文本的语言（`zh`、`en`、`ja`、`ko`、`fr`、`de`、`es`）。请务必询问用户的选择，切勿自动默认或推断。

## 工作流程

### 第 0 步：检查 API 密钥

快速检查系统中是否已配置 `GLM_API_KEY` 或 `OPENROUTER_API_KEY`。如果未找到密钥，请停止操作并指导用户进行配置（参见上述设置说明）。在没有有效密钥的情况下，请勿继续执行后续步骤。

### 第 1 步：验证输入内容

在生成图片之前：
- 确认文章长度至少为 200 个单词。如果文章太短，提示用户：“文章可能太短，无法生成有意义的插图——是否仍要继续？”
- 统计文章中的主要章节或主题转换点（如 H2 标题、段落分隔处）。这些信息将用于确定图片的插入位置。
- 询问用户希望图片中的文本使用哪种语言。切勿根据文章的原始语言自动推断语言设置。

### 第 2 步：生成图片提示

从 `references/scrapbook-prompt.md` 文件中读取折页书系统的提示信息。

**语言处理规则：**
- 默认情况下（`zh`），生成的图片说明会使用中文。
- 如果指定语言为 `en` 或其他语言，在将数据传递给 `generate.py` 之前，需将所有 `title` 和 `description` 字段的文本翻译为目标语言。同时保持 JSON 数据的结构不变。

根据这些提示信息，分析文章内容并生成一个 JSON 数据结构，用于指导图片生成。

```json
{
  "project_title": "Article title — Scrapbook Style",
  "style": "Physical Mixed-Media Scrapbook",
  "total_images": 3,
  "images": [
    {
      "image_id": 1,
      "title": "Image caption",
      "description": "300-500 character visual description in scrapbook style...",
      "insert_after": "Exact sentence or heading after which to insert the image"
    }
  ]
}
```

每 300–400 个单词的文章内容对应生成一张图片。

### 第 3 步：并行生成所有图片

**重要提示：** 必须同时启动所有图片生成任务。每张图片的生成时间约为 20–40 秒。顺序生成会浪费用户时间。建议使用后台进程或并发执行命令来同时处理所有图片。

对于 JSON 数据结构中的每张图片，分别运行相应的脚本（所有任务需同时执行）：
```bash
# Launch ALL images concurrently — do NOT wait for one to finish before starting the next
python3 scripts/generate.py "<description_1>" --language <lang> --size 1088x1920 &
python3 scripts/generate.py "<description_2>" --language <lang> --size 1088x1920 &
python3 scripts/generate.py "<description_3>" --language <lang> --size 1088x1920 &
wait  # Wait for all to complete
```

在 OpenClaw 代理环境中，建议使用 `exec` 工具进行并发调用（每张图片对应一个任务），而非顺序执行。代理必须在一次操作中完成所有并发调用，以确保图片生成过程能够并行进行。

**额外参数：**
- `--provider glm|openrouter`：用于覆盖自动检测结果。
- `--model <model>`：用于指定使用的 OpenRouter 模型（默认为 `openai/gpt-5-image-mini`）。

脚本会自动执行以下操作：
- （仅针对 OpenRouter）添加边缘裁剪保护代码。
- 在每次生成操作结束后显示每张图片的生成成本。

**异常处理：** 如果某张图片的生成失败，记录错误信息并继续处理剩余的图片。不要终止整个生成过程。在输出结果中标记失败的图片（格式为：`[图片生成失败：<错误信息>]`）。

收集每张成功生成的图片的 URL 或本地路径以及其生成成本。

### 第 4 步：组合最终的 Markdown 文本

将生成的图片按照指定的 `insert_after` 标签插入文章中：

```markdown
![Image caption](image_url)
```

如果未找到 `insert_after` 标签，則将图片插入最近的段落分隔处。

## 输出格式

返回完整的 Markdown 文本，包含：
1. 原始文章的所有内容。
2. 在合适位置插入的图片。
3. 来自 JSON 数据结构的图片说明文字。
4. 文章末尾添加总结信息：`<!-- 生成了 N 张图片，其中 M 张失败，总成本为 $X.XX -->`

## 代理运行方式

该工具由 OpenClaw 主代理会话执行，不会创建子代理。代理会读取文章内容，生成图片生成所需的提示信息，然后依次调用 `generate.py` 脚本，并最终组合成完整的 Markdown 文本。

## 成功标准

满足以下条件即视为成功：
1. 文章内容经过验证（长度符合要求或用户已确认）。
2. 生成了包含 2–5 张图片的 JSON 数据结构。
3. 至少有一张图片生成成功。
4. 最终输出的 Markdown 文本中包含所有插入的图片。

## 异常情况处理：
- **文章太短（<200 个单词）**：提示用户确认是否继续生成。
- **生成失败**：记录错误信息并继续处理其他图片，不要终止整个流程。
- **未找到 `insert_after` 标签**：将图片插入最近的段落分隔处。
- **未配置 API 密钥**：立即显示错误信息并提供配置指南。
- **所有图片生成失败**：返回原始文章内容，并附上错误总结。

## 使用建议：
- 根据文章长度生成 2–5 张图片。
- 将图片插入文章中的主要主题转换点（而非段落中间）。
- 生成的图片说明应严格遵循 `references/scrapbook-prompt.md` 文件中的折页书风格要求。
- 使用 `portrait` 方向（1088x1920）的图片更适合内联显示。
- 使用 OpenRouter 和 `gpt-5-image-mini` 模型时，每张图片的成本约为 0.045–0.050 美元。
- 使用 GLM 模型时，每张图片的成本约为 0.10 元（约合 0.014 美元）。