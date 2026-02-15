---
name: zotero
description: 通过 Web API 管理 Zotero 参考文献库：支持搜索、按 DOI/ISBN/PMID 列出文献（包含重复项检测功能）、删除或标记文献为“已丢弃”、更新元数据和标签、导出为 BibTeX/RIS/CSL-JSON 格式、从文件批量添加文献、检查 PDF 附件中的内容、实现引用之间的交叉引用、通过 CrossRef 查找缺失的 DOI，以及获取开放获取的 PDF 文档。该工具支持输出 JSON 格式的数据，便于脚本化操作。适用于用户需要查询学术参考文献、管理引用、整理文献库、获取论文对应的 PDF 文件、导出参考书目或专门使用 Zotero 的场景。
metadata: {"clawdbot":{"emoji":"📚","requires":{"env":["ZOTERO_API_KEY","ZOTERO_USER_ID"]},"primaryEnv":"ZOTERO_API_KEY"}}
---

# Zotero 技能

通过 REST API v3 与 Zotero 个人库或群组库进行交互。

## 设置

需要两个环境变量：

```
ZOTERO_API_KEY   — Create at https://www.zotero.org/settings/keys/new
ZOTERO_USER_ID   — Found on the same page (numeric, not username)
```

对于群组库，请将 `ZOTERO_USER_ID` 更改为 `ZOTERO_GROUP_ID`。

可选的环境变量：CrossRef/Unpaywall 优雅请求池（可提高 DOI 查找成功率）：

```
CROSSREF_EMAIL   — Your email (optional; uses fallback if unset)
```

如果缺少凭据，请告知用户所需信息，并将他们引导至密钥创建页面。

## CLI 脚本

所有操作均使用 `scripts/zotero.py`（Python 3，无外部依赖）。

```bash
python3 scripts/zotero.py <command> [options]
```

### 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `items` | 列出顶级条目 | `zotero.py items --limit 50` |
| `search` | 按查询条件搜索 | `zotero.py search "cognitive load"` |
| `get` | 获取条目详细信息及附件 | `zotero.py get ITEMKEY` |
| `collections` | 列出所有收藏夹 | `zotero.py collections` |
| `tags` | 列出所有标签 | `zotero.py tags` |
| `children` | 获取条目的附件/笔记 | `zotero.py children ITEMKEY` |
| `add-doi` | 通过 DOI 添加条目（支持去重） | `zotero.py add-doi 10.1234/example` |
| `add-isbn` | 通过 ISBN 添加条目（支持去重） | `zotero.py add-isbn 978-0-123456-78-9` |
| `add-pmid` | 通过 PubMed ID 添加条目 | `zotero.py add-pmid 12345678` |
| `delete` | 将条目移至回收站（可恢复） | `zotero.py delete KEY1 KEY2 --yes` |
| `update` | 修改条目元数据/标签 | `zotero.py update KEY --add-tags "new"` |
| `export` | 导出为 BibTeX/RIS/CSL-JSON | `zotero.py export --format bibtex` |
| `batch-add` | 从文件批量添加条目 | `zotero.py batch-add dois.txt --type doi` |
| `check-pdfs` | 检查哪些条目有/没有 PDF | `zotero.py check-pdfs` |
| `crossref` | 将引用与库中的条目进行匹配 | `zotero.py crossref bibliography.txt` |
| `find-dois` | 通过 CrossRef 查找并添加缺失的 DOI | `zotero.py find-dois --limit 10` |
| `fetch-pdfs` | 为条目获取开放获取的 PDF | `zotero.py fetch-pdfs --dry-run` |

### 全局标志

- `--json` — 以 JSON 格式输出结果（适用于 items、search、get 命令）

### 常见选项

- `--limit N` — 返回的最大条目数量（默认值：25）
- `--sort FIELD` — 按 `dateModified`、`title`、`creator`、`date` 排序
- `--direction asc|desc` — 排序方向
- `--collection KEY` — 按收藏夹过滤或添加条目到收藏夹
- `--type TYPE` — 按条目类型过滤（journalArticle、book、conferencePaper 等）
- `--tags "tag1,tag2"` — 在创建条目时添加标签
- `--force` — 在添加条目时忽略重复项

## 工作流程

### 通过 DOI 添加论文

```bash
python3 zotero.py add-doi "10.1093/jamia/ocaa037" --tags "review"
# Warns if already in library. Use --force to override.
```

**去重机制：** 将 DOI 转换为元数据，根据第一作者在库中搜索对应的条目，并比较 DOI 字段。

### 从文件批量添加条目

```bash
# One identifier per line, # for comments
python3 zotero.py batch-add dois.txt --type doi --tags "imported"
```

**去重处理：** 报告添加成功/失败/失败的条目数量。

### 导出参考文献

```bash
python3 zotero.py export --format bibtex --output refs.bib
python3 zotero.py export --format csljson --collection COLLKEY
```

### 更新标签/元数据

```bash
python3 zotero.py update ITEMKEY --add-tags "important" --remove-tags "unread"
python3 zotero.py update ITEMKEY --title "Corrected Title" --date "2024"
python3 zotero.py update ITEMKEY --doi "10.1234/example"
python3 zotero.py update ITEMKEY --url "https://example.com/paper"
python3 zotero.py update ITEMKEY --add-collection COLLKEY
```

### 删除条目

```bash
python3 zotero.py delete KEY1 KEY2 --yes           # Trash (recoverable, default)
python3 zotero.py delete KEY1 --permanent --yes    # Permanent delete
```

### 引用交叉引用

```bash
python3 zotero.py crossref my-paper.txt
```

从文本中提取 `Author (Year)` 模式，并与库中的条目进行匹配。

### 查找缺失的 DOI

```bash
# Dry run (default) — show matches without writing anything
python3 zotero.py find-dois --limit 20

# Actually write DOIs to Zotero
python3 zotero.py find-dois --apply

# Filter by collection
python3 zotero.py find-dois --collection COLLKEY --apply
```

扫描缺少 DOI 的 `journalArticle` 和 `conferencePaper` 条目，通过 CrossRef 查询，并根据标题相似度（>85%）、确切年份以及第一作者的姓氏进行匹配。默认为干运行模式（使用 `--apply` 命令进行实际操作）；仅修改 DOI 字段，不更改其他元数据。每次向 CrossRef 发送请求之间有 1 秒的延迟（采用优雅请求池机制）。

### 获取开放获取的 PDF

```bash
# Dry run — show which PDFs are available and from where
python3 zotero.py fetch-pdfs --dry-run --limit 10

# Fetch and attach as linked URLs (no storage quota used)
python3 zotero.py fetch-pdfs --limit 20

# Also save PDFs locally
python3 zotero.py fetch-pdfs --download-dir ./pdfs

# Upload to Zotero storage instead of linked URL
python3 zotero.py fetch-pdfs --upload --limit 10

# Only try specific sources
python3 zotero.py fetch-pdfs --sources unpaywall,semanticscholar
```

按顺序尝试三个开放获取资源：Unpaywall → Semantic Scholar → DOI 内容协商。默认情况下，会创建带有链接的 PDF 附件（无需占用 Zotero 的存储空间）。使用 `--upload` 命令将 PDF 上传到 Zotero 存储空间；使用 `--download-dir` 命令将 PDF 保存到本地。

**资源来源：** `unpaywall`、`semanticscholar`、`doi`（默认使用全部三个）

**速率限制：** 在使用 Unpaywall 和 Semantic Scholar 之间有 1 秒的延迟；在请求 DOI 之间有 2 秒的延迟。

### 使用 JSON 进行脚本编程

```bash
python3 zotero.py --json items --limit 100 | jq '.items[].DOI'
python3 zotero.py --json get ITEMKEY | jq '.title'
```

## 注意事项

- 无外部依赖，仅使用 Python 3 标准库（urllib、json、 argparse）
- 执行写入操作需要具有写入权限的 API 密钥
- 如果 Zotero 的翻译服务器不可用（返回 503 错误），则会使用 CrossRef 代替进行 DOI 查找
- **输入验证：** DOI 必须遵循 `10.xxxx/...` 的格式；条目键应为 8 个字符的字母数字组合（例如 `VNPN6FHT`）；ISBN 必须是有效的校验和。
- `check-pdfs` 会获取所有条目的 PDF 文件；对于包含 500 条目以上的库，此操作可能较慢
- `fetch-pdfs` 也会处理所有条目；可以使用 `--collection` 参数来限定处理范围
- 程序的速率限制较为宽松；批量添加操作会在条目之间添加 1 秒的延迟
- 有关常见错误和故障排除的详细信息，请参阅 [references/troubleshooting.md](references/troubleshooting.md)