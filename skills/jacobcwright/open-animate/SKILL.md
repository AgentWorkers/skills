---
name: open-animate
description: **Open Animate**——专为AI代理设计的创意工具套件。它支持创建专业的动态图形、生成图片以及渲染MP4视频。无论您需要制作视频、动画、动态图形、社交媒体片段、产品发布资料还是任何形式的视觉内容，Open Animate都是理想的选择。该工具具备资产生成功能（包括图片和背景的处理），同时支持通过动画预设、过渡效果及各种组件来实现视频的复杂合成。
license: Apache-2.0
metadata:
  openclaw:
    emoji: "\U0001F3AC"
    homepage: https://open-animate.com
    requires:
      bins:
        - npx
    install:
      - kind: node
        package: oanim
        bins:
          - oanim
        label: "Install oanim CLI (npm)"
---
# Open Animate — 专为代理设计的创意工具套件

使用 Open Animate，您可以创建专业的动态图形并生成视觉素材。只需描述您的需求，系统便会自动生成 MP4 格式的视频文件。

## 先决条件

本技能基于 **Remotion** 的核心技术进行开发，您需要具备使用 Remotion API 的相关经验：
```bash
npx skills add remotion-dev/skills
```

## 工作流程

### 1. 初始化项目
```bash
npx oanim init my-video
cd my-video
```

### 2. 使用 `@oanim/core` 进行素材组合
```tsx
import { fadeUp, popIn, Background, SafeArea, palettes } from '@oanim/core';
```

请参阅 `references/animation-cookbook.md` 以获取完整的预设设置参考。

### 3. 预览效果
```bash
npx remotion studio
```

### 4. 将素材渲染为 MP4 格式
```bash
npx oanim render
```

### 5. 生成并使用媒体素材（可选）
```bash
# Generate image, video, or audio
npx oanim assets gen-image --prompt "dark gradient abstract" --out public/bg.png
npx oanim assets run --model fal-ai/kling-video/v1/standard/text-to-video \
  --input '{"prompt":"cinematic abstract motion","duration":"5"}' --out public/clip.mp4
npx oanim assets run --model fal-ai/stable-audio \
  --input '{"prompt":"ambient electronic, no vocals","duration_in_seconds":30}' --out public/music.mp3
```

随后，您可以将这些素材应用到您的作品中：
```tsx
import { Img, OffthreadVideo, Audio, staticFile } from 'remotion';

<Img src={staticFile('bg.png')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
<OffthreadVideo src={staticFile('clip.mp4')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
<Audio src={staticFile('music.mp3')} volume={0.25} />
```

## 功能列表

| 功能                | 所用工具                |
|------------------|----------------------|
| 项目搭建工具           | `oanim init`             |
| 动画预设（淡入、弹出、弹簧效果）    | `@oanim/core`             |
| 组件（终端、卡片、徽章、发光球体）     | `@oanim/core`             |
| 场景过渡效果（模糊淡入、圆形剪辑、擦拭效果） | `@oanim/core`             |
| 字体效果（动画文字、打字机文字、倒计时） | `@oanim/core`             |
| 设计元素（5 种调色板、字体、间距设置） | `@oanim/core`             |
| 视频渲染工具           | `oanim render`             |
| 云渲染服务           | `oanim render --cloud`           |
| AI 图像生成工具         | `oanim assets gen-image`         |
| AI 视频生成工具         | `oanim assets run`           |
| AI 音频生成工具         | `oanim assets run`           |
| 媒体合成工具           | `<Img>`, `<OffthreadVideo>`, `<Audio>`       |
| 图像编辑工具           | `oanim assets edit-image`         |
| 背景去除工具           | `oanim assets remove-bg`         |
| 图像放大工具           | `oanim assets upscale`         |
| 任何 fal.ai 模型           | `oanim assets run`           |

## 参考资料

- `references/workflow.md` — 代理工作的详细步骤指南
- `references/scene-config.md` — `animate.json` 数据格式参考
- `references/composition-patterns.md` — 多场景合成设计模式
- `references/animation-cookbook.md` — `@oanim/core` 的所有预设设置说明
- `references/asset-generation.md` — AI 资源生成指南
- `references/media-guide.md` — 如何在作品中使用生成的媒体文件（图片、视频、音频）

## 模板示例

- `templates/launch-video.md` — 4 个场景的产品发布视频（时长 5 秒）
- `templates/explainer.md` — 基于步骤的解释性视频（时长 20 秒）
- `templates/logo-reveal.md` — 带有发光效果的Logo动画（时长 5 秒）
- `templates/meme-caption.md` — 垂直方向的社交媒体视频片段（时长 6 秒）
- `templates/investor-update.md` — 统计数据仪表盘（时长 15 秒）