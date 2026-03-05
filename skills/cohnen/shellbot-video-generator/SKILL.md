---
name: shellbot-video-generator
description: 使用 Remotion 的 AI 视频制作工作流程：适用于创建视频、短片、广告或动态图形。该流程可根据需求自动生成宣传视频、产品演示视频、社交媒体视频、动画讲解视频等程序化视频内容。它能够制作出高质量、专业的动态图形（而非简单的幻灯片展示）。使用该流程需要具备 `FIRECRAWL_API_KEY` 来执行网站抓取和品牌资产提取操作。
metadata:
  openclaw:
    primaryEnv: "FIRECRAWL_API_KEY"
    requires:
      env:
        - "FIRECRAWL_API_KEY"
    homepage: "https://getshell.ai"
---
# 视频生成器（Remotion）

使用 React 和 Remotion 通过编程方式创建专业的动态图形视频。

## 必须遵循的故事结构（AIDA）

每个视频都必须按照 AIDA 的结构进行：

1. **吸引注意力（Attention）** — 在前 3 秒内明确说明要解决的问题。
2. **引发兴趣（Interest）** — 介绍解决方案，展示其功能及其重要性。
3. **激发欲望（Desire）** — 展示使用场景，让观众感受到实际应用效果。
4. **引导行动（Action）** — 以包含激励措施（折扣、免费试用、限时优惠）的呼叫行动（CTA）结束。

## 默认工作流程（务必遵循）

1. **使用 Firecrawl 抓取品牌数据**（如果视频中包含产品信息）。
2. **使用本地模板创建项目**：
   ```bash
   cd output && bash ../scripts/remotion.sh init <project-name>
   ```
3. **使用 `npm install` 安装依赖项**。
4. **构建所有动态图形场景**。
5. **在后台运行 Remotion Studio**：
   ```bash
   cd output/<project-name> && npm run dev
   ```
   等待端口 3000 上显示“服务器已准备好”的提示。
6. **通过 Cloudflare 隧道发布视频**：
   ```bash
   bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000
   ```
7. **将公开 URL 发送给用户**（例如：`https://xxx.trycloudflare.com`）。

用户可以在浏览器中预览视频，提出修改请求，你再编辑源文件。Remotion 会自动热加载修改内容。

### 渲染（仅在用户明确要求导出时进行）：
```bash
cd output/<project-name>
npx remotion render CompositionName out/video.mp4
```

## 快速入门

```bash
# Scaffold project from local template (no network needed)
cd output && bash ../scripts/remotion.sh init my-video
cd my-video && npm install

# Add motion libraries
npm install lucide-react

# Start dev server
npm run dev

# Expose publicly
bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000
```

## 收集视觉素材

**强制要求：** 每个视频都需要视觉素材——徽标、截图、产品图片、品牌颜色。请在设计场景之前收集这些素材。素材来源有三种：

### 1. 使用 Firecrawl 抓取（适用于任何产品/公司网站）

Firecrawl 可以抓取网站信息，并一次性提取品牌数据及可复用的图片：

```bash
# Scrape and auto-download assets to the project's public/images/brand/
bash scripts/firecrawl.sh "https://example.com" output/my-video/public/images/brand
```

抓取结果会返回一个 JSON 对象，其中包含以下内容：`brandName`（品牌名称）、`tagline`（标语）、`headline`（标题）、`description`（描述）、`features`（功能）、`logoUrl`（徽标链接）、`faviconUrl`（图标链接）、`primaryColors`（品牌主色调的十六进制代码）、`ctaText`（呼叫行动文本）、`socialLinks`（社交媒体链接）、`imageUrls`（封面图片、产品图片、插图等）。

同时，系统会自动将这些图片下载到 `screenshot.png`、`og-image.png`、`favicon.png`、`logo.png` 以及所有提取的页面图片（`image-1.png`、`image-2.png` 等）文件夹中。

**API 密钥：** 将 `FIRECRAWL_API_KEY` 设置在环境变量或 `.env` 文件中。

### 2. 用户提供的素材

用户可以直接提供徽标、图片或截图（以文件路径或 URL 的形式）。务必询问用户是否需要包含特定素材，并将它们保存到 `public/images/` 目录中：

```bash
mkdir -p public/images
curl -sL "https://user-provided-url.com/logo.png" -o public/images/logo.png
```

### 3. 从抓取数据中手动下载素材

如果需要从抓取的Markdown内容中下载特定图片（例如计划卡片、频道图标），请直接进行下载：

```bash
curl -sL "https://example.com/path/to/image.png" -o public/images/image.png
```

### 在 Remotion 中使用素材

使用 `staticFile()` 函数引用下载的素材：

```tsx
import { Img, staticFile } from "remotion";

<Img src={staticFile("images/brand/logo.png")} />
<Img src={staticFile("images/brand/screenshot.png")} />
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

### 应避免的技巧（幻灯片式设计）

- 场景切换时使用渐变为黑色的效果。
- 在纯色背景上放置居中的文本。
- 所有场景使用相同的过渡效果。
- 线性或机械式的动画效果。
- 静态的屏幕布局。
- 使用 `slideLeft`、`slideRight`、`crossDissolve`、`fadeBlur` 等预设过渡效果。
- **绝对不要使用表情符号图标**，应使用 Lucide React 提供的图标。

### 应追求的动态图形设计技巧

- **重叠的过渡效果**——下一个场景在当前场景结束前就开始显示。
- **分层构图**（背景/中间层/前景层）。
- 使用模拟物理效果的动画（如弹簧动画）来营造自然的感觉。
- 不同场景之间的动画时长要有所变化（2-5 秒）。
- 在不同场景中保持视觉元素的连续性。
- 使用 `clipPath`、3D 变形等自定义过渡效果。
- 使用 Lucide React 绘制所有图标（`npm install lucide-react`）——绝对不要使用表情符号。

## 过渡效果技巧

1. **渐变/缩放**——元素逐渐放大直至充满屏幕，然后成为下一个场景的背景。
2. **擦拭效果**——彩色形状从屏幕一侧滑过，展示下一个场景。
3. **缩放进入**——摄像机逐渐进入元素，然后展示新场景。
4. **路径渐显**——圆形或多边形从某个点开始逐渐显现。
5. **固定元素**——在周围元素变化时，某个元素保持不变。
6. **方向性过渡**——第一个场景从右侧退出，第二个场景从右侧进入。
7. **分割/展开**——屏幕分成多个部分，各部分依次滑动展示。
8. **三维旋转**——场景在 Y 轴上进行旋转。

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

### 字体设计
- 最多使用一种显示字体和一种正文字体。
- 使用粗体标题，调整字距以增强层次感。
- 通过不同的字体粗细来区分内容的层级。
- 保持文本简短（观众无法暂停观看）。

### 颜色搭配
- **使用 Firecrawl 抓取到的品牌颜色** 作为主要配色方案，确保与产品的实际外观一致。
- **除非品牌特别要求或用户特别指定，否则避免使用紫色或靛蓝色渐变**。
- 简洁明了的背景效果通常更佳——单一的深色调或微妙的渐变效果比复杂的多层纹理更合适。
- 从品牌设计中提取有意义的强调色。

### 布局设计
- 使用不对称的布局，避免文本居中显示。
- 将元素边缘对齐以创造视觉张力。
- 适当留白作为设计元素。
- 谨慎使用深度效果——可以使用轻微的背景模糊或单一的渐变效果，而不是复杂的纹理叠加。

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

将需要保持显示的元素放置在序列块之外：

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

在发布视频之前，请进行以下测试：

- **静音测试**：视频内容在没有声音的情况下是否仍能清晰传达信息？
- **眯眼测试**：在眯眼观看时，页面的层次结构是否仍能清晰可见？
- **时长测试**：动画是否自然流畅，没有机械感？
- **一致性测试**：相似的元素是否表现一致？
- **幻灯片式效果测试**：视频看起来是否不像普通的 PowerPoint 演示文稿？
- **循环播放测试**：视频能否顺利循环播放至开头？

## 实现步骤

1. **使用 Firecrawl 抓取品牌数据**（如果视频中包含产品信息，先抓取该产品的网站数据）。
2. **确定整体风格**——设定视频的氛围、摄像机视角和情感基调。
3. **视觉方向**——选择颜色、字体、品牌风格和动画效果。
4. **分解场景**——列出每个场景的详细信息，包括描述、时长、文字内容和过渡效果。
5. **收集素材**——用户提供的素材、自动生成的图片/视频以及抓取到的品牌素材。
6. **设置时长**——调整各场景的时长（2-3 秒的简短场景，4-5 秒的复杂场景）。
7. **创建背景层**——为所有场景添加动画背景。
8. **构建每个场景**——为每个场景设置进入/退出动画，以及关键动画效果。
9. **设计开场场景**——创建具有吸引力的开场动画。
10. **构建故事结构**——根据内容来组织中间场景。
11. **设计结尾部分**——确保视频有一个有意义的结尾。
12. **启动 Remotion Studio**——在端口 3000 上运行 `npm run dev`。
13. **通过 Cloudflare 隧道发布视频**：执行 `bash skills/cloudflare-tunnel/scripts/tunnel.sh start 3000` 命令。
14. **将公开 URL 发送给用户**——用户可以预览并实时提出修改请求。
15. **迭代修改**——根据用户反馈编辑源文件并重新生成视频。
16. **仅在用户要求导出最终版本时进行渲染**。

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

有关可复用的组件，请参阅 `references/components.md`：
- 动态背景效果
- 终端窗口界面
- 功能卡片
- 统计数据显示组件
- 呼叫行动按钮
- 文本渐显动画效果

## Cloudflare 隧道管理

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