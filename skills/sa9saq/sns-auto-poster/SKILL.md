---
description: 使用基于 Cron 的队列管理系统，来安排和自动化在 X（Facebook）/Twitter 上发布的内容。
---

# SNS自动发布工具

通过Cron调度和队列管理实现自动化的社交媒体发布功能。

## 系统要求

- Python 3.8及以上版本
- `requests` 库（使用 `pip install requests` 安装）
- 平台API凭证（详见配置文件）
- OpenClaw Cron任务调度工具

## 快速入门

```bash
# Add a post to the queue
python3 {skill_dir}/poster.py add --platform x --text "Hello world!" --schedule "2025-01-15 09:00"

# Add with image
python3 {skill_dir}/poster.py add --platform x --text "Check this out" --image /path/to/img.png

# Process pending posts now
python3 {skill_dir}/poster.py run

# List queued posts
python3 {skill_dir}/poster.py list

# Clear completed posts
python3 {skill_dir}/poster.py clean
```

## Cron任务设置

```bash
# Process queue every 15 minutes
openclaw cron add --schedule "*/15 * * * *" --command "python3 {skill_dir}/poster.py run"

# Daily morning post from template
openclaw cron add --schedule "0 9 * * *" --command "python3 {skill_dir}/poster.py run-template morning"
```

## 配置文件

### 必需的环境变量

| 变量        | 平台        | 说明                          |
|-------------|------------|-----------------------------------------|
| `X_CONSUMER_KEY` | X/Twitter    | API消费者密钥                          |
| `X_CONSUMER_SECRET` | X/Twitter    | API消费者密钥秘钥                          |
| `X_ACCESS_TOKEN` | X/Twitter    | OAuth访问令牌                          |
| `X_ACCESS_TOKEN_SECRET` | X/Twitter    | OAuth访问令牌秘钥秘钥                          |

将这些变量保存在 `~/.openclaw/secrets.env` 文件中，切勿将其提交到Git仓库。

### 发布队列（`queue.json`）

```json
[{"id": "uuid", "platform": "x", "text": "Hello!", "image": null, "schedule": "2025-01-15T09:00:00", "status": "pending"}]
```

### 模板文件（`templates/morning.json`）

```json
{"platform": "x", "text": "☀️ Good morning! Today is {date}. {custom_message}", "schedule_time": "09:00"}
```

## 支持的平台

| 平台        | 支持状态      | 认证方式                        |
|-------------|-------------|-----------------------------------------|
| X (Twitter)    | ✅ 已支持       | OAuth 1.0a                          |
| Bluesky      | 🔜 计划中      | 应用密码认证                          |
| Mastodon     | 🔜 计划中      | OAuth 2.0                          |

## 特殊情况与故障排除

- **重复发布**：X平台不允许在短时间内发布相同的推文。请添加时间戳或修改文本内容。
- **频率限制**：X平台每3小时允许发布约300条推文。队列处理程序会遵守这一限制。
- **图片过大**：X平台允许的图片最大大小为5MB。发布前请对图片进行压缩。
- **令牌过期**：如果发布失败并返回401错误，需在 developer.x.com 重新生成令牌。
- **队列损坏**：如果 `queue.json` 文件格式错误，请备份文件并重新创建。
- **错过调度时间**：过去安排的发布任务会在下一次任务执行时自动发布，不会过期。

## 安全性注意事项

- **切勿在输出中显示API凭证**。
- 将凭证保存在 `secrets.env` 文件中，并设置权限为 `chmod 600` 以保护文件安全。
- 发布前请验证内容长度（X平台限制推文长度为280个字符）。
- 在启用自动调度功能之前，请先检查队列中的所有待发布内容。