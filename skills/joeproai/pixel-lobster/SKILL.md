---
name: pixel-lobster
description: "这是一个像素艺术风格的桌面“龙虾”，它能够根据 OpenClaw 的文本转语音（TTS）功能进行同步发音。适用场景包括：  
1. 用户需要为其 AI 代理创建一个可视化的头像；  
2. 用户希望在使用 AI 代理时看到动画效果；  
3. 用户希望设置或配置这个像素艺术“龙虾”应用程序。  
本文档将指导用户完成该 Electron 应用程序的安装、配置及启动过程。"
tags: ["avatar", "tts", "desktop", "overlay", "lip-sync", "electron", "xtts", "animation"]
---
# Pixel Lobster

这是一个透明的桌面插件，它展示了一个像素艺术的龙虾形象。当你的 OpenClaw 代理发出语音时，这个龙虾形象会随之动画化。该效果依赖于本地 TTS 服务器提供的音频数据——只有在进行人工智能语音播放时，龙虾的嘴巴才会动起来，而在播放音乐或系统音频时嘴巴是静止的。

这个应用程序已完全包含在该技能包中，无需从外部仓库克隆任何代码。

## 系统要求

- 安装了 Node.js 18 及更高版本，并且能够使用 `npx` 命令。
- 需要有一个正在运行的 TTS 服务器，该服务器提供 `GET /audio/envelope` 端点（推荐使用基于 XTTS 的服务器，端口为 8787；或者使用 OpenClaw 提供的 TTS 代理来调用其他兼容 OpenAI 的 TTS 服务）。
- 支持 Windows 或 Linux 桌面系统（macOS 不受支持）。

## 安装

该应用程序位于 `<skill_dir>/app/` 目录下。只需执行一次以下命令来安装所有依赖项：

```bash
cd <skill_dir>/app
npm install
```

## 配置

在启动应用程序之前，请编辑 `<skill_dir>/app/config.json` 文件。主要配置参数如下：

| 参数 | 默认值 | 说明 |
|-------|---------|--------|
| `audioMode` | `"tts"` | `"tts"` 表示仅对 TTS 语音做出响应；`"system"` 表示捕获所有音频输出 |
| `ttsUrl` | `"http://127.0.0.1:8787"` | TTS 服务器的基地址 |
| `monitor` | `"primary"` | 显示位置（`"primary"`、`"secondary"`、`"left"`、`"right"` 或其他索引值 |
| `lobsterScale` | `4` | 鲸鱼图像的缩放比例（4 表示图像高度为 480 像素） |
| `clickThrough` | `false` | 默认设置为关闭点击穿透功能（即龙虾图像不会遮挡鼠标点击） |
| `swimEnabled` | `true` | 启用龙虾的游动动画 |

## 启动应用程序

```bash
cd <skill_dir>/app
npx electron .
```

或者使用随附的帮助脚本（该脚本会自动执行首次安装时的 `npm install` 操作）：

```bash
bash <skill_dir>/scripts/launch.sh
```

## 键盘快捷键

| 键 | 功能 |
|------|------|
| F8 | 将窗口切换到下一个显示屏幕（在所有显示器之间循环切换） |
| F9 | 切换点击穿透模式 |
| F12 | 打开/关闭开发者工具 |

## 与 OpenClaw 的集成

在使用 OpenClaw 和本地 XTTS 服务器时，将 `audioMode` 设置为 `"tts"`，并将 `ttsUrl` 指向你的 XTTS 服务器的地址。在语音播放期间，龙虾图像会以 45 毫秒的间隔查询音频数据；在空闲时，查询间隔为 500 毫秒。这一过程对 CPU 资源的消耗非常小。

如果你使用的是 OpenClaw TTS 代理（端口为 8788），请将 `ttsUrl` 设置为代理的端口（8787），而不是直接指向 XTTS 服务器的端口——因为音频数据是从 TTS 服务器获取的，而非代理。

## 嘴部动画的同步问题

如果龙虾嘴巴的动画与音频不同步（比如嘴巴动作提前或滞后）：
- 如果嘴巴动作过早：增加 `ttsPlayStartOffsetMs` 的值（默认为 1100 毫秒）。
- 如果嘴巴动作滞后：减小 `ttsPlayStartOffsetMs` 的值。

这些参数是根据 Windows 上的 PowerShell MediaPlayer 进行优化的。对于其他播放方式，可能需要根据实际情况进行调整。

## 嘴部动画的形状

有六种不同的嘴部表情可以模拟自然的语音效果：
- **A**：张大嘴巴发 “ah” 声音 |
- **B**：咧嘴大笑发 “ee” 声音 |
- **C**：圆睁嘴巴发 “oh” 声音 |
- **D**：微微撅嘴发 “oo” 声音 |
- **E**：半张开嘴巴发 “eh” 声音 |
- **F**：露出牙齿发 “ff” 声音 |
- **X**：表示静音或暂停。

通过使用这些不同的嘴部形状，可以使得动画更加自然，避免显得机械或重复。