---
name: save-to-obsidian
description: 通过 SSH 将 Markdown 内容保存到远程的 Obsidian 文档库中。
version: 1.0.0
---
# 将Markdown内容保存到Obsidian

通过SSH将Markdown内容保存到远程的Obsidian仓库中。

## 前提条件

**此功能适用于未启用iCloud同步的机器**（例如Linux/Ubuntu服务器）。如果您的机器已经启用了iCloud Desktop同步并且可以直接访问Obsidian仓库，那么您不需要使用此功能——只需将文件直接复制到仓库路径即可。

## 使用场景

用户输入指令：“保存到Obsidian”、“发送到Obsidian”或“复制到Obsidian”。

## 执行步骤

1. 将内容写入一个临时的.md文件（请遵循以下格式规则）。
2. 使用`scp`命令将文件复制到远程仓库：`scp <文件路径> user@远程主机:/路径/到/obsidian/仓库/`
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

**配置说明：** 代理程序应使用`WORKSPACE/TOLS.md`文件中配置的SSH主机地址和仓库路径。

## 格式规则

所有保存到Obsidian的内容都必须遵循以下规则：

### 图表：使用Mermaid（强制要求）
- **严禁**使用ASCII框图、ASCII艺术或纯文本图表。
- **必须**使用Mermaid格式的代码块（例如：````mermaid`）。
- Obsidian能够直接渲染Mermaid图表；ASCII格式的图表可能显示不完整或无法正确显示。
- 支持的图表类型包括：流程图、序列图、状态图、类图、ER图、甘特图、饼图、思维导图、时间线图、象限图和图表。

### 表格：使用Markdown表格
- Obsidian能够直接渲染Markdown表格。
- 对于复杂的数据，建议使用表格而非项目符号列表。

### 链接：使用wiki链接或相对链接
- 在Obsidian笔记之间创建链接：`[[笔记名称]]`。
- 外部链接：使用标准的Markdown格式：`[链接文本](网址)`。

### 其他注意事项
- 使用标题（##）来组织内容结构——Obsidian的目录面板依赖于这些标题。
- 如果需要元数据，请使用YAML格式的前言部分。
- 为了跨平台兼容性，请确保文件名使用kebab-case格式（不包含空格）。

## 其他说明
- 该功能使用现有的SSH密钥进行身份验证（无需输入密码）。
- 目标位置：远程主机上的Obsidian仓库路径。
- 如果仓库位于iCloud文件夹中，文件会通过iCloud自动同步。