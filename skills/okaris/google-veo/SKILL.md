---
name: google-veo
description: "通过 `inference.sh` CLI 使用 Google Veo 模型生成视频。支持的模型包括：Veo 3.1、Veo 3.1 Fast、Veo 3、Veo 3 Fast、Veo 2。功能包括：文本转视频、电影级视频输出、高质量视频生成。触发命令包括：`veo`、`google veo`、`veo 3`、`veo 2`、`veo 3.1`、`vertex ai video`、`google video generation`、`google video ai`、`veo model`、`veo video`。"
allowed-tools: Bash(infsh *)
---
# 使用 Google Veo 生成视频

您可以通过 [inference.sh](https://inference.sh) 命令行工具，利用 Google Veo 模型来生成视频。

![使用 Google Veo 生成视频的示例](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg2c0egyg243mnyth4y6g51q.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot over a mountain lake"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。整个安装过程不需要任何特殊权限或后台进程。如需手动安装和验证，请参考 [此处](https://dist.inference.sh/cli/checksums.txt)。

## 可用的 Veo 模型

| 模型        | 应用 ID      | 处理速度    | 视频质量    |
|-------------|------------|-----------|-----------|
| Veo 3.1       | `google/veo-3-1`    | 较慢       | 最高质量    |
| Veo 3.1 Fast   | `google/veo-3-1-fast` | 快速       | 极佳质量    |
| Veo 3        | `google/veo-3`     | 中等质量    | 极佳质量    |
| Veo 3 Fast   | `google/veo-3-fast` | 快速       | 非常好的质量 |
| Veo 2        | `google/veo-2`     | 中等质量    | 良好质量    |

## 搜索适用的 Veo 应用

```bash
infsh app list --search "veo"
```

## 使用示例

- **电影级镜头**  
- **产品演示**  
- **自然场景**  
- **动作场景**  
- **城市景观**  

## 制作提示

- **摄像机运动方式**：无人机拍摄、跟踪拍摄、平移、缩放、推拉镜、稳定器拍摄  
- **光线效果**：黄金时刻、蓝色时刻、摄影棚灯光、霓虹灯光、自然光  
- **风格**：电影风格、纪录片风格、商业风格、艺术风格、写实风格  
- **播放方式**：慢动作、延时拍摄、实时播放  

## 示例工作流程

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
npx skills add inference-sh/skills@inference-sh

# All video generation models
npx skills add inference-sh/skills@ai-video-generation

# AI avatars & lipsync
npx skills add inference-sh/skills@ai-avatar-video

# Image generation (for image-to-video)
npx skills add inference-sh/skills@ai-image-generation
```

- 查看所有可用的视频应用：`infsh app list --category video`  

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过命令行工具运行应用程序  
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 应用程序的实时运行状态  
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 媒体处理工作流程的构建方法