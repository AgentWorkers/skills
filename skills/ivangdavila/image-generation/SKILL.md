---
name: Image Generation
slug: image-generation
version: 1.0.2
homepage: https://clawic.com/skills/image-generation
description: 使用提示工程（Prompt Engineering）技术，结合风格控制（Style Control），为 Midjourney、DALL-E、Stable Diffusion、Flux 和 Leonardo 等 AI 模型生成图像。同时提供相应的使用指南（Provider Guides）。
changelog: Added detailed provider endpoints documentation and feedback section
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要由 AI 生成的图像。该工具负责处理文本到图像的转换、图像编辑、风格转换、图像放大以及选择合适的图像生成服务。

## 架构

用户的偏好信息存储在 `~/image-generation/` 目录中。具体设置方法请参阅 `memory-template.md` 文件。

```
~/image-generation/
├── memory.md      # Current provider, style, projects
└── history.md     # Past generations (optional)
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 内存设置 | `memory-template.md` |
| 提示技巧 | `prompting.md` |
| API 使用指南 | `api-patterns.md` |
| OpenAI/DALL-E | `openai.md` |
| Midjourney | `midjourney.md` |
| Stable Diffusion | `stable-diffusion.md` |
| Flux | `flux.md` |
| Leonardo | `leonardo.md` |
| Ideogram | `ideogram.md` |
| Replicate | `replicate.md` |

## 核心规则

### 1. 先查看用户偏好信息
请阅读 `~/image-generation/memory.md` 文件，了解用户选择的图像生成服务、偏好的风格以及项目背景信息。

### 2. 先生成草图再确定最终效果
- 首先尝试生成 512x512 或 1024x1024 大小的图像以验证提示的有效性。
- 生成 4 个以上的变体版本。
- 只选择最符合要求的图像进行放大处理。

### 3. 根据任务选择合适的图像生成服务

| 任务 | 最适合的服务 |
|------|---------------|
| 真实主义效果 | Midjourney, Flux Pro |
| 在图像中添加文本 | Ideogram, DALL-E 3 |
| 快速迭代 | Flux Schnell, Leonardo |
| 最高的控制精度 | Stable Diffusion |
| 图像修复/编辑 | DALL-E 3, Stable Diffusion |
| 预算有限的 API | Replicate, Leonardo |

### 4. 提示编写规范
- 先明确主题：例如 “一只红狐狸”，而非 “森林里有一只红狐狸”。
- 使用具体的风格关键词：如 “电影级光照”、“油画风格”、“工作室摄影”。
- 表达要具体：例如 “黄金时刻的阳光”，而非 “良好的光照条件”。
- 确保图像的宽高比与需求匹配：肖像画为 1:1，风景画为 16:9。

### 5. 更新用户偏好信息
- 当用户更换图像生成服务或偏好风格时，及时更新 `memory.md` 文件。
- 当开始新项目时，也需要将新信息添加到 `memory.md` 中。

## 常见问题及解决方法

- **图像中的手或手指显示不正确** → 重新生成图像或使用图像修复工具。
- **文本显示混乱** → 使用 Ideogram 工具处理文本，或在后期添加文本。
- **人脸变形** → 在提示中添加 “详细的人脸特征”，或使用专门的人脸修复模型。
- **风格不一致** → 固定随机种子值（seed），或使用参考图像。
- **出现水印** → 检查模型训练情况，使用无水印的模型。

## 安全性与隐私

**会离开您设备的数据：**
- 发送给所选 AI 生成服务的提示内容。

**保留在本地的数据：**
- 用户的偏好设置（存储在 `~/image-generation/` 目录中）。
- 无任何遥测数据或分析信息被发送。

**本工具不会：**
- 存储生成的图像（图像存储由图像生成服务负责）。
- 访问 `~/image-generation/` 目录之外的文件。

## 外部接口

| 服务提供商 | 接口地址 | 发送的数据 | 功能 |
|----------|----------|-----------|---------|
| OpenAI | api.openai.com | 提示文本 | 使用 DALL-E 生成图像 |
| Midjourney | discord.com | 提示文本 | 生成图像 |
| Stability AI | api.stability.ai | 提示文本 | 使用 Stable Diffusion 生成图像 |
| Replicate | api.replicate.com | 提示文本 | 使用 Flux 或 Stable Diffusion 生成图像 |
| Leonardo | cloud.leonardo.ai | 提示文本 | 使用 Leonardo 生成图像 |
| Ideogram | api.ideogram.ai | 提示文本 | 在图像中添加文本 |

外部接口的具体地址取决于所选择的图像生成服务。不会发送其他任何数据。

## 安全注意事项

使用本工具时，提示内容会发送给第三方 AI 服务提供商（如 OpenAI、Midjourney、Stability AI 等）。请确保您信任这些服务才能继续使用本工具。

## 反馈方式

- 如果本工具对您有帮助，请在 ClawHub 上给它打星评价：`clawhub star image-generation`
- 为了保持功能更新，请执行 `clawhub sync` 操作。