---
name: book-capture-obsidian
description: 将书籍元数据从照片或 Goodreads 的 CSV 导出文件中捕获并转换为 Obsidian Markdown 格式的笔记。这些元数据可用于提取条形码和 OCR 标识的 ISBN、丰富笔记内容、执行幂等的笔记更新操作、进行批量数据迁移以及生成仪表板。
---
# Book Capture Obsidian

执行此工作流以将书籍添加到或迁移到 Obsidian 文档库中。

## 工作流程

1. 如果目标 Obsidian 文档库路径尚未提供，向用户询问该路径。
2. 读取 `references/configuration.md` 文件并设置环境变量。
3. 选择一种导入模式：
   - 使用 `scripts/ingest_photo.py` 进行图片导入。
   - 使用 `scripts/migrate_goodreads_csv.py` 从 Goodreads 导入书籍数据。
4. 在从 Goodreads 迁移数据时，建议使用 `--group-by-shelf` 选项，并启用 Google 数据增强功能。
5. 使用 `scripts/upsert_obsidian_note.py` 命令将书籍信息插入 Obsidian 文档库。
6. 使用 `scripts/generate_dashboard.py` 命令刷新仪表板。
7. 运行验证和安全检查：
   - `sh scripts/run_ci_local.sh`
   - `sh scripts/security_scan_no_pii.sh`

## 必需参考文件

- `references/configuration.md`：包含运行时设置和可移植性相关内容。
- `references/data-contracts.md`：定义数据规范和输出格式。
- `references/migration-runbook.md`：描述从 Goodreads 导入书籍的详细步骤。
- `references/troubleshooting.md`：提供数据提取和合并过程中可能遇到的问题的解决方法。

## 操作规则

- 在进行批量写入之前，必须明确指定目标文档库的路径（`BOOK_CAPTURE_VAULT_PATH` 或 `--vault-path`）。
- 首先尝试提取书籍的条形码信息；如果条形码信息无法获取，则使用 OCR 技术进行识别。
- 保持文件名易于阅读（格式为 `书名 - 作者（出版社，出版年份）`）。
- 将 `shelf` 属性保留在书籍信息中，并在所有笔记中添加 `book` 标签。
- 当书籍有分卷元数据时，使用统一的系列标签（例如 `theexpanse`、`harrypotter`）；避免为每个分卷创建单独的笔记。
- 在更新过程中保留用户的自定义笔记内容。
- 确保重复执行该工作流时结果的一致性和幂等性（即每次执行都会得到相同的结果）。
- 不要在生成的文件中存储任何敏感信息或个人身份标识符。
- 简化书籍的前置信息（frontmatter）：仅保留 `title`、`author`、`publisher`、`year`、`isbn_10`、`isbn_13`、`cover`、`shelf`、`source`、`source_url`、`tags` 等字段；删除 `published_date`、`genre`、`status`、`date_started`、`date_read`、`needs_review`、`goodreads_book_id` 等字段。