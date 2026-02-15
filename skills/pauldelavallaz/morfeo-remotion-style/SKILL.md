---
name: morfeo-remotion-style
description: Morfeo Academy的Remotion视频风格指南：  
在为Paul/Morfeo Academy创建Remotion视频、故事或动画时，请遵循本指南。  
该指南适用于以下场景：  
- 使用“estilo Morfeo”、“mi estilo Remotion”、“video para Morfeo”或任何与Morfeo相关的Remotion视频请求时。
---

# Morfeo Remotion 样式

本样式指南适用于与 Morfeo Academy 品牌相匹配的 Remotion 视频制作。

## 品牌颜色

```typescript
export const colors = {
  lime: "#cdff3d",      // Primary accent - VERY IMPORTANT
  black: "#050508",     // Background
  darkGray: "#111111",  // Secondary bg
  white: "#FFFFFF",     // Text
  gray: "#888888",      // Muted text
};
```

## 字体排版

```typescript
import { loadFont as loadDMSans } from "@remotion/google-fonts/DMSans";
import { loadFont as loadInstrumentSerif } from "@remotion/google-fonts/InstrumentSerif";
import { loadFont as loadJetBrainsMono } from "@remotion/google-fonts/JetBrainsMono";

export const fonts = {
  heading: `${instrumentSerif}, serif`,  // Títulos - ALWAYS italic
  body: `${dmSans}, sans-serif`,         // Cuerpo
  mono: `${jetBrainsMono}, monospace`,   // Código
};
```

**规则：**
- 标题：使用 **Instrument Serif** 字体，**始终使用斜体**，字体大小为 400
- 正文：使用 DM Sans 字体，字体大小为 400-600
- 代码/技术内容：使用 JetBrains Mono 字体

## 表情符号

通过 CDN 使用 Apple 表情符号（Remotion 无法渲染系统自带的表情符号）：

```typescript
// See references/AppleEmoji.tsx for full component
<AppleEmoji emoji="🤖" size={28} />
<InlineEmoji emoji="🎙️" size={38} />  // For inline with text
```

## 品牌图标（WhatsApp、Telegram 等）

使用内联 SVG 图标，而非图标库（图标库在 Remotion 中无法正常显示）：

```typescript
// See references/BrandIcon.tsx for full component
<BrandIcon brand="whatsapp" size={44} />
<BrandIcon brand="telegram" size={44} />
```

## 动画风格

### Spring Config
```typescript
spring({ 
  frame, 
  fps, 
  from: 0, 
  to: 1, 
  config: { damping: 15 }  // Standard damping
});
```

### 视频元素展示顺序（交错式显示）
1. **标签**（第 0-15 帧）：从顶部逐渐显示并滑动
2. **表情符号**（第 15 帧以后）：从 0 开始逐渐放大
3. **标题**（第 30-50 帧）：从底部逐渐显示并滑动
4. **文字**（第 60、90、120 帧）：交错式逐渐显示

### 表情符号的脉动效果
```typescript
const pulse = interpolate(
  frame % 60,
  [0, 30, 60],
  [1, 1.1, 1],
  { extrapolateRight: "clamp" }
);
```

## 常见元素

### 绿色标签（屏幕顶部）
```typescript
<div style={{
  position: "absolute",
  top: 80,
  fontSize: 28,
  fontWeight: 600,
  fontFamily: fonts.body,
  color: colors.black,
  backgroundColor: colors.lime,
  padding: "12px 28px",
  borderRadius: 30,
  display: "flex",
  alignItems: "center",
  gap: 8,
}}>
  <AppleEmoji emoji="🤖" size={28} /> TEXT HERE
</div>
```

### 大号表情符号（屏幕中央）
```typescript
<AppleEmoji emoji="🗣️" size={140} />
```

### 标题（使用斜体的 Instrument Serif 字体）
```typescript
<h1 style={{
  fontSize: 68,
  fontWeight: 400,
  fontFamily: fonts.heading,
  fontStyle: "italic",  // ALWAYS
  color: colors.white,
  textAlign: "center",
  lineHeight: 1.15,
}}>
  Text with <span style={{ color: colors.lime }}>lime accent</span>
</h1>
```

## 视频规格
- **格式：** 1080x1920（9:16 的竖屏视频）
- **帧率：** 30 帧/秒
- **时长：** 每个视频片段 5 秒（共 150 帧）
- **背景颜色：** 始终使用 `colors.black`（#050508）

## 项目设置

```bash
npx create-video@latest --template blank
npm i @remotion/google-fonts
```

## 文件结构

```
src/
├── styles.ts          # Colors & fonts exports
├── AppleEmoji.tsx     # Emoji component
├── BrandIcon.tsx      # Brand icons (WhatsApp, Telegram, etc.)
├── [StoryName].tsx    # Individual stories
└── Root.tsx           # Composition setup
```

## 参考资料
- `references/styles.ts` - 完整的样式文件
- `references/AppleEmoji.tsx` - Apple 表情符号组件
- `references/BrandIcon.tsx` - 品牌图标组件
- `references/MorfeoStory-example.tsx` - 完整的视频示例文件

## 禁止使用的内容
- ❌ **禁止使用系统自带的字体**（无法正常显示）
- ❌ **禁止使用 simple-icons 等图标库**（无法在 Remotion 中使用）
- ❌ **禁止使用非斜体的标题**
- ❌ **禁止使用 palette 之外的颜色**
- ❌ **必须使用绿色作为视觉重点颜色**