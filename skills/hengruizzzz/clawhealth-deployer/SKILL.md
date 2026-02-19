---
name: clawhealth-deployer
description: 将 ClawHealth（适用于 Open Wearables 的设备）部署到这台机器上，并将其连接到 OpenClaw；用户随后可以通过 ClawHealth iOS 应用程序（我们发布的 SDK）来传输数据。需要注意的是，该过程不会自动安装 OpenClaw——用户必须已经安装了 OpenClaw。
metadata:
  openclaw:
    requires:
      bins: ["docker", "git", "make", "node"]
    emoji: "❤️"
---
# ClawHealth 部署工具

将 **ClawHealth**（Open Wearables 的后端服务）部署到这台机器上，并将其连接到 OpenClaw 的 MCP（中间件服务器）中。用户可以通过 **ClawHealth iOS 应用**（该应用基于我们发布的 SDK 构建）将他们的健康数据连接到系统中，这样助手就可以根据实际的健康数据回答诸如“我上周的睡眠情况如何？”或“我的步数是多少？”之类的问题。

**前提条件：** OpenClaw 已经安装并运行（例如通过 [openclaw.ai](https://openclaw.ai/) 或 ClawHub）。此工具仅负责部署 ClawHealth 并将其连接到现有的 OpenClaw 中。

## 该工具的功能

1. 如果 `~/ClawHealth`（或 `$CLAWHEALTH_INSTALL_DIR`）目录中尚不存在 **ClawHealth** 仓库，会将其克隆到该目录中。
2. 运行 `make deploy-openclaw` 命令：启动 Docker（包含 PostgreSQL、Redis 和 API 服务），执行数据迁移操作，生成示例数据，创建 API 密钥，并配置 MCP（中间件服务器）。
3. 将 **open-wearables** MCP 服务器的配置信息合并到您的 OpenClaw 配置文件（`~/.clawdbot/clawdbot.json5`）中，以便网关能够与 ClawHealth 通信。
4. 提醒用户重启 OpenClaw 网关。之后，用户需要通过安装 **ClawHealth iOS 应用**（该应用使用了我们发布的 SDK）并将 HealthKit 数据同步到后端，这样 OpenClaw 就可以查询他们的健康数据了。

## 适用场景

- 当用户表示想要“部署 ClawHealth”、“安装 ClawHealth”、“将健康数据连接到 OpenClaw”或“为 OpenClaw 配置 Open Wearables”时。
- 当用户已经拥有 OpenClaw 并希望助手能够查询他们的睡眠、活动或锻炼数据时。

## 运行步骤（对于代理端）

1. **检查环境**：确保系统上安装了 `docker`、`git`、`make` 和 `node` 工具。如果 Docker 未运行，请提示用户启动它。
2. 从该工具的目录中运行安装脚本：
   ```bash
   bash scripts/install.sh
   ```
   可选的环境变量：
   - `CLAWHEALTH_INSTALL_DIR`：用于克隆或使用仓库的路径（默认值：`~/ClawHealth`）。
   - `CLAWHEALTH_REPO_URL`：仓库的 URL（默认值：`https://github.com/the-momentum/open-wearables.git`）。
3. 重启 OpenClaw 网关，以便加载新的 MCP 服务器配置：
   ```bash
   clawdbot gateway restart
   ```
4. 告知用户接下来的两个步骤：
   - **链接数据**：安装 **ClawHealth iOS 应用**（该应用包含我们发布的 SDK），并登录或配置应用以连接到 ClawHealth 后端，从而实现 HealthKit 数据的同步。这样 OpenClaw 就可以查询用户的健康数据了。
   - **在聊天中测试**：在 OpenClaw（例如 Telegram/WhatsApp）中询问“我可以查询谁的健康数据？”或“我上周的睡眠情况如何？”（系统会立即显示示例数据；用户使用 iOS 应用后，他们自己的数据也会显示出来。）

## 数据链接方法（iOS 应用 + SDK）

我们通过 **iOS 应用** 帮助用户将健康数据连接到已部署的 ClawHealth 后端。该应用使用了我们发布的 SDK（支持 HealthKit 数据同步和安全的令牌交换机制）。部署完成后，建议用户按照以下步骤操作：

- **ClawHealth iOS 应用**：可以在 App Store 或 TestFlight 中下载该应用（或从 [ClawHealth 官网](https://github.com/the-momentum/open-wearables) 下载）。用户安装应用后登录或连接到他们的 ClawHealth 实例，然后进行数据同步；之后 OpenClaw 就可以查询这些数据了。
- **SDK 文档**：[Open Wearables 数据同步 SDK](https://docs.openwearables.io/sdk) 和 [Flutter SDK (iOS)](https://docs.openwearables.io/sdk/flutter) 为希望在自家应用中实现相同数据同步功能的开发者提供了详细指南。

## 如果用户已经在其他地方运行了 ClawHealth

用户可以手动添加 MCP 服务器：在他们的 ClawHealth 仓库中运行 `make deploy-openclaw` 命令以获取配置信息，然后将生成的 `mcp.servers["open-wearables"]` 配置段合并到 `~/.clawdbot/clawdbot.json5` 文件中。或者，他们也可以使用相同的安装脚本，只是将 `CLAWHEALTH_INSTALL_DIR` 指向他们已经克隆的仓库路径。

## 参考链接

- [ClawHealth / Open Wearables 仓库](https://github.com/the-momentum/open-wearables)
- [数据同步 SDK 及 iOS（Flutter SDK）](https://docs.openwearables.io/sdk)：介绍如何通过 iOS 应用实现数据同步
- [OpenClaw](https://openclaw.ai/)
- [ClawHub](https://clawhub.ai/)