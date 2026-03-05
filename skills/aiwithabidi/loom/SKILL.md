---
name: loom
description: "**Loom** — 通过开发者API管理视频录制文件、字幕文件以及文件夹"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🎥", "requires": {"env": ["LOOM_ACCESS_TOKEN"]}, "primaryEnv": "LOOM_ACCESS_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🎥 Loom

Loom — 通过开发者 API 管理视频录像、字幕和文件夹

## 所需条件

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `LOOM_ACCESS_TOKEN` | ✅ | 开发者 API 访问令牌 |

## 快速入门

```bash
# List videos
python3 {{baseDir}}/scripts/loom.py videos --per_page <value>

# Get video
python3 {{baseDir}}/scripts/loom.py video-get id <value>

# Update video
python3 {{baseDir}}/scripts/loom.py video-update id <value> --title <value> --description <value>

# Delete video
python3 {{baseDir}}/scripts/loom.py video-delete id <value>

# Get transcript
python3 {{baseDir}}/scripts/loom.py video-transcript id <value>

# List comments
python3 {{baseDir}}/scripts/loom.py video-comments id <value>

# List folders
python3 {{baseDir}}/scripts/loom.py folders

# Get folder
python3 {{baseDir}}/scripts/loom.py folder-get id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `videos` | 列出所有视频 |
| `video-get` | 获取视频信息 |
| `video-update` | 更新视频信息 |
| `video-delete` | 删除视频 |
| `video-transcript` | 获取视频字幕 |
| `video-comments` | 列出视频评论 |
| `folders` | 列出所有文件夹 |
| `folder-get` | 获取文件夹信息 |
| `folder-videos` | 列出文件夹中的视频 |
| `user` | 获取当前用户信息 |
| `members` | 列出工作空间成员 |

## 输出格式

所有命令默认以 JSON 格式输出。添加 `--human` 选项可获取易读的格式化输出。

```bash
python3 {{baseDir}}/scripts/loom.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/loom.py` | 主 CLI 工具 — 集中了所有命令 |

## 致谢
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供支持 |
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)