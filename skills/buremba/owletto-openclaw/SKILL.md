---
name: owletto-openclaw
description: 安装并配置 OpenClaw 的 Owletto 内存插件，包括 OAuth 登录功能以及 MCP（Memory Control Panel）的健康状态验证功能。
---
# Owletto OpenClaw 设置

当用户希望 Owletto 的长期记忆功能在 OpenClaw 中正常工作时，请使用此技能。

## 设置流程

1. 确保已具备 CLI（命令行界面）的运行环境。

```bash
node --version
pnpm --version
owletto --help
```

2. 安装 OpenClaw 插件包。

```bash
openclaw plugins install owletto-openclaw-plugin
```

3. 登录 Owletto 以获取 MCP（内存控制）访问权限。

```bash
owletto login --mcpUrl https://owletto.com/mcp
```

4. 配置 OpenClaw 插件设置。

```bash
owletto configure --mcpUrl https://owletto.com/mcp/acme
```

5. 验证身份验证及 MCP 连接是否正常。

```bash
owletto health --mcpUrl https://owletto.com/mcp/acme
```

## 直接使用 CLI

设置完成后，可以直接通过 CLI 与 Owletto 进行交互：

- `owletto mcp tools` — 列出可用的工具
- `owletto mcp call <tool> --params '<json>'` — 调用任意工具
- `owletto token --raw` — 获取用于脚本编写的 bearer token（令牌）

示例：
- `owletto mcp call search --params '{"query":"spotify"}'`
- `owletto mcp call save_content --params '{"entity_id":1,"content":"user prefers dark mode","metadata":{}}'`
- `owletto mcp call get_content --params '{"query":"user preferences","limit":5}'`

## 注意事项

- 对于自托管环境或非默认环境，请将 `https://owletto.com/mcp/acme` 替换为目标 MCP 的 URL。
- 如果 `openclaw` 未添加到系统的 PATH 环境变量中，请先安装 OpenClaw CLI，然后再重新执行设置步骤。
- 如果无法通过浏览器登录，请在其他机器或浏览器上完成 OAuth 认证，之后再通过支持浏览器的 shell 重新执行设置步骤。