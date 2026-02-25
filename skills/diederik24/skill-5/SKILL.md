---
name: video-generator
description: 使用 Remotion 的 AI 视频制作工作流程：适用于创建视频、短片、广告或动态图形。该流程可根据需求自动生成宣传视频、产品演示视频、社交媒体视频、动画解释视频等程序化视频内容。其生成的成果为精美的动态图形，而非简单的幻灯片展示。
---
# 视频生成器（Remotion）

使用 React 和 Remotion 通过编程方式创建专业的动态图形视频。

## 默认工作流程（务必遵循）

1. **抓取品牌数据**（如果视频中包含产品信息）：使用 Firecrawl 工具。
2. 在 `output/<project-name>/` 目录下创建项目。
3. 制作所有包含动态图形的场景。
4. 使用 `npm install` 安装所需的依赖项。
5. 修改 `package.json` 中的脚本，以便使用 `npx remotion`（而非 `bun`）：
   ```json
   "scripts": {
     "dev": "npx remotion studio",
     "build": "npx remotion bundle"
   }
   ```
6. 以后台进程的方式启动 Remotion Studio：
   ```bash
   cd output/<project-name> && npm run dev
   ```
   等待端口 3000 上的 “Server ready” 信号。
7. 通过 Cloudflare Tunnel 将视频公开，以便用户可以访问：
   ```bash
   bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000
   ```
8. 将公共 URL 发送给用户（例如：`https://xxx.trycloudflare.com`）。

用户可以在浏览器中预览视频，提出修改请求，您只需编辑源文件即可。Remotion 会自动进行热重载。

### 渲染（仅在用户明确要求导出时执行）：
```bash
cd output/<project-name>
npx remotion render CompositionName out/video.mp4
```

## 快速入门

```bash
# Scaffold project
cd output && npx --yes create-video@latest my-video --template blank
cd my-video && npm install

# Add motion libraries
npm install lucide-react

# Fix scripts in package.json (replace any "bun" references with "npx remotion")

# Start dev server
npm run dev

# Expose publicly
bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000
```

## 使用 Firecrawl 获取品牌数据

**强制要求：** 当视频中提到或展示任何产品/公司时，在设计视频之前，使用 Firecrawl 抓取该产品的网站信息，包括品牌数据、颜色、截图和文案。这可以确保视觉效果的准确性和品牌一致性。

API 密钥：在 `.env` 文件中设置 `FIRECRAWL_API_KEY`（详见 `TOOLS.md`）。

### 使用方法

```bash
bash scripts/firecrawl.sh "https://example.com"
```

Firecrawl 会返回结构化的品牌数据：`brandName`（品牌名称）、`tagline`（标语）、`headline`（标题）、`description`（描述）、`features`（功能）、`logoUrl`（Logo 链接）、`faviconUrl`（favicon 链接）、`primaryColors`（主要颜色）、`ctaText`（呼叫行动文本）、`socialLinks`（社交媒体链接），以及截图 URL 和原始图片 URL。

### 抓取数据后下载资源

```bash
mkdir -p public/images/brand
curl -s "https://example.com/favicon.svg" -o public/images/brand/logo.svg
curl -s "${OG_IMAGE_URL}" -o public/images/brand/og-image.png
curl -sL "${SCREENSHOT_URL}" -o public/images/brand/screenshot.png
```

## 核心架构

### 场景管理

采用基于场景的架构，并设置适当的过渡效果：

```tsx
const SCENE_DURATIONS: Record<string, number> = {
  intro: 3000,     // 3s hook
  problem: 4000,   // 4s dramatic
  solution: 3500,  // 3.5s reveal
  features: 5000,  // 5s showcase
  cta: 3000,       // 3s close
};
```

### 视频结构模式

```tsx
import {
  AbsoluteFill, Sequence, useCurrentFrame,
  useVideoConfig, interpolate, spring,
  Img, staticFile, Audio,
} from "remotion";

export const MyVideo = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill>
      {/* Background music */}
      <Audio src={staticFile("audio/bg-music.mp3")} volume={0.35} />

      {/* Persistent background layer - OUTSIDE sequences */}
      <AnimatedBackground frame={frame} />

      {/* Scene sequences */}
      <Sequence from={0} durationInFrames={90}>
        <IntroScene />
      </Sequence>
      <Sequence from={90} durationInFrames={120}>
        <FeatureScene />
      </Sequence>
    </AbsoluteFill>
  );
};
```

## 动态图形设计原则

### 应避免的元素：

- 场景切换时使用渐变为黑色的效果。
- 在纯色背景上放置居中的文本。
- 所有元素的过渡效果都相同。
- 线性或机械式的动画效果。
- 静态的屏幕画面。
- 使用预设的过渡效果（如 `slideLeft`、`slideRight`、`crossDissolve`、`fadeBlur`）。
- 绝不要使用表情符号图标，应使用 Lucide React 提供的图标。

### 应追求的动态图形效果：

- 过渡效果要自然流畅（下一个场景应在当前场景结束后立即开始）。
- 使用分层构图（背景/中间层/前景层）。
- 通过模拟物理效果（如弹簧动画）来实现自然的动态效果。
- 不同场景的动画时长要有所变化（2-5 秒）。
- 在不同场景中保持视觉元素的连续性。
- 使用 `clipPath`、3D 变换和变形等自定义过渡效果。
- 所有图标都应使用 Lucide React 绘制（`npm install lucide-react`）——绝对不要使用表情符号图标。

## 过渡效果技巧：

1. **变形/缩放**：元素逐渐放大直至填满屏幕，然后成为下一个场景的背景。
2. **擦除效果**：彩色形状从屏幕一侧滑过，露出下一个场景。
3. **缩放进入/缩放退出**：镜头逐渐靠近或远离某个元素，然后进入新的场景。
4. **渐变显示**：圆形或多边形从某个点开始逐渐显现。
5. **固定元素**：在周围元素变化时，某个元素保持不变。
6. **方向性过渡**：第一个场景从右侧退出，第二个场景从右侧进入。
7. **分割/展开**：屏幕被分割，各个部分依次滑开。
8. **透视翻转**：场景在三维空间中沿 Y 轴旋转。

## 动画时长参考

```tsx
// Timing values (in seconds)
const timing = {
  micro: 0.1-0.2,      // Small shifts, subtle feedback
  snappy: 0.2-0.4,     // Element entrances, position changes
  standard: 0.5-0.8,   // Scene transitions, major reveals
  dramatic: 1.0-1.5,   // Hero moments, cinematic reveals
};

// Spring configs
const springs = {
  snappy: { stiffness: 400, damping: 30 },
  bouncy: { stiffness: 300, damping: 15 },
  smooth: { stiffness: 120, damping: 25 },
};
```

## 视觉风格指南

### 字体设计：
- 最多使用一种显示字体和一种正文字体。
- 使用粗体标题，并调整字距以增强层次感。
- 通过不同的字体粗细来区分内容的层次结构。
- 保持文本简短（观众无法暂停观看）。

### 颜色搭配：
- 使用 Firecrawl 抓取到的品牌颜色作为主要配色方案，确保与产品的实际外观一致。
- 除非品牌特别要求或用户明确指定，否则避免使用紫色或靛蓝色渐变。
- 简洁明了的背景设计最为合适——单色深色调或柔和的渐变效果比复杂的多层纹理更佳。
- 颜色应从品牌风格中提取，以突出重点。

### 布局设计：
- 使用非对称的布局和偏心的文字排列方式。
- 将元素边缘对齐以营造视觉张力。
- 适当留白作为设计元素。
- 尽量减少使用深度效果——轻微的背景模糊或单一的渐变效果比复杂的纹理更合适。

## Remotion 的关键功能

### 插值技术

```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp"
});

const scale = spring({
  frame, fps,
  from: 0.8, to: 1,
  durationInFrames: 30,
  config: { damping: 12 }
});
```

### 具有重叠效果的序列设计

```tsx
<Sequence from={0} durationInFrames={100}>
  <Scene1 />
</Sequence>
<Sequence from={80} durationInFrames={100}>
  <Scene2 />
</Sequence>
```

### 跨场景的连续性设计

将需要保持不变的元素放置在序列块之外：

```tsx
const PersistentShape = ({ currentScene }: { currentScene: number }) => {
  const positions = {
    0: { x: 100, y: 100, scale: 1, opacity: 0.3 },
    1: { x: 800, y: 200, scale: 2, opacity: 0.5 },
    2: { x: 400, y: 600, scale: 0.5, opacity: 1 },
  };

  return (
    <motion.div
      animate={positions[currentScene]}
      transition={{ duration: 0.8, ease: "easeInOut" }}
      className="absolute w-32 h-32 rounded-full bg-gradient-to-r from-coral to-orange"
    />
  );
};
```

## 质量测试

在交付视频之前，请进行以下测试：

- **静音测试**：视频内容在无声状态下是否仍能清晰呈现？
- **眯眼测试**：在眯眼看时，视频的层次结构是否仍然清晰可见？
- **时长测试**：动画是否自然流畅，没有机械感？
- **一致性测试**：相似的元素是否表现一致？
- **幻灯片效果测试**：视频看起来是否不像 PowerPoint 演示文稿？
- **循环播放测试**：视频能否顺利循环回开头？

## 实施步骤：

1. 使用 Firecrawl 抓取品牌数据（如果视频中包含产品信息）。
2. 确定视频的整体风格、镜头风格和情感基调。
3. 规划视频的视觉元素，包括颜色、字体、品牌风格和动画效果。
4. 列出所有场景的详细信息，包括场景名称、时长、文字内容及过渡效果。
5. 准备所需的资源，包括用户提供的素材、自动生成的图片/视频以及抓取到的品牌数据。
6. 为每个场景设定合适的时长（2-3 秒的简短场景，4-5 秒的复杂场景）。
7. 创建一个始终存在的背景层。
8. 为每个场景设计进入/退出动画，以及关键的时间节点。
9. 以一个引人注目的场景作为视频的开场。
10. 构建视频的叙事结构，确保内容连贯。
11. 启动 Remotion Studio（在端口 3000 上运行 `npm run dev`）。
12. 通过 Cloudflare Tunnel 公开视频。
13. 将视频的公共 URL 发送给用户，用户可以预览并实时提出修改请求。
14. 根据用户的反馈编辑源文件，并进行热重载。
15. 仅在用户要求导出最终版本时才进行渲染。

## 文件结构

```
my-video/
├── src/
│   ├── Root.tsx              # Composition definitions
│   ├── index.ts              # Entry point
│   ├── index.css             # Global styles
│   ├── MyVideo.tsx           # Main video component
│   └── scenes/               # Scene components (optional)
├── public/
│   ├── images/
│   │   └── brand/            # Firecrawl-scraped assets
│   └── audio/                # Background music
├── remotion.config.ts
└── package.json
```

## 常用组件

有关可复用的组件，请参考 `references/components.md`：
- 动态背景效果
- 终端窗口
- 功能卡片
- 统计数据显示
- 呼叫行动按钮
- 文本渐显动画

## Cloudflare Tunnel 的使用与管理

```bash
# Start tunnel (exposes port 3000 publicly)
bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000

# Check status
bash skills/cloudflare-tunnel/scripts/tunnel.sh status 3000

# List all tunnels
bash skills/cloudflare-tunnel/scripts/tunnel.sh list

# Stop tunnel
bash skills/cloudflare-tunnel/scripts/tunnel.sh stop 3000
```