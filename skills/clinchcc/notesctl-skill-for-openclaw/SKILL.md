---
name: notesctl
description: 通过确定性的本地脚本来管理 Apple Notes（创建、添加、列出、搜索、导出和编辑）。当用户要求 OpenClaw 添加笔记、列出笔记、搜索笔记或管理笔记文件夹时，可以使用这些脚本。
metadata:
  {
    "openclaw": {
      "emoji": "📝",
      "os": ["darwin"],
      "requires": { "bins": ["memo", "python3", "osascript"] }
    }
  }
---

# notesctl（用于 Apple Notes，低令牌使用量）

## 目标

通过将 Apple Notes 操作路由到预打包的脚本中，最小化令牌的使用量并避免因引用方式不当而导致的错误。

## 快速入门

### 创建新笔记（标题和内容固定）

- 推荐使用 JSON 格式通过标准输入（stdin）：

```bash
echo '{"title":"Title","body":"Line 1\nLine 2","folder":"Notes"}' | {baseDir}/scripts/notes_post.sh
```

- 直接使用命令参数：

```bash
{baseDir}/scripts/notes_new.sh "Title" $'Body line 1\nBody line 2' "Notes"
```

### 列出/搜索/导出笔记

```bash
{baseDir}/scripts/notes_list.sh "Notes"
{baseDir}/scripts/notes_search.sh "query" "Notes"
{baseDir}/scripts/notes_export.sh "query" "Notes" "/tmp"  # interactive select then export
```

## 输出格式规范

- 输出信息应简洁明了：例如：“已写入 Notes：<标题>”。

## 关于编辑现有笔记的注意事项

编辑现有笔记存在一定的风险：
- 建议采用追加内容的方式，或者创建一个新笔记并引用原有笔记。
- 如果用户确实需要交互式编辑功能，可以使用 `memo notes -e`（手动选择内容后使用编辑器进行编辑）。