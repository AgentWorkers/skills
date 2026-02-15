---
name: recgov-availability
description: 请访问recreation.gov网站，查询联邦露营地（包括国家公园、美国林业局管理的露营地以及土地管理局管理的露营地）的可用性。查询时需要提供露营地的ID，这些ID可以从ridb-search或recreation.gov网站获取。
---

# recreation.gov 可用性检查工具

通过 recreation.gov 查询联邦营地的空位情况。

## 快速入门

```bash
cd /Users/doop/moltbot/skills/recgov-availability

# Check availability (campground ID from URL or ridb-search)
python3 scripts/check.py -c 233965 --start 2026-07-10 --nights 2

# Multiple campgrounds
python3 scripts/check.py -c 233965 233900 --start 2026-07-10 --nights 2

# Filter to tent sites, JSON output
python3 scripts/check.py -c 233965 --start 2026-07-10 --nights 2 --type tent --json
```

## 查找营地ID

从网址 `recreation.gov/camping/campgrounds/233965` 可以获取营地ID `233965`。

或者使用 ridb-search 工具：
```bash
python3 ../ridb-search/scripts/search.py -l "Newport, OR" --camping-only
```

## 命令选项

| 选项          | 描述                                      |
|----------------|-------------------------------------------|
| `-c, --campground`    | 要检查的营地ID（必需）                          |
| `-s, --start`     | 开始日期（格式：YYYY-MM-DD）                        |
| `-n, --nights`     | 所需连续住宿天数（默认：1天）                      |
| `-t, --type`     | 营地类型：帐篷、房车、标准型、小屋、团体型                |
| `--electric`    | 仅限有电设施的营地                      |
| `--nonelectric` | 仅限无电设施的营地                      |
| `--include-group`   | 包括团体型营地                          |
| `--pets`       | 仅限允许携带宠物的营地                      |
| `--shade`       | 仅限有遮阳设施的营地                      |
| `--fire-pit`     | 有火坑的营地                          |
| `--vehicle-length N` | 车辆最小长度（单位：英尺）                      |
| `--show-sites`    | 显示各个营地的详细信息                        |
| `--json`       | 输出结果为JSON格式                         |

## 状态说明

| 状态            | 含义                                      |
|----------------|-------------------------------------------|
| ✅ 可预订        | 可立即预订                              |
| ❌ 已预订        | 营位已被他人预订                          |
| ⏳ 尚未开放      | 预订服务尚未启动                          |
| 🚗 先到先得      | 按先到先得原则分配（不支持预订）                    |

## 覆盖范围

- 国家公园管理局（National Park Service）的营地 |
- 美国农业部森林服务局（USDA Forest Service）的营地 |
- 美国土地管理局（BLM）管理的休闲设施 |
- 美国陆军工程兵团（Army Corps of Engineers）管理的区域 |

如需查询州立公园的营地信息，请使用 `reserveamerica` 工具。

## 注意事项

- 无需API密钥 |
- 需要Python 3.8及以上版本（仅使用标准库） |
- 使用某些选项（如 `--pets`, `--shade`）时可能需要额外的API请求 |
- 预订窗口通常为6个月前开始

更多详细信息请参阅 README.md 文件。