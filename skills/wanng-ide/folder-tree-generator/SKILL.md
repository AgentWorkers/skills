---
name: folder-tree-generator
description: 生成目录结构的 ASCII 树形图或 JSON 表示形式。当您需要可视化文件层次结构、记录文件夹内容或调试目录布局时，可以使用此功能。
---
# 文件夹树生成器

这是一个实用工具，可以将目录结构以 ASCII 树形格式或 JSON 格式可视化。

## 使用方法

```bash
# Generate ASCII tree for current directory
node skills/folder-tree-generator/index.js

# Generate ASCII tree for specific directory
node skills/folder-tree-generator/index.js /path/to/dir

# Generate JSON output
node skills/folder-tree-generator/index.js --json

# Limit depth
node skills/folder-tree-generator/index.js --depth 2
```

## 选项

- `--json`：以 JSON 格式输出结果。
- `--depth <n>`：限制递归深度。
- `[dir]`：要扫描的目录（默认值：`.`）。

## 示例

**ASCII 输出：**
```
.
├── file1.txt
└── dir1
    ├── file2.txt
    └── file3.txt
```

**JSON 输出：**
```json
{
  "name": ".",
  "type": "directory",
  "children": [
    { "name": "file1.txt", "type": "file" },
    { "name": "dir1", "type": "directory", "children": [...] }
  ]
}
```