---
name: clawarr-suite
description: 全面管理自托管的媒体库系统（包括 Sonarr、Radarr、Lidarr、Readarr、Prowlarr、Bazarr、Overseerr、Plex、Tautulli、SABnzbd、Recyclarr、Unpackerr、Notifiarr、Maintainerr、Kometa、FlareSolverr）。支持深度库资源探索、数据分析、仪表板生成、内容管理、请求处理、字幕管理、索引器控制、下载监控、质量参数同步、库资源自动清理、通知路由功能，以及与媒体跟踪工具（如 Trakt、Letterboxd、Simkl）的集成。
homepage: https://github.com/omiron33/clawarr-suite
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["bash", "curl", "jq", "bc", "sed"] },
        "security":
          {
            "networkScope": "local-lan-and-user-configured-hosts",
            "secretsPolicy": "api keys loaded from env/user config only; never hardcoded",
            "destructiveActions": "none by default; explicit command required for delete/remove actions"
          },
        "capabilities":
          [
            "arr-api-management",
            "docker-service-observability",
            "dashboard-generation",
            "media-tracker-sync"
          ]
      }
  }
---
# ClawARR套件

这是一个用于自托管媒体自动化堆栈的统一深度集成控制工具。该工具提供了对整个*arr生态系统*的全面代理可执行操作，包括丰富的分析功能、仪表板生成以及高级库探索功能。

## 安全性与扫描器透明度

- **优先使用本地资源**：所有API调用都针对用户提供的本地主机（通常是局域网/NAS）。
- **不嵌入敏感信息**：API密钥/令牌来自环境变量或用户自己的配置文件。
- **无数据传输风险**：脚本不会将凭证或库数据传输到第三方端点。
- **破坏性操作需用户明确授权**：删除/移除操作需要用户/代理的明确指令。
- **设置逻辑避免动态执行**：使用明确的变量映射来确保扫描器的兼容性。

## 快速入门

**首次设置（推荐）：**
```bash
scripts/setup.sh <host-ip-or-hostname>
```
发现服务、获取API密钥、验证连接并输出配置信息。

**常见操作：**
```bash
scripts/status.sh              # Health check all services
scripts/library.sh stats all   # Library statistics
scripts/analytics.sh activity  # Current Plex streams
scripts/dashboard.sh           # Generate HTML dashboard
scripts/manage.sh wanted all   # Show missing content
scripts/requests.sh list       # Overseerr requests
```

## 脚本概述

### 核心操作
- **`setup.sh`** — 带有自动发现功能的引导式设置向导
- **`discover.sh`** — 扫描主机上的*arr服务*
- **`status.sh`** — 检查所有已配置服务的运行状态
- **`diagnose.sh`** — 自动故障排除

### 库探索 (`library.sh`)
针对Radarr/Sonarr/Lidarr的深度统计和探索：
```bash
library.sh stats [app]          # Overall library stats
library.sh quality [app]        # Quality profile breakdown
library.sh missing [app]        # Missing/wanted content
library.sh unmonitored [app]    # Unmonitored items
library.sh recent [app] [days]  # Recently added (default: 7)
library.sh genres [app]         # Genre distribution
library.sh years [app]          # Year distribution
library.sh studios [app]        # Studio/network breakdown
library.sh nofiles [app]        # Monitored but no files
library.sh disk [app]           # Disk usage by root folder
```

### 分析 (`analytics.sh)`
来自Tautulli/Plex的丰富视图分析：
```bash
analytics.sh activity                 # Currently watching
analytics.sh history [count]          # Watch history
analytics.sh most-watched [period]    # Most watched (week/month/year)
analytics.sh popular-genres [period]  # Popular genres
analytics.sh peak-hours               # Peak watching hours
analytics.sh user-stats [user]        # User activity
analytics.sh library-stats            # Plex library stats
analytics.sh recent-added [count]     # Recently added to Plex
analytics.sh play-totals              # Total play statistics
```

### 内容管理 (`manage.sh)`
添加、删除和管理内容：
```bash
manage.sh add-movie "<title>" [quality] [root]
manage.sh add-series "<title>" [quality] [root]
manage.sh remove <app> <id>
manage.sh wanted [app]
manage.sh calendar [app] [days]
manage.sh history [app] [count]
manage.sh rename <app> <id>
manage.sh refresh <app> [id]
```

### 请求管理 (`requests.sh`)
监控请求处理：
```bash
requests.sh list [pending|approved|available|all]
requests.sh approve <id>
requests.sh deny <id> [reason]
requests.sh info <id>
requests.sh stats
```

### 字幕管理 (`subtitles.sh`)
Bazarr相关操作：
```bash
subtitles.sh wanted
subtitles.sh history [count]
subtitles.sh search <series|movie> <id>
subtitles.sh languages
```

### 索引器管理 (`indexers.sh`)
Prowlarr相关操作：
```bash
indexers.sh list
indexers.sh test [id]
indexers.sh stats
```

### 下载客户端 (`downloads.sh`)
SABnzbd相关操作：
```bash
downloads.sh active
downloads.sh speed
downloads.sh history [count]
downloads.sh pause
downloads.sh resume
downloads.sh queue
```

### 仪表板生成 (`dashboard.sh)`
生成自包含的HTML仪表板：
```bash
dashboard.sh [output_file]
```
创建美观的暗主题仪表板，包含：
- 系统健康状况
- 下载活动
- 库统计信息
- 最近活动
- 视频观看分析
- 磁盘使用情况

输出默认为`clawarr-dashboard.html`（可在任何浏览器中打开）。

### 媒体跟踪器集成 (`trakt.sh`, `trackers.sh`, `letterboxd.sh`, `simkl.sh`

跨Trakt.tv、Letterboxd、Simkl等服务跟踪和同步您的观看记录。

**统一接口 (`trackers.sh`):**
```bash
trackers.sh setup              # Interactive setup wizard
trackers.sh status             # Show configured trackers
trackers.sh sync plex trakt    # Sync Plex → Trakt
trackers.sh export trakt json  # Export watch history
trackers.sh import letterboxd file.csv
trackers.sh compare trakt simkl
```

**Trakt.tv集成 (`trakt.sh`):**

*认证：*
```bash
trakt.sh auth                  # Device code OAuth flow
trakt.sh auth-status           # Check authentication
```

*个人资料与统计：*
```bash
trakt.sh profile [username]    # Show profile
trakt.sh stats [username]      # Detailed statistics
```

*观看记录与历史：*
```bash
trakt.sh watching              # Currently watching
trakt.sh history [movies|shows|episodes] [limit]
trakt.sh sync-history export file.json
trakt.sh sync-history import file.json
```

*抓取记录：*
```bash
trakt.sh scrobble start movie 12345
trakt.sh scrobble stop movie 12345 100
trakt.sh checkin movie "Inception"
```

*列表与收藏：*
```bash
trakt.sh watchlist [movies|shows]
trakt.sh watchlist-add movie "Dune Part Two"
trakt.sh collection movies
trakt.sh collection-add movie 12345
trakt.sh lists                 # Custom lists
trakt.sh list-items my-favorites
```

*评分：*
```bash
trakt.sh ratings movies 8      # Movies rated 8+
trakt.sh rate movie "Inception" 10
```

*发现功能：*
```bash
trakt.sh recommendations movies
trakt.sh trending shows
trakt.sh popular movies
trakt.sh calendar all 7        # Next 7 days
```

*搜索：*
```bash
trakt.sh search "Breaking Bad" show
```

*同步：*
```bash
trakt.sh sync-plex             # Sync Plex watch history to Trakt
```

**Letterboxd集成 (`letterboxd.sh`):**
```bash
letterboxd.sh export           # Export from Plex as Letterboxd CSV
letterboxd.sh import diary.csv # Import Letterboxd diary
letterboxd.sh profile username # View public profile
letterboxd.sh diary username 2024
```

**Simkl集成 (`simkl.sh`):**
```bash
simkl.sh auth                  # OAuth authentication
simkl.sh profile               # Show profile
simkl.sh stats                 # Viewing statistics
simkl.sh history movies        # Watch history
simkl.sh watchlist all         # View watchlist
simkl.sh sync                  # Sync with Plex
```

### Traktarr与Retraktarr集成

自动发现内容并将库同步到Trakt列表。

**Traktarr (Trakt → Radarr/Sonarr):**
```bash
# Status and configuration
trakt.sh traktarr-status       # Check if installed
trakt.sh traktarr-config       # Configure Traktarr

# Add content from Trakt lists
trakt.sh traktarr-add movies trending 10
trakt.sh traktarr-add movies anticipated 15
trakt.sh traktarr-add movies popular 5
trakt.sh traktarr-add shows trending 5
trakt.sh traktarr-add movies watchlist 50
```

**Retraktarr (Radarr/Sonarr → Trakt):**
```bash
# Status and configuration
trakt.sh retraktarr-status     # Check if installed
trakt.sh retraktarr-config     # Configure Retraktarr

# Sync library to Trakt lists
trakt.sh retraktarr-sync all   # Sync movies and shows
trakt.sh retraktarr-sync movies
trakt.sh retraktarr-sync shows
```

**通过设置向导安装：**
```bash
trackers.sh setup
# Choose option 5 for Traktarr
# Choose option 6 for Retraktarr
# Offers to install via pip if not found
```

**功能说明：**
- **Traktarr：**自动将Trakt列表中的内容（热门、预期、观看列表、自定义）添加到Radarr/Sonarr以供下载
- **Retraktarr：**将您的Radarr/Sonarr库同步回Trakt，作为公共或私有列表

有关完整设置、定时任务安排和使用模式的详细信息，请参阅`references/traktarr-retraktarr.md`。

### Prowlarr索引器管理 (`prowlarr.sh)`
跨所有*arr应用*集中管理索引器：
```bash
prowlarr.sh indexers              # List all indexers
prowlarr.sh test [id]             # Test indexer(s)
prowlarr.sh stats                 # Indexer & app sync statistics
prowlarr.sh search <query> [type] # Search across all indexers (type: movie|tv|audio|book)
prowlarr.sh apps                  # List sync targets (Sonarr/Radarr/etc)
prowlarr.sh add-app <type> <url> <key>  # Add app sync target
prowlarr.sh sync                  # Trigger sync to all apps
prowlarr.sh status                # Health check
prowlarr.sh logs [count]          # Recent logs
```

### Recyclarr质量配置文件 (`recyclarr.sh)`
将TRaSH Guide的质量配置文件同步到Sonarr/Radarr：
```bash
recyclarr.sh status               # Check status & config
recyclarr.sh sync [instance]      # Sync profiles (all or specific)
recyclarr.sh diff [instance]      # Preview changes without applying
recyclarr.sh profiles             # List available TRaSH profiles
recyclarr.sh qualities [app]      # List quality definitions
recyclarr.sh config               # Show current config
recyclarr.sh create-config        # Generate config template
recyclarr.sh logs [count]         # View recent logs
```

### Maintainerr库清理 (`maintainerr.sh)`
根据规则自动清理库：
```bash
maintainerr.sh status             # Check status
maintainerr.sh rules              # List cleanup rules
maintainerr.sh collections        # List managed collections
maintainerr.sh run [rule_id]      # Trigger rules (all or specific)
maintainerr.sh media <rule_id>    # Show media matched by a rule
maintainerr.sh exclude <media_id> <rule_id>  # Exclude media from rule
maintainerr.sh logs               # View activity log
```

### Notifiarr通知 (`notifiarr.sh)`
跨*arr服务*统一管理通知：
```bash
notifiarr.sh status               # Check status & integrations
notifiarr.sh triggers             # List notification triggers
notifiarr.sh services             # Show connected services
notifiarr.sh test [channel]       # Send test notification
notifiarr.sh config               # Configuration summary
notifiarr.sh logs                 # Recent notification log
```

### Kometa收藏管理 (`kometa.sh`)
Plex收藏、叠加层和元数据自动化：
```bash
kometa.sh status                  # Check container status
kometa.sh run [library]           # Run Kometa (all or specific library)
kometa.sh collections             # Show Plex collections
kometa.sh overlays                # Check overlay config
kometa.sh config                  # Show Kometa config
kometa.sh templates               # List available default collections/overlays
kometa.sh logs [count]            # View recent logs
```

### Unpackerr档案提取 (`unpackerr.sh)`
为下载客户端自动提取档案：
```bash
unpackerr.sh status               # Check status & config
unpackerr.sh activity             # Recent extraction activity
unpackerr.sh errors               # Recent errors/warnings
unpackerr.sh config               # Show configuration
unpackerr.sh logs [count]         # View recent logs
unpackerr.sh restart              # Restart container
```

### 旧版脚本
- **`queue.sh`** — 查看下载队列（使用`manage.sh wanted`或`downloads.sh active`获取更多详细信息）
- **`search.sh`** — 搜索内容（使用`manage.sh add-*`完成整个工作流程）

## 配置

### 环境变量

**核心服务：**
```bash
export CLAWARR_HOST=192.168.1.100
export SONARR_KEY=abc123...
export RADARR_KEY=def456...
export LIDARR_KEY=ghi789...
export READARR_KEY=jkl012...
export PROWLARR_KEY=mno345...
export BAZARR_KEY=pqr678...
export OVERSEERR_KEY=stu901...
export PLEX_TOKEN=vwx234...
export TAUTULLI_KEY=yz567...
export SABNZBD_KEY=abc890...
export NOTIFIARR_KEY=xyz123...

# Companion services (auto-detected, keys optional)
export PROWLARR_KEY=abc123...   # Required for prowlarr.sh

# Docker-based services (SSH access for remote management)
export RECYCLARR_SSH=mynas       # SSH host for recyclarr container
export KOMETA_SSH=mynas          # SSH host for kometa container
export UNPACKERR_SSH=mynas       # SSH host for unpackerr container
export DOCKER_CONFIG_BASE=/opt/docker  # Docker config root (default: /volume1/docker for Synology)
```

**媒体跟踪器（可选）：**
```bash
# Trakt.tv (register app at https://trakt.tv/oauth/applications/new)
export TRAKT_CLIENT_ID=your_client_id
export TRAKT_CLIENT_SECRET=your_client_secret

# Simkl (register at https://simkl.com/settings/developer)
export SIMKL_CLIENT_ID=your_client_id
export SIMKL_CLIENT_SECRET=your_client_secret

# Letterboxd (requires API approval)
export LETTERBOXD_API_KEY=your_api_key  # Optional, uses CSV export if not set
```

**令牌存储：**
- 令牌自动保存在`~/.config/clawarr/`目录下
- 文件：`trakt_tokens.json`, `simkl_tokens.json`
- 权限：600（用户仅读写）

请将配置保存在`.env`文件中，并在运行脚本前加载。

### 标准端口
- Sonarr: 8989
- Radarr: 7878
- Lidarr: 8686
- Readarr: 8787
- Prowlarr: 9696
- Bazarr: 6767
- Overseerr: 5055
- Plex: 32400
- Tautulli: 8181
- SABnzbd: 38080
- Notifiarr: 5454
- Maintainerr: 6246
- FlareSolverr: 8191
- Homarr: 7575

## API密钥获取

### 方法1：/initialize.json（最简单）
大多数*arr应用*在公共端点暴露API密钥：
```bash
curl -s http://HOST:7878/initialize.json | jq -r '.apiKey'
```

对于旧版本（v3）：
```bash
curl -s http://HOST:7878/initialize.js | grep -o "apiKey: '[^']*'" | cut -d"'" -f2
```

### 方法2：配置文件
**Docker/Unraid/Synology：** `/config/config.xml`（在容器内部）
```bash
grep '<ApiKey>' /path/to/config.xml | sed 's/.*<ApiKey>\(.*\)<\/ApiKey>.*/\1/'
```

### 方法3：Web UI
设置 → 通用 → 安全 → API密钥

### Plex令牌
通过Plex Web UI获取：
1. 打开任意媒体项目
2. “获取信息” → “查看XML”
3. URL中包含`X-Plex-Token=...`

或者使用：
```bash
curl -u "username:password" -X POST \
  'https://plex.tv/users/sign_in.json' \
  -H "X-Plex-Client-Identifier: <unique-id>"
```

### Tautulli API密钥
设置 → Web界面 → API → API密钥

### SABnzbd API密钥
配置 → 通用 → 安全 → API密钥

## 常见工作流程

### 库分析
```bash
# Get complete library overview
scripts/library.sh stats all

# Find quality upgrade candidates
scripts/library.sh quality radarr

# Show missing content
scripts/library.sh missing all

# Check disk usage
scripts/library.sh disk all
```

### 视频观看分析
```bash
# Current activity
scripts/analytics.sh activity

# Most watched this month
scripts/analytics.sh most-watched month

# User statistics
scripts/analytics.sh user-stats

# Peak hours
scripts/analytics.sh peak-hours
```

### 请求管理
```bash
# Show pending requests
scripts/requests.sh list pending

# Approve request
scripts/requests.sh approve 123

# Request statistics
scripts/requests.sh stats
```

### 内容管理
```bash
# Add movie
scripts/manage.sh add-movie "Dune Part Two"

# Show calendar
scripts/manage.sh calendar all 7

# View history
scripts/manage.sh history radarr 30

# Show wanted/missing
scripts/manage.sh wanted all
```

### 索引器管理（Prowlarr）
```bash
# List and test all indexers
scripts/prowlarr.sh indexers
scripts/prowlarr.sh test

# Search across all indexers
scripts/prowlarr.sh search "Dune" movie

# Add Sonarr/Radarr as sync targets
scripts/prowlarr.sh add-app sonarr http://host:8989 <sonarr_key>
scripts/prowlarr.sh add-app radarr http://host:7878 <radarr_key>

# Trigger indexer sync to all apps
scripts/prowlarr.sh sync
```

### 质量配置文件（Recyclarr）
```bash
# Preview changes
scripts/recyclarr.sh diff

# Sync TRaSH Guides profiles
scripts/recyclarr.sh sync

# Check status
scripts/recyclarr.sh status
```

### 库清理（Maintainerr）
```bash
# View rules and matched media
scripts/maintainerr.sh rules
scripts/maintainerr.sh media 1

# Run cleanup
scripts/maintainerr.sh run

# Exclude something from cleanup
scripts/maintainerr.sh exclude 12345 1
```

### 收藏与叠加层（Kometa）
```bash
# Run collection/overlay generation
scripts/kometa.sh run

# View existing collections
scripts/kometa.sh collections

# See available templates
scripts/kometa.sh templates
```

### 仪表板
```bash
# Generate dashboard
scripts/dashboard.sh my-dashboard.html

# Open in browser
open my-dashboard.html
```

### 媒体跟踪工作流程

**初始设置：**
```bash
# Set up Trakt.tv
scripts/trackers.sh setup
# Select option 1 (Trakt.tv)
# Follow device auth flow

# Check status
scripts/trackers.sh status
```

**将Plex数据同步到Trakt：**
```bash
# One-time sync of watch history
scripts/trakt.sh sync-plex

# Or use unified interface
scripts/trackers.sh sync plex trakt
```

**导出到Letterboxd：**
```bash
# Generate Letterboxd-compatible CSV
scripts/letterboxd.sh export

# Upload at letterboxd.com/import/
```

**跨跟踪器同步：**
```bash
# Export from Trakt, convert for Letterboxd
scripts/trackers.sh sync trakt letterboxd

# Compare two services
scripts/trackers.sh compare trakt simkl
```

**发现与推荐：**
```bash
# Get personalized recommendations
scripts/trakt.sh recommendations movies

# See what's trending
scripts/trakt.sh trending shows

# Check upcoming releases
scripts/trakt.sh calendar all 7
```

**跟踪观看记录：**
```bash
# See what you're currently watching
scripts/trakt.sh watching

# View watch history
scripts/trakt.sh history movies 50

# Rate something you watched
scripts/trakt.sh rate movie "Inception" 10
```

**Traktarr/Retraktarr自动化：**
```bash
# Set up Traktarr (Trakt → Arr)
scripts/trackers.sh setup  # Option 5

# Add trending movies to Radarr
scripts/trakt.sh traktarr-add movies trending 10

# Add anticipated shows to Sonarr
scripts/trakt.sh traktarr-add shows anticipated 5

# Set up Retraktarr (Arr → Trakt)
scripts/trackers.sh setup  # Option 6

# Sync library to Trakt lists
scripts/trakt.sh retraktarr-sync all

# Schedule automation (cron):
# Traktarr every 6 hours: 0 */6 * * * traktarr run
# Retraktarr daily at 3am: 0 3 * * * retraktarr sync
```

## 故障排除

### 无法导入文件

**诊断：**
```bash
scripts/diagnose.sh
```

常见原因：
1. **Docker挂载失败** — 容器重新启动但主机未重启
2. **路径映射问题** — 下载客户端和*arr应用**查看的路径不同
3. **权限问题** — *arr应用**无法读取下载目录
4. **类别不匹配** — 下载的文件属于错误的类别

**解决方案：**
```bash
# Restart containers (fixes stale mounts)
docker restart radarr sonarr

# Check path mappings
# Settings → Download Clients → Remote Path Mappings
```

### 下载队列卡住

**检查下载客户端：**
```bash
scripts/downloads.sh active
scripts/downloads.sh speed
```

**检查*arr队列**：
```bash
scripts/manage.sh wanted all
```

**检查索引器：**
```bash
scripts/indexers.sh test
scripts/indexers.sh stats
```

### 字幕缺失

```bash
scripts/subtitles.sh wanted
scripts/subtitles.sh search series <id>
```

## 参考文档

- **`references/api-endpoints.md`** — 所有服务的完整API参考
- **`references/tracker-apis.md`** — 媒体跟踪器API文档（Trakt, Simkl, Letterboxd）
- **`references/traktarr-retraktarr.md** — Traktarr与Retraktarr自动化的完整指南
- **`references/companion-services.md` — Prowlarr, Recyclarr, FlareSolverr, Unpackerr, Maintainerr, Kometa的参考资料
- **`references/common-issues.md** — 故障排除指南及解决方案
- **`references/setup-guide.md** — 平台特定的安装指南
- **`references/prompts.md` — 为代理提供的建议性自然语言提示
- **`references/dashboard-templates.md** — 仪表板的HTML/CSS模板

## 代理提示示例

请参阅`references/prompts.md`以获取完整列表。示例包括：

**库与下载：**
- “显示当前正在下载的内容”
- “这周添加了哪些电影？”
- “生成我的媒体库仪表板”
- “本月观看次数最多的节目是什么？”
- “查找所有可以升级到4K的720p电影”
- “显示所有被监控节目的缺失剧集”
- “这周有什么新电影上映？”
- “批准所有待处理的Overseerr请求”
- “每个库我使用了多少磁盘空间？”
- “显示我过去30天的Plex观看统计”
- “缺少哪些字幕？”
- “测试所有索引器的性能”

**媒体跟踪：**
- “为我的Plex库设置Trakt跟踪”
- “将我的Plex观看历史同步到Trakt”
- “我在Trakt上当前正在看什么？”
- “显示我这个月的Trakt观看历史”
- “根据我的Trakt评分推荐电影”
- “显示Trakt上的热门电影”
- “将我的电影列表导出到Letterboxd”
- “比较我的Trakt和Simkl观看历史”
- “显示我正在跟踪的即将上映的电影”
- “在Trakt上给《盗梦空间》打10分”
- “将《沙丘2》添加到我的Trakt观看列表”
- “显示我的Letterboxd配置信息”
- “我在Trakt上评分最高的电影是什么？”

**Prowlarr与索引器：**
- “显示所有索引器并测试它们”
- “在所有索引器中搜索《绝命毒师》”
- “将Prowlarr索引器同步到Sonarr和Radarr”
- **在Prowlarr中添加Sonarr作为同步目标”

**质量配置文件（Recyclarr）：**
- “同步TRaSH Guide的质量配置文件”
- “预览Recyclarr会做出的更改”
- “显示Radarr可用的质量配置文件”
- “Sonarr有哪些质量定义？”

**库清理（Maintainerr）：**
- “显示我的库清理规则”
- “哪些电影被标记为需要删除？”
- “立即运行所有清理规则”
- “从清理规则中排除这部电影”

**收藏与叠加层（Kometa）：**
- “运行Kometa更新收藏”
- “显示我所有的Plex收藏”
- “有哪些叠加层模板可用？”
- “将IMDb Top 250收藏添加到我的电影库”

**通知（Notifiarr）：**
- “检查Notifiarr的状态和集成情况”
- “发送测试通知”
- “显示最近的通知”

**档案提取（Unpackerr）：**
- “检查Unpackerr的状态”
- “显示最近的提取活动”
- “有提取错误吗？”

**Traktarr/Retraktarr自动化：**
- “设置Traktarr自动添加热门电影”
- “将Trakt上的前10部热门电影添加到Radarr”
- **配置Traktarr监控我的Trakt观看列表**
- **将我的Radarr库同步到公共Trakt列表**
- “显示Traktarr的状态和配置”
- “通过Traktarr将热门节目添加到Sonarr”
- **设置Trakt和我的*arr应用*之间的自动同步”
- “Retraktarr在做什么？是否已同步？”

## 技术说明

### Bash 3.2兼容性
所有脚本兼容macOS bash 3.2：
- 不支持关联数组（`declare -A`）
- 不支持大写参数扩展（`${var^^}`）
- 使用`$(echo "$var" | tr '[:lower:]' '[:upper:]')`进行大小写转换
- 不使用`|&`（管道标准错误输出），改用`2>&1`

### 依赖项
- **curl** — HTTP请求
- **jq** — JSON解析
- **bc** — 数学计算（用于百分比、GB转换）
- **sed** — 文本处理

这些工具在macOS/Linux上都是标准配置。

### 安全性
- 绝不记录API密钥
- 确认破坏性操作（删除、移除）需要用户确认
- 对批量操作进行速率限制
- 使用HTTPS进行远程访问

### 性能
- 脚本尽可能缓存API响应
- 仪表板生成每次运行时只拉取一次数据
- 在可能的情况下，批量操作使用批量API

## 版本兼容性

已测试兼容以下版本：
- Sonarr v4.x（API v3）
- Radarr v5.x（API v3）
- Lidarr v2.x（API v1）
- Readarr v0.3.x（API v1）
- Prowlarr v1.x（API v1）
- Bazarr v1.4.x
- Overseerr v1.33.x（API v1）
- Plex Media Server（所有最新版本）
- Tautulli v2.x（API v2）
- SABnzbd v4.x
- Recyclarr v7.x
- Unpackerr v0.14.x
- Notifiarr v0.8.x
- Maintainerr v2.x
- Kometa v2.x（Plex Meta Manager的继任者）
- FlareSolverr v3.x

## 贡献

如需报告问题或建议功能，请通过GitHub进行。请提供以下信息：
- 脚本名称及执行命令
- 错误输出（请对API密钥进行加密处理！）
- 服务版本
- 平台（Docker/Unraid/Synology等）

## 许可证

MIT许可证 - 详情请参见仓库。