---
name: whatisxlistening-to
description: 查询 Last.fm 的收听数据，显示当前正在播放的歌曲，将收听记录同步到本地数据库，并部署一个个性化的“当前正在播放”网页仪表板。当用户询问当前正在播放的音乐、收听统计信息或希望设置 Last.fm 仪表板时，可以使用该功能。
---

# whatisxlistening.to

这是一个结合了Last.fm命令行界面（CLI）与实时“当前正在播放”音乐信息的网页仪表板的工具。

**在线演示**: https://whatisbenlistening.to

## 快速入门

### 命令行界面 (CLI)

```bash
# 1. Initialize config
./lastfm init
# Edit ~/.config/lastfm/config.json with your API key

# 2. Test
./lastfm now
./lastfm stats
./lastfm recent
```

### 仪表板

```bash
# Docker
docker run -d -p 8765:8765 \
  -e LASTFM_API_KEY=your_key \
  -e LASTFM_USERNAME=your_user \
  -e TZ=America/Los_Angeles \
  ghcr.io/poiley/whatisxlistening.to:latest

# → http://localhost:8765
```

## 命令行界面 (CLI) 命令

| 命令 | 描述 |
|---------|-------------|
| `lastfm init` | 创建配置文件模板 |
| `lastfm now` | 显示当前或最近播放的歌曲 |
| `lastfm stats` | 显示收听统计信息 |
| `lastfm recent [N]` | 显示最近播放的N首歌曲（默认为10首） |
| `lastfm backfill` | 将完整的收听历史数据下载到本地数据库 |
| `lastfm sync` | 同步新的收听记录（增量方式） |
| `lastfm search <查询>` | 根据艺术家、歌曲或专辑在本地数据库中搜索 |
| `lastfm db` | 显示本地数据库的统计信息 |

## 设置

### 1. 获取Last.fm API密钥

1. 访问 https://www.last.fm/api/account/create
2. 创建一个应用程序（任意名称）
3. 复制您的API密钥

### 2. 创建配置文件

```bash
./lastfm init
# Then edit ~/.config/lastfm/config.json:
```

```json
{
  "api_key": "YOUR_API_KEY",
  "username": "YOUR_LASTFM_USERNAME"
}
```

## Clawdbot 使用说明

| 用户输入 | 执行操作 |
|-----------|--------|
| “我正在听什么？” | `lastfm now` |
| “我的收听统计” | `lastfm stats` |
| “我最近听了什么？” | `lastfm recent` |
| “搜索Radiohead” | `lastfm search "Radiohead"` |

---

## 仪表板部署

### Docker

请参阅 `k8s/` 目录和 `README.md` 以获取使用Docker进行部署的完整指南。

```bash
kubectl create namespace listening-dashboard
kubectl create secret generic lastfm-credentials \
  -n listening-dashboard \
  --from-literal=api_key=YOUR_KEY \
  --from-literal=username=YOUR_USER
kubectl apply -k k8s/
```

## 环境变量

| 变量 | 是否必填 | 描述 |
|----------|----------|-------------|
| `LASTFM_API_KEY` | ✅ | Last.fm API密钥 |
| `LASTFM_USERNAME` | ✅ | Last.fm用户名 |
| `DISPLAY_NAME` | ❌ | 仪表板标题中的显示名称（默认为用户名） |
| `TZ` | ❌ | “今日”统计数据的时区（例如：`America/Los_Angeles`） |
| `PORT` | ❌ | 服务器端口（默认：8765） |

## API接口

| 接口 | 描述 |
|----------|-------------|
| `GET /` | 当前正在播放的歌曲信息 |
| `GET /history` | 收听历史记录页面 |
| `GET /healthz` | 系统健康检查 |
| `GET /api/config` | 返回用户信息（`username, display_name`） |
| `GET /api/now` | 当前或最近播放的歌曲 |
| `GET /api/stats` | 收听统计信息（总计、艺术家、今日收听量等） |
| `GET /api/recent?limit=N&page=N` | 带有专辑封面的最近播放歌曲列表 |

## 相关文件

```
whatisxlistening.to/
├── SKILL.md              # Clawdbot skill config
├── lastfm                # CLI symlink
├── lastfm_cli.py         # CLI source
├── config.example.json   # Config template
├── server.py             # Dashboard server
├── schema.sql            # SQLite schema
├── Dockerfile
├── README.md
├── web/
│   ├── index.html        # Now playing page
│   └── history.html      # History browser
├── k8s/                  # Kubernetes manifests
└── tests/                # 100% coverage
```

## 许可证

MIT许可证