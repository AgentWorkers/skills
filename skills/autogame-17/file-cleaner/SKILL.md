---
name: file-cleaner
description: 这是一种专门用于安全清理临时文件和目录的技能。当您需要删除临时文件、清除缓存或删除日志以释放空间或维护系统整洁时，可以使用该技能。出于安全考虑，该技能仅适用于 `temp/`, `logs/` 和 `cache/` 目录。
---
# 文件清理工具

该工具可安全地删除文件和目录，并内置了严格的安全检查机制，以防止意外删除重要的工作区文件。

## 使用方法

```bash
node skills/file-cleaner/index.js <path>
```

## 示例

- 清理指定的临时目录：
```bash
node skills/file-cleaner/index.js temp/my-experiment
```

- 清理日志文件：
```bash
node skills/file-cleaner/index.js logs/debug.log
```

## 安全性

- 仅删除以 `temp/`、`logs/` 或 `cache/` 开头的文件路径。
- 会阻止删除工作区根目录（`skills/`）或其他受保护的路径。