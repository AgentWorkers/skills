---
name: teleport-tsh-ssh
description: 使用 Teleport 的 tsh CLI，结合机器 ID（tbot）身份文件，可以通过 SSH 连接到由 Teleport 管理的主机，或通过 Teleport 的访问控制机制执行远程命令。当需要连接到 Teleport 主机时，可以触发该功能；在 Teleport 节点上执行命令；或者使用由 tbot 更新的身份文件来排查 tsh 访问问题。该功能与 teleport-tbot-bootstrap 技能配合使用，用于创建和持久化本地机器 ID 身份信息。
---
# teleport-tsh-ssh

此技能用于通过 `tsh` 命令访问 Teleport SSH 节点，并支持使用明确的身份文件（`-i` 参数）以及持久化的代理设置。

请将其与 `teleport-tbot-bootstrap` 技能配合使用，以设置并维护本地的机器 ID 身份信息。

## 兼容性

已在 Teleport/tsh/tbot **18.7.0** 版本上进行了测试。

## 身份验证要求

在使用 `tsh` 命令时，必须始终传递 `-i <identity-file>` 参数。

默认的身份文件路径为：
- `~/.openclaw/workspace/tbot/identity`

如果默认路径不存在，系统会自动查找工作区内的身份文件，并使用最匹配的文件。

## 身份文件查找机制

当默认身份文件缺失时，系统会在工作区内搜索以下格式的文件：
- `identity`
- `*.identity`
- `tbot/identity`

在使用前，请验证这些文件的格式。一个有效的 Teleport 机器 ID 身份文件通常包含以下内容：
- `-----BEGIN PRIVATE KEY-----`
- 一个 OpenSSH 用户证书行（例如：`*-cert-v01@openssh.com ...`)
- 一个或多个 `-----BEGIN CERTIFICATE-----` 块

系统会优先选择最新的、格式正确的文件（优先考虑位于 `tbot/` 目录下的文件）。

## 安全注意事项

- 严禁提交身份文件、机器人状态目录、令牌或注册密钥。
- 在自动化场景中，建议使用明确的文件路径和最小权限的角色映射。

## 已知限制（v1.0.0）

- 仅支持访问 Teleport SSH 节点（`tsh ssh`、`tsh ls`、`tsh scp`）。
- 不支持访问 Teleport 应用程序或 Kubernetes 数据库。

## 代理设置

代理的解析顺序如下：
1. 如果设置了 `TELEPORT_PROXY` 环境变量，请使用该代理。
2. 如果未设置，则从 `~/.openclaw/workspace/tbot/proxy`（单行文本文件）中读取已保存的代理地址。
3. 如果代理地址未设置，系统会提示用户输入代理地址，并将其保存到 `~/.openclaw/workspace/tbot/proxy` 文件中以供后续使用。

在所有使用代理的 `tsh` 命令中，务必包含代理地址，例如：
- `tsh -i <identity> --proxy=<proxy> ...`

## 快速使用流程

1. 确保已安装 `tsh`。
2. 查找身份文件的路径（先尝试默认路径，再使用备用机制）。
3. 如果未找到有效的身份文件，提示用户提供文件路径。
4. 设置代理地址（先使用 `TELEPORT_PROXY`，再使用已保存的代理地址）。
5. 在需要时检查身份验证状态：`tsh -i <identity> --proxy=<proxy> status`。
6. 如需列出可用节点，执行 `tsh -i <identity> --proxy=<proxy> ls`。
7. 使用指定的身份文件和代理地址连接或执行命令：
   - `tsh -i <identity> --proxy=<proxy> ssh <host>`
   - `tsh -i <identity> --proxy=<proxy> ssh <host> -- <command> [args...]`
8. 返回简洁的结果以及详细的错误信息。

## 命令示例

- 交互式 shell：
  - `tsh -i <identity> --proxy=<proxy> ssh <host>`
- 远程命令执行：
  - `tsh -i <identity> --proxy=<proxy> ssh <host> -- <command> [args...]`
- 设置远程登录用户：
  - `tsh -i <identity> --proxy=<proxy> ssh <login>@<host>`
  - 或 `tsh -i <identity> --proxy=<proxy> ssh --login=<login> <host>`
- 列出可用节点：
  - `tsh -i <identity> --proxy=<proxy> ls`

如果用户询问可用节点，请执行 `tsh ls` 并返回结果。

当用户需要命令输出时，建议使用非交互式模式。

## 使用 Teleport SCP 复制文件

使用 `tsh scp` 命令进行文件传输，语法与 OpenSSH 的 `scp` 命令相同：
- 从本地复制到远程：`tsh -i <identity> --proxy=<proxy> scp <local_path> <host>:<remote_path>`
- 从远程复制到本地：`tsh -i <identity> --proxy=<proxy> scp <host>:<remote_path> <local_path>`

## 故障排除指南

- 如果出现 “`tsh: command not found`” 错误，请安装 Teleport 客户端。
- 如果身份文件缺失或无法读取，请尝试备用文件；如果仍未找到文件，请询问用户文件路径。
- 如果代理地址缺失，请询问用户并提供正确的代理地址，然后重新尝试。
- 如果出现 “未登录” 或证书过期的问题，请刷新机器 ID 信息（检查 tbot 服务状态）。
- 如果出现 “访问被拒绝” 的错误，请检查角色/登录信息是否正确，并验证主机和身份文件的来源。
- 如果找不到目标主机，请使用 `tsh -i <identity> --proxy=<proxy> ls` 命令进行验证。

## Clawhub 相关说明

### Clawhub 简介

使用 `tsh` 命令（并指定 `-i` 参数以提供机器 ID 身份信息），可以执行 Teleport SSH 操作、远程命令、列出节点以及使用 `tsh scp` 进行文件传输。

### 配合使用建议

建议与 `teleport-tbot-bootstrap` 技能结合使用，以创建并维护本地的机器 ID 身份信息。

### Clawhub 详细说明

该技能实现了以下功能：
- 通过明确的身份验证机制标准化对 Teleport 服务器的访问流程。
- 强制使用身份验证信息。
- 一致地解析代理地址。
- 支持主机查找、命令执行以及文件传输功能，并提供实用的故障排除指导。

## 参考资料

- `references/tsh-ssh-reference.md`
- https://goteleport.com/docs/reference/cli/tsh/#tsh-ssh