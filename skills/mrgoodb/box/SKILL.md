---
name: box
description: 通过 Box API 管理文件和文件夹。安全地上传、下载和共享内容。
metadata: {"clawdbot":{"emoji":"📦","requires":{"env":["BOX_ACCESS_TOKEN"]}}}
---
# Box
企业级云存储服务。

## 环境配置
```bash
export BOX_ACCESS_TOKEN="xxxxxxxxxx"
```

## 列出文件夹中的文件
```bash
curl "https://api.box.com/2.0/folders/0/items" -H "Authorization: Bearer $BOX_ACCESS_TOKEN"
```

## 上传文件
```bash
curl -X POST "https://upload.box.com/api/2.0/files/content" \
  -H "Authorization: Bearer $BOX_ACCESS_TOKEN" \
  -F "attributes={\"name\":\"file.txt\",\"parent\":{\"id\":\"0\"}}" \
  -F "file=@localfile.txt"
```

## 下载文件
```bash
curl "https://api.box.com/2.0/files/{fileId}/content" -H "Authorization: Bearer $BOX_ACCESS_TOKEN" -o file.txt
```

## 链接
- 文档：https://developer.box.com