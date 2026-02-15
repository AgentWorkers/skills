---
name: philips-hue-thinking
description: 使用飞利浦 Hue 灯作为视觉 AI 活动指示器：思考时灯光会闪烁红色，完成任务后变为绿色。
homepage: https://github.com/yourusername/philips-hue-thinking
metadata: {"clawdbot":{"emoji":"🚦","requires":{"bins":["hue"]},"install":[{"id":"manual","kind":"manual","label":"Copy hue script to PATH"}]}}
---

# Philips Hue 智能指示灯

**视觉 AI 活动指示器** — 通过 Philips Hue 智能灯泡将您的 AI 助手的工作状态与您的物理环境连接起来。

![演示](https://img.shields.io/badge/status-active-green)

## 功能介绍

将 Philips Hue 灯泡变成一个 **AI 活动指示器**：

| 灯的状态 | 含义 |
|-------------|---------|
| 🟢 **绿色** | 准备就绪 / 已完成 / 闲置 |
| 🔴 **闪烁的红色** | AI 正在思考、分析或规划 |
| 🔴 **稳定的红色** | AI 正在积极执行任务 |

## 为什么使用这个工具？

- **环境感知** — 无需查看屏幕即可了解 AI 的工作状态 |
- **保护工作流程** — 视觉指示器可在您专注工作时防止干扰 |
- **完成任务后的反馈** — 绿色灯光表示“已准备好执行下一个任务” |
- **增强交互体验** — “我的 AI 在我的家中有了实体存在感”

## 快速入门

### 1. 设置 Hue Bridge

```bash
# Find your bridge IP (check router or Hue app), then run:
hue setup <bridge-ip>

# Example:
hue setup 192.168.1.100
```

### 2. 找到您的灯泡

```bash
hue lights

# Output:
#   2: Bed room 1 💡 ON
#   3: Bedroom 2 ⚫ OFF
#   5: Front door 💡 ON  ← Use this one
```

### 3. 开始使用

```bash
# AI starts thinking
hue thinking 5

# AI is done
hue done 5
```

## 安装

### 方法 1：将脚本添加到系统路径

```bash
# Clone or download
git clone https://github.com/yourusername/philips-hue-thinking.git

# Add to PATH
cp philips-hue-thinking/hue /usr/local/bin/
chmod +x /usr/local/bin/hue
```

### 方法 2：直接使用脚本

```bash
# Add to your shell profile (.zshrc or .bashrc)
export PATH="$PATH:/path/to/philips-hue-thinking"

# Then reload
source ~/.zshrc
```

## 命令

### 核心命令

```bash
# Setup (press bridge button first!)
hue setup <bridge-ip>

# List all lights
hue lights

# Thinking mode (pulsing red)
hue thinking <light-id>

# Done (solid green)
hue done <light-id>

# Set any color
hue set <light-id> <color>
```

### 可用的颜色

```bash
hue set 5 red
hue set 5 green
hue set 5 blue
hue set 5 yellow
hue set 5 purple
hue set 5 orange
```

### 实用命令

```bash
# Turn off
hue off 5

# Pulse continuously
hue pulse 5 --color red
```

## 工作流程集成

### 与 AI 助手结合使用

**规划模式：**
```
User: "Planning mode — I want to build a website"
AI:  [runs 'hue thinking 5'] 🔴 Pulsing...
     "Here are my questions..."
User: [answers]
AI:  [runs 'hue done 5'] ✅ Green
     "Starting build now..."
     [runs 'hue thinking 5'] 🔴 Solid red while building
AI:  [runs 'hue done 5'] ✅ Green
     "Done!"
```

### Shell 别名

将以下内容添加到 `~/.zshrc` 文件中：

```bash
# Quick aliases
alias think='hue thinking 5'
alias done='hue done 5'
```

然后只需输入：
```bash
think  # Light pulses red
done   # Light turns green
```

## 技术细节

### 工作原理

1. **通过 Hue Bridge API 进行通信** — 使用本地 HTTP API 进行数据交换 |
2. **使用 CIE 色彩空间** — 确保颜色显示的准确性 |
3. **通过 Bash 循环控制灯光亮度** — 实现灯光的闪烁效果 |
4. **无状态设计** — 配置信息存储在 `~/.config/philips-hue/` 文件中 |

### CIE 色彩空间

| 颜色 | X | Y |
|-------|---|---|
| 红色 | 0.675 | 0.322 |
| 绿色 | 0.214 | 0.709 |
| 蓝色 | 0.167 | 0.040 |
| 黄色 | 0.492 | 0.476 |
| 紫色 | 0.265 | 0.100 |
| 橙色 | 0.600 | 0.380 |

### 闪烁效果

```bash
# Brightness oscillation
254 (bright) → 50 (dim) → 254

# Timing
~2 second cycle
Background process keeps pulsing
```

## 配置

配置信息存储在：`~/.config/philips-hue/config.json` 文件中

```json
{
  "bridge_ip": "192.168.1.100",
  "username": "your-api-key"
}
```

## 系统要求

- Philips Hue Bridge（版本 2） |
- Philips Hue 彩色灯泡 |
- 安装了 `curl` 的 macOS/Linux 系统 |
- Bash 4.0 或更高版本

## 故障排除

### “链接按钮未按下”

请按下 Hue Bridge 上的物理按钮，然后在 30 秒内完成设置。

### 灯泡无响应

```bash
# Check connection
hue lights

# Verify config
cat ~/.config/philips-hue/config.json
```

### 闪烁不停

```bash
# Kill background process
pkill -f "hue-pulse-loop"

# Reset light
hue done 5
```

## 未来改进方向

- [ ] 根据 AI 会话状态自动触发指示灯 |
- [ ] 为不同任务类型使用多个灯泡 |
- [ ] 实现“心跳模式”（每 30 分钟闪烁一次） |
- [ ] 显示错误状态（灯光闪烁紫色） |
- [ ] 成功完成时显示庆祝效果（灯光变彩）

## 许可证

MIT 许可证 — 详见 LICENSE 文件

## 致谢

由 Jesse 和 Kate（Clawdbot）开发  
灵感来源于对 AI 实体化存在的需求

---

**有问题吗？** 可在 Twitter 上向 @jesse 提问或发送私信。