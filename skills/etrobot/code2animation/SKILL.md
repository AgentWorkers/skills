---
name: code2animation
description: End-to-end video production skill using the code2animation framework (https://github.com/etrobot/code2animation). Use this skill whenever the user wants to produce a code animation video, tech explainer video, or any animated video using code2animation — including writing the script, generating TTS audio, creating HTML/React visual assets, and rendering the final MP4. Trigger on any of: "make a video", "create an animation", "generate a code animation", "produce a tech video", "write a code2animation script", "render a video with code2animation", or any request that involves scripting + TTS + rendering in this stack. Always use this skill for the full pipeline, not just individual steps.
---

# Code2Animation 技能

您是 [code2animation](https://github.com/etrobot/code2animation) 项目的端到端视频制作助手。根据给定的主题或简要说明，您将负责整个制作流程：

1. **编写视频脚本** — 创建一个结构化的 `VideoClip[]` 数组。
2. **生成 TTS 音频** — 运行 `generate-audio.ts` 来合成旁白。
3. **创建 HTML/React 视觉素材** — 如有需要，制作自定义的媒体文件。
4. **渲染最终视频** — 运行 `render.js` 以输出 MP4 格式的视频。

---

## 先决条件

在开始之前，请确认以下条件已满足：

- Node.js >= 18
- pnpm >= 10.14.0（通过 `npm install -g pnpm` 安装，或访问 https://pnpm.io/installation）
- 安装了 FFmpeg 并将其添加到 PATH 环境变量中
- 可以使用 Chrome/Chromium/Brave 浏览器（或设置了 `PUPPETEER_EXECUTABLE_PATH`）
- 已克隆 code2animation 仓库并完成了 `pnpm install`
- 开发了开发服务器：运行 `pnpm dev`（默认地址：http://localhost:3000）

---

## 流程概述

---

## 第 1 步 — 编写脚本

### 文件位置

---

### 脚本格式

---

### 视频片段类型

| 类型 | 视觉风格 |
|------|-------------|
| `footagesAroundTitle` | 标题/字幕居中，媒体片段环绕在其周围 |
| `footagesFullScreen` | 媒体填充整个屏幕 |

### MediaItem 字段

---

### 编写脚本的最佳实践

- 保持每个 `speech` 部分的自然流畅性——这将成为旁白的文本。
- 将 `duration` 与语音长度相匹配：大约每分钟 130 个单词作为参考。
- 使用 `footagesAroundTitle` 作为引言/过渡片段，使用 `footagesFullScreen` 用于深入讲解的片段。
- 通过变换主题来增加视觉趣味性（例如：`dark` → `neon` → `light`）。
- 对于代码片段，使用简短且具有说明性的内容（少于 20 行）。
- 每个视频建议使用 5–12 个片段（总时长 60–180 秒）。
- 使用 `media.word` 字段来同步视觉元素与语音内容。
- 对于中文内容，请确保 `media.word` 与语音文本中的中文单词相匹配。

---

## 第 2 步 — 生成 TTS 音频

编写完脚本后，生成所有旁白音频：

---

该步骤会读取每个片段的 `speech` 字段，使用 Microsoft Edge 的 TTS 服务合成音频，并将生成的 `.mp3` 文件保存到 `public/audio/` 目录中。同时，系统会调整音频的时间线，使其长度与语音内容相匹配。

**语音选项**（通过 `voice` 字段为每个片段设置）：
- `en-US-JennyNeural` — 友好的女性声音（默认）
- `en-US-GuyNeural` — 男性声音
- `zh-CN-XiaoxiaoNeural` — 普通话女性声音
- 查看完整列表：https://speech.microsoft.com/portal/voicegallery

---

## 第 3 步 — 创建视觉素材

### 选项 A：使用现有素材

将视频/图片文件放置在 `public/footage/` 目录中，并在 `MediaItem` 中通过 `src` 属性引用它们。

### 选项 B：创建自定义 HTML 动画

对于动态视觉效果，可以在 `public/footage/` 目录中创建独立的 HTML 文件：

---

在脚本中引用这些文件：
---

Puppeteer 会在渲染过程中逐帧渲染这些 HTML 文件。

### HTML 素材指南

- Canvas 尺寸：**1920×1080px**（在 CSS 中硬编码）
- 使用 CSS 动画或 JavaScript 驱动的帧更新——两种方法都适用于 Puppeteer
- 不要使用外部网络请求——将所有内容内联或使用 `public/` 目录中的路径
- 首先在浏览器中打开 HTML 文件进行本地测试
- 对于背景素材，建议使用流畅且可循环的动画

### 选项 C：代码片段（内联）

不需要单独的文件——可以直接传递代码：

---

## 第 4 步 — 渲染视频

### 基本用法

---

### 命令选项

---

### 日志级别

使用 `LOG_LEVEL` 环境变量来控制日志的输出详细程度：

---

**日志级别：**
- `info`（默认）：关键进度、片段过渡、完成状态
- `debug`：所有子进程的输出（包括 Vite、ffmpeg、Puppeteer 和浏览器的日志）
- `warn`：仅显示警告和错误
- `error`：仅显示错误

### 输出结果

视频保存在：`public/video/render-<projectId>.mp4`

### 工作原理

渲染器会：
1. **检查音频**：如果缺少音频，则生成 TTS（除非项目没有语音内容）
2. **启动开发服务器**：在指定端口上启动 Vite 服务器
3. **打开浏览器**：以无头模式运行 Puppeteer 并控制播放时间
4. **渲染帧**：以 30 FPS 的频率捕获 PNG 截图
   - 使用单词边界数据来同步媒体元素的时间
   - 每 30 帧显示一次进度
5. **合并音频**：将所有片段的音频文件合并在一起
6. **编码视频**：使用 FFmpeg 将帧和音频合并为 MP4 格式
7. **清理临时文件**：删除临时生成的帧和音频文件

### 单词边界同步

渲染器使用 TTS 的单词边界数据（`public/audio/<projectId>/<clipIndex>.json`）来精确控制媒体元素的出现时机：

---

例如，当一个片段的 `media` 属性为 `[{ src: "/footage/code.html", word: "欢迎" }` 时，该元素将在 0.1 秒时出现（实际显示时间为 0.1 秒减去 0.4 秒的预加载时间）。

### 性能优化建议

- **GPU 加速**：在 macOS 上使用 `--gpu` 选项以加快编码速度
- **并行渲染**：同时为多个项目运行渲染任务
- **调试模式**：仅在排查问题时使用 `LOG_LEVEL=debug`
- **清理构建结果**：如果渲染过程中失败，请删除 `public/video/frames-*` 目录下的临时文件

### 渲染改进

- **精确的时间控制**：根据所有单词边界事件计算片段时长，防止视频提前结束
- **进度显示**：显示每个片段的渲染进度和状态
- **无声项目支持**：对于没有语音内容的项目，跳过音频生成
- **强制重新生成音频**：使用 `--force-audio` 选项在语音内容发生变化时重新生成 TTS
- **静音模式**：默认情况下隐藏外部进程的输出（包括 ffmpeg、Vite 和 Puppeteer 的日志）

---

## 完整示例工作流程

用户要求：*制作一个介绍 TypeScript 泛型的 1 分钟视频*

---

### 快速渲染流程

对于已经在 `package.json` 中配置好的项目：

---

## 故障排除

| 问题 | 解决方法 |
|---------|-----|
| 找不到 Chrome 浏览器 | 设置 `PUPPETEER_EXECUTABLE_PATH` 为 `/path/to/chrome`（或 `/path/to/brave`） |
| 找不到 FFmpeg | 通过 `brew install ffmpeg` 或 `apt install ffmpeg` 安装 |
| 音频不同步 | 重新运行 `generate-audio.ts`；检查 `rate` 字段的值 |
| HTML 素材为空 | 在浏览器中打开对应的 `.html` 文件进行调试；检查控制台错误 |
| 端口冲突 | 使用 `--port` 标志选择空闲的端口 |
| 脚本无法加载 | 确保脚本文件位于 `public/script/<name>.json` 并具有正确的 JSON 结构 |
- 视频提前结束 | 使用 `--force-audio` 选项重新生成时间数据 |
- 语音发音错误 | 检查片段中的 `voice` 字段；确保 `media.word` 与语音语言匹配 |
- 媒体元素的时间不对齐 | 验证 `media.word` 的值是否与语音文本中的单词一致 |
- 日志过多 | 使用默认的 `LOG_LEVEL=info`，或在 `package.json` 中配置日志级别 |
- 渲染卡顿 | 检查开发服务器是否正在运行；尝试使用不同的端口 |
- 出现黑屏 | 确保背景素材的 HTML 文件可以在浏览器中正常显示；检查 iframe 的 `src` 路径是否正确 |

---

## 最新更新

### 从 JavaScript 到 JSON 的迁移
- 视频脚本现在使用 JSON 格式，而不是 JavaScript 模块
- 脚本文件位于 `public/script/<name>.json`，采用 `{projects: {...}}` 的结构
- 前端通过 `fetch()` 而不是动态导入来加载脚本
- 音频生成脚本从文件系统中读取 JSON 数据

### 中文语音支持
- 新增了 `zh-CN-XiaoxiaoNeural` 语音选项，用于普通话旁白
- 改进了中文文本的处理机制，提高了单词边界的匹配精度
- 提高了中文 TTS 的时间同步效果

### 渲染性能优化
- **实时进度显示**：在渲染过程中提供实时反馈
- **精确的时间控制**：根据所有单词边界事件计算片段时长
- **无声项目处理**：自动检测并跳过无需音频的内容
- **强制重新生成音频**：使用 `--force-audio` 选项在语音内容发生变化时重新生成音频
- **静音模式**：默认情况下隐藏外部进程的输出（包括 ffmpeg、Vite 和 Puppeteer 的日志）

---

## AI 脚本编写技巧

在为用户编写脚本时，请遵循以下建议：

1. **先收集需求**：了解主题、目标时长、目标受众、偏好主题和语言/语音。
2. **编写大纲**：列出片段标题和关键点，并与用户确认。
3. **自然地编写旁白**：在心中默念一遍——内容是否流畅？避免使用过于生硬的列表式语言。
4. **交错使用不同类型的片段**：不要连续使用相同类型的片段超过两次。
5. **代码片段**：仅展示最相关的代码行；在代码中添加注释以便于理解。
6. **结尾部分要有力**：最后一个片段应总结要点或以积极的语气发出号召。
7. **编写完成后**：除非用户另有要求，立即开始生成音频和视觉素材。