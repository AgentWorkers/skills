---
name: best-image
description: 最高质量的AI图像生成服务（每张图片的成本约为0.12-0.20美元）。支持通过EvoLink API实现文本到图像、图像到图像以及图像编辑的功能。
homepage: https://evolink.ai
metadata: {"openclaw": {"emoji": "🎨", "requires": {"env": ["EVOLINK_API_KEY"]}, "primaryEnv": "EVOLINK_API_KEY"}}
---
# EvoLink 最佳图片生成与编辑工具

通过 EvoLink Nano Banana Pro (gemini-3-pro-image-preview) API 生成和编辑图片。

## 使用方法

建议先尝试使用 Python（无需额外依赖，支持所有平台）：

```bash
python3 {baseDir}/scripts/generate.py --prompt "一只可爱的猫" --size "auto"
```

可选参数：
- `--size`：自动选择（auto）、1:1、2:3、3:2、3:4、4:3、4:5、5:4、9:16、16:9、21:9
- `--quality`：1K、2K、4K
- `--image-urls`：多个图片的 URL（格式：jpeg/jpg/png/webp）

如果无法使用 Python：

- **Windows**：请参考 `{baseDir}/references/powershell.md` 中的 PowerShell 替代方案
- **Unix/macOS**：请参考 `{baseDir}/references/curl_heredoc.md` 中的 curl 替代方案

## API 密钥

- 必需设置环境变量 `EVOLINK_API_KEY`，可通过 [https://evolink.ai] 获取密钥

## 使用指令

- **中文指令**：`最佳图片生成：xxx` / `编辑图片：xxx`
- **英文指令**：`best image: xxx` / `edit image: xxx`

指令后的内容将被视为提示（`prompt`），默认使用自动选择的尺寸（`auto`）和 2K 的质量进行图片生成。

在进行图片转换或编辑时，用户需要提供图片的 URL。

## 注意事项：

- 脚本会输出 `MEDIA:<path>` 作为图片的存储路径，无需额外处理即可自动上传到 OC（OpenClaw）。
- 图片会保存在本地（格式根据 URL 自动检测为 png/jpg/webp）；URL 有效期约为 24 小时，但本地文件会永久保存。
- 使用 `--quality 4K` 会产生额外费用。
- `--image-urls` 参数最多支持 10 个图片 URL（每张图片大小不超过 10MB，格式为 jpeg/jpg/png/webp）。