---
name: home-music
description: **控制全屋音乐场景：结合 Spotify 播放与 Airfoil 扬声器路由**  
提供多种快速预设模式，适用于早晨、聚会或放松时光。
homepage: local
metadata: {"clawdbot":{"emoji":"🏠","os":["darwin"]}}
triggers:
  - music scene
  - morning music
  - party mode
  - chill music
  - house music
  - stop music
---

```
    ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫
    
    🏠  H O M E   M U S I C  🎵
    
    ╔══════════════════════════════════════════╗
    ║   Whole-House Music Scenes               ║
    ║   One command. All speakers. Perfect.    ║
    ╚══════════════════════════════════════════╝
    
    ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫
```

> “为什么要点击17次呢？一个命令就能完成所有事情啊？”——Owen 🐸

---

## 🎯 这个技能有什么作用？

**Home Music** 将 Spotify 和 Airfoil 结合在一起，创造出神奇的音乐体验。只需一个命令，就能让合适的播放列表以完美的音量在相应的扬声器上播放。

**想象一下：**
- 你醒来时：`home-music morning`——浴室里播放轻柔的音乐
- 朋友来访时：`home-music party`——所有扬声器都播放摇滚乐
- 想要放松时：`home-music chill`——整个空间都弥漫着轻松的氛围
- 一天结束的时候：`home-music off`——一片寂静，宁静而祥和。

---

## 📋 所需依赖项

| 依赖项 | 说明 | 链接 |
|------|-----|------|
| 🍏 **macOS** | 该技能使用 AppleScript | — |
| 🟢 **Spotify 桌面应用** | 音乐来源，必须运行中 | [spotify.com](https://spotify.com) |
| 📡 **Airfoil** | 将音频传输到 AirPlay 扬声器 | [rogueamoeba.com](https://rogueamoeba.com/airfoil/) |
| 🎵 **spotify-applescript** | 用于控制 Spotify 的 Clawdbot 技能 | `skills/spotify-applescript/` |

> ⚠️ **重要提示：** 在开始使用任何音乐场景之前，务必确保 Spotify 和 Airfoil 都已运行！

---

## 🎬 音乐场景

### 🌅 早晨
*美好的一天从这里开始*

```bash
home-music morning
```
- **扬声器：** Sonos Move
- **音量：** 40%
- **播放列表：** 早晨播放列表
- **氛围：** ☕ 咖啡与愉悦的心情

---

### 🎉 派对
*庆祝的时刻！*

```bash
home-music party
```
- **扬声器：** 所有扬声器（电脑、MacBook、Sonos Move、客厅电视）
- **音量：** 70%
- **播放列表：** 摇滚派对混音
- **氛围：** 🤘 邻居们可能会讨厌这个设置

---

### 😌 放松
*纯粹的放松*

```bash
home-music chill
```
- **扬声器：** Sonos Move
- **音量：** 30%
- **播放列表：** 轻松休闲音乐
- **氛围：** 🧘 宁静的氛围

---

### 🔇 关闭
*回归寂静*

```bash
home-music off
```
- 暂停 Spotify 播放
- 断开所有扬声器的连接
- **氛围：** 🤫 终于安静下来了

---

### 📊 当前状态
*现在正在播放什么？*

```bash
home-music status
```

显示：
- 当前 Spotify 播放的曲目
- 连接的扬声器

---

## 🔧 安装方法

```bash
# Make the script executable
chmod +x ~/clawd/skills/home-music/home-music.sh

# Symlink for global access
sudo ln -sf ~/clawd/skills/home-music/home-music.sh /usr/local/bin/home-music
```

现在，你可以在终端的任何地方使用 `home-music` 了！🎉

---

## 🎨 自定义播放列表与音乐场景

### 更改播放列表

打开 `home-music.sh` 文件，找到播放列表的配置：

```bash
# === PLAYLIST CONFIGURATION ===
PLAYLIST_MORNING="spotify:playlist:19n65kQ5NEKgkvSAla5IF6"
PLAYLIST_PARTY="spotify:playlist:37i9dQZF1DXaXB8fQg7xif"
PLAYLIST_CHILL="spotify:playlist:37i9dQZF1DWTwnEm1IYyoj"
```

**如何获取播放列表的 URI：**
1. 在 Spotify 中右键点击播放列表
2. 选择“分享” → “复制 Spotify URI”
3. 或者直接复制 URL 并提取其中的 `/playlist/` 部分

### 添加新的音乐场景

在 `main` 块中添加一个新的场景配置：

```bash
# In home-music.sh after the "scene_chill" function:

scene_workout() {
    echo "💪 Starting Workout scene..."
    airfoil_set_source_spotify
    airfoil_connect "Sonos Move"
    sleep 0.5
    airfoil_volume "Sonos Move" 0.8
    "$SPOTIFY_CMD" play "spotify:playlist:YOUR_WORKOUT_PLAYLIST"
    "$SPOTIFY_CMD" volume 100
    echo "✅ Workout: Sonos Move @ 80%, Pump it up!"
}

# And in the case block:
    workout)
        scene_workout
        ;;
```

---

### 可用的扬声器

```bash
ALL_SPEAKERS=("Computer" "Andy's M5 Macbook" "Sonos Move" "Living Room TV")
```

你可以添加任何支持 AirPlay 的扬声器——只要它们能在 Airfoil 中被识别即可。

---

## 🐛 故障排除

### ❌ “扬声器无法连接”

**检查 1：** Airfoil 是否正在运行？
```bash
pgrep -x Airfoil || echo "Airfoil is not running!"
```

**检查 2：** 扬声器是否已连接到网络？
- 打开 Airfoil 应用
- 确认扬声器是否出现在列表中
- 尝试手动连接

**检查 3：** 扬声器的名称是否正确？
- 扬声器的名称区分大小写！
- 打开 Airfoil 并复制正确的名称

---

### ❌ “没有声音”

**检查 1：** Spotify 是否正在播放？**
```bash
~/clawd/skills/spotify-applescript/spotify.sh status
```

**检查 2：** Airfoil 的音频源设置是否正确？
- 打开 Airfoil
- 确认是否选择了 “Spotify” 作为音频源
- 如果没有：点击“Source” → 选择 Spotify

**检查 3：** 扬声器的音量是否调至合适水平？**
```bash
# Manually check volume
osascript -e 'tell application "Airfoil" to get volume of (first speaker whose name is "Sonos Move")'
```

---

### ❌ “Spotify 无法启动”

**Spotify 是否已经打开？**
```bash
pgrep -x Spotify || open -a Spotify
```

**spydra-applescript 是否已安装？**
```bash
ls ~/clawd/skills/spotify-applescript/spotify.sh
```

---

### ❌ “权限被拒绝”

```bash
chmod +x ~/clawd/skills/home-music/home-music.sh
```

---

## 🔊 直接使用 Airfoil 命令

如果你想手动控制 Airfoil，可以尝试以下命令：

```bash
# Connect a speaker
osascript -e 'tell application "Airfoil" to connect to (first speaker whose name is "Sonos Move")'

# Set speaker volume (0.0 - 1.0)
osascript -e 'tell application "Airfoil" to set (volume of (first speaker whose name is "Sonos Move")) to 0.5'

# Disconnect a speaker
osascript -e 'tell application "Airfoil" to disconnect from (first speaker whose name is "Sonos Move")'

# List connected speakers
osascript -e 'tell application "Airfoil" to get name of every speaker whose connected is true'

# Set audio source
osascript -e 'tell application "Airfoil"
    set theSource to (first application source whose name contains "Spotify")
    set current audio source to theSource
end tell'
```

---

## 📁 相关文件

```
skills/home-music/
├── SKILL.md        # This documentation
└── home-music.sh   # The main script
```

---

## 💡 专业提示

1. **设置别名** 以更快地使用该技能：
   ```bash
   alias mm="home-music morning"
   alias mp="home-music party"
   alias mc="home-music chill"
   alias mo="home-music off"
   ```

2. **结合 Clawdbot 使用：**
   > “嘿，开启派对模式”
   > “播放一些轻松的音乐”
   > “停止音乐”

3. **组合多个场景：** 例如创建一个名为 “dinner”的场景，设置播放 25% 音量的爵士乐——非常适合招待客人！

---

## 🐸 致谢

```
╭─────────────────────────────────────────────╮
│                                             │
│   Crafted with 💚 by Owen the Frog 🐸      │
│                                             │
│   "Ribbit. Music makes everything better."  │
│                                             │
╰─────────────────────────────────────────────╯
```

**作者：** Andy Steinberger（在 Clawdbot Owen 的帮助下完成）  
**版本：** 1.0.0  
**许可协议：** MIT 许可协议  
**灵感来源：** 长满睡莲的池塘 🪷

---

*这个技能是否让你的生活变得更美好了？Owen 非常感谢你的支持！🪰*