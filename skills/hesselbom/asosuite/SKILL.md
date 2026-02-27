---
name: asosuite
description: 使用 ASO Suite CLI 进行应用商店优化（ASO），支持 iPhone、iPad、Mac、Apple TV、Apple Watch 和 VisionOS 平台。该工具可以帮助您查找具有流行度/难度数据的关键词，跟踪关键词在搜索结果中的排名变化，以及监控应用的评分、编辑推荐和图表展示情况。
homepage: https://www.asosuite.com/
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["asosuite"]},"install":[{"id":"npm","kind":"node","package":"asosuite","bins":["asosuite"],"label":"Install asosuite (npm)"}]}}
---
# ASO Suite CLI

使用 `asosuite` 可以在 iPhone、iPad、Mac、Apple TV、Apple Watch 和 VisionOS 应用程序上运行 ASO（应用商店优化）相关工作流程：发现具有流行度和难度数据的关键词，跟踪关键词在榜单中的排名变化，以及监控应用的评价、编辑推荐内容，并以机器可读的格式输出相关数据。

## 设置

安装：

```bash
npm install -g asosuite
asosuite help
```

登录：

```bash
asosuite login
```

## 优先使用 JSON 格式

为了便于解析数据，请在所有支持 JSON 格式的命令后始终添加 `--json` 参数。  
不支持 `--json` 参数的命令包括：`login`、`logout`。

## 默认参数

- `region=US`  
- `platform=iphone`  
- `period=30`（用于获取图表数据和应用评价数据）  
- 支持的平台：iPhone (`iphone`)、iPad (`ipad`)、Mac (`mac`)、Apple TV (`appletv`)、Apple Watch (`watch`)、VisionOS (`vision`)  

## 命令参考（所有命令）

- `asosuite login`  
- `asosuite logout`  
- `asosuite subscription [--json]`  
- `asosuite search-apps [--json] [--region <REGION>] [--platform <PLATFORM>] <query...>`  
- `asosuite list-apps [--json]`  
- `asosuite keywords [--json] [--region <REGION>] [--platform <PLATFORM>] [--app <APP_ID_OR_URL>] <keyword...>`  
- `asosuite track-app [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`  
- `asosuite untrack-app [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`  
- `asosuite plan-app [--json] --name <APP_NAME> [--id <PLANNED_APP_ID>] [--region <REGION>] [--platform <PLATFORM>]`  
- `asosuite unplan-app [--json] --id <PLANNED_APP_ID> [--region <REGION>] [--platform <PLATFORM>]`  
- `asosuite tracked-keywords list [--json] [--region <REGION>] [--platform <PLATFORM>] [--page <NUMBER>] [--sort <FIELD>] [--order <asc|desc>] --app <APP_ID_OR_URL_OR_PLANNED_ID>`  
- `asosuite tracked-keywords add [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> <keyword...>`  
- `asosuite tracked-keywords remove [--json] [--region <REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL_OR_PLANNED_ID> <keyword...>`  
- `asosuite related-apps list [--json] --app <APP_ID_OR_URL> [--platform <PLATFORM>]`  
- `asosuite related-apps add [--json] --app <APP_ID_OR_URL> --related <APP_ID_OR_URL> [--platform <PLATFORM>] [--region <REGION>]`  
- `asosuite related-apps remove [--json] --app <APP_ID_OR_URL> --related <APP_ID_OR_URL> [--platform <PLATFORM>]`  
- `asosuite events list [--json] [--app <APP_ID_OR_URL>]`  
- `asosuite events add [--json] --text <TEXT> [--date <YYYY-MM-DD>] [--app <APP_ID_OR_URL>]`  
- `asosuite events delete [--json] <EVENT_ID>`  
- `asosuite charts [--json] [--period <7|30|90>] [--region <REGION> | --regions <REGION,REGION>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`  
- `asosuite features [--json] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`  
- `asosuite ratings [--json] [--period <7|30|90>] [--platform <PLATFORM>] --app <APP_ID_OR_URL>`  

## 常用 ASO 命令（支持 JSON 格式）  

```bash
# Account info
asosuite subscription --json

# Discover apps
asosuite search-apps --json --region US --platform iphone "chat gpt"

# Tracked/planned apps
asosuite list-apps --json
asosuite track-app --json --app 6448311069 --platform iphone --region US
asosuite untrack-app --json --app 6448311069 --platform iphone --region US
asosuite plan-app --json --name "My Next App" --platform iphone --region US
asosuite unplan-app --json --id my-next-app --platform iphone --region US

# Keyword research + tracking
asosuite keywords --json --region US --platform iphone --app 6448311069 "step counter" "water tracker"
asosuite tracked-keywords list --json --app 6448311069 --platform iphone --region US --page 1 --sort relevance --order desc
asosuite tracked-keywords add --json --app 6448311069 --platform iphone --region US "step counter" "water tracker"
asosuite tracked-keywords remove --json --app 6448311069 --platform iphone --region US "step counter" "water tracker"

# Related apps / competitors
asosuite related-apps list --json --app 6448311069 --platform iphone
asosuite related-apps add --json --app 6448311069 --related 333903271 --platform iphone --region US
asosuite related-apps remove --json --app 6448311069 --related 333903271 --platform iphone

# Charts, featuring, ratings
asosuite charts --json --app 6448311069 --platform iphone --period 30
asosuite features --json --app 6448311069 --platform iphone
asosuite ratings --json --app 6448311069 --platform iphone --period 30

# Events
asosuite events list --json --app 6448311069
asosuite events add --json --app 6448311069 --text "Started ASO for 'keyword x'" --date 2026-02-25
asosuite events delete --json 123
```  

## 注意事项

- `tracked-keywords list` 每页最多返回 50 个关键词。  
- `tracked-keywords list` 的排序字段包括：`keyword`（关键词）、`relevance`（相关性）、`popularity`（流行度）、`difficulty`（难度）、`position`（排名）、`lastUpdate`（更新时间）。  
- 服务器限制：  
  - 每次请求最多返回 50 个关键词。  
  - `tracked-keywords add`/`tracked-keywords remove` 每次请求最多添加/删除 200 个关键词。