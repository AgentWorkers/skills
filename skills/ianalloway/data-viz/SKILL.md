---
name: data-viz
description: "通过命令行创建数据可视化效果。无需离开终端，即可从 CSV/JSON 数据生成图表、图形和图像。"
homepage: https://github.com/red-data-tools/YouPlot
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "uplot-gem",
              "kind": "shell",
              "command": "gem install youplot",
              "bins": ["uplot"],
              "label": "Install YouPlot (Ruby gem)",
            },
            {
              "id": "termgraph-pip",
              "kind": "shell", 
              "command": "pip install termgraph",
              "bins": ["termgraph"],
              "label": "Install termgraph (Python)",
            },
          ],
      },
  }
---
# 数据可视化

可以从 CSV、JSON 或通过管道传输的数据生成基于终端的图表和可视化效果。

## 使用 YouPlot 进行快速可视化

YouPlot（`uplot`）可以在终端中生成 Unicode 格式的图表。

### 条形图

```bash
echo -e "Apple,30\nBanana,45\nCherry,20\nDate,35" | uplot bar -d, -t "Fruit Sales"
```

### 折线图

```bash
seq 1 20 | awk '{print $1, sin($1/3)*10+10}' | uplot line -t "Sine Wave"
```

### 直方图

```bash
awk 'BEGIN{for(i=0;i<1000;i++)print rand()}' | uplot hist -t "Random Distribution" -n 20
```

### 散点图

```bash
awk 'BEGIN{for(i=0;i<100;i++)print rand()*100, rand()*100}' | uplot scatter -t "Random Points"
```

## 从 CSV 文件生成图表

```bash
# Bar chart from CSV
cat sales.csv | uplot bar -d, -H -t "Monthly Sales"

# Line chart with headers
cat timeseries.csv | uplot line -d, -H -t "Stock Price"
```

## 从 JSON 文件生成图表（使用 jq）

```bash
# Extract data from JSON and plot
curl -s "https://api.example.com/data" | jq -r '.items[] | "\(.name),\(.value)"' | uplot bar -d,
```

## Termgraph（Python 的替代方案）

简单的水平条形图：

```bash
echo -e "2020 50\n2021 75\n2022 90\n2023 120" | termgraph
```

带颜色的条形图：

```bash
echo -e "Sales 150\nCosts 80\nProfit 70" | termgraph --color green
```

## Gnuplot（高级用法）

用于生成适合出版的高质量图表：

```bash
# Quick line plot
gnuplot -e "set terminal dumb; plot sin(x)"

# From data file
gnuplot -e "set terminal dumb; plot 'data.txt' with lines"
```

## Sparklines（迷你图表）

内联迷你图表：

```bash
# Using spark (if installed)
echo "1 5 22 13 5" | spark
# Output: ▁▂█▅▂

# Pure bash sparkline
data="1 5 22 13 5"; min=$(echo $data | tr ' ' '\n' | sort -n | head -1); max=$(echo $data | tr ' ' '\n' | sort -n | tail -1); for n in $data; do printf "\u258$((7-7*($n-$min)/($max-$min)))"; done; echo
```

## ASCII 表格

将数据格式化为表格：

```bash
# Using column
echo -e "Name,Score,Grade\nAlice,95,A\nBob,82,B\nCarol,78,C" | column -t -s,

# Using csvlook (csvkit)
cat data.csv | csvlook
```

## 实际应用示例

### 股票价格图表

```bash
# Fetch and plot stock data (using Alpha Vantage free API)
curl -s "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=demo" | \
  jq -r '.["Time Series (Daily)"] | to_entries | .[:20] | reverse | .[] | "\(.key) \(.value["4. close"])"' | \
  uplot line -t "AAPL Stock Price"
```

### 系统指标

```bash
# CPU usage over time
for i in {1..20}; do
  top -bn1 | grep "Cpu(s)" | awk '{print 100-$8}'
  sleep 1
done | uplot line -t "CPU Usage %"
```

### API 响应时间

```bash
# Measure and plot response times
for i in {1..10}; do
  curl -s -o /dev/null -w "%{time_total}\n" https://example.com
done | uplot line -t "Response Time (s)"
```

## 提示

- 对于逗号分隔的数据，使用 `-d`；对于制表符分隔的数据，使用 `-d'\t'`
- 如果数据包含标题行，请使用 `-H`
- 使用 `head` 或 `tail` 命令来限制显示的数据量
- 结合 `jq` 进行 JSON 数据的提取和处理
- 使用 `watch` 命令实现图表的实时更新：`watch -n1 'command | uplot bar'`