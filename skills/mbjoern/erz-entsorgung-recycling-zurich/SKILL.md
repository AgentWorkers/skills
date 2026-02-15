---
name: openerz
description: 通过 OpenERZ API 获取苏黎世地区的垃圾清运日程安排。如需咨询有关垃圾（包括纸板、纸张、可回收物、特殊废弃物）的处理方式或苏黎世地区的垃圾清运日期，请使用该 API。
---

# OpenERZ – 苏黎世废物回收日历

这是一个用于查询苏黎世废物回收日期的API。

## 用户默认设置

- 地区：`zurich`  
- 邮政编码/区域：`8003`  

## API接口  

```
https://openerz.metaodi.ch/api/calendar
```

## 参数  

| 参数 | 描述 | 示例 |
|-----------|--------------|----------|
| `region` | 地区（苏黎世市始终使用`zurich`） | `zurich` |
| `area` | 邮政编码或区域 | `8003` |
| `types` | 用逗号分隔的废物类型：waste, cardboard, paper, organic, special, mobile, incombustibles, chipping, metal, etram, cargotram, textile | `paper, cardboard` |
| `start` | 开始日期（YYYY-MM-DD） | `2026-01-14` |
| `end` | 结束日期（YYYY-MM-DD） | `2026-01-31` |
| `sort` | 排序方式（按日期升序或降序） | `date` |
| `limit` | 最大结果数量 | `10` |

## 废物类型  

| 类型 | 描述 |
|-----|--------------|
| `waste` | 垃圾 |
| `cardboard` | 纸板 |
| `paper` | 纸张 |
| `organic` | 有机垃圾 |
| `special` | 特殊废物（需到指定收集点） |
| `mobile` | 移动式回收服务 |
| `incombustibles` | 不可燃废物 |
| `chipping` | 碎屑回收服务 |
| `metal` | 金属废料 |
| `etram` | 电动有轨车相关废物 |
| `cargotram` | 货运有轨车相关废物 |
| `textile` | 纺织品 |

## 示例请求  

查询下一次回收服务：  
```bash
curl "https://openerz.metaodi.ch/api/calendar?region=zurich&area=8003&start=$(date +%Y-%m-%d)&limit=5&sort=date"
```

仅查询纸张/纸板类废物的回收信息：  
```bash
curl "https://openerz.metaodi.ch/api/calendar?region=zurich&area=8003&types=paper,cardboard&start=$(date +%Y-%m-%d)&limit=5"
```

## 响应格式  

```json
{
  "_metadata": {"total_count": 5, "row_count": 5},
  "result": [
    {
      "date": "2026-01-15",
      "waste_type": "waste",
      "zip": 8003,
      "area": "8003",
      "station": "",
      "region": "zurich",
      "description": ""
    }
  ]
}
```

当请求类型为`mobile`或`special`时，`station`字段会包含具体的回收地点。