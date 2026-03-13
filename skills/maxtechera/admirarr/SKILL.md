---
name: admirarr
description: "管理 Jellyfin/Plex 结合 *Arr 媒体服务器堆栈：检查状态、添加内容、监控下载进度、诊断问题以及重启相关服务。"
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - admirarr
---
# Admirarr

这是一个用于自托管媒体服务器堆栈的命令行工具（CLI）。它使用一个可执行文件，提供了26个命令，并且所有输出都以JSON格式呈现。

**安装方法：**  
`curl -fsSL https://get.admirarr.dev | sh`

## 命令列表

### 状态与诊断  
```bash
admirarr status [-o json] [--live]     # Fleet dashboard — services, libraries, queues, disk
admirarr health [-o json]              # Health warnings from Radarr, Sonarr, Prowlarr
admirarr disk [-o json]                # Disk space breakdown
admirarr docker [-o json]              # Docker container status
admirarr doctor [-o json]              # 15 diagnostic categories, 34 checks
admirarr doctor --fix                  # Built-in fixes → AI agent for the rest
```

### 库管理  
```bash
admirarr movies [-o json]             # Movie library with file status
admirarr shows [-o json]              # TV shows with episode counts
admirarr recent [-o json]             # Recently added (Jellyfin or Plex)
admirarr history [-o json]            # Watch history
admirarr missing [-o json]            # Monitored without files
admirarr requests [-o json]           # Seerr media requests
```

### 搜索与添加媒体内容  
```bash
admirarr search "<query>" [-o json]   # Search all Prowlarr indexers
admirarr find "<query>" [-o json]     # Search Radarr releases
admirarr add-movie "<query>"          # Interactive: search → pick → add to Radarr
admirarr add-show "<query>"           # Interactive: search → pick → add to Sonarr
```

### 下载管理  
```bash
admirarr downloads [-o json]          # Active qBittorrent torrents
admirarr downloads pause [hash|all]   # Pause torrents
admirarr downloads resume [hash|all]  # Resume torrents
admirarr downloads remove <hash> [--delete-files]
admirarr queue [-o json]              # Radarr + Sonarr import queues
```

### 索引器配置  
```bash
admirarr indexers [-o json]           # Prowlarr indexer status
admirarr indexers setup               # Interactive indexer wizard
admirarr indexers add <name>          # Add an indexer
admirarr indexers remove <name>       # Remove an indexer
admirarr indexers test                # Test all indexer connectivity
admirarr indexers sync                # Sync indexers to config.yaml
```

### 媒体质量设置  
```bash
admirarr recyclarr                    # Recyclarr status
admirarr recyclarr sync [instance]    # Run Recyclarr sync
admirarr recyclarr verify             # Check quality profiles
admirarr recyclarr instances          # List configured instances
```

### 服务器管理  
```bash
admirarr scan                         # Trigger media server library scan
admirarr restart <service>            # Restart a Docker container
admirarr logs <service>               # Recent logs
admirarr setup                        # Full setup wizard (12 phases)
admirarr migrate                      # Generate Docker Compose stack
```

## 支持的媒体服务器服务  
**默认服务组合：**  
Jellyfin, Radarr, Sonarr, Prowlarr, qBittorrent, Gluetun, Seerr, Bazarr, FlareSolverr, Watchtower  

**可选服务：**  
Plex, Lidarr, Readarr, Whisparr, SABnzbd, Autobrr, Unpackerr, Recyclarr, Profilarr, Tdarr, Tautulli, Jellystat, Notifiarr, Maintainerr  

该工具会自动检测系统上安装的媒体服务器（优先检测Jellyfin，其次为Plex）。无论采用何种部署方式，所有服务的信息均通过HTTP接口进行获取。

## 工作流程示例  

| 目标 | 所需命令 |  
|---|---|  
| 了解服务器状态 | `status` → `doctor` → `health` |  
| 解决问题 | `doctor -o json` → 问题定位 → `restart` / 问题修复 → 再次执行 `doctor` |  
| 添加媒体内容 | `movies -o json`（检查是否存在）→ `add-movie` → `downloads` → `queue` |  
| 处理下载失败 | `downloads -o json` → `queue -o json` → `health` → `doctor` |  
| 查找缺失的媒体文件 | `missing -o json` → `requests -o json` |  

## 使用规则：  
- 所有输出均以JSON格式提供（使用 `-o json` 选项）。  
- 在执行重启或可能破坏数据操作的命令前，需先获得用户确认。  
- 数据以表格形式呈现，而非原始JSON格式。  
- 禁止删除用户的文件或媒体文件。  
- 禁止直接修改与媒体服务器相关的数据库文件。