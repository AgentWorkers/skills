---
name: iqair
description: 通过 IQAir API 获取全球任何地点的实时空气质量数据。该接口返回空气质量指数（AQI）以及相应的视觉指示器和空气质量等级。当被询问空气质量、污染程度或特定城市/地区的空气质量时（例如：“里加的空气质量如何？”、“在北京外出安全吗？”、“空气质量怎么样？”），可以使用此接口。此外，在查询一般天气信息时，也可以结合空气质量数据来提供更全面的天气报告（例如：“布达佩斯的天气如何？”、“今天的天气状况如何？”）。
metadata:
  openclaw:
    homepage: https://github.com/atesluks/openclaw-skill-iqair
    requires:
      env: ["IQAIR_API_KEY"]
---
# IQAir空气质量检测器

通过IQAir API获取实时空气质量数据，并以格式化的方式输出，包括AQI指数、表情符号指示器和空气质量等级。

## 先决条件

**需要API密钥**：用户必须拥有一个免费的IQAir API密钥，并将其存储在`IQAIR_API_KEY`环境变量中。

如果密钥未设置，请指导用户：
1. 访问 https://dashboard.iqair.com/personal/api-keys
2. 注册/登录并订阅免费的社区计划
3. 复制API密钥
4. 设置环境变量：`export IQAIR_API_KEY="your_key_here"`

## 快速使用方法

**按城市名称查询：**
```bash
python scripts/get_aqi.py Riga Latvia
python scripts/get_aqi.py London "United Kingdom"
python scripts/get_aqi.py Budapest Hungary
```

**按坐标查询（最可靠的方式）：**
```bash
python scripts/get_aqi.py --lat 56.9496 --lon 24.1052
```

**根据IP地址查询最近的城市：**
```bash
python scripts/get_aqi.py --nearest
```

## 如何响应用户查询

当用户询问空气质量时：

1. **确定位置** - 从用户的查询中提取城市/国家信息
2. **运行脚本** - 使用`scripts/get_aqi.py`并传递相应的参数
3. **返回格式化结果** - 脚本会提供表情符号、AQI值、空气质量等级和位置信息

**示例交互过程：**

用户："里加的空气质量如何？"

响应过程：
- 获取位置信息：里加，拉脱维亚
- 运行脚本：`python scripts/get_aqi.py Riga Latvia`
- 输出结果：`🟢 19 - 良好\n里加，拉脱维亚`
- 回答："里加的空气质量目前非常好！🟢 19（良好）"

## 处理位置名称

- **城市/国家名称**：使用IQAir数据库中显示的准确名称
- 首都城市：通常省名与城市名称相同
- 如果城市查询失败，可以尝试使用坐标进行查询

**常见的位置输入格式**：
- 里加，拉脱维亚 → `Riga Latvia`（省名默认为城市名称）
- 伦敦，英国 → `London "United Kingdom"`（如果包含空格，请用引号括起来）
- 纽约，美国 → `"New York" "United States" "New York"`（城市、国家、州名）

**不确定时**：建议使用`--lat`和`--lon`参数进行基于坐标的查询（更可靠）

## 输出格式

脚本返回一个简洁的格式化字符串：
```
🟢 45 - Good
Riga, Latvia
```

根据AQI等级自定义响应内容：
- **0-50（🟢 良好）**："空气质量极佳，适合户外活动"
- **51-100（🟡 一般）**："空气质量尚可，敏感人群应减少长时间户外活动"
- **101-150（🟠 有轻微危害）**："对敏感人群不健康，儿童和呼吸系统有问题的人应减少户外活动"
- **151-200（🔴 有害）**："所有人都可能受到健康影响，应减少户外活动"
- **201-300（🟣 非常有害）**："健康警报，避免户外活动"
- **301+（🟤 危险）**："紧急情况，请待在室内"

## 技术细节

有关API规范、端点和错误处理的信息，请参阅`references/api.md`。

## 使用限制

免费社区计划的限制如下：
- 每分钟5次请求
- 每天500次请求
- 每月10,000次请求

请避免在短时间内对同一位置进行多次请求。