---
name: owntracks-location
description: >
  通过 OwnTracks 的 HTTP Webhook 接收器实现实时手机位置跟踪，支持对特定地点的查询以及基于距离的搜索功能。适用场景包括：  
  (1) 用户询问“我在哪里？”；  
  (2) 存储用户指定的位置（如家、健身房、工作地点）；  
  (3) 按距离查询附近的地点；  
  (4) 查看用户的移动历史记录。  
  所需条件：  
  - 手机上需安装 OwnTracks 应用程序；  
  - 确保设备连接到 Tailscale 或局域网（LAN）；  
  - 使用 Node.js 22 及更高版本；  
  - 数据库建议使用 better-sqlite3。
---
# OwnTracks 位置服务

通过 OwnTracks 实现实时位置追踪，数据通过 HTTP Webhook 发送到 SQLite 数据库中。

## 架构

```
Phone (OwnTracks) → HTTP POST → server.mjs (port 18793) → SQLite + latest.json
Agent queries → places.mjs CLI or curl http://localhost:18793/latest
```

## 设置

### 1. 启动接收端服务

```bash
node scripts/server.mjs
# Default port: 18793. Override: OWNTRACKS_PORT=9999
# Data dir override: OWNTRACKS_DATA=/path/to/data
```

**建议**：将此服务设置为用户的 systemd 服务，以实现数据持久化。

```bash
mkdir -p ~/.config/systemd/user
cat << 'EOF' > ~/.config/systemd/user/owntracks-receiver.service
[Unit]
Description=OwnTracks Location Receiver
After=network.target

[Service]
Type=simple
Environment=OWNTRACKS_PORT=18793
Environment=OWNTRACKS_DATA=<SKILL_DIR>/scripts/data
ExecStart=/usr/local/bin/node <SKILL_DIR>/scripts/server.mjs
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now owntracks-receiver
```

请将 `<SKILL_DIR>` 替换为该技能目录的绝对路径。

### 2. 在手机上配置 OwnTracks

1. 从 F-Droid 或 Play Store 安装 OwnTracks 应用。
2. 进入手机设置 → 首选项 → 模式 → **HTTP**。
3. 设置 Webhook 地址为 `http://<host-tailscale-ip>:18793/owntracks`。
4. 在地图上点击任意位置以发送测试信号。

手机必须位于与接收端（同一局域网或通过 Tailscale 连接）相同的范围内。

### 3. 验证功能

```bash
curl http://localhost:18793/latest
# Should return JSON with lat, lon, acc, batt, etc.
```

## Places CLI 工具

该工具支持通过哈弗辛（Haversine）算法查询指定位置的距离。

```bash
# Add a place
node scripts/places.mjs add "Home" 41.3200 1.8900 home "Olivella"
node scripts/places.mjs add "Gym" 41.2229 1.7385 gym "Aqua Sport, Vilanova"

# Where am I? (reads OwnTracks latest + finds nearest named place)
node scripts/places.mjs where

# Find nearby places from arbitrary coordinates
node scripts/places.mjs nearest 41.22 1.74 5 500

# Search by name/category/notes
node scripts/places.mjs search "gym"

# List all
node scripts/places.mjs list
node scripts/places.mjs list gym

# Remove
node scripts/places.mjs remove "Old Place"
```

## 用户交互流程

- 当用户询问“我在哪里？”时：
  - 系统会从 `/latest` 获取当前位置信息。
- 如果用户指定了某个具体位置，系统会：
  1. 通过 Nominatim 或网络搜索获取该位置的详细信息。
  2. 使用 `node scripts/places.mjs` 命令将位置信息（经纬度、类别）添加到数据库中。

## 服务器端接口

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| POST | `/owntracks` | 发送位置数据（请求格式：`_type: "location"`） |
| GET | `/latest` | 获取用户最近的位置信息 |
| GET | `/history?limit=50` | 查看用户的历史位置记录 |
| GET | `/health` | 检查服务器运行状态 |

## 所需依赖库/软件

- Node.js 22 及更高版本
- `better-sqlite3`（用于处理位置数据）
- OwnTracks 应用程序（适用于 Android/iOS 平台）
- 确保手机与接收端之间有网络连接（推荐使用 Tailscale 作为网络中继）