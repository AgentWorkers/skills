---
name: apple-notes-custom
description: **macOS上的Apple Notes.app集成**：通过AppleScript可以列出文件夹中的笔记，读取、创建、搜索、编辑和删除笔记。
metadata: {"clawdbot":{"emoji":"📝","os":["darwin"]}}
---

# Apple Notes

您可以通过 AppleScript 来操作 Notes.app。脚本的执行路径为：`cd {baseDir}`

## 命令

| 命令 | 用法 |
|---------|-------|
| 列出文件夹 | `scripts/notes-folders.sh [--tree] [--counts]` |
| 列出笔记 | `scripts/notes-list.sh [folder] [limit]` |
| 读取笔记 | `scripts/notes-read.sh <名称或ID> [folder]` |
| 创建笔记 | `scripts/notes-create.sh <folder> <标题> <正文>` |
| 搜索笔记 | `scripts/notes-search.sh <查询> [folder] [limit] [--仅标题]` |
| 编辑笔记 | `scripts/notes-edit.sh <名称或ID> <新正文> [folder]` |
| 删除笔记 | `scripts/notes-delete.sh <名称> <folder>` ⚠️ 需指定文件夹 |

## 文件夹路径

所有命令都支持使用 `/` 作为分隔符来指定子文件夹路径：

```bash
scripts/notes-list.sh "Scanned/Medical & Health" 10
scripts/notes-read.sh "blood test" "Scanned/Medical & Health"
scripts/notes-create.sh "Property/416 Garfield" "Inspection notes" "Roof looks good"
```

### 文件夹结构

该文件夹包含 4000 多条笔记，主要结构如下：

- **Scanned** — 主文件夹，下含多个子文件夹（如 Medical & Health、Receipts 等）
- **Fetish** — 主文件夹，下含多个子文件夹（如 AW、Bimbo、Events 等）
- **Hobbies** — 主文件夹，下含多个子文件夹（如 3d printing、Homelab 等）
- **Property** — 每个地址对应一个子文件夹

使用 `--tree --counts` 可查看完整的文件夹层次结构。

## 文件夹列表

```bash
scripts/notes-folders.sh                  # Flat list
scripts/notes-folders.sh --counts         # With note counts
scripts/notes-folders.sh --tree --counts  # Full hierarchy with counts
```

## 笔记列表

```bash
scripts/notes-list.sh "Notes" 10                      # Specific folder
scripts/notes-list.sh "Scanned/Receipts" 5             # Subfolder
scripts/notes-list.sh "" 10                             # All folders (shows folder name per note)
```

- 如果不指定文件夹，输出格式为：`ID | 日期 | 文件夹 | 标题`
- 如果指定了文件夹，输出格式为：`ID | 日期 | 标题`

## 读取笔记

```bash
scripts/notes-read.sh "blood test" "Scanned/Medical & Health"   # By name (partial match)
scripts/notes-read.sh "x-coredata://…/ICNote/p12345"            # By ID (direct lookup, fast)
```

输出内容包括：标题、文件夹、修改日期和笔记 ID，以及笔记正文。

## 搜索笔记

- 首先进行标题搜索（速度较快），若未找到则进行正文搜索（速度较慢）：

```bash
scripts/notes-search.sh "tax" "" 10                    # All folders
scripts/notes-search.sh "receipt" "Scanned/Receipts" 5  # Specific folder
scripts/notes-search.sh "keyword" "" 10 --title-only    # Skip body search
```

输出格式为：`ID | 日期 | 文件夹 | 标题`

## 创建笔记

```bash
scripts/notes-create.sh "Notes" "My Title" "Body text here"   # With body
scripts/notes-create.sh "Notes" "Empty Note"                    # Title only
```

创建笔记后，会返回笔记的 ID。

## 编辑笔记

```bash
scripts/notes-edit.sh "My Note" "New body content" "Notes"              # By name
scripts/notes-edit.sh "x-coredata://…/ICNote/p12345" "New body"         # By ID
```

## 删除笔记

```bash
scripts/notes-delete.sh "Old Note" "Notes"                    # Folder required
scripts/notes-delete.sh "receipt" "Scanned/Receipts"
```

⚠️ 为确保安全性，**必须指定文件夹**——这样可以避免在 4000 多条笔记中误删除笔记。

## 性能提示

| 情况 | 提示 |
|-----------|-----|
| 列出/搜索所有笔记 | **务必指定文件夹**——遍历 4000 多条笔记会非常慢 |
| 读取已知的笔记 | 使用之前列表或搜索中获得的 **ID** 进行快速查找 |
| 在大型文件夹中搜索 | 如果不需要搜索正文，可以使用 `--仅标题` 选项 |
| 找到正确的文件夹 | 先使用 `--tree --counts` 查看文件夹结构 |

## 错误信息

| 错误 | 原因 |
|-------|-------|
| `Error: 无法获取文件夹` | 文件夹名称不存在或路径错误 |
| `未找到匹配的笔记…` | 在指定范围内未找到匹配项 |
| 正文为空 | 仅包含扫描内容或图片的笔记无法提取文本 |

## 技术细节

- 读取/编辑/删除操作支持部分名称匹配（匹配到第一个条目即可）
- 支持多行正文，通过临时文件实现
- 文件夹名称区分大小写
- 为确保 AppleScript 的安全性，所有用户输入内容都会进行转义处理（使用引号或反斜杠）
- 使用 `number of` 而不是 `count of`（`count of` 是 AppleScript 的保留词）