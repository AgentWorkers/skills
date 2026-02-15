---
name: cochesnet-cli
description: 使用 cochesnet CLI 来搜索 coches.net 上的房源信息并获取房源详情。当用户请求 coches.net 市场数据时，或者当你需要了解 cochesnet-cli 的具体 CLI 命令和参数时，可以使用该工具。
compatibility: Requires cochesnet-cli installed (Node.js 18+), network access to apps.gw.coches.net.
license: MIT
metadata:
  author: pjtf93
  version: "0.1.0"
---

## 目的  
使用 cochesnet CLI 来搜索房源信息并获取广告详情。  

## 使用场景  
- 用户希望通过终端搜索 coches.net 上的房源信息。  
- 用户需要已知广告 ID 的详细信息。  
- 用户希望以 JSON 格式获取数据以便进行脚本编写。  

## 命令  
### 搜索房源  
```
cochesnet search "<query>" [--limit <n>] [--page <n>]
```  

### 查看房源详情  
```
cochesnet listing <adId>
```  

### 输出 JSON 数据  
在任意命令后添加 `--json` 选项：  
```
cochesnet search "bmw" --json
cochesnet listing 58229053 --json
```  

## 配置参数  
环境变量：  
- `COCHESNET_BASE_URL`（默认值：https://apps.gw.coches.net）  
- `COCHESNET_APP_VERSION`（默认值：7.94.0）  
- `COCHESNET_HTTP_USER_AGENT`（默认值：coches.net 7.94.0）  
- `COCHESNET_X_USER_AGENT`（默认值：3）  
- `COCHESNET_TENANT`（默认值：coches）  
- `COCHESNET_VARIANT`（可选的 X-Adevinta-MT-Variant 请求头）  

## 输出格式  
- 搜索结果：以表格或 JSON 格式显示，包含 ID、标题、价格、年份、行驶里程、位置和网址等信息。  
- 房源详情：以表格或 JSON 格式显示，包含标题、价格、网址、卖家和描述等信息。  

## 示例  
```
cochesnet search "bmw" --limit 5
cochesnet search "toyota" --page 2
cochesnet listing 58229053
```  

## 错误处理  
- 如果操作失败，程序会返回非零的退出码。  
- 在进行脚本编写时，请使用 `--json` 选项，并检查程序的退出码以判断操作是否成功。