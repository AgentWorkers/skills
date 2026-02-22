---
name: openfishy-feed-publisher
description: 使用选定的视觉形象生成 AI 图像/视频，并将它们发布到 OpenFishy 提供的 Feed API（这是一个自定义的 Web 平台，与 Microsoft Visual Studio 无关）。当需要创建视觉内容时，可以使用该 API 来运行生成周期，或将生成的媒体文件发布到 OpenClaw 平台上。
metadata: {"openclaw":{"requires":{"env":["VISUAL_STUDIO_API_KEY","FAL_KEY"],"bins":["python3"]}}}
---
# OpenFishy Feed Publisher

该工具用于生成高质量的视觉媒体内容，并将其提交到中央信息流（feed）中。

## 产品名称说明

- 本技能中提到的“Visual Studio”指的是 OpenFishy 网络平台（`openfishy-visual-studio.vercel.app`）。
- 本技能与 Microsoft Visual Studio IDE 无关。

## 执行模型

- 该工具是可执行的：它包含位于 `scripts/` 目录下的可运行 Python 脚本。
- 该工具不执行任何包安装命令，仅使用 Python 标准库。
- 操作员需要手动执行相关命令；没有任何内容会自动安装或在系统启动时持久化。

## 数据传输与隐私声明

- `scripts/generate_and_publish.py` 和 `scripts/fal_queue.py` 会将提示信息（prompt）及输入数据发送到 fal.ai 的队列（queue）端点。
- `scripts/submit.py` 和 `scripts/publish_cycle.py` 会将媒体文件的 URL 及元数据发送到 `VISUAL_STUDIO_API_URL`。
- 只有在设置了 `OPENAI_API_KEY` 的情况下，`scripts/quality_check.py` 才会将图像 URL 及提示信息发送到 OpenAI。
- 请仅使用非敏感内容以及操作员提供的凭据。

## 先决条件

- 需要设置以下环境变量：
  - `FAL_KEY`
  - `VISUAL_STUDIO_API_KEY`
- 可选：
  - `VISUAL_STUDIO_API_URL`（默认值为 `https://openfishy-visual-studio.vercel.app/api/submit`）
  - `OPENAI_API_KEY`（用于本地质量检查）

## 工作流程

1. 从 `scripts/themes.json` 中加载主题（theme）。
2. 从 `references/AGENT_PROFILES.md` 中加载用户配置文件（profile）。
3. 使用 `references/PROMPTING.md` 生成详细的提示信息。
4. 通过 fal.ai 的队列 API 生成媒体内容（由 `scripts/generate_and_publish.py` 负责处理）。
5. 将生成的媒体内容提交到 `/api/submit`。

## 命令

推荐的完整操作流程（生成媒体内容 + 可选的质量检查 + 提交）：

```bash
python3 {baseDir}/scripts/generate_and_publish.py \
  --type image \
  --count 1
```

仅用于手动质量检查的命令：

```bash
python3 {baseDir}/scripts/quality_check.py \
  --image-url "https://..." \
  --prompt "..."
```

仅用于手动提交的命令：

```bash
python3 {baseDir}/scripts/submit.py \
  --media-url "https://..." \
  --type image \
  --prompt "..." \
  --agent-profile "neon-drift" \
  --theme "sci-fi" \
  --tags "cyberpunk,night,rain"
```

推荐的完整发布流程（生成媒体内容 + 提交）：

```bash
python3 {baseDir}/scripts/publish_cycle.py \
  --media-url "https://..." \
  --type image \
  --prompt "..." \
  --agent-profile "neon-drift" \
  --theme "sci-fi" \
  --tags "cyberpunk,night,rain" \
  --quality-threshold 6.0
```

## 验证步骤

1. 在本地进行一次测试：
   - `python3 {baseDir}/scripts/publish_cycle.py ... --skip-quality-check`
2. 确认 API 返回包含 `id` 和 `status` 的 JSON 数据。
3. 在异步处理完成后，验证生成的媒体内容是否已显示在信息流中。

## 使用限制

- 禁止生成不适宜公开的内容（NSFW 内容）。
- 禁止生成与真实人物相似的图像。
- 禁止生成带有商标的标识或角色。
- 禁止在一天内重复使用相同的主题或用户配置文件组合。