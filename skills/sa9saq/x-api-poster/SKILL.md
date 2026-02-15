---
description: 通过 OAuth 1.0a API v2 将推文发布到 X/Twitter，支持文本、图片、回复和话题（threads）的发布。
---

# 使用X API在Twitter上发布内容

通过官方的v2 API和OAuth 1.0a认证方式在X（Twitter）上发布内容。

## 所需条件

- Python 3.8及以上版本
- `requests`库（使用`pip install requests`安装）
- X API的认证信息（消费者密钥/密钥以及对访问令牌/密钥）

## 快速入门

```bash
# Post a tweet
python3 {skill_dir}/post.py "Hello from OpenClaw!"

# Post with image
python3 {skill_dir}/post.py "Check this out" /path/to/image.png

# Reply to a tweet
python3 {skill_dir}/post.py "Reply text" 1234567890123456789

# Reply with image
python3 {skill_dir}/post.py "Reply with pic" 1234567890123456789 /path/to/image.png
```

## 配置

### 必需的环境变量

| 变量          | 描述                                      |
|---------------|-----------------------------------------|
| `X_CONSUMER_KEY`    | API消费者密钥                                      |
| `X_CONSUMER_SECRET` | API消费者密钥的对称密钥                               |
| `X_ACCESS_TOKEN`    | OAuth 1.0a访问令牌                                      |
| `X_ACCESS_TOKEN_SECRET` | OAuth 1.0a访问令牌的对称密钥                               |

将这些变量保存在`~/.openclaw/secrets.env`文件中，并设置文件权限为`chmod 600`。

### 获取API密钥

1. 访问[developer.x.com](https://developer.x.com/)
2. 创建一个项目和应用
3. 启用具有“读取和写入”权限的OAuth 1.0a认证
4. 生成消费者密钥和访问令牌
5. 将它们添加到`~/.openclaw/secrets.env`文件中

## API详细信息

- **发布内容**：`POST https://api.twitter.com/2/tweets`（v2）
- **上传媒体文件**：`POST https://upload.twitter.com/1.1/media/upload.json`（v1.1）
- **认证方式**：使用HMAC-SHA1签名进行OAuth 1.0a认证（内置功能，无需外部OAuth库）

## 特殊情况与故障排除

- **字符长度限制**：发布前请验证文本长度。URL通常占用约23个字符（包括t.co链接）。
- **重复推文**：X会拒绝连续发送相同的推文。请修改推文内容或稍后重试。
- **图片格式**：支持PNG、JPEG、GIF、WEBP格式。图片文件大小上限为5MB，GIF文件为15MB。
- **401 Unauthorized**：访问令牌过期或权限不足。请在developer.x.com重新生成令牌。
- **403 Forbidden**：应用程序可能需要更高的访问权限。请检查项目等级。
- **429 Rate Limited**：免费账户每24小时只能发布约50条推文。收到`x-rate-limit-reset`头部信息后，请稍后重试。
- **缺少环境变量**：脚本在尝试发布前应检查所有4个环境变量是否都已设置。如果缺少任何变量，应立即报错并终止操作。

## 安全性注意事项

- **切勿记录或显示API认证信息**——在任何错误输出中都应对其进行屏蔽。
- 将认证信息保存在`secrets.env`文件中，并设置文件权限为`chmod 600`，切勿将其存储在代码或Git仓库中。
- 发布前请验证推文内容，以防意外泄露认证信息。
- 在发送推文前请进行审核——自动发布的推文应经过人工审核。