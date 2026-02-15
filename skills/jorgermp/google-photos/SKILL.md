---
name: google-photos
description: 管理 Google Photos 图库。可以上传照片、创建相册以及查看图库中的内容。适用于用户需要备份、整理或通过 Google Photos 共享图片的场景。
metadata: {"openclaw":{"emoji":"📸","requires":{"apis":["photoslibrary.googleapis.com"]}}}
---

# Google Photos

本技能提供了一种与 Google Photos Library API 交互的方式，以实现照片管理的自动化。

## 设置

1. **启用 API**：在您的 Google Cloud Console 项目中启用“Google Photos Library API”。
2. **凭据**：下载您的 OAuth 2.0 客户端 ID 凭据，并将其保存为 `credentials.json` 文件。
3. **环境**：本技能使用位于其所在文件夹中的 Python 虚拟环境。

## 使用方法

所有命令均通过 `scripts/gphotos.py` 脚本执行。

### 列出相册
用于查找现有相册的 ID。
```bash
./scripts/gphotos.py --action list --credentials /path/to/credentials.json --token /path/to/token.pickle
```

### 创建新相册
```bash
./scripts/gphotos.py --action create --title "Vacations 2026" --credentials /path/to/credentials.json --token /path/to/token.pickle
```

### 上传照片
您可以选择指定 `--album-id` 参数，将照片上传到指定的相册中。
```bash
./scripts/gphotos.py --action upload --photo "/path/to/image.jpg" --album-id "ALBUM_ID" --credentials /path/to/credentials.json --token /path/to/token.pickle
```

## 隐私与安全

- 本技能仅能访问您上传的照片或明确分享给应用程序的照片。
- 凭据和令牌会存储在本地，必须妥善保管。
- 请勿共享您的 `credentials.json` 或 `token.pickle` 文件。