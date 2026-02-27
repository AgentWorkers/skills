<skill>
  <id>clawbridge</id>
  <name>ClawBridge 仪表板</name>
  <version>1.0.0</version>
  <description>专为 OpenClaw 代理设计的移动优先任务控制工具。作为本地 Node.js 侧车进程运行，提供 Web 仪表板以实时监控代理活动、追踪 340 多种模型的代币使用情况，并远程触发定时任务。可选地，可创建仅用于出站的 Cloudflare 隧道以实现远程访问。</description>
  <author>DreamWing</author>
  <homepage>https://clawbridge.app</homepage>
  <license>MIT</license>
  <tags>仪表板、监控、移动设备、用户界面、控制面板、成本追踪、Cloudflare、隧道</tags>

  <!-- 该技能的安装与运行方式 -->
  <runtime>
    <type>node</type>
    <entrypoint>index.js</entrypoint>
    <persistence>注册一个用户级别的 systemd 服务（clawbridge.service），该服务在登录时自动启动并在失败时重启。</persistence>
  </runtime>

  <!-- 系统要求 -->
  <requires>
    <dependency name="node" version=">=18" required="true" />
    <dependency name="npm" version=">=9" required="true" />
    <dependency name="git" version="any" required="false" description="用于增量更新；如果未安装 git，则会回退到 tarball 下载。"
    <dependency name="cloudflared" version="latest" required="false" description>如果启用 Cloudflare 隧道，则会自动从 github.com/cloudflare/cloudflared 下载。仅在没有 VPN（如 Tailscale/WireGuard）的情况下使用远程访问时需要。"
  </requires>

  <!-- 需要配置的凭据/环境变量（保存在 .env 文件中） -->
  <credentials>
    <env name="ACCESS_KEY" description>用于登录仪表板的随机生成的 32 位十六进制密钥。首次安装时自动生成。</description>
    <env name="PORT" description>仪表板监听的本地 TCP 端口。默认为 3000，如果已被占用则会自动递增。</description>
    <env name="TUNNEL_TOKEN" description>用于永久性隧道的 Cloudflare 隧道令牌。可选——省略该参数可使用临时快速隧道。</description>
    <env name="ENABLE_EMBEDDED_TUNNEL" description>当 Cloudflare 隧道（永久性或快速隧道）处于活动状态时设置为 'true'。</description>
    <env name="OPENCLAW_PATH" description>OpenClaw 可执行文件的绝对路径。会从 PATH 变量中自动检测；如果找到该文件，则会保存到 .env 中。</description>
  </credentials>

  <!-- 网络配置 -->
  <network>
    <connection purpose="依赖项安装" destination="registry.npmjs.org" direction="出站" trigger="安装/更新" />
    <connection purpose="源代码下载" destination="github.com/dreamwing/clawbridge" direction="出站" trigger="安装/更新" />
    <connection purpose="下载 cloudflared 可执行文件" destination="github.com/cloudflare/cloudflared" direction="出站" trigger="仅在未找到 cloudflared 时安装。"
    <connection purpose="Cloudflare 隧道中继" destination="*.cloudflareaccess.com, *.trycloudflare.com" direction="出站" trigger="仅在启用隧道时触发。"
    <connection purpose="仪表板 UI" destination="localhost" direction="入站" trigger="运行时" />
  </network>

  <!-- 文件系统路径的读写操作 -->
  <filesystem>
    <path type="写入" location="skills/clawbridge/.env" description>保存 ACCESS_KEY、PORT 以及可选的隧道配置信息。</path>
    <path type="写入" location="skills/clawbridge/data/" description>存储本地代理日志和代币使用情况数据。</path>
    <path type="写入" location="~/.config/systemd/user/clawbridge.service" description>保存用户级别的 systemd 服务配置文件。</path>
    <path type="写入" location="skills/clawbridge/cloudflared" description>仅在使用隧道时保存 cloudflared 可执行文件。</path>
  </filesystem>

  <!-- 安装方法——使用此仓库中提供的脚本**
  <install>
    curl -sL https://raw.githubusercontent.com/dreamwing/clawbridge/master/install.sh | bash
  </install>

  <instructions>
    ClawBridge 会作为持久化的后台服务进行安装。

    安装完成后，可以通过终端输出显示的本地 IP 地址访问仪表板。
    系统会生成一个随机生成的 `ACCESS_KEY`，请妥善保管该密钥，因为它用于登录。

    要启用远程访问（可选），请在提示时提供 Cloudflare 隧道令牌；如果不提供，则会使用临时快速隧道 URL。

    要更新到最新版本：
      curl -sL https://raw.githubusercontent.com/dreamwing/clawbridge/master/install.sh | bash

    要停止服务：
      systemctl --user stop clawbridge

    完整文档：https://github.com/dreamwing/clawbridge/blob/master/README.md
  </instructions>
</skill>

# ClawBridge 仪表板

**将您的代理功能随身携带。**

ClawBridge 是一个专为 OpenClaw 设计的轻量级、以移动设备为主的 Web 仪表板。它作为本地侧车进程运行，提供以下功能：
- 🧠 **实时活动监控**：通过 WebSocket 功能实时查看代理的执行情况和运行状态。
- 💰 **代币管理**：追踪 340 多种模型的代币使用情况，并提供每日/每月的详细统计。
- 🚀 **任务控制**：可通过手机手动触发定时任务。
- 🔒 **默认安全设置**：支持 API 密钥认证、会话 cookie，以及可选的 Cloudflare 隧道以实现远程访问。

## 该技能的功能
1. 从 GitHub 安装 ClawBridge Node.js 应用程序到 `skills/clawbridge/` 目录。
2. 生成一个随机的 `ACCESS_KEY` 并将其保存到 `.env` 文件中。
3. 注册一个用户级别的 systemd 服务以实现自动启动。
4. （可选）下载 `cloudflared` 并配置远程访问所需的隧道。

## 安装步骤

```bash
curl -sL https://raw.githubusercontent.com/dreamwing/clawbridge/master/install.sh | bash
```

请参阅 [README.md](https://github.com/dreamwing/clawbridge/blob/master/README.md) 以获取完整安装说明。