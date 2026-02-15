---
name: google-veo
description: |
  Generate videos with Google Veo models via inference.sh CLI.
  Models: Veo 3.1, Veo 3.1 Fast, Veo 3, Veo 3 Fast, Veo 2.
  Capabilities: text-to-video, cinematic output, high quality video generation.
  Triggers: veo, google veo, veo 3, veo 2, veo 3.1, vertex ai video, google video generation,
  google video ai, veo model, veo video
allowed-tools: Bash(infsh *)
---

# 使用 Google Veo 生成视频

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）使用 Google Veo 模型来生成视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot over a mountain lake"}'
```

## Veo 模型

| 模型 | 应用 ID | 生成速度 | 视频质量 |
|-------|--------|-------|---------|
| Veo 3.1 | `google/veo-3-1` | 生成速度较慢 | 视频质量最佳 |
| Veo 3.1 Fast | `google/veo-3-1-fast` | 生成速度较快 | 视频质量优秀 |
| Veo 3 | `google/veo-3` | 生成速度中等 | 视频质量优秀 |
| Veo 3 Fast | `google/veo-3-fast` | 生成速度较快 | 视频质量非常好 |
| Veo 2 | `google/veo-2` | 生成速度中等 | 视频质量良好 |

## 搜索可用的 Veo 应用程序

```bash
infsh app list --search "veo"
```

## 示例

### 电影风格镜头

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Cinematic drone shot flying through a misty forest at sunrise, volumetric lighting"
}'
```

### 产品演示

```bash
infsh app run google/veo-3 --input '{
  "prompt": "Sleek smartphone rotating on a dark reflective surface, studio lighting"
}'
```

### 自然场景

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Timelapse of clouds moving over a mountain range, golden hour"
}'
```

### 动作场景

```bash
infsh app run google/veo-3 --input '{
  "prompt": "Slow motion water droplet splashing into a pool, macro shot"
}'
```

### 城市场景

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Busy city street at night with neon signs and rain reflections, Tokyo style"
}'
```

## 提示与建议

- **摄像机运动方式**：无人机拍摄、跟踪拍摄、平移、缩放、推拉镜头、稳定器拍摄
- **光线设置**：黄金时刻、蓝调时刻、摄影棚灯光、立体光效果、霓虹灯光、自然光
- **风格选择**：电影风格、纪录片风格、商业广告风格、艺术风格、写实风格
- **时间控制**：慢动作、延时摄影、实时拍摄

## 样本工作流程

```bash
# 1. Generate sample input to see all options
infsh app sample google/veo-3-1-fast --save input.json

# 2. Edit the prompt
# 3. Run
infsh app run google/veo-3-1-fast --input input.json
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# All video generation models
npx skills add inference-sh/agent-skills@ai-video-generation

# AI avatars & lipsync
npx skills add inference-sh/agent-skills@ai-avatar-video

# Image generation (for image-to-video)
npx skills add inference-sh/agent-skills@ai-image-generation
```

- 查看所有视频应用程序：`infsh app list --category video`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用程序
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 应用程序的实时运行状态
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 媒体处理工作流程的构建方法