---
name: gdocs-markdown
description: **将 Markdown 文件转换为 Google 文档的技能**  
当用户希望将 Markdown 内容转换为 Google 文档，或者在使用 `gog CLI` 时需要向 Google 文档中添加内容时，可以使用此技能。该技能通过 Drive 上传来实现 Markdown → DOCX → Google 文档的转换过程。需要注意的是，`gog CLI` 仅支持创建、导出、分类和复制文档，但不支持写入或更新文档内容。
---

# 从 Markdown 文件创建 Google 文档

使用以下工作流程将 Markdown 文件转换为 Google 文档：Markdown → DOCX → 上传到 Google Drive → 在 Google Docs 中使用：

## 为什么需要这个技能

`gog docs` 命令行工具（CLI）不支持向 Google Docs 写入或更新内容。它仅支持以下操作：
- `create`：创建空白文档
- `export`：导出为文件
- `cat`：读取内容
- `copy`：复制现有文档

这个技能提供了从 Markdown 文件创建包含内容的 Google 文档所需的工作流程。

## 作者

由 **techla** 创建

## 先决条件

- 使用 Google 账户登录 `gog` CLI
- 安装 `pandoc` 工具（如果未安装，首次使用时会自动下载）

## 安装说明

从 ClawHub 安装该工具后，请修复脚本的权限设置：
```bash
chmod +x ~/.openclaw/workspace/skills/gdocs-markdown/scripts/gdocs-create.sh
```

## 使用方法

### 快速创建

```bash
# Create Google Doc from markdown file
gdocs-create.sh /path/to/file.md "Tiêu đề Document"
```

### 手动工作流程

如果您需要更多控制，请按照以下步骤操作：

1. **确保已安装 pandoc：**
   ```bash
   # Auto-downloaded to /tmp/pandoc-3.1.11/bin/pandoc on first use
   # Or use system pandoc if available
   ```

2. **将 Markdown 文件转换为 DOCX 格式：**
   ```bash
   /tmp/pandoc-3.1.11/bin/pandoc input.md -o output.docx
   ```

3. **上传到 Google Drive（自动转换为 Google 文档）：**
   ```bash
   gog drive upload output.docx
   ```

4. **结果：** Google Drive 会返回转换后的 Google 文档链接

## 脚本参考

请参阅 `scripts/gdocs-create.sh` 脚本，该脚本可自动化整个工作流程。

## 示例

```bash
# Create a report from markdown
echo "# Báo Cáo\n\nNội dung..." > /tmp/report.md
gdocs-create.sh /tmp/report.md "Báo Cáo Tháng 2"

# Output: https://docs.google.com/document/d/xxxxx/edit
```

## 注意事项

- Google Drive 会在上传时自动将 DOCX 文件转换为 Google Docs 格式
- 转换后的文档可以在 Google Docs 中进行编辑
- 如果只需要 Google Docs 版本，原始的 DOCX 文件仍会保留在 Google Drive 中，但也可以删除