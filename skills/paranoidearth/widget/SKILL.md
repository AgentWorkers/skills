---
name: widget
description: 在 macOS 上创建、更新、隐藏、显示、列出以及删除 Übersicht 桌面小部件。每当用户需要桌面小部件或桌面工具时，都可以使用此技能。
argument-hint: "[operation, e.g. add a clock / hide the pomodoro / list all widgets]"
allowed-tools: Bash(bash *), Bash(cp *), Bash(mv *), Bash(rm *), Bash(ls *), Write, Edit
---
# WidgetDesk 技能

## 环境要求
- Widget 目录：`~/Library/Application Support/Übersicht/widgets/`
- 模板目录：安装后位于 `~/.claude/skills/widget/templates/`；或位于此仓库内的 `/.claude/skills/widget/templates/`
- 主机要求：Übersicht 已安装，并可在 `/Applications/Übersicht.app` 或 `/Applications/Uebersicht.app` 中找到

## 第一步
- 在克隆的 WidgetDesk 仓库中工作时，首先运行 `bash scripts/setup.sh`
- `scripts/setup.sh` 是默认的入口脚本：它会安装缺失的主机依赖项，启动 Übersicht，准备 Widget 目录，安装技能，并验证结果
- 仅在用户明确要求进行干运行检查或诊断安装问题时，使用 `bash scripts/setup.sh --check`
- 仅使用 `bash ~/.claude/skills/widget/scripts/doctor.sh` 进行快速的安装后健康检查
- 安装完成后，可以在 `~/.claude/skills/widget/` 下找到已安装的技能文件

## 参考文件
- 可重用的实现模式：[patterns.md](patterns.md)
- 主机管理脚本：`scripts/` 用于设置、启动 Übersicht、检查环境、安装 Widget 以及列出 Widget

---

## 硬性约束

### 1. 布局
- 所有 Widget 的默认位置设置为 `position: fixed`
- 任何底部对齐的 Widget 必须满足 `bottom >= 90px`
- 默认的边缘间距为 `40px`
- 默认宽度应在 `140px` 到 `360px` 之间
- 默认高度应在 `48px` 到 `220px` 之间
- 仅在用户明确要求使用较大尺寸的 Widget 时才超出这些限制

### 2. 交互
- 仅用于显示的 Widget 的默认交互设置为 `pointer-events: none`
- 仅在 Widget 真正需要点击、拖动或输入文本时才启用交互
- 交互式控件必须易于点击
- 默认情况下避免复杂的多步骤桌面交互

### 3. 刷新
- 基于命令的 Widget 通常应在 `1000ms` 到 `600000ms` 之间刷新
- 对于时钟或时间敏感的 UI，刷新间隔可小于 `1000ms`
- 纯前端 Widget 应将 `refreshFrequency` 设置为 `false`
- 避免频繁的网络请求

### 4. 实现
- 使用小写拼写（kebab-case）的文件名
- 在创建新结构之前，优先使用现有的模板和 `patterns.md`
- 优先使用 macOS 的内置功能，而不是额外的依赖项
- 不要硬编码敏感信息
- 默认情况下，Widget 应为单文件结构，除非用户明确要求更复杂的实现

### 5. 视觉风格
- 保持风格的一致性、简洁性，并符合 macOS 的设计风格
- 默认使用深色半透明卡片效果
- 推荐的角半径为 `14px` 到 `20px`
- 优先使用 `SF Pro Display` 和 `SF Mono` 字体
- 动画效果应简洁、轻量且具有明确的目的性
- 不要为每个 Widget 都设计全新的视觉风格

---

## 操作说明

```bash
# First-time setup inside this repo
bash scripts/setup.sh
bash scripts/setup.sh --check

# Fast post-install health check
bash ~/.claude/skills/widget/scripts/doctor.sh

# Start Übersicht
bash ~/.claude/skills/widget/scripts/start-uebersicht.sh

# Install or update a template widget
bash ~/.claude/skills/widget/scripts/install-widget.sh \
  ~/.claude/skills/widget/templates/clock.jsx

# List installed widgets
bash ~/.claude/skills/widget/scripts/list-widgets.sh

# Write a brand-new custom widget
cat > ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx << 'EOF'
{widget_code}
EOF

# Hide a widget without deleting it
mv ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx \
   ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx.disabled

# Show a hidden widget
mv ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx.disabled \
   ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx

# Delete a widget
rm ~/Library/Application\ Support/Übersicht/widgets/{name}.jsx
```

建议使用 `scripts/` 中的辅助脚本来处理主机相关操作。只有在创建或替换实际的 JSX 内容时，才直接编写 Widget 文件。

当用户请求一个已存在的标准 Widget（该 Widget 有内置模板）时，不要从头开始重新编写。如有需要，运行 `scripts/setup.sh`，然后安装相应的模板。
在 `scripts/setup.sh` 成功完成且主机应用程序可用之前，不要安装或复制任何 Widget 文件。

---

## Widget 格式

```jsx
// Optional shell command. stdout is passed into render as output.
export const command = "date '+%H:%M:%S'"

// Refresh frequency in milliseconds. Pure frontend widgets should use false.
export const refreshFrequency = 1000

// CSS positioning. Use position: fixed.
export const className = `
  position: fixed;
  bottom: 90px;
  right: 40px;
`

// render receives { output, error }
export const render = ({ output }) => {
  return <div>{output?.trim()}</div>
}
```

---

## 必需遵守的规则

### 规则 1：切勿从 `react` 模块中导入 React
```jsx
// Bad
import { useState } from 'react'

// Good
import { React } from 'uebersicht'
```

### 规则 2：切勿在 `render` 方法中直接调用 Hooks
```jsx
// Bad
export const render = () => {
  const [n, setN] = React.useState(0)
}

// Good
const Widget = () => {
  const { useState } = React
  const [n, setN] = useState(0)
  return <div>{n}</div>
}

export const render = () => <Widget />
```

### 规则 3：切勿从状态更新函数中返回函数
```jsx
// Bad
setRemaining(r => {
  if (r <= 1) return p => p === 'work' ? BREAK : WORK
})

// Good
useEffect(() => {
  if (remaining !== 0) return
  setPhase(p => p === 'work' ? 'break' : 'work')
  setRemaining(p => p === 'work' ? BREAK : WORK)
}, [remaining])
```

---

## 位置参考

| 位置 | CSS 样式 |
|----------|-----|
| 右下角 | `bottom: 90px; right: 40px;` |
| 左下角 | `bottom: 90px; left: 40px;` |
| 右上角 | `top: 40px; right: 40px;` |
| 左上角 | `top: 40px; left: 40px;` |

---

## 内置模板

| 文件名 | 功能 | 默认位置 |
|------|---------|------------------|
| `clock.jsx` | 时钟和日期显示 | 右下角 |
| `horizon-clock.jsx` | 水平时钟 | 右下角 |
| `pomodoro.jsx` | 波莫多罗计时器 | 左下角 |
| `now-playing.jsx` | 当前正在播放的音乐 | 中心位置 |
| `system-stats.jsx` | CPU、内存、电池信息 | 右上角 |
| `weather-canvas.jsx` | 动态天气卡片 | 左上角 |
| `git-pulse.jsx` | 本地 Git 活动热图 | 右上角 |
| `memo-capsule.jsx` | 本地快速笔记卡片 | 中心位置 |
| `volume-knob.jsx` | 系统音量控制旋钮 | 右侧 |
| `tap-counter.jsx` | 具有持久本地状态的简单交互式计数器 | 右下角 |

如果模板已经符合需求，可以直接复制使用；或者将其作为自定义 Widget 的起点。

---

## 样式基础

```css
background: rgba(8, 12, 20, 0.72);
backdrop-filter: blur(24px);
-webkit-backdrop-filter: blur(24px);
border-radius: 18px;
border: 1px solid rgba(255, 255, 255, 0.08);
box-shadow: 0 14px 40px rgba(0, 0, 0, 0.35);
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
color: rgba(255, 255, 255, 0.92);
```

对于仅用于显示的 Widget，添加以下样式：

```css
pointer-events: none;
```

---

## 有用的 macOS Shell 命令

```bash
date '+%H:%M:%S'
date '+%Y年%-m月%-d日 %A'
pmset -g batt | grep -o '[0-9]*%' | head -1
top -l 1 | grep "CPU usage" | awk '{print $3}'
curl -s "wttr.in/?format=%t+%C"
```

在渲染之前，请记得使用 `.trim()` 命令来处理输出内容。