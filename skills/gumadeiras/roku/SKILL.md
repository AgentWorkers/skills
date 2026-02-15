---
name: roku
description: 通过命令行界面（CLI）控制Roku设备：支持设备发现、远程控制、应用程序启动、搜索功能，以及用于实时控制的HTTP桥接模式。
homepage: https://github.com/gumadeiras/roku-cli
repository: https://github.com/gumadeiras/roku-cli
metadata: {"clawdbot":{"emoji":"📺","requires":{"bins":["roku"]},"install":[{"id":"node","kind":"node","package":"roku-ts-cli","bins":["roku"],"label":"Install Roku CLI (npm)"}]}}
---

# Roku CLI

这是一个快速的TypeScript命令行工具（CLI），用于通过ECP API控制Roku设备。

## 安装

```bash
npm install -g roku-ts-cli@latest
```

## 快速入门

```bash
# Discover devices and save an alias
roku discover --save livingroom --index 1

# Use the alias
roku --host livingroom device-info
roku --host livingroom apps
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `roku discover` | 在网络中查找Roku设备 |
| `roku --host <ip> device-info` | 获取设备信息 |
| `roku --host <ip> apps` | 列出已安装的应用程序 |
| `roku --host <ip> command <key>` | 发送遥控器指令 |
| `roku --host <ip> literal <text>` | 在Roku设备上输入文本 |
| `roku --host <ip> search --title <query>` | 搜索内容 |
| `roku --host <ip> launch <app>` | 启动应用程序 |
| `roku --host <ip> interactive` | 进入交互式遥控器模式 |

## 交互式模式

```bash
roku livingroom                    # interactive control
roku --host livingroom interactive # same thing
```

使用箭头键、回车键和ESC键进行类似遥控器的操作。

## 桥接服务

运行一个持续的HTTP桥接服务，作为操作系统（macOS）或systemd（Linux）的原生服务：

```bash
# Install and start the service
roku bridge install-service --port 19839 --token secret --host livingroom --user
roku bridge start --user

# Service management
roku bridge status --user
roku bridge stop --user
roku bridge uninstall --user
```

通过HTTP发送命令：

```bash
# Send key
curl -X POST http://127.0.0.1:19839/key \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret" \
  -d '{"key":"home"}'

# Type text
curl -X POST http://127.0.0.1:19839/text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret" \
  -d '{"text":"hello"}'

# Launch app
curl -X POST http://127.0.0.1:19839/launch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer secret" \
  -d '{"app":"plex"}'

# Health check
curl http://127.0.0.1:19839/health -H "Authorization: Bearer secret"
```

### 桥接端点

| 端点 | 请求体 |
|----------|------|
| `POST /key` | `{"key": "home"}` |
| `POST /text` | `{"text": "hello"}` |
| `POST /search` | `{"title": "Stargate"}` |
| `POST /launch` | `{"app": "plex"}` |
| `GET /health` | — |
| `GET /health?deep=1` | 深度健康检查（探测Roku设备的状态） |

## 别名

```bash
# Save device alias
roku discover --save livingroom --index 1
roku alias set office 192.168.1.20

# Save app alias  
roku alias set plex 13535

# List aliases
roku alias list

# Use aliases
roku --host livingroom launch plex
```

## 遥控器指令

home, back, select, up, down, left, right, play, pause, rev, fwd, replay, info, power, volume_up, volume_down, mute

## 注意事项

- Roku设备必须与CLI处于同一网络中。
- 桥接服务作为原生服务运行（macOS使用launchd，Linux使用systemd）。
- 使用`--user`标志以用户空间模式运行服务（无需sudo权限）。
- 在桥接模式下使用`--token`进行身份验证。

## 代码来源

https://github.com/gumadeiras/roku-cli