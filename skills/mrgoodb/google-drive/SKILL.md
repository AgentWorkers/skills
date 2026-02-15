---
name: google-drive
description: 管理 Google Drive 文件和文件夹。通过 Drive API 进行文件的上传、下载、共享和整理。
metadata: {"clawdbot":{"emoji":"📁","requires":{"env":["GOOGLE_ACCESS_TOKEN"]}}}
---

# Google Drive

云文件存储与共享服务。

## 环境配置

```bash
export GOOGLE_ACCESS_TOKEN="ya29.xxxxxxxxxx"
```

## 列出文件

```bash
curl "https://www.googleapis.com/drive/v3/files?pageSize=20" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 搜索文件

```bash
curl "https://www.googleapis.com/drive/v3/files?q=name%20contains%20'report'" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 获取文件元数据

```bash
curl "https://www.googleapis.com/drive/v3/files/{fileId}?fields=*" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 下载文件

```bash
curl "https://www.googleapis.com/drive/v3/files/{fileId}?alt=media" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -o downloaded_file.pdf
```

## 上传文件

```bash
curl -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -F "metadata={\"name\": \"myfile.txt\"};type=application/json" \
  -F "file=@localfile.txt"
```

## 创建文件夹

```bash
curl -X POST "https://www.googleapis.com/drive/v3/files" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Folder", "mimeType": "application/vnd.google-apps.folder"}'
```

## 共享文件

```bash
curl -X POST "https://www.googleapis.com/drive/v3/files/{fileId}/permissions" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "reader", "type": "user", "emailAddress": "user@example.com"}'
```

## 相关链接：
- 控制台：https://console.cloud.google.com/apis/library/drive.googleapis.com
- 文档：https://developers.google.com/drive/api/v3/reference