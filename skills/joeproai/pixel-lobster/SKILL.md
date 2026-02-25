---
name: pixel-lobster
description: "这款像素艺术风格的桌面“龙虾”角色能够根据 OpenClaw 的文本转语音（TTS）服务进行同步发音。适用场景包括：  
(1) 用户需要为他们的 AI 代理创建一个可视化的化身；  
(2) 用户希望在使用 AI 代理时看到动态动画效果；  
(3) 用户需要设置或配置这款像素龙虾角色的功能。  
该指南会指导用户从 GitHub 下载并安装基于 Electron 的应用程序，配置音频播放方式，并将其连接到用户的文本转语音服务器。"
tags: ["avatar", "tts", "desktop", "overlay", "lip-sync", "electron", "xtts", "animation"]
---
# Pixel Lobster

这是一个透明的桌面插件，它展示了一个像素艺术的龙虾形象。当你的 OpenClaw 代理发出语音时，这个龙虾形象会随之动画化。该插件的动画效果依赖于来自本地 TTS 服务器的音频数据——只有在进行人工智能语音播放时，龙虾的嘴巴才会动起来，而音乐或系统音频则不会影响龙虾的动画。

## 系统要求

- 安装了 Node.js 18 及更高版本，并且能够使用 `npx` 命令。
- 运行中的 TTS 服务器，能够提供 `GET /audio/envelope` 的接口（推荐使用基于 OpenAI 技术的 XTTS 服务器，端口为 8787；或者使用 OpenClaw 提供的 TTS 代理）。
- 支持 Windows 或 Linux 桌面系统（macOS 不受支持）。

## 安装方法

该插件是一个独立的 Electron 项目。你可以从 GitHub 上克隆该项目并安装所需的依赖库：

```bash
git clone https://github.com/JoeProAI/pixel-lobster.git
cd pixel-lobster
npm install
```

## 配置方法

将配置文件（位于 `assets/config.json` 中）复制到克隆后的项目目录中，然后根据需要进行修改：

```bash
cp <skill_dir>/assets/config.json pixel-lobster/config.json
```

主要配置参数如下：

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `audioMode` | `"tts"` | `"tts"`：仅对 TTS 语音做出反应；`"system"`：捕获所有音频输出 |
| `ttsUrl` | `"http://127.0.0.1:8787"` | TTS 服务器的基地址 |
| `monitor` | `"primary"` | 显示位置：`"primary"`、`"secondary"`、`"left"`、`"right"` |
| `lobsterScale` | `4` | 鲸鱼图像的缩放比例（4 表示图像高度为 480 像素） |
| `clickThrough` | `false` | 默认关闭点击穿透功能（防止龙虾图像遮挡点击操作） |
| `swimEnabled` | `true` | 启用龙虾的游动动画 |

## 启动方法

```bash
cd pixel-lobster
npm start
```

或者使用提供的辅助脚本来启动插件：

```bash
bash <skill_dir>/scripts/launch.sh /path/to/pixel-lobster
```

## 键盘快捷键

| 键 | 功能 |
|------|--------|
| F8 | 将窗口切换到下一个显示屏幕（在所有屏幕间循环切换） |
| F9 | 切换点击穿透模式（允许或禁止点击穿透） |
| F12 | 打开开发者工具 |

## 与 OpenClaw 的集成方法

在使用 OpenClaw 和本地 XTTS 服务器时，将 `audioMode` 设置为 `"tts"`，并将 `ttsUrl` 指向你的 XTTS 服务器的地址。在语音播放期间，该插件会以 45 毫秒的间隔向 TTS 服务器发送请求；在静止状态下，则以 500 毫秒的间隔发送请求。这种集成方式对 CPU 资源的影响很小。

如果你使用的是 OpenClaw 提供的 TTS 代理（端口为 8788），请将 `ttsUrl` 设置为 8787（即直接指向 XTTS 服务器的地址），因为音频数据是由 TTS 服务器提供的，而非代理服务器。

## 关于嘴唇同步的注意事项

如果龙虾嘴巴的动作与音频不同步（提前或延迟）：

- 如果嘴巴动作过早：增加 `ttsPlayStartOffsetMs` 的值（默认为 1100 毫秒）。
- 如果嘴巴动作过晚：减少 `ttsPlayStartOffsetMs` 的值。

这些配置参数是基于 Windows 上的 PowerShell MediaPlayer 进行优化的。其他播放方式可能需要进行相应的调整。

## 鲸鱼嘴巴的动画效果

有六种不同的嘴型可以模拟自然的发音效果：

- **A**：张大嘴巴发 “ah” 音 |
- **B**：咧嘴大笑发 “ee” 音 |
- **C**：圆睁嘴巴发 “oh” 音 |
- **D**：微微撅嘴发 “oo” 音 |
- **E**：半张开嘴巴发 “eh” 音 |
- **F**：露出牙齿发 “ff” 音 |
- **X**：表示静音或暂停。

通过使用不同的嘴型，可以使得动画更加自然。同时，通过模拟物理效果和变化多样的动画动作，可以避免动画显得过于机械或重复。