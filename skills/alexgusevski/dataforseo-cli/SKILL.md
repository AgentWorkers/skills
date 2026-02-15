---
name: dataforseo-cli
description: 专为AI代理设计的、支持大型语言模型（LLM）的关键词研究命令行工具。通过DataForSEO API查询关键词的搜索量、每次点击费用（CPC）、关键词难度以及竞争情况；能够找到相关关键词并分析竞争对手的排名。默认输出格式为TSV文件（专为AI代理的工作流程优化）。适用于SEO研究、内容规划或竞争性关键词分析等场景。
license: MIT
metadata:
  author: alexgusevski
  version: "1.0.0"
---

# 使用 dataforseo-cli 进行关键词研究

这是一个专为大型语言模型（LLM）设计的关键词研究命令行工具，它封装了 DataForSEO API 的功能，并默认输出 TSV 格式的数据——这种格式紧凑、结构清晰，非常适合用于自动化处理。

## 设置

### 1. 通过 npm 安装

```bash
npm install -g dataforseo-cli
```

### 2. 认证

在运行任何数据相关命令之前，请先配置您的 DataForSEO API 凭据：

```bash
# With login + password
dataforseo-cli --set-credentials login=YOUR_LOGIN password=YOUR_PASSWORD

# Or with base64 token (from DataForSEO email)
dataforseo-cli --set-credentials base64=YOUR_BASE64_TOKEN
```

凭据存储在 `~/.config/dataforseo-cli/config.json` 文件中。

要验证凭据是否已正确设置，请检查该文件是否存在：
```bash
cat ~/.config/dataforseo-cli/config.json
```

如果凭据缺失或无效，API 命令（如 `volume`、`related`、`competitor`）将无法正常执行。而 `locations` 和 `languages` 命令则无需凭据即可使用（使用本地数据）。

## 命令

### `volume` — 关键词指标

获取关键词的搜索量、点击成本（CPC）、关键词难度（0–100）、竞争程度以及 12 个月的搜索趋势。

```bash
dataforseo-cli volume <keywords...> [options]
```

**参数：**
- `<keywords...>` — 一个或多个关键词（必填）。可以通过多次调用合并多个关键词以减少 API 请求次数。

**选项：**
- `-l, --location <code>` — 地区代码（默认：`2840` = 美国）
- `--language <code>` — 语言代码（默认：`en`）
- `--json` — 以 JSON 数组形式输出
- `--table` / `--human` — 以人类可读的表格形式输出

**示例：**
```bash
dataforseo-cli volume "seo tools" "keyword research" "backlink checker"
```

**输出（TSV 格式）：**
```
keyword	volume	cpc	difficulty	competition	trend
seo tools	12500	2.35	45	HIGH	14800,13900,12500,12100,11800,12000,12500,13000,12800,12500,12200,11900
```

- `difficulty` — 难度等级（0-100：0-30 为简单，31-60 为中等，61-100 为困难）
- `cpc` — 每次点击的费用（美元）
- `competition` — 竞争程度（LOW / MEDIUM / HIGH）
- `trend` — 近 12 个月的搜索量（最新数据在前）

### `related` — 相关关键词建议

根据一个种子关键词生成相关关键词建议。

```bash
dataforseo-cli related <seed> [options]
```

**参数：**
- `<seed>` — 种子关键词（必填）

**选项：**
- `-l, --location <code>` — 地区代码（默认：`2840` = 美国）
- `--language <code>` — 语言代码（默认：`en`）
- `-n, --limit <n>` — 最多结果数量（默认：50）
- `--json` — 以 JSON 数组形式输出
- `--table` / `--human` — 以人类可读的表格形式输出

**示例：**
```bash
dataforseo-cli related "ai agents" -n 20
```

**输出（TSV 格式）：**
```
keyword	volume	cpc	competition	difficulty
best ai agents	8100	3.10	0.82	52
ai agent framework	2400	1.85	0.65	38
```

### `competitor` — 域名关键词分析

查看某个域名当前在哪些关键词上排名较高。

```bash
dataforseo-cli competitor <domain> [options]
```

**参数：**
- `<domain>` — 目标域名（必填，例如 `ahrefs.com`）

**选项：**
- `-l, --location <code>` — 地区代码（默认：`2840` = 美国）
- `--language <code>` — 语言代码（默认：`en`）
- `-n, --limit <n>` — 最多结果数量（默认：50）
- `--json` — 以 JSON 数组形式输出
- `--table` / `--human` — 以人类可读的表格形式输出

**示例：**
```bash
dataforseo-cli competitor semrush.com -n 10
```

**输出（TSV 格式）：**
```
keyword	position	volume	cpc	difficulty	url
backlink checker	1	33100	4.50	72	https://ahrefs.com/backlink-checker
```

### `locations` — 查找地区代码

列出所有可用的地区代码，或按名称进行筛选。此功能无需 API 凭据即可使用。

**参数：**
- `[search]` — 可选参数，用于按名称筛选（例如 `sweden`、`new york`）

**不使用搜索参数** — 列出所有地区：
```bash
dataforseo-cli locations
```

**使用搜索参数** — 按名称筛选：
```bash
dataforseo-cli locations sweden
```

**输出（TSV 格式）：**
```
code	name	country	type
2752	Sweden	SE	Country
```

### `languages` — 查找语言代码

列出所有可用的语言代码，或按名称进行筛选。此功能无需 API 凭据即可使用。

**参数：**
- `[search]` — 可选参数，用于按名称筛选（例如 `sweden`、`new york`）

**不使用搜索参数** — 列出所有语言：
```bash
dataforseo-cli languages
```

**使用搜索参数** — 按名称筛选：
```bash
dataforseo-cli languages swedish
```

**输出（TSV 格式）：**
```
name	code
Swedish	sv
```

## 输出格式

所有数据命令默认输出 TSV（制表符分隔的值）格式——这是对大型语言模型来说最节省令牌（即计算资源）的结构化格式。

| 标志 | 描述 |
|------|-------------|
| *(默认)* | TSV — 最节省令牌的格式，适合自动化处理 |
| `--json` | JSON 数组 — 适用于需要结构化解析的情况 |
| `--table` / `--human` | 以人类可读的表格形式输出 |

## 缓存

结果会被缓存到 `~/.config/dataforseo-cli/cache/` 目录中，以避免重复调用 API 从而节省成本。相同的查询、地区和语言组合会直接从缓存中获取结果。

```bash
dataforseo-cli --print-cache
```

## SEO 文章研究工作流程：

1. **从种子关键词开始：`dataforseo-cli volume "your topic"`
2. **扩展相关关键词：`dataforseo-cli related "your topic" -n 30`
3. **筛选关键词：`dataforseo-cli competitor competitor-domain.com -n 20`
4. **根据最佳关键词群组撰写文章**

## 提示：
- 在 `volume` 命令中批量输入关键词——DataForSEO 的费用是按 API 请求计费的，而非按关键词计费。
- 默认地区设置为美国（代码 `2840`）。如需针对特定地区或国际市场进行 SEO，请务必设置 `--location` 参数。
- 可使用 `locations` 和 `languages` 命令查看所有可用的选项。
- 关键词难度等级：0-30 表示简单，31-60 表示中等，61-100 表示困难。