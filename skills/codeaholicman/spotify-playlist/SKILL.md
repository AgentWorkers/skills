---
name: spotify-playlist
description: 根据自然语言请求构建和管理Spotify播放列表。支持搜索歌曲、艺术家和专辑，创建播放列表，管理歌曲内容，以及查看用户的收听历史记录。适用于用户需要创建播放列表、查找音乐、查看自己最近听过的歌曲，或进行任何与Spotify相关的操作的场景。例如：“为我创建一个适合雨天周日的播放列表”、“我最近在听什么音乐？”、“找到类似‘Bonobo’风格的歌曲”。
---
# Spotify 播放列表生成器

使用 Spotify Web API 从自然语言请求中生成播放列表。  
已更新以适应 2026 年 2 月的 API 变更（开发模式）。

## 先决条件

- Spotify Premium 账户（自 2026 年 2 月起，开发模式应用需要此账户）  
- 安装 Python 3 并导入 `requests` 库  

## 设置步骤

1. 在 [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) 创建一个应用。  
2. 将回调 URI 设置为 `http://127.0.0.1:8765/callback`（必须是 `127.0.0.1`，而非 `localhost`，因为 Spotify 不允许使用 `localhost`）。  
3. 运行身份验证流程：  
   ```bash
python3 scripts/auth.py --client-id <ID> --client-secret <SECRET>
```  

4. 在浏览器中打开生成的 URL 并完成授权。  
5. 如果回调页面自动加载，说明设置成功；否则，复制完整的回调 URL 并运行以下命令：  
   ```bash
python3 scripts/auth.py --client-id <ID> --client-secret <SECRET> --code-url "<FULL_REDIRECT_URL>"
```  

生成的访问令牌会保存在 `~/.openclaw/workspace/config/.spotify-tokens.json` 文件中，当遇到 401 错误时令牌会自动刷新。  

## API 脚本参考  

所有相关命令位于 `scripts/spotify.py` 文件中。所有输出结果均为 JSON 格式。  
```bash
# Search (tracks, artists, or albums)
python3 scripts/spotify.py search "bohemian rhapsody" --limit 5
python3 scripts/spotify.py search "Bonobo" --type artist --limit 3
python3 scripts/spotify.py search "Moon Safari" --type album --limit 3

# Create playlist
python3 scripts/spotify.py create "Rainy Sunday" --description "Chill vibes" --private

# Add/remove tracks (by Spotify URI)
python3 scripts/spotify.py add <playlist_id> spotify:track:xxx spotify:track:yyy
python3 scripts/spotify.py remove <playlist_id> spotify:track:xxx

# List playlists
python3 scripts/spotify.py my-playlists --limit 10

# View playlist contents
python3 scripts/spotify.py playlist-tracks <playlist_id> --limit 50

# Listening history
python3 scripts/spotify.py top-tracks --time-range short --limit 20
python3 scripts/spotify.py recently-played --limit 20

# Profile
python3 scripts/spotify.py me
```  

## 播放列表生成流程

当用户请求创建播放列表时，系统会执行以下步骤：  
1. **解析请求**：提取用户的偏好（情绪、音乐类型、时代背景、活动类型或特定的艺术家/歌曲）。  
2. **搜索歌曲**：通过多种搜索方式找到符合用户偏好的歌曲。  
3. **利用播放历史记录**：参考用户的 `top-tracks` 和 `recently-played` 列表来个性化推荐。  
4. **创建播放列表**：为播放列表设置创意名称和描述，添加 15–30 首歌曲。  
5. **分享链接**：返回播放列表的 Spotify URL。  

### 使用建议：  
- 从不同角度进行多次搜索（例如：艺术家名称、音乐类型、时代背景与情绪的组合）。  
- 在播放列表中同时包含热门歌曲和较少人听过的作品，以获得更好的听觉体验。  
- 使用 `top-tracks --time-range short` 查看用户近期的音乐喜好；`top-tracks --time-range long` 可查看用户的历史收藏。  
- 通常建议添加 15–30 首歌曲，除非用户另有要求。  
- 根据用户的整体音乐风格而非具体请求内容，为播放列表起富有创意的名称。  

## 2026 年 2 月 API 限制（开发模式）  

- **推荐功能已被移除**：现在需要通过搜索和人工筛选来创建播放列表。  
- 部分响应数据中不再包含歌曲的流行度信息（可能导致返回结果为空）。  
- 播放列表相关的 API 端点从 `/tracks` 更改为 `/items`（已在脚本中处理）。  
- 应用所有者需要使用 Spotify Premium 账户。  
- 每个应用最多支持 5 位用户，每位开发者只能使用一个应用。  
- 不支持批量查询专辑、艺术家或歌曲的功能（需单独进行查询）。  

## 定时任务建议  

结合 OpenClaw 的定时任务功能来实现自动化播放列表生成：  
- **每周更新**：每周一根据不同主题生成新的播放列表。  
- **按时间段定制播放列表**：为早晨、下午或晚上分别生成适合的播放列表。  
- **根据通勤时间生成播放列表**：根据通勤时长自动推荐合适的音乐。  
- **根据天气调整播放列表**：根据天气情况调整播放列表的风格。