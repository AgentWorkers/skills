---
name: openclaw
description: 全面掌握 OpenClaw 生态系统的安装、配置和管理技能（包括 Gateway、Channels、Models、Automation、Nodes 以及 Deployment 等组件）。
---

# OpenClaw 技能中心

这是 OpenClaw 的终极命令中心，提供了用于管理平台各个方面的指令和脚本，从首次安装到高级的多代理编排。

## 核心功能
- **基础设施**：原生服务、Docker Compose、Nix 构建环境以及回滚管理。
- **连接性**：支持全球通信渠道（WhatsApp、Telegram、Discord）和机器人 API。
- **智能功能**：支持主流大语言模型（LLM）的 OAuth 认证、模型别名管理以及本地模型扫描。
- **设备与硬件**：支持移动节点（摄像头、音频、GPS）功能，以及与 macOS 的集成。
- **高级逻辑**：支持 OpenProse（并行代理）和子代理管理，以及浏览器控制功能。

## 统一命令工具
所有操作均通过以下统一脚本执行：
`bash scripts/openclaw.sh [命令] [参数]`

### 1. 设置与维护
- `install`：安装或更新命令行界面（CLI）。
- `setup`：运行入门向导并安装相关服务。
- `doctor`：进行全面的状态和配置检查。
- `status`：显示连接状态和代理运行情况。
- `reset`：执行系统重置。

### 2. 服务与部署
- `service {start|stop|restart|logs}`：管理后台守护进程。
- `docker {setup|up|down|logs}`：管理容器化环境。

### 3. 通信渠道与认证
- `channel login [whatsapp|telegram|discord]`：连接消息传递账户。
- `channel list`：查看当前激活的通信渠道。
- `auth {anthropic|openai}`：管理 OAuth 提供者令牌。
- `pairing`：管理移动节点的设备授权。

### 4. 高级交互功能
- `browser {start|open|screenshot}`：使用 Playwright 实现的浏览器控制功能。
- `cron {list|add|remove}`：安排定期任务。
- `plugin {install|enable}`：管理插件和扩展程序。
- `msg [目标] [消息]`：从终端发送消息。

## 文档与参考资料
请参阅以下本地指南以获取详细的技术信息：
- `references/cli-full.md`：所有 CLI 命令及其子命令的完整列表。
- `references/config-schema.md`：`openclaw.json` 的结构及环境变量说明。
- `references/nodes-platforms.md`：Windows（WSL2）、macOS 和移动节点的使用指南。
- `references/deployment.md`：Docker、Nix、Hetzner 服务器的部署及更新/回滚流程。
- `references/advanced-tools.md`：OpenProse、浏览器、插件和子代理的相关信息。
- `references/hubs.md`：在线文档的集中链接列表。

## 故障排除
- **权限问题**：全局安装时请使用 `sudo`，或检查 `~/.openclaw` 文件的权限设置。
- **连接丢失**：确保 Node.js 版本 >= 22，并使用 `openclaw.sh service restart` 重启相关服务。
- **无法扫描 QR 码**：确认网关端口（18789）可以通过回环网络或隧道访问。