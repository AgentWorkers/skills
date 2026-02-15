---
name: remotion-video-toolkit
description: 这是一个完整的工具包，用于使用 Remotion 和 React 进行程序化视频制作。该工具包涵盖了动画、时间控制、渲染（支持 CLI、Node.js、Lambda 和 Cloud Run）、字幕添加、3D 效果、图表、文本效果、过渡效果以及媒体处理等功能。适用于编写 Remotion 代码、构建视频生成流程或创建数据驱动的视频模板。
---

# Remotion Video Toolkit

本工具包帮助您编写React组件，并获取实际的MP4视频文件。它教会您的AI代理如何使用Remotion进行开发——从创建第一个动画到构建完整的渲染流程。

**包含29条规则，涵盖了Remotion的所有主要功能。**

---

## 使用本工具包可以构建的内容：

**大规模个性化视频**
- 将用户数据作为JSON属性传递，为每个用户生成独特的视频。例如：Spotify的封面视频、GitHub的欢迎动画、入职引导视频等——一个模板即可生成数千个不同的输出结果。

**自动化社交媒体视频**
- 自动获取实时数据（如统计数据、排行榜、产品指标），无需人工编辑时间线即可生成每日或每周的视频内容。

**动态广告和营销视频**
- 可替换客户名称、产品图片、价格等信息。使用相同的模板生成无限种变体，通过API或Lambda在服务器端进行渲染。

**动画数据可视化**
- 将仪表板和KPI报告转换为包含动画图表和过渡效果的共享视频。

**TikTok和Reels字幕**
- 为音频添加字幕，以逐字显示的方式呈现，并可导出用于上传。

**产品展示视频**
- 从数据库自动生成视频，包含产品图片、规格信息、价格等详细内容。

**教育和解释性内容**
- 动态课程材料、证书视频、逐步指导教程等，全部由代码驱动生成。

**视频生成服务**
- 将视频渲染功能作为HTTP端点提供。您的应用程序发送JSON数据，即可获得对应的视频文件。

---

## 系统要求：

- **Node.js** 18及以上版本
- **React** 18及以上版本（Remotion支持逐帧渲染React组件）
- **Remotion**：使用`npx create-video@latest`命令进行快速搭建
- **FFmpeg**：随`@remotion(renderer`包提供，无需单独安装
- **服务器端渲染支持**：需要AWS账户（Lambda）或GCP账户（Cloud Run）。

---

## 工具包内容结构：

### 核心功能

| 规则 | 说明 |
|------|-------------|
| [组合元素](rules/compositions.md) | 定义视频、静态图片、文件夹、默认属性及动态元数据 |
| [渲染流程](rules/rendering.md) | 命令行接口（CLI）、Node.js API、AWS Lambda、Cloud Run、Express服务器实现方式 |
| [元数据计算](rules/calculate-metadata.md) | 在渲染时动态设置视频时长、尺寸和属性 |

### 动画与时间控制

| 规则 | 说明 |
|------|-------------|
| [动画效果](rulesanimations.md) | 淡入淡出、缩放、旋转、滑动等动画效果 |
| [时间控制](rules/timing.md) | 插值曲线、缓动效果、物理模拟等动画技术 |
| [场景顺序](rules/sequencing.md) | 场景的延迟、串联及协调播放 |
| [过渡效果](rules/transitions.md) | 场景之间的过渡效果 |
| [视频剪辑](rules/trimming.md) | 剪裁动画的开始或结束部分 |

### 文本与排版

| 规则 | 说明 |
|------|-------------|
| [文本动画](rules/text-animations.md) | 打字机效果、文字高亮、渐显渐隐等文本动画 |
| [字体](rulesfonts.md) | 使用Google Fonts或本地字体 |
| [文本适配](rules/measuring-text.md) | 根据容器大小调整文本显示，检测文本溢出情况 |

### 媒体处理

| 规则 | 说明 |
|------|-------------|
| [视频处理](rules/videos.md) | 视频的嵌入、剪辑、速度调整、音量控制、循环播放、音高调整 |
| [音频处理](rules/audio.md) | 音频的导入、剪辑、淡入淡出效果 |
| [图片处理](rules/images.md) | 使用Img组件处理图片 |
| [GIF处理](rules/gifs.md) | 同步时间线的GIF播放 |
| [媒体资源管理](rules/assets.md) | 将各种媒体文件导入到视频中 |
| [兼容性检测](rules/can-decode.md) | 检查浏览器对媒体文件的兼容性 |

### 字幕与字幕显示

| 规则 | 说明 |
|------|-------------|
| [字幕生成](rules/transcribe-captions.md) | 通过Whisper、Deepgram或AssemblyAI将音频转换为字幕 |
| [字幕显示](rules/display-captions.md) | 以TikTok风格逐字显示字幕 |
| [导入SRT文件](rules/import-srt-captions.md) | 读取现有的.srt字幕文件 |

### 数据可视化

| 规则 | 说明 |
|------|-------------|
| [图表制作](rules/charts.md) | 动态条形图、折线图等数据可视化效果 |

### 高级功能

| 规则 | 说明 |
|------|-------------|
| [3D内容](rules/3d.md) | 使用Three.js和React Three Fiber实现3D效果 |
| [Lottie动画](rules/lottie.md) | 通过Lottie导入After Effects动画 |
| [样式设计](rules/tailwind.md) | 使用Tailwind CSS为视频添加样式 |
| [元素尺寸测量](rules/measuring-dom-nodes.md) | 在渲染时测量DOM元素的尺寸 |

### 媒体辅助工具

| 规则 | 说明 |
|------|-------------|
| [视频时长获取](rules/get-video-duration.md) | 获取视频的总时长（秒） |
| [视频尺寸获取](rules/get-video-dimensions.md) | 获取视频的宽度和高度 |
| [音频时长获取](rules/get-audio-duration.md) | 获取音频的时长 |
| [帧提取](rules/extract-frames.md) | 在指定时间点提取视频帧 |

---

## 快速入门

```bash
# Scaffold a project
npx create-video@latest my-video

# Preview in browser
cd my-video && npm start

# Render to MP4
npx remotion render src/index.ts MyComposition out/video.mp4

# Pass dynamic data
npx remotion render src/index.ts MyComposition out.mp4 --props '{"title": "Hello"}'
```

---

## 贡献方式：

**源代码地址：** [github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit)

如果您发现任何遗漏的内容或更好的实现方法，请随时提交Pull Request——欢迎添加新规则、优化示例或修复错误。

本工具包由[Zone 99](https://99.zone)团队开发。