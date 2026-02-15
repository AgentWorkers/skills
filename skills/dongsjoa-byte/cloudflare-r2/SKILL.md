---
name: cloudflare-r2
description: 使用 `wrangler CLI` 将文件上传到 Cloudflare 的 R2 存储空间。适用于需要将图片、视频或其他文件上传到 R2 以用于 CDN 托管，或管理 R2 存储桶内容的情况。该命令会在执行“上传到 R2”、“上传到 Cloudflare”等操作时被触发。
metadata:
  {"openclaw": {"requires": {"bins": ["wrangler"]}, "install": [{"id": "node", "kind": "node", "package": "wrangler", "bins": ["wrangler"], "label": "Install Wrangler CLI (npm)"}]}}
---

# Cloudflare R2

在 Cloudflare R2 存储桶中上传和管理文件。

## 先决条件

- `wrangler` CLI：`npm install -g wrangler`
- R2 配置文件位于 `~/.config/cloudflare/r2.json`

## 配置格式

```json
{
  "bucket": "your-bucket-name",
  "accountId": "your-account-id",
  "publicDomain": "pub-xxx.r2.dev",
  "apiToken": "your-api-token"
}
```

## 快速上传

单个文件：
```bash
scripts/r2-upload.sh <local-file> [remote-path]
```

批量上传：
```bash
scripts/r2-upload.sh <directory> <remote-prefix>
```

## 手动命令

```bash
# Set credentials
export CLOUDFLARE_ACCOUNT_ID="$(jq -r .accountId ~/.config/cloudflare/r2.json)"
export CLOUDFLARE_API_TOKEN="$(jq -r .apiToken ~/.config/cloudflare/r2.json)"
BUCKET=$(jq -r .bucket ~/.config/cloudflare/r2.json)

# Upload
wrangler r2 object put "$BUCKET/path/to/file.png" --file local.png --remote

# List objects
wrangler r2 object list $BUCKET --prefix "path/" --remote

# Delete
wrangler r2 object delete "$BUCKET/path/to/file.png" --remote
```

## 公共 URL

上传完成后，文件可以通过以下地址访问：
```
https://<publicDomain>/<remote-path>
```

示例：`https://pub-xxx.r2.dev/article/image.png`