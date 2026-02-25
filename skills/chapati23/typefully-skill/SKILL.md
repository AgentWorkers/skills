---
name: typefully
description: 在 Typefully 上，您可以创建、安排发布时间、列出待发布的帖子、编辑以及删除这些帖子。该工具支持单条推文（Twitter）、推文串（Threads），以及跨多个平台的帖子（如 X、LinkedIn、Threads、Bluesky、Mastodon）。当用户需要通过 Typefully 来起草或管理社交媒体帖子时，可以使用该工具。
version: 1.2.0
homepage: https://github.com/gisk0/typefully-skill
requires:
  env:
    - TYPEFULLY_API_KEY
  tools:
    - curl
    - python3
---
# Typefully Skill

通过 v2 API 管理 Typefully 的草稿。

## 设置

1. 通过以下方式设置您的 API 密钥：
   - 环境变量：`export TYPEFULLY_API_KEY=your-key`
   - 密码存储：`pass insert typefully/api-key`
2. （可选）设置您的社交账号 ID：
   - 环境变量：`export TYPEFULLY_SOCIAL_SET_ID=123456`
   - 密码存储：`pass insert typefully/social-set-id`
   - 如果未设置，脚本会自动检测（如果存在多个账户，则会报错——使用 `list-social-sets` 来查找您的账户）。
3. 在 Typefully 的 **设置 → API** 中启用“开发模式”，以便在用户界面中查看草稿 ID。

## 脚本用法

```bash
bash scripts/typefully.sh <command> [options]
```

### 命令

| 命令 | 描述 |
|---------|-------------|
| `list-drafts [status] [limit]` | 列出草稿。状态：`draft`、`scheduled`、`published`（默认：全部）。默认限制数量：10。|
| `create-draft <text> [--thread] [--platform x,linkedin,...] [--schedule <iso8601\|next-free-slot>]` | 创建草稿。对于多线程帖子，使用 `\n---\n` 分隔。可以使用 `-` 或省略文本以从标准输入读取内容。默认平台：x。|
| `get-draft <draft_id>` | 获取单个草稿的详细信息。|
| `edit-draft <draft_id> <text> [--thread] [--platform x,linkedin]` | 更新草稿内容。支持使用 `--thread` 进行多线程编辑。|
| `schedule-draft <draft_id> <iso8601\|next-free-slot\|now>` | 安排草稿的发布时间或立即发布。|
| `delete-draft <draft_id>` | 删除草稿。|
| `list-social-sets` | 列出可用的社交账号（账户）。|

### 示例

**创建一个简单的推文草稿：**
```bash
bash scripts/typefully.sh create-draft "Just shipped a new feature 🚀"
```

**创建一个多线程帖子：**
```bash
bash scripts/typefully.sh create-draft "First tweet of the thread\n---\nSecond tweet\n---\nThird tweet" --thread
```

**从标准输入创建多线程帖子（适用于较长的内容）：**
```bash
cat <<'EOF' | bash scripts/typefully.sh create-draft - --thread
First tweet of the thread\n---\nSecond tweet\n---\nThird tweet with the punchline
EOF
```

**创建跨平台的草稿（X + LinkedIn）：**
```bash
bash scripts/typefully.sh create-draft "Exciting update!" --platform x,linkedin
```

**为特定时间安排草稿的发布：**
```bash
bash scripts/typefully.sh create-draft "Morning thoughts ☀️" --schedule "2026-03-01T09:00:00Z"
```

**安排草稿在下一个空闲时间发布：**
```bash
bash scripts/typefully.sh schedule-draft 8196074 next-free-slot
```

**列出最近的草稿：**
```bash
bash scripts/typefully.sh list-drafts draft 5
```

## 注意事项

- `publish_at: "now"` 表示立即发布——请谨慎使用。
- `publish_at: "next-free-slot"` 会根据用户的 Typefully 队列安排发布时间。
- 多线程帖子在文本参数中通过 `\n---\n` 分隔。
- 脚本输出 JSON 格式的数据；可以使用 `jq` 进行格式化。
- 所有 API 错误都会显示有意义的错误信息（如 401、404、429 等）。