---
name: dataforseo-cli
description: 这是一个专为AI代理设计的、适用于大语言模型（LLM）的关键词研究命令行工具（CLI）。该工具可通过DataForSEO API查询关键词的搜索量、每次点击费用（CPC）、关键词的难度以及竞争情况，还能找到相关的关键词并分析竞争对手的排名结果。默认输出格式为TSV文件（该格式非常适合AI代理处理数据）。适用于SEO研究、内容规划或关键词竞争分析等场景。
license: MIT
metadata:
  author: alexgusevski
  version: "1.0.6"
---
# 使用 dataforseo-cli 进行关键词研究

这是一个专为大型语言模型（LLM）设计的关键词研究命令行工具，它封装了 DataForSEO API 的功能，并默认以 TSV（制表符分隔的值）格式输出结果——这种格式紧凑、结构清晰，非常适合用于自动化处理。

**npm:** https://www.npmjs.com/package/dataforseo-cli  
**GitHub:** https://github.com/alexgusevski/dataforseo-cli  

## 设置  

### 1. 通过 npm 安装  

```bash
npm install -g dataforseo-cli
```  

### 2. 检查凭据  

```bash
dataforseo-cli status
```  

如果凭据已经配置好，就可以直接使用了。如果没有，请先进行身份验证：  

```bash
# With login + password
dataforseo-cli --set-credentials login=YOUR_LOGIN password=YOUR_PASSWORD

# Or with base64 token (from DataForSEO email)
dataforseo-cli --set-credentials base64=YOUR_BASE64_TOKEN
```  

凭据存储在 `~/.config/dataforseo-cli/config.json` 文件中。`locations` 和 `languages` 命令在无需凭据的情况下也可以使用（使用本地数据）。  

## 命令  

### `status` — 检查凭据  

在不进行任何 API 调用的情况下，检查 API 凭据是否已配置。  

```bash
dataforseo-cli status
```  

如果凭据配置正确，程序会输出 0；否则输出 1。同时会显示登录用户名（不显示密码）。  

### `volume` — 关键词指标  

获取关键词的搜索量、点击成本（CPC）、关键词难度（0–100 分）、竞争程度以及 12 个月的搜索趋势。  

**参数：**  
- `<keywords...>` — 一个或多个关键词（必填）。可以通过一次调用批量查询多个关键词，以减少 API 请求次数。  

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

- `difficulty` — 难度等级（0–100 分：0-30 为简单，31-60 为中等，61-100 为困难）  
- `cpc` — 每次点击的成本（美元）  
- `competition` — 竞争程度（LOW / MEDIUM / HIGH）  
- `trend` — 过去 12 个月的搜索量（最新结果在前）  

### `related` — 相关关键词建议  

根据一个种子关键词生成相关的关键词建议。  

**参数：**  
- `<seed>` — 种子关键词（必填）  

**选项：**  
- `-l, --location <code>` — 地区代码（默认：`2840` = 美国）  
- `--language <code>` — 语言代码（默认：`en`）  
- `-n, --limit <n>` — 最大结果数量（默认：50）  
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

**参数：**  
- `<domain>` — 目标域名（必填，例如 `ahrefs.com`）  

**选项：**  
- `-l, --location <code>` — 地区代码（默认：`2840` = 美国）  
- `--language <code>` — 语言代码（默认：`en`）  
- `-n, --limit <n>` — 最大结果数量（默认：50）  
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

列出所有可用的地区代码，或按名称进行筛选。该功能无需 API 凭据即可使用。  

**参数：**  
- `[search]` — 可选参数：按名称筛选（例如 `sweden`、`new york`）  

**不使用搜索参数** — 列出所有地区代码：  
```bash
dataforseo-cli locations
```  

**使用搜索参数** — 按名称筛选地区代码：  
```bash
dataforseo-cli locations sweden
```  

**输出（TSV 格式）：**  
```
code	name	country	type
2752	Sweden	SE	Country
```  

### `languages` — 查找语言代码  

列出所有可用的语言代码，或按名称进行筛选。该功能无需 API 凭据即可使用。  

**参数：**  
- `[search]` — 可选参数：按名称筛选（例如 `sweden`、`new york`）  

**不使用搜索参数** — 列出所有语言代码：  
```bash
dataforseo-cli languages
```  

**使用搜索参数** — 按名称筛选语言代码：  
```bash
dataforseo-cli languages swedish
```  

**输出（TSV 格式）：**  
```
name	code
Swedish	sv
```  

## 输出格式  

所有数据命令默认以 TSV 格式输出（制表符分隔的值），这是对大型语言模型来说最节省令牌（即计算资源）的结构化格式。  

| 标志 | 描述 |  
|------|-------------|  
| *(默认)* | TSV — 最节省令牌的格式，适合自动化处理 |  
| `--json` | JSON 数组 | 需要结构化解析时使用 |  
| `--table` / `--human` | 人类可读的表格 | 适合人工审核 |  

## 缓存  

结果会被缓存到 `~/.config/dataforseo-cli/cache/` 目录中，以避免重复的 API 请求并节省成本。相同的查询、地区和语言组合会直接从缓存中获取结果。  

```bash
dataforseo-cli --print-cache
```  

## 工作流程：SEO 文章研究  

1. **从种子关键词开始：** `dataforseo-cli volume "你的主题"`  
2. **扩展相关关键词：** `dataforseo-cli related "你的主题" -n 30`  
3. **筛选关键词：** 选择搜索量大于 100、难度低于 60 的关键词  
4. **分析竞争对手：** `dataforseo-cli competitor competitor-domain.com -n 20`  
5. **根据最佳关键词集群撰写文章**  

## 提示：  
- 在 `volume` 命令中批量查询关键词：DataForSEO 的计费是基于每次 API 请求的，而非每个关键词。  
- 默认地区代码为美国（2840）。根据需要进行本地或国际 SEO 时，请务必设置 `--location` 参数。  
- 使用 `locations` 和 `languages` 命令查看所有可用选项。  
- 关键词难度等级：0-30 表示简单，31-60 表示中等，61-100 表示困难。