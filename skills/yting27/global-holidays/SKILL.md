---
name: holidays
description: >
  每当任务涉及检查、生成或处理公共假期信息时（无论针对哪个国家或地区，如州、省、区域），请使用此技能。适用的场景包括：  
  - “[日期] 是公共假期吗？”  
  - “列出 [国家/年份] 的所有公共假期”  
  - “在 [日期范围] 内查找公共假期”  
  - “确定工作日/非工作日”  
  - “跳过公共假期”  
  - “创建假期日历”  
  - 以及任何需要判断某个日期是否为政府规定的公共假期的任务。  
  此外，当需要将公共假期与自定义假期或个人假期日期结合使用时，也请使用此技能。  
  **请注意：**  
  - 请勿将此技能用于一般的日期运算、时区转换或日历渲染，除非这些操作与公共假期直接相关。
---
# holidays — Python Holiday Library

## 概述

`holidays` 是一个 Python 库，它可以动态生成各国及各地区官方规定的节假日列表。该库支持 249 个国家（根据 ISO 3166-1 标准），并通过 ISO 3166-2 标准支持各个地区的划分（如州、省、地区）。

该库的核心对象是 `HolidayBase`，它的工作方式类似于 Python 中的 `dict`，将日期与节假日名称进行映射。以下所有示例都可以在 shell 中直接运行：

```bash
python <<'EOF'
# your code here
EOF
```

---

## 安装

```bash
pip install --upgrade holidays
```

要获取最新开发版本，请执行以下命令：

```bash
pip install --upgrade https://github.com/vacanza/holidays/tarball/dev
```

---

## 快速参考

| 任务 | 方法                |
|------|-------------------|
| 获取某国/某年的所有节假日 | `country_holidays('US', years=2024)` |
| 获取某个地区的节假日 | `country_holidays('US', subdiv='CA', years=2024)` |
| 获取指定日期范围内的节假日 | `holidays_obj['2024-01-01':'2024-01-31']` |
| 检查某个日期是否为节假日 | `holidays_obj.get('2024-12-25')` （返回节假日名称或 `None`） |
| 添加自定义节假日 | `holidays_obj.update({'2024-07-10': 'My Birthday!'})` |
| 列出所有支持的国家 | `list_supported_countries()` |
| 列出支持多语言节假日的国家 | `list_localized_countries()` |

---

## 核心 API

### `country_holidays()` — 主函数

```python
country_holidays(
    country,          # ISO 3166-1 alpha-2 code, e.g. 'US', 'GB', 'DE'
    subdiv=None,      # ISO 3166-2 subdivision code, e.g. 'CA', 'TX', 'BY'
    years=None,       # int or list of ints, e.g. 2024 or [2023, 2024]
    expand=True,      # auto-expand years when checking dates outside current range
    observed=True,    # include observed holidays (e.g. holiday on weekend → Monday)
    language=None,    # ISO 639-1 language code for holiday names, e.g. 'en', 'de'
    categories=None,  # filter to specific holiday categories (country-dependent)
)
```

该函数返回一个 `HolidayBase` 对象（类似字典的结构：`{日期: 节日名称}`）。

---

## 常见操作

### 1. 获取某国某年的所有节假日

```python
from holidays import country_holidays

us_holidays = country_holidays('US', years=2024)
for date, name in sorted(us_holidays.items()):
    print(date, name)
```

### 2. 获取某个地区的节假日

使用 ISO 3166-2 标准的地区代码（例如，`'CA'` 表示加利福尼亚州，`'BY'` 表示巴伐利亚州）。

```python
from holidays import country_holidays

ca_holidays = country_holidays('US', subdiv='CA', years=2024)
for date, name in sorted(ca_holidays.items()):
    print(date, name)
```

### 3. 获取指定日期范围内的节假日

使用日期字符串（格式为 `YYYY-MM-DD`）从 `HolidayBase` 对象中提取相应的节假日信息。

```python
from holidays import country_holidays

ca_holidays = country_holidays('US', subdiv='CA', years=2024)
for day in ca_holidays['2024-01-01':'2024-01-31']:
    print(f"{day}: {ca_holidays.get(day)}")
```

### 4. 检查某个日期是否为节假日

如果日期是节假日，`.get()` 方法会返回节假日名称；否则返回 `None`。

```python
from holidays import country_holidays

ca_holidays = country_holidays('US', subdiv='CA')

# Is December 25 a holiday?
name = ca_holidays.get('2024-12-25')
print(name)   # → 'Christmas Day'

# Is December 26 a holiday?
name = ca_holidays.get('2024-12-26')
print(name)   # → None
```

**提示：** 使用 `if date in holidays_obj:` 进行布尔判断（比 `.get()` 更快）。

### 5. 使用自定义节假日

自定义节假日信息存储在 `$HOME/openclaw-personal/custom-holidays.json` 文件中：

```json
{
  "2024-07-10": "My Birthday!",
  "2024-10-01": "Family Celebration"
}
```

可以使用 `.update()` 方法将这些自定义节假日信息合并到国家的节假日列表中。

```python
import json
from pathlib import Path
from holidays import country_holidays

custom_file = Path("~/openclaw-personal/custom-holidays.json").expanduser()
with open(custom_file) as f:
    custom_data = json.load(f)

holidays_2024 = country_holidays('US', years=2024)
holidays_2024.update(custom_data)

print(holidays_2024.get('2024-07-10'))  # → 'My Birthday!'
```

### 6. 列出所有支持的国家及地区

```python
from holidays import list_supported_countries

# include_aliases=True also returns common aliases (e.g. 'UK' for 'GB')
supported = list_supported_countries(include_aliases=True)
print(supported['US'])   # → list of supported US subdivision codes
```

### 7. 使用多语言版本的节假日名称

部分国家支持多种语言的节假日名称显示。

```python
from holidays import list_localized_countries, country_holidays

localized = list_localized_countries(include_aliases=True)

# Get supported languages for Malaysia
langs = localized['MY']   # e.g. ['en_MY', 'ms_MY', 'zh_CN']

# Generate holidays in the first available language
for date, name in sorted(country_holidays('MY', years=2025, language=langs[0]).items()):
    print(date, name)
```

---

## 需要了解的关键参数：

- **`observed=True`（默认值）：** 如果节假日落在周末，系统会返回实际的放假日期（通常是周一）。将 `observed` 设置为 `False` 可仅获取法定放假日期。
- **`expand=True`（默认值）：** 如果查询的日期超出了指定的年份范围，库会自动将该年份添加到结果中。将 `expand` 设置为 `False` 可避免这种情况。
- **多年份查询：** 可通过传递年份列表（如 `years=[2023, 2024, 2025]`）一次性获取多个年份的节假日信息。
- **日期格式：** `HolidayBase` 字典的键可以是 `datetime.date`、`datetime.datetime` 或 `'YYYY-MM-DD'` 字符串。
- **国家代码：** 使用 ISO 3166-1 的两位字母代码（如 `'US'`、`GB`、`DE`）。当 `include_aliases=True` 时，也支持使用别名（如 `'UK'`）。

---

## 依赖项

- **Python**：3.8 及更高版本
- **软件包：** `holidays`（通过 PyPI 安装：`pip install --upgrade holidays`）
- 无需额外的系统依赖项。