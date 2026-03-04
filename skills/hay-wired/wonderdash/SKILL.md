---
name: wonderdash-widgets
description: 通过 GitHub 在用户的 WonderDash 移动仪表板上创建和管理小部件（widgets）。
version: 5.0.0
user-invocable: false

metadata:
  openclaw:
    requires:
      bins:
        - git
        - ssh
    os:
      - darwin
      - linux
    emoji: "\U0001F4F1"
---
# WonderDash 小部件技能（v5 — WebView + 索引 + 每个小部件一个文件）

您可以通过将单独的 JSON 文件写入 GitHub 仓库来管理用户 WonderDash 移动端仪表板上的小部件，同时使用 `dashboard.json` 索引来控制小部件的显示顺序和可见性。

## 设置

WonderDash 会向您发送一条设置消息，其中包含：
- **仓库 URL**：`git@github.com:{username}/wonderdash-widgets.git`
- **SSH 私钥**：一个以 OpenSSH PEM 格式表示的 Ed25519 密钥

请保存该 SSH 密钥并配置访问权限：

```bash
# Save the key
cat > ~/.ssh/wonderdash_deploy << 'KEYEOF'
<paste the key here>
KEYEOF
chmod 600 ~/.ssh/wonderdash_deploy

# Add SSH config
cat >> ~/.ssh/config << 'EOF'
Host wonderdash-github
  HostName github.com
  User git
  IdentityFile ~/.ssh/wonderdash_deploy
  IdentitiesOnly yes
EOF

# Clone the repo
git clone wonderdash-github:{username}/wonderdash-widgets.git
```

## 仓库结构

```
wonderdash-widgets/
├── dashboard.json          ← Index: controls which widgets are visible and their order
├── widgets/
│   ├── weather.json        ← Widget content
│   ├── portfolio.json
│   ├── tasks.json
│   └── old-widget.json     ← Archived: file exists but not listed in index
```

## 仪表板索引（`dashboard.json`）

位于仓库根目录的索引文件用于控制哪些小部件会显示以及显示的顺序：

```json
{
  "widgets": ["weather", "portfolio", "tasks"]
}
```

- 数组中的顺序即为仪表板上的显示顺序
- 每个条目都是一个小部件 ID，指向 `widgets/{id}.json` 文件
- 未包含在数组中的小部件将被隐藏（归档）——但其文件仍会保留在仓库中
- 如果 `dashboard.json` 不存在，则 `widgets/` 目录下的所有小部件都会被显示（无顺序）

## 小部件格式

每个小部件文件（`widgets/{id}.json`）包含一个单独的小部件对象：

```json
{
  "id": "weather",
  "size": "S",
  "renderer": "webview",
  "html": "<div>...</div>"
}
```

字段：
- **id**（字符串）：唯一的标识符——必须与文件名匹配（例如，`weather` → `widgets/weather.json`）
- **size**（`"S"` | `"M"` | `"L"`）：小部件的显示大小
- **renderer**（`"webview"` | `"html"`，可选）：渲染引擎。默认为 `"html"`（原生方式）。使用 `"webview` 可以实现更丰富的视觉效果。
- **html**（字符串）：包含内联样式的独立 HTML 代码

## 渲染器

### `"webview"` — 适用于大多数小部件的丰富类型

使用完整的浏览器引擎进行渲染。支持以下功能：
- CSS 渐变、阴影、`border-radius`、`backdrop-filter`
- CSS 动画（`@keyframes`、`transition`）
- SVG（图表、图标、折线图）
- Canvas
- JavaScript（实时时钟、计数器、数据格式化）
- Base64 编码的图片（`<img src="data:image/png;base64,...">`）
- 完整的 CSS flexbox 和 grid 布局

应用程序会使用默认的深色主题（`background: #1f2937`, `color: #fff`, 系统字体）来包裹您的 HTML 代码。您只需提供页面内容即可。

### `"html"` — 轻量级小部件（默认类型）

通过原生组件进行渲染（不依赖浏览器）。速度更快、更轻量，但仅支持基本的 HTML 元素和内联样式。不支持 JavaScript、动画、渐变或 SVG。适用于简单的文本/数字显示。

**对于任何需要视觉效果的小部件，请使用 `"webview"`。** 对于仅显示文本且性能比外观更重要的简单小部件，请使用 `"html"`。

## 小部件大小

参考苹果的 iOS 小部件系统设计：

| 大小 | 尺寸 | 布局 | 适用场景 |
|------|-----------|--------|----------|
| **S**（小） | 174 × 174 px | 方形布局，单列显示 | 单个指标、状态信息、图标 |
| **M**（中） | 361 × 174 px | 全宽显示 | 信息卡片、折线图、摘要信息 |
| **L**（大） | 361 × 382 px | 全宽显示 | 图表、表格、日历、信息流 |

两个小部件可以并排显示。中号和大型小部件会占据整个屏幕宽度。

## 创建小部件

创建小部件文件后，需要将其添加到索引文件中。

```bash
cd wonderdash-widgets
mkdir -p widgets

# 1. Create the widget file
cat > widgets/weather.json << 'EOF'
{
  "id": "weather",
  "size": "S",
  "renderer": "webview",
  "html": "..."
}
EOF

# 2. Add to dashboard.json index
# If dashboard.json doesn't exist yet, create it:
echo '{ "widgets": ["weather"] }' > dashboard.json
# If it already exists, read it, append the new ID to the widgets array, and write it back.

git add widgets/weather.json dashboard.json
git commit -m "Add weather widget"
git push
```

## 更新小部件

只需编辑小部件文件并提交更改。除非需要重新排序，否则无需修改 `dashboard.json`。

```bash
git add widgets/weather.json
git commit -m "Update weather widget"
git push
```

## 重新排序 / 归档 / 删除

- **重新排序**：修改 `dashboard.json` 中的数组顺序，然后提交并推送更改。
- **归档**：从 `dashboard.json` 中删除该小部件的 ID — 小部件文件仍保留在仓库中。
- **恢复**：将小部件的 ID 加回数组中。
- **永久删除**：从 `dashboard.json` 中删除该小部件，并通过 `git rm widgets/{id}.json` 删除对应的文件，然后提交并推送更改。

用户需要手动刷新仪表板才能看到更新后的内容。

## 设计指南

- **深色主题**：背景颜色为 `#1f2937`（灰度80%），文本颜色为 `#ffffff`，次要颜色为 `#9ca3af`（灰度40%），强调色为 `#3b82f6`（蓝色50%），成功状态为 `#22c55e`，警告状态为 `#eab308`，错误状态为 `#ef4444`。
- **自包含**：所有内容均为内联显示，不依赖外部资源（CDN、API、远程图片）。
- **JSON 编码**：在 JSON 字符串中处理 HTML 中的引号时需要进行转义。在 `style` 属性中使用 `\"` 表示双引号，或在 HTML 中使用单引号（例如：`style='...'`）。
- **适应大小**：内容必须完全显示在小部件的指定尺寸内，不得滚动。WebView 默认会设置 `overflow: hidden`。
- **柔和的动画效果**：使用平滑的过渡效果来提升视觉体验，避免使用过于炫目的动画。

## 示例

### 小型小部件 — 带渐变背景的温度显示（`widgets/temperature.json`）

一个带有渐变背景和柔和光效的温度显示组件。

```json
{
  "id": "temperature",
  "size": "S",
  "renderer": "webview",
  "html": "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg,#1e3a5f,#1f2937);padding:16px'><div style='font-size:11px;color:#60a5fa;text-transform:uppercase;letter-spacing:2px;font-weight:600'>Temperature</div><div style='font-size:52px;font-weight:bold;margin:8px 0;background:linear-gradient(180deg,#fff,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>72°</div><div style='font-size:13px;color:#9ca3af'>☀️ Sunny</div></div>"
}
```

### 小型小部件 — 带 CSS 动画的状态指示器（`widgets/api-status.json`）

一个带有 CSS 动画的脉冲式状态指示器。

```json
{
  "id": "api-status",
  "size": "S",
  "renderer": "webview",
  "html": "<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}.pulse{animation:pulse 2s ease-in-out infinite}</style><div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:16px'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px'>API Status</div><div class='pulse' style='width:48px;height:48px;border-radius:50%;background:radial-gradient(circle,#22c55e,#15803d);box-shadow:0 0 20px rgba(34,197,94,0.4);margin-bottom:12px'></div><div style='font-size:15px;font-weight:600;color:#22c55e'>Operational</div><div style='font-size:12px;color:#6b7280;margin-top:4px'>99.9% uptime</div></div>"
}
```

### 中型小部件 — SVG 折线图（`widgets/revenue.json`）

一个包含内联 SVG 折线图的收入信息卡片。

```json
{
  "id": "revenue",
  "size": "M",
  "renderer": "webview",
  "html": "<div style='display:flex;align-items:center;height:100%;padding:16px;gap:20px'><div style='flex:1'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Monthly Revenue</div><div style='font-size:32px;font-weight:bold;margin:6px 0'>$48.2k</div><div style='font-size:13px;color:#22c55e;font-weight:500'>↑ 12.5% vs last month</div></div><div style='width:140px;height:60px'><svg viewBox='0 0 140 60' style='width:100%;height:100%'><defs><linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='#3b82f6' stop-opacity='0.3'/><stop offset='100%' stop-color='#3b82f6' stop-opacity='0'/></linearGradient></defs><path d='M0,45 L20,40 L40,42 L60,30 L80,35 L100,20 L120,18 L140,10 L140,60 L0,60Z' fill='url(#g)'/><polyline points='0,45 20,40 40,42 60,30 80,35 100,20 120,18 140,10' fill='none' stroke='#3b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg></div></div>"
}
```

### 中型小部件 — 带渐变边框的信息卡片（`widgets/next-meeting.json`）

一个带有渐变边框的会议信息卡片。

```json
{
  "id": "next-meeting",
  "size": "M",
  "renderer": "webview",
  "html": "<div style='display:flex;align-items:center;height:100%;padding:16px;gap:16px'><div style='width:4px;height:80%;border-radius:2px;background:linear-gradient(180deg,#8b5cf6,#3b82f6)'></div><div style='flex:1'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Next Meeting</div><div style='font-size:18px;font-weight:bold;margin:6px 0'>Sprint Planning</div><div style='font-size:13px;color:#9ca3af'>2:00 PM — 3:00 PM</div><div style='display:flex;gap:6px;margin-top:8px'><span style='font-size:11px;background:#374151;color:#d1d5db;padding:2px 8px;border-radius:10px'>Team Alpha</span><span style='font-size:11px;background:#374151;color:#d1d5db;padding:2px 8px;border-radius:10px'>Zoom</span></div></div></div>"
}
```

### 大型小部件 — 带 SVG 的比特币价格图表（`widgets/btc-price.json`）

一个带有渐变背景、网格线和价格标签的比特币价格图表。

```json
{
  "id": "btc-price",
  "size": "L",
  "renderer": "webview",
  "html": "<div style='display:flex;flex-direction:column;height:100%;padding:16px'><div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px'><div><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Bitcoin</div><div style='font-size:28px;font-weight:bold;margin-top:4px'>$67,432</div></div><div style='text-align:right'><div style='font-size:14px;color:#22c55e;font-weight:600'>+2.4%</div><div style='font-size:12px;color:#6b7280'>24h</div></div></div><div style='flex:1;margin-top:8px;position:relative'><svg viewBox='0 0 330 240' style='width:100%;height:100%' preserveAspectRatio='none'><defs><linearGradient id='cg' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='#f59e0b' stop-opacity='0.25'/><stop offset='100%' stop-color='#f59e0b' stop-opacity='0'/></linearGradient></defs><line x1='0' y1='60' x2='330' y2='60' stroke='#374151' stroke-width='0.5'/><line x1='0' y1='120' x2='330' y2='120' stroke='#374151' stroke-width='0.5'/><line x1='0' y1='180' x2='330' y2='180' stroke='#374151' stroke-width='0.5'/><text x='325' y='58' fill='#6b7280' font-size='10' text-anchor='end'>69k</text><text x='325' y='118' fill='#6b7280' font-size='10' text-anchor='end'>67k</text><text x='325' y='178' fill='#6b7280' font-size='10' text-anchor='end'>65k</text><path d='M0,180 C30,175 50,160 80,140 C110,120 130,90 160,100 C190,110 210,130 230,80 C250,40 270,55 300,30 C310,25 320,28 330,20 L330,240 L0,240Z' fill='url(#cg)'/><path d='M0,180 C30,175 50,160 80,140 C110,120 130,90 160,100 C190,110 210,130 230,80 C250,40 270,55 300,30 C310,25 320,28 330,20' fill='none' stroke='#f59e0b' stroke-width='2.5' stroke-linecap='round'/><circle cx='330' cy='20' r='4' fill='#f59e0b'/><circle cx='330' cy='20' r='8' fill='#f59e0b' opacity='0.2'/></svg></div><div style='display:flex;justify-content:space-between;font-size:11px;color:#6b7280;margin-top:4px'><span>6h ago</span><span>4h</span><span>2h</span><span>Now</span></div></div>"
}
```

### 大型小部件 — 带 CSS 栅格的日历（`widgets/calendar.json`）

一个带有 CSS 栅格布局的月度日历，突出显示重要日期。

```json
{
  "id": "calendar",
  "size": "L",
  "renderer": "webview",
  "html": "<style>.day{display:flex;align-items:center;justify-content:center;height:36px;border-radius:50%;font-size:13px;color:#d1d5db}.today{background:#3b82f6;color:#fff;font-weight:bold}.event{position:relative}.event::after{content:'';position:absolute;bottom:2px;left:50%;transform:translateX(-50%);width:4px;height:4px;background:#f59e0b;border-radius:50%}.muted{color:#4b5563}</style><div style='display:flex;flex-direction:column;height:100%;padding:16px'><div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'><div style='font-size:16px;font-weight:bold'>March 2026</div><div style='font-size:12px;color:#9ca3af'>3 events</div></div><div style='display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center'><div style='font-size:11px;color:#6b7280;padding:4px 0'>Su</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Mo</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Tu</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>We</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Th</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Fr</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Sa</div><div class='day'>1</div><div class='day today'>2</div><div class='day'>3</div><div class='day event'>4</div><div class='day'>5</div><div class='day'>6</div><div class='day'>7</div><div class='day'>8</div><div class='day'>9</div><div class='day event'>10</div><div class='day'>11</div><div class='day'>12</div><div class='day'>13</div><div class='day'>14</div><div class='day'>15</div><div class='day'>16</div><div class='day'>17</div><div class='day event'>18</div><div class='day'>19</div><div class='day'>20</div><div class='day'>21</div><div class='day'>22</div><div class='day'>23</div><div class='day'>24</div><div class='day'>25</div><div class='day'>26</div><div class='day'>27</div><div class='day'>28</div><div class='day'>29</div><div class='day'>30</div><div class='day'>31</div></div></div>"
}
```

### `dashboard.json` 示例

```json
{
  "widgets": ["temperature", "api-status", "revenue", "next-meeting", "btc-price", "calendar"]
}
```