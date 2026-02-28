---
name: playlistable-mcp
description: 使用 Playlistable MCP 创建由 AI 支持的 Spotify 播放列表，并通过该平台发现新音乐。当用户希望根据某种情绪或提示生成播放列表、搜索歌曲或艺术家、获取个性化播放列表建议，或管理自己的播放列表时，可以使用该工具。该服务需要通过 https://mcp.playlistable.io/authorize 进行 OAuth 认证。支持使用环境变量 `PLAYLISTABLE_API_KEY` 或配置文件 `config/auth.json` 来配置认证信息。
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["node"],"env":["PLAYLISTABLE_API_KEY"]},"primaryEnv":"PLAYLISTABLE_API_KEY"}}
---
# Playlistable MCP

使用 Playlistable MCP 服务器创建由 AI 驱动的 Spotify 播放列表，并发现新音乐。

## 认证

需要一个 Playlistable API 密钥（通过环境变量 `PLAYLISTABLE_API_KEY` 或 `config/auth.json` 设置）。

获取 API 密钥的步骤如下：

```bash
node {baseDir}/scripts/auth.mjs
```

整个过程完全自动化：系统会启动一个本地 HTTP 服务器，打开浏览器进行 Spotify OAuth 认证，捕获重定向信息，通过 PKCE 机制将授权码兑换为 API 密钥，并将其保存到 `{baseDir}/config/auth.json` 文件中。无需手动复制粘贴密钥。

如果密钥已经保存在 `config/auth.json` 中，脚本会自动从该文件中读取密钥。

## 工作原理

位于 `https://mcp.playlistable.io` 的 MCP 服务器通过 Streamable HTTP 协议提供各种工具。`mcp-call.mjs` 脚本可以直接发送 JSON-RPC 请求，无需使用任何 MCP SDK。

### 常见操作流程

- **生成播放列表**：用户描述一种心情，`generate_playlist` 函数会创建一个异步 Spotify 播放列表，并立即返回播放列表的 URL。歌曲会自动添加到播放列表中。
- **浏览播放列表**：`get_playlists` 函数可以列出用户所有的播放列表；`get_playlist` 函数可以获取特定播放列表的详细信息和其中的歌曲。
- **编辑播放列表**：`edit_playlist` 函数可以通过 Spotify 歌曲 ID 来添加或删除歌曲。
- **搜索音乐**：`search_songs` 和 `search_artists` 函数可以直接在 Spotify 上进行搜索。
- **获取推荐**：`playlist_suggestions` 函数会根据用户的听歌历史和当前时间推荐 6 首歌曲。

## 脚本示例

### 认证过程

```bash
node {baseDir}/scripts/auth.mjs
```

### 调用 MCP 工具

```bash
node {baseDir}/scripts/mcp-call.mjs <tool> [json-params]
node {baseDir}/scripts/mcp-call.mjs --list-tools
```

### 使用示例

```bash
# Generate a playlist
node {baseDir}/scripts/mcp-call.mjs generate_playlist '{"mood": "chill lo-fi for studying"}'

# Get personalized suggestions
node {baseDir}/scripts/mcp-call.mjs playlist_suggestions '{"userHour": 22}'

# List playlists
node {baseDir}/scripts/mcp-call.mjs get_playlists

# Get playlist details
node {baseDir}/scripts/mcp-call.mjs get_playlist '{"id": "PLAYLIST_ID"}'

# Edit playlist songs
node {baseDir}/scripts/mcp-call.mjs edit_playlist '{"id": "PLAYLIST_ID", "addedSongs": ["4iV5W9uYEdYUVa79Axb7Rh"], "removedSongs": []}'

# Delete playlist
node {baseDir}/scripts/mcp-call.mjs delete_playlist '{"id": "PLAYLIST_ID"}'

# Search songs
node {baseDir}/scripts/mcp-call.mjs search_songs '{"query": "Blinding Lights", "limit": 5}'

# Search artists
node {baseDir}/scripts/mcp-call.mjs search_artists '{"query": "The Weeknd", "limit": 5}'

# List all available tools
node {baseDir}/scripts/mcp-call.mjs --list-tools
```

## 提供的工具

| 工具            | 描述                                      | 必需参数                         |
|------------------|-----------------------------------------|-------------------------------------------|
| `generate_playlist`    | 根据用户描述的心情生成播放列表                    | `mood` (字符串, 必需)                     |
| `get_playlists`     | 获取播放列表的详细信息和歌曲列表                   | `id` (字符串, 必需)                     |
| `get_playlists`     | 分页显示用户的播放列表                         | `lastDocId` (字符串, 可选)                   |
| `edit_playlist`     | 通过 Spotify 歌曲 ID 添加或删除歌曲                   | `id`, `addedSongs`, `removedSongs`            |
| `delete_playlist`    | 删除播放列表                                   | `id` (字符串, 必需)                     |
| `playlist_suggestions` | 根据用户听歌历史和时间推荐歌曲                         | `userHour` (0-23, 可选)                   |
| `search_songs`     | 在 Spotify 上搜索歌曲                             | `query`, `limit` (1-10)                    |
| `search_artists`     | 在 Spotify 上搜索艺术家                             | `query`, `limit` (1-10)                    |

有关参数详情、响应格式和错误处理的完整信息，请参阅 [references/api_reference.md](references/api_reference.md)。

## 播放列表生成流程（重要提示）

播放列表的生成大约需要 30 秒。请务必按照以下步骤操作：

1. 调用 `generate_playlist` 函数，系统会立即返回播放列表的 `id` 和 Spotify URL。
2. 立即将 Spotify URL 分享给用户。
3. 等待约 15 秒后，每 10 秒再次调用 `get_playlists` 函数，直到返回的状态变为 “ready”。
4. 状态变为 “ready” 后，向用户展示播放列表中的歌曲。

可以使用 `--wait` 标志来实现自动等待和更新播放列表的功能：

```bash
node {baseDir}/scripts/mcp-call.mjs generate_playlist '{"mood": "..."}' --wait
```

该脚本会自动执行生成播放列表、等待状态变化的流程（约 30 秒），然后打印出完整的播放列表。

## 注意事项

- 免费用户只能使用有限的 “试听版” 播放列表；付费用户可以使用完整的播放列表。
- `playlist_suggestions` 功能会考虑时间因素，通过传递 `userHour` 参数可以获得更合适的推荐（例如，适合晨练或深夜放松的歌曲）。
- 歌曲是通过 Spotify 的歌曲 ID 来识别的（例如：`4iV5W9uYEdYUVa79Axb7Rh`）。可以使用 `search_songs` 函数来查找歌曲的 ID。