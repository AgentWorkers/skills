---
name: chart-splat
description: 通过 Chart Splat API 生成精美的图表。当用户需要创建、生成或以图表、图形或曲线图的形式可视化数据时，可以使用该 API。支持线图、柱状图、饼图、甜甜圈图、雷达图、极坐标面积图以及蜡烛图/OHLC 图。生成的图表将以 PNG 格式返回。
version: 1.1.0
license: MIT
compatibility: Requires Node.js and npx with network access to api.chartsplat.com
metadata:
  author: workingdevshero
  version: "1.1.0"
  homepage: https://chartsplat.com
  openclaw:
    requires:
      env:
        - CHARTSPLAT_API_KEY
      bins:
        - node
        - npx
    primaryEnv: CHARTSPLAT_API_KEY
    emoji: "bar-chart"
    homepage: https://chartsplat.com
    os:
      - darwin
      - linux
      - win32
    install:
      - kind: node
        package: chartsplat-cli
        bins: [chartsplat]
        label: "Install Chart Splat CLI via npm"
---
# Chart Splat

使用 Chart Splat API 从数据生成美观的图表。图表通过 Chart.js 在服务器端渲染，并以 PNG 图像的形式返回。

## 支持的图表类型

| 类型 | 适用场景 |
|------|----------|
| `line` | 随时间变化的趋势 |
| `bar` | 比较不同类别的数据 |
| `pie` | 表示整体中的部分占比 |
| `doughnut` | 表示整体中的部分占比（带中心空隙） |
| `radar` | 多变量数据对比 |
| `polarArea` | 采用径向布局比较不同类别的数据 |
| `candlestick` | 金融/加密货币的 OHLC 价格数据 |
| `ohlc` | 金融/加密货币的 OHLC 价格数据（条形图形式） |

## 方法 1：命令行界面（推荐）

通过 `npx` 使用 `chartsplat` 命令行工具。无需安装。

```bash
npx -y chartsplat-cli bar \
  --labels "Q1,Q2,Q3,Q4" \
  --data "50,75,60,90" \
  --title "Quarterly Revenue" \
  --color "#8b5cf6" \
  -o chart.png
```

### 命令行选项

| 标志 | 说明 |
|------|-------------|
| `-l, --labels <csv>` | 以逗号分隔的标签 |
| `-d, --data <csv>` | 以逗号分隔的数值数据 |
| `-t, --title <text>` | 图表标题 |
| `--label <text>` | 图例中的数据集标签 |
| `-c, --color <hex>` | 背景颜色 |
| `-w, --width <px>` | 图像宽度（默认：800 像素） |
| `--height <px>` | 图像高度（默认：600 像素） |
| `-o, --output <file>` | 输出文件路径（默认：chart.png） |
| `--config <file>` | 用于复杂图表的 JSON 配置文件 |

### 命令行图表相关命令

```bash
npx -y chartsplat-cli line -l "Mon,Tue,Wed,Thu,Fri" -d "100,200,150,300,250" -o line.png
npx -y chartsplat-cli bar -l "A,B,C" -d "10,20,30" -o bar.png
npx -y chartsplat-cli pie -l "Red,Blue,Green" -d "30,50,20" -o pie.png
npx -y chartsplat-cli doughnut -l "Yes,No,Maybe" -d "60,25,15" -o doughnut.png
npx -y chartsplat-cli radar -l "Speed,Power,Range,Durability,Precision" -d "80,90,70,85,95" -o radar.png
npx -y chartsplat-cli polararea -l "N,E,S,W" -d "40,30,50,20" -o polar.png
npx -y chartsplat-cli candlestick --config ohlc.json -o chart.png
```

### 蜡烛图

蜡烛图和 OHLC 图需要一个 JSON 配置文件，因为其数据格式比简单的 CSV 列表更复杂。使用 `--config` 选项提供包含 OHLC 数据点的文件。

```bash
npx -y chartsplat-cli candlestick --config ohlc.json -o candlestick.png
```

配置文件格式（`ohlc.json`）：

```json
{
  "type": "candlestick",
  "data": {
    "datasets": [{
      "label": "VVV Price",
      "data": [
        { "x": 1740441600000, "o": 4.23, "h": 4.80, "l": 4.10, "c": 4.45 },
        { "x": 1740528000000, "o": 4.45, "h": 5.50, "l": 4.30, "c": 5.34 },
        { "x": 1740614400000, "o": 5.34, "h": 6.20, "l": 5.10, "c": 5.97 }
      ]
    }]
  }
}
```

每个 OHLC 数据点需要包含以下字段：`x`（以毫秒为单位的数值时间戳，或日期字符串，例如 `"2025-02-25"`）、`o`（开盘价）、`h`（最高价）、`l`（最低价）、`c`（收盘价）。

### 通过配置文件创建复杂图表

对于多数据集或自定义图表，编写一个 JSON 配置文件，然后将其传递给命令行工具：

```bash
npx -y chartsplat-cli bar --config chart-config.json -o chart.png
```

请参阅 [examples/sample-charts.json](examples/sample-charts.json) 了解配置文件示例，以及 [references/api-reference.md](references/api-reference.md) 中的完整配置规范。

## 方法 2：辅助脚本

使用随附的辅助脚本快速生成图表，无需安装命令行工具：

```bash
node scripts/generate-chart.js bar "Q1,Q2,Q3,Q4" "50,75,60,90" "Revenue" chart.png
```

或者使用配置文件：

```bash
node scripts/generate-chart.js --config chart-config.json -o chart.png
```

## 输出处理

- 图表以 PNG 格式保存到指定的输出路径
- 默认输出文件为当前目录下的 `chart.png`
- 对于 Discord、Slack 等消息平台，返回文件路径：`MEDIA: /path/to/chart.png`
- 命令行工具和辅助脚本会自动处理 Base64 编码解码

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|-----|
| `API key required` | 缺少 `CHARTSPLAT_API_KEY` | 在代理配置中设置环境变量 |
| `Invalid API key` | API 密钥无效或已被吊销 | 在 chartsplat.com/dashboard 生成新的密钥 |
| `Rate limit exceeded` | 达到月度使用限制 | 升级计划或等待恢复 |
| `Invalid chart configuration` | 请求数据格式不正确 | 确保 `data.labels` 和 `data.datasets` 都存在（蜡烛图/OHLC 图仅需要 `data.datasets`） |

## 提示

- 确保 `labels` 和 `data` 数组的长度相同 |
- 使用十六进制颜色（例如 `#8b5cf6`）以保持样式一致性 |
- 对于饼图/甜甜圈图，使用颜色数组作为 `backgroundColor` 来为每个部分着色 |
- 默认尺寸（800x600 像素）适用于大多数场景；如需展示效果可调整大小 |
- `--config` 标志接受任何有效的 Chart.js 配置以实现完全自定义