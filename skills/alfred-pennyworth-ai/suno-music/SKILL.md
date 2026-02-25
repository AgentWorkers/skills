---
name: suno-music
description: "通过 Suno 生成 AI 音乐和歌曲。适用场景包括：  
(1) 用户希望创作或生成一首歌曲/音乐；  
(2) 用户需要歌词创作服务；  
(3) 用户需要为特定场合（如生日、庆祝活动、搞笑场景、摇篮曲等）准备歌曲。  
该工具需要 gcui-art/suno-api 自托管服务器的支持，并支持自定义歌词、风格/流派标签以及器乐曲目。当前版本为 Suno v5。"
---
# Suno 音乐生成

通过本地的 [gcui-art/suno-api](https://github.com/gcui-art/suno-api) 服务器来生成歌曲。

## 设置

1. 克隆并安装依赖：`git clone https://github.com/gcui-art/suno-api && cd suno-api && npm install && npm run build`
2. 创建 `.env` 文件，填写你的 Suno cookie 以及可选的 2Captcha 密钥（详情请参阅仓库的 README 文件）。
3. 启动服务器：`PORT=3100 npm start`（或创建一个 LaunchAgent/systemd 服务）。
4. 验证服务器是否正常运行：`curl http://localhost:3100/api/get_limit`

如果未在 `http://localhost:3100` 上运行，请设置 `SUNO_API_URL` 环境变量。

## 快速生成（简单模式）

对于简单的请求（例如“生成一首关于 X 的歌曲”），Suno 会自动编写歌词：

```bash
scripts/suno.sh generate --prompt "DESCRIPTION" --wait
```

## 自定义生成（完全控制）

你可以指定具体的歌词和音乐风格：

```bash
scripts/suno.sh custom --prompt "LYRICS" --style "GENRE TAGS" --title "TITLE" --wait
```

- 使用 `--instrumental` 选项可生成无伴奏版本。
- 使用 `--negative-tags "TAGS"` 可排除某些音乐风格。

## 先生成歌词

当用户提供主题但未提供歌词时，系统会先生成歌词，用户可以查看后进行修改，再选择具体的音乐风格：

```bash
scripts/suno.sh lyrics --prompt "THEME"
```

## 查看状态/创作者信息

```bash
scripts/suno.sh status --ids "ID1,ID2"
scripts/suno.sh credits
```

## 下载音频文件

```bash
scripts/suno.sh download --url "AUDIO_URL" --out "/path/to/file.mp3"
```

## 工作流程

1. **模糊想法** → 使用 `generate` 命令让 Suno 根据描述生成歌词。
2. **具体需求** → 先编写歌词，再使用 `custom` 命令指定风格和标题。
3. **先查看生成的歌词** → 用户可以查看、修改后再次使用 `custom` 命令生成歌曲。
4. 请务必使用 `--wait` 选项，系统会等待音频文件准备完成（大约需要 60-120 秒）。
5. 每次生成会生成 **2 个版本的歌曲**。
6. 下载音频文件并通过消息工具发送给用户（作为附件）。
7. 生成的歌曲会出现在用户的 Suno 图书馆或播放列表中。

## 音乐风格标签示例

- `pop, upbeat, happy, female vocals`（流行、欢快、女声）
- `country, acoustic guitar, male vocals, storytelling`（乡村、原声吉他、男声、叙事风格）
- `hip hop, trap beats, autotuned vocals`（嘻哈、陷阱节奏、自动调音的人声）
- `classical, orchestral, cinematic`（古典、管弦乐、电影风格）
- `rock, electric guitar, energetic, anthem`（摇滚、电吉他、充满活力的颂歌）
- `thrash metal, aggressive riffs, double bass drums, distorted guitar`（激流金属、强烈的节奏、失真吉他）
- `jazz, smooth, saxophone, lounge`（爵士、柔和、萨克斯风、轻松氛围）
- `lullaby, soft, gentle, music box`（摇篮曲、轻柔、音乐盒音效）
- `folk, banjo, americana, warm`（民谣、班卓琴、美式乡村风格）
- `edm, electronic, dance, synth`（电子音乐、舞曲、合成器）
- `r&b, soulful, smooth, groovy`（节奏布鲁斯、富有灵魂感、流畅的节奏）

## 更新 Cookie

如果遇到认证错误，请更新 Suno cookie：

1. 在浏览器中打开 `suno.com/create`，然后打开开发者工具（F12），选择“网络”标签页。
2. 刷新页面，找到包含 `?__clerk_api_version` 的请求。
3. 复制 Cookie 头部的值，更新 `.env` 文件，然后重新启动服务器。

## 注意事项

- 默认模型为 Suno v5（`chirp-crow`）；可以通过 `--model` 参数进行更改。
- 每次生成歌曲都会生成相应的创作者信息（每首歌曲对约 10 条创作者信息）。
- 音频文件为 MP3 格式，时长通常为 2-4 分钟。
- 2Captcha 密钥是可选的，但建议使用以确保系统的长期稳定性。