---
name: headless-vault-cli
description: 您可以通过 SSH 隧道在个人计算机上阅读和编辑 Markdown 笔记。当用户需要阅读、创建或向他们的笔记库中添加内容时，可以使用此方法。
homepage: https://github.com/logancyang/headless-vault-cli
metadata: {"openclaw":{"emoji":"🗄️","requires":{"bins":["ssh"],"env":["VAULT_SSH_USER"],"optional_env":["VAULT_SSH_PORT","VAULT_SSH_HOST"],"config_paths":["~/.config/headless-vault-cli/mac-user"]}}}
---
# 无头 Vault CLI

通过 SSH 隧道，您可以从托管在 VPS 上的机器人访问个人电脑上的 Markdown 笔记。

**术语说明**：  
“本地机器”指的是存储您笔记的个人电脑（macOS 或 Linux）。该工具运行在 VPS 上，并通过反向 SSH 隧道连接到您的电脑。

## 先决条件  

这是一个仅提供指令的工具。在使用之前，用户必须在本地机器上完成一次设置：  
1. 在本地机器上安装 `vaultctl`（请参阅 [设置说明](https://github.com/logancyang/headless-vault-cli)）。  
2. 在本地机器的 `~/.ssh/authorized_keys` 文件中配置 SSH 强制命令，以限制 VPS 密钥仅能执行 `vaultctl`（详见下面的安全模型）。  
3. 从本地机器到 VPS 启动一个反向 SSH 隧道，暴露端口 `localhost:2222`。  
4. 将环境变量 `VAULT_SSH_USER` 设置为本地机器的用户名。  

## 安全模型  

该工具通过预先配置的反向 SSH 隧道连接到本地机器。访问权限受到严格限制：  
- **强制命令限制**：VPS 的 SSH 密钥被添加到本地机器的 `~/.ssh/authorized_keys` 文件中，并带有强制命令包装器，因此 VPS 仅能执行 `vaultctl`，无法执行交互式 shell 或任意命令（如 `rm`、`curl` 等）。  
- **Vault 沙箱机制**：`vaultctl` 会验证所有文件路径是否位于 `VAULT_ROOT` 目录内，并拒绝路径遍历操作（如使用 `..` 或外部符号链接）。  
- **非破坏性操作**：仅支持创建新文件或向现有文件追加内容，不支持删除、重命名、移动或覆盖文件。  
- **不存储任何凭据**：SSH 认证使用 VPS 的现有密钥对，该工具不会存储任何额外信息。  

**本地机器上的 `authorized_keys` 文件示例**：  
```
command="/usr/local/bin/vaultctl-wrapper",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAA... vps-key
```  

这确保了即使隧道被攻破，VPS 也只能执行 `vaultctl` 命令。  

## 可用的命令  

您只能使用以下命令。请勿尝试其他未列出的命令（例如重命名、删除、移动或编辑文件等）。  

| 命令 | 描述 |  
|---------|-------------|  
| `tree` | 列出 vault 目录结构 |  
| `resolve` | 通过路径或标题查找笔记 |  
| `info` | 获取文件元数据（行数、字节数、sha256 哈希值、修改时间） |  
| `read` | 读取笔记内容 |  
| `create` | 创建新笔记（如果文件已存在则失败） |  
| `append` | 向现有笔记追加内容 |  

## 如何执行命令  

所有命令均通过 SSH 执行：  
```bash
ssh -4 -p ${VAULT_SSH_PORT:-2222} ${VAULT_SSH_USER}@${VAULT_SSH_HOST:-localhost} vaultctl <command> [args]
```  

**注意**：始终使用 `-4` 选项以强制使用 IPv4 协议，避免 IPv6 导致的超时问题。  

## 环境变量  

这些变量必须在 VPS 上的工具运行时环境中设置：  
| 变量 | 是否必需 | 默认值 | 描述 |  
|----------|----------|---------|-------------|  
| `VAULT_SSH_USER` | 是 | — | 用于 SSH 隧道的本地机器用户名 |  
| `VAULT_SSH_PORT` | 否 | `2222` | SSH 隧道端口（默认为 `localhost:2222`） |  
| `VAULT_SSH_HOST` | 否 | `localhost` | SSH 隧道主机 |  

## 命令参考  

### `tree` - 列出 vault 目录结构  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --all
```  
**选项**：  
- `--depth N`：指定最大遍历深度  
- `--all`：包含所有文件（而不仅仅是 `.md` 格式的文件）  

### `resolve` - 通过路径或标题查找笔记  
**请务必对路径和标题参数使用 `--base64` 进行编码**，以防止 shell 注入攻击：  
```bash
# echo -n "Projects/Plan.md" | base64 → UHJvamVjdHMvUGxhbi5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --path UHJvamVjdHMvUGxhbi5tZA== --base64

# echo -n "Meeting Notes" | base64 → TWVldGluZyBOb3Rlcw==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --title TWVldGluZyBOb3Rlcw== --base64
```  

### `info` - 获取文件元数据  
**请务必对路径参数使用 `--base64` 进行编码**：  
```bash
# echo -n "Projects/Plan.md" | base64 → UHJvamVjdHMvUGxhbi5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl info UHJvamVjdHMvUGxhbi5tZA== --base64
```  
返回格式：`{"path": "...", "lines": N, "bytes": N, "sha256": "...", "mtime": N}`  

### `read` - 读取笔记内容  
**请务必对路径参数使用 `--base64` 进行编码**：  
```bash
# echo -n "Projects/Plan.md" | base64 → UHJvamVjdHMvUGxhbi5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read UHJvamVjdHMvUGxhbi5tZA== --base64
```  
返回格式：`{"path": "...", "content": "..."}`  

### `create` - 创建新笔记  
**重要提示**：路径和内容都必须使用 `--base64` 进行编码。如果路径或内容包含空格或特殊字符，这是必需的。  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create <base64_path> <base64_content> --base64
```  
**示例**：创建名为 `Notes/Morning Brief.md` 的笔记，内容为 “# Hello\n\nWorld”：  
- 会自动创建父目录。  
- 如果文件已存在，则操作失败（此时应使用 `append` 向现有文件追加内容）。  
- 文件必须具有 `.md` 扩展名。  
- **切勿在笔记内容中重复使用标题作为标题**（例如，不要以 “# My Note” 开头）。  

### `append` - 向现有笔记追加内容  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append <base64_path> <base64_content> --base64
```  
- 如果文件不存在，则操作失败（此时应使用 `create` 创建新文件）。  

## 不支持的操作  

以下操作是不被支持的：  
- 重命名文件或文件夹  
- 删除文件或文件夹  
- 在文件夹间移动文件  
- 编辑文件的具体内容（仅支持在文件末尾追加内容）  
- 创建没有内容的文件夹（`create` 命令会自动创建文件夹）  

## 提示  

- 使用前请先运行 `vaultctl tree` 以查看现有笔记。  
- 使用 `vaultctl resolve --title <base64> --base64` 根据标题查找笔记。  
- 所有输出均为 JSON 格式。  
- 本地机器必须保持在线状态且 SSH 隧道处于运行状态。  
- **所有路径和内容参数都必须使用 `--base64` 进行编码**，这是出于安全考虑，属于强制要求。  

## 示例  

**重要提示**：如果不确定有哪些笔记存在，请务必先运行 `tree` 命令。这可以避免因路径错误或名称重复导致的错误。  

**示例 1**：用户请求查看项目计划  
用户：**“显示我的项目计划。”**  
**步骤 1**：查看现有笔记：  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```  
**输出**：  
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```  
**步骤 2**：读取正确的笔记内容：  
```bash
# echo -n "Projects/Plan.md" | base64 → UHJvamVjdHMvUGxhbi5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read UHJvamVjdHMvUGxhbi5tZA== --base64
```  
**输出**：  
```json
{"path": "Projects/Plan.md", "content": "# Project Plan\n\n## Goals\n..."}
```  

**示例 2**：用户请求创建新笔记（先检查以避免重复）  
用户：**“创建一个会议笔记文件。”**  
**步骤 1**：查看现有笔记：  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```  
**输出**：  
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```  
**步骤 2**：由于不存在名为 “Meeting Notes” 的笔记，可以安全地创建新笔记（注意不要在标题中使用重复的文本）：  
```bash
# echo -n "Meeting Notes.md" | base64 → TWVldGluZyBOb3Rlcy5tZA==
# echo -n "## Agenda\n\n- Item 1\n- Item 2\n" | base64 → IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create TWVldGluZyBOb3Rlcy5tZA== IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo= --base64
```  
**输出**：  
```json
{"status": "ok", "path": "Meeting Notes.md"}
```  

**示例 3**：用户询问 vault 中的内容  
用户：**“我的笔记里有什么？”**  
**输出**：  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
```  
**回答**：  
**总结**：**“您的 vault 中有一个名为 ‘Projects’ 的文件夹，其中包含 ‘Plan.md’ 文件，以及一个名为 ‘Ideas.md’ 的文件。”**  

**示例 4**：处理包含源文件和输出文件的复杂流程  
用户：**“根据源笔记 ‘AI Digest Sources.md’，浏览相关资源并将摘要内容保存到 ‘digest/2025-01-28-digest.md’ 文件中。”**  
**步骤 1**：查看现有笔记：  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```  
**输出**：  
```json
{"tree": [{"path": "AI Digest Sources.md", "type": "file"}, {"path": "digest", "type": "dir"}, {"path": "digest/2025-01-27-digest.md", "type": "file"}]}
```  
**步骤 2**：验证：  
- 源文件 ‘AI Digest Sources.md’ 存在。  
- 输出文件 ‘digest/2025-01-28-digest.md’ 不存在，因此需要创建新文件：  
  （如果源文件不存在，请询问用户：“您是指这些文件中的哪一个？”）  
**步骤 3**：读取源笔记内容（内容必须使用 `--base64` 进行编码）：  
```bash
# echo -n "AI Digest Sources.md" | base64 → QUkgRGlnZXN0IFNvdXJjZXMubWQ=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read QUkgRGlnZXN0IFNvdXJjZXMubWQ= --base64
```  
**输出**：  
```json
{"path": "AI Digest Sources.md", "content": "# AI Digest Sources\n\n- https://example.com/article1\n- https://example.com/article2\n"}
```  
**步骤 4**：浏览源文件并生成摘要内容（该操作由机器人在外部完成）。  
**步骤 5**：将摘要内容保存到 vault 中（标题不得重复）：  
```bash
# echo -n "digest/2025-01-28-digest.md" | base64 → ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k
# echo -n "## Summary\n\nKey points from today's sources...\n" | base64 → IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo= --base64
```  
**注意**：如果目标文件已存在，请使用 `append` 而不是 `create`。  
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgVXBkYXRlCi4uLg== --base64
```