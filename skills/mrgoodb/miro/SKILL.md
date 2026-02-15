---
name: miro
description: 通过 Miro API 管理 Miro 平板上的白板、便签和形状元素。实现程序化地创建协作式白板。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["MIRO_ACCESS_TOKEN"]}}}
---

# Miro

这是一个用于团队协作的白板平台。

## 环境配置

```bash
export MIRO_ACCESS_TOKEN="xxxxxxxxxx"
```

## 列出所有白板

```bash
curl "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## 创建新白板

```bash
curl -X POST "https://api.miro.com/v2/boards" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Project Planning", "description": "Sprint planning board"}'
```

## 查看白板信息

```bash
curl "https://api.miro.com/v2/boards/{board_id}" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## 创建便签

```bash
curl -X POST "https://api.miro.com/v2/boards/{board_id}/sticky_notes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"content": "New idea!", "shape": "square"},
    "position": {"x": 0, "y": 0},
    "style": {"fillColor": "yellow"}
  }'
```

## 绘制形状

```bash
curl -X POST "https://api.miro.com/v2/boards/{board_id}/shapes" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"shape": "rectangle", "content": "Task 1"},
    "position": {"x": 100, "y": 100},
    "geometry": {"width": 200, "height": 100}
  }'
```

## 查看白板上的所有内容

```bash
curl "https://api.miro.com/v2/boards/{board_id}/items" \
  -H "Authorization: Bearer $MIRO_ACCESS_TOKEN"
```

## 链接：
- 仪表盘：https://miro.com/app/dashboard/
- 文档：https://developers.miro.com/reference/api-reference