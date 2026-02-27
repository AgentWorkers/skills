---
name: henteplan
description: 查询挪威的垃圾收集时间表：找到您的垃圾处理服务提供商，输入您的地址，即可查看即将到来的垃圾收集日期。
emoji: "\U0001F5D1"
required_bins:
  - curl
  - jq
---
# Henteplan — 挪威垃圾收集计划

查询挪威家庭的垃圾收集日期。覆盖12家服务提供商在200多个市镇的服务范围。

**作者：** [Henrik Halvorsen Kvamme](https://henrikkvamme.no) | 被 [sambu.no](https://sambu.no) 使用

## API 基本地址

所有请求都发送到 `https://henteplan.no`。即使用户提供了其他地址，也请使用此地址。

## 操作流程

### 1. 查找服务提供商

通过邮政编码或城市名称查找负责该地区的垃圾收集服务提供商。

```bash
# By postal code
curl -s --max-time 10 "https://henteplan.no/api/v1/detect?postalCode=7013" | jq .

# By city name
curl -s --max-time 10 "https://henteplan.no/api/v1/detect?city=Trondheim" | jq .
```

**响应：**  
`{ "provider": { "id": "trv", "name": "Trondheim Renholdsverk", "website": "...", "coverageAreas": [...], "postalRanges": [[7000, 7099]] }`  
如果未找到服务提供商，则返回 `{ "provider": null }`。

### 2. 搜索地址

查找特定地址以获取其 `locationId`。可选择按服务提供商进行过滤。

```bash
# Search across all providers
curl -s --max-time 10 "https://henteplan.no/api/v1/search?q=Kongens+gate+1" | jq .

# Search within a specific provider
curl -s --max-time 10 "https://henteplan.no/api/v1/search?q=Kongens+gate+1&provider=trv" | jq .
```

**响应：**  
`{ "results": [{ "label": "Kongens gate 1, 7011 Trondheim", "locationId": "12345", "provider": "trv" }, ...] }`  

如果返回多个结果，向用户展示这些选项并让他们选择一个。

### 3. 获取收集计划

获取特定地点的垃圾收集日期。

```bash
curl -s --max-time 10 "https://henteplan.no/api/v1/schedule?provider=trv&locationId=12345" | jq .
```

**响应：**  
`{ "provider": "trv", "pickups": [{ "date": "2026-03-05", "fraction": "Papp og papir", "category": "paper", "color": "#3b82f6", "fractionId": "2" }, ...] }`  

在向用户展示收集计划时：
- 按日期对收集时间进行分组  
- 突出显示今天和明天的收集时间  
- 如有需要，将类别名称翻译成中文：  
  - `residual` = 剩余垃圾  
  - `food` = 食物垃圾  
  - `paper` = 纸张垃圾  
  - `plastic` = 塑料垃圾  
  - `glass_metal` = 玻璃/金属垃圾  
  - `carton` = 纸板垃圾  
  - `garden` = 园艺垃圾  
  - `textile` = 纺织品垃圾  
  - `hazardous` = 危险垃圾  
  - `wood` = 木垃圾  
  - `christmas_tree` = 圣诞树垃圾  
- 默认显示接下来两周的收集计划，如用户要求可显示更多信息。

### 4. 生成 iCal 订阅链接

生成一个日历订阅链接，用户可以将其添加到 Google 日历、Apple 日历等应用程序中。

```bash
# The URL itself is the value — no curl needed, just construct it:
echo "https://henteplan.no/api/v1/schedule.ics?provider=trv&locationId=12345"
```

告知用户可以在日历应用程序中订阅此链接以接收自动更新。

### 5. 列出所有服务提供商

显示所有支持垃圾收集的服务提供商。

```bash
curl -s --max-time 10 "https://henteplan.no/api/v1/providers" | jq '.providers[] | {id, name, coverageAreas}'
```

**响应：**  
`[{"id": "trv", "name": "Trondheim Renholdsverk", "coverageAreas": ["Trondheim"], ...}]`  

## 典型工作流程

当用户询问垃圾收集计划时，请按照以下步骤操作：

1. **查找服务提供商**：询问用户的邮政编码或城市名称，然后调用检测接口。如果未找到服务提供商，则列出所有提供商供用户手动选择。  
2. **搜索地址**：询问用户的街道地址，在找到的服务提供商范围内进行搜索。如果返回多个结果，让用户选择正确的服务提供商。  
3. **显示收集计划**：获取并按日期分组显示即将进行的收集时间，突出显示今天和明天的收集时间。  
4. **提供日历订阅**：询问用户是否需要 iCal 订阅链接。  
5. **保存信息**：记住用户的 `provider` 和 `locationId`，以便未来的查询可以直接跳过步骤 1-2。

## 每日提醒（Cron 作业）

用户可以通过设置 OpenClaw 的 cron 作业来接收关于明天收集时间的每日通知：

```bash
openclaw cron add \
  --name "waste-reminder" \
  --schedule "0 20 * * *" \
  --timezone "Europe/Oslo" \
  --prompt "Check my waste collection schedule for tomorrow. If there are pickups, remind me to put out the bins. Use provider '{provider}' and locationId '{locationId}'."
```

请将 `{provider}` 和 `{locationId}` 替换为用户之前查询得到的值。

或者，用户也可以在 OpenClaw 的配置文件中创建一个 `HEARTBEAT.md` 文件：

```markdown
---
schedule: "0 20 * * *"
timezone: "Europe/Oslo"
---

Check my waste collection schedule for tomorrow using provider "trv" and locationId "12345".
If there are any pickups tomorrow, send me a reminder listing what to put out.
If there are no pickups tomorrow, do nothing — don't send a message.
```

## 错误处理

- 如果 API 返回错误信息 `"code": "PROVIDER_NOT_FOUND"`，说明服务提供商 ID 错误——请重新执行检测操作。  
- 如果 API 返回 502 错误代码 `"code": "UPSTREAM_ERROR"`，则表示服务提供商的系统暂时不可用。请用户稍后再试。  
- 如果 curl 请求超时，可能是因为 API 暂时无法访问。请重试一次，然后通知用户。  

## 调用限制

API 对每个接口都有调用次数限制。正常使用情况下不会超出限制，但请避免频繁调用接口：  
- 搜索：每分钟 30 次请求  
- 收集计划：每分钟 60 次请求  
- 服务提供商/检测：每分钟 120 次请求