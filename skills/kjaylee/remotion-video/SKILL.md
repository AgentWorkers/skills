---
name: remotion-video
description: 使用 Remotion 在 MiniPC 上创建程序化视频。适用于制作视频内容、动画、动态图形、社交媒体剪辑或任何基于 React 的视频项目。涵盖动画、素材、音频、字幕、过渡效果以及渲染等方面的内容。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from remotion-dev/skills, adapted for our MiniPC Remotion setup
---

# 使用Remotion在MiniPC上进行视频制作

使用MiniPC上的Remotion工具，可以通过编程方式制作视频。

## 开发环境

- **项目目录：** `$HOME/remotion-videos`  
- **执行命令：** `npx remotion render <CompositionId> out/video.mp4`  
- **ffmpeg**：已安装  
- **传输方式：** 通过MiniPC的HTTP服务器（端口9877）使用curl将视频传输到Mac Studio

## 核心概念

### **Composition（组合）**：视频的基本构成单元  
```tsx
<Composition
  id="MyVideo"
  component={MyComponent}
  durationInFrames={150}  // 30fps × 5초 = 150프레임
  fps={30}
  width={1920}
  height={1080}
/>
```

### **时间控制**  
```tsx
const frame = useCurrentFrame();         // 현재 프레임
const { fps, durationInFrames } = useVideoConfig();

// 보간 (interpolate)
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp'
});

// 스프링 애니메이션
const scale = spring({ frame, fps, config: { damping: 200 } });
```

### **序列化（Sequentialization）**  
```tsx
<Sequence from={0} durationInFrames={60}>
  <IntroScene />
</Sequence>
<Sequence from={60} durationInFrames={90}>
  <MainContent />
</Sequence>
```

## 常用制作模式

### 资源的使用

- **图片：** `<Img src={staticFile('logo.png')} />`  
- **视频：** `<OffthreadVideo src={staticFile('clip.mp4')} />`  
- **音频：** `<Audio src={staticFile('bgm.mp3')} volume={0.5} />`  
- **字体：** 使用Google Fonts的`Noto Sans KR`  
- **本地字体：** 需要将其放置在`public/`文件夹中  

### 字幕/字幕文件

- **使用`@remotion/captions`包**  
- 从JSON或SRT格式的文件中加载字幕，并确保字幕与视频同步  

### 过渡效果（Transitions）

- **使用`@remotion/transitions`**来实现淡入、淡出、擦除等效果  
- 通过`<TransitionSeries>`组件实现场景切换  

### Tailwind CSS

- 在项目中启用`@remotion/tailwind`后，可以方便地使用相关的CSS样式  

### 3D内容

- **结合`@react-three/fiber`和`@remotion/three`**  
- 将Three.js创建的3D场景同步到Remotion的时间轴中  

## 渲染过程

```bash
# 기본 렌더링
cd $HOME/remotion-videos
npx remotion render MyVideo out/video.mp4

# 고품질
npx remotion render MyVideo out/video.mp4 --codec h264 --crf 18

# 투명 배경 (WebM)
npx remotion render MyVideo out/video.webm --codec vp8

# GIF
npx remotion render MyVideo out/animation.gif --every-nth-frame 2
```

## 制作工作流程

1. **规划：** 确定每个场景的组成、时长和分辨率。  
2. **准备资源：** 将图片、音频和字体文件放入`public/`文件夹。  
3. **编写组件代码：** 使用React为每个场景编写对应的代码。  
4. **预览：** 在MiniPC上使用`npx remotion studio`进行预览。  
5. **渲染：** 使用无头渲染（headless rendering）将视频输出为MP4或WebM格式。  
6. **传输：** 将渲染后的视频通过HTTP服务器传输到Mac Studio。  

## 注意事项

- **渲染过程可能较为耗时**：视频渲染需要较长的时间。  
- **默认帧率为30fps**：可根据需求调整为60fps。  
- **注意内存使用**：高分辨率或长视频可能会超出MiniPC的内存限制。  
- **无法直接通过GitHub推送**：请在Mac Studio端进行代码的推送和上传。