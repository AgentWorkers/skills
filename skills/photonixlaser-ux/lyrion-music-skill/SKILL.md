---
name: lyrion-music
description: 通过 JSON-RPC API 来控制 Lyrion 音乐服务器（LMS）。使用此技能可以执行播放/暂停/停止操作、调节音量、管理播放列表、选择播放器以及查询音乐数据库等功能。需要确保 LMS 在端口 9000 上运行。
---

# Lyrion 音乐服务器技能

通过 JSON-RPC API 控制 Lyrion 音乐服务器（前身为 Logitech Media Server）。

## 配置

默认主机：`192.168.20.40:9000`（可通过环境变量 `LYRION_HOST` 进行配置）

## 使用方法

使用 `scripts/lyrion.sh` 脚本执行所有操作：

```bash
./skills/lyrion-music/scripts/lyrion.sh <befehl> [parameter]
```

### 命令

**播放器管理：**
- `players` - 显示所有播放器的列表
- `status [player_id]` - 查看指定播放器的当前状态

**播放控制：**
- `play [player_id]` - 开始播放
- `pause [player_id]` - 暂停播放
- `stop [player_id]` - 停止播放
- `power [player_id] [on|off]` - 开/关指定播放器

**音量控制：**
- `volume [player_id] [0-100|+|-]` - 设置/调整音量
- `mute [player_id]` - 将指定播放器静音

**播放列表管理：**
- `playlist [player_id]` - 显示指定播放器的当前播放列表
- `clear [player_id]` - 清空播放列表
- `add [player_id] <url/pfad>` - 将指定文件添加到播放列表
- `playtrack [player_id] <index>` - 播放播放列表中的指定曲目

**数据库操作：**
- `artists` - 显示所有艺术家列表
- `albums [artist_id]` - 显示艺术家的所有专辑列表
- `songs [album_id]` - 显示专辑中的所有歌曲列表
- `search <search_term>` - 全局搜索

## API 参考

请参阅 [references/api.md](references/api.md) 以获取完整的 API 文档。

## 示例

```bash
# Alle Player anzeigen
./skills/lyrion-music/scripts/lyrion.sh players

# Wiedergabe im Wohnzimmer starten (Player ID erforderlich)
./skills/lyrion-music/scripts/lyrion.sh play aa:bb:cc:dd:ee:ff

# Lautstärke auf 50% setzen
./skills/lyrion-music/scripts/lyrion.sh volume aa:bb:cc:dd:ee:ff 50

# Playlist leeren und Album abspielen
./skills/lyrion-music/scripts/lyrion.sh clear aa:bb:cc:dd:ee:ff
./skills/lyrion-music/scripts/lyrion.sh add aa:bb:cc:dd:ee:ff "db:album.id=123"
./skills/lyrion-music/scripts/lyrion.sh play aa:bb:cc:dd:ee:ff
```