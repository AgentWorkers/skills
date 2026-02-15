---
name: airfoil
description: 通过 Airfoil 在命令行控制 AirPlay 扬声器：使用简单的 CLI 命令来连接/断开设备、调节音量以及管理多房间音频播放。
metadata: {"clawdbot":{"emoji":"🔊","os":["darwin"],"requires":{"bins":["osascript"]}}}
---

# 🔊 Airfoil 技能

```
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🎵  A I R F O I L   S P E A K E R   C O N T R O L  🎵  ║
    ║                                                           ║
    ║        Stream audio to any AirPlay speaker                ║
    ║              from your Mac via CLI                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
```

> “为什么要用鼠标去操作电脑，直接用语音命令不就好了吗？” 🐸

---

## 📖 这个技能的作用是什么？

**Airfoil 技能** 允许你直接通过终端或 Clawd 来完全控制你的 AirPlay 扬声器——无需使用鼠标。

**功能包括：**
- 📡 **列表** — 显示所有可用的扬声器
- 🔗 **连接** — 连接到某个扬声器
- 🔌 **断开** — 从某个扬声器断开连接
- 🔊 **音量** — 调节音量（0-100%）
- 📊 **状态** — 显示已连接的扬声器及其音量水平

---

## ⚙️ 使用要求

| 需求 | 详情 |
|------|---------|
| **操作系统** | macOS（需要使用 AppleScript） |
| **应用程序** | [Airfoil](https://rogueamoeba.com/airfoil/mac/)（由 Rogue Amoeba 开发） |
| **价格** | 35 美元（提供免费试用） |

### 安装步骤

1. **安装 Airfoil：**
   ```bash
   # Via Homebrew
   brew install --cask airfoil
   
   # Or download from rogueamoeba.com/airfoil/mac/
   ```

2. **启动 Airfoil** 并授予其访问权限（系统设置 → 隐私与安全 → 访问辅助功能）

3. **技能即可使用！** 🚀

---

## 🛠️ 命令说明

### `list` — 显示所有扬声器

```bash
./airfoil.sh list
```

**输出：**
```
Computer, Andy's M5 Macbook, Sonos Move, Living Room TV
```

---

### `connect <扬声器名称>` — 连接到指定的扬声器

```bash
./airfoil.sh connect "Sonos Move"
```

**输出：**
```
Connected: Sonos Move
```

> 注意：扬声器名称必须完全匹配（区分大小写！）

---

### `disconnect <扬声器名称>` — 断开与指定扬声器的连接

```bash
./airfoil.sh disconnect "Sonos Move"
```

**输出：**
```
Disconnected: Sonos Move
```

---

### `volume <扬声器名称> <0-100>` — 设置扬声器音量

```bash
# Set to 40%
./airfoil.sh volume "Sonos Move" 40

# Set to maximum
./airfoil.sh volume "Living Room TV" 100

# Quiet mode for night time
./airfoil.sh volume "Sonos Move" 15
```

**输出：**
```
Volume Sonos Move: 40%
```

---

### `status` — 显示已连接的扬声器

```bash
./airfoil.sh status
```

**输出：**
```
Sonos Move: 40%
Living Room TV: 65%
```

如果没有任何扬声器连接：
```
No speakers connected
```

---

## 🎯 使用示例

### 🏠 “在客厅播放音乐”
```bash
./airfoil.sh connect "Sonos Move"
./airfoil.sh volume "Sonos Move" 50
# → Now fire up Spotify/Apple Music and enjoy!
```

### 🎬 “设置电影观看模式”
```bash
./airfoil.sh connect "Living Room TV"
./airfoil.sh volume "Living Room TV" 70
./airfoil.sh disconnect "Sonos Move"  # If still connected
```

### 🌙 “全部关闭”
```bash
for speaker in "Sonos Move" "Living Room TV"; do
    ./airfoil.sh disconnect "$speaker" 2>/dev/null
done
echo "All speakers disconnected 🌙"
```

---

## 🔧 故障排除

### ❌ “找不到扬声器”

**问题：** “执行错误：Airfoil 无法找到扬声器……”

**解决方法：**
1. 确认拼写正确：`./airfoil.sh list`
2. 扬声器名称区分大小写（例如：“sonos move” 和 “Sonos Move” 是不同的）
3. 确保扬声器处于同一网络中，并且已开启且可被访问

---

### ❌ “Airfoil 无法启动 / 没有权限”

**问题：** AppleScript 无法控制 Airfoil

**解决方法：**
1. 进入系统设置 → 隐私与安全 → 访问辅助功能
2. 确保终端（或 iTerm）已添加到允许使用的应用程序列表中
3. 确保 Airfoil 已添加到允许使用的应用程序列表中
4. 有时需要重启 macOS （有时这会解决问题 🙄）

---

### ❌ “音量调节无效”

**问题：** 调节音量的命令没有效果

**解决方法：**
1. 确保扬声器已连接后再尝试调节音量
2. 先使用 `connect` 命令连接扬声器，再使用 `volume` 命令调节音量
3. 有些扬声器可能有硬件上的音量限制

---

### ❌ “Airfoil 未安装”

**问题：** “执行错误：应用程序未运行”

**解决方法：**
```bash
# Start Airfoil
open -a Airfoil

# Or install it
brew install --cask airfoil
```

---

### ❌ “出现 ‘bc: command not found’ 错误”

**问题：** 音量调节命令无法执行

**解决方法：**
```bash
# Install bc (should be standard on macOS)
brew install bc
```

---

## 📋 已测试的扬声器

以下扬声器已通过测试：

| 扬声器 | 类型 | 备注 |
|---------|------|-------|
| `Computer` | 本地扬声器 | 始终可用 |
| `Andy’s M5 Macbook` | Mac 电脑 | 当连接到网络时可用 |
| `Sonos Move` | Sonos 扬声器 | 支持蓝牙或 WiFi 连接 |
| `Living Room TV` | Apple TV | 可通过 AirPlay 连接 |

> 使用 `./airfoil.sh list` 命令来查看你自己的扬声器列表！

---

## 🔗 与 Clawd 的集成

此技能可与 Clawd 完美配合使用！示例如下：

```
"Hey Clawd, connect the Sonos Move"
→ ./airfoil.sh connect "Sonos Move"

"Turn the music down"
→ ./airfoil.sh volume "Sonos Move" 30

"Which speakers are on?"
→ ./airfoil.sh status
```

---

## 📜 更新日志

| 版本 | 更新日期 | 更新内容 |
|---------|------|---------|
| 1.0.0 | 2025-01-25 | 首次发布 |
| 1.1.0 | 2025-06-10 | 文档更新 |
| 1.2.0 | 2025-06-26 | 翻译为中文，并适配 ClawdHub 使用 |

---

## 🐸 致谢

```
  @..@
 (----)
( >__< )   "This skill was crafted with love
 ^^  ^^     by a frog and his human!"
```

**作者：** Andy Steinberger（在 Clawdbot Owen 的帮助下完成）  
**技术支持：** [Airfoil](https://rogueamoeba.com/airfoil/mac/)（由 Rogue Amoeba 开发）  
**所属项目：** [Clawdbot](https://clawdhub.com) 技能库

---

<div align="center">

**专为 Clawdbot 社区制作**

*呱呱！* 🐸

</div>