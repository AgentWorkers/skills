---
name: spotify-connect
description: **远程控制 Spotify Connect 设备（音箱、电视、Echo、手机、桌面设备）的播放功能**  
当用户需要播放音乐、暂停、跳曲、调节音量、查看可用音频设备，或将播放权限转移到特定设备时，可以使用该功能。该功能支持多个具有命名配置文件的 Spotify 账户，但需订阅 Spotify Premium 版本才能使用全部功能。
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: ["uv"]
      env:
        SPOTIFY_CLIENT_ID: "required"
        SPOTIFY_CLIENT_SECRET: "required"
---

# Spotify Connect

您可以控制任何支持Spotify Connect功能的设备上的播放操作。该功能支持多个已登录的Spotify账户。

## 设置（只需完成一次）

1. 在 [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) 上创建一个Spotify应用程序：
   - 将重定向URI设置为 `http://127.0.0.1:8888/callback`
   - 启用“Web API”和“Web Playback SDK”功能
   - 记下客户端ID（Client ID）和客户端密钥（Client Secret）
2. 设置环境变量（或将其添加到OpenClaw的 `env_vars` 配置文件中）：
   ```bash
   export SPOTIFY_CLIENT_ID="your-client-id"
   export SPOTIFY_CLIENT_SECRET="your-client-secret"
   ```
3. 运行初次身份验证（会打开浏览器）：
   ```bash
   uv run {baseDir}/scripts/spotify.py auth --name "alice"
   ```
   此操作会创建一个带有自动更新令牌的账户配置文件。

4. （可选）添加更多账户：
   ```bash
   uv run {baseDir}/scripts/spotify.py auth --name "bob"
   ```

5. （可选）在 `~/.openclaw/spotify-connect/devices.json` 文件中配置设备别名：
   ```json
   {
     "kitchen": "Kitchen Echo",
     "kids": "Kids Room Echo",
     "office": "Office Speaker"
   }
   ```

## 依赖项

Python依赖项通过 [PEP 723](https://peps.python.org/pep-0723/) 进行管理，`uv run` 会自动处理安装过程，无需手动执行 `pip install`。

## 账户管理

当前激活的账户将用于所有播放命令。账户信息存储在 `~/.openclaw/spotify-connect/accounts.json` 文件中。

## 命令

所有命令的格式为：`uv run {baseDir}/scripts/spotify.py <command> [args]`

### 列出设备
```bash
# Current account only
uv run {baseDir}/scripts/spotify.py devices

# All accounts in parallel (recommended before playing on a specific device)
uv run {baseDir}/scripts/spotify.py devices --all-accounts
```

### 播放音乐
```bash
# Resume playback (current device or specify one)
uv run {baseDir}/scripts/spotify.py play
uv run {baseDir}/scripts/spotify.py play --device "kitchen"

# Play a song, artist, album, or playlist (searches Spotify)
uv run {baseDir}/scripts/spotify.py play --query "Bohemian Rhapsody"
uv run {baseDir}/scripts/spotify.py play --query "artist:Radiohead"
uv run {baseDir}/scripts/spotify.py play --query "album:OK Computer"
uv run {baseDir}/scripts/spotify.py play --query "playlist:Chill Vibes"
uv run {baseDir}/scripts/spotify.py play --uri "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"

# Play on a specific device
uv run {baseDir}/scripts/spotify.py play --query "Daft Punk" --device "office"
```

### 控制播放
```bash
uv run {baseDir}/scripts/spotify.py pause
uv run {baseDir}/scripts/spotify.py next
uv run {baseDir}/scripts/spotify.py prev
uv run {baseDir}/scripts/spotify.py volume 75
uv run {baseDir}/scripts/spotify.py volume 75 --device "kitchen"
uv run {baseDir}/scripts/spotify.py shuffle on
uv run {baseDir}/scripts/spotify.py shuffle off
uv run {baseDir}/scripts/spotify.py repeat track   # track, context, or off
```

### 转移播放任务
```bash
uv run {baseDir}/scripts/spotify.py transfer "kitchen"
```

### 查看当前正在播放的内容
```bash
uv run {baseDir}/scripts/spotify.py status
```

## 设备匹配

设备名称采用模糊匹配方式。可以使用 `devices.json` 文件中的别名或Spotify设备的部分名称进行匹配。如果存在歧义，脚本会列出所有匹配的设备。

**重要提示：跨账户设备识别**：当用户请求在某个特定设备或房间播放音乐时，首先运行 `devices --all-accounts` 命令，以获取所有账户下的所有设备列表。然后切换到拥有目标设备的账户再执行播放命令。请勿假设设备属于某个特定的账户。

## 常见错误

- **“没有活动的设备”**：请先在任意设备上打开Spotify应用程序，或使用 `--device` 参数指定目标设备。
- **“需要Spotify Premium账户”**：使用Spotify Premium账户才能使用Spotify Connect功能。
- **“设备未找到”**：运行 `devices` 命令查看可用设备；部分处于休眠状态的设备可能不会显示在列表中（请先在该设备上播放音乐以唤醒设备）。
- **“没有活动的账户”**：运行 `auth --name <name>` 进行身份验证，或使用 `switch <name>` 选择所需的账户。