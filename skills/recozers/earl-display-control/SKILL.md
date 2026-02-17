---
name: earl-display-control
description: 管理Earl的电视仪表板（VisuoSpatial Sketchpad）：唤醒显示屏、重启本地服务器、启动信息亭浏览器，并更新Earl的相关信息（情绪状态、家居状况、热门观点、草图绘制内容以及天气信息）。在需要执行以下操作时使用该功能：唤醒Earl、更新电视内容、发布家居相关信息、添加热门观点、刷新仪表板、更新Earl的情绪状态；同时，当显示屏显示“Earl正在睡觉”或“无法同步”时，也需要使用该功能。
  Manage Earl's TV dashboard (VisuoSpatial Sketchpad) — wake the display,
  restart the local server, launch the kiosk browser, and update Earl's mind
  (mood, house stuff, hot takes, sketchpad doodles, weather). Use when asked to
  "wake Earl", "update the TV", "post house stuff", "add a hot take",
  "refresh the dashboard", "update Earl's mood", or when the display shows
  "Earl is sleeping" / "Could not sync".
metadata:
  openclaw:
    emoji: "📺"
    os: [darwin, win32, linux]
    requires:
      bins: [python3]
  homepage: https://github.com/recozers/earl-display-control
---
# Earl 显示控制

这是一项用于管理 VisuoSpatial Sketchpad 的技能——具体来说，是用于控制 Earl 家里客厅电视的显示界面。该技能包括启动 HTTP 服务器、打开信息亭浏览器，以及通过 Python API 更新 `earl_mind.json` 文件。

以下所有文件路径中的 `{baseDir}` 都表示该技能的根目录（即包含 `VisuoSpatialSketchpad/` 的仓库根目录）。

## 快速响应检查清单

1. **唤醒请求**（“Earl 醒来了”、“无法同步”、“Earl 正在睡觉”）
   - 启动本地服务器（参见 [服务器管理](#server-management)）
   - 打开信息亭浏览器（参见 [启动信息亭](#launching-the-kiosk)）
   - 确认服务器状态：查看服务器日志中是否有 `GET /earl_mind.json ... 200` 的响应

2. **内容更新**（情绪、家居信息、热门观点、涂鸦、天气）
   - 使用位于 `{baseDir}/VisuoSpatialSketchpad/earl_api.py` 中的 `EarlMind` API
   - 如果显示内容看起来过时，请在更新后重新启动信息亭

## 服务器管理

从 `VisuoSpatialSketchpad` 目录启动 HTTP 服务器：

```bash
cd {baseDir}/VisuoSpatialSketchpad && python3 -m http.server 8000
```

将服务器进程设置为后台运行，以便命令行提示符可以返回到其他操作。

### 强制关闭卡住的服务器

**macOS / Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Windows (PowerShell):**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

## 启动信息亭

**macOS:**
```bash
open -a "Google Chrome" --args --kiosk http://localhost:8000/sketchpad.html
```
如果 Chrome 浏览器不可用，Safari 也可以使用：
```bash
open -a Safari http://localhost:8000/sketchpad.html
```

**Windows (PowerShell):**
```powershell
Start-Process msedge.exe '--kiosk http://localhost:8000/sketchpad.html --edge-kiosk-type=fullscreen'
```

**Linux:**
```bash
xdg-open http://localhost:8000/sketchpad.html
```
如果需要使用 Chromium 浏览器，可以参考此处：
```bash
chromium-browser --kiosk http://localhost:8000/sketchpad.html
```

每次唤醒 Earl 后，务必重新启动信息亭——浏览器可能会缓存旧页面。

## EarlMind API 参考

所有 API 方法都位于 `{baseDir}/VisuoSpatialSketchpad/earl_api.py` 中。请从 `VisuoSpatialSketchpad` 目录运行该文件：

```python
from earl_api import EarlMind
mind = EarlMind()
```

每个修改数据的方法都会自动保存数据，并更新 `meta.last_updated` 和 `meta.update_count` 的值。

### 方法参考

| 方法 | 功能 | 关键参数 |
|--------|---------|----------------|
| `set_mood(mood, energy, vibe, expression)` | 设置 Earl 的情绪和内心独白 | `mood`: 字符串, `energy`: 0-1 的浮点数, `vibe`: 字符串, `expression`: 字符串 |
| `set_photo(url, caption)` | 设置 Earl 的头像图片 | `url`: 字符串（URL 或本地路径），`caption`: 字符串 |
| `post_house_stuff(title, detail, priority, category, icon)` | 添加家居提醒 | `priority`: “高”/“中”/“低”，`icon`: 表情符号字符串 |
| `resolve_house_stuff(item_id)` | 根据 ID 删除已处理的家居提醒 | `item_id`: 字符串（例如 “hs_a1b2c3”） |
| `clear_house_stuff()` | 清除所有家居提醒信息 | — |
| `update_room(room_id, status, notes, attention)` | 更新房间的状态 | `attention`: 0-1 的浮点数 |
| `add_room(room_id, name, x, y, icon, status, notes, attention)` | 添加新房间 | `x`, `y`: 归一化的位置坐标 |
| `sweep()` | 记录整个房屋的更新情况 | — |
| `hot_take(topic, take, heat, emoji)` | 添加或更新热门观点 | `heat`: 0-1 的浮点数，如果主题已存在则会更新 |
| `drop_take(topic)` | 根据主题删除热门观点 | — |
| `doodle(label, x, y, size, color, note)` | 在画板上绘制表情符号涂鸦 | `x`, `y`: 坐标, `size`: 像素值, `color`: 十六进制颜色代码 |
| `sketch_note(text, x, y, size, color)` | 在画板上添加文本注释 | 与绘制涂鸦的功能相同 |
| `clear_sketchpad()` | 清除画板上的所有内容 | — |
| `learn_pattern(pattern, confidence, observations)` | 记录长期行为模式 | `confidence`: 0-1 的浮点数, `observations`: 整数 |
| `summary()` | 获取易于阅读的状态摘要 | 返回字符串 |
| `snapshot()` | 获取原始的思维状态数据 | 返回字典 |

### 常见用法示例

```python
# Set mood
mind.set_mood("happy", energy=0.9, vibe="Sun's out, vibes are immaculate.")

# Post a house reminder
mind.post_house_stuff("Bins go out tonight", detail="Wednesday again.", priority="high", category="chores", icon="🗑️")

# Drop a hot take
mind.hot_take("Pineapple on pizza", "Controversial but I respect the audacity.", heat=0.6, emoji="🍕")

# Doodle on the sketchpad
mind.doodle("🌧️", x=0.3, y=0.2, size=30, note="Rain starting")

# Log a pattern
mind.learn_pattern("The cat sits by the window at 3pm", confidence=0.7, observations=5)
```

### 天气更新

运行天气相关脚本以获取 Open-Meteo 的实时数据，更新 Earl 的情绪和能量状态，并在画板上显示天气涂鸦：

```bash
cd {baseDir}/VisuoSpatialSketchpad && python3 update_weather_ping.py
```

## earl_mind.json 结构

仪表板的数据来自 `{baseDir}/VisuoSpatialSketchpad/earl_mind.json` 文件。其顶层结构如下：

```
{
  "identity":          { name, role, mood, energy (0-1), current_vibe, avatar_expression, photo, photo_caption }
  "spatial_awareness": { house_name, location: { latitude, longitude, timezone, temperature_unit, wind_speed_unit }, last_sweep, rooms: [...] }
  "house_stuff":       { items: [{ id, title, detail, priority, category, icon }] }
  "earl_unplugged":    [{ id, topic, take, heat (0-1), emoji, date }]
  "sketchpad":         { canvas: [{ id, type ("doodle"|"note"), label, x, y, size, color, note }] }
  "long_term_patterns": [{ pattern, confidence (0-1), observations }]
  "meta":              { schema_version, last_updated (ISO 8601), update_count }
}
```

如果直接编辑 JSON 文件，请务必更新 `meta.last_updated` 和 `meta.update_count` 的值，并使用 `ensure_ascii=False, indent=2` 选项进行编写。

## 故障排除

- **服务器频繁崩溃**：检查是否存在重复的 Python 进程。在 macOS/Linux 上使用 `lsof -i:8000`；在 Windows 上使用 `Get-Process python`。
- **浏览器无法全屏显示**：先结束所有无关的浏览器进程。在 macOS 上使用 `pkill -f "Google Chrome"`；在 Windows 上使用 `taskkill /IM msedge.exe /F`。
- **内容无法更新**：重新启动信息亭以清除缓存，并验证 JSON 文件是否正确保存。
- **天气信息无法显示**：检查 `earl_mind.json` 中的 `spatial_awareness.location.latitude` 和 `longitude` 是否已设置（不应为 0.0）。
- **导入错误**：确保从 `VisuoSpatialSketchpad` 目录运行 Python 脚本，或者将其添加到 `sys.path` 环境变量中。

## 操作流程

每次 Earl 发出“唤醒”信号时，都需按照以下步骤操作：重启服务器 → 启动信息亭 → 应用内容更改 → 如有必要，再次重新启动信息亭。