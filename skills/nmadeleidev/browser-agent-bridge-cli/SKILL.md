---
name: browser-bridge-cli
description: 当您需要控制或对用户的 Chrome 浏览器标签页执行某些操作时，请使用此技能。
---
# 浏览器桥接 CLI（Browser Bridge CLI）

## 使用场景

当您需要控制 Chrome 浏览器中的某个标签页时，请使用此工具。典型应用场景包括：
- 在实时用户浏览器环境中进行自动化操作
- 观察页面内容（包括交互式元素和 DOM 结构）
- 执行远程标签页操作（如导航、点击、输入、滚动）
- 解决代理程序与浏览器之间的连接问题

项目链接：  
https://github.com/NmadeleiDev/browser_agent_bridge

## 功能概述

该工具包含三个相互关联的部分：
- Chrome 扩展程序接收来自用户的标签页操作指令。
- 桥接服务器负责在浏览器与操作者之间传递消息。
- 操作者通过 CLI 发送指令并接收操作结果。

### 使用的 CLI 命令：
- `browser-bridge-server`：用于启动服务器
- `browser-bridge`：用于执行具体的操作命令

## 先决条件：
- Python 3.10 或更高版本
- 安装了 Chrome 浏览器
- 具有终端访问权限
- 能够安装和运行 Chrome 扩展程序

## 代理程序启动前的准备工作

在启动服务器之前，必须生成安全的令牌（切勿使用默认的弱令牌）。  
**令牌生成示例：**  
```bash
python3 - <<'PY'
import secrets
print("BRIDGE_SHARED_TOKEN=" + secrets.token_urlsafe(32))
print("BRIDGE_OPERATOR_TOKEN=" + secrets.token_urlsafe(32))
PY
```

启动服务器时，请使用生成的令牌。仅将客户端令牌（`BRIDGE_SHARED_TOKEN`）共享给用户以完成扩展程序的配置；操作者令牌则保留供 CLI 使用。

## CLI 安装方法  
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install browser-agent-bridge
```

后续可进行升级：  
```bash
pipx upgrade browser-agent-bridge
```

## 启动桥接服务器

**本地设置示例：**  
使用静态身份验证进行简单配置：  
```bash
export BRIDGE_AUTH_MODE=static
export BRIDGE_SHARED_TOKEN='change-me-strong-token'
export BRIDGE_OPERATOR_TOKEN='Str0ng!Operator#42'
browser-bridge-server >/tmp/browser-bridge-server.log 2>&1 &
echo $! >/tmp/browser-bridge-server.pid
```

在后台运行 `browser-bridge-server`。请确保该进程不会随当前终端会话关闭，因为代理程序需要该终端来执行后续的 CLI 命令、检查状态及进行故障排查。如果需要验证服务器是否正常启动，请查看日志文件或进程状态。

**默认端点：**
- 扩展程序客户端 WebSocket：`ws://127.0.0.1:8765/ws/client`
- 操作者 CLI WebSocket：`ws://127.0.0.1:8765/ws/operator`

## 配置 Chrome 扩展程序（操作步骤）：
1. 打开 Chrome 的“扩展程序”页面（`chrome://extensions`）。
2. 启用“开发者模式”。
3. 点击“加载解压的扩展程序文件”。
4. 从 [项目仓库](https://github.com/NmadeleiDev/browser_agent_bridge) 选择相应的扩展程序文件夹（`extension/`）。
5. 点击“安装扩展程序”。
6. 填写以下信息：
   - **桥接服务器 WebSocket 地址**：`ws://127.0.0.1:8765/ws/client`
   - **实例 ID**：`local-instance`
   - **客户端 ID**：`chrome-main`
   - **认证令牌（JWT）**：由代理程序生成的 `BRIDGE_SHARED_TOKEN` 值
7. 点击“保存”后，再点击“连接”。
8. 确认弹窗显示已成功连接到服务器。

## 操作者 CLI 使用方法

所有示例代码中使用的参数如下：
- `instance_id=local-instance`
- `client_id=chrome-main`
- 操作者令牌：`Str0ng!Operator#42`
- 操作者 WebSocket 地址：`ws://127.0.0.1:8765/ws/operator`

### 常用命令：
- **列出连接的客户端**：`list-clients`
- **检查特定客户端是否连接**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' list-clients
````
- **确认标签页操作通道是否可用**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  ping-tab --instance-id local-instance --client-id chrome-main
````
- **观察当前页面的交互式元素**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  observe --instance-id local-instance --client-id chrome-main --max-nodes 150
````
- **获取页面 HTML 内容**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  send-command --instance-id local-instance --client-id chrome-main \
  --type get_html --payload '{"max_chars":40000}'
````
- **带有自适应加载等待功能的导航**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  send-command --instance-id local-instance --client-id chrome-main \
  --type navigate --payload '{"url":"https://example.com","wait_for_load":true,"wait_for_load_ms":7000}'
````
- **无加载等待的点击操作**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  send-command --instance-id local-instance --client-id chrome-main \
  --type click --payload '{"selector":"a[href]","wait_for_load":false}'
````
- **在元素中输入文本**：````bash
browser-bridge --server-ws-url ws://127.0.0.1:8765/ws/operator --token 'Str0ng!Operator#42' \
  send-command --instance-id local-instance --client-id chrome-main \
  --type type --payload '{"selector":"input[name=q]","text":"browser bridge"}'
````

### 推荐的操作流程：
1. 确保服务器进程正在运行。
2. 确保扩展程序已正确连接到服务器（检查 `instance_id`、`client_id` 和令牌是否匹配）。
3. 运行 `list-clients` 命令。
4. 运行 `connect-status` 命令检查连接状态。
5. 在执行操作前先运行 `observe` 命令观察页面。
6. 使用 `send-command` 命令执行具体操作（如导航、点击、输入、滚动、获取页面内容）。
7. 执行操作后再次运行 `observe` 命令以确认页面状态。

## 常见问题及解决方法：
- **目标客户端未连接**：
  - 确认弹窗显示已连接状态。
  - 检查 `instance_id` 和 `client_id` 是否与 CLI 参数一致。
  - 重新连接扩展程序并重试。
- **操作者认证失败**：
  - 确保提供的令牌（`--token`）与 `BRIDGE_operator_TOKEN` 一致。
- **命令执行超时**：
  - 增加 `--timeout-s` 参数的值。
  - 对于需要加载内容的操作，可以在请求中禁用或减少加载等待时间。
  - 确保操作的页面是正常可访问的（非受限页面，例如 `chrome://*`）。
- **服务器未响应**：
  - 重试一次；必要时扩展程序可以重新加载内容。
- **操作响应缓慢**：
  - 将 `wait_for_load` 参数设置为 `false` 以获得即时响应。
  - 或者减小 `wait_for_load_ms` 的值。

## 安全注意事项：
- 将令牌视为敏感信息，严格保密。
- 在非本地环境中使用 TLS 协议（`wss://`）并使用强密码。

## 完成标准：
- `list-clients` 命令能返回正确的客户端列表。
- `connect-status` 命令确认连接成功。
- `ping-tab` 命令确认服务器已准备好接收请求。
- `observe` 命令能返回页面数据。
- `send-command` 命令能返回有效的操作结果。