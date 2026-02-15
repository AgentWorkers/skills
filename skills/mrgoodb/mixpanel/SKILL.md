---
name: mixpanel
description: 通过 Mixpanel API 追踪事件并分析用户行为。查询分析数据、管理用户资料以及导出数据。
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["MIXPANEL_TOKEN","MIXPANEL_API_SECRET"]}}}
---

# Mixpanel

产品分析工具。

## 环境配置

```bash
export MIXPANEL_TOKEN="xxxxxxxxxx"          # Project token (tracking)
export MIXPANEL_API_SECRET="xxxxxxxxxx"     # API secret (querying)
export MIXPANEL_PROJECT_ID="123456"
```

## 跟踪事件

```bash
curl "https://api.mixpanel.com/track" \
  -d "data=$(echo -n '{"event":"Button Clicked","properties":{"distinct_id":"user123","token":"'$MIXPANEL_TOKEN'"}}' | base64)"
```

## 跟踪事件（JSON格式）

```bash
curl -X POST "https://api.mixpanel.com/import?strict=1" \
  -u "$MIXPANEL_API_SECRET:" \
  -H "Content-Type: application/json" \
  -d '[{"event":"Purchase","properties":{"distinct_id":"user123","time":'$(date +%s)',"price":29.99}}]'
```

## 查询事件（JQL语法）

```bash
curl "https://mixpanel.com/api/2.0/jql" \
  -u "$MIXPANEL_API_SECRET:" \
  -d 'script=function main(){return Events({from_date:"2024-01-01",to_date:"2024-01-31"}).groupBy(["name"],mixpanel.reducer.count())}'
```

## 获取用户资料

```bash
curl "https://mixpanel.com/api/2.0/engage?distinct_id=user123" \
  -u "$MIXPANEL_API_SECRET:"
```

## 更新用户资料

```bash
curl "https://api.mixpanel.com/engage#profile-set" \
  -d "data=$(echo -n '{"$token":"'$MIXPANEL_TOKEN'","$distinct_id":"user123","$set":{"plan":"premium"}}' | base64)"
```

## 链接：
- 仪表盘：https://mixpanel.com
- 文档：https://developer.mixpanel.com