---
name: teleport-tbot-bootstrap
description: 在 macOS 上，使用 LaunchAgent 和 tbot 配置一个持久的 Teleport 机器 ID（tbot）设置。当需要设置、自动化或验证本地 Teleport 机器人身份时，该设置会自动触发，包括处理代理/令牌/连接方式的输入信息、LaunchAgent 的持久化存储，以及首次运行时与 tsh 的验证。该功能补充了 teleport-tsh-ssh 技能，使得日常的 SSH/命令/SCP 操作能够使用更新后的身份信息进行。
---
# teleport-tbot-bootstrap

在 macOS 上设置一个本地的、持久的机器 ID 机器人，以便通过 OpenClaw/agent 进行 SSH 访问。  
将该机器人与 `teleport-tsh-ssh` 配合使用，在身份验证更新完成后，即可通过该机器人进行操作主机的访问。

## 兼容性  
已针对 Teleport/tbot **18.7.0** 进行测试。  

## 需要收集的输入信息：  
- Teleport 代理地址（例如 `teleport.example.com:443`）  
- 机器人的登录凭证（根据集群设置，可能是令牌或注册密钥）  
- 机器人的角色/名称（来自 Teleport 的配置信息）  
- 可选的输出目录（默认为 `~/.openclaw/workspace/tbot`）  

## LaunchAgent 的行为（macOS）  
使用 LaunchAgent 来保持用户会话的持久性：  
- 在用户登录时自动启动。  
- 当通过 `launchctl bootstrap gui/<uid> ...` 加载时立即启动。  
- 当 `KeepAlive` 设置为 `true` 时自动重启。  
- 如果安装在 `~/Library/LaunchAgents` 目录下，则不需要 root 权限。  
只有在系统需要全局 root 权限时，才使用 LaunchDaemon。  

## 工作流程：  
1. 确保满足以下前提条件：`tbot`、`tsh` 可写输出目录可用。  
2. 创建输出目录和状态目录（默认为 `~/.openclaw/workspace/tbot` 和 `~/.openclaw/workspace/tbot/state`）。  
3. 通过 `tbot configure identity` 生成配置文件（不要手动编写配置）：  
   - 目标路径应指向输出目录（`file://.../tbot`）。  
   - 存储路径应指向状态目录（`file://.../tbot/state`）。  
   - 设置代理和连接方法（推荐使用 `bound_keypair`）。  
   - 将配置文件写入 `~/.openclaw/workspace/tbot/tbot.yaml`。  
4. 创建 LaunchAgent 的 plist 文件，以便通过 `RunAtLoad` 和 `KeepAlive` 选项运行 `tbot start -c <config>`。  
5. 加载并启动 LaunchAgent。  
6. 验证身份验证输出文件是否存在且内容是最新的（位于 `.../tbot/identity`）。  
7. 使用 `tsh -i <identity> --proxy=<proxy> ls` 验证访问路径是否正确。  
8. 报告状态及后续步骤。  

## 关于 `bound_keypair` 的使用建议：  
- 建议使用 `bound_keypair` 连接方法，以便在系统中断（如睡眠或重启后）能够恢复连接。  
- 在适当的情况下，设置较高的恢复限制以确保连接的稳定性。  
- 首次设置时使用新的机器人状态目录；重复使用其他机器人或令牌的状态可能导致密钥匹配问题。  
- 先在 Teleport 端进行预注册（包括机器人角色、令牌等配置）。确保访问权限是按节点范围设置的（例如 `openclaw-allowed: "true"`），以实现按需访问。  
- 参见：  
  - `references/teleport-prereq-examples.yaml`  
  - https://goteleport.com/docs/reference/cli/tbot/  

## 安全注意事项：  
- 绝不要将登录凭证或注册密钥提交到 Git。  
- 将 `tbot.yaml`、机器人状态文件和身份验证输出文件视为敏感信息。  
- 建议使用安全的密钥传递方式（如交互式输入、密钥管理工具或环境变量注入），而非明文聊天记录。  

## 已知的限制（v1.0.0）：  
- 仅支持 SSH 身份验证相关的功能（不支持 Teleport 应用程序或 Kubernetes 的输出）。  
- 使用 LaunchAgent 的用户上下文；不提供完整的 LaunchDaemon 或 root 权限自动化功能。  

## 命令参考：  
- 生成配置文件：`tbot configure identity --output ~/.openclaw/workspace/tbot/tbot.yaml ...`  
- 单次启动（用于测试）：`tbot start -c ~/.openclaw/workspace/tbot/tbot.yaml`  
- 加载 LaunchAgent：`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.tbot.plist`  
- 重启 LaunchAgent：`launchctl kickstart -k gui/$(id -u)/com.openclaw.tbot`  

## Clawhub 的相关说明：  
### Clawhub 简介：  
使用 LaunchAgent 和 `tbot configure identity` 在 macOS 上设置一个持久的 Teleport 机器 ID（`tbot`）身份。  

### 配合使用说明：  
与 `teleport-tsh-ssh` 结合使用，以便使用更新后的身份进行日常的 SSH 或 SCP 操作。  

### Clawhub 详细说明：  
- 设置一个本地的、持久的机器 ID 机器人，用于自动化操作。  
- 使用 `tbot configure identity` 生成配置文件，安装用户 LaunchAgent（`com.openclaw.tbot`），并通过 `tsh` 进行身份验证测试。  
- 支持 LaunchAgent 的持久性功能（无需 root 权限），支持使用 `bound_keypair` 进行连接；提供预注册示例（包括角色、机器人和令牌配置），以及按节点范围设置访问权限的指导。  

## 相关资源：  
- 设置脚本：`scripts/bootstrap_tbot_launchagent.sh`  
- Teleport 配置示例：`references/teleport-prereq-examples.yaml`  
- LaunchAgent 模板说明：`references/launchagent-notes.md`  

## 卸载/清理步骤：  
- 卸载 LaunchAgent：`launchctl bootout gui/$(id -u)/com.openclaw.tbot`  
- 删除相关文件：`rm -f ~/Library/LaunchAgents/com.openclaw.tbot.plist`  
- 如需，可删除机器人文件：`rm -rf ~/.openclaw/workspace/tbot`