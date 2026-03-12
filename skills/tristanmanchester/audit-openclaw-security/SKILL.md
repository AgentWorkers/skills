---
name: audit-openclaw-security
description: 审计并加强 OpenClaw 的部署环境，同时解读 `openclaw security audit` 的审计结果。此功能适用于用户希望增强 OpenClaw 的安全性、审查网关的暴露情况/身份验证机制/反向代理设置、Tailscale Serve 或 Funnel 的配置、检查私信/群组的访问权限（配对设置、允许列表、提及权限控制、`session.dmScope` 等设置）、限制工具的权限使用、实施沙箱隔离措施，以及审核插件、技能配置、密钥管理、日志保留策略等。此外，该功能还可用于锁定 Docker、macOS 或笔记本电脑上的 OpenClaw 安装环境。但不适用于与 OpenClaw 无关的通用操作系统、Docker 或云平台的常规安全加固需求。
license: MIT
compatibility: Best with local shell access (Claude Code, OpenClaw desktop/CLI, or a similar agent runtime). In chat-only environments, ask the user to run the bundled commands locally and share redacted outputs.
metadata: {"author":"community","version":"2.1.0","validated_for":"2026.3.8","upstream":"OpenClaw docs + Agent Skills guidance (validated 2026-03-11)"}
---
# audit-openclaw-security

对 OpenClaw 部署环境进行一次**防御性、有权限限制的安全审计**，并将审计结果转化为可行的修复计划。

本文档适用于 **OpenClaw 2026.3.8** 版本，在引用命令中的捆绑脚本时使用了 `{baseDir}`。

## 安全审计原则

1. **仅审计用户拥有权限或明确被允许评估的系统。**
2. **切勿索要原始敏感信息。** 不要请求网关令牌/密码、模型 API 密钥、会话 cookie、OAuth 凭据或原始凭证文件。
3. 优先选择可共享或已脱敏的输出结果：
   - `openclaw status --all`
   - `openclaw status --deep`
   - `openclaw gateway probe --json`
   - `openclaw security audit --json`
   - `openclaw security audit --deep --json`
4. 将 **网关**、**控制界面**、**浏览器控制**、**配对节点** 和 **自动化接口** 视为操作员级别的访问权限。
5. 默认设置为 **仅审计**。在修改任何配置、执行 `--fix` 操作、更改防火墙设置或重启之前，先创建备份并获取用户的明确批准。
6. 当用户需要修复措施时，明确执行备份操作：
   - `openclaw backup create --verify`
   - 如果配置无效但仍需要保留状态和凭证信息，使用 `--no-include-workspace`
   - 如果用户仅希望在修改前获取最小范围的配置信息，使用 `--only-config`

## “良好安全状态”的表现

- 除非有特殊且经过防护的理由，否则网关应绑定到 **loopback** 模式。
- 启用了强化的网关认证机制。
- 无意中的公开暴露（如 LAN 绑定、端口转发、过于宽松的反向代理设置、Tailscale Funnel 功能）。
- 控制界面要么绑定到本地主机（localhost/Serve），要么通过受信任的代理进行源地址限制。
- 私信（DM）需要配对或严格的允许列表控制。
- 组（groups）需要启用提及（mention）功能，并且在启用了广泛功能的工具情况下不应被公开访问。
- `session.dmScope` 设置得当：
  - 对于多用户环境，设置为 `per-channel-peer`
  - 如果同一提供者管理多个账户，则设置为 `per-account-channel-peer`
- 工具权限最小化：
  - 对面向收件箱的代理，设置 `tools.profile: "messaging"`
  - 在不受信任的接口上，禁止 `group:runtime`、`group:fs`、`group:automation`
  - 设置 `tools.fs_workspaceOnly: true`
  - `tools.exec.security: "deny"` 或至少需要审批才能使用
  - 除非有特殊需求，否则禁用 `tools.elevated.enabled`
- 插件和技能（skills）应经过明确授权，具有最小化的写入权限，且不能被用作数据持久化途径。
- 敏感信息、聊天记录和日志的访问权限受到严格控制，并有明确的保留策略。

## 逐步使用捆绑文件

仅打开执行任务所需的额外文件：

- `references/command-cheatsheet.md` — 完整的命令参考指南
- `references/openclaw-audit-checks.md` — 当前的高风险检查项词汇表
- `references/openclaw-baseline-config.md` — 安全基线配置示例
- `references/platform-mac-mini.md`
- `references/platform-personal-laptop.md`
- `references/platform-docker.md`
- `references/platform-aws-ec2.md`
- `assets/report-template.md` — 报告模板

## 第 0 步 — 快速了解环境

收集足够的背景信息以选择合适的审计路径：

- OpenClaw 运行在何处？
  - macOS 主机 / Mac mini
  - 个人笔记本电脑
  - Docker 主机
  - EC2 / VPS / 其他云虚拟机
- 安装方式是什么？
  - 原生安装
  - 使用 Docker 或 Compose 配置
  - 从源代码仓库拉取安装包
- 是否可以访问本地 shell？
  - **模式 A**：仅通过聊天界面进行审计 / 用户直接运行命令
  - **模式 B**：代理可以直接运行 shell 命令

## 模式 A — 辅助式自我审计（仅通过聊天界面）

要求用户在 OpenClaw 主机上运行以下命令，并分享审计结果。

### 最小审计集

```bash
openclaw --version
openclaw status --all
openclaw status --deep
openclaw gateway status
openclaw gateway probe --json
openclaw channels status --probe
openclaw doctor
openclaw security audit --json
openclaw security audit --deep --json
```

### 有用的附加工具

```bash
openclaw health --json
openclaw backup create --dry-run --json
openclaw backup create --only-config --dry-run --json
openclaw skills list --eligible --json
openclaw plugins list --json
```

### 安全的配置读取方式

建议优先读取特定配置项，而不是全部配置内容：

```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.allowTailscale
openclaw config get gateway.controlUi.allowedOrigins
openclaw config get gateway.trustedProxies
openclaw config get gateway.allowRealIpFallback
openclaw config get discovery.mdns.mode
openclaw config get session.dmScope
openclaw config get tools.profile
openclaw config get tools.fs.workspaceOnly
openclaw config get tools.exec.security
openclaw config get tools.elevated.enabled
openclaw config get channels.defaults.dmPolicy
openclaw config get channels.defaults.groupPolicy
openclaw config get logging.redactSensitive
```

### 私信/组消息的后续检查

如果问题表现为“机器人在线但私信或组消息功能异常”，请检查配对设置和提及（mention）功能：

```bash
openclaw pairing list <channel>
```

`<channel>` 的示例包括 `discord`、`slack`、`signal`、`telegram`、`whatsapp`、`matrix`、`imessage` 和 `bluebubbles`。

### 如果用户需要共享配置文件

OpenClaw 的配置文件通常采用 JSON5 格式。在共享前请对其进行脱敏处理：

```bash
python3 "{baseDir}/scripts/redact_openclaw_config.py" ~/.openclaw/openclaw.json > openclaw.json.redacted
```

### 主机/网络快照

**macOS**

```bash
whoami
sw_vers
uname -a
lsof -nP -iTCP -sTCP:LISTEN
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode
fdesetup status || true
```

**Linux / 云虚拟机**

```bash
whoami
cat /etc/os-release
uname -a
ss -ltnp
sudo ufw status verbose || true
sudo nft list ruleset || true
sudo iptables -S || true
```

**Docker / Compose**

```bash
docker ps --format 'table {{.Names}}	{{.Image}}	{{.Ports}}'
docker compose ps || true
docker port openclaw-gateway 18789 || true
```

## 模式 B — 自动化本地审计（具有 shell 访问权限）

运行捆绑提供的审计工具和报告生成工具：

```bash
bash "{baseDir}/scripts/collect_openclaw_audit.sh" --out ./openclaw-audit
python3 "{baseDir}/scripts/render_report.py" --input ./openclaw-audit --output ./openclaw-security-report.md
```

然后查看 `openclaw-security-report.md`，根据需要调整报告内容，并将最终报告呈现给用户。

### 关于审计工具的说明

- 该工具默认为 **只读** 模式。
- 它不会执行 `openclaw security audit --fix` 操作。
- 它收集可共享的 CLI 日志和基本的主机/网络信息。
- 它会捕获当前重要的审计数据，例如：
  - `openclaw status --deep`
  - `openclaw gateway probe --json`
  - `openclaw channels status --probe`
  - 安全的配置值读取
  - 备份操作的元数据

## 如何解读审计结果

以 OpenClaw 自带的审计输出作为主要依据，将其转化为清晰的威胁分析报告。

### 审计优先级

按照以下顺序处理问题：

1. **任何开放的功能和启用的工具**  
   首先限制私信/组消息功能，然后加强工具策略和沙箱安全。
2. **公共网络暴露**  
   如 LAN 绑定、反向代理设置不当、权限控制不足等问题。
3. **浏览器/节点/控制界面的访问权限**  
   这些应被视为操作员级别的访问权限，而不仅仅是普通功能。
4. **文件系统权限**  
   状态目录、配置文件、认证配置文件、日志和聊天记录的位置。
5. **插件和技能的权限管理**  
   仅允许由授权用户安装和使用的插件。
6. **模型和提示注入的防御能力**  
   虽然重要，但不能替代访问控制机制。

### 在新版本的 OpenClaw 中容易忽略的隐患

特别注意以下高风险检查项：

- `gateway.control_ui.allowed_origins_required`
- `gateway.control_ui.host_header_origin_fallback`
- `gateway.real_ip_fallbackenabled`
- `config.insecure_or_dangerous_flags`
- `sandbox.dangerous_network_mode`
- `tools.exec.host_sandbox_no_sandbox_defaults`
- `tools.exec.host_sandbox_no_sandbox_agents`
- `tools.exec.safeBins_interpreter_unprofiled`
- `skills_workspace.symlink_escape`
- `security.exposure.open_groups_with_elevated`
- `security.exposure.open_groups_with_runtime_or_fs`
- `security.trust_model.multi_user_heuristic`

使用 `references/openclaw-audit-checks.md` 和 `assets/openclaw_checkid_map.json` 将每个问题与可能的配置路径和修复措施对应起来。

## 核心修复方法

### 1) 网关暴露和认证

- 建议将网关绑定到 **loopback** 模式。
- 对于非本地使用的情况，要求使用令牌或密码进行认证。
- 不要将 `gateway.remote.*` 设置视为本地访问的防护措施；真正的防护应依赖于 `gateway.auth.*`。
- 如果用户需要新的共享凭证，使用 `openclaw doctor --generate-gateway-token` 命令来生成令牌。

### 2) 反向代理和浏览器源地址策略

如果网关前面有反向代理：
- 配置 `gateway.trustedProxies`
- 除非有特殊需求，否则保持 `gateway.allowRealIpFallback` 为 `false`
- 对于非 loopback 模式的控制界面，设置 `gateway.controlUi.allowedOrigins`
- 除非用户明确同意，否则不要启用 `gateway.auth.allowTailscale`

### 3) Tailscale Serve 与 Funnel 的区别

- `tailscale.mode: "serve"` 使网关仅用于内部网络。
- `tailscale.mode: "funnel"` 表示公开访问，属于高风险情况。
- `gateway.auth.allowTailscale` 允许通过 Tailscale 身份验证进行无令牌的 Control UI/WebSocket 访问，但这要求网关主机本身是可信的。
- 如果不受信任的代码可以在主机上运行，或者网关前面有反向代理，应禁用 `gateway.auth.allowTailscale`，并要求使用令牌/密码或受信任的代理进行认证。

### 4) 私信和组的隔离

- 对面向收件箱的机器人使用 `dmPolicy: "pairing"` 或 `allowlist` 进行控制。
- 对于共享或支持类型的收件箱，设置 `session.dmScope: "per-channel-peer"`。
- 对于多账户通道环境，建议使用 `per-account-channel-peer`。
- 除非工具功能非常有限，否则避免使用 `groupPolicy: "open"`。
- 对于组消息，需要启用提及（mention）功能，并使用 `agents.list[].groupChat.mentionPatterns` 进行控制。

### 5) 工具权限的优化

从 `references/openclaw-baseline-config.md` 中的保守配置开始设置。

面向用户的代理的默认安全配置：
- `tools.profile: "messaging"`
- 禁用 `group:automation`
- 禁用 `group:runtime`
- 禁用 `group:fs`
- 设置 `tools.fs_workspaceOnly: true`
- `tools.exec.security: "deny"` 并要求用户确认
- `tools.exec.applyPatch_workspaceOnly: true`
- 禁用 `tools.elevated.enabled`

### 6) 节点/浏览器/自动化的权限控制

- 配对节点被视为远程执行接口，应像对待操作员访问一样进行审计。
- 浏览器控制不仅仅是简单的页面浏览；实际上它代表了远程操作员的操作能力。
- `gateway` 和 `cron` 工具会创建持久化数据，不应从不受信任的聊天界面访问。

### 7) 敏感信息、日志和可写路径的权限管理

仔细审计这些路径，但不要请求原始内容：

- `~/.openclaw/openclaw.json`
- `~/.openclaw/secrets.json`
- `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- `~/.openclaw/agents/<agentId>/sessions/*.jsonl`
- `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 配置文件存储在 `~/.openclaw/credentials/` 目录下

## 平台特定的指导

根据实际环境选择相应的配置文件：

- macOS 主机 / Mac mini -> `references/platform-mac-mini.md`
- 个人笔记本电脑 -> `references/platform-personal-laptop.md`
- Docker / Compose -> `references/platform-docker.md`
- EC2 / VPS -> `references/platform-aws-ec2.md`

## 报告格式

使用 `assets/report-template.md` 或 `{baseDir}/scripts/render_report.py` 生成的报告。

最终报告应包括：
- 执行摘要
- 环境概述
- 带有敏感信息屏蔽的审计结果表
- 有序的修复计划
- 需要执行的修复命令
- 剩余风险和操作建议

## 故障排除提示

### “openclaw: command not found”

- 确认 CLI 已安装并添加到 `PATH` 环境变量中。
- 在 Windows 上，建议使用 WSL2 环境进行 shell 基本的审计操作。
- 重新运行官方的安装或更新命令，然后尝试 `openclaw --version`。

### “Gateway won’t start — configuration invalid”

OpenClaw 会在配置错误、值无效或类型不正确时自动停止运行。这是有意的设计，与安全性相关。

可以使用以下命令进行诊断：
```bash
openclaw doctor
openclaw doctor --fix
```

即使配置无效，`openclaw status`、`openclaw gateway status`、`openclaw gateway probe` 和 `openclaw health` 等诊断命令仍然有用。

### “Runtime: running” 但 “RPC probe: failed”

请关注诊断信息，而不仅仅是系统状态：
- `Probe target`
- `Listening`
- `Last gateway error`

这通常表示服务配置不一致、认证不匹配，或者监听器无法被 CLI 访问。

### “Bot is online but DMs fail”

检查以下内容：
```bash
openclaw channels status --probe
openclaw pairing list <channel>
```

常见原因包括：
- 配对请求未获批准
- `dmPolicy` 对预期发送者的限制过于严格
- 提供者端的权限或令牌设置不正确

### “Groups are silent”

检查以下配置：
- `groupPolicy`
- `requireMention`
- `mentionPatterns`
- 结合运行时/文件系统权限设置的审计结果

## 触发审计的提示（用于检查工具作者是否正确配置）

以下情况应触发审计：
- “你能对我的 OpenClaw 配置进行安全审计吗？”
- “我的 OpenClaw 网关通过 Tailscale Serve 暴露了，这安全吗？”
- “请解释 `openclaw security audit --deep --json` 的审计结果。”
- “我在 VPS 上使用 Docker 运行 OpenClaw，需要帮助加强安全性。”
- “我的 OpenClaw 控制界面出现了关于源地址和代理的问题。”
- “我的机器人在线但私信无法发送；你能检查配对设置和访问权限吗？”

以下情况不应触发审计：
- 与 OpenClaw 无关的 macOS 安全优化建议
- 与 OpenClaw 无关的 Docker 安全问题
- 与 OpenClaw 无关的 AWS 或 VPS 安全问题
- 与 OpenClaw 无关的其他软件审计任务