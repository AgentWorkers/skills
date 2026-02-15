---
name: paperless
description: 通过 ppls CLI 与 Paperless-NGX 文档管理系统进行交互。可以执行搜索、检索、上传和整理文档等操作。
emoji: 📄
metadata: {"clawdbot":{"requires":{"bins":["ppls"],"env":["PPLS_HOSTNAME","PPLS_TOKEN"]},"install":[{"id":"node","kind":"node","package":"@nickchristensen/ppls","bins":["ppls"],"label":"Install ppls CLI (npm/bun)"}]}}
---

# Paperless-NGX 命令行界面（Paperless-NGX CLI）

使用 `ppls` 在 Paperless-NGX 中搜索和管理文档。

## 设置

```bash
npm install -g @nickchristensen/ppls
ppls config set hostname http://your-paperless-host
ppls config set token your-api-token
```

## 搜索文档

```bash
# By name
ppls documents list --name-contains "invoice" --json

# By date range
ppls documents list --created-after 2024-01-01 --created-before 2024-12-31 --json

# By tag (OR — any of these tags)
ppls documents list --tag 5 --tag 12 --json

# By tag (AND — must have all)
ppls documents list --tag-all 5,12 --json

# Exclude tags
ppls documents list --tag-not 3 --json

# By correspondent
ppls documents list --correspondent 7 --json

# By document type
ppls documents list --document-type 2 --json

# Documents missing metadata
ppls documents list --no-correspondent --json
ppls documents list --no-tag --json

# Recently added/modified
ppls documents list --added-after 2024-06-01 --json
ppls documents list --modified-after 2024-06-01 --json

# Combine filters
ppls documents list --correspondent 7 --created-after 2024-01-01 --tag 5 --json
```

## 查看和下载文档

```bash
# Get full document details (includes OCR content)
ppls documents show 1234 --json

# Download single document
ppls documents download 1234 --output ~/Downloads/doc.pdf

# Download multiple documents
ppls documents download 1234 5678 --output-dir ~/Downloads

# Download original (pre-processed) version
ppls documents download 1234 --original
```

## 上传文档

```bash
# Simple upload (Paperless auto-processes)
ppls documents add scan.pdf

# With metadata
ppls documents add receipt.pdf \
  --title "Store Receipt" \
  --correspondent 5 \
  --document-type 2 \
  --tag 10
```

## 管理元数据

```bash
# List tags/correspondents/document-types
ppls tags list --json
ppls correspondents list --json
ppls document-types list --json

# Create new
ppls tags add "Tax 2024" --color "#ff0000"
ppls correspondents add "New Vendor"
ppls document-types add "Contract"

# Update document metadata
ppls documents update 1234 --title "New Title" --correspondent 5 --tag 10
```

## 提示：

- **进行 AI/自动化操作时，请务必使用 `--json` 格式**——这是最易于解析的格式。
- **日期格式**：`YYYY-MM-DD` 或完整的 ISO 8601 格式。
- **文档 ID 是数字**——可以使用 `list --json` 命令来查找它们。
- **过滤器可以重复使用**：`--tag 1 --tag 2` 或 `--tag 1,2` 都可以。
- **分页**：对于大量结果，可以使用 `--page` 和 `--page-size` 参数进行分页显示。

## 链接：

- [ppls 在 GitHub 上的仓库](https://github.com/NickChristensen/ppls)
- [Paperless-NGX 文档](https://docs.paperless-ngx.com/)