---
name: spotify-history
description: 通过 Spotify Web API，您可以访问用户的收听历史记录、热门艺术家/歌曲信息，并获得个性化的推荐。该功能适用于获取用户的近期播放记录、分析音乐品味或生成推荐内容。使用前需要完成一次 OAuth 设置。
---

# Spotify 历史记录与推荐功能

您可以访问自己的 Spotify 听歌记录，并获得个性化的音乐推荐。

## 设置（只需一次）

### 快速设置（推荐）

运行设置向导：
```bash
bash skills/spotify-history/scripts/setup.sh
```

该向导将指导您完成以下步骤：
1. 创建一个 Spotify 开发者应用。
2. 安全地保存登录凭据。
3. 授权访问权限。

### 手动设置

1. **创建 Spotify 开发者应用**
   - 访问 [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
   - 点击 **创建应用**
   - 填写以下信息：
     - **应用名称：** `Clawd`（或任意名称）
     - **应用描述：** **个人助理集成**
     - **回调 URI：** `http://127.0.0.1:8888/callback` ⚠️ 请使用正确的 URL！
   - 保存并复制 **客户端 ID** 和 **客户端密钥**。

2. **保存凭据**

   **选项 A：凭据文件（推荐）**
   ```bash
   mkdir -p credentials
   cat > credentials/spotify.json <<EOF
   {
     "client_id": "your_client_id",
     "client_secret": "your_client_secret"
   }
   EOF
   chmod 600 credentials/spotify.json
   ```

   **选项 B：环境变量**
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   ```

3. **身份验证**

   **使用浏览器（本地机器）：**
   ```bash
   python3 scripts/spotify-auth.py
   ```

   **无浏览器环境（headless）：**
   ```bash
   python3 scripts/spotify-auth.py --headless
   ```
   按照提示通过 URL 进行身份验证，并粘贴回调地址。

生成的令牌会保存在 `~/.config/spotify-clawd/token.json` 文件中，过期后会自动刷新。

## 使用方法

### 命令行

```bash
# Recent listening history
python3 scripts/spotify-api.py recent

# Top artists (time_range: short_term, medium_term, long_term)
python3 scripts/spotify-api.py top-artists medium_term

# Top tracks
python3 scripts/spotify-api.py top-tracks medium_term

# Get recommendations based on your top artists
python3 scripts/spotify-api.py recommend

# Raw API call (any endpoint)
python3 scripts/spotify-api.py json /me
python3 scripts/spotify-api.py json /me/player/recently-played
```

### 时间范围

- `short_term` — 大约过去 4 周内的内容
- `medium_term` — 大约过去 6 个月内的内容（默认值）
- `long_term` — 所有历史记录

### 示例输出

```
Top Artists (medium_term):
  1. Hans Zimmer [soundtrack, score]
  2. John Williams [soundtrack, score]
  3. Michael Giacchino [soundtrack, score]
  4. Max Richter [ambient, modern classical]
  5. Ludovico Einaudi [italian contemporary classical]
```

## 代理使用方法

当用户询问音乐相关问题时：
- “我最近听了什么？” → 使用 `spotify-api.py recent`
- “我的热门艺术家是谁？” → 使用 `spotify-api.py top-artists`
- “推荐新音乐” → 使用 `spotify-api.py recommend` 并结合您的音乐知识进行推荐

为了提供更准确的推荐，系统会结合 API 数据和您的音乐偏好来推荐用户库中尚未拥有的相似艺术家。

## 故障排除

### “找不到 Spotify 凭据！”
- 确保 `credentials/spotify.json` 文件存在，或者环境变量已正确设置。
- 系统会先检查凭据文件，再检查环境变量。
- 运行 `bash skills/spotify-history/scripts/setup.sh` 命令来生成新的凭据。

### “未授权。请先运行 spotify-auth.py。”
- 令牌可能已过期或无效。
- 运行 `python3 scripts/spotify-auth.py` 命令进行身份验证（如果使用无浏览器环境，请加上 `--headless` 参数）。

### “HTTP 错误 400：请求错误”（令牌刷新时出现）
- 凭据已更改或无效。
- 重新运行设置脚本：`bash skills/spotify-history/scripts/setup.sh`
- 或者更新 `credentials/spotify.json` 文件中的客户端 ID 和客户端密钥。

### “HTTP 错误 401：未经授权”
- 令牌已过期，自动刷新失败。
- 删除旧令牌并重新进行身份验证：
  ```bash
  rm ~/.config/spotify-clawd/token.json
  python3 scripts/spotify-auth.py
  ```

### 无浏览器环境
- 使用 `--headless` 参数：`python3 scripts/spotify-auth.py --headless`
- 手动在任何设备上打开身份验证页面。
- 复制回调地址（格式为 `http://127.0.0.1:8888/callback?code=...`），并在提示时将其粘贴回去。

## 安全注意事项

- 令牌的权限设置为 0600（仅用户可读写）。
- 客户端密钥应严格保密。
- 为安全起见，回调 URI 使用 `127.0.0.1`（仅限本地访问）。

## 所需的权限范围

- `user-read-recently-played` — 查看最近听过的歌曲
- `user-top-read` — 查看热门艺术家和歌曲
- `user-read-playback-state` — 查看当前的播放状态
- `user-read-currently-playing` — 查看当前正在播放的歌曲