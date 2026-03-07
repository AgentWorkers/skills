---
name: owletto-openclaw
description: 安装并配置 OpenClaw 的 Owletto 内存插件，包括 OAuth 登录功能以及 MCP（Memory Control Panel）的健康状态验证功能。
---
# Owletto OpenClaw 设置

当用户希望将 Owletto 的长期记忆功能集成到 OpenClaw 中时，请使用此技能。

## 设置流程

1. 确保已具备使用 CLI 的前提条件。

```bash
node --version
pnpm --version
owletto --help
```

2. 安装 OpenClaw 插件包。

```bash
openclaw plugins install owletto-openclaw-plugin
```

3. 登录到 Owletto 以获取 MCP（Memory Control Platform）访问权限。

```bash
owletto openclaw login --mcpUrl https://owletto.com/mcp
```

4. 配置 OpenClaw 插件的相关设置。

```bash
owletto openclaw configure --mcpUrl https://owletto.com/mcp
```

5. 验证身份验证及 MCP 连接是否正常。

```bash
owletto openclaw health --mcpUrl https://owletto.com/mcp
```

## 注意事项

- 对于自托管环境或非默认环境，请将 `https://owletto.com/mcp` 替换为实际的 MCP URL。
- 如果 `openclaw` 未添加到系统的 PATH 环境变量中，请先安装 OpenClaw 的 CLI，然后再重新执行设置流程。
- 如果无法通过浏览器登录，请在其他机器或浏览器上完成 OAuth 验证，之后通过具有浏览器访问权限的 shell 重新执行设置流程。