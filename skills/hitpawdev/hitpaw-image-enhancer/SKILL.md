---
name: hitpaw-image-enhancer
description: 使用 HitPaw 的 AI 增强 API 来优化图片和视频的质量
version: "1.0.1"
author: Nova (HitPaw-Official)
type: cli
entry: dist/cli.js
repository: https://github.com/HitPaw-Official/openclaw-skill-hitpaw-enhancer
keywords:
  - image
  - video
  - enhancement
  - upscale
  - hitpaw
  - ai
license: MIT
capabilities:
  - image_enhancement
  - image_upscaling
  - photo_enhance
  - video_enhancement
  - video_upscaling
requirements:
  node: ">=18"
  packages:
    - axios
    - commander
    - ora
    - chalk
    - fs-extra
environment:
  variables:
    - name: HITPAW_API_KEY
      description: Your HitPaw API key
      required: true
---
# HitPaw 图像与视频增强技能

这是一个强大的 OpenClaw 技能，它整合了 HitPaw 的先进 AI 增强技术，适用于 **图像** 和 **视频** 的处理。通过多种 AI 模型实现增强、放大、修复和去噪等功能。

---

## 🎯 特点

基于官方的 [HitPaw API 文档](https://developer.hitpaw.com/image/Introduction)，该技能利用了 HitPaw 专家研发团队自主研发的工业级 AI 模型。

### 核心优势

- **质量**：适用于专业场景，从商业摄影到档案修复，质量达到行业标准。
- **保真度**：保留原始图像的细节和特征，确保输出与输入一致。
- **效率**：优化了低延迟和高吞吐量，能够大规模处理各种增强任务。

---

## 📸 图像增强

根据 [图像 API 介绍](https://developer.hitpaw.com/image/Introduction)，我们的图像处理服务提供了世界级的功能，能够处理各种修复场景：

### 关键功能

- **放大**：使用标准或高保真模型，将低分辨率输入文件转换为高分辨率输出。
- **面部修复**：提供“清晰”（柔和/美化）和“自然”（有质感/真实）两种面部修复选项。
- **锐化与去噪**：去除模糊和传感器噪声，同时保持图像的原始结构。
- **生成式修复**：利用扩散技术重建严重损坏的肖像或普通图像的细节。

### 模型类别

图像 API 提供了两种类型的 AI 模型，以满足不同的需求：

- **标准模型**：快速高效，注重保留原始的保真度和细节。推荐用于大多数专业和通用修复场景。
- **生成模型**：利用 Stable Diffusion 技术生成最高质量的输出，能够“想象”缺失的细节。适用于传统放大方法无法处理的极低质量图像。

#### 标准模型

如 [可用模型](https://developer.hitpaw.com/image/available-models) 文档中所述：

| 模型 | 放大倍数 | 描述 | 适用场景 |
|-------|------------|-------------|----------|
| `general_2x` / `general_4x` | 2x / 4x | 通用增强模型 | 通用照片、风景照片 |
| `face_2x` / `face_4x` | 2x / 4x | 肖像模型（清晰风格） | 软化/美化的肖像增强 |
| `face_v2_2x` / `face_v2_4x` | 2x / 4x | 肖像模型（自然风格） | 自然/真实的肖像增强 |
| `high_fidelity_2x` / `high_fidelity_4x` | 2x / 4x | 高保真模型 | 专业摄影，高质量源文件的保守放大 |
| `sharpen_denoise_1x` | 1x | 锐化去噪模型 | 强化去噪 |
| `detail_denoise_1x` | 1x | 细节去噪模型 | 保留纹理的温和去噪 |

#### 生成模型

由 Stable Diffusion 技术驱动：

| 模型 | 放大倍数 | 描述 | 适用场景 |
|-------|------------|-------------|----------|
| `generative_portrait_1x/2x/4x` | 1x/2x/4x | 生成式肖像模型 | 极低质量的肖像，重建细节 |
| `generative_general_1x/2x/4x` | 1x/2x/4x | 生成式增强模型 | 严重压缩或分辨率极低的普通图像 |

**技术亮点**：
- 生成模型在纹理生成和锐化方面表现优异。
- 它们可以填补传统放大方法无法恢复的缺失细节。
- 非常适合源数据严重损坏的修复任务。

#### 图像使用示例

```bash
# General photo upscaling (landscape, architecture)
enhance-image -u landscape.jpg -m general_4x -o hd_landscape.jpg

# Portrait beautification (soft skin)
enhance-image -u selfie.jpg -m face_4x -o portrait_beautified.jpg

# Professional archival restoration (natural look)
enhance-image -u old_photo.png -m face_v2_2x -o restored.png --keep-exif

# Denoise grainy low-light photo
enhance-image -u night_photo.jpg -m sharpen_denoise_1x -o clean.jpg

# Generative reconstruction for severely degraded image
enhance-image -u blurry_face.jpg -m generative_portrait_2x -o ai_face.jpg
```

---

## 🎬 视频增强

根据 [视频 API 介绍](https://developer.hitpaw.com/video/Introduction)，我们的视频处理服务提供了工业级的视频修复和放大解决方案：

### 关键功能

- **视频放大**：使用深度卷积和特征学习技术，将 SD 或 HD 视频转换为 4K 超高清。
- **肖像修复**：专门模型用于检测、稳定和增强视频流中的面部，去除运动模糊和噪声，同时保持面部特征。
- **通用修复**：基于 GAN 技术的全面解决方案，用于去噪、去模糊和增强普通视频内容的细节。
- **生成式重建**：利用 Stable Diffusion 为极低质量的视频重建纹理和细节。

### 核心特点

- **时间稳定性**：与仅处理图像的模型不同，我们的视频引擎确保帧与帧之间的平滑过渡，消除闪烁和抖动。
- **清晰度**：恢复精细细节，去除流媒体或老式媒体中常见的压缩伪影。
- **性能**：优化了推理时间，能够高效处理大量视频处理任务。

### 模型类别

- **修复与放大（标准）**：如 Ultra HD 和 General Restore 模型，专注于清理视频并提高分辨率，而不改变基本内容。它们依赖于像素级的准确性和时间一致性。
- **生成式视频**：使用先进的逻辑重建技术，适用于源视频数据不足的“不可能”修复任务，生成真实的纹理和细节。

#### 可用的视频模型

来自 [视频模型文档](https://developer.hitpaw.com/video/available-models)：

| 模型 | 描述 | 适用场景 |
|-------|-------------|----------|
| `ultrahd_restore_2x` | 超高清模型 | 高清放大；1080p→4K 的自然效果 |
| `general_restore_1x` / `2x` / `4x` | 通用修复模型 | 通用视频修复、去噪、去模糊 |
| `portrait_restore_1x` / `2x` | 肖像修复模型 | 多人脸修复，具有时间稳定性 |
| `face_soft_2x` | 视频面部美化模型 | 保持一致外观的面部美化 |
| `generative_1x` | 生成式视频模型 | 严重损坏视频的极端修复 |

**技术亮点**：
- 通过多帧架构生成真实纹理，消除闪烁。
- 处理严重的压缩、高 ISO 噪声和复杂的运动模糊。
- 保持帧与帧之间的身份一致性。

#### 视频使用示例

```bash
# Convert old 720p footage to 4K
enhance-video -u old_clip.mp4 -m ultrahd_restore_2x -r 3840x2160 -o 4k_remastered.mp4

# Restore grainy, noisy home video
enhance-video -u home_movie.avi -m general_restore_2x -r 1920x1080 -o cleaned.mp4

# Beautify faces in vlog/interview
enhance-video -u interview.mp4 -m face_soft_2x -r 1920x1080 -o soft_faces.mp4

# Stabilize and restore old family footage with multiple faces
enhance-video -u family_reunion.mov -m portrait_restore_2x -r 1920x1080 -o restored.mp4

# Generative AI restoration for severely degraded source
enhance-video -u heavily_compressed.mp4 -m generative_1x -r 1920x1080 -o regenerated.mp4
```

---

## 🚀 为什么选择 HitPaw API？

- **行业领先的质量**：适合商业摄影、档案修复和广播级视频修复的专业级输出。
- **无与伦比的保真度**：严格保留原始细节和主体特征，确保输出与输入一致。
- **全面的模型目录**：16 个专门模型，几乎覆盖所有修复场景。
- **可扩展的性能**：优化了低延迟和高吞吐量的工作负载。

---

## 📊 快速参考

### 图像模型选择指南

| 场景 | 推荐模型 |
|----------|-------------------|
| 通用照片放大 | `general_2x` 或 `general_4x` |
| 肖像美化 | `face_2x` 或 `face_4x` |
| 肖像自然效果 | `face_v2_2x` 或 `face_v2_4x` |
| 专业档案修复 | `high_fidelity_2x` / `high_fidelity_4x` |
| 低光环境下的颗粒感 | `sharpen_denoise_1x` |
| 轻微去噪 | `detail_denoise_1x` |
| 严重损坏的图像 | `generative_portrait_*` 或 `generative_general_*` |

### 视频模型选择指南

| 场景 | 推荐模型 |
|----------|-------------------|
| SD → 4K 放大 | `ultrahd_restore_2x` |
| 通用修复 | `general_restore_2x` |
| 面试/视频博客美化 | `face_soft_2x` |
| 老式家庭录像（多人脸） | `portrait_restore_2x` |
| 严重压缩/损坏的视频 | `generative_1x` |

---

## 安装

```bash
clawhub install hitpaw-image-enhancer
```

## 配置

设置您的 HitPaw API 密钥：

```bash
export HITPAW_API_KEY="your_api_key_here"
```

或在您的 OpenClaw 工作区创建一个 `.env` 文件：

```
HITPAW_API_KEY=your_api_key_here
```

在以下链接获取您的 API 密钥：https://playground.hitpaw.com/

直接在浏览器中测试 API：[HitPaw Playground →](https://playground.hitpaw.com/)

---

## 📸 示例与图库

> **注意**：请将实际的“前后对比”截图放在 `images/` 文件夹中。详情请参阅 `images/README.md`。

### 图像增强示例

| 场景 | 前 | 后 |
|----------|--------|-------|
| 通用放大（2x） | ![之前](images/image-before.jpg) | ![之后](images/image-after.jpg) |
| 肖像增强 | ![之前](images/face-before.jpg) | ![之后](images/face-after.jpg) |
| 生成式肖像 | ![之前](images/gen-before.jpg) | ![之后](images/gen-after.jpg) |

### 视频增强示例

| 场景 | 原始帧 | 增强后的帧 |
|----------|----------------|----------------|
| 通用修复 | ![原始](images/video-original.jpg) | ![增强后的](images/video-enhanced.jpg) |
| 肖像修复 | ![之前](images/portrait-video-before.jpg) | ![之后](images/portrait-video-after.jpg) |

---

# 图像命令

## 使用方法：`enhance-image`

### 命令行选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `--url`, `-u` | 字符串 | **必需** | 需要增强的图像的 URL |
| `--output`, `-o` | 字符串 | 输出文件路径 |
| `--model`, `-m` | 字符串 | `general_2x` | 图像模型（见下文） |
| `--extension`, `-e` | 字符串 | 输出格式（.jpg, .png, .webp） |
| `--dpi` | 数字 | 原始 DPI | 目标 DPI |
| `--keep-exif` | 布尔值 | 否 | 保留原始文件的 EXIF 数据 |
| `--poll-interval` | 数字 | 5 | 轮询间隔（秒） |
| `--timeout` | 数字 | 300 | 最大等待时间（秒） |

#### 可用的图像模型

| 模型 | 放大倍数 | 适用场景 | DPI 支持 |
|-------|------------|----------|-------------|
| `general_2x` / `general_4x` | 2x / 4x | 通用照片、风景照片 | ✅ |
| `face_2x` / `face_4x` | 2x / 4x | 肖像和面部增强 | ✅ |
| `face_v2_2x` / `face_v2_4x` | 2x / 4x | 改进的面部模型 | ✅ |
| `high_fidelity_2x` / `high_fidelity_4x` | 2x / 4x | 高质量保留 | ✅ |
| `sharpen_denoise_1x` | 1x | 去噪与锐化 | ✅ |
| `detail_denoise_1x` | 1x | 细节保留 | ✅ |
| `generative_*` (1x/2x/4x) | — | AI 生成填充 | ❌ |

#### 示例

```bash
# Simple 2x upscale with general model
enhance-image -u photo.jpg -o enhanced.jpg -m general_2x

# Face enhancement 4x
enhance-image -u portrait.jpg -m face_4x -o portrait_4x.jpg --keep-exif

# High fidelity with custom DPI
enhance-image -u old-photo.png -m high_fidelity_2x -dpi 300 -o hd.png

# Batch processing
for img in *.jpg; do
  enhance-image -u "$img" -o "upscaled/$img" -m general_4x
done
```

---

# 视频命令

## 使用方法：`enhance-video`

### ⚠️ 重要说明

- **需要提供分辨率**（`--resolution` 或 `-r`）。格式应为 `WIDTHxHEIGHT`（例如，`1920x1080`）。
- 确保目标分辨率 **不超过 API 的最大输出分辨率**（总像素数不超过 36 MP）。
- 视频处理可能需要 **几分钟到几小时**，具体取决于视频长度。如有需要，可以使用 `--timeout` 延长处理时间。
- 输入视频必须是 **公开可访问的 URL**（不支持本地文件）。

### 命令行选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `--url`, `-u` | 字符串 | **必需** | 需要增强的视频的 URL |
| `--output`, `-o` | 字符串 | 输出文件路径 |
| `--model`, `-m` | 字符串 | `general_restore_2x` | 视频模型 |
| `--resolution`, `-r` | 字符串 | **必需** | 目标分辨率（格式为 WxH，例如，`1920x1080`） |
| `--original-resolution` | 字符串 | **可选** | 原始分辨率（例如，`1280x720`） |
| `--extension`, `-e` | 字符串 | 输出格式（.mp4, .mov, .avi） |
| `--fps` | 数字 | **可选** | 目标帧率（如果省略则保留原始帧率） |
| `--keep-audio` | 布尔值 | 是否保留音频轨道 |
| `--poll-interval` | 数字 | 10 | 轮询间隔（秒） |
| `--timeout` | 数字 | 600 | 最大等待时间（秒） |

#### 可用的视频模型

| 模型 | 描述 | 适用场景 |
|-------|-------------|----------|
| `general_restore_1x` / `2x` / `4x` | 通用视频修复 | 通用放大 |
| `face_soft_2x` | 脸部美化增强 | 肖像视频 |
| `portrait_restore_1x` / `2x` | 肖像修复 | 以面部为主的视频 |
| `ultrahd_restore_2x` | 超高清放大 | 最高质量放大 |
| `generative_1x` | 生成式修复 | AI 驱动的修复 |

#### 示例

```bash
# Upscale to 1080p using general_restore_2x
enhance-video -u input.mp4 -o output_1080p.mp4 -m general_restore_2x -r 1920x1080

# Upscale to 4K with specific original resolution
enhance-video -u clip.mov -o 4k.mov -m general_restore_4x -r 3840x2160 --original-resolution 1920x1080

# Denoise with portrait model
enhance-video -u portrait_video.avi -m portrait_restore_2x -r 1920x1080 -o clean_portrait.mp4

# Add color to B&W (if generative model supports)
enhance-video -u bw_vintage.mp4 -m generative_1x -r 1920x1080 -o colorized.mp4
```

## 金币消耗

### 图像增强
- 2x/4x 模型：每张图片约 75 金币
- 1x 模型：每张图片约 50 金币
- 生成模型：每张图片约 100 多金币

### 视频增强
金币费用取决于视频长度、模型和分辨率。大致费用如下：
- 放大模型：每分钟约 200-400 金币
- 修复模型：每分钟约 150-300 金币

**请随时查看最新费用信息**：https://playground.hitpaw.com/

---

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `无效的 API 密钥` | 密钥错误或已过期 | 更新 `HITPAW_API_KEY` |
| 金币不足 | 账户余额过低 | 在 HitPaw Playground 充值 |
| 不支持的模型 | 模型名称拼写错误或不可用 | 查看上面的模型列表 |
| 无效的文件扩展名 | 不支持的输出格式 | 图像使用 `.jpg/.png/.webp`；视频使用 `.mp4/.mov/.avi` |
| 无效的视频 URL | 视频无法公开访问 | 确保视频可以通过 HTTPS 访问 |
| 输入/目标分辨率超出限制 | 总像素数超过 36 MP（例如，7680x4320 = 约 33 MP） | 降低分辨率 |
| 视频时长超过限制 | 视频时长超过 1 小时 | 先修剪视频 |
| 请求次数超出限制 | 请求过多 | 请稍后重试 |

## 技术细节

### API 兼容性

该技能实现了官方的 HitPaw API，具体细节如下：
- **基础 URL**：`https://api-base.hitpaw.com`
- **图像端点**：`POST /api/photo-enhancer`
- **视频端点**：`POST /api/video-enhancer`
- **状态端点**：`POST /api/task-status`

两个端点都会返回一个 `job_id`。使用状态端点轮询，直到状态变为 `COMPLETED`，然后从 `res_url` 下载结果。

### 轮询策略

- **图像**：默认每 5 秒轮询一次，超时时间为 300 秒（5 分钟）。
- **视频**：默认每 10 秒轮询一次，超时时间为 600 秒（10 分钟）。

对于较长的视频，根据需要增加 `--timeout`（例如，`--timeout 3600` 表示 1 小时）。

### 分辨率处理

对于视频，**分辨率是必需的**。根据您的需求选择：
- 保持原始尺寸？设置 `resolution` 为原始尺寸（使用 `--original-resolution` 可获得更好的质量）。
- 放大？将原始宽度/高度乘以放大倍数（2x, 4x）。
- 缩小？虽然不常见，但也可以；只需指定较小的尺寸。

**最大输出**：总像素数不超过 36 兆像素（宽度 × 高度 ≤ 36,000,000 像素）。
示例：3840×2160 = 8.3 MP ✅, 7680×4320 = 33.2 MP ✅, 8192×4608 = 37.7 MP ❌。

### 音频保留

默认情况下，`enhance-video` 会保留音频轨道（`--keep-audio`，默认值为 true）。使用 `--no-keep-audio` 可以去除音频。

---

## 支持

- 图像 API 文档：https://developer.hitpaw.com/image/API-reference
- 视频 API 文档：https://developer.hitpaw.com/video/API-reference
- 测试平台：https://playground.hitpaw.com/
- 联系方式：support@hitpaw.com

此技能是与 HitPaw API 的 **非官方集成**。您必须拥有有效的 API 密钥，并遵守 HitPaw 的使用条款。技能作者不对因此产生的任何费用负责。

## 许可证

MIT © HitPaw-Official