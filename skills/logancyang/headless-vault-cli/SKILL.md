---
name: headless-vault-cli
description: 您可以通过 SSH 隧道在个人电脑上阅读和编辑 Markdown 笔记。当用户需要阅读、创建或向他们的笔记库中添加内容时，可以使用此方法。
homepage: https://github.com/logancyang/headless-vault-cli
metadata:
  category: productivity
  interface: CLI
  capabilities:
    - ssh
  dependencies: []
openclaw:
  emoji: "🗄️"
  install:
    env:
      - VAULT_SSH_USER
  requires:
    env:
      - VAULT_SSH_USER
    optional_env:
      - VAULT_SSH_PORT
      - VAULT_SSH_HOST
---
# 无头 Vault CLI

通过 SSH 隧道，您可以从托管在 VPS 上的机器人访问个人电脑上的 Markdown 笔记。

**术语说明**：“本地机器”指的是存储您笔记的个人电脑（macOS 或 Linux）。该功能在 VPS 上运行，并通过反向 SSH 隧道连接到您的本地机器。

## 先决条件

这是一个仅提供指令的功能。在使用之前，用户必须在本地机器上完成一次设置：

1. 在本地机器上安装 `vaultctl`（请参阅 [设置说明](https://github.com/logancyang/headless-vault-cli)）。
2. 在本地机器的 `~/.ssh/authorized_keys` 中配置 SSH 强制命令，以限制 VPS 密钥仅能执行 `vaultctl`（详见下面的安全模型）。
3. 从本地机器到 VPS 启动一个反向 SSH 隧道，暴露端口 `localhost:2222`。
4. 将环境变量 `VAULT_SSH_USER` 设置为本地机器的用户名。

## 安全模型

该功能通过预先配置的反向 SSH 隧道连接到本地机器。访问受到以下限制：

- **强制命令限制**：VPS 的 SSH 密钥被添加到本地机器的 `~/.ssh/authorized_keys` 中，并带有强制命令包装器，因此 VPS 仅能执行 `vaultctl`——无法执行交互式 shell 或任意命令（如 `rm`、`curl` 等）。
- **Vault 沙箱机制**：`vaultctl` 会验证所有文件路径是否位于 `VAULT_ROOT` 内部，并拒绝路径遍历尝试（例如使用 `..` 或外部符号链接）。
- **非破坏性操作**：仅支持创建新文件（`create`）和向现有文件追加内容（`append`）——不支持删除、重命名、移动或覆盖文件。
- **不存储任何凭证**：SSH 认证使用 VPS 的现有 SSH 密钥对；该功能不会存储任何额外的敏感信息。

**本地机器上的 `authorized_keys` 示例条目**：
```
command="/usr/local/bin/vaultctl-wrapper",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAA... vps-key
```

这确保了即使隧道被攻破，VPS 也只能执行 `vaultctl` 命令。

## 可用的命令

您只能使用以下命令。请勿尝试未列出的命令（例如：重命名、删除、移动或编辑文件）。

| 命令 | 描述 |
|---------|-------------|
| `tree` | 列出 Vault 目录结构 |
| `resolve` | 通过路径或标题查找笔记 |
| `info` | 获取文件元数据（行数、字节数、sha256 哈希值、修改时间） |
| `read` | 读取笔记内容 |
| `create` | 创建新笔记（如果文件已存在，则失败） |
| `append` | 向现有笔记追加内容 |
| `set-root` | 设置 Vault 的根目录 |

## 如何执行命令

所有命令都是通过 SSH 执行的：
```bash
ssh -4 -p ${VAULT_SSH_PORT:-2222} ${VAULT_SSH_USER}@${VAULT_SSH_HOST:-localhost} vaultctl <command> [args]
```

始终使用 `-4` 选项来强制使用 IPv4 协议（以避免 IPv6 超时问题）。

## 环境变量

这些变量必须在 VPS 上的技能运行时环境中设置：

| 变量 | 是否必需 | 默认值 | 描述 |
|----------|----------|---------|-------------|
| `VAULT_SSH_USER` | 是 | — | 用于 SSH 隧道的本地机器用户名 |
| `VAULT_SSH_PORT` | 否 | `2222` | SSH 隧道的本地主机端口 |
| `VAULT_SSH_HOST` | 否 | `localhost` | SSH 隧道的宿主地址 |

## 命令参考

### `tree` - 列出 Vault 目录结构
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --all
```
选项：
- `--depth N` - 遍历的最大深度
- `--all` - 包含所有文件（而不仅仅是 `.md` 格式的文件）

### `resolve` - 通过路径或标题查找笔记
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --title "Meeting Notes"
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --path "Projects/Plan.md"
```

**对于包含空格的路径/标题**，请使用 `--base64` 选项：
```bash
# echo -n "My Meeting Notes" | base64 → TXkgTWVldGluZyBOb3Rlcw==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl resolve --title TXkgTWVldGluZyBOb3Rlcw== --base64
```

### `info` - 获取文件元数据
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl info "Projects/Plan.md"
```
返回 JSON 格式的数据：`{"path": "...", "lines": N, "bytes": N, "sha256": "...", "mtime": N}`

**对于包含空格的路径**，请使用 `--base64` 选项：
```bash
# echo -n "Notes/My File.md" | base64 → Tm90ZXMvTXkgRmlsZS5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl info Tm90ZXMvTXkgRmlsZS5tZA== --base64
```

### `read` - 读取笔记内容
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "Projects/Plan.md"
```
返回 JSON 格式的数据：`{"path": "...", "content": "..."}`

**对于包含空格的路径**，请使用 `--base64` 选项：
```bash
# echo -n "Notes/My File.md" | base64 → Tm90ZXMvTXkgRmlsZS5tZA==
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read Tm90ZXMvTXkgRmlsZS5tZA== --base64
```

### `create` - 创建新笔记
**重要提示**：在使用路径和内容时，必须同时使用 `--base64` 选项对它们进行 Base64 编码。这对于包含空格或特殊字符的路径/内容是必需的。

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create <base64_path> <base64_content> --base64
```

**示例**：创建名为 “Notes/Morning Brief.md” 的笔记，内容为 “# Hello\n\nWorld”：
```bash
# Encode path: echo -n "Notes/Morning Brief.md" | base64 → Tm90ZXMvTW9ybmluZyBCcmllZi5tZA==
# Encode content: echo -n "# Hello\n\nWorld" | base64 → IyBIZWxsbwoKV29ybGQ=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create Tm90ZXMvTW9ybmluZyBCcmllZi5tZA== IyBIZWxsbwoKV29ybGQ= --base64
```

- 会自动创建父目录。
- 如果文件已存在，则创建失败（此时应使用 `append` 选项向现有文件追加内容）。
- 文件必须具有 `.md` 扩展名。
- **切勿在笔记内容中使用标题作为行首**（例如，对于 “My Note.md”，不要以 “# My Note” 开头）。

### `append` - 向现有笔记追加内容
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append <base64_path> <base64_content> --base64
```

- 如果文件不存在，则创建失败（此时应使用 `create` 选项）。

### `set-root` - 设置 Vault 的根目录
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl set-root /path/to/vault
```

## 不支持的操作

以下操作是不被支持的：
- 重命名文件或文件夹
- 删除文件或文件夹
- 在文件夹之间移动文件
- 编辑文件的特定部分（只能追加内容）
- 创建没有内容的文件夹（文件夹会通过 `create` 命令自动创建）

## 提示

- 总是先运行 `vaultctl tree` 来查看现有的笔记。
- 使用 `vaultctl resolve --title "..."` 根据标题查找笔记。
- 所有输出都是 JSON 格式。
- 本地机器必须保持在线状态，并且 SSH 隧道必须处于运行中。
- **对于包含空格的路径**：使用 `--base64` 选项对路径进行 Base64 编码（此选项适用于 `read`、`info`、`create` 和 `append` 命令）。

## 示例

**重要提示**：如果您不确定有哪些笔记存在，请务必先运行 `tree` 命令。这可以避免因路径错误或名称重复而导致的错误。

### 示例 1：用户请求读取笔记（先检查）
用户：“显示我的项目计划”

步骤 1：检查现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

步骤 2：然后读取正确的笔记路径：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "Projects/Plan.md"
```
输出：
```json
{"path": "Projects/Plan.md", "content": "# Project Plan\n\n## Goals\n..."}
```

### 示例 2：用户请求创建笔记（先检查以避免重复）
用户：“创建一个会议笔记文件”

步骤 1：检查现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

步骤 2：由于不存在 “Meeting Notes” 文件，可以安全地创建新笔记（注意不要在标题中使用相同的名称）：
```bash
# echo -n "Meeting Notes.md" | base64 → TWVldGluZyBOb3Rlcy5tZA==
# echo -n "## Agenda\n\n- Item 1\n- Item 2\n" | base64 → IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create TWVldGluZyBOb3Rlcy5tZA== IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo= --base64
```
输出：
```json
{"status": "ok", "path": "Meeting Notes.md"}
```

### 示例 3：用户询问 Vault 的内容
用户：“我的笔记里有什么？”

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}, {"path": "Ideas.md", "type": "file"}]}
```

然后向用户总结：“您的 Vault 中有一个名为 ‘Projects’ 的文件夹，其中包含 ‘Plan.md’ 文件，以及一个位于根目录下的 ‘Ideas.md’ 文件。”

### 示例 4：包含源笔记和输出笔记的复杂工作流程
用户：“根据源笔记 ‘AI Digest Sources.md’，浏览相关资源并将摘要保存到 ‘digest/2025-01-28-digest.md’ 文件中”

步骤 1：检查现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "AI Digest Sources.md", "type": "file"}, {"path": "digest", "type": "dir"}, {"path": "digest/2025-01-27-digest.md", "type": "file"}]}
```

步骤 2：验证：
- 源笔记 “AI Digest Sources.md” 存在。
- 输出文件 “digest/2025-01-28-digest.md” 不存在，因此需要创建新文件（使用 `create` 命令）。

（如果源笔记不存在：停止操作并询问用户：“您是指这些文件中的哪一个？[列出可选文件]”）

（如果目标文件已经存在：使用 `append` 命令而不是 `create`。）

步骤 3：读取源笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "AI Digest Sources.md"
```
输出：
```json
{"path": "AI Digest Sources.md", "content": "# AI Digest Sources\n\n- https://example.com/article1\n- https://example.com/article2\n"}
```

步骤 4：浏览源笔记并生成摘要内容（这些操作由机器人在外部完成）。

步骤 5：将摘要内容保存到 Vault 中（注意不要在标题中使用相同的名称）：
```bash
# echo -n "digest/2025-01-28-digest.md" | base64 → ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k
# echo -n "## Summary\n\nKey points from today's sources...\n" | base64 → IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo= --base64
```

（如果目标文件已经存在：使用 `append` 命令而不是 `create`。）
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgVXBkYXRlCi4uLg== --base64
```