---
name: chart-image
version: 2.2.0
description: **生成高质量图表图像的工具**  
该工具能够根据数据生成适用于出版物的图表图像，支持多种图表类型，包括折线图、条形图、面积图、点状图、蜡烛图、饼图/甜甜圈图、热力图、多系列图以及堆叠图。适用于数据可视化、图表制作、时间序列分析，以及为报告或警报生成图表图像的场景。专为 Fly.io/VPS 环境设计，无需进行任何本地编译，也不依赖 Puppeteer 或浏览器；完全基于 Node.js 构建，并提供了预编译的二进制文件。
provides:
  - capability: chart-generation
    methods: [lineChart, barChart, areaChart, pieChart, candlestickChart, heatmap]
---

# 图表图像生成器

使用Vega-Lite根据数据生成PNG格式的图表图像，非常适合无头服务器环境。

## 为什么需要这项技能？

**专为Fly.io / VPS / Docker环境设计：**
- ✅ **无需原生编译**：使用预构建的二进制文件（与需要编译工具的`canvas`不同）
- ✅ **无需Puppeteer/浏览器**：纯Node.js实现，无需下载Chrome浏览器，也没有无头浏览器的额外开销
- ✅ **轻量级**：总依赖库大小约为15MB，而基于Puppeteer的解决方案则超过400MB
- ✅ **启动速度快**：无需等待浏览器加载，可在500毫秒内生成图表
- ✅ **支持离线使用**：无需外部API调用（与QuickChart.io不同）

## 设置（一次性操作）

```bash
cd /data/clawd/skills/chart-image/scripts && npm install
```

## 快速使用方法

```bash
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type line \
  --data '[{"x":"10:00","y":25},{"x":"10:30","y":27},{"x":"11:00","y":31}]' \
  --title "Price Over Time" \
  --output chart.png
```

## 图表类型

### 折线图（默认）
```bash
node chart.mjs --type line --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output line.png
```

### 条形图
```bash
node chart.mjs --type bar --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output bar.png
```

### 面积图
```bash
node chart.mjs --type area --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output area.png
```

### 饼图/甜甜圈图
```bash
# Pie
node chart.mjs --type pie --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output pie.png

# Donut (with hole)
node chart.mjs --type donut --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output donut.png
```

### 蜡烛图（OHLC）
```bash
node chart.mjs --type candlestick \
  --data '[{"x":"Mon","open":100,"high":110,"low":95,"close":105}]' \
  --open-field open --high-field high --low-field low --close-field close \
  --title "Stock Price" --output candle.png
```

### 热力图
```bash
node chart.mjs --type heatmap \
  --data '[{"x":"Mon","y":"Week1","value":5},{"x":"Tue","y":"Week1","value":8}]' \
  --color-value-field value --color-scheme viridis \
  --title "Activity Heatmap" --output heatmap.png
```

### 多系列折线图
在同一图表上比较多个趋势：
```bash
node chart.mjs --type line --series-field "market" \
  --data '[{"x":"Jan","y":10,"market":"A"},{"x":"Jan","y":15,"market":"B"}]' \
  --title "Comparison" --output multi.png
```

### 堆叠条形图
```bash
node chart.mjs --type bar --stacked --color-field "category" \
  --data '[{"x":"Mon","y":10,"category":"Work"},{"x":"Mon","y":5,"category":"Personal"}]' \
  --title "Hours by Category" --output stacked.png
```

### 体积叠加（双Y轴）
价格线与体积条形图结合：
```bash
node chart.mjs --type line --volume-field volume \
  --data '[{"x":"10:00","y":100,"volume":5000},{"x":"11:00","y":105,"volume":3000}]' \
  --title "Price + Volume" --output volume.png
```

### 小型内联图表（Sparkline）
```bash
node chart.mjs --sparkline --data '[{"x":"1","y":10},{"x":"2","y":15}]' --output spark.png
```
默认大小为80x20像素，透明显示，无坐标轴。

## 选项参考

### 基本选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--type` | 图表类型：折线图、条形图、面积图、点状图、饼图、甜甜圈图、蜡烛图、热力图 | 折线图 |
| `--data` | 数据点的JSON数组 | - |
| `--output` | 输出文件路径 | chart.png |
| `--title` | 图表标题 | - |
| `--width` | 图表宽度（像素） | 600 |
| `--height` | 图表高度（像素） | 300 |

### 坐标轴选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--x-field` | X轴对应的字段名 | x |
| `--y-field` | Y轴对应的字段名 | y |
| `--x-title` | X轴标签 | 对应字段名 |
| `--y-title` | Y轴标签 | 对应字段名 |
| `--x-type` | X轴类型：顺序型、时间型、数值型 | 顺序型 |
| `--y-domain` | Y轴刻度范围（自动选择最小值/最大值） | 自动 |

### 视觉效果选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--color` | 折线图/条形图的颜色 | #e63946 |
| `--dark` | 深色模式 | false |
| `--svg` | 以SVG格式输出而非PNG | false |
| `--color-scheme` | Vega颜色方案（例如category10、viridis等） | - |

### 警报/监控选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--show-change` | 在最后一个数据点显示百分比变化标注 | false |
| `--focus-change` | 将Y轴放大到数据范围的2倍 | false |
| `--focus-recent N` | 仅显示最近N个数据点 | 全部数据点 |
| `--show-values` | 显示最小值/最大值标记 | false |

### 多系列/堆叠选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--series-field` | 多系列折线图使用的字段 | - |
| `--stacked` | 启用堆叠条形图模式 | false |
| `--color-field` | 用于堆叠/颜色分类的字段 | - |

### 蜡烛图选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--open-field` | OHLC开市价对应的字段 | open |
| `--high-field` | OHLC最高价对应的字段 | high |
| `--low-field` | OHLC最低价对应的字段 | low |
| `--close-field` | OHLC收盘价对应的字段 | close |

### 饼图/甜甜圈图选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--category-field` | 饼图扇区分类对应的字段 | x |
| `--donut` | 是否以甜甜圈形式显示（带中心孔） | false |

### 热力图选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--color-value-field` | 用于热力图强度的字段 | value |
| `--y-category-field` | Y轴分类对应的字段 | y |

### 体积叠加选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--volume-field` | 用于体积条形图的字段（启用双Y轴） | - |
| `--volume-color` | 体积条形图的颜色 | #4a5568 |

### 格式化选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--y-format` | Y轴格式：百分比、美元、紧凑型、小数点后4位、科学计数法或d3格式字符串 | 自动 |
| `--subtitle` | 图表标题下方的副标题 | - |
| `--hline` | 水平参考线：`value`、`value,color` 或 `value,color,label`（可重复显示） | - |

### 注释选项
| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--annotation` | 静态文本注释 | - |
| `--annotations` | 事件标记的JSON数组 | - |

## 警报样式图表（推荐用于监控界面）

```bash
node chart.mjs --type line --data '[...]' \
  --title "Iran Strike Odds (48h)" \
  --show-change --focus-change --show-values --dark \
  --output alert.png
```

**仅显示最近的操作记录：**
```bash
node chart.mjs --type line --data '[hourly data...]' \
  --focus-recent 4 --show-change --focus-change --dark \
  --output recent.png
```

## 时间轴注释

在图表上标记事件：
```bash
node chart.mjs --type line --data '[...]' \
  --annotations '[{"x":"14:00","label":"News broke"},{"x":"16:30","label":"Press conf"}]' \
  --output annotated.png
```

## 时间轴设置（适用于具有日期间隔的时间序列数据）

当X轴值为ISO日期且需要根据实际时间间隔显示数据时，使用`--x-type temporal`：

## Y轴格式化

优化Y轴数值的显示效果：
```bash
# Dollar amounts
node chart.mjs --data '[...]' --y-format dollar --output revenue.png
# → $1,234.56

# Percentages (values as decimals 0-1)
node chart.mjs --data '[...]' --y-format percent --output rates.png
# → 45.2%

# Compact large numbers
node chart.mjs --data '[...]' --y-format compact --output users.png
# → 1.2K, 3.4M

# Crypto prices (4 decimal places)
node chart.mjs --data '[...]' --y-format decimal4 --output molt.png
# → 0.0004

# Custom d3-format string
node chart.mjs --data '[...]' --y-format ',.3f' --output custom.png
```

可用格式化选项：`percent`、`dollar`/`usd`、`compact`、`decimal2`、`decimal4`、`scientific`

## 图表副标题

在图表标题下方添加说明性文字：
```bash
node chart.mjs --title "MOLT Price" --subtitle "20,668 MOLT held" --data '[...]' --output molt.png
```

## 主题选择

使用`--dark`选项切换到深色模式。根据时间自动选择模式：
- **夜间（20:00-07:00本地时间）**：`--dark`
- **白天（07:00-20:00本地时间）**：默认的浅色模式

## 数据传输

```bash
echo '[{"x":"A","y":1},{"x":"B","y":2}]' | node chart.mjs --output out.png
```

## 自定义Vega-Lite配置

用于高级图表定制：
```bash
node chart.mjs --spec my-spec.json --output custom.png
```

## ⚠️ 重要提示：**务必发送生成的图表！**

生成图表后，**务必将其发送给用户**。
不要仅将其保存到文件中并口头描述——图表的目的是为了直观展示数据。

```bash
# 1. Generate the chart
node chart.mjs --type line --data '...' --output /data/clawd/tmp/my-chart.png

# 2. Send it! Use message tool with filePath:
#    action=send, target=<channel_id>, filePath=/data/clawd/tmp/my-chart.png
```

**提示：**
- 将文件保存到`/data/clawd/tmp/`（永久存储位置），而非`/tmp/`（可能被清理）
- 使用`action=send`命令并指定文件路径——`thread-reply`不支持文件附件
- 在消息文本中添加简短的说明
- 在以色列时间20:00-07:00期间自动使用深色模式

---
*更新时间：2026-02-04 - 新增了`--y-format`（百分比/美元/紧凑型/小数点后4位）和`--subtitle`选项*