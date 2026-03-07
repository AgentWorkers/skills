---
name: remotion-server
version: "1.1.0"
description: 使用 Remotion v5 在任何 Linux 服务器上进行无头视频渲染——无需 Mac 或图形用户界面（GUI）。提供用于聊天演示、宣传视频等场景的模板。该技术基于 Chrome Headless Shell，实现快速且无依赖的渲染过程。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-remotion-server
homepage: https://remotion.dev
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - node
        - npm
    tags:
      - video
      - remotion
      - rendering
      - react
      - headless
---
# Remotion Server

使用 Remotion，您可以在任何 Linux 服务器上无头渲染视频，无需 Mac 或图形用户界面。

## 设置（一次性操作）

安装浏览器所需的依赖项：
```bash
bash {baseDir}/scripts/setup.sh
```

## 快速入门

### 创建项目：
```bash
bash {baseDir}/scripts/create.sh my-video
cd my-video
```

### 渲染视频：
```bash
npx remotion render MyComp out/video.mp4
```

## 模板

### 聊天演示（类似 Telegram 的风格）
创建一个带有动画聊天消息的电话模拟界面。
```bash
bash {baseDir}/scripts/create.sh my-promo --template chat
```

编辑 `src/messages.json` 文件：
```json
[
  {"text": "What's the weather?", "isUser": true},
  {"text": "☀️ 72°F and sunny!", "isUser": false}
]
```

### 标题卡
简单的动画标题/介绍卡片。
```bash
bash {baseDir}/scripts/create.sh my-intro --template title
```

## 聊天使用示例

- “制作一个关于 [主题] 的聊天视频”
- “为 [功能] 创建一个宣传视频”
- “渲染一个显示 [文本] 的标题卡”

## Linux 依赖项

设置脚本会安装以下软件：
- libnss3、libatk、libcups2、libgbm 等
- 这些是 Chrome 无头 shell 所必需的

对于 Ubuntu/Debian 系统：
```bash
sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgbm1 libpango-1.0-0 libcairo2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2
```

## 输出格式

- MP4（h264） - 默认格式
- WebM（vp8/vp9）
- GIF
- PNG 序列图像

```bash
npx remotion render MyComp out/video.webm --codec=vp8
npx remotion render MyComp out/video.gif --codec=gif
```

## 隐私声明

⚠️ **所有模板仅使用虚拟演示数据！**
- 虚拟 GPS 坐标（旧金山：37.7749, -122.4194）
- 占位名称和值
- 绝不包含真实用户数据

在发布之前，请务必查看生成的内容。