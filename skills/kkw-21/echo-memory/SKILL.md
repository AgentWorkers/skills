# 回声内存（Echo Memory）

使用 Luhmann 编码将 OpenClaw 的 Markdown 内存文件同步到 Supabase 数据库。解析、编码内存数据，并将数据从本地工作区上传到云存储。

## 命令

```bash
echo-memory sync          # Parse + encode + embed + upsert to Supabase
echo-memory restore       # Restore markdown files from Supabase
echo-memory status        # Show sync status and diff
```

## 选项

- `--dry-run` — 预览更改内容，不进行实际写入
- `--incremental` — 仅同步已更改的文件（通过 git diff 工具检测差异）