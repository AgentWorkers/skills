---
name: r2
description: Cloudflare R2存储管理：通过rclone进行设置、上传、下载和同步操作
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["rclone"]},"env":["R2_CONFIG"],"install":[{"id":"rclone","kind":"shell","command":"curl -fsSL https://rclone.org/install.sh | sudo bash","label":"Install rclone"}]}}
---

# r2 ☁️

使用 rclone 管理 Cloudflare 的 R2 存储服务。

## 安装

```bash
curl -fsSL https://rclone.org/install.sh | sudo bash
```

## 所需凭据

在控制面板中，将 `R2_CONFIG` 设置为以下 JSON 格式：

```json
{
  "access_key_id": "YOUR_ACCESS_KEY_ID",
  "secret_access_key": "YOUR_SECRET_ACCESS_KEY",
  "endpoint": "https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com",
  "bucket": "your-bucket-name"
}
```

**从 Cloudflare 获取凭据：**
1. 访问 https://dash.cloudflare.com → R2
2. 创建具有对象读取/写入/列出权限的 API 令牌
3. 复制账户 ID（来自 R2 控制面板 URL）
4. 端点格式：`https://<account_id>.r2.cloudflarestorage.com`

## 设置

```bash
# Quick setup
r2-setup --config '{"access_key_id":"...","secret_access_key":"...","endpoint":"...","bucket":"..."}'
```

或者以交互式方式运行：
```bash
./skills/r2/scripts/setup.sh
```

## 命令

### 上传

```bash
r2-upload /path/to/file.txt              # Upload single file
r2-upload /path/to/folder/               # Upload folder contents
r2-upload /path/to/file.txt --bucket other-bucket  # Upload to specific bucket
```

### 下载

```bash
r2-download file.txt /local/path/        # Download single file
r2-download folder/ /local/              # Download folder
r2-download file.txt                     # Download to current dir
```

### 列出

```bash
r2-ls                                    # List bucket contents
r2-ls my-bucket                          # List specific bucket
r2-ls --long                             # Long format with sizes
```

### 同步（单向）

```bash
r2-sync /local/folder/ r2:bucket/        # Local → R2
r2-sync r2:bucket/ /local/folder/        # R2 → Local
r2-sync /local/ r2:bucket/ --delete      # Mirror (delete extra files on dest)
```

### 删除

```bash
r2-rm file.txt                           # Delete single file
r2-rm folder/                            # Delete folder contents
r2-purge my-bucket                       # Delete all files in bucket
```

## 显示凭据

```bash
./skills/r2/scripts/show-creds.sh           # Human-readable
./skills/r2/scripts/show-creds.sh --raw     # JSON format for UI
```

## 直接使用 rclone 命令

```bash
# Copy files
rclone copy /local/file.txt r2:bucket/

# Sync with progress
rclone sync /local/ r2:bucket/ -P

# Check disk usage
rclone size r2:bucket
```

## 配置位置

- **环境变量配置**：`~/.config/r2/config.json`（或在控制面板中设置 `R2_CONFIG`）
- **rclone 配置文件**：`~/.config/rclone/rclone.conf`
- **命名远程存储**：`r2`

## 故障排除

### 403 访问拒绝
令牌权限不足。请在 Cloudflare 中更新 API 令牌，确保包含以下权限：
- 对象读取 ✅
- 对象写入 ✅
- 对象列出 ✅

### 未找到桶
请先创建相应的桶：
```bash
rclone mkdir r2:bucket-name
```