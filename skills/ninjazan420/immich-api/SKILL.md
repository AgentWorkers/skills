---
name: immich-api
description: |
  Immich Photo Management API Bridge. Use for interacting with self-hosted Immich instances via REST API.
  Triggers when: (1) User wants to manage photos, albums, or assets in Immich, (2) Building automation around photo backups, 
  (3) Searching or organizing media, (4) User management in Immich, (5) Upload/download photos via API, 
  (6) Getting album or library information, (7) Working with Immich jobs/queues, (8) Any Immich-related photo tasks
---

# Immich API Bridge

## 配置

### 选项 1：环境变量

**Windows（PowerShell）：**
```powershell
$env:IMMICH_URL = "https://your-immich-instance.com"
$env:IMMICH_API_KEY = "your-api-key-here"
```

**Linux/macOS（bash）：**
```bash
export IMMICH_URL="https://your-immich-instance.com"
export IMMICH_API_KEY="your-api-key-here"
```

**在 Immich 中生成 API 密钥：** 用户资料 → API 密钥 → 创建 API 密钥

### 选项 2：CLI 参数
```bash
python scripts/upload_photos.py --url "https://your-immich.com" --api-key "your-key" --folder ./photos
python scripts/download_album.py --url "https://your-immich.com" --api-key "your-key" --album-id "abc123" --output ./downloads
```

## 快速入门

### 认证
```bash
# Test connection
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/server-info/ping"
```

### 基本 URL
```
{IMMICH_URL}/api
```

## 常见操作

### 相册
```bash
# List albums
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/albums"

# Create album
curl -X POST -H "x-api-key: $IMMICH_API_KEY" -H "Content-Type: application/json" \
  -d '{"albumName":"My Album"}' "$IMMICH_URL/api/albums"

# Get album assets
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/albums/{albumId}"
```

### 资产
```bash
# Get all assets (paginated)
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/assets?limit=100"

# Upload asset
curl -X POST -H "x-api-key: $IMMICH_API_KEY" \
  -F "file=@/path/to/photo.jpg" \
  "$IMMICH_URL/api/assets"

# Get thumbnail
curl -H "x-api-key: $IMMICH_API_KEY" \
  "$IMMICH_URL/api/assets/{assetId}/thumbnail?format=jpeg" -o thumb.jpg

# Get original file
curl -H "x-api-key: $IMMICH_API_KEY" \
  "$IMMICH_URL/api/assets/{assetId}/original" -o original.jpg
```

### 用户
```bash
# List users
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/users"

# Get current user
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/user/me"
```

### 搜索
```bash
# Search assets
curl -X POST -H "x-api-key: $IMMICH_API_KEY" -H "Content-Type: application/json" \
  -d '{"query":"beach","take":10}' "$IMMICH_URL/api/search/assets"
```

### 库
```bash
# List libraries
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/libraries"

# Scan library
curl -X POST -H "x-api-key: $IMMICH_API_KEY" \
  "$IMMICH_URL/api/libraries/{libraryId}/scan"
```

### 作业
```bash
# Get job statuses
curl -H "x-api-key: $IMMICH_API_KEY" "$IMMICH_URL/api/jobs"

# Trigger job (e.g., thumbnail generation)
curl -X POST -H "x-api-key: $IMMICH_API_KEY" -H "Content-Type: application/json" \
  -d '{"jobName":"thumbnail-generation","force":true}' "$IMMICH_URL/api/jobs"
```

## 脚本使用

使用 `scripts/` 目录中的脚本进行复杂操作：
- `upload_photos.py` - 批量上传照片
- `download_album.py` - 下载整个相册
- `sync_library.py` - 同步外部库

请参阅 `references/api-endpoints.md` 以获取完整的 API 端点参考信息。