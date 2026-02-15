---
name: prowlarr
version: 1.0.0
description: 搜索索引器并管理 Prowlarr。当用户请求“搜索种子文件”、“查找索引器”、“查找新发布的资源”、“检查索引器状态”、“列出所有索引器”、“使用 Prowlarr 进行搜索”或提及“Prowlarr/索引器管理”时，请使用这些功能。
---

# Prowlarr 功能

通过 API 在所有索引器中搜索内容，并对 Prowlarr 进行管理。

## 设置

配置文件：`~/.clawdbot/credentials/prowlarr/config.json`

```json
{
  "url": "https://prowlarr.example.com",
  "apiKey": "your-api-key"
}
```

从 Prowlarr 的“设置” → “通用” → “安全” → “API 密钥”处获取您的 API 密钥。

---

## 快速参考

### 搜索发布内容

```bash
# Basic search across all indexers
./scripts/prowlarr-api.sh search "ubuntu 22.04"

# Search torrents only
./scripts/prowlarr-api.sh search "ubuntu" --torrents

# Search usenet only
./scripts/prowlarr-api.sh search "ubuntu" --usenet

# Search specific categories (2000=Movies, 5000=TV, 3000=Audio, 7000=Books)
./scripts/prowlarr-api.sh search "inception" --category 2000

# TV search with TVDB ID
./scripts/prowlarr-api.sh tv-search --tvdb 71663 --season 1 --episode 1

# Movie search with IMDB ID
./scripts/prowlarr-api.sh movie-search --imdb tt0111161
```

### 列出索引器

```bash
# All indexers
./scripts/prowlarr-api.sh indexers

# With status details
./scripts/prowlarr-api.sh indexers --verbose
```

### 索引器状态与统计信息

```bash
# Usage stats per indexer
./scripts/prowlarr-api.sh stats

# Test all indexers
./scripts/prowlarr-api.sh test-all

# Test specific indexer
./scripts/prowlarr-api.sh test <indexer-id>
```

### 索引器管理

```bash
# Enable/disable an indexer
./scripts/prowlarr-api.sh enable <indexer-id>
./scripts/prowlarr-api.sh disable <indexer-id>

# Delete an indexer
./scripts/prowlarr-api.sh delete <indexer-id>
```

### 应用程序同步

```bash
# Sync indexers to Sonarr/Radarr/etc
./scripts/prowlarr-api.sh sync

# List connected apps
./scripts/prowlarr-api.sh apps
```

### 系统信息

```bash
# System status
./scripts/prowlarr-api.sh status

# Health check
./scripts/prowlarr-api.sh health
```

---

## 搜索类别

| ID | 类别 |
|----|----------|
| 2000 | 电影 |
| 5000 | 电视节目 |
| 3000 | 音频 |
| 7000 | 书籍 |
| 1000 | 游戏机游戏 |
| 4000 | 个人电脑游戏 |
| 6000 | 其他类型 |

子类别：2010（电影/外语）、2020（电影/其他类型）、2030（电影/标清）、2040（电影/高清）、2045（电影/超高清）、2050（电影/蓝光）、2060（电影/3D）、5010（电视节目/Web-DL 格式）、5020（电视节目/外语）、5030（电视节目/标清）、5040（电视节目/高清）、5045（电视节目/超高清）等。

---

## 常见使用场景

**“搜索最新的 Ubuntu ISO 镜像”**
```bash
./scripts/prowlarr-api.sh search "ubuntu 24.04"
```

**“查找《权力的游戏》第 1 部第 1 集”**
```bash
./scripts/prowlarr-api.sh tv-search --tvdb 121361 --season 1 --episode 1
```

**“搜索 4K 格式的《盗梦空间》”**
```bash
./scripts/prowlarr-api.sh search "inception 2160p" --category 2045
```

**“检查我的索引器是否正常运行”**
```bash
./scripts/prowlarr-api.sh stats
./scripts/prowlarr-api.sh test-all
```

**“将索引器更新推送到 Sonarr/Radarr”**
```bash
./scripts/prowlarr-api.sh sync
```