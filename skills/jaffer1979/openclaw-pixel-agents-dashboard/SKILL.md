---
name: pixel-agents
description: OpenClaw 部署的实时像素艺术操作控制面板：该面板以字符精灵的形式可视化代理的活动情况，同时显示实时活动信息、硬件监控数据、服务控制功能以及任务生成过程。
---
# Pixel Agents 仪表板

这是一个实时像素艺术操作仪表板，它将 OpenClaw 代理的活动以角色精灵的形式在共享办公环境中可视化。

## 设置（首次使用）

```bash
npm install
bash skill/scripts/setup.sh
npm run build
npm start
```

设置脚本会自动检测您的代理节点、找到网关，并生成配置文件。

或者，您也可以直接运行 `npm start` — 如果没有配置文件，设置向导会自动在您的浏览器中打开。

## 配置

请参阅 `dashboard.config.example.json` 以了解所有可配置的选项：

| 字段 | 描述 |
|-------|-------------|
| `server.port` | 仪表板端口号（默认：5070） |
| `gateway.url` | OpenClaw 网关的 URL |
| `gateway.token` | 网关认证令牌（使用 `${ENV_VAR}`） |
| `agents[]` | 代理节点的定义（ID、名称、表情符号、调色板） |
| `features.*` | 控制交互式元素的启用/禁用 |
| `remoteAgents[]` | 需要远程监控的 SSH 目标节点 |

## 故障排除

| 问题 | 解决方法 |
|---------|-----|
| 端口已被占用 | 更改 `server.port` 的值，或设置环境变量 `PIXEL_AGENTS_PORT` |
| 未显示代理节点 | 检查 `openclaw.agentsDir` 的路径是否正确 |
| 网关错误 | 验证 `gateway.url` 和 `gateway.token` 的值是否正确 |