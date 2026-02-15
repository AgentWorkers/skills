---
name: surfline
description: 从 Surfline 的公共端点获取冲浪预报和当前海况信息（无需登录）。这些功能可用于查询 Surfline 的各个冲浪地点的 ID，获取特定地点的预报/海况数据，以及汇总多个常用冲浪地点的信息。
---

# Surfline（公共接口，无需登录）

此技能使用 Surfline 的 **公共接口**（无需账号或 Cookie）。

## 快速入门

1) 查找某个冲浪点的 ID：

```bash
python3 scripts/surfline_search.py "Cardiff Reef"
python3 scripts/surfline_search.py "D Street"
```

2) 获取某个冲浪点的信息（默认输出文本和 JSON 格式的数据）：

```bash
python3 scripts/surfline_report.py <spotId>
# or only one format:
python3 scripts/surfline_report.py <spotId> --text
python3 scripts/surfline_report.py <spotId> --json
```

3) 收藏的冲浪点汇总（支持多个冲浪点）（默认输出文本和 JSON 格式的数据）：

请创建 `~/.config/surfline/favorites.json` 文件（参考 `references/favorites.json.example`）。

```bash
python3 scripts/surfline_favorites.py
```

## 注意事项

- 请适度使用请求接口，避免频繁发送大量请求（以免对服务器造成负担）。脚本中已实现了基本的缓存机制。
- 冲浪点的 ID 是稳定的，只需获取一次即可保存。
- 如果 Surfline 修改了接口或字段的名称，请更新 `scripts/surfline_client.py` 文件。