# Catbox/Litterbox 文件上传工具

可将文件上传至 catbox.moe（永久存储）或 litterbox.catbox.moe（临时存储）。

## 使用方法

**上传至 Litterbox（临时存储，推荐方式）：**
```bash
python upload.py /path/to/file.mp4
python upload.py /path/to/file.mp4 --time 24h
```

**上传至 Catbox（永久存储）：**
```bash
python upload.py /path/to/file.png --service catbox --userhash YOUR_HASH
```

## 选项

- `--service`：`litterbox`（默认）或 `catbox`
- `--time`：文件在 Litterbox 中的过期时间：`1h`、`12h`、`24h`、`72h`（默认为 `24h`）
- `--userhash`：Catbox 账户哈希值（可选，用于追踪文件上传者）

## 限制

| 服务 | 最大文件大小 | 存储时长 |
|---------|----------|----------|
| Litterbox | 1 GB | 1小时至72小时 |
| Catbox | 200 MB | 永久存储 |

## 返回值

上传成功后，会返回文件的 URL。