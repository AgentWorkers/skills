---
name: nextcloud
description: 通过 WebDAV API 访问 Nextcloud 文件。可以同步文档以用于 RAG（检索、聚合和生成）索引，上传文件，管理文件夹，并自动化工作流程。适用于浏览云文件、将文件同步到本地 RAG 系统、上传录制内容，或执行任何与 Nextcloud 文件相关的操作。
---
# Nextcloud 技能

通过 WebDAV API 操作 Nextcloud 文件存储系统。

## 设置

配置凭据（只需运行一次）：

```bash
python3 nextcloud_helper.py setup \
  --url https://cloud.example.com \
  --user admin \
  --pass "your-app-password" \
  --rag-path /home/user/data/work-sync
```

或者使用环境变量：
```bash
export NEXTCLOUD_URL="https://cloud.example.com"
export NEXTCLOUD_USER="admin"
export NEXTCLOUD_PASS="your-app-password"
export NEXTCLOUD_RAG_PATH="/home/user/data/work-sync"
```

## 快速入门

```bash
cd /path/to/skill/scripts

# List files
python3 nextcloud_helper.py list Documents/

# Upload file
python3 nextcloud_helper.py upload local.txt Documents/notes.txt

# Download file  
python3 nextcloud_helper.py download Documents/notes.txt local.txt

# Sync folder to local
python3 nextcloud_helper.py sync Documents/Work/ --local /home/user/data/work
```

## 大文件上传

对于大于 50MB 的文件，使用 `--http11` 选项以避免 HTTP/2 协议错误：

```bash
python3 nextcloud_helper.py upload large_video.mp4 Videos/movie.mp4 --http11
```

## RAG 同步工作流程

1. 同步远程文件夹：
```python
from nextcloud_helper import sync_down
result = sync_down(["Documents/Notes", "Documents/Transcripts"], 
                  "/home/user/data/work-sync")
print(f"Synced {result['synced']} files")
```

2. 使用您喜欢的工具重新索引 RAG 数据：
```bash
# Example with your RAG system
python3 rag_helper.py reindex
```

## 自动检测

查找最近的录制文件：
```python
from nextcloud_helper import find_files_by_ext
recordings = find_files_by_ext("Recordings", 
                               (".mp3", ".mp4", ".m4a"),
                               max_age_hours=24)
```

## 参考文档

- [WebDAV API 参考](references/webdav-api.md) - 完整的 API 端点文档

## 常见问题

| 问题 | 解决方案 |
|-------|----------|
| HTTP/2 协议错误 | 上传时使用 `--http11` 选项 |
| 上传时返回 000 状态码 | 连接中断，请使用 `--http11` 重新尝试 |
| 大文件上传失败 | 增加超时时间或使用分块上传 |
| 认证失败 | 检查 Nextcloud 设置中的应用程序密码 |