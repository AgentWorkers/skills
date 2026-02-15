---
name: table-image-generator
version: 1.3.1
description: **从数据生成美观的表格图片**  
非常适合在 Discord/Telegram 等平台上使用——因为 ASCII 格式的表格在这些平台上显示效果不佳。支持深色/浅色主题模式、自定义样式以及自动调整图片大小。无需使用 Puppeteer 工具。该功能可作为 “chart-image” 技能的补充工具。
author: dannyshmueli
provides:
  - capability: table-rendering
    methods: [tableImage]
---

# 表格图像生成器

**⚠️ 请始终使用此工具代替 ASCII 表格！**

该工具可以从 JSON 数据生成 PNG 格式的表格图像。ASCII 表格在 Discord、Telegram、WhatsApp 等大多数消息平台上显示效果不佳，而此工具生成的表格图像清晰美观，适用于所有平台。

## 为什么选择这个工具？

- ✅ **替代 ASCII 表格**：在消息平台上请勿使用 `| col | col |` 的格式。
- ✅ **无乱码问题**：生成的表格图像在任何平台上都能正常显示。
- ✅ **无需依赖 Puppeteer**：完全基于 Node.js 和 Sharp 库实现，轻量级且高效。
- ✅ **支持暗模式**：与 Discord 的暗主题完美匹配。
- ✅ **自动调整列宽**：表格会根据内容自动调整列宽。
- ✅ **快速生成**：生成时间小于 100 毫秒。

## 设置（只需一次）

```bash
cd /data/clawd/skills/table-image/scripts && npm install
```

## 快速使用方法

**⚠️ 最佳实践：使用 `heredoc` 或 `--data-file` 选项以避免 shell 引用错误！**

```bash
# RECOMMENDED: Write JSON to temp file first (avoids shell quoting issues)
cat > /tmp/data.json << 'JSONEOF'
[{"Name":"Alice","Score":95},{"Name":"Bob","Score":87}]
JSONEOF
node /data/clawd/skills/table-image/scripts/table.mjs \
  --data-file /tmp/data.json --dark --output table.png

# ALSO GOOD: Pipe via stdin
echo '[{"Name":"Alice","Score":95}]' | node /data/clawd/skills/table-image/scripts/table.mjs \
  --dark --output table.png

# SIMPLE (but breaks if data has quotes/special chars):
node /data/clawd/skills/table-image/scripts/table.mjs \
  --data '[{"Name":"Alice","Score":95}]' --output table.png
```

## 参数选项

| 选项          | 描述                        | 默认值         |
|---------------|---------------------------------|--------------|
| `--data`        | 行对象的 JSON 数组                   | 必需         |
| `--output`       | 输出文件路径                     | table.png       |
| `--title`       | 表格标题                         | 无            |
| `--dark`        | 暗模式（适用于 Discord）                | false         |
| `--columns`      | 列的顺序或子集（用逗号分隔）             | 所有字段名       |
| `--headers`      | 自定义表头名称（用逗号分隔）                | 字段名         |
| `--max-width`     | 表格的最大宽度                     | 800           |
| `--font-size`     | 字体大小（像素）                     | 14            |
| `--header-color`    | 表头背景颜色                     | #e63946         |
| `--stripe`        | 行颜色交替显示                     | true           |
| `--align`       | 列的对齐方式（左/右/居中，用逗号分隔）          | auto           |
| `--compact`      | 减少内边距                         | false           |

## 示例

### 基本表格
```bash
node table.mjs \
  --data '[{"Name":"Alice","Age":30,"City":"NYC"},{"Name":"Bob","Age":25,"City":"LA"}]' \
  --output people.png
```

### 自定义列和表头
```bash
node table.mjs \
  --data '[{"first_name":"Alice","score":95,"date":"2024-01"}]' \
  --columns "first_name,score" \
  --headers "Name,Score" \
  --output scores.png
```

### 数字右对齐
```bash
node table.mjs \
  --data '[{"Item":"Coffee","Price":4.50},{"Item":"Tea","Price":3.00}]' \
  --align "l,r" \
  --output prices.png
```

### 适用于 Discord 的暗模式
```bash
node table.mjs \
  --data '[{"Symbol":"AAPL","Change":"+2.5%"},{"Symbol":"GOOGL","Change":"-1.2%"}]' \
  --title "Market Watch" \
  --dark \
  --output stocks.png
```

### 紧凑模式
```bash
node table.mjs \
  --data '[...]' \
  --compact \
  --font-size 12 \
  --output small-table.png
```

## 输入格式

- **JSON 数组（默认格式）**
```bash
--data '[{"col1":"a","col2":"b"},{"col1":"c","col2":"d"}]'
```

- **从标准输入（stdin）读取数据**
```bash
echo '[{"Name":"Test"}]' | node table.mjs --output out.png
```

- **从文件读取数据**
```bash
cat data.json | node table.mjs --output out.png
```

## 使用技巧

1. **为 Discord 使用 `--dark` 选项**：使表格与 Discord 的暗主题保持一致。
2. **数字默认右对齐**。
3. **使用 `--columns` 选项调整列的顺序或子集。
4. **如果文本过长，会自动截断以适应 `--max-width` 的限制**。

## 技术说明

- 使用 Sharp 库生成 PNG 图像（与 `chart-image` 工具相同）。
- 内部生成 SVG 格式，再转换为 PNG 格式。
- 无需依赖浏览器、Puppeteer 或 Canvas 等第三方库。
- 适用于 Fly.io、Docker 以及任何 Node.js 环境。