---
name: habit-ai
description: 通过 Habit AI API 追踪营养摄入、饮食记录、水分摄入、体重变化、步数数据、冥想情况以及日记内容。该功能可用于记录食物摄入、检查卡路里摄入量、监测水分摄入、记录体重或步数、撰写日记，以及获取人工智能提供的营养建议，或根据照片/描述分析食物成分。使用该服务需要拥有 Habit AI 账户和 API 密钥（格式为 hab_*）。
---
# Habit AI

通过Habit AI的REST API来跟踪健康和营养状况。

## 设置

1. 在https://habitapp.ai（或iOS应用程序）上创建账户。
2. 进入“设置” → “API密钥” → “创建密钥”。
3. 将密钥存储在环境变量中：`export HABITAI_API_KEY="hab_..."`

所有请求都使用以下信息：
- 基本URL：`https://habitapp.ai/api/v1`
- 认证头：`Authorization: Bearer $HABITAI_API_KEY`
- 内容类型：`application/json`

## 快速参考

| 操作 | 方法 | 端点 |
|--------|--------|----------|
| 记录餐食 | POST | `/meals` |
| 当天的餐食 | GET | `/meals?date=YYYY-MM-DD` |
| 每日营养状况 | GET | `/nutrition/daily?date=YYYY-MM-DD` |
| 每周营养状况 | GET | `/nutrition/weekly?date=YYYY-MM-DD` |
| 记录饮水量（毫升） | POST | `/water` |
| 记录体重（千克） | POST | `/weight` |
| 记录步数 | POST | `/steps` |
| 记录冥想时间 | POST | `/meditation` |
| 记录日记 | POST | `/journal` |
| AI饮食教练 | POST | `/coaches/eating` |
| AI正念教练 | POST | `/coaches/mindfulness` |
| AI冥想教练 | POST | `/coaches/meditation` |
| 获取个人资料 | GET | `/profile` |
| 更新个人资料 | PUT | `/profile` |

有关端点的完整详细信息（请求/响应模式、所有参数），请参阅[references/api.md](references/api.md)。

## 正确记录餐食的方法

### ⚠️ 重要提示：**使用AI模型分析食物内容，然后按照以下结构通过POST请求到 `/meals`**

**请勿** 调用 `/analyze/food-image` 或 `/analyze/meal-description`——而是使用您自己的视觉/语言能力来分析食物，然后构建以下JSON结构并通过POST请求到 `/meals`。

### 第0步：查看用户个人资料中的过敏原/饮食限制

在分析之前，先调用 `GET /profile` 以查看 `foodSensitivities` 和 `diet` 字段。将这些信息纳入以下评估中：
- **健康评分**：如果餐食包含用户敏感的成分，请降低评分。
- **健康评分说明**：说明餐食的整体营养优缺点。
- **健康敏感性说明**：如果餐食包含用户的过敏原或敏感成分，请说明具体是哪些成分以及原因。如果没有匹配的敏感成分，则留空字符串。

### 第1步：自行分析食物

对于**图片**：查看图片并识别每种成分，估算份量，并使用美国农业部（USDA）的数据计算营养价值。

对于**描述**：解析餐食描述，并以相同的方式计算营养价值。

### 第2步：按照以下结构通过POST请求到 `/meals`

每个字段都很重要。iOS系统会从 `nutritionalSummary`（嵌套对象）中获取数据——如果该字段缺失，餐食的卡路里显示为0。

```json
{
  "mealName": "Grilled Chicken Salad with Ranch",
  "calories": 520,
  "protein": 42,
  "carbs": 18,
  "fat": 32,
  "fiber": 4,
  "sodium": 890,
  "sugar": 6,
  "healthScore": 7,
  "healthScoreExplanation": "Lean protein from grilled chicken and fiber from greens, but ranch dressing adds significant fat and sodium.",
  "mealType": "lunch",
  "analysisConfidenceLevel": 8,
  "ingredients": [
    {
      "name": "grilled chicken breast",
      "calories": 280,
      "protein": 35,
      "carbs": 0,
      "fat": 14,
      "sugar": 0,
      "fiber": 0,
      "sodium": 400,
      "healthScore": 8,
      "measurementType": "grams",
      "measurementValue": 200
    },
    {
      "name": "mixed salad greens",
      "calories": 20,
      "protein": 2,
      "carbs": 4,
      "fat": 0,
      "sugar": 1,
      "fiber": 2,
      "sodium": 30,
      "healthScore": 9,
      "measurementType": "cups",
      "measurementValue": 2
    },
    {
      "name": "ranch dressing",
      "calories": 220,
      "protein": 5,
      "carbs": 14,
      "fat": 18,
      "sugar": 5,
      "fiber": 2,
      "sodium": 460,
      "healthScore": 3,
      "measurementType": "spoons",
      "measurementValue": 3
    }
  ]
}
```

### 字段参考

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `mealName` | 字符串 | 是 | 显示名称（例如“鸡肉凯撒沙拉”）。如果没有这个字段，餐食在应用程序中将没有名称。 |
| `calories` | 数字 | 是 | 总卡路里（千卡）。必须大于0。 |
| `protein` | 数字 | 是 | 总蛋白质（克） |
| `carbs` | 数字 | 是 | 总碳水化合物（克） |
| `fat` | 数字 | 是 | 总脂肪（克） |
| `fiber` | 数字 | 是 | 总纤维（克） |
| `sodium` | 数字 | 是 | 总钠（毫克） |
| `sugar` | 数字 | 是 | 总糖（克） |
| `healthScore` | 整数 | 是 | 这顿餐食的整体健康程度（1=非常不健康，10=非常健康） |
| `mealType` | 字符串 | 是 | 可以是：`breakfast`（早餐）、`lunch`（午餐）、`dinner`（晚餐）、`snack`（零食） |
| `analysisConfidenceLevel` | 整数 | 是 | 对营养估计的信心程度（1=完全猜测，10=来自包装上的准确数据）。对于图片分析使用6-8，对于描述使用5-7。 |
| `healthScoreExplanation` | 字符串 | 是 | 1-2句话的营养优缺点说明（例如：“鸡肉提供了良好的蛋白质，但香肠和酱料中的钠含量较高。” |
| `healthSensitivityExplanation` | 字符串 | 是 | 如果餐食包含用户的过敏原或食物敏感成分，请说明具体是哪些成分。如果没有敏感成分或用户未设置敏感成分，则留空字符串 `""`。 |
| `ingredients` | 数组 | 是 | 成分对象数组（见下文） |
| `imageUrl` | 字符串 | 否 | 食物图片的URL。首先通过 `POST /meals/upload-image` 获取该URL（见下文）。 |
| `dateScanned` | 字符串 | 否 | ISO 8601时间戳。如果省略则默认为当前时间。 |
| `serving` | 数字 | 否 | 份量倍数（默认为1.0） |

### 成分对象

`ingredients` 数组中的每个成分都必须包含以下字段：

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `name` | 字符串 | 成分名称（例如“烤鸡胸肉”） |
| `calories` | 数字 | 该成分的卡路里（千卡） |
| `protein` | 数字 | 蛋白质（克） |
| `carbs` | 数字 | 碳水化合物（克） |
| `fat` | 数字 | 脂肪（克） |
| `sugar` | 数字 | 糖（克） |
| `fiber` | 数字 | 纤维（克） |
| `sodium` | 数字 | 钠（毫克） |
| `healthScore` | 整数 | 该特定成分的健康评分（1-10） |
| `measurementType` | 字符串 | 必须是以下之一：`grams`（克）、`ounces`（盎司）、`cups`（杯）、`spoons`（汤匙）、`servings`（份）。用于表示块/片/碗/份量；`spoons` 用于表示汤匙/茶匙。 |
| `measurementValue` | 数字 | 指定单位中的数量 |

### 重要规则

1. **所有营养值必须是数字，不能是字符串**。例如：“calories”: 520 而不是 “calories”: “520”。
2. **所有成分的卡路里总和应接近总卡路里**（误差在5%以内）。
3. `mealName` 是必填项——如果没有这个字段，餐食在iOS系统中将不可见。
4. `healthScore` 是1-10之间的整数——根据实际情况判断（快餐=2-4，家常菜=6-8，生沙拉=9-10）。
5. `analysisConfidenceLevel` 是1-10之间的整数——诚实地反映你的不确定性。
6. **钠的单位是毫克**，其他所有单位的数值都是克（卡路里除外）。

### 上传餐食图片（缩略图）

如果你有食物图片，请先上传以获取URL：

```bash
curl -X POST https://habitapp.ai/api/v1/meals/upload-image \
  -H "Authorization: Bearer $HABITAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"imageBase64": "<base64-encoded-image>"}'
```

返回值：`{"success": true, "imageUrl": "https://firebasestorage.googleapis.com/..."}`

然后在POST请求 `/meals` 时传递 `imageUrl`。你也可以将其附加到现有的餐食记录中：

```json
{"imageBase64": "<base64>", "mealId": "<existing-meal-id>"}
```

**包含图片的完整流程：**
1. 使用base64编码上传图片到 `POST /meals/upload-image` → 获取 `imageUrl`。
2. 使用营养数据和 `imageUrl` 通过 `POST` 请求到 `/meals`。

## 其他操作

### 查看剩余卡路里

1. 通过 `GET /nutrition/daily` 查看当天的总卡路里。
2. 通过 `GET /profile` 查看卡路里目标。
3. 计算差值：`caloriesGoal - totalCalories`。

### 快速记录饮水量

```bash
curl -X POST https://habitapp.ai/api/v1/water \
  -H "Authorization: Bearer $HABITAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 500}'
```

饮水量单位为毫升。1杯约等于237毫升，1玻璃杯约等于250毫升。

## 注意事项

- 如果省略日期，默认使用用户的时区设置。
- 饮水量单位为毫升。
- 体重单位为千克（1磅约等于0.4536千克）。
- 如果个人资料中包含身高/体重/性别信息，系统会自动计算消耗的卡路里。
- 每个账户最多可以使用5个API密钥。