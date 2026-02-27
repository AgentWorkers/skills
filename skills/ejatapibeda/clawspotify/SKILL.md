---
name: clawspotify
description: "控制 Spotify 播放功能：播放、暂停、继续播放、跳过当前曲目、返回上一首曲目、重新开始播放、搜索歌曲、将歌曲加入播放列表、调整音量、随机播放、重复播放，以及查看当前正在播放的歌曲信息。"
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: ["bash", "python3"]
---
# clawspotify

您可以直接通过 OpenClaw 代理来控制 Spotify 的播放功能。该功能支持 **免费和高级** Spotify 账户。

## 触发条件

当用户执行以下操作时，可以使用该技能：
- 播放、暂停、继续播放、跳过当前曲目或播放列表
- 搜索歌曲、艺术家或播放列表（不进行播放）
- 将曲目添加到播放队列
- 查看当前正在播放的内容
- 调整音量或设置随机播放/重复播放模式
- 设置用户的 Spotify 会话（首次使用时）

## 认证

clawspotify 使用用户的 Spotify 浏览器 cookies（`sp_dc` 和 `sp_key`），**无需官方 API 密钥**。该功能同样适用于 **免费和高级** 账户。

### 一次性设置（如何获取 cookies）

1. 在浏览器中打开 **https://open.spotify.com** 并登录。
2. 按下 **F12** 打开开发者工具。
3. 转到 **应用程序** 标签 → **Cookies** → `https://open.spotify.com`。
4. 找到并复制 `sp_dc` 的值。
5. 找到并复制 `sp_key` 的值。
6. 运行以下命令：
```bash
clawspotify setup --sp-dc "AQC..." --sp-key "07c9..."
```

会话信息会被保存在 `~/.config/spotapi/session.json` 文件中，并会自动重用。

> 如果用户提供了他们的 `sp_dc` 和 `sp_key` 值，请为他们运行设置命令。

### 多账户管理

```bash
clawspotify setup --sp-dc "..." --sp-key "..." --id "work"
clawspotify status --id "work"
```

## 命令列表

### 查看当前播放状态

```bash
clawspotify status
```

### 搜索音乐（不进行播放）

```bash
clawspotify search "Bohemian Rhapsody"        # 搜索曲目，显示前 5 个结果
clawspotify search-playlist "Workout"         # 搜索播放列表，显示前 5 个结果
```

### 搜索并播放音乐

```bash
clawspotify play "Bohemian Rhapsody"          # 播放第一个搜索结果
clawspotify play "Bohemian Rhapsody" --index 2    # 播放第二个搜索结果（索引从 0 开始）
clawspotify play-playlist "Lofi Girl"         # 播放第一个播放列表的结果
```

### 播放控制

```bash
clawspotify pause                # 暂停播放
clawspotify resume               # 继续播放
clawspotify skip                 # 跳到下一首曲目
clawspotify prev                 # 跳到上一首曲目
clawspotify restart               # 从头开始播放
```

### 添加曲目到播放队列

```bash
clawspotify queue "Stairway to Heaven"
clawspotify queue "spotify:track:3z8h0TU..."    # 通过 URI 添加曲目
```

### 调整音量

```bash
clawspotify volume 50                # 将音量调至 50%
clawspotify volume 0                # 静音
clawspotify volume 100               # 将音量调至最大
```

### 设置随机播放/重复播放模式

```bash
clawspotify shuffle on              # 启用随机播放
clawspotify shuffle off             # 关闭随机播放
clawspotify repeat on              # 启用重复播放
clawspotify repeat off             # 关闭重复播放
```

## 注意事项：
- 该功能支持 **免费和高级** Spotify 账户。
- 为了使播放命令生效，Spotify 必须在 **至少一台设备**（PC、手机或网页端）上处于打开状态。
- Cookies 会定期过期——如果命令执行失败并显示 401 错误，请使用新的 Cookies 重新运行设置命令。
- 默认的会话标识符为 `"default"`。可以使用 `--id` 参数来管理多个账户。
- **脚本位置：`{skill_folder}/clawspotify.sh`
- **平台提示：** 如果用户使用 Windows 系统，需要安装 WSL、Git Bash 或 Cygwin 才能运行此技能。