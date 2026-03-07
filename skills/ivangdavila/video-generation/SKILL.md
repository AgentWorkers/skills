---
name: AI Video Generation
slug: video-generation
version: 1.0.1
homepage: https://clawic.com/skills/video-generation
description: 使用 Sora 2、Veo 3、Seedance、Runway 以及现代 API，通过可靠的提示（prompt）和渲染工作流程来创建 AI 视频。
changelog: Added current model routing and practical API playbooks for modern AI video generation workflows.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":[],"env.optional":["OPENAI_API_KEY","GOOGLE_CLOUD_PROJECT","RUNWAY_API_KEY","LUMA_API_KEY","FAL_KEY","REPLICATE_API_TOKEN","VIDU_API_KEY","TENCENTCLOUD_SECRET_ID","TENCENTCLOUD_SECRET_KEY"],"config":["~/video-generation/"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 文件。

## 使用场景

当用户需要使用当前的模型和 API 生成、编辑或调整 AI 视频时，可以使用此技能。通过该技能，用户可以选择合适的模型组合，编写更精确的运动指令，并运行可靠的异步视频处理流程。

## 架构

用户的偏好设置会保存在 `~/video-generation/` 目录中。具体设置方法请参考 `memory-template.md` 文件。

```text
~/video-generation/
├── memory.md      # Preferred providers, model routing, reusable shot recipes
└── history.md     # Optional run log for jobs, costs, and outputs
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 初始设置 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 迁移指南 | `migration.md` |
| 模型快照 | `benchmarks.md` |
| 异步 API 模式 | `api-patterns.md` |
| OpenAI Sora 2 | `openai-sora.md` |
| Google Veo 3.x | `google-veo.md` |
| Runway Gen-4 | `runway.md` |
| Luma Ray | `luma.md` |
| ByteDance Seedance | `seedance.md` |
| Kling | `kling.md` |
| Vidu | `vidu.md` |
| Pika via Fal | `pika.md` |
| MiniMax Hailuo | `minimax-hailuo.md` |
| 复制路由 | `replicate.md` |
| 开源本地模型 | `open-source-video.md` |
| 分发脚本 | `promotion.md` |

## 核心规则

### 1. 在调用 API 之前解析模型别名

请先将社区名称映射到实际的 API 模型 ID。例如：`sora-2`、`sora-2-pro`、`veo-3.0-generate-001`、`gen4_turbo`、`gen4_aleph`。

### 2. 根据任务选择模型，而非品牌偏好

| 任务 | 首选模型 | 备选模型 |
|------|--------------|--------|
| 仅生成高级提示 | `sora-2-pro` | `veo-3.1-generate-001` |
| 快速生成草图（低成本） | `veo-3.1-fast-generate-001` | `gen4_turbo` |
| 长格式电影镜头 | `gen4_aleph` | `ray-2` |
| 强大的图像到视频控制能力 | `veo-3.0-generate-001` | `gen4_turbo` |
| 多镜头叙事一致性 | `seedance` 系列模型 | `hailuo-2.3` |
| 优先考虑本地隐私的工作流程 | `Wan2.2` / `HunyuanVideo` | `CogVideoX` |

### 3. 先使用低成本模型进行初步生成，再使用高级模型优化

先使用低成本的模型进行快速生成，验证运动和构图效果，然后使用高级模型或更长的时长重新渲染。

### 4. 将提示设计为具体的拍摄指令

提示中必须包含主题、动作、摄像机运动、镜头风格、光线效果以及场景时间安排。对于参考帧和开始/结束帧，要明确说明其连续性要求。

### 5. 默认情况下假设所有操作都是异步的，并可能失败

所有提供的 API 都应支持任务排队、轮询/重试、取消以及在请求超时前的下载功能。

### 6. 设置备用方案

如果首选模型被禁用或负载过重：
1) 使用同一提供商的较低等级模型；
2) 使用其他提供商的等效模型；
3) 使用开源模型或本地模型进行生成。

## 常见错误

- 在代码中仅使用模型昵称可能导致 API 请求失败；
- 在未验证 3-5 秒的草图之前就直接生成 8-10 秒的视频会导致资源浪费；
- 生成后进行裁剪而非保持原始比例会导致构图质量下降；
- 忽略提示中的优化选项会导致不同提供商生成的视频风格不一致；
- 重复使用过期的输出 URL 会导致导出失败；
- 将所有提供商视为同步操作会导致任务卡顿和超时处理问题。

## 外部接口

| 提供商 | 接口地址 | 发送的数据 | 用途 |
|----------|----------|-----------|---------|
| OpenAI | `api.openai.com` | 提示文本、可选的输入图片/视频参考 | Sora 2 视频生成 |
| Google Vertex AI | `aiplatform.googleapis.com` | 提示文本、可选的图片输入、生成参数 | Veo 3.x 视频生成 |
| Runway | `api.dev.runwayml.com` | 提示文本、可选的输入媒体 | Gen-4 视频生成及图像转视频 |
| Luma | `api.lumalabs.ai` | 提示文本、可选的关键帧/开始/结束图片 | Ray 视频生成 |
| Fal | `queue.fal.run` | 提示文本、可选的输入媒体 | Pika 和 Hailuo 的 API |
| Replicate | `api.replicate.com` | 提示文本、可选的输入媒体 | 多模型路由和实验 |
| Vidu | `api.vidu.com` | 提示文本、可选的开始/结束/参考图片 | Vidu 的文本/图片/参考视频 API |
| Tencent MPS | `mps.tencentcloudapi.com` | 提示文本和生成参数 | 统一的 AIGC 视频任务 API |

**注意：** 不会向外部发送其他任何数据。

## 安全与隐私

**离开您机器的数据：**
- 提示文本
- 可选的参考图片或片段
- 请求的渲染参数（时长、分辨率、宽高比）

**保留在本地的数据：**
- 用户的偏好设置（保存在 `~/video-generation/memory.md` 中）
- 本地任务历史记录（保存在 `~/video-generation/history.md` 中）

**此技能不会：**
- 将 API 密钥存储在项目文件中；
- 将媒体文件上传到请求范围之外的地方；
- 除非用户要求，否则不会删除本地资产。

## 信任机制

此技能会将提示和媒体文件发送给第三方 AI 提供商。只有在您信任这些提供商的情况下，才建议安装相关工具。

## 相关技能

如果用户同意，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：
  - `image-generation`：在视频生成前构建静态概念图和关键帧；
  - `image-edit`：准备干净的参考图片、遮罩和风格化帧；
  - `video-edit`：对生成的片段进行后期处理和最终导出；
  - `video-captions`：添加字幕和文本叠加效果；
  - `ffmpeg`：组合、转码并打包最终输出文件。

## 反馈

- 如果觉得此技能有用，请给 `clawhub` 点星（star）；
- 要保持最新信息，请使用 `clawhub sync` 命令。