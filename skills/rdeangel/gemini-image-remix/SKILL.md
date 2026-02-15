---
name: gemini-image-remix
description: 使用 Gemini 进行高级图像生成和重新混音。支持 Gemini 2.5 Flash Image（默认设置）以及 Gemini 3.0 Pro（Nano Banana Pro）等模型。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Gemini 图像生成与编辑工具

这是一个功能强大的工具，支持文本到图像的生成以及复杂的图像编辑与合成。默认情况下，它使用 **Gemini 2.5 Flash Image** 模型来快速生成高质量的结果；同时，它也支持更高级的模型（如 **Gemini 3.0 Pro (Nano Banana Pro)**，以完成更复杂的艺术创作任务。

## 图像生成

根据文本提示创建令人惊叹的视觉效果。

```bash
uv run {baseDir}/scripts/remix.py --prompt "a cybernetic owl in a neon forest" --filename "owl.png"
```

## 图像编辑与合成

使用一个或多个参考图像来指导图像的生成过程。非常适合用于风格转换、背景替换或角色修改等操作。

```bash
uv run {baseDir}/scripts/remix.py --prompt "change the art style to a pencil sketch" --filename "sketch.png" -i "original.png"
```

## 多图像合成

可以将最多 14 张不同的图像元素组合成一个连贯的场景。

```bash
uv run {baseDir}/scripts/remix.py --prompt "place the character from image 1 into the environment of image 2" --filename "result.png" -i "character.png" -i "env.png"
```

## 高级模型选择

可以选择更高级的模型（如 **Nano Banana Pro**）来进行高保真度的图像处理。

```bash
uv run {baseDir}/scripts/remix.py --model "gemini-3-pro-image-preview" --prompt "highly detailed oil painting of a dragon" --filename "dragon.png"
```

## 常用选项：

- `--prompt`, `-p`：图像描述或具体的编辑指令。
- `--filename`, `-f`：生成图像的 PNG 文件路径。
- `--input-image`, `-i`：输入图像的路径（最多可重复使用 14 次）。
- `--resolution`, `-r`：分辨率（默认值为 `1K`、`2K` 或 `4K`）。
- `--aspect-ratio`, `-a`：输出图像的宽高比（例如 `1:1`、`16:9`、`9:16`、`4:3`、`3:4`）。
- `--model`, `-m`：要使用的模型（默认为 `gemini-2.5-flash-image`）。支持的模型包括：`gemini-2.5-flash-image`、`gemini-3-pro-image-preview`。
- `--api-key`, `-k`：Gemini API 密钥（默认使用环境变量 `GEMINI_API_KEY`）。