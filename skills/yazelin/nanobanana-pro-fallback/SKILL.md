---
name: nanobanana-pro-fallback
description: "**Nano Banana Pro**：支持自动模型回退机制，可通过 **Gemini Image API** 生成或编辑图像。使用命令行运行：  
`uv run {baseDir}/scripts/generate_image.py --prompt 'desc' --filename 'out.png' [--resolution 1K|2K|4K] [-i input.png]`  
支持 **文本到图像** 以及 **图像到图像** 的转换（最多支持 14 种转换方式），支持 1K、2K、4K 分辨率。  
回退流程为：`gemini-2.5-flash-image → gemini-2.0-flash-exp`。  
必须使用 `uv run` 命令执行，不可使用 `python3`。"
version: 0.4.4
license: MIT
homepage: https://github.com/yazelin/nanobanana-pro
author: yazelin
compatibility:
  platforms:
    - openclaw
    - ching-tech-os
metadata:
  openclaw:
    emoji: "🍌"
    requires:
      bins: ["uv"]
      env: ["GEMINI_API_KEY"]
    primaryEnv: GEMINI_API_KEY
    install:
      - id: uv-brew
        kind: brew
        formula: uv
        bins: ["uv"]
        label: "Install uv (brew)"
  ctos:
    requires_app: ""
    mcp_servers: ""
---

# Nano Banana Pro（带回退机制）

使用随附的脚本生成或编辑图像。如果某个 Gemini 模型失败，系统会自动尝试其他模型。

⚠️ **重要提示：必须使用 `uv run` 或 `generate` 包装器脚本，切勿直接使用 `python3`——否则相关依赖项将无法被加载。**

**生成图像（选项 A：使用包装器脚本）**  
```bash
{baseDir}/scripts/generate --prompt "your image description" --filename "output.png" --resolution 1K
```

**生成图像（选项 B：使用 `uv run`）**  
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png" --resolution 1K
```

**编辑单张图像**  
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "edit instructions" --filename "output.png" -i "/path/in.png" --resolution 2K
```

**多张图像合成（最多 14 张图像）**  
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "combine these into one scene" --filename "output.png" -i img1.png -i img2.png -i img3.png
```

**API 密钥**  
- 使用环境变量 `GEMINI_API_KEY`  
- 或者在 `~/.openclaw/openclaw.json` 文件中设置 `skills."nanobanana-pro-fallback".apiKey` 或 `skills."nanobanana-pro-fallback".env.GEMINI_API_KEY`  

**注意事项**  
- 分辨率选项：`1K`（默认）、`2K`、`4K`  
- 模型的使用顺序：`gemini-2.5-flash-image` → `gemini-2.0-flash-exp-image-generation`（可通过环境变量 `NANOBANANA_FALLBACK_MODELS` 进行配置）  
- 文件名格式：`yyyy-mm-dd-hh-mm-ss-name.png`  
- 脚本会输出 `MEDIA:` 行，以便 OpenClaw 在支持的聊天平台上自动显示图像  
- 请勿直接读取生成的图像文件，只需返回其保存路径即可。