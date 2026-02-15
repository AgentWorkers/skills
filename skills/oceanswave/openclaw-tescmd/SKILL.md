---
name: openclaw-tescmd
slug: openclaw-tescmd
displayName: OpenClaw Tesla (tescmd)
version: 0.9.7
description: 通过 tescmd 节点控制特斯拉车辆并进行遥测的安装与设置指南。
homepage: https://github.com/oceanswave/openclaw-tescmd
metadata: {"category":"platform","platform":"tesla","node":"tescmd"}
---

# OpenClaw Tesla (tescmd) — 设置指南

此插件通过 [tescmd](https://github.com/oceanswave/tescmd) 节点将特斯拉车辆连接到 OpenClaw Gateway。安装并配对后，插件会自动注册所有工具、命令、斜杠命令以及遥测事件类型。

本文档仅涵盖 **安装和设置** 的内容。运行时工具的使用、工作流程和错误处理由 `tescmd` 提供（请调用 `tescmd_help` 以获取完整参考信息）。

**您将获得：**
- 39 个可通过代理调用的工具
- 14 个斜杠命令
- 实时遥测数据流
- 超级充电站信息（通过 supercharge.info 提供超过 10,000 个充电站的位置）
- 当节点断开连接时使用 CLI 作为备用方案

**仓库：**
- 插件：https://github.com/oceanswave/openclaw-tescmd
- tescmd 节点（Python CLI）：https://github.com/oceanswave/tescmd

---

## 架构

```
Agent (you)
  ↓  tool calls
OpenClaw Gateway
  ↓  node.invoke.request
openclaw-tescmd Plugin
  ↓  WebSocket dispatch
tescmd Node (Python)
  ├─ Tesla Fleet API (REST)
  ├─ Vehicle Command Protocol (VCSEC — signed commands)
  └─ Fleet Telemetry Stream (WebSocket)
  ↓
Tesla Vehicle
```

该插件是 tescmd 节点的 **网关端对应组件**。它定义了工具的接口并路由调用请求。tescmd 节点负责与特斯拉的所有直接通信。

---

## 设置

### 第 1 步：检查先决条件

在开始之前，请确认所需工具已安装并完成身份验证。

#### 必需工具：git

```bash
git --version
```

如果未安装，请安装：
- macOS：`xcode-select --install`
- Linux：`sudo apt install git` 或 `sudo dnf install git`

#### 必需工具：GitHub CLI (gh)

```bash
gh --version
gh auth status
```

如果未安装 `gh`：
- macOS：`brew install gh`
- Linux：请参阅 https://github.com/cli/cli/blob/trunk/docs/install_linux.md

如果未登录：
```bash
gh auth login
```

**告知用户：**“请在终端中完成 GitHub CLI 的登录。根据提示选择您的偏好设置并完成基于浏览器的身份验证流程。”

等待用户确认登录完成后再继续。

#### 必需工具：Python 3.11 或更高版本

```bash
python3 --version
```

必须使用 Python 3.11 或更高版本。如果未安装：
- macOS：`brew install python@3.12`
- Linux：`sudo apt install python3.12` 或使用 pyenv

#### 推荐工具：Tailscale

Tailscale 提供了一个公共 HTTPS 端点，用于特斯拉车队的遥测数据流传输，无需任何基础设施设置。

```bash
tailscale version
tailscale status
```

如果未安装：
- macOS：`brew install tailscale` 或从 https://tailscale.com/download 下载
- Linux：`curl -fsSL https://tailscale.com/install.sh | sh`

如果未登录：
```bash
sudo tailscale up
```

**告知用户：**“如果系统提示，请在浏览器中完成 Tailscale 的登录。”

等待用户确认登录完成后再继续。

---

### 第 2 步：安装 tescmd OpenClaw 插件

#### 标准安装：

```bash
openclaw plugins install @oceanswave/openclaw-tescmd
```

#### 验证安装：

```bash
openclaw plugins list
```

您应该会看到版本号为 0.9.0 或更高版本的插件。

#### 插件管理命令：

| 命令 | 功能 |
|---------|---------|
| `openclaw plugins list` | 列出已安装的插件 |
| `openclaw plugins info openclaw-tescmd` | 查看插件详细信息 |
| `openclaw plugins doctor` | 检查插件状态 |
| `openclaw plugins update openclaw-tescmd` | 更新到最新版本 |
| `openclaw plugins enable openclaw-tescmd` | 启用插件 |
| `openclaw plugins disable openclaw-tescmd` | 禁用插件（不卸载） |

---

### 第 3 步：安装 tescmd CLI

```bash
pip install tescmd
```

验证安装结果：
```bash
tescmd --version
```

---

### 第 4 步：运行 tescmd 设置向导

tescmd 设置向导是 **交互式的**，需要用户在终端和浏览器中完成相应的操作。您无法自动完成此步骤。

```bash
tescmd setup
```

**告知用户：**“我已经启动了 tescmd 设置向导。这个过程会引导您完成以下步骤：**
1. 创建特斯拉开发者应用程序
2. 生成您的 EC 密钥对
3. 通过 GitHub Pages 或 Tailscale Funnel 存储您的公钥
4. 在特斯拉车队 API 中注册
5. 在浏览器中完成 OAuth2 登录
6. 将密钥与车辆配对（需要亲自到车辆现场操作）

“请按照终端中的提示操作，并在设置完成后告诉我。”

**等待用户确认设置完成后再继续。**

#### 验证设置

用户确认完成后，检查身份验证状态：
```bash
tescmd auth status
```

此时应显示一个有效的令牌。如果令牌过期或丢失，用户需要重新运行设置向导：
```bash
tescmd auth login
```

---

### 第 5 步：识别车辆

列出账户中的车辆以获取车辆识别号（VIN）：
```bash
tescmd vehicle list
```

请记住 VIN，因为它是执行 `serve` 命令所必需的。

---

### 第 6 步：启动 tescmd 节点并与 Gateway 配对

tescmd 节点将特斯拉车队 API 与 OpenClaw Gateway 连接起来。首次连接需要一次性配对批准。

#### 首次配对：

仅使用 Gateway URL 启动节点（无需令牌）：
```bash
tescmd serve <VIN> --openclaw <gateway_ws_url>
```

节点会向 Gateway 发送 `node.pair.request` 请求并等待批准。该请求会在 **5 分钟** 后过期，请及时批准。

**在另一个终端中**，批准配对请求：
```bash
openclaw nodes pending                # View waiting pair requests
openclaw nodes approve <requestId>    # Approve the node
```

批准后，Gateway 会生成一个身份验证令牌。节点会将其保存到 `~/.config/tescmd/bridge.json` 文件中，并建立已认证的连接。无需手动处理令牌。

**告知用户：**“使用 `tescmd serve <VIN> --openclaw <gateway_url>` 启动 tescmd 节点，然后在另一个终端中运行 `openclaw nodes pending` 和 `openclaw nodes approve <requestId>` 以完成配对。”

**等待用户确认配对完成后再继续。**

#### 后续连接（已配对的情况）：

配对完成后，节点会使用保存的令牌自动重新连接：
```bash
tescmd serve <VIN> --openclaw <gateway_ws_url>
```

如有需要，您也可以显式传递令牌：
```bash
tescmd serve <VIN> --openclaw <gateway_ws_url> --openclaw-token <gateway_token>
```

#### 节点管理命令：

| 命令 | 功能 |
|---------|---------|
| `openclaw nodes pending` | 查看待处理的配对请求 |
| `openclaw nodes approve <id>` | 批准某个节点 |
| `openclaw nodes reject <id>` | 拒绝某个节点 |
| `openclaw nodes status` | 列出已配对的节点及其状态 |

#### 运行模式：

| 模式 | 命令 | 描述 |
|------|---------|-------------|
| **全模式**（默认） | `tescmd serve <VIN> --openclaw <url>` | 包含 MCP 服务器、遥测数据和 OpenClaw 桥接 |
| **仅桥接模式** | `tescmd serve <VIN> --no-mcp --openclaw <url>` | 仅包含遥测数据和 OpenClaw，不包含 MCP 服务器 |
| **使用 Tailscale** | `tescmd serve <VIN> --tailscale --openclaw <url>` | 通过 Tailscale Funnel 提供 MCP 服务 |
| **模拟运行** | `tescmd serve <VIN> --dry-run` | 以 JSONL 格式记录事件，不连接 Gateway |

#### 关键参数说明：

| 参数 | 描述 |
|------|-------------|
| `<VIN>` | 车辆识别号（位置参数） |
| `--openclaw <ws_url>` | Gateway 的 WebSocket URL（例如 `ws://host:18789`） |
| `--openclaw-token <token>` | Gateway 的身份验证令牌（配对后自动保存） |
| `--openclaw-config <path>` | 桥接配置文件（默认：`~/.config/tescmd/bridge.json`） |
| `--transport <type>` | MCP 传输方式：`streamable-http`（默认）或 `stdio` |
| `--port <num>` | MCP HTTP 端口（默认：8080） |
| `--host <addr>` | MCP 绑定地址（默认：127.0.0.1） |
| `--telemetry-port <num>` | 遥测 WebSocket 端口（默认：4443） |
| `--fields <preset>` | 遥测字段：`driving`、`charging` 或 `all` |
| `--interval <sec>` | 遥测数据轮询间隔（秒） |
| `--no-telemetry` | 禁用遥测数据流 |
| `--no-mcp` | 禁用 MCP 服务器 |
| `--no-log` | 禁用 CSV 格式的遥测数据记录 |
| `--dry-run` | 以 JSONL 格式记录事件，不连接 Gateway |
| `--tailscale` | 通过 Tailscale Funnel 提供 MCP 服务 |
| `--client-id <id>` | MCP 的 OAuth 客户端 ID |
| `--client-secret <secret>` | MCP 的 OAuth 客户端密钥 |

#### 环境变量（替代参数设置方式）：

这些参数可以设置在 `~/.config/tescmd/.env` 文件中：
```bash
TESLA_CLIENT_ID=your-client-id
TESLA_CLIENT_SECRET=your-client-secret
TESLA_VIN=5YJ3E1EA1NF000000
TESLA_REGION=na                    # na, eu, or cn
OPENCLAW_GATEWAY_URL=ws://gateway.example.com:18789
OPENCLAW_GATEWAY_TOKEN=your-token
TESLA_COMMAND_PROTOCOL=auto        # auto, signed, or unsigned
```

---

### 第 7 步：验证连接

确认节点已启动并成功配对后，验证其是否已连接到 Gateway：
```bash
openclaw nodes status
```

或者使用代理工具：
- 调用 `tescmd_node_status` 来检查连接状态

如果连接成功，插件中的工具即可使用。请调用 `tescmd_help` 以获取完整的运行时参考信息，包括工具的使用方法、工作流程和错误处理方式。

---

## 设置故障排除

| 问题 | 解决方案 |
|---------|----------|
| “没有节点连接” | 启动节点：`tescmd serve <VIN> --openclaw <url>` |
| 配对请求未显示 | 查看 `openclaw nodes pending` — 请求会在 5 分钟后过期。重新启动节点以生成新请求。 |
| 节点连接后又断开 | 检查 Gateway URL。运行 `tescmd auth status` 以验证特斯拉的身份验证状态。 |
| 身份验证/令牌错误 | 重新进行身份验证：`tescmd auth login` |
| 设置向导出现问题 | 重新运行 `tescmd setup` 或查看 https://github.com/oceanswave/tescmd |
| 插件无法加载 | 运行 `openclaw plugins doctor`。检查 `openclaw plugins list` 以确认插件是否存在。 |
| 触发器显示“不可用” | 重新启动节点并启用遥测数据传输：移除 `--no-telemetry` 参数或添加 `--fields all` 参数 |

---

## 配置

基本配置由 tescmd 节点处理，无需额外配置。

```json
{
  "plugins": {
    "entries": {
      "openclaw-tescmd": {
        "enabled": true,
        "config": {
          "debug": false
        }
      }
    }
  }
}
```

---

## CLI 快速参考

### tescmd CLI 命令

```bash
tescmd serve <VIN> --openclaw <url>                              # Start node (uses stored token)
tescmd serve <VIN> --openclaw <url> --openclaw-token <token>     # Start node (explicit token)
tescmd setup                        # Interactive setup wizard
tescmd auth status                  # Check auth token status
tescmd auth login                   # Re-authenticate with Tesla
tescmd vehicle list                 # List vehicles on account
tescmd vehicle info                 # Full vehicle data snapshot
tescmd cache status                 # Check cache stats
```