---
name: obsidian
description: 使用 Obsidian 文书管理系统（基于纯 Markdown 的笔记格式），并通过 `obsidian-cli` 实现自动化操作。
homepage: https://help.obsidian.md
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["obsidian-cli"]},"install":[{"id":"brew","kind":"brew","formula":"yakitrak/yakitrak/obsidian-cli","bins":["obsidian-cli"],"label":"Install obsidian-cli (brew)"}]}}
---

# Obsidian

Obsidian 的“vault”实际上只是一个普通的文件夹，存储在磁盘上。

**典型的 vault 结构：**
- **Notes**：`.md` 文件（纯文本 Markdown 格式；可以用任何文本编辑器进行编辑）
- **Config**：`.obsidian/` 文件（工作区设置和插件配置；通常不建议通过脚本直接修改）
- **Canvases**：`.canvas` 文件（JSON 格式的画布数据）
- **Attachments**：你可以根据 Obsidian 的设置来指定附件的存放位置（例如图片、PDF 等文件）

## 查找当前激活的 vault

Obsidian 的桌面应用程序会从以下文件中记录当前的 vault 信息：
- `~/Library/Application Support/obsidian/obsidian.json`

`obsidian-cli` 命令会从这个文件中读取 vault 的信息；vault 的名称通常就是该文件夹的名称（文件路径的后缀）。

**快速查询当前激活的 vault 或笔记的位置：**
- 如果你已经设置了默认的 vault：`obsidian-cli print-default --path-only`
- 否则，可以阅读 `~/Library/Application Support/obsidian/obsidian.json` 文件，然后找到其中 `“open”: true` 标记的 vault。

**注意事项：**
- 通常会使用多个 vault（例如 iCloud 存储的笔记、工作相关的笔记、个人笔记等）。不要随意猜测 vault 的位置，应该查看配置文件。
- 避免在脚本中硬编码 vault 的路径；建议直接读取配置文件或使用 `obsidian-cli print-default` 命令来获取信息。

## `obsidian-cli` 快速入门

**设置默认的 vault：**
- `obsidian-cli set-default "<vault-folder-name>"`
- `obsidian-cli print-default` 或 `obsidian-cli print-default --path-only`

**搜索：**
- `obsidian-cli search "query"` （用于搜索笔记的标题）
- `obsidian-cli search-content "query"` （用于搜索笔记内容；会显示笔记的片段和具体行）

**创建笔记：**
- `obsidian-cli create "Folder/New note" --content "..." --open`
- 需要确保你的系统安装了 Obsidian，并且支持 Obsidian 的 URI 协议（`obsidian://...`）。
- 注意：不要尝试通过 URI 在隐藏的文件夹（如 `.something/...`）下创建笔记，否则 Obsidian 可能会拒绝执行操作。

**移动/重命名笔记：**
- `obsidian-cli move "old/path/note" "new/path/note"`
- 此操作会更新整个 vault 中的引用（如 `[[wikilinks]]` 和 Markdown 链接）；这是使用 `obsidian-cli` 的主要优势。

**删除笔记：**
- `obsidian-cli delete "path/note"`

**建议：**
在适当的情况下，直接编辑 `.md` 文件进行修改；Obsidian 会自动更新相应的文件结构。