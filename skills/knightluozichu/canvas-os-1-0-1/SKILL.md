---
name: canvas-os
description: Canvas 作为一个应用程序平台：您可以在 OpenClaw Canvas 上构建、存储和运行丰富的可视化应用程序。
homepage: https://www.clawhub.ai/fraction12/canvas-os
metadata:
  openclaw:
    emoji: "🖥️"
    category: ui
    requires:
      bins: ["python3"]
---

# Canvas OS

Canvas 是一个应用程序平台，允许您在 OpenClaw Canvas 上构建、存储和运行丰富的可视化应用程序。

## 设计理念

Canvas 可以被视为一个操作系统，而应用程序则通过 Canvas 进行开发和运行。

**丰富的 HTML/CSS/JS 用户界面** —— 不仅仅是文本；支持完整的交互性、动画和实时数据展示。

## 快速命令

| 命令 | 功能                |
|---------|-------------------|
| "Open [app]" | 启动服务器，导航到 Canvas，注入数据 |
| "Build me a [type]" | 根据模板创建应用程序并打开它 |
| "Update [element]" | 通过 JavaScript 修改界面元素 |
| "Show [data] on canvas" | 在 Canvas 上快速显示数据 |
| "Close canvas" | 停止服务器，隐藏 Canvas 面板 |

## 工作原理

**核心原则：** 应用程序是在 **Canvas** 上运行的，而不是在浏览器标签页中运行的。Canvas 是您的用户界面窗口。

### Canvas 的加载方式

由于安全限制，Canvas 无法直接访问文件路径。以下是三种可行的加载方式：

| 方法 | 适用场景 | 优点 | 缺点 |
|--------|-----------|------|------|
| **本地主机服务器** | 复杂的应用程序或需要外部资源的情况 | 可使用完整的浏览器功能 | 需要管理端口号 |
| **直接 HTML 注入** | 快速展示或演示 | 无需服务器，立即生效 | 不能使用外部资源，且存在大小限制 |
| **数据 URL** | 适用于小型内容 | 代码独立 | 在某些系统上可能不稳定 |

**注意：** `file:///path/to/file.html` 这种方式因 Canvas 的安全策略而被禁止使用。

**参考文档：** `CANVAS-LOADING.md` 以获取详细指南和故障排除方法。

**辅助脚本：** `canvas-inject.py` — 用于将 HTML 格式化为可直接注入的格式。

### 1. 应用程序由 HTML/CSS/JS 文件组成
```
~/.openclaw/workspace/apps/[app-name]/
├── index.html    # The UI (self-contained recommended)
├── data.json     # Persistent state
└── manifest.json # App metadata
```

### 2. 通过本地主机服务器部署应用程序
```bash
cd ~/.openclaw/workspace/apps/[app-name]
python3 -m http.server [PORT] > /dev/null 2>&1 &
```

### 3. 在 Canvas 中导航到本地主机
```bash
NODE="Your Node Name"  # Get from: openclaw nodes status
openclaw nodes canvas navigate --node "$NODE" "http://localhost:[PORT]/"
```

**重要提示：** 应用程序将在 **Canvas** 面板上显示，而不是在浏览器中。

### 4. 通过 JavaScript 注入数据
```bash
openclaw nodes canvas eval --node "$NODE" --js "app.setData({...})"
```

**注意：** 在当前的 OpenClaw 版本中，`openclaw-canvas://` 这种 URL 方式存在问题，请使用 `http://localhost:` 代替。

## 打开应用程序

**功能说明：** 应用程序将在 **Canvas** 面板上显示，而不是在浏览器标签页中。

### 方法 1：使用本地主机服务器（推荐用于复杂应用程序）

具体步骤：
```bash
NODE="Your Node Name"
PORT=9876
APP="my-app"

# 1. Kill any existing server on the port
lsof -ti:$PORT | xargs kill -9 2>/dev/null

# 2. Start server
cd ~/.openclaw/workspace/apps/$APP
python3 -m http.server $PORT > /dev/null 2>&1 &

# 3. Wait for server
sleep 1

# 4. Navigate Canvas
openclaw nodes canvas navigate --node "$NODE" "http://localhost:$PORT/"

# 5. Inject data
openclaw nodes canvas eval --node "$NODE" --js "app.loadData({...})"
```

### 方法 2：直接 HTML 注入（适用于快速展示）

**适用场景：** 当文件路径因安全限制而无法使用时，或者需要立即显示内容时。

**注意：** Canvas 会阻止 `file:///path/to/file.html` 这种文件路径的访问。在这种情况下，请使用直接 HTML 注入方法。

**重要限制：** 为确保安全，Canvas 禁止使用 `file:///` 路径。请始终使用本地主机或直接 HTML 注入方式。

## 应用程序开发

### 应用程序的 API 规范

每个应用程序都应该提供一个 `window.app` 或 `window.[appname]` 对象：

```javascript
window.app = {
  // Update values
  setValue: (key, val) => {
    document.getElementById(key).textContent = val;
  },
  
  // Bulk update
  loadData: (data) => { /* render all */ },
  
  // Notifications
  notify: (msg) => { /* show toast */ }
};
```

### 双向通信

应用程序可以通过深层链接发送命令：

```javascript
function sendToAgent(message) {
  window.location.href = `openclaw://agent?message=${encodeURIComponent(message)}`;
}

// Button click → agent command
document.getElementById('btn').onclick = () => {
  sendToAgent('Refresh my dashboard');
};
```

## 模板

### 仪表盘
- 包含统计卡片、进度条和列表等元素；使用独立的 HTML 代码。
- 默认端口：9876
- API：`dashboard.setRevenue()`、`dashboard.setProgress()`、`dashboard.notify()`

### 追踪器
- 用于记录习惯或任务，支持复选框和进度条；使用独立的 HTML 代码。
- 默认端口：9877
- API：`tracker.setItem()`、`tracker.addItem()`、`tracker.toggleItem()`

## 快速展示（A2UI）

**适用于不需要完整应用程序的临时展示场景：**
```bash
openclaw nodes canvas a2ui push --node "$NODE" --text "
📊 QUICK STATUS

Revenue: \$500
Users: 100

Done!
"
```

## 端口分配

| 应用程序类型 | 默认端口 |
|----------|--------------|
| 仪表盘 | 9876 |
| 追踪器 | 9877 |
| 计时器 | 9878 |
| 显示器 | 9879 |
| 自定义应用程序 | 9880+ |

## 设计规范

1. **代码独立性** —— 使用内联的 CSS/JS 以确保应用程序的可移植性。
2. **采用深色主题** —— 与 OpenClaw 的整体设计风格保持一致。
3. **公开应用程序的 API** —— 允许通过 `window.app.*` 方法进行更新。
4. **为需要更新的元素添加 ID**。
5. **显示实时时钟** —— 以表明应用程序正在运行中。
6. **使用深层链接** —— 以实现双向通信。

## 故障排除

**应用程序在浏览器中打开而不是在 Canvas 上？**
- 确保使用了 `openclaw nodes canvas navigate` 而不仅仅是 `open` 命令。
- `canvas navigate` 命令专门用于导航到 Canvas 面板。

**在 Canvas 上显示“未找到”错误？**
- **文件路径问题：** Canvas 会阻止 `file:///` 类型的 URL 访问（出于安全考虑）。
- **数据 URL 可能失败：** 尝试使用 `canvas eval` 和 `document.write()` 进行直接 HTML 注入。
- 对于本地主机服务器：检查服务器是否正在运行：`curl http://localhost:[PORT]/`。
- 确认端口号是否正确。
- 使用 `http://localhost:` 而不是 `openclaw-canvas://`（该 URL 方式可能存在问题）。

**即使使用了正确的 URL，Canvas 仍然显示“未找到”错误？**
- 这是由于安全限制：Canvas 无法访问本地文件系统。
- **解决方法：** 使用方法 2（直接 HTML 注入）或方法 1（通过本地主机服务器部署）。

**应用程序无法更新？**
- 检查 `window.app` API 是否已定义：`openclaw nodes canvas eval --js "typeof window.app"`。
- 确认 JavaScript 代码中的 `eval` 语法是否正确（单引号需要放在双引号内）。

**服务器端口已被占用？**
- 找到并关闭占用的端口：`lsof -ti:[PORT] | xargs kill -9`

## 辅助脚本

### canvas-inject.py

这是一个 Python 脚本，用于实现直接 HTML 注入（方法 2）。

```bash
# Example usage in Python
from canvas_inject import inject_html_to_canvas

html = open("my-dashboard.html").read()
commands = inject_html_to_canvas(html, node_name="Your Node")

# Then use canvas tool with these commands
canvas.present(**commands["step1_present"])
canvas.eval(**commands["step2_inject"])
```

**或者，您也可以手动按照方法 2 的步骤进行操作。**

## 系统要求

- 安装支持 Canvas 功能的 OpenClaw（macOS 应用程序）。
- 安装 Python 3（用于运行 HTTP 服务器）。
- 需要一个具备 Canvas 功能的节点。