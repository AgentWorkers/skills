---
name: webchat-audio-notifications
description: 为 Moltbot/Clawdbot 的网页聊天功能添加音频通知功能，支持 5 个不同的通知强度级别（从“低音量”到“高音量，足以被任何人听到”），并且仅在浏览器标签页处于后台状态时才会触发通知。
version: 1.1.0
author: brokemac79
repository: https://github.com/brokemac79/webchat-audio-notifications
homepage: https://github.com/brokemac79/webchat-audio-notifications
tags:
  - webchat
  - notifications
  - audio
  - ux
  - browser
  - howler
metadata:
  clawdbot:
    emoji: 🔔
    compatibility:
      minVersion: "2026.1.0"
      browsers:
        - Chrome 92+
        - Firefox 90+
        - Safari 15+
        - Edge 92+
    dependencies:
      - howler.js (included)
    files:
      - client/howler.min.js
      - client/notification.js
      - client/sounds/notification.mp3
      - client/sounds/alert.mp3
    install:
      - kind: manual
        label: Install webchat audio notifications
        instructions: |
          1. Copy files to your webchat directory:
             - client/howler.min.js → /webchat/js/
             - client/notification.js → /webchat/js/
             - client/sounds/ → /webchat/sounds/
          
          2. Add to your webchat HTML before closing </body>:
          
          ```html
          <script src="/js/howler.min.js"></script>
          <script src="/js/notification.js"></script>
          <script>
            const notifier = new WebchatNotifications({
              soundPath: '/sounds/notification'
            });
            notifier.init();
          </script>
          ```
          
          3. Hook into message events:
          
          ```javascript
          socket.on('message', () => {
            if (notifier) notifier.notify();
          });
          ```
          
          4. Test by switching tabs and triggering a message
          
          See docs/integration.md for full guide.
---

# 🔔 Webchat音频通知

Moltbot/Clawdbot Webchat的浏览器音频通知功能：当有新消息到达时，会播放通知音效——但仅当对应的标签页处于后台状态时才会触发。

## 主要特性

- 🔔 **智能通知**：仅当标签页被隐藏时才会播放通知音效。
- 🎚️ **音量控制**：音量可调（0-100%）。
- 🎵 **5个音量等级**：从“微弱”（1级）到“无法忽略”（5级）。
- 📁 **自定义音效**：可以上传自己的音频文件（MP3、WAV、OGG、WebM格式）。
- 🔕 **一键切换**：通过点击即可轻松启用或禁用通知功能。
- 💾 **持久化设置**：用户偏好设置会保存在localStorage中。
- 📱 **移动设备兼容**：在移动设备上仍能正常使用。
- 🚫 **自动播放处理**：遵循浏览器的自动播放策略。
- ⏱️ **冷却时间**：防止通知频繁弹出（每次通知之间有3秒的间隔）。
- 🐞 **调试模式**：可选的日志记录功能。

## 快速入门

### 测试原型

```bash
cd examples
python3 -m http.server 8080
# Open http://localhost:8080/test.html
```

**测试步骤：**
1. 切换到另一个标签页。
2. 点击“触发通知”按钮。
3. 你应该能听到通知音效！

### 基本集成

```javascript
// Initialize
const notifier = new WebchatNotifications({
  soundPath: './sounds',
  soundName: 'level3',  // Medium intensity (default)
  defaultVolume: 0.7
});

await notifier.init();

// Trigger on new message
socket.on('message', () => notifier.notify());

// Use different levels for different events
socket.on('mention', () => {
  notifier.setSound('level5');  // Loudest for mentions
  notifier.notify();
});
```

## API

### 构造函数选项

```javascript
new WebchatNotifications({
  soundPath: './sounds',               // Path to sounds directory
  soundName: 'level3',                 // level1 (whisper) to level5 (very loud)
  defaultVolume: 0.7,                  // 0.0 to 1.0
  cooldownMs: 3000,                    // Min time between alerts
  enableButton: true,                  // Show enable prompt
  debug: false                         // Console logging
});
```

**音量等级：**
- `level1`（9.5KB）：最微弱的音量。
- `level2`（12KB）：较柔和的音量。
- `level3`（13KB）：默认音量。
- `level4`（43KB）：较大的音量，容易引起注意。
- `level5`（63KB）：非常响亮的音量，绝对不会被忽略。

### 方法

- `init()`：初始化（在Howler加载完成后调用）。
- `notify(eventType?)`：触发通知（仅在标签页被隐藏时触发）。
- `test()`：立即播放音效（不考虑标签页的状态）。
- `enabled(bool)`：启用/禁用通知功能。
- `setVolume(0-1)`：设置音量。
- `setSound(level)`：更改音量等级（`level1`至`level5`）。
- `getSettings()`：获取当前设置。

## 浏览器兼容性

| 浏览器 | 版本 | 支持情况 |
|---------|---------|---------|
| Chrome | 92+ | 完全支持 |
| Firefox | 90+ | 完全支持 |
| Safari | 15+ | 完全支持 |
| 移动设备 | 最新版本 | 部分支持 |

**总体情况：** 92%的用户浏览器支持Web Audio API。

## 文件结构

```
webchat-audio-notifications/
├── client/
│   ├── notification.js       # Main class (10KB)
│   ├── howler.min.js         # Audio library (36KB)
│   └── sounds/
│       ├── level1.mp3        # Whisper (9.5KB)
│       ├── level2.mp3        # Soft (12KB)
│       ├── level3.mp3        # Medium (13KB, default)
│       ├── level4.mp3        # Loud (43KB)
│       └── level5.mp3        # Very Loud (63KB)
├── examples/
│   └── test.html            # Standalone test with all levels
├── docs/
│   └── integration.md       # Integration guide
└── README.md                # Full documentation
```

## 集成指南

请参阅`docs/integration.md`，其中包含：
- 逐步集成指南。
- 针对Moltbot的特定集成方法。
- React/Vue框架的示例代码。
- 常见集成模式（如@提及、DND提示、徽章显示等）。
- 测试 checklist。

## 配置示例

### 简单配置

```javascript
const notifier = new WebchatNotifications();
await notifier.init();
notifier.notify();
```

### 高级配置

```javascript
const notifier = new WebchatNotifications({
  soundPath: '/assets/sounds',
  soundName: 'level2',  // Start with soft
  defaultVolume: 0.8,
  cooldownMs: 5000,
  debug: true
});

await notifier.init();

// Regular messages = soft
socket.on('message', () => {
  notifier.setSound('level2');
  notifier.notify();
});

// Mentions = very loud
socket.on('mention', () => {
  notifier.setSound('level5');
  notifier.notify();
});

// DMs = loud
socket.on('dm', () => {
  notifier.setSound('level4');
  notifier.notify();
});
```

### 带有UI控制的配置

```html
<input type="range" min="0" max="100" 
       onchange="notifier.setVolume(this.value / 100)">
<button onclick="notifier.test()">Test 🔊</button>
```

## 故障排除

**为什么没有声音？**
- 确保先点击页面（部分浏览器有自动播放限制）。
- 检查标签页是否真的被隐藏。
- 确认音量设置大于0。
- 查看浏览器控制台是否有错误信息。

**标签页处于活动状态时仍播放声音？**
- 启用调试模式。
- 检查是否有“标签页可见，因此跳过通知”的提示信息。
- 如果问题持续存在，请报告给开发者。

**移动设备无法使用？**
- iOS设备需要用户手动触发播放。
- 考虑使用视觉提示（如闪烁的favicon）作为替代方案。

## 性能

- **文件大小：** 压缩后约为122KB。
- **内存占用：** 播放期间约为2MB。
- **CPU消耗：** 可忽略不计（由浏览器原生处理）。
- **网络请求：** 仅需要一次性下载，之后会缓存。

## 安全性

- ✅ 不会发送任何外部请求。
- ✅ 仅使用localStorage存储数据。
- ✅ 不会进行任何跟踪行为。
- ✅ 不需要任何特殊权限。

## 许可证

MIT许可证。

## 致谢

- **音频库：** [Howler.js](https://howlerjs.com/)（MIT许可证）
- **音效资源：** [Mixkit.co](https://mixkit.co/)（免版税）
- **作者：** @brokemac79
- **适用项目：** [Moltbot/Clawdbot](https://github.com/moltbot/moltbot)社区

## 贡献方式

1. 使用`examples/test.html`进行测试。
2. 启用调试模式。
3. 将遇到的问题连同浏览器控制台的错误信息一起报告给开发者。

## 开发计划

- [ ] 支持WebM格式（文件更小）。
- [ ] 为不同事件（如@提及、私信等）设置不同的音效。
- [ ] 提供视觉提示（如favicon闪烁）。
- [ ] 支持系统通知API。
- [ ] 添加“免打扰”功能。

---

**状态：** ✅ v1.1.0版本已完成，支持5个音量等级。
**已测试的浏览器：** Chrome、Firefox、Safari。
**适用场景：** 生产环境及ClawdHub平台。

## 链接

- 📖 [完整文档](./README.md)
- 🔧 [集成指南](./docs/integration.md)
- 🧪 [测试页面](./examples/test.html)
- 💬 [社区讨论区](https://discord.com/channels/1456350064065904867/1466181146374307881)

---