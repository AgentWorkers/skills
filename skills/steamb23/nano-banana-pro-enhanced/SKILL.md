---
name: nano-banana-pro-enhanced
description: 通过 Gemini 3 Pro Image (Nano Banana Pro) 生成或编辑图像。
metadata:
  openclaw:
    emoji: "🍌"
    homepage: https://ai.google.dev/
    primaryEnv: GEMINI_API_KEY
    requires:
      bins: [uv]
      env: [GEMINI_API_KEY]
    install:
      - id: uv-brew
        kind: brew
        formula: uv
        bins: [uv]
        label: "Install uv (brew)"
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

**批量处理 API（价格便宜 50%，非阻塞式）**  
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
- `--batch` 选项始终为非阻塞式：提交任务后会立即打印 `BATCH_JOB:` 标识符并退出程序。  
- 提交任务后，会在 `HEARTBEAT.md` 文件中添加一个临时任务列表。  
  ```
  # Temporary Check List

  - **Nano Banana Batch job**: Check `batches/abc123` for job result. When ready, retrieve and send to user with mediaUrl parameter. Remove this item after reporting the result.
  ```  
- 如果用户明确要求定时检查任务状态，可以使用 cronjob 而不是 `HEARTBEAT.md`。  
- 脚本会将待处理的任务记录在 `memory/pending-batch-jobs.json` 文件中；该文件在任务完成时会自动删除。文件格式为：`[{"job_name", "filename", "prompt", "created_at"}]`。  

**API 密钥：**  
- 使用环境变量 `GEMINI_API_KEY`；  
- 或者在 `~/.clawdbot/clawdbot.json` 文件中设置 `skills."nano-banana-pro".apiKey` 或 `skills."nano-banana-pro".env.GEMINI_API_KEY`。  

**其他说明：**  
- 分辨率选项：`1K`（默认）、`2K`、`4K`。  
- 宽高比选项：`1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`（仅适用于图像生成，编辑时忽略）。  
- 文件名格式：`YYYYMMDD-hhmmss-name.png`（包含时间戳）。  
- 脚本会输出保存后的文件路径；如需通过消息渠道发送图像，请在渠道操作中使用 `mediaUrl` 参数（例如：`mediaUrl: "/absolute/path/to/output.png"`）。  
- 请勿直接读取原始图像文件，只需提供保存后的文件路径并通过 `mediaUrl` 将图像发送给用户即可。