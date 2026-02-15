---
name: gotrain
description: MTA系统列车发车信息（纽约市地铁、长岛铁路公司LIRR、Metro-North）。当用户需要查询MTA交通系统的列车时刻、时刻表或服务提醒时，请使用该功能。该服务涵盖纽约大都会地区的MTA地铁、LIRR和Metro-North线路。
metadata: {"clawdbot":{"requires":{"bins":["gotrain"]},"install":[{"id":"node","kind":"node","package":"gotrain-cli","bins":["gotrain"],"label":"Install gotrain CLI (npm)"}]}}
---

# gotrain

这是一个用于查询纽约市公共交通（MTA地铁、LIRR、Metro-North）出发时间的命令行工具（CLI）。

## 安装

```bash
npm install -g gotrain-cli
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `gotrain stations [query]` | 列出/搜索车站 |
| `gotrain departures <station-id>` | 显示指定车站的出发时间 |
| `gotrain alerts` | 查看当前的服务提醒 |
| `gotrain fav <id>` | 将车站添加为收藏 |
| `gotrain favs` | 查看收藏的车站列表 |

## 常见车站ID

- `MNR-149` - 新黑文（New Haven） |
- `MNR-151` - 新黑文-州街（New Haven-State St） |
- `MNR-1` - 格兰德中央站（Grand Central） |
- `MNR-203` - 宾州车站（Penn Station, MNR） |
- `LIRR-349` | 格兰德中央站（Grand Central） |
- `SUBWAY-631` | 格兰德中央站-42街（Grand Central-42 St） |

## 示例

```bash
# Search for Penn Station
gotrain stations penn

# New Haven to Grand Central departures
gotrain departures MNR-149

# Check service alerts
gotrain alerts

# Add favorite station
gotrain fav MNR-149
```

## 来源

https://github.com/gumadeiras/gotrain-cli