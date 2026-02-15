---
name: who-growth-charts
description: 生成世界卫生组织（WHO）推荐的儿童生长图表（包括身高、体重和BMI数据），并附带相应的百分位数曲线。用户可根据需要下载官方的WHO参考数据。该工具适用于用户咨询儿童生长情况、百分位数信息，或需要为孩子生成生长图表的情况。
version: 1.2.1
homepage: https://github.com/odrobnik/who-growth-charts-skill
metadata: {"openclaw": {"emoji": "📈", "requires": {"bins": ["python3"], "python": ["pandas", "matplotlib", "scipy", "openpyxl"]}}}
---

生成包含百分位曲线和儿童数据叠加的WHO儿童生长标准图表。

## 功能

- **按年龄计算的身高**（0-19岁）
- **按年龄计算的体重**（0-10岁）
- **按年龄计算的BMI**（0-19岁）
- 支持**男孩和女孩**
- 可根据需要从cdn.who.int下载WHO数据（数据会缓存到本地）
- 将儿童的实际测量数据与趋势线叠加显示

## 示例

| 身高 | 体重 | BMI |
|--------|--------|-----|
| <img src="examples/anna_height.png" width="250"> | <img src="examples/anna_weight.png" width="250"> | <img src="examples/anna_bmi.png" width="250"> |

## 先决条件

安装Python依赖项：
```bash
pip install pandas matplotlib scipy openpyxl
```

## 使用方法

### 基本图表生成

```bash
python3 ./scripts/growth_chart.py "Child Name" "DD.MM.YYYY" --sex F --type all
```

参数：
- `name`：儿童的名字（用于图表标题）
- `birthdate`：出生日期（格式为DD.MM.YYYY）
- `--sex` / `-s`：`F`（女性）或 `M`（男性） — 默认值：F
- `--type` / `-t`：`height`（身高）、`weight`（体重）、`bmi`（BMI）或 `all`（全部） — 默认值：all
- `--data` / `-d`：包含测量数据的JSON文件
- `--output` / `-o`：图表的输出目录

### 使用测量数据

创建一个包含身高/体重测量数据的JSON文件（身高单位为米，体重单位为千克）：
```json
{
  "heights": [ ["2024-01-15T10:00:00", 1.05] ],
  "weights": [ ["2024-01-15T10:00:00", 17.5] ]
}
```

```bash
python3 ./scripts/growth_chart.py "Emma" "06.07.2016" --sex F --data emma_data.json --type all
```

### 与Withings集成

结合`withings-family`技能自动获取体重数据：
```bash
# Get Withings weight data (assuming withings-family skill is installed)
python3 ../withings-family/scripts/withings.py emma body > /tmp/withings.json

# Parse and generate charts
# (The growth chart script handles Withings JSON format if implemented, otherwise transform it)
```

## 输出结果

默认情况下，图表和缓存文件会被保存在以下路径：

- `<workspace>/who-growth-charts/`
- `<workspace>/who-growth-charts/cache/`

其中`<workspace>`是包含`skills/`目录的文件夹（脚本会自动查找该文件夹；如果当前工作目录符合工作空间的格式，也会使用当前工作目录，这样可以正确处理符号链接的工作空间）。

您可以通过`WHO_GROWTH_CHARTS_WORKSPACE=/path/to/workspace`来覆盖工作空间的查找路径。