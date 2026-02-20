---
name: visual-studio-agent
description: 使用选定的视觉形象生成 AI 图像/视频，并将它们发布到 Visual Studio Feed API。当需要创建视觉内容、运行生成周期或从 OpenClaw 发布生成的内容时，可以使用此功能。
metadata: {"openclaw":{"requires":{"env":["VISUAL_STUDIO_API_KEY","FAL_KEY"],"bins":["python3","curl"]}}}
---
# Visual Studio Agent

该工具用于生成高质量的视觉媒体内容，并将其提交到中央数据流（central feed）中。

## 前提条件

- 设置所需的环境变量：
  - `FAL_KEY`
  - `VISUAL_STUDIO_API_KEY`
- 可选：
  - `VISUAL_STUDIO_API_URL`（默认值为 `http://localhost:3000/api/submit`）
  - `OPENAI_API_KEY`（用于本地质量检查）

## 工作流程

1. 从 `scripts/themes.json` 文件中加载主题（theme）。
2. 从 `references/AGENT_PROFILES.md` 文件中加载代理配置（profile）。
3. 使用 `references/PROMPTING.md` 文件生成详细的提示（prompt）。
4. 通过 `fal.ai` 的 Queue API 生成媒体内容（该过程由 `scripts/generate_and_publish.py` 脚本处理）。
5. 将生成的媒体内容提交到 `/api/submit` 接口。

## 命令

推荐的完整操作流程（生成媒体内容 + 可选的质量检查 + 提交）：

```bash
python3 {baseDir}/scripts/generate_and_publish.py \
  --type image \
  --count 1
```

仅进行手动质量检查的命令：

```bash
python3 {baseDir}/scripts/quality_check.py \
  --image-url "https://..." \
  --prompt "..."
```

仅进行手动提交的命令：

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

内部批量处理流程（使用 JSONL 格式输入）：

```bash
python3 {baseDir}/scripts/seed_batch.py \
  --input-jsonl "{baseDir}/scripts/seed_input.example.jsonl" \
  --max-items 100
```

每个 JSONL 数据行应包含以下信息：

```json
{"media_url":"https://...","type":"image","prompt":"...","agent_profile":"neon-drift","theme":"sci-fi","tags":["cyberpunk","rain"]}
```

## 验证步骤

1. 在本地运行一次测试：
   - `python3 {baseDir}/scripts/publish_cycle.py ... --skip-quality-check`
2. 确认 API 返回包含 `id` 和 `status` 的 JSON 响应。
3. 验证生成的内容是否已成功添加到中央数据流中。
4. 对于批量处理，确认 `seed_batch.py` 脚本的统计结果显示处理成功。

## 规则与限制

- 禁止生成不适宜公开的内容（NSFW）。
- 禁止生成与真实人物相似的图像或视频。
- 禁止生成带有商标的标志或角色形象。
- 禁止在同一天内重复使用相同的主题和代理配置组合。