# Canvas 功能

在连接的 OpenClaw 节点（Mac 应用、iOS、Android）上显示 HTML 内容。

## 概述

Canvas 工具允许您在任何连接的节点的画布视图中展示网页内容。非常适合用于：

- 显示游戏、可视化效果和仪表板
- 展示生成的 HTML 内容
- 进行交互式演示

## 工作原理

### 架构

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Canvas Host    │────▶│   Node Bridge    │────▶│  Node App   │
│  (HTTP Server)  │     │  (TCP Server)    │     │ (Mac/iOS/   │
│  Port 18793     │     │  Port 18790      │     │  Android)   │
└─────────────────┘     └──────────────────┘     └─────────────┘
```

1. **Canvas 主机服务器**：从 `canvasHost.root` 目录提供静态的 HTML/CSS/JS 文件
2. **节点桥接器**：将画布的 URL 传递给连接的节点
3. **节点应用程序**：在 WebView 中渲染内容

### 与 Tailscale 的集成

Canvas 主机服务器的绑定方式取决于 `gateway.bind` 的设置：

| 绑定模式 | 服务器绑定地址 | 画布 URL 使用地址 |
| ---------- | ------------------- | -------------------------- |
| `loopback` | 127.0.0.1           | 本地主机（仅限本地）     |
| `lan`      | 局域网接口       | 局域网 IP 地址             |
| `tailnet`  | Tailscale 接口 | Tailscale 主机名         |
| `auto`     | 可用的最佳地址   | Tailscale > 局域网 > loopback |

**重要提示：** `canvasHostHostForBridge` 是从 `bridgeHost` 派生而来的。当节点连接到 Tailscale 时，接收到的 URL 为：

```
http://<tailscale-hostname>:18793/__openclaw__/canvas/<file>.html
```

这就是为什么使用 `localhost` 无法正常工作的原因——节点实际上接收的是 Tailscale 的主机名！

## 常用操作

| 操作        | 描述                                      |
| ---------- | ------------------------------------ |
| `present`     | 显示画布（可选目标 URL）                         |
| `hide`      | 隐藏画布                                  |
| `navigate`    | 导航到新的 URL                              |
| `eval`      | 在画布中执行 JavaScript                         |
| `snapshot`    | 截取画布的截图                             |

## 配置

在 `~/.openclaw/openclaw.json` 文件中配置：

```json
{
  "canvasHost": {
    "enabled": true,
    "port": 18793,
    "root": "/Users/you/clawd/canvas",
    "liveReload": true
  },
  "gateway": {
    "bind": "auto"
  }
}
```

### 实时刷新

当 `liveReload: true`（默认值）时，Canvas 主机会：

- 监控根目录中的文件变化（通过 `chokidar`）
- 将 WebSocket 客户端注入 HTML 文件
- 当文件发生变化时自动刷新连接的画布

这对开发非常有用！

## 工作流程

### 1. 创建 HTML 内容

将文件放置在画布的根目录中（默认路径为 `~/clawd/canvas/`）：

```bash
cat > ~/clawd/canvas/my-game.html << 'HTML'
<!DOCTYPE html>
<html>
<head><title>My Game</title></head>
<body>
  <h1>Hello Canvas!</h1>
</body>
</html>
HTML
```

### 2. 获取画布主机的 URL

检查您的网关绑定方式：

```bash
cat ~/.openclaw/openclaw.json | jq '.gateway.bind'
```

然后构建相应的 URL：

- **loopback**：`http://127.0.0.1:18793/__openclaw__/canvas/<file>.html`
- **lan/tailnet/auto**：`http://<hostname>:18793/__openclaw__/canvas/<file>.html`

获取您的 Tailscale 主机名：

```bash
tailscale status --json | jq -r '.Self.DNSName' | sed 's/\.$//'
```

### 3. 查找连接的节点

```bash
openclaw nodes list
```

查找支持画布功能的 Mac/iOS/Android 节点。

### 4. 显示内容

```
canvas action:present node:<node-id> target:<full-url>
```

**示例：**

```
canvas action:present node:mac-63599bc4-b54d-4392-9048-b97abd58343a target:http://peters-mac-studio-1.sheep-coho.ts.net:18793/__openclaw__/canvas/snake.html
```

### 5. 导航、截图或隐藏画布

```
canvas action:navigate node:<node-id> url:<new-url>
canvas action:snapshot node:<node-id>
canvas action:hide node:<node-id>
```

## 调试

### 白屏或内容无法加载

**原因：** 服务器绑定地址与节点的期望地址不匹配。

**调试步骤：**

1. 检查服务器绑定地址：`cat ~/.openclaw/openclaw.json | jq '.gateway.bind'`
2. 查看画布使用的端口：`lsof -i :18793`
3. 直接测试 URL：`curl http://<hostname>:18793/__openclaw__/canvas/<file>.html`

**解决方法：** 使用与绑定模式匹配的完整主机名，而不是 `localhost`。

### 出现 “需要节点” 错误

始终指定 `node:<node-id>` 参数。

### 出现 “节点未连接” 错误

节点可能处于离线状态。使用 `openclaw nodes list` 命令查找在线节点。

### 内容未更新

如果实时刷新功能不起作用：

1. 检查配置文件中的 `liveReload: true` 设置
2. 确保文件位于画布的根目录中
3. 查看日志中的错误信息

## URL 路径结构

Canvas 主机服务器从 `/__openclaw__/canvas/` 前缀提供内容：

```
http://<host>:18793/__openclaw__/canvas/index.html  → ~/clawd/canvas/index.html
http://<host>:18793/__openclaw__/canvas/games/snake.html → ~/clawd/canvas/games/snake.html
```

`/__openclaw__/canvas/` 前缀由 `CANVAS_HOST_PATH` 常量定义。

## 提示

- 为了获得最佳效果，请保持 HTML 文件的独立性（内嵌 CSS/JS）
- 使用默认的 `index.html` 作为测试页面（其中包含桥接器诊断信息）
- 画布会一直显示，直到您手动隐藏它或导航到其他页面
- 实时刷新功能可加快开发速度——只需保存文件即可自动更新！
- A2UI 的 JSON 推送功能正在开发中，目前请使用 HTML 文件