---
name: publer-post
description: 通过 Publer API 将内容发布到社交媒体。适用于安排或发布 TikTok（轮播图、视频）、Instagram、Facebook、Twitter/X 或任何支持 Publer 的平台。该 API 支持媒体上传、帖子创建、任务调度以及任务状态监控。适用于所有需要“将内容发布到 TikTok”、“安排帖子发布”、“在社交媒体上发布内容”或“将内容上传到 Publer”的场景。
metadata:
  openclaw:
    emoji: 📱
    requires:
      bins: ["python3"]
      env: ["PUBLER_API_KEY", "PUBLER_WORKSPACE_ID"]
      packages: ["requests"]
    primaryEnv: PUBLER_API_KEY
    install:
      - id: python-requests
        kind: pip
        package: requests
        label: Install Python requests library
---
# Publer Post

通过 Publer API 发布和安排社交媒体内容。

## 先决条件

**Python 依赖项：**
```bash
pip install -r requirements.txt
```

**环境变量**（请存储在 TOOLS.md 文件中或在运行前设置）：
- `PUBLER_API_KEY` — 来自 Publer 的 API 密钥（需要企业计划）
- `PUBLER_WORKSPACE_ID` — 你的工作空间 ID
- `PUBLER_TIKTOK_ACCOUNT_ID` — TikTok 账户 ID（可选，可通过 `accounts` 命令获取）

## 脚本：`scripts/publer.py`

### 列出账户
```bash
python3 scripts/publer.py accounts
```
首先使用此命令来获取账户 ID。

### 上传媒体文件
```bash
python3 scripts/publer.py upload slide_1.jpg slide_2.jpg slide_3.jpg
```
返回媒体文件的 ID（每个 ID 占一行，格式为 JSON）。将这些 ID 收集起来，用于后续的发布操作。

### 立即发布 TikTok 轮播视频
```bash
python3 scripts/publer.py post \
  --account-id $PUBLER_TIKTOK_ACCOUNT_ID \
  --type photo \
  --title "Post title (max 90 chars)" \
  --text "Caption with #hashtags" \
  --media-ids id1,id2,id3,id4,id5,id6,id7,id8
```

### 安排 TikTok 轮播视频的发布时间
```bash
python3 scripts/publer.py post \
  --account-id $PUBLER_TIKTOK_ACCOUNT_ID \
  --type photo \
  --title "Post title" \
  --text "Caption" \
  --media-ids id1,id2,id3 \
  --schedule "2025-06-01T09:00:00Z"
```

### 干运行（预览数据包）
添加 `--dry-run` 选项，以在不发送数据的情况下打印 JSON 数据包。

### 检查任务状态
```bash
python3 scripts/publer.py job-status <job_id>
```

## 工作流程：发布 TikTok 轮播视频
1. 上传所有幻灯片图片 → 收集媒体文件的 ID
2. 使用 `post` 命令，指定发布类型为 `photo`，并提供标题、说明文字及标签，同时传入逗号分隔的媒体文件 ID
3. 脚本会持续监控任务状态，直到任务完成 → 确认发布成功

## 选项：
- `--privacy`：PUBLIC_TO_EVERYONE（默认值）、MUTUAL_follow FRIENDS、FOLLOWER_OF_CREATOR、SELF_ONLY
- `--auto-music` / `--no-auto-music`：是否自动为轮播视频添加音乐（默认值为开启）
- `--no-poll`：不等待任务完成即可提交发布请求

## API 参考
有关端点的详细信息，请参阅 [references/api.md](references/api.md)。