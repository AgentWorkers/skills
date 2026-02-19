---
name: save-to-obsidian
description: 通过 SSH 将 Markdown 内容保存到远程的 Obsidian 文档库中。
version: 1.0.0
---
# 保存到 Obsidian

该功能通过 SSH 将 Markdown 内容保存到远程的 Obsidian 仓库中。

## 前提条件

**此功能适用于未启用 iCloud 同步的机器**（例如 Linux/Ubuntu 服务器）。如果您的机器已经启用了 iCloud Desktop 同步并且可以直接访问 Obsidian 仓库，那么您就不需要使用此功能——只需将文件直接复制到仓库路径即可。

## 使用场景

用户输入指令：“保存到 Obsidian”、“发送到 Obsidian”或“复制到 Obsidian”。

## 执行流程

1. 将内容写入一个临时的 `.md` 文件（需遵循以下格式规则）。
2. 使用 `scp` 命令将文件复制到远程仓库：`scp <文件路径> user@远程主机:/路径/到/obsidian/仓库/`
3. 向用户确认操作是否成功。

**示例：**
```bash
# Write content to temp file
cat > /tmp/my-note.md << 'EOF'
# My Note
Content here
EOF

# Copy to remote Obsidian vault
scp /tmp/my-note.md myuser@vault.example.com:~/Obsidian/MyVault/

# Clean up
rm /tmp/my-note.md
```

**配置说明：** 该功能依赖于工作区中的 `TOOLS.md` 文件中配置的 SSH 主机和仓库路径。

## 格式规则

所有保存到 Obsidian 的内容都必须遵循以下规则：

### 图表：使用 Mermaid（强制要求）
- **严禁** 使用 ASCII 方框图、ASCII 艺术或纯文本图表。
- **必须** 使用 Mermaid 格式的代码块（````mermaid`）。
- Obsidian 可以直接渲染 Mermaid 图表；ASCII 图表可能会显示异常。
- 支持的图表类型包括：流程图、序列图、状态图、类图、ER 图、甘特图、饼图、思维导图、时间线图、象限图和图表。

### 表格：使用 Markdown 表格
- Obsidian 可以直接渲染 Markdown 表格。
- 对于复杂的数据，建议使用表格而非项目符号列表。

### 链接：使用 wiki 链接或相对链接
- 在 Obsidian 笔记之间创建链接：`[[笔记名称]]`
- 外部链接：使用标准 Markdown 格式：`[链接文本](网址)`

### 其他注意事项
- 使用标题（`##`）来组织内容结构——Obsidian 的大纲面板依赖于这些标题。
- 如果需要元数据，请使用 YAML 格式的 frontmatter。
- 为了跨平台兼容性，文件名应使用驼峰式命名法（不包含空格）。

## 执行者

此功能由 OpenClaw 的主代理会话执行。`save-to-obsidian.sh` 脚本通过 `exec` 工具以 shell 命令的形式运行。不会生成任何子代理。文件传输完成后，iCloud 同步会自动完成，无需额外操作。

## 成功标准

保存操作成功的前提条件包括：
1. `scp` 命令以 0 状态码退出。
2. 文件成功上传到仓库，并且文件名正确。
3. iCloud 同步已完成文件同步（通常需要 1-2 分钟；此过程不由该功能监控）。

**失败情况：**
- SSH 连接失败：脚本会输出错误信息并退出。
- 仓库路径不存在。
- 磁盘空间不足。
- 文件名包含无法被 iCloud 同步的字符（脚本会自动处理这些字符）。

**特殊情况处理：**
- **SSH 连接失败**：脚本会输出错误信息并退出。
- 文件名重复：文件会被自动覆盖（`scp` 命令不会发出警告，用户需要确认是否确实需要覆盖该文件）。
- 文件名中包含特殊字符：脚本会自动处理这些字符（将空格替换为连字符，删除无效字符）。
- 文件内容为空：`scp` 会传输一个大小为 0 字节的文件；虽然这不是错误，但应予以提示。
- 文件没有明确的标题：如果内容没有 H1 标题，脚本应在保存前提示用户输入文件名。
- iCloud 同步延迟：文件应在 1-2 分钟内上传到仓库；如果 5 分钟后仍未显示，请检查 iCloud 的同步状态。

## 其他说明：
- 该功能使用现有的 SSH 密钥进行身份验证（无需输入密码）。
- 目标路径是远程主机上的 Obsidian 仓库位置。
- 如果仓库位于 iCloud 文件夹中，文件会通过 iCloud 自动同步。

## 配置方式

该功能从工作区的 `TOOLS.md` 文件中读取 SSH 和仓库的配置信息：

| 变量          | 描述                                      | 设置位置                    |
|-----------------|----------------------------------------|-------------------------|
| SSH 主机         | 托管 Obsidian 仓库的远程主机的名称/IP             | TOOLS.md                    |
| SSH 用户名        | 远程主机上的用户名                             | TOOLS.md                    |
| SSH 密钥路径       | SSH 私钥的路径（默认：`~/.ssh/id_rsa`）             | TOOLS.md                    |
| 仓库路径         | 远程主机上 Obsidian 仓库的绝对路径                   | TOOLS.md                    |

**示例 `TOOLS.md` 配置：**
```
## Obsidian Remote Vault
- SSH host: myserver.local
- SSH user: your-username
- Vault path: ~/Obsidian/MyVault/
```

**注意：** 该功能不依赖于任何 API 密钥或令牌，仅使用 SSH 密钥进行身份验证。