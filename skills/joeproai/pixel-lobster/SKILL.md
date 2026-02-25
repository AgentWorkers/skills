---
name: pixel-lobster
description: "这款像素艺术风格的桌面“龙虾”角色能够根据 OpenClaw 的文本转语音（TTS）功能进行同步发音。适用场景包括：  
(1) 用户需要为他们的 AI 代理创建一个可视化的化身；  
(2) 用户希望在使用 AI 代理时看到一个会随着代理说话而动画化的桌面元素；  
(3) 用户需要设置或配置这款像素龙虾角色的功能。  
该指南会指导用户从 GitHub 下载并安装基于 Electron 的应用程序，配置音频播放模式，并将其连接到用户的文本转语音服务器。"
tags: ["avatar", "tts", "desktop", "overlay", "lip-sync", "electron", "xtts", "animation"]
---
# Pixel Lobster

这是一个透明的桌面插件，上面显示着一个像素艺术的龙虾图案。当你的 OpenClaw 代理发出语音时，这个龙虾会开始动画播放。该插件的效果依赖于来自本地 TTS 服务器的音频数据——只有在进行人工智能语音播放时，龙虾的嘴巴才会动起来，音乐或系统音频则不会影响动画效果。

## 系统要求

- 安装了 Node.js 18 及更高版本，并且能够使用 `npx` 命令。
- 运行中的 TTS 服务器，且提供 `GET /audio/envelope` 接口（建议使用基于 OpenAI 的 XTTS 服务，端口为 8787；或者通过 OpenClaw 的 TTS 代理来使用其他兼容的 TTS 服务）。
- 支持 Windows 或 Linux 操作系统（macOS 不受支持）。

## 安装方法

该插件是一个独立的 Electron 项目。你可以从 GitHub 上克隆该项目，然后安装所需的依赖项：

```bash
git clone https://github.com/JoeProAI/pixel-lobster.git
cd pixel-lobster
npm install
```

## 配置方法

将配置文件（位于 `assets/config.json` 中）复制到克隆后的项目目录中，根据需要进行修改：

```bash
cp <skill_dir>/assets/config.json pixel-lobster/config.json
```

主要配置参数如下：

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `audioMode` | `"tts"` | `"tts"`：仅对 TTS 语音做出响应；`"system"`：捕获所有音频输出 |
| `ttsUrl` | `"http://127.0.0.1:8787"` | TTS 服务器的基地址 |
| `monitor` | `"primary"` | `"primary"`、`"secondary"`、`"left"`、`"right"`：显示位置 |
| `lobsterScale` | `4` | 鲎鱼的尺寸比例（4 表示龙虾高度为 480 像素） |
| `clickThrough` | `false` | 默认关闭点击穿透功能（防止龙虾遮挡点击操作） |
| `swimEnabled` | `true` | 启用龙虾的游动动画 |

## 启动方法

```bash
cd pixel-lobster
npm start
```

或者使用随附的帮助脚本进行启动：

```bash
bash <skill_dir>/scripts/launch.sh /path/to/pixel-lobster
```

## 键盘快捷键

| 键 | 功能 |
|------|--------|
| F9 | 切换点击穿透模式 |
| F12 | 打开开发者工具 |

## 与 OpenClaw 的集成方法

在使用 OpenClaw 和本地 XTTS 服务器时，将 `audioMode` 设置为 `"tts"`，并将 `ttsUrl` 指向你的 XTTS 服务器的地址。在语音播放期间，该插件会以 45 毫秒的间隔向 TTS 服务器发送请求；在空闲状态下，请求间隔为 500 毫秒。这种设计几乎不会对 CPU 资源造成影响。

如果你使用的是 OpenClaw 的 TTS 代理（端口为 8788），请将 `ttsUrl` 设置为 8787（即直接指向 TTS 服务器的地址），因为音频数据的请求端点位于 TTS 服务器本身，而非代理服务器。

## 嘴部动画的同步问题

如果龙虾的嘴巴动作与音频不同步（提前或延迟）：

- 如果嘴巴动作过早：增加 `ttsPlayStartOffsetMs` 的值（默认为 1100 毫秒）。
- 如果嘴巴动作过晚：减少 `ttsPlayStartOffsetMs` 的值。

默认设置适用于 Windows 系统上的 PowerShell MediaPlayer；其他播放引擎可能需要相应调整。

## 嘴部动画的形状

共有六种不同的嘴部表情，用于模拟自然的语音效果：

- **A**：张大嘴巴发 “ah” 声音 |
- **B**：咧嘴大笑发 “ee” 声音 |
- **C**：圆睁嘴巴发 “oh” 声音 |
- **D**：微微撅嘴发 “oo” 声音 |
- **E**：半张开嘴巴发 “eh” 声音 |
- **F**：露出牙齿发 “ff” 声音 |
- **X**：表示静音或暂停。

通过使用不同的嘴部形状，可以避免动画显得机械或重复。插件采用了物理模拟算法来确保动画更加自然。