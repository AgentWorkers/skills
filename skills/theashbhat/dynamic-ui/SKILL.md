---
name: dynamic-ui
description: 使用 HTML 模板和 wkhtmltoimage 将表格、图表、统计数据、信息卡以及仪表板渲染为图像。
metadata:
  openclaw:
    requires:
      bins: ["wkhtmltoimage", "jq"]
    install:
      - id: apt-wkhtmltopdf
        kind: apt
        packages: ["wkhtmltopdf", "jq", "fonts-noto-color-emoji"]
        bins: ["wkhtmltoimage", "jq"]
        label: "Install wkhtmltoimage + jq (apt)"
      - id: brew-wkhtmltopdf
        kind: brew
        packages: ["wkhtmltopdf", "jq"]
        bins: ["wkhtmltoimage", "jq"]
        label: "Install wkhtmltoimage + jq (brew)"
    installHint: |
      This skill requires wkhtmltoimage and jq. Install with:
      Ubuntu/Debian: sudo apt-get install -y wkhtmltopdf jq fonts-noto-color-emoji
      macOS: brew install wkhtmltopdf jq
---
# 动态用户界面技能

使用 HTML 模板和 `wkhtmltoimage` 工具，将动态视觉内容（表格、图表、统计数据、信息卡、仪表板等）渲染为图像。

## 触发条件
- `render`、`visualize`、`chart`、`dashboard`、`dynamic-ui`

## 使用方法

```bash
# Basic usage
./scripts/render.sh <template> --data '<json>'

# With options
./scripts/render.sh table --data '{"columns":["A","B"],"rows":[["1","2"]]}' --style dark --output out.png

# From stdin
echo '{"labels":["Q1","Q2"],"values":[100,200]}' | ./scripts/render.sh chart-bar --style modern
```

## 模板

| 模板 | 描述 | 输入格式 |
|----------|-------------|--------------|
| `table` | 数据表格 | `{"columns": [...], "rows": [[...], ...]}` |
| `chart-bar` | 条形图 | `{"labels": [...], "values": [...], "title": "..."}` |
| `stats` | 关键绩效指标（KPI）信息卡 | `{"stats": [{"label": "...", "value": "...", "change": "..."}]}` |
| `card` | 信息卡 | `{"title": "...", "subtitle": "...", "body": "...", "status": "green\|yellow\|red"}` |
| `dashboard` | 复合界面 | `{"title": "...", "widgets": [{"type": "stat\|table\|chart", ...}]}` |

## 选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--data`, `--input` | JSON 数据（或使用标准输入） | - |
| `--style` | 主题风格：modern、dark、minimal | modern |
| `--output`, `-o` | 输出路径 | 标准输出（base64 编码） |
| `--width` | 图像宽度（像素） | 800 |

## 主题风格

- **modern**：紫色/蓝色渐变背景、阴影效果、圆角设计 |
- **dark**：深色背景、浅色文字、细边框 |
- **minimal**：纯白色背景、细边框设计 |

## 示例

```bash
# Render a table
./scripts/render.sh table --data '{"columns":["Name","Score"],"rows":[["Alice","95"],["Bob","87"]]}' -o table.png

# Render a bar chart
./scripts/render.sh chart-bar --data '{"labels":["Jan","Feb","Mar"],"values":[120,150,180],"title":"Monthly Sales"}' --style dark -o chart.png

# Render stats
./scripts/render.sh stats --data '{"stats":[{"label":"Users","value":"12.5K","change":"+12%"},{"label":"Revenue","value":"$45K","change":"+8%"}]}' -o stats.png
```

## 💡 将图像发送给用户

渲染图像后，通常需要将其发送给用户。以下是推荐的工作流程：

### 推荐工作流程：
```bash
# 1. Render to ~/.openclaw/media/ (recommended path)
./scripts/render.sh table --data '...' -o ~/.openclaw/media/my-table.png

# 2. Send inline via message tool
message(action=send, filePath=/home/ubuntu/.openclaw/media/my-table.png, caption="Caption", channel=telegram, to=<user_id>)
```

### 提示：
- **将图像保存到 `~/.openclaw/media/` 目录**：该路径适用于内联显示。
- **添加描述性标题**：帮助用户理解图像内容。
- **根据需求判断**：如果用户有要求，也可以将图像保存到磁盘。

### 完整工作流程示例：
```bash
# Render
echo '{"title":"My Data","columns":["A","B"],"rows":[["1","2"]]}' | \
  ./scripts/render.sh table -o ~/.openclaw/media/data.png

# Send
message(action=send, filePath=/home/ubuntu/.openclaw/media/data.png, caption="Here's your data", channel=telegram, to=USER_ID)
```

## 所需依赖项
- `/usr/bin/wkhtmltoimage`：用于将 HTML 文件转换为图像的工具 |
- `jq`：用于解析 JSON 数据的命令行工具