---
name: arr-all
version: 1.0.0
description: Radarr、Sonarr 和 Lidarr 的统一命令行界面：支持搜索、添加和管理电影（Radarr）、电视节目（Sonarr）以及音乐（Lidarr），并提供日历视图和设备健康状况监控功能。
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
    optional:
      bins: ["column"]
---

# Arr-All

这是一个用于管理 Radarr（电影）、Sonarr（电视节目）和 Lidarr（音乐）的统一接口。

## 设置

### 配置

你可以使用一个统一的配置文件，或者现有的单独配置文件。

**统一配置（推荐）：**
创建 `~/.openclaw/credentials/arr-all/config.json` 文件：

```json
{
  "radarr": {
    "url": "http://localhost:7878",
    "apiKey": "...",
    "defaultQualityProfile": 1
  },
  "sonarr": {
    "url": "http://localhost:8989",
    "apiKey": "...",
    "defaultQualityProfile": 1,
    "defaultSeriesType": "standard"
  },
  "lidarr": {
    "url": "http://localhost:8686",
    "apiKey": "...",
    "defaultQualityProfile": 2,
    "defaultMetadataProfile": 7
  }
}
```

**旧版配置：**
现有的配置文件（位于 `~/.openclaw/credentials/{radarr,sonarr,lidarr}/config.json`）也是支持的。

## 使用方法

命令格式：`arr-all <类型> <操作> [参数]`

### 常用命令

所有媒体类型都支持以下核心命令：

- **搜索**：`arr-all [电影|电视|音乐] search "查询内容"`
- **添加**：`arr-all [电影|电视|音乐] add <ID>`
- **检查**：`arr-all [电影|电视|音乐] exists <ID>`
- **删除**：`arr-all [电影|电视|音乐] remove <ID> [--delete-files]`
- **配置**：`arr-all [电影|电视|音乐] config`

### 公共命令

- **日历**：`arr-all calendar [天数=7]`（显示即将发布的媒体内容）
- **状态**：`arr-all health`（查看所有应用程序的状态）
- **连接状态**：`arr-all status`（查看连接状态）
- **综合搜索**：`arr-all search "查询内容"`（同时搜索三种媒体类型）

### 类型特定功能

**电影（Radarr）：**

- `arr-all movie add-collection <ID>`
- `arr-all movie collections`（查看电影收藏列表）

**电视节目（Sonarr）：**

- `arr-all tv add <ID> [--monitor latest|all|none|seasons:1,2]`（添加电视节目或按季度监控）
- `arr-all tv seasons <ID>`（查看电视节目的季数）
- `arr-all tv monitor-season <ID> <季度>`（监控特定季度的节目）

**音乐（Lidarr）：**

- `arr-all music add <ID> [--discography]`（添加音乐专辑）
- `arr-all music albums <ID>`（查看音乐专辑列表）
- `arr-all music monitor-album <ID>`（监控特定专辑的播放情况）

## 示例

**添加一部电影：**

```bash
arr-all movie search "Dune"
arr-all movie add 438631
```

**查看日历：**

```bash
arr-all calendar
```

**查看应用程序状态：**

```bash
arr-all health
```