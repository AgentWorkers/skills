---
name: goplaces
description: 通过 `goplaces` CLI 查询 Google Places API，支持文本搜索、获取地点详情、解析地点信息以及查看评论。该工具既可用于方便用户查找地点信息，也可用于脚本中获取 JSON 格式的地点数据。
homepage: https://github.com/steipete/goplaces
metadata: {"clawdbot":{"emoji":"📍","requires":{"bins":["goplaces"],"env":["GOOGLE_PLACES_API_KEY"]},"primaryEnv":"GOOGLE_PLACES_API_KEY","install":[{"id":"brew","kind":"brew","formula":"steipete/tap/goplaces","bins":["goplaces"],"label":"Install goplaces (brew)"}]}}
---

# goplaces

这是一个用于与现代 Google Places API 进行交互的命令行工具（CLI）。默认输出为人类可读的格式，使用 `--json` 参数时可以获取 JSON 格式的输出，适用于脚本编写。

**安装方法：**
- 使用 Homebrew：`brew install steipete/tap/goplaces`

**配置参数：**
- 必需参数：`GOOGLE_PLACES_API_KEY`（用于访问 Google Places API）。
- 可选参数：`GOOGLE_PLACES_BASE_URL`（用于测试或代理请求）。

**常用命令：**
- **搜索**：`goplaces search "coffee" --open-now --min-rating 4 --limit 5`  
  （搜索咖啡店，要求评分至少为 4 分，显示前 5 条结果。）
- **定位**：`goplaces search "pizza" --lat 40.8 --lng -73.9 --radius-m 3000`  
  （搜索位于特定地理位置（纬度 40.8、经度 -73.9、半径 3000 米）的披萨店。）
- **分页**：`goplaces search "pizza" --page-token "NEXT_PAGE_TOKEN"`  
  （分页查询披萨店结果，使用指定的分页令牌。）
- **查询详情**：`goplaces details <place_id> --reviews`  
  （查询指定地点的详细信息及评论。）
- **获取 JSON 数据**：`goplaces search "sushi" --json`  
  （以 JSON 格式获取搜索结果。）

**其他注意事项：**
- `--no-color` 或 `NO_COLOR` 选项可禁用 ANSI 颜色显示。
- **价格等级**：0 到 4（0 表示免费，4 表示非常昂贵）。
- `--type` 参数仅接受一个值，用于过滤搜索结果类型。