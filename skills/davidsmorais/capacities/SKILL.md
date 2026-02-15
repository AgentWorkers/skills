---
name: capacities
description: 管理容量信息、每日记录以及网页链接。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "env": ["CAPACITIES_API_TOKEN"] },
        "primaryEnv": "CAPACITIES_API_TOKEN",
      },
  }
---

# Capacities 技能

使用此技能与您的 Capacities “第二大脑” 进行交互。

## 需求条件
- `CAPACITIES_API_TOKEN`：从桌面应用程序的“设置” > “Capacities API” 中获取。
- `CAPACITIES_SPACE_ID`：（可选）如果未提供，则会使用第一个可用的空间。

## 使用方法

### 每日笔记
要将想法、任务或笔记添加到今天的每日笔记中：
```
curl -X POST https://api.capacities.io/save-to-daily-note -H "Authorization: Bearer $CAPACITIES_API_TOKEN" -H "Content-Type: application/json" -d '{"spaceId": "$CAPACITIES_SPACE_ID", "mdText": "您的笔记内容"}'
```

### 网页链接
要将网页链接保存到您的空间中：
```
curl -X POST https://api.capacities.io/save-weblink -H "Authorization: Bearer $CAPACITIES_API_TOKEN" -H "Content-Type: application/json" -d '{"spaceId": "$CAPACITIES_SPACE_ID", "url": "https://example.com"}'
```

### 搜索/查询
要查找对象的 ID：
```
curl -X POST https://api.capacities.io/lookup -H "Authorization: Bearer $CAPACITIES_API_TOKEN" -H "Content-Type: application/json" -d '{"spaceId": "$CAPACITIES_SPACE_ID", "searchTerm": "我的笔记"}'
```

### 空间信息
要获取所有对象类型和结构：
```
curl -X GET "https://api.capacities.io/space-info?spaceid=$CAPACITIES_SPACE_ID" -H "Authorization: Bearer $CAPACITIES_API_TOKEN"
```