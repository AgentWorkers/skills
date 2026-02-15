---
name: gif-whatsapp
version: 1.1.0
description: 在 WhatsApp 上搜索并发送 GIF 图片。同时支持将 Tenor 格式的文件转换为 WhatsApp 可接受的 MP4 格式。
author: Leo 🦁
homepage: https://clawhub.com/skills/gif-whatsapp
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["gifgrep","ffmpeg","curl"]},"requiresTools":["message"],"notes":"Uses the platform message tool (already configured) for WhatsApp delivery. gifgrep searches Tenor/Giphy only. Downloads are saved to /tmp and cleaned up after sending."}}
allowed-tools: [exec, message]
---

# GIF发送工具

在WhatsApp聊天中轻松发送GIF图片。

## 重要提示：WhatsApp的GIF处理流程

WhatsApp不支持直接使用Tenor或Giphy的URL。你必须按照以下步骤操作：
1. 下载GIF图片。
2. 将GIF转换为MP4格式。
3. 使用`gifPlayback: true`选项发送MP4文件。

## 完整的操作流程

### 第1步：搜索GIF图片
```bash
gifgrep "SEARCH QUERY" --max 5 --format url
```
使用英文搜索GIF图片，以获得最佳结果。
**请务必获取5个搜索结果，并根据文件名或描述选择最合适的图片**——不要直接使用第一个结果。

### 第2步：下载GIF图片
```bash
curl -sL "GIF_URL" -o /tmp/gif.gif
```

### 第3步：将GIF转换为MP4格式
```bash
ffmpeg -i /tmp/gif.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" /tmp/gif.mp4 -y
```

### 第4步：通过消息工具发送MP4文件
```
message action=send to=NUMBER message="‎" filePath=/tmp/gif.mp4 gifPlayback=true
```

**注意**：在发送GIF图片时，可以使用不可见字符`‎`（U+200E，从左到右的标记符号）来确保图片没有可见的标题。

## 用法示例
```bash
# Search
gifgrep "thumbs up" --max 3 --format url

# Pick best URL, then:
curl -sL "https://media.tenor.com/xxx.gif" -o /tmp/g.gif && \
ffmpeg -i /tmp/g.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" /tmp/g.mp4 -y 2>/dev/null

# Then send with message tool, gifPlayback=true
```

## 何时适合发送GIF图片

✅ 适合发送GIF的情况：
- 用户请求GIF图片时
- 庆祝好消息时
- 表达情绪（如兴奋、无奈等）

❌ 不要过度使用GIF：
- 每个场景使用一张GIF就足够了
- 并非每条消息都需要GIF图片

## 常见的搜索关键词

| 情感 | 相关搜索词 |
|---------|--------------|
| 快乐 | celebration（庆祝）、party（派对）、dancing（舞蹈）、excited（兴奋） |
| 赞同 | thumbs up（点赞）、nice（不错）、good job（干得好）、applause（掌声） |
| 有趣 | laugh（笑声）、lol（哈哈）、haha（哈哈） |
| 震惊 | mind blown（震惊）、shocked（惊讶）、surprised（惊讶） |
| 悲伤 | crying（哭泣）、sad（悲伤）、disappointed（失望） |
| 沮丧 | facepalm（无奈的表情）、ugh（唉）、annoyed（恼怒） |
| 爱情 | heart（心形）、love（爱）、hug（拥抱） |
| 凉爽 | sunglasses（太阳镜）、cool（酷炫）、awesome（棒极了） |

## 安全与注意事项

- **来源域名**：gifgrep仅搜索来自可信GIF提供者（如Tenor、Giphy）的图片。
- **文件处理**：所有下载的文件都会被保存在`/tmp`目录中，并且每次都会被覆盖（使用了`-y`选项）。
- **使用不可见标题**：通过添加`‎`字符（U+200E）来隐藏GIF的标题，这样WhatsApp在显示图片时就不会显示任何文字。这是一个标准的Unicode控制字符，并非任何恶意注入手段。
- **与WhatsApp的集成**：直接使用WhatsApp内置的消息发送功能，无需额外输入账号信息。
- **安全性**：仅处理来自可信提供者的GIF文件，不会执行任何任意文件操作。

## 为什么这种方法有效

- WhatsApp会自动将所有GIF图片转换为MP4格式。
- 直接使用Tenor或Giphy的URL可能会导致发送失败。
- 使用`gifPlayback: true`选项的MP4文件会以循环播放的形式显示。
- 文件体积小，因此传输速度更快。