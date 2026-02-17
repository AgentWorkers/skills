---
name: sudoku
description: 从在线资源获取数独谜题，并将它们以 JSON 格式存储在工作区中；根据需要渲染谜题图像；之后再显示谜题的解答。
version: 2.1.2
homepage: https://github.com/odrobnik/sudoku-skill
metadata:
  openclaw:
    emoji: "🧩"
    requires:
      bins: ["python3"]
      python: ["requests", "Pillow", "lzstring"]
---
# 数独

## 概述

该工具用于获取、渲染和显示数独谜题。可以使用 `sudoku.py` 从 `sudokuonline.io` 获取新的数独谜题，生成可打印的 PDF 文件或图片，并显示谜题的答案。

有关保存的 JSON 格式的详细信息，请参阅 [DATA_FORMAT.md](references/DATA_FORMAT.md)。

## 可用的谜题类型

*   `kids4n`：4x4 的儿童数独
*   `kids4l`：带字母的 4x4 儿童数独
*   `kids6`：6x6 的儿童数独
*   `kids6l`：带字母的 6x6 儿童数独
*   `easy9`：经典的 9x9 数独（简单难度）
*   `medium9`：经典的 9x9 数独（中等难度）
*   `hard9`：经典的 9x9 数独（高难度）
*   `evil9`：经典的 9x9 数独（极高难度）

## 设置/要求

- 所需软件：`python3`
- 所需 Python 库：
  ```bash
  python3 -m pip install requests Pillow lzstring
  ```

## 获取谜题

该工具可以获取一个新的数独谜题并将其保存为 JSON 格式。默认输出为 JSON 格式（使用 `--text` 可以获取人类可读的文本格式）。

**获取一个经典的简单难度数独谜题：**
```bash
./scripts/sudoku.py get easy9
```

**获取一个 6x6 的儿童数独谜题：**
```bash
./scripts/sudoku.py get kids6
```

## 渲染谜题

可以将数独谜题渲染为图片或 PDF 文件。

**将最新的谜题渲染为 A4 大小的 PDF 文件（用于打印）：**
```bash
./scripts/sudoku.py render --pdf
```

**将最新的谜题渲染为清晰的 PNG 图片（用于查看）：**
```bash
./scripts/sudoku.py render
```

**通过短 ID 获取特定的谜题：**
```bash
./scripts/sudoku.py render --id a09f3680
```

## 显示谜题答案

可以显示最新谜题或特定谜题的答案。使用 `--id <short_id>`（例如 `a09f3680`）来指定要显示的谜题。

**将完整答案显示为可打印的 PDF 文件：**
```bash
./scripts/sudoku.py reveal --pdf
```

**将特定 ID 的完整答案显示为 PDF 文件：**
```bash
./scripts/sudoku.py reveal --id a09f3680 --image
```

**将完整答案显示为 PNG 图片：**
```bash
./scripts/sudoku.py reveal
```

**显示单个单元格的内容（第 3 行，第 7 列）：**
```bash
./scripts/sudoku.py reveal --cell 3 7
```

**显示特定的 3x3 区域（索引为 5）：**
```bash
./scripts/sudoku.py reveal --box 5
```

## 共享链接**

可以生成已保存谜题的共享链接。默认情况下，链接指向最新的谜题；使用 `--id <short_id>` 可以指定特定的谜题。

**生成一个 SudokuPad 共享链接（默认格式）：**
```bash
./scripts/sudoku.py share
```

**生成特定 ID 的共享链接：**
```bash
./scripts/sudoku.py share --id a09f3680
```

**生成 SCL 共享链接：**
```bash
./scripts/sudoku.py share --type scl
```

**Telegram 格式提示：**
建议将链接格式化为简短的按钮样式链接，并隐藏完整的 URL：`[Easy Classic \[<id>\]](<url>)`。