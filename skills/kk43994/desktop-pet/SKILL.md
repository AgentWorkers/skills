---
name: desktop-pet
description: "给 OpenClaw 赋予一个“实体”吧——它是一个小巧的、由玻璃制成的桌面宠物，可以模拟各种液体流动的视觉效果；它具备语音克隆功能，支持 15 种以上的眼部表情变化，还能在桌面显示歌词，并且拥有 7 种不同的情绪色彩。OpenClaw 基于 Electron 开发，所有动画效果都通过纯 CSS 和 JS 实现。"
homepage: https://github.com/kk43994/claw-desktop-pet
metadata: {"clawdbot":{"emoji":"🦞","requires":{"bins":["node","npm"],"env":[]}}}
---

# 🦞 Claw Desktop Pet — 为 OpenClaw 增添实体形态

这是一个桌面 AI 伴侣，让你的 OpenClaw 代理在桌面上拥有一个真实的“存在”。

## 它是什么？

这是一个 67 像素的流体玻璃球，它会“呼吸”、眨眼、说话，并对用户的操作做出反应。信息会以白色发光文字的形式显示在桌面上，就像漂浮的歌词一样。你的 OpenClaw 代理再也不会“隐形”了！

## 主要功能

- 🫧 **流体玻璃球**：67 像素的球体，支持 7 种不同的情感表达颜色
- 👀 **15 种以上的眼神表情**：眨眼、好奇、困倦、惊讶、跟随鼠标移动
- 🎵 **桌面歌词**：文字以打字机风格显示，带有白色发光效果，鼠标可以穿过这些文字
- 🎤 **语音克隆**：使用 MiniMax Speech 技术实现语音克隆，支持 7 种情感表达，能自动识别用户的情感
- 🎨 **双窗口架构**：由精灵图和歌词组成，完全透明
- ⚫ **离线/在线动画效果**：从灰色睡眠状态变为彩色状态，并伴有粒子效果
- 💬 **Feishu/Lark 协同**：支持双向消息同步
- 🛡️ **企业级稳定性**：具备自动重启、错误处理和性能监控功能

## 快速入门

```bash
# Clone the project
git clone https://github.com/kk43994/claw-desktop-pet.git
cd claw-desktop-pet

# Install dependencies
npm install

# Start (basic mode)
npm start

# Full AI mode — requires OpenClaw gateway running
openclaw gateway start
npm start
```

## 语音设置（可选）

### MiniMax Speech（推荐使用——支持语音克隆和情感表达）
请在 `pet-config.json` 文件中设置你的 MiniMax API 密钥：
```json
{
  "minimax": {
    "apiKey": "your-api-key",
    "voiceId": "your-cloned-voice-id"
  }
}
```

### 备选方案：Edge TTS（免费，无需额外设置）
直接使用 Microsoft Edge 的 TTS 功能作为备用方案。

## 技术架构

```
┌── Sprite Window (200×220) ──┐  ┌── Lyrics Window (400×100) ──┐
│  67px fluid glass ball       │  │  Desktop lyrics overlay      │
│  15+ eye expressions         │  │  Typewriter + white glow     │
│  SVG icon toolbar            │  │  Mouse pass-through          │
│  7 mood color systems        │  │  Auto-fade after voice done  │
└──────────────────────────────┘  └──────────────────────────────┘
```

## 使用的技术栈

- **Electron**：桌面应用程序框架（支持双窗口透明效果）
- **OpenClaw**：AI 对话引擎
- **MiniMax Speech**：用于实现语音克隆和情感表达
- **Pure CSS/JS**：所有动画效果均使用纯 CSS 和 JavaScript 实现，无需使用精灵图文件

## 设计理念

- **“空气感”用户界面**：设计风格类似桌面歌词，不会干扰用户的工作
- **iOS 风格的极简主义**：简洁优雅，仅使用图标作为操作按钮
- **“龙虾”主题**：通过红色和橙色的流体颜色来表达角色的特性（而非使用真实的肢体）
- **设计灵感来源**：Nomi 机器人、AIBI 机器人、Bunny Hole 等设计作品

## 链接

- 🔗 GitHub：https://github.com/kk43994/claw-desktop-pet
- 📖 完整的文档请参阅 README 文件
- 📄 采用 MIT 许可协议

---

由 Zhouk (kk43994) 用爱心和创意制作