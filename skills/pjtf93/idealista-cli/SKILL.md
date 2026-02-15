---
name: idealista-cli
description: 使用 `idealista-cli` 根据位置（城市、城镇、地区、街道）搜索 Idealista 上的房源信息，并获取房源详情。当用户需要 Idealista 市场数据或 `idealista-cli` 的命令/参数时，可参考本指南。
compatibility: Requires idealista-cli installed (Node.js 18+), network access to app.idealista.com.
license: MIT
metadata:
  author: pjtf93
  version: "0.1.0"
---

## 目的  
搜索 Idealista 上的房源信息并获取房源详情。  

## 使用场景  
- 用户希望按城市/城镇/地区/街道进行搜索。  
- 用户需要通过房源 ID 获取房源详情。  
- 用户希望以 JSON 格式获取数据以便进行脚本编写。  

## 命令  
### 地点查询  
```
idealista locations "<query>" --operation <sale|rent|transfer> --property-type <homes|rooms|offices|garages|land>
```  

### 搜索房源  
```
idealista search "<query>" --operation <sale|rent|transfer> --property-type <homes|rooms|offices|garages|land>
```  

可选过滤条件：  
- `--page <n>`  
- `--limit <n>`  
- `--min-price <金额>` / `--max-price <金额>`  
- `--min-size <平方米>` / `--max-size <平方米>`  
- `--bedrooms <卧室数量>`  
- `--order <排序字段>` / `--sort <排序方式>`  
- `--location-id <ID>` （用于跳过特定地点的查询）  

### 房源详情  
```
idealista listing <adId>
```  

### JSON 输出  
在任意命令后添加 `--json` 选项即可获取 JSON 格式的数据：  
```
idealista search "madrid" --json
idealista listing 123456789 --json
```  

## 配置  
默认值来自 APK 文件；如有需要，可通过环境变量进行覆盖：  
- `IDEALISTA_API_KEY`  
- `IDEALISTA_SIGNATURE_SECRET`  
- `IDEALISTA_OAUTH_CONSUMER_KEY`  
- `IDEALISTA_OAUTH_CONSUMER_SECRET`  
- `IDEALISTA_DEVICE_ID`  
- `IDEALISTA_APP_VERSION`  
- `IDEALISTA_BASE_URL`  
- `IDEALISTA_USER_AGENT`  
- `IDEALISTA_DNT`  

## 输出格式  
- 地点信息：以表格或 JSON 格式显示 `locationId`、名称和类型。  
- 搜索结果：以表格或 JSON 格式显示房源 ID、价格、卧室数量、面积、地址和位置信息。  
- 房源详情：以表格或 JSON 格式显示价格、卧室数量、面积、地址、网址和房源描述。  

## 示例  
```
idealista locations "madrid" --operation sale --property-type homes
idealista search "madrid" --operation rent --property-type homes --limit 20
idealista listing 123456789
```  

## 错误处理  
- 如果操作失败，程序将返回非零的退出代码。  
- 在进行脚本编写时，请使用 `--json` 选项并检查退出代码以判断操作是否成功。