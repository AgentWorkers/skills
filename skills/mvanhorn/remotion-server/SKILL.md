---
name: remotion-server
description: 使用 Remotion 进行无头视频渲染。该技术适用于任何 Linux 服务器，无需 Mac 或图形用户界面（GUI）。提供用于聊天演示、宣传视频等多种用途的模板。
homepage: https://remotion.dev
user-invocable: true
disable-model-invocation: true
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins: [node, npx]
    os: [linux]
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
创建一个带有动画聊天信息的电话模拟界面。
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

## Linux 所需依赖项

设置脚本会安装以下库：
- libnss3、libatk、libcups2、libgbm 等
- 这些是 Chrome 无头 shell 所必需的

对于 Ubuntu/Debian：
```bash
sudo apt install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgbm1 libpango-1.0-0 libcairo2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2
```

**注意：** Remotion 4.0.418 及更高版本使用自定义的 Chrome 可执行文件，并针对 Linux x64 和 ARM64 架构提供了专有的编解码器，从而提高了兼容性。

## 输出格式

- MP4 (h264) - 默认格式
- WebM (vp8/vp9)
- GIF
- PNG 序列图

```bash
npx remotion render MyComp out/video.webm --codec=vp8
npx remotion render MyComp out/video.gif --codec=gif
```

## 隐私声明

所有模板仅使用模拟数据：
- 模拟的 GPS 坐标（旧金山：37.7749, -122.4194）
- 占位名称和值
- 绝不包含真实用户数据

在发布之前，请务必检查生成的内容。

## 安全性与权限

**此技能的功能：**
- 通过 `scripts/setup.sh` 安装用于无头渲染的 Chromium 依赖项
- 通过 `scripts/create.sh` 在本地创建 Remotion 项目框架
- 使用 `npx remotion render` 将视频文件渲染到本地磁盘

**此技能不执行以下操作：**
- 不需要任何 API 密钥或凭证
- 不会上传视频或数据到外部服务
- 在设置过程中不会访问网络资源（仅限于 npm 包的下载）
- 不会访问个人数据——所有模板都使用占位内容
- 无法被代理程序自动调用（`disable-model-invocation: true`）

**捆绑的脚本：** `scripts/setup.sh`（安装依赖项），`scripts/create.sh`（创建项目框架）

在使用前请先查看这些脚本。设置脚本会在 Linux 上运行 `apt install` 命令来安装浏览器依赖项。