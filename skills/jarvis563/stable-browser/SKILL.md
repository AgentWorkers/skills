---
name: stable-browser
description: 使用 Chrome DevTools Protocol (CDP) 来设置可靠的浏览器自动化方案，而不是依赖那些容易出问题的浏览器扩展程序。当浏览器扩展程序频繁断开连接、抛出 WebSocket 403 错误，或者当你需要稳定的无头浏览器控制（用于网页抓取、表单填写、社交媒体发布等自动化任务时），请使用 CDP。只需将 `profile="chrome"` 替换为可靠的 CDP 连接即可。
---
# 稳定的浏览器连接方案

请使用直接的 Chrome DevTools 协议连接，以替代不可靠的浏览器扩展程序中继。

## 问题所在

OpenClaw 浏览器扩展程序中继（`profile="chrome"`）经常出现以下问题：
- WebSocket 连接失败（403 错误）
- 端口混淆（网关端口与中继端口不一致）
- 自动化操作过程中连接中断
- 出现“无法访问浏览器控制服务”的错误
- 标签页或徽标的显示出现问题

## 解决方案：使用 Chrome DevTools（CDP）

启动 Chrome 时启用调试端口，并直接通过该协议进行连接。无需安装任何扩展程序。

### 快速设置

运行设置脚本以完成所有配置：

```bash
bash scripts/setup-cdp.sh
```

该脚本将：
1. 在 `~/.chrome-debug-profile` 目录下创建一个专用的 Chrome 配置文件
2. 将 `browser.cdpUrl` 添加到您的 OpenClaw 配置文件中
3. （针对 macOS）创建一个启动代理，使 Chrome 在登录时自动启动
4. 验证连接是否正常工作

### 手动设置

如果您希望手动配置，请参阅 [references/manual-setup.md](references/manual-setup.md)。

### 使用方法

设置完成后，始终使用 `profile="openclaw"`（而非 `profile="chrome"`）：

```
browser(action="snapshot", profile="openclaw")
browser(action="navigate", profile="openclaw", targetUrl="https://example.com")
browser(action="screenshot", profile="openclaw")
```

### 与扩展程序中继的主要区别

| 特性 | 扩展程序中继 | 直接使用 CDP |
|---------|----------------|------------|
| 稳定性 | 经常断开连接 | 非常稳定 |
| 设置过程 | 需要安装扩展程序并附加标签页 | 仅需运行一次脚本 |
| 身份验证/cookie | 共享您的主 Chrome 账户信息 | 使用专用配置文件 |
| 连接速度 | 需通过扩展程序进行额外转发 | 直接使用协议 |
| 无头模式 | 不支持 | 可选（使用 `--headless=new` 参数）

### 专用配置文件

使用 CDP 时，Chrome 会使用 `~/.chrome-debug-profile` 作为专用配置文件。这意味着：
- 登录一次后，会保持登录状态
- 您的主 Chrome 浏览器不会受到影响
- 不会与其他扩展程序发生冲突
- 即使 Chrome 更新，配置也不会被破坏

### 使用技巧

- **首次使用**：登录您需要访问的网站（如 Google、GitHub、X、LinkedIn 等）。
- **多标签页处理**：CDP 会管理所有标签页；可以使用 `targetId` 来固定特定标签页。
- **无头模式**：在启动命令中添加 `--headless=new` 以进行隐式操作。
- **端口冲突**：如果端口 9222 被其他程序占用，请在启动命令和配置文件中更改端口。
- **重启 Chrome**：执行 `pkill -f 'remote-debugging-port=9222' && sleep 1 && bash scripts/setup-cdp.sh`。

### 故障排除

- **“无法访问浏览器”**：可能是 Chrome 未启用调试模式。请运行 `setup-cdp.sh` 或手动启动 Chrome。
- **端口 9222 被占用**：可能是其他程序占用了该端口。使用 `lsof -i :9222` 命令查找占用该端口的进程并终止它。
- **会话失效**：如果 Chrome 崩溃，请使用 `pkill -f chrome-debug-profile` 重启 Chrome。
- **配置文件损坏**：删除 `~/.chrome-debug-profile` 文件并重新运行设置脚本。