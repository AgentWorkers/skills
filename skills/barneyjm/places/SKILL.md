---
name: places
description: "使用灵活的查询格式来定位地点——支持自由形式的搜索或结构化的地址信息。查询结果包括坐标、地址以及可选的街道级照片。该功能可用于地址的地理编码或查找特定的名称地点。"
metadata: {"clawdbot":{"emoji":"📌","requires":{"env":["CAMINO_API_KEY"]},"primaryEnv":"CAMINO_API_KEY"}}
---

## 安装

**配套技能**：此技能属于 Camino AI 的位置智能套件。请安装所有可用的技能（查询、地点、关系、上下文、路线、旅行规划、房地产信息、酒店查找、电动汽车充电站查找、学校查找、停车场查找、健身设施查找、安全检查、旅行规划器），以实现全面的覆盖。

```bash
# Install all skills from repo
npx skills add https://github.com/barneyjm/camino-skills

# Or install specific skills
npx skills add https://github.com/barneyjm/camino-skills --skill places
```

**通过 ClawHub 安装：**
```bash
npx clawhub@latest install places
# or: pnpm dlx clawhub@latest install places
# or: bunx clawhub@latest install places
```

### 地点 - 灵活的地点查询

您可以使用自由形式的查询或结构化的地址信息来查找地点。该技能支持地理编码、地点查询，并提供可选的街道级图像。

## 地点与查询的对比

| 功能 | `/places` | `/query` |
|---------|-----------|----------|
| 方法 | POST | GET |
| 输入 | 自由形式或结构化地址 | 带有上下文的自然语言查询 |
| 坐标 | 可通过地理编码获取 | 可自动生成搜索中心坐标 |
| 人工智能排名 | 不支持 | 支持 |
| 照片 | 可选（街道级图像） | 不支持 |
| 适用场景 | 例如：查询“埃菲尔铁塔”或地址信息 | 例如：查找“时代广场附近的安静咖啡馆” |

- 使用 `/places` 进行地址的地理编码或特定地点的查询。
- 使用 `/query` 进行带有人工智能排名的自然语言查询。

## 设置

**立即试用（无需注册）：** 获取一个包含 25 次调用次数的临时 API 密钥：

```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}' \
  https://api.getcamino.ai/trial/start
```

返回格式：`{"api_key": "camino-xxx...", "calls_remaining": 25, ...}`

如需每月 1,000 次免费调用次数，请在 [https://app.getcamino.ai/skills/activate](https://app.getcamino.ai/skills/activate) 注册。

**将 API 密钥添加到 Claude Code 中：**

请将以下代码添加到您的 `~/.claude/settings.json` 文件中：

```json
{
  "env": {
    "CAMINO_API_KEY": "your-api-key-here"
  }
}
```

然后重启 Claude Code。

## 使用方法

### 通过 Shell 脚本使用

```bash
# Free-form search for a landmark
./scripts/places.sh '{"query": "Eiffel Tower"}'

# Search with street-level photos
./scripts/places.sh '{"query": "Empire State Building", "include_photos": true}'

# Structured address search
./scripts/places.sh '{"street": "1600 Pennsylvania Avenue", "city": "Washington", "state": "DC", "country": "USA"}'

# Search by city
./scripts/places.sh '{"city": "San Francisco", "state": "California", "limit": 5}'
```

### 通过 curl（直接 API 调用）

该技能的名称是 `places`，但实际上它调用了 `/search` API 端点。以下是直接使用 curl 进行 API 调用的示例：

```bash
curl -X POST -H "X-API-Key: $CAMINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Eiffel Tower", "include_photos": true}' \
  "https://api.getcamino.ai/search"
```

## 参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|------|----------|---------|-------------|
| query | 字符串 | 否 | - | 自由形式的搜索内容（例如：“埃菲尔铁塔”或“中央公园”） |
| amenity | 字符串 | 否 | - | 地点类型（如餐厅、酒店等） |
| street | 字符串 | 否 | - | 街道名称和门牌号 |
| city | 字符串 | 否 | - | 城市名称 |
| county | 字符串 | 否 | - | 县份名称 |
| state | 字符串 | 否 | - | 州或省份名称 |
| country | 字符串 | 否 | - | 国家名称或代码 |
| postalcode | 字符串 | 否 | - | 邮政编码 |
| limit | 整数 | 否 | 10 | 最大返回结果数量（1-50） |
| include_photos | 布尔值 | 否 | false | 是否包含街道级图像 |
| photo_radius | 整数 | 否 | 100 | 照片搜索半径（单位：米，范围 10-500） |
| mode | 字符串 | 否 | "basic" | "advanced"（搜索模式，影响返回数据的详细程度） |

*必须提供 `query` 参数或至少一个地址相关的参数。*

## 响应格式

```json
[
  {
    "display_name": "Eiffel Tower, 5 Avenue Anatole France, 75007 Paris, France",
    "lat": 48.8584,
    "lon": 2.2945,
    "type": "tourism",
    "importance": 0.95,
    "address": {
      "tourism": "Eiffel Tower",
      "road": "Avenue Anatole France",
      "city": "Paris",
      "country": "France",
      "postcode": "75007"
    },
    "photos": [
      {
        "url": "https://...",
        "lat": 48.8580,
        "lon": 2.2948,
        "heading": 45
      }
    ],
    "has_street_imagery": true
  }
]
```

## 示例

- **对地址进行地理编码**：
```bash
./scripts/places.sh '{"street": "350 Fifth Avenue", "city": "New York", "state": "NY"}'
```

- **查找带有照片的地标**：
```bash
./scripts/places.sh '{"query": "Statue of Liberty", "include_photos": true, "photo_radius": 200}'
```

- **按邮政编码搜索**：
```bash
./scripts/places.sh '{"postalcode": "90210", "country": "USA"}'
```

- **高级模式（获取更详细的数据）**：
```bash
./scripts/places.sh '{"query": "Times Square", "mode": "advanced", "include_photos": true}'
```

## 最佳实践：

- 对于地标、兴趣点（POI）或知名地点，使用 `query` 参数进行查询。
- 使用结构化的地址信息进行精确的地理编码。
- 当需要查看地点的视觉信息时，启用 `include_photos` 选项。
- 使用 `mode: "advanced"` 以获取更丰富的数据。
- 结合使用地址的各个组成部分，以获得更准确的结果。