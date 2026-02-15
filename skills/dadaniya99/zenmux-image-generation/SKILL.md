---
name: zenmux-image-generation
description: 通过 ZenMux API（Pro/Elite）生成图像。支持文本转图像、图像转图像以及多图像融合功能。
---

# ZenMux 图像生成技能（Gemini 3 Pro）

该技能使用 ZenMux API，基于 **Gemini 3 Pro Image (Nano Banana Pro)** 模型生成高保真度的图像。

## 功能

*   **文本转图像**：根据描述性提示生成视觉效果。
*   **图像转图像**：根据提示修改现有图像。
*   **多图像融合**：结合多个参考图像的元素或风格（例如，从一张图像中提取字符，从另一张图像中提取服装/风格）。

## 使用方法

要生成图像，请执行 `scripts/generate.py` 脚本。

**重要提示：**
*   必须设置 `ZENMUX_API_KEY` 环境变量。
*   **模型**：默认值为 `google/gemini-3-pro-image-preview`。
*   **服务提供商**：ZenMux（需要 **Pro** 或更高级别的订阅计划）。

### 1. 文本转图像
```bash
ZENMUX_API_KEY="YOUR_KEY" python3 scripts/generate.py --prompt "a cybernetic lobster in space"
```

### 2. 图像转图像
```bash
ZENMUX_API_KEY="YOUR_KEY" python3 scripts/generate.py --prompt "make it winter" --images "summer.png"
```

### 3. 多图像融合（高级）
```bash
ZENMUX_API_KEY="YOUR_KEY" python3 scripts/generate.py --prompt "put this child in this costume" --images "child.png" "costume.jpg"
```

### 参数

*   `--prompt`（必选）：任务的文字描述。
*   `--images`（可选）：一个或多个参考图像文件的路径。
*   `--model`（可选）：默认值为 `google/gemini-3-pro-image-preview`。
*   `--output`（可选）：默认值为 `generated_image.png`。