---
name: video-gen
description: 使用腾讯云VOD的AIGC模型（如Kling、Vidu、Hailuo等）生成视频。现已支持完整的API接口。
---

# 视频生成技能（VOD AIGC）

该技能使用腾讯云VOD AIGC API生成高质量的人工智能视频，支持**文本转视频（Text-to-Video, T2V）**和**图像转视频（Image-to-Video, I2V）**功能，支持多种模型。

## 支持的模型
- **Kling** (1.6, 2.0, 2.1, 2.5, 2.6, o1)
- **Hailuo** (02, 2.3)
- **Vidu** (q2, q2-turbo, q2-pro)
- **Jimeng** (3.0pro)
- **Seedance** (1.0-pro, 1.5-pro, 等)
- **GV** (3.1)
- **OS** (2.0)

## 使用方法

```bash
node skills/video-gen/index.js "<Prompt>" [options]
```

### 参数选项

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--model <名称>` | 模型名称（如Kling、Hailuo、Vidu等） | Kling |
| `--model-version <版本>` | 模型版本（例如2.1、2.5） | 2.5 |
| `--image <URL>` | 用于图像转视频的参考图片URL | 无 |
| `--last-frame <URL>` | 最后一帧图片URL（适用于Kling 2.1、Vidu、GV） | 无 |
| `--resolution <分辨率>` | 720P、1080P、2K、4K | 1080P |
| `--ratio <宽高比>` | 16:9、9:16、1:1 | 16:9 |
| `--enhance` | 启用提示增强功能 | 禁用 |
| `--chat-id <ID>` | 用于显示进度信息的Feishu聊天ID | 无 |

### 示例

**1. 基本的文本转视频（使用Kling 2.5模型）**
```bash
node skills/video-gen/index.js "A cyberpunk city in rain" --model Kling --model-version 2.5 --chat-id "oc_..."
```

**2. 图像转视频（使用Hailuo 2.3模型）**
```bash
node skills/video-gen/index.js "Make the cat jump" --model Hailuo --model-version 2.3 --image "https://example.com/cat.jpg"
```

**3. 指定视频的开始和结束帧（使用Kling 2.1模型）**
```bash
node skills/video-gen/index.js "Morph from day to night" --model Kling --model-version 2.1 --image "https://.../day.jpg" --last-frame "https://.../night.jpg"
```

## 运行所需的环境变量
需要以下`.env`文件中的变量：
- `VITE_VOD_SECRET_ID`
- `VITE_VOD_SECRET_KEY`
- `VITE_VOD_SUB_APP_ID`