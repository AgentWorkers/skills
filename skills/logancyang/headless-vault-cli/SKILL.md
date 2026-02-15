---
name: headless-vault-cli
description: 您可以通过 SSH 隧道在个人电脑上阅读和编辑 Markdown 笔记。当用户需要阅读、创建或向他们的笔记库中添加内容时，可以使用此方法。
homepage: https://github.com/logancyang/headless-vault-cli
metadata: {"moltbot":{"emoji":"🗄️"}}
---

# 无头 Vault CLI

您可以通过 SSH 隧道，从托管在 VPS 上的 Moltbot 访问个人电脑上的 Markdown 笔记。

**术语说明**：“本地机器”指的是存储您笔记的个人电脑（macOS 或 Linux）。该工具运行在 VPS 上，并通过反向 SSH 隧道连接到您的电脑。

## 可用命令

您只能使用以下命令。请勿尝试未列出的命令（没有重命名、删除、移动或编辑文件的命令）。

| 命令 | 描述 |
|---------|-------------|
| `tree` | 列出 vault 目录结构 |
| `resolve` | 通过路径或标题查找笔记 |
| `info` | 获取文件元数据（行数、字节数、sha256 哈希值、修改时间） |
| `read` | 读取笔记内容 |
| `create` | 创建新笔记（如果文件已存在，则失败） |
| `append` | 向现有笔记追加内容 |
| `set-root` | 设置 vault 的根目录 |

## 如何运行命令

所有命令均通过 SSH 执行：
```bash
ssh -4 -p ${VAULT_SSH_PORT:-2222} ${VAULT_SSH_USER}@${VAULT_SSH_HOST:-localhost} vaultctl <command> [args]
```

始终使用 `-4` 选项来强制使用 IPv4 协议（以避免 IPv6 连接超时问题）。

## 命令参考

### `tree` - 列出 vault 目录结构
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --all
```
选项：
- `--depth N` - 最大遍历深度
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
**重要提示**：路径和内容都必须使用 `--base64` 选项进行 Base64 编码。这对于包含空格或特殊字符的路径/内容是必需的。

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create <base64_path> <base64_content> --base64
```

**创建名为 "Notes/Morning Brief.md" 且内容为 "# Hello\n\nWorld" 的笔记的示例**：
```bash
# Encode path: echo -n "Notes/Morning Brief.md" | base64 → Tm90ZXMvTW9ybmluZyBCcmllZi5tZA==
# Encode content: echo -n "# Hello\n\nWorld" | base64 → IyBIZWxsbwoKV29ybGQ=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create Tm90ZXMvTW9ybmluZyBCcmllZi5tZA== IyBIZWxsbwoKV29ybGQ= --base64
```

- 会自动创建父目录
- 如果文件已存在，则创建失败（此时应使用 `append` 命令向现有文件追加内容）
- 文件必须具有 `.md` 扩展名
- **切勿在笔记内容中重复使用标题作为标题**（例如，对于 "My Note.md"，不要以 "# My Note" 开头）

### `append` - 向现有笔记追加内容
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl append <base64_path> <base64_content> --base64
```

- 如果文件不存在，则创建失败（此时应使用 `create` 命令）

### `set-root` - 设置 vault 的根目录
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl set-root /path/to/vault
```

## 不支持的操作

以下操作是不被支持的：
- **重命名** 文件或文件夹
- **删除** 文件或文件夹
- **在文件夹之间移动** 文件
- **编辑** 文件的特定部分（只能追加内容到文件末尾）
- **创建** 无内容的文件夹（文件夹会通过 `create` 命令自动创建）

## 环境变量

这些环境变量由 `tunnel-setup.sh` 脚本自动配置：
- `VAULT_SSH_USER` - 本地机器的用户名（自动检测）
- `VAULT_SSH_PORT` - 隧道端口（默认：2222）
- `VAULT_SSH_HOST` - 隧道主机（默认：localhost）

## 提示

- 在使用任何命令之前，请务必先运行 `vaultctl tree` 以查看现有的笔记。
- 使用 `vaultctl resolve --title "..."` 根据标题查找笔记。
- 所有输出均为 JSON 格式。
- 本地机器必须处于在线状态，并且 SSH 隧道必须处于运行中。
- **对于包含空格的路径**：请使用 `--base64` 选项对路径进行 Base64 编码（此选项适用于 `read`、`info`、`create` 和 `append` 命令）。

## 示例

**重要提示**：如果您不确定有哪些笔记存在，请务必先运行 `tree` 命令。这可以避免因路径错误或名称重复导致的错误。

### 示例 1：用户请求阅读笔记（先检查）
用户：**显示我的项目计划**

步骤 1 - 查看现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

步骤 2 - 然后读取正确的笔记路径：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "Projects/Plan.md"
```
输出：
```json
{"path": "Projects/Plan.md", "content": "# Project Plan\n\n## Goals\n..."}
```

### 示例 2：用户请求创建笔记（先检查以避免重复）
用户：**创建一个会议笔记文件**

步骤 1 - 查看现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}]}
```

步骤 2 - 由于不存在 "Meeting Notes" 文件，可以安全地创建新笔记（切勿在笔记内容中使用该标题作为标题）：
```bash
# echo -n "Meeting Notes.md" | base64 → TWVldGluZyBOb3Rlcy5tZA==
# echo -n "## Agenda\n\n- Item 1\n- Item 2\n" | base64 → IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create TWVldGluZyBOb3Rlcy5tZA== IyMgQWdlbmRhCgotIEl0ZW0gMQotIEl0ZW0gMgo= --base64
```
输出：
```json
{"status": "ok", "path": "Meeting Notes.md"}
```

### 示例 3：用户询问 vault 的内容
用户：**我的笔记里有什么？**

```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree --depth 2
```
输出：
```json
{"tree": [{"path": "Projects", "type": "dir"}, {"path": "Projects/Plan.md", "type": "file"}, {"path": "Ideas.md", "type": "file"}]}
```

然后向用户总结：**您有一个名为 "Projects" 的文件夹，其中包含 "Plan.md" 文件，以及一个位于根目录下的 "Ideas.md" 文件。**

### 示例 4：包含源笔记和输出笔记的复杂工作流程
用户：**根据源笔记 'AI Digest Sources.md'，浏览相关资料并将摘要保存到 'digest/2025-01-28-digest.md' 文件中**

步骤 1 - 查看现有笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl tree
```
输出：
```json
{"tree": [{"path": "AI Digest Sources.md", "type": "file"}, {"path": "digest", "type": "dir"}, {"path": "digest/2025-01-27-digest.md", "type": "file"}]}
```

步骤 2 - 验证：
- 源笔记 "AI Digest Sources.md" 存在 ✓
- 输出文件 "digest/2025-01-28-digest.md" 不存在 → 将使用 `create` 命令创建新文件

（如果源笔记不存在：请停止操作并询问用户：“您是指这些文件中的哪一个？”）
（如果目标文件已经存在：请使用 `append` 命令而不是 `create`）

步骤 3 - 读取源笔记：
```bash
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl read "AI Digest Sources.md"
```
输出：
```json
{"path": "AI Digest Sources.md", "content": "# AI Digest Sources\n\n- https://example.com/article1\n- https://example.com/article2\n"}
```

步骤 4 - 浏览相关资料并生成摘要内容（这些操作由外部脚本完成）

步骤 5 - 将摘要内容保存到 vault 中（切勿在文件标题中重复使用标题）：
```bash
# echo -n "digest/2025-01-28-digest.md" | base64 → ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k
# echo -n "## Summary\n\nKey points from today's sources...\n" | base64 → IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo=
ssh -4 -p 2222 ${VAULT_SSH_USER}@localhost vaultctl create ZGlnZXN0LzIwMjUtMDEtMjgtZGlnZXN0Lm1k IyMgU3VtbWFyeQoKS2V5IHBvaW50cyBmcm9tIHRvZGF5J3Mgc291cmNlcy4uLgo= --base64
```

（如果目标文件已经存在：请使用 `append` 命令而不是 `create`）