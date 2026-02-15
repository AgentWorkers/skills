---
name: countries
version: 1.0.0
description: "这是一个用于AI代理查询其人类用户所在国家信息的命令行工具（CLI）。该工具通过REST Countries API来获取国家信息，且无需进行身份验证（无需登录或提供用户名/密码）。"
homepage: https://restcountries.com
metadata:
  openclaw:
    emoji: "🌍"
    requires:
      bins: ["bash", "curl", "jq", "bc"]
    tags: ["countries", "geography", "reference", "api", "cli"]
---

# 国家信息查询

这是一个用于AI代理查询国家信息的命令行工具（CLI），可以帮助代理回答用户关于国家的问题。例如：“蒙古的首都是哪里？”现在，您的AI代理就可以回答这个问题了。

该工具使用REST Countries API（v3.1）进行数据查询，无需注册账户或API密钥。

## 使用方法

```
"Tell me about Japan"
"What countries are in South America?"
"Which country has Tokyo as capital?"
"Info on country code DE"
```

## 命令

| 功能 | 命令                |
|--------|-------------------|
| 按名称搜索 | `countries search "查询"`     |
| 获取详细信息 | `countries info <国家代码>`    |
| 按地区列出 | `countries region <地区>`    |
| 按首都搜索 | `countries capital <首都>`    |
| 列出所有国家 | `countries all`       |

### 示例

```bash
countries search "united states"   # Find country by name
countries info US                  # Get full details by alpha-2 code
countries info USA                 # Also works with alpha-3
countries region europe            # All European countries
countries capital tokyo            # Find country by capital
countries all                      # List all countries (sorted)
```

### 可用的地区

有效地区：`africa`、`americas`、`asia`、`europe`、`oceania`

## 输出结果

**搜索/列表结果：**
```
[US] United States — Washington D.C., Americas, Pop: 331M, 🇺🇸
```

**详细信息输出：**
```
🌍 Japan
   Official: Japan
   Code: JP / JPN / 392
   Capital: Tokyo
   Region: Asia — Eastern Asia
   Population: 125.8M
   Area: 377930 km²
   Languages: Japanese
   Currencies: Japanese yen (JPY)
   Timezones: UTC+09:00
   Borders: None (island/isolated)
   Driving: left side
   Flag: 🇯🇵

🗺️ Map: https://goo.gl/maps/...
```

## 注意事项

- 使用REST Countries API v3.1（restcountries.com）
- 无需认证或速率限制
- 国家代码格式：alpha-2（例如：US）、alpha-3（例如：USA）或数字格式（例如：840）
- 人口数据会以“K/M/B”后缀表示（千/百万/十亿）
- 所有地区名称均使用小写形式

---

## 代理实现说明

**脚本位置：`{skill_folder}/countries`（`scripts/countries`的封装脚本）**

**当用户询问国家相关信息时：**
1. 运行 `./countries search "名称"` 以获取国家代码
2. 运行 `./countries info <国家代码>` 以获取详细信息
3. 运行 `./countries region <地区>` 以获取该地区的国家列表
4. 运行 `./countries capital <首都>` 以查询特定国家的首都

**常见使用场景：**
- “X属于哪个国家？” → 按名称搜索
- “介绍一下X国家” → 先搜索国家名称，再获取详细信息
- “欧洲的国家有哪些？” → 选择“region europe”进行查询
- “X国家的首都是哪里？” → 先搜索国家名称，再查看首都信息
- “哪个国家的首都是X？” → 按首都名称进行搜索

**不适用场景：**
- 历史上的国家、有争议的地区或非主权领土