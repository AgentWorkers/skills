---
name: instagram-poster
description: 通过 Telegram 自动将图片发布到 Instagram。可以使用 WaveSpeed 生成图片，或者使用用户自己提供的图片。通过使用住宅代理（residential proxy）来规避 Instagram 的机器人检测机制。适用于以下场景：用户希望将图片发布到 Instagram、自动发布图片、在 Instagram 上分享照片、安排 Instagram 发布时间、发布 Reel 视频中的图片等。需要使用环境变量 `IG_USERNAME` 和 `IG_PASSWORD`，或者已保存的 Instagram 会话信息。使用住宅代理时，需要用户具备操作浏览器的相关技能。
metadata:
  openclaw:
    emoji: 📸
    os: [linux, darwin, win32]
    requires:
      skills: [human-browser]
      env: [IG_USERNAME, IG_PASSWORD]
---
# instagram-poster

直接从您的AI代理将图片发布到Instagram——使用真实的居民IP地址来规避机器人检测。

## 快速入门

```bash
node {baseDir}/scripts/post.js \
  --image ./photo.jpg \
  --caption "Good morning 🌅 #photography" \
  --user YOUR_USERNAME \
  --pass YOUR_PASSWORD
```

发布由WaveSpeed生成的图片：

```bash
# 1. Generate image
node /workspace/.agents/skills/wavespeed/scripts/wavespeed.js generate \
  --model flux-schnell --prompt "sunset over mountains" --output /tmp/post.png

# 2. Post to Instagram
node {baseDir}/scripts/post.js \
  --image /tmp/post.png \
  --caption "Golden hour 🏔️ #nature #photography"
```

## 选项

| 标志 | 环境变量 | 描述 |
|------|-----|-------------|
| `--image` | `IG_IMAGE` | 本地文件路径或HTTPS URL |
| `--caption` | `IG_CAPTION` | 发布说明（可选） |
| `--user` | `IG_USERNAME` | Instagram用户名 |
| `--pass` | `IG_PASSWORD` | Instagram密码 |
| `--session` | `IG_SESSION_PATH` | Cookie会话文件（默认：`~/.openclaw/ig-session.json`） |

## 会话缓存

首次运行时，会登录Instagram并将Cookie保存到`~/.openclaw/ig-session.json`文件中。
后续运行将重用该会话，无需重新登录。

## 在openclaw.json中配置

```json5
{
  skills: {
    entries: {
      "instagram-poster": {
        env: {
          IG_USERNAME: "your_username",
          IG_PASSWORD: "your_password"
        }
      }
    }
  }
}
```

## 工作原理

1. 通过`human-browser`启动一个使用**罗马尼亚居民IP地址**的隐秘浏览器。
2. 以真实iPhone用户的身份登录Instagram，通过所有机器人检测。
3. 上传您的图片并提交说明。
4. 保存会话Cookie，以便保持登录状态。

## 必备条件

- 安装了[human-browser](https://clawhub.ai/skills/human-browser)技能。
- 需要订阅`human-browser`服务（使用居民代理）→ [humanbrowser.dev](https://humanbrowser.dev)。
- 拥有Instagram账户凭证。

## 代理使用示例

```
User: Post this sunset photo to Instagram with caption "Golden hour 🌅"
Agent: node {baseDir}/scripts/post.js --image /tmp/sunset.jpg --caption "Golden hour 🌅"
```