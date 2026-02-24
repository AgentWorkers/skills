---
name: apple-notes
description: 在 macOS 上，可以通过 `memo` CLI 来管理 Apple Notes（创建、查看、编辑、删除、搜索、移动和导出笔记）。当用户要求 Clawdbot 添加笔记、列出笔记、搜索笔记或管理笔记文件夹时，可以使用该工具。
homepage: https://github.com/antoniorodr/memo
metadata: {"clawdbot":{"emoji":"📝","os":["darwin"],"requires":{"bins":["memo"]},"install":[{"id":"brew","kind":"brew","formula":"antoniorodr/memo/memo","bins":["memo"],"label":"Install memo via Homebrew"}]}}
---

# Apple Notes CLI

使用 `memo notes` 命令可以直接从终端管理 Apple Notes。您可以创建、查看、编辑、删除笔记，搜索笔记，将笔记在不同文件夹之间移动，以及将笔记导出为 HTML 或 Markdown 格式。

## 安装

- 使用 Homebrew：`brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- 手动安装（通过 pip）：`pip install .`（在克隆仓库后执行此命令）
- 仅适用于 macOS；如果系统提示，请授予 `Notes.app` 自动化访问权限。

## 查看笔记

- 列出所有笔记：`memo notes`
- 按文件夹过滤笔记：`memo notes -f "文件夹名称"`
- 模糊搜索笔记：`memo notes -s "查询内容"`

## 创建笔记

- 添加新笔记：`memo notes -a`
  - 系统会打开一个交互式编辑器供您编写笔记内容。
- 快速添加笔记（仅提供标题）：`memo notes -a "笔记标题"`

## 编辑笔记

- 编辑现有笔记：`memo notes -e`
  - 系统会交互式地选择要编辑的笔记。

## 删除笔记

- 删除笔记：`memo notes -d`
  - 系统会交互式地选择要删除的笔记。

## 移动笔记

- 将笔记移动到指定文件夹：`memo notes -m`
  - 系统会交互式地选择笔记和目标文件夹。

## 导出笔记

- 将笔记导出为 HTML 或 Markdown 格式：`memo notes -ex`
  - 系统会使用 Mistune 工具对笔记内容进行 Markdown 处理。

## 限制

- 无法编辑包含图片或附件的笔记。
- 部分交互式操作可能需要终端权限。

## 注意事项

- 仅适用于 macOS。
- 需要确保 `Apple Notes.app` 可以正常使用。
- 如需进行自动化操作，请在系统设置 > 隐私与安全 > 自动化中授予相应权限。