# WhatsApp 视频功能

使用 Remotion 工具创建具有 WhatsApp 风格的动画聊天视频，非常适合在 X、TikTok 和 Instagram Reels 上使用。

## 主要功能

- 📱 具有动态岛（Dynamic Island）功能的真实 iPhone 界面
- 💬 WhatsApp 暗黑模式 UI（颜色、气泡和时间戳均精确还原）
- 📜 消息滚动时自动滚动
- 🔤 大字号、易读的字体（专为移动设备优化）
- 🎵 消息通知音效
- ✨ 消息出现时的弹簧动画效果
- ⌨️ 打字指示器（显示“...”气泡）
- 🔗 链接预览卡片
- ✅ 已读标记（蓝色对勾）
- **支持粗体**和代码格式

## 默认设置

- **宽高比：** 4:5（1080×1350）——最适合 X/Instagram 的信息流显示
- **无开场/结尾动画**——视频直接从聊天内容开始和结束
- **字体大小：** 2 倍——在移动设备上更易阅读
- **自动滚动**——确保所有消息都能显示

## 先决条件

此功能需要具备 **Remotion Best Practices** 技能：

```bash
npx skills add remotion-dev/skills -a claude-code -y -g
```

## 快速入门

```bash
cd ~/Projects/remotion-test
```

在 `src/WhatsAppVideo.tsx` 中编辑聊天内容，然后进行渲染：

```bash
npx remotion render WhatsAppDemo out/my-video.mp4 --concurrency=4
```

## 如何创建新视频

### 1. 定义消息内容

编辑 `src/WhatsAppVideo.tsx` 中的 `ChatMessages` 组件：

```tsx
// Incoming message (from assistant)
<Message
  text="Your message text here"
  isOutgoing={false}
  time="8:40 AM"
  delay={125}  // Frame when message appears (30fps)
/>

// Outgoing message (from user)
<Message
  text="Your outgoing message"
  isOutgoing={true}
  time="8:41 AM"
  delay={200}
  showCheck={true}
/>

// Typing indicator (shows "..." bubbles)
<TypingIndicator delay={80} duration={45} />
```

### 2. 时间控制

- **30 fps** = 每秒 30 帧
- `delay={30}` = 消息在 1 秒后显示
- `delay={60}` = 消息在 2 秒后显示
- `duration={45}` = 消息持续 1.5 秒

**典型流程：**
1. 第一条消息：`delay={20}`（约 0.7 秒）
2. 打字指示器：`delay={80}`，`duration={45}`（显示打字过程）
3. 回复：`delay={125}`（打字结束后）
4. 下一条消息：`delay={175}`，`duration={45}`（回复内容）
5. 下一条回复：`delay={220}`

### 3. 调整滚动效果

在 `ChatMessages` 组件中，根据消息数量更新滚动效果：

```tsx
const scrollAmount = interpolate(
  frame,
  [scrollStart, scrollStart + 60, messageFrame, lastFrame],
  [0, firstScroll, firstScroll, finalScroll],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

如果消息过多，可以适当增加滚动速度。

### 4. 文本格式

支持以下文本格式：
- **粗体**：`**bold text**
- **代码**：使用反引号 `**` 包围代码
- 换行：在字符串中使用 `\n`
- 表情符号：直接使用即可 🎬

### 5. 自定义标题

在 `ChatHeader` 组件中，可以修改以下内容：
- 名称：`Pokey 🐡` → 更改为你的助手名称
- 状态：`online`（在线）
- 头像表情符号

### 6. 更新视频时长

在 `Root.tsx` 中设置 `durationInFrames` 以匹配视频长度：
- 计算从第一条消息出现到视频结束所需的帧数，并加上约 100 帧的缓冲时间
- 以 30 fps 计算：450 帧 = 15 秒

### 7. 渲染视频

```bash
# Standard render
npx remotion render WhatsAppDemo out/video.mp4 --concurrency=4

# Higher quality
npx remotion render WhatsAppDemo out/video.mp4 --codec h264 --crf 18

# Preview in browser
npm run dev
```

## 平台适配

编辑 `Root.tsx` 以适应不同平台的尺寸：

| 平台 | 尺寸 | 宽高比 | 适用场景 |
|----------|------------|--------------|----------|
| **X/Instagram 信息流** | 1080×1350 | 4:5 | 默认设置，显示效果最佳 |
| **X/TikTok/Reels** | 1080×1920 | 9:16 | 全屏垂直显示 |
| **X 平方屏** | 1080×1080 | 1:1 | 通用尺寸 |
| **YouTube/X 横屏** | 1920×1080 | 16:9 | 横屏显示 |

## 项目结构

```
~/Projects/remotion-test/
├── src/
│   ├── WhatsAppVideo.tsx   # Main video component
│   └── Root.tsx            # Composition config
├── public/
│   └── sounds/
│       ├── pop.mp3         # Message received
│       └── send.mp3        # Message sent
└── out/                    # Rendered videos
```

## 音效

音效通过 `Sequence` 模块触发：

```tsx
<Sequence from={125}>
  <Audio src={staticFile("sounds/pop.mp3")} volume={0.5} />
</Sequence>
```

## 使用技巧

1. **编辑时预览**：运行 `npm run dev` 可实时查看效果
2. **逐帧检查**：使用时间轴工具调整动画时机
3. **保持消息简洁**：过长的消息可能需要调整滚动效果
4. **在移动设备上测试**：检查视频在真实尺寸下的可读性

## 使用 Pokey 生成视频

只需描述对话内容：
- “创建一个 WhatsApp 视频，内容是我请求你[执行某事]”
- “制作一个展示[对话内容的聊天视频”

Pokey 会负责编写消息内容、设置动画时机、渲染视频，并生成 MP4 文件。