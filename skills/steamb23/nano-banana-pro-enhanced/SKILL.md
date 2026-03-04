---
name: nano-banana-pro-enhanced
description: 通过 Gemini 3 Pro Image（Nano Banana Pro）生成或编辑图像。
metadata: {"openclaw":{"emoji":"🍌","homepage":"https://ai.google.dev/","primaryEnv":"GEMINI_API_KEY","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---
# Nano Banana Pro（Gemini 3 Pro 图像生成工具）

请使用随附的脚本来生成或编辑图像。

**生成图像：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K --aspect-ratio 16:9
```

**编辑图像：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "/path/in.png" --resolution 2K
```

**批量处理 API（价格便宜 50%，非阻塞式）：**
```bash
# Single image
uv run {baseDir}/scripts/generate_image.py --prompt "description" --filename "output.png" --batch

# Multiple images from JSON file
uv run {baseDir}/scripts/generate_image.py --batch-file .tmp/requests.json

# Check / retrieve result of a previous job
uv run {baseDir}/scripts/generate_image.py --batch-check "batches/abc123" --filename "output.png"
```

**批量处理文件格式（JSON 数组）：**
```json
[
  {
    "prompt": "a cute cat",
    "filename": "cat.png",
    "resolution": "1K",
    "aspect_ratio": "16:9"
  },
  {
    "prompt": "a dog running",
    "filename": "dog.png",
    "resolution": "2K"
  }
]
```

**批量处理注意事项：**
- `--batch` 选项始终为非阻塞式：提交任务后会立即打印 `BATCH_JOB:` 标识符并退出。
- 提交任务后，会在 `HEARTBEAT.md` 文件中添加一个临时检查列表，说明请求该图像的原因（上下文/目的），以便在会话重置后也能清晰了解。
  ```
  # Temporary Check List

  - **Nano Banana Batch job**: <why this image was requested>. Check `batches/abc123` for job result. When ready, retrieve and send to user with mediaUrl parameter. Remove this item after reporting the result.
  ```

- 如果用户明确要求定时检查任务，请使用 cronjob 而不是 `HEARTBEAT.md`。
- 脚本会在 `memory/pending-batch-jobs.json` 文件中记录待处理的任务。该文件在任务提交时创建，在 `--batch-check` 命令执行完成后删除。文件格式为：`[{"job_name", "filename", "prompt", "created_at"}]`。当文件为空时会被删除。

**API 密钥：**
- 使用环境变量 `GEMINI_API_KEY`。
- 或者在 `~/.clawdbot/clawdbot.json` 文件中设置 `skills."nano-banana-pro".apiKey` 或 `skills."nano-banana-pro".env.GEMINI_API_KEY`。

**其他注意事项：**
- 分辨率选项：`1K`（默认）、`2K`、`4K`。
- 宽高比选项：`1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`（仅适用于图像生成，编辑时忽略）。
- 文件名中应包含时间戳：`YYYYMMDD-hhmmss-name.png`。
- 脚本会输出保存后的文件路径。若要通过消息渠道发送图像，请在渠道操作中使用 `mediaUrl` 参数（例如：`mediaUrl: "/absolute/path/to/output.png"`）。
- 请勿重新读取图像文件；只需提供保存路径并通过 `mediaUrl` 将图像发送给用户即可。