---
name: nano-banana-pro
description: 通过 Gemini 3 Pro Image（Nano Banana Pro）生成或编辑图像。
homepage: https://ai.google.dev/
metadata: {"openclaw":{"emoji":"🍌","requires":{"bins":["uv"],"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Nano Banana Pro（Gemini 3 Pro 镜像）

使用随附的脚本来生成或编辑图像。

**生成镜像：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

**编辑单个图像：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" -i "/path/in.png" --resolution 2K
```

**多图像合成（最多 14 张图像）：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

**API 密钥：**
- 使用环境变量 `GEMINI_API_KEY`
- 或者在 `~/.clawdbot/openclaw.json` 文件中设置 `skills."nano-banana-pro".apiKey` 或 `skills."nano-banana-pro".env.GEMINI_API_KEY`

**注意事项：**
- 分辨率选项：`1K`（默认）、`2K`、`4K`。
- 文件名格式：`yyyy-mm-dd-hh-mm-ss-name.png`。
- 脚本会输出一行 `MEDIA:`，以便 OpenClaw 在支持的聊天平台上自动插入该图像。
- 请勿读取已保存的图像文件，只需提供其保存路径即可。