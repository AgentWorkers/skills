---
name: Skreenshot
description: Organize, tag, search, and manage screenshots on macOS. Use when users need to: (1) find specific screenshots, (2) organize screenshots into folders by category/project, (3) search screenshot content via OCR, (4) bulk rename or move screenshots, (5) clean up old screenshots, or (6) integrate with CleanShot X or macOS screenshot tool.
---

# 屏幕截图管理

在 macOS 系统中，屏幕截图会大量生成——默认情况下，这些截图会被保存在桌面文件夹中，容易导致文件杂乱无章且容易被遗忘。本文档提供了一些实用的工作流程，帮助您更好地管理这些截图。

## 快速入门

**查找屏幕截图：**
```bash
# List recent screenshots (last 7 days)
find ~/Desktop -name "Screenshot*.png" -mtime -7 | head -20

# Search by content (OCR)
textsnip -i ~/Desktop/Screenshot*.png | grep -i "receipt"
```

**整理屏幕截图：**
```bash
# Move to categorized folders
mkdir -p ~/Pictures/Screenshots/{work,personal,receipts,memes}
mv ~/Desktop/Screenshot*.png ~/Pictures/Screenshots/personal/
```

## 默认的截图保存位置

macOS 默认将截图保存在 `~/Desktop` 文件夹中。您可以通过以下命令更改保存位置：
```bash
# Set custom location
defaults write com.apple.screencapture location ~/Pictures/Screenshots
killall SystemUIServer
```

## 截图文件命名规则

默认命名格式：`Screenshot YYYY-MM-DD at HH.MM.SS.png`

您还可以根据截图的上下文使用更智能的命名规则：
```bash
# Use script for batch rename with date + optional tags
python scripts/rename_screenshots.py --add-tags work,receipt
```

## 使用 OCR 工具搜索截图内容

您可以使用以下工具通过 OCR 技术搜索截图中的文本：
- **textsnip**（命令行工具）：`textsnip -i *.png | grep "搜索关键词"`
- **EasyOCR**（Python 库）：详见 `references/ocr-setup.md`
- **macOS 内置功能**：使用“Live Selection”功能（按 Cmd+Shift+4 然后拖动鼠标选择区域）

## 屏幕截图的组织策略

### 按项目/客户分类
```
Pictures/Screenshots/
├── client-acme/
├── client-globex/
└── personal/
```

### 按类别分类
```
Pictures/Screenshots/
├── receipts/
├── bugs/
├── inspiration/
├── memes/
└── reference/
```

### 按日期自动归档
```
Pictures/Screenshots/
├── 2026/
│   ├── 01-january/
│   ├── 02-february/
│   └── ...
```

## CleanShot X 的集成

如果您使用 CleanShot X：
- 可以将截图保存到自定义文件夹中（配置灵活）
- 支持 OCR 搜索功能（按 Cmd+Shift+O）
- 支持自动上传到云端（可选）

详细的工作流程请参阅 `references/cleancast-x.md`。

## 自动化脚本

### `scripts/rename_screenshots.py`
使用智能规则批量重命名截图文件（例如：添加日期、应用程序名称或标签）。

### `scripts/archive_old_screenshots.py`
将超过 N 天的旧截图移动到归档文件夹。

### `scripts/ocr_search.py`
根据文本内容搜索所有截图。

## 工作流程示例

**“找到显示错误信息的截图”**
1. 按日期范围搜索截图。
2. 使用 OCR 工具搜索错误信息。
3. 打开搜索结果。

**“整理桌面上的截图”**
1. 运行脚本将旧截图归档。
2. 将新截图移动到相应的分类文件夹中。
3. （如有需要）更新相关链接（如维基链接或文档链接）。

---

**参考资料：**
- `references/ocr-setup.md` - OCR 工具的设置与使用方法
- `references/cleancast-x.md` - CleanShot X 的使用指南
- `references/automation-patterns.md` - 高级自动化脚本示例