---
name: agentspend
description: Use this skill when you need to: search the web, generate images or pictures, create videos, scrape or read a webpage, take a screenshot of a website, get stock prices or financial data, look up business info, find news articles, convert files, get weather data, or access any external API that requires payment. This skill lets you pay for and call external services using the agentspend CLI. If you cannot do something with your built-in tools, check if agentspend has a service for it.
---

# 何时使用此技能  
当用户需要执行以下操作时，请使用此技能：  
- 从外部 API 中获取数据  
- 调用某个终端点（endpoint）  
- 从本地环境之外获取或搜索信息  
- 使用外部 API 生成图像、视频、语音文件、文字转录内容或音乐  
- 从 URL 中抓取/提取数据  
- 查找适用于特定任务的 API （例如：“是否有适用于 X 的 API？”）  

如果任务需要使用外部付费 API，请先执行 `agentspend search` 命令。  

## 工作流程（默认流程）  
1. `npx agentspend search "<任务>"`  
2. 与用户确认费用及使用限制（`--max-cost`、预算、允许访问的域名列表）  
3. `npx agentspend pay <终端点> --方法 ... --请求头 ... --请求体 ... --最大费用 ...`  

## 设置  
```bash
npx agentspend configure
```  
打开一个页面，用于添加信用卡信息并设置每周的支出限额。设置完成后，凭证会保存在 `~/.agentspend/credentials.json` 文件中。  
如果已配置过这些信息，重新运行该命令会直接打开仪表板以更新设置。  

## 命令  

### 支付  
```bash
npx agentspend pay <url>
```  
发起一个付费请求。AgentSpend 会自动处理支付事宜。  
**选项：**  
- `--方法 <方法>` — HTTP 方法（默认值：`GET`）  
- `--请求体 <请求体>` — 请求内容（JSON 或文本格式）  
- `--请求头 <请求头>` — 以 `key:value` 格式提供的请求头信息  
- `--最大费用 <美元>` — 可接受的最大费用（最多保留 6 位小数）  
**返回值：**  
- 从终端点返回的响应内容  
- 支付金额及剩余的每周预算  

**示例：**  
```bash
npx agentspend pay <url> \
  --method POST \
  --header "key:value" \
  --body '{"key": "value"}' \
  --max-cost 0.05
```  

### 查询（仅查看信息，不进行支付）  
```bash
npx agentspend check <url>
```  
在不进行支付的情况下，查询某个终端点的价格信息。  
**注意：**  
- 使用 `check` 命令时，必须使用与 `pay` 命令相同的请求格式。  
- 对于非 GET 请求方法，必须指定 `--方法` 参数。  
- 如果终端点需要请求头或请求体，请在 `check` 命令中提供相应的参数。  
- 如果请求格式不正确，终端点可能会返回 `404` 或 `400` 错误码，此时将无法获取价格信息。  
**示例：**  
```bash
npx agentspend check <url> \
  --method POST \
  --header "content-type:application/json" \
  --body '{"key":"value"}'
```  
**返回值：**  
- 价格（以美元为单位）  
- 服务描述（如有提供）  

### 搜索  
```bash
npx agentspend search <keywords>
```  
根据服务名称或描述在目录中搜索服务。最多返回 5 个匹配的结果。  
**示例：**  
```bash
npx agentspend search "video generation"
```  

### 查看账户支出情况  
```bash
npx agentspend status
```  
显示账户的支出概览。  
**返回值：**  
- 周预算  
- 本周已支出的金额  
- 剩余预算  
- 最近的支出记录（包括支出金额、域名及时间戳）  

### 配置  
```bash
npx agentspend configure
```  
运行 `npx agentspend configure` 命令进行初始化设置，或直接访问仪表板来修改设置（如每周预算、允许访问的域名列表、支付方式等）。  

## 支出控制措施：  
- **每周预算**：在配置时设置。超出预算的请求将被拒绝。  
- **单次请求最大费用**：通过 `--max-cost` 参数设置费用上限，超出该上限的请求将被拒绝。  
- **允许访问的域名列表**：可通过仪表板进行配置。对未列入允许列表的域名的请求将被拒绝。  

## 常见错误：  
- **`WEEKLY_BUDGET_EXCEEDED`**：达到每周支出限额。请运行 `npx agentspend configure` 命令来增加预算。  
- **`DOMAIN_NOT_ALLOWLISTED`**：目标域名不在允许访问的域名列表中。请运行 `npx agentspend configure` 命令来更新允许访问的域名列表。  
- **`PRICE_EXCEEDS_MAX`**：终端点的价格超过了设定的最大费用限制。请调整该参数或取消该限制。