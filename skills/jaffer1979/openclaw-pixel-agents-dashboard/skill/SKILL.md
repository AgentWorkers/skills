---
name: pixel-agents
description: 安装、配置并管理 Pixel Agents 控制面板——这是一个专为 OpenClaw 部署设计的实时像素艺术操作控制面板。当用户需要设置、启动、停止、配置或排查 Pixel Agents 控制面板的相关问题时，可以使用该工具。该工具支持自动发现本地代理、管理网关连接、生成配置文件以及进行服务管理。
---
# Pixel Agents 仪表板

这是一个实时像素艺术操作仪表板，它以角色精灵的形式在共享办公环境中可视化 OpenClaw 代理的运行状态。

## 设置（首次使用）

运行自动配置脚本以发现代理并生成配置文件：

```bash
bash scripts/setup.sh
```

该脚本将执行以下操作：
1. 查找您的 OpenClaw 代理目录（`~/.openclaw/agents/`）
2. 检测网关的 URL 和端口
3. 发现所有已配置的代理
4. 生成 `dashboard.config.json` 文件
5. 安装依赖项并构建相关资源

如果无法自动发现代理或网关，脚本会使用默认值生成配置文件，然后设置向导会完成其余的设置工作。

## 启动/停止

```bash
# Start the dashboard
cd <project-dir> && npm start

# Or if installed globally
pixel-agents
```

默认端口：5070。您可以通过设置环境变量 `PIXEL_AGENTS_PORT` 来更改端口。

## 配置

配置文件：`dashboard.config.json`（位于项目根目录或 `~/.config/pixel-agents/`）

关键设置：
- `gateway.url` — OpenClaw 网关地址（默认值：`http://localhost:18789`）
- `gateway.token` — 使用环境变量 `${OPENCLAW_GATEWAY_TOKEN}` 进行配置
- `agents[]` — 一个包含代理信息的数组（格式：`{id, name, emoji, palette, alwaysPresent}`）
- `features` — 控制是否显示某些组件（如：serverRack、breakerPanel、hamRadio、fireAlarm 等）

请参阅 `dashboard.config.example.json` 以获取完整的配置示例。

## 故障排除

| 问题 | 解决方案 |
|-------|-----|
| 端口已被占用 | 将 `PIXEL_AGENTS_PORT` 设置为 5071，或修改配置文件中的 `server.port` |
| 未找到代理 | 确保 `openclaw.agentsDir` 指向正确的路径 |
| 无法访问网关 | 验证网关是否正在运行：`curl http://localhost:18789/v1/models` |
| 精灵显示不完整 | 运行 `npm run build` 命令——资源文件位于 `public/assets/` 目录下 |