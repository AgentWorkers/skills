---
name: sora
description: 使用 OpenAI 的 Sora API 生成视频。当用户请求根据文本提示或参考图像生成、创建或制作视频时，可以使用该 API。该 API 支持图像到视频的转换，并能自动调整视频大小。
---

# Sora 视频生成

使用 OpenAI 的 Sora API 生成视频。

## API 参考

**端点：** `POST https://api.openai.com/v1/videos`

### 参数

| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `prompt` | 字符串 | 视频的文字描述（必填） |
| `input_reference` | 文件 | 可选的参考图像（用于指导视频生成） |
| `model` | `sora-2`, `sora-2-pro` | 使用的模型（默认：sora-2） |
| `seconds` | `4`, `8`, `12` | 视频时长（默认：4 秒） |
| `size` | `720x1280`, `1280x720`, `1024x1792`, `1792x1024` | 输出分辨率 |

### 重要说明

- **图像尺寸必须与视频尺寸完全匹配** —— 脚本会自动调整图像大小 |
- 视频生成通常需要 1-3 分钟 |
- 视频在大约 1 小时后失效 —— 请立即下载

## 使用方法

```bash
# Basic text-to-video
uv run ~/.clawdbot/skills/sora/scripts/generate_video.py \
  --prompt "A cat playing piano" \
  --filename "output.mp4"

# Image-to-video (auto-resizes image)
uv run ~/.clawdbot/skills/sora/scripts/generate_video.py \
  --prompt "Slow dolly shot, steam rising, warm lighting" \
  --filename "output.mp4" \
  --input-image "reference.png" \
  --seconds 8 \
  --size 720x1280

# With specific model
uv run ~/.clawdbot/skills/sora/scripts/generate_video.py \
  --prompt "Cinematic scene" \
  --filename "output.mp4" \
  --model sora-2-pro \
  --seconds 12
```

## 脚本参数

| 参数 | 描述 | 默认值 |
|------|-------------|---------|
| `--prompt`, `-p` | 视频描述（必填） | - |
| `--filename`, `-f` | 输出文件路径（必填） | - |
| `--input-image`, `-i` | 参考图像路径 | 无 |
| `--seconds`, `-s` | 视频时长（4 秒、8 秒或 12 秒） | 8 秒 |
| `--size`, `-sz` | 分辨率 | 720x1280 |
| `--model`, `-m` | 使用的模型（sora-2 或 sora-2-pro） | sora-2 |
| `--api-key`, `-k` | OpenAI API 密钥 | 环境变量 |
| `--poll-interval` | 每 N 秒检查一次状态 | 10 秒 |

## API 密钥

设置 `OPENAI_API_KEY` 环境变量或通过 `--api-key` 传递 API 密钥。

## 视频提示的编写技巧

### 优秀的提示示例包括：

1. **相机运动**：推拉、平移、缩放、跟踪拍摄
2. **动作描述**：旋转、上升、下降、移动
3. **光线效果**：黄金时刻、烛光、戏剧性的边缘光线
4. **氛围**：蒸汽、粒子效果、散景、雾气
5. **风格/情绪**：电影风格、商业风格、生活方式风格、编辑风格

### 示例提示：

**食品广告：**
```
Slow dolly shot of gourmet dish, soft morning sunlight streaming through window, 
subtle steam rising, warm cozy atmosphere, premium food commercial aesthetic
```

**生活方式风格：**
```
Golden hour light slowly shifting across mountains, gentle breeze rustling leaves, 
serene morning atmosphere, premium lifestyle commercial
```

**产品拍摄：**
```
Cinematic close-up, dramatic lighting with warm highlights, 
slow reveal, luxury commercial style
```

## 工作流程：图像 → 视频

1. 使用 Nano Banana Pro 生成图像（或使用现有图像）
2. 将图像作为 `--input-image` 参数传递给 Sora API
3. 编写描述所需动作/氛围的提示
4. 脚本会自动调整图像大小以匹配视频尺寸

## 输出结果

- 视频保存为 MP4 格式
- 通常文件大小为 1.5-3MB（8 秒视频）
- 分辨率与 `--size` 参数设置一致