---
name: file-organizer-skill
description: 根据文件的扩展名或创建日期，将文件组织到相应的文件夹中。系统支持“Dry-Run”（预运行）、“Recursive”（递归）和“Undo”（撤销）功能。
---

# 文件整理器（黄金标准）

## 功能
- **智能排序**：可根据文件扩展名（默认）或日期（年/月）进行分组。
- **安全性**：支持冲突解决（自动重命名文件）、模拟执行（Dry Run）功能以及撤销操作。
- **深度清理**：提供递归扫描选项。
- **审计**：生成 `organize_history.json` 文件以记录操作记录。

## 使用方法

### 基本排序（按扩展名）
```bash
python3 scripts/organize.py /path/to/folder
```

### 按日期排序（年/月）
非常适合用于照片或档案文件的管理。
```bash
python3 scripts/organize.py /path/to/folder --date
```

### 模拟执行（Dry Run）
可以查看在不移动任何文件的情况下会发生什么变化。
```bash
python3 scripts/organize.py /path/to/folder --dry-run
```

### 撤销操作
使用 `organize_history.json` 文件恢复之前的文件状态。
```bash
python3 scripts/organize.py --undo /path/to/folder/organize_history.json
```

## 配置
通过修改 `scripts/organize.py` 文件中的 `get_default_mapping()` 函数，可以添加自定义的文件扩展名排序规则。