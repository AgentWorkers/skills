---
name: Folders
description: 索引重要的目录，并在执行安全文件夹操作时进行适当的安全检查。
metadata: {"clawdbot":{"emoji":"📂","os":["linux","darwin","win32"]}}
---

## 文件夹索引

在 `~/.config/folder-index.json` 中维护一个轻量级的索引，以便在不重新扫描文件系统的情况下快速找到重要文件或文件夹的位置。

```json
{
  "folders": [
    {"path": "/Users/alex/projects/webapp", "type": "project", "note": "Main client project"}
  ]
}
```

当用户询问“X 在哪里？”或“我的项目 Y 在哪里？”时，首先查看索引。如果找不到相关内容，再进行针对性的搜索，并提供搜索结果。

## 文件夹搜索与索引功能

- 搜索可能存在的文件夹位置：`~/projects`、`~/Documents`、`~/code`、`~/dev`、`~/work`
- 通过以下文件标记来识别项目：`.git`、`package.json`、`pubspec.yaml`、`Cargo.toml`、`go.mod`、`pyproject.toml`、`.sln`
- 一旦找到相关文件或文件夹，立即停止搜索（不会递归搜索 `node_modules`、`vendor`、`build` 目录）
- 显示搜索结果，但不会自动将新发现的文件或文件夹添加到索引中：例如：“在 `~/code` 目录中找到了 8 个项目。是否要将它们添加到索引中？”

## 路径安全性

- 在执行任何操作之前，对路径进行规范化处理（处理 `~`、`..`、符号链接等）
- 忽略系统路径：`/`、`/etc`、`/var`、`/usr`、`/System`、`/Library`、`C:\Windows`、`C:\Program Files`
- 在遍历文件系统时跳过符号链接，并单独记录它们的存在

## 破坏性操作的处理

- 使用操作系统的回收站功能而不是永久删除文件
- 明确说明文件的可恢复性：例如：“`node_modules` 目录中的文件可以通过 `npm install` 恢复”

## 不同平台的特殊注意事项

- **macOS**：仅包含 `.DS_Store` 的文件夹实际上为空；将 `.app` 文件视为一个独立的文件项。
- **Windows**：路径长度超过 260 个字符时，需要在路径前添加 `\\?\` 前缀。
- **网络驱动器**：在进行批量操作前发出警告——这些驱动器可能响应较慢或处于离线状态。