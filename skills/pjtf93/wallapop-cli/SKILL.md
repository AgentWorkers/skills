---
name: wallapop-cli
description: 使用 Wallapop CLI 来搜索列表、获取商品详情、查看用户资料以及列出分类。当用户请求 Wallapop 市场数据时，或者当你需要使用 Wallapop CLI 的命令和参数时，可以参考这些说明。
compatibility: Requires wallapop-cli installed (Node.js 18+), network access to api.wallapop.com, and optional WALLAPOP_ACCESS_TOKEN for non-search endpoints.
---

## 目的  
提供简洁、正确的命令，用于使用 wallapop-cli。  

## 使用场景  
- 用户询问如何从终端搜索 Wallapop 上的房源信息。  
- 用户需要通过 CLI 参数来过滤搜索结果（价格、位置、类别、数量限制）。  
- 用户需要查询房源或用户的信息。  
- 用户需要 JSON 格式的输出结果以便进行脚本编写。  

## 命令  
### 搜索房源  
```
wallapop search "<query>" [--lat <lat>] [--lng <lng>] [--min-price <n>] [--max-price <n>] [--category <id>] [--limit <n>]
```  
**注意：**  
- 如果省略了 `--lat` 或 `--lng` 参数，系统会使用配置的位置信息。  
- `--limit` 参数用于限制搜索结果的数量。  

### 查看房源详情  
```
wallapop item <item_id>
```  

### 查看用户资料  
```
wallapop user <user_id>
```  

### 查看房源类别  
```
wallapop categories
```  

### 输出格式（所有命令）  
添加全局参数 `--json` 可以使输出结果为 JSON 格式：  
```
wallapop --json search "laptop"
wallapop --json item abc123
```  

## 配置  
- 位置信息可以通过环境变量设置：  
  - `WALLAPOP_LAT`  
  - `WALLAPOP_LNG`  
- 非搜索功能的访问令牌（可选）：  
  - `WALLAPOP_ACCESS_TOKEN`  

## 输出格式要求  
- 搜索结果：包含房源 ID、标题、价格、距离以及发布用户信息的表格或 JSON 数组。  
- 房源详情：包含房源标题、描述、分类信息、发布用户信息的表格或 JSON 数据。  
- 用户资料：包含用户个人信息的表格或 JSON 数据。  
- 房源类别：包含类别 ID 和名称的表格或 JSON 列表。  

## 示例（使用占位符）  
```
wallapop search "camera" --min-price 50 --max-price 200
wallapop search "chair" --lat 40.0 --lng -3.0 --limit 5
wallapop item abc123
wallapop user user123
wallapop --json categories
```  

## 错误处理  
- 如果操作失败，程序会返回非零的退出码。  
- 在脚本中使用 `--json` 参数时，应通过检查退出码来处理错误。