---
name: workspace-files
description: 请在 OpenClaw 工作区沙箱内安全地操作文件。该沙箱仅用于列出目录、读取文本文件、写入文本文件以及按文件名在 `~/.openclaw/workspace` 目录中搜索文件。
metadata: {"clawdbot":{"notes":["Sandbox limited to /home/cmart/.openclaw/workspace"]}}
---
# 工作区文件

这些文件操作仅限于 OpenClaw 工作区沙箱环境。

## 沙箱环境

所有文件路径必须位于以下目录内：
`/home/cmart/.openclaw/workspace`

请勿在沙箱环境之外的路径上使用这些命令。

## 快速命令

- 列出目录内容  
  `/{baseDir}/scripts/workspace-files.sh list-dir "01_AGENTS"`

- 读取文本文件  
  `/{baseDir}/scripts/workspace-files.sh read-file "TOOLS.md"`

- 写入文本文件  
  `/{baseDir}/scripts/workspace-files.sh write-file "07_OUTPUTS/test.txt" "hola mundo"`

- 按名称搜索文件  
  `/{baseDir}/scripts/workspace-files.sh search-files "SKILL.md"`

## 命令参考

### list-dir

`/{baseDir}/scripts/workspace-files.sh list-dir "<相对路径>"`

示例：
- `/{baseDir}/scripts/workspace-files.sh list-dir "."`
- `/{baseDir}/scripts/workspace-files.sh list-dir "01_AGENTS"`

### read-file

`/{baseDir}/scripts/workspace-files.sh read-file "<相对路径>"`

示例：
- `/{baseDir}/scripts/workspace-files.sh read-file "TOOLS.md"`
- `/{baseDir}/scripts/workspace-files.sh read-file "01_AGENTS/_REGISTRY.md"`

### write-file

`/{baseDir}/scripts/workspace-files.sh write-file "<相对路径>" "<内容>"`

示例：
- `/{baseDir}/scripts/workspace-files.sh write-file "07_OUTPUTS/demo.txt" "contenido de prueba"`

### search-files

`/{baseDir}/scripts/workspace-files.sh search-files "<搜索模式>"`

示例：
- `/{baseDir}/scripts/workspace-files.sh search-files "SKILL.md"`
- `/{baseDir}/scripts/workspace-files.sh search-files "compa"`

## 注意事项

- 请在工作区沙箱内仅使用相对路径。
- 这些命令仅用于文本文件和目录的查看操作。
- 不适用于二进制文件的编辑。
- 请注意，这些命令不保证能在沙箱环境之外具有写入权限。