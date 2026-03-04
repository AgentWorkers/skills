---
name: deep-scout
description: "多阶段深度智能处理流程（搜索 → 过滤 → 获取 → 合成）。该流程将用户输入的查询转化为一份包含完整来源引用的结构化研究报告。"
version: "0.1.4"
metadata:
  {"openclaw": {"requires": {"bins": ["bash", "python3"], "anyBins": ["timeout", "gtimeout"]}}}
---
# deep-scout

这是一个多阶段的深度智能处理流程（搜索 → 过滤 → 获取 → 合成）。

## 🛠️ 安装

### 1. 使用 OpenClaw（推荐）
告诉 OpenClaw：“安装 deep-scout 技能”。代理将自动处理安装和配置。

### 2. 手动安装（通过 CLI）
如果您更喜欢使用终端，请运行以下命令：
```bash
clawhub install deep-scout
```

## 🚀 使用方法

```
/deep-scout "Your research question" [--depth 5] [--freshness pw] [--country US] [--style report]
```

### 参数说明
| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--depth N` | 5 | 需要完全获取的 URL 数量（1–10） |
| `--freshness` | `pw` | `pd`=过去一天，`pw`=过去一周，`pm`=过去一个月，`py`=过去一年 |
| `--country` | `US` | Brave 搜索时使用的国家代码（2 个字母） |
| `--language` | `en` | 语言代码（2 个字母） |
| `--search-count` | 8 | 过滤前的总结果数量 |
| `--min-score` | 4 | 保留的最小相关性得分（0–10） |
| `--style` | `report` | `report` \| `comparison` \| `bullets` \| `timeline` | 报告格式 |
| `--dimensions` | `auto` | 比较维度（用逗号分隔，适用于 `--style comparison`） |
| `--output FILE` | stdout | 将报告写入文件 |
| `--no-browser` | — | 禁用浏览器回退机制 |
| `--no-firecrawl` | — | 禁用 Firecrawl 回退机制 |

---

## 🛠️ 流程 — 代理执行步骤

当调用此技能时，将执行以下四个阶段的流程：

---

### 第 1 阶段：搜索
使用 `web_search` 进行搜索：
```
query: <user query>
count: <search_count>
country: <country>
search_lang: <language>
freshness: <freshness>
```

收集每个搜索结果的标题、URL 和摘要。  
如果返回的结果少于 3 个，尝试使用 `freshness: "py"` 重新搜索（放宽搜索条件）。

---

### 第 2 阶段：过滤
加载 `prompts/filter.txt` 文件，并替换其中的模板变量：
- `{{query}}` → 用户的搜索查询 |
- `{{freshness}}` → 新鲜度参数 |
- `{{min_score}}` → 最小相关性得分参数 |
- `{{results_json}}` → 搜索结果的 JSON 数组 |

使用该查询提示调用大型语言模型（LLM），解析返回的 JSON 数组。  
仅保留 `keep: true` 的结果，并按得分降序排序。  
选择排名前 `depth` 位的 URL 列出作为获取目标。

**去重处理：** 每个根域名最多保留 2 个结果（已在过滤步骤中处理）。

---

### 第 3 阶段：获取数据（分层次处理）
对于过滤后的 URL 列表中的每个 URL：

**第 1 层 — web_fetch（快速获取）：**
```
Call web_fetch(url)
If content length >= 200 chars → accept, trim to max_chars_per_source
```

**第 2 层 — Firecrawl（深度获取/JavaScript 数据）：**
```
If Tier 1 fails or returns < 200 chars:
  Run: scripts/firecrawl-wrap.sh <url> <max_chars>
  If output != "FIRECRAWL_UNAVAILABLE" and != "FIRECRAWL_EMPTY" → accept
```

**第 3 层 — 浏览器（最后手段）：**
```
If Tier 2 fails:
  Call browser(action="open", url=url)
  Call browser(action="snapshot")
  Load prompts/browser-extract.txt, substitute {{query}} and {{max_chars_per_source}}
  Call LLM with snapshot content + extraction prompt
  If output != "FETCH_FAILED:..." → accept
```

**如果所有层次都失败：** 使用第 1 阶段搜索结果中的原始摘要，并标记为 `[snippet only]`。**

将数据存储为 `{ url: extracted_content }` 的字典格式。

---

### 第 4 阶段：合成报告
根据 `--style` 参数选择报告模板：
- `report` / `bullets` / `timeline` → 使用 `prompts/synthesize-report.txt` 模板生成报告 |
- `comparison` → 使用 `prompts/synthesize-comparison.txt` 模板生成对比报告 |

替换模板变量：
- `{{query}}` → 用户的搜索查询 |
- `{{today}}` → 当前日期（YYYY-MM-DD） |
- `{{language}}` → 语言参数 |
- `{{source_count}}` → 成功获取的数据源数量 |
- `{{dimensions_or_auto}}` | 维度参数（或 "auto"） |
- `{{fetched_content_blocks}}` | 获取的数据内容 |

使用填充好的参数调用大型语言模型生成最终报告。  
如果设置了 `--output FILE`，则将报告写入指定文件；否则，将报告输出到控制台。

---

## ⚙️ 配置
默认配置位于 `config.yaml` 文件中。可以通过上述 CLI 参数进行覆盖。

---

## 📂 项目结构

```
skills/deep-scout/
├── SKILL.md                     ← This file (agent instructions)
├── config.yaml                  ← Default parameter values
├── prompts/
│   ├── filter.txt               ← Stage 2: relevance scoring prompt
│   ├── synthesize-report.txt    ← Stage 4: report/bullets/timeline synthesis
│   ├── synthesize-comparison.txt← Stage 4: comparison table synthesis
│   └── browser-extract.txt      ← Stage 3: browser snapshot extraction
├── scripts/
│   ├── run.sh                   ← CLI entrypoint (emits pipeline actions)
│   └── firecrawl-wrap.sh        ← Firecrawl CLI wrapper with fallback handling
└── examples/
    └── openclaw-acquisition.md  ← Example output: OpenClaw M&A intelligence
```

---

## 🔧 错误处理
| 错误情况 | 处理方式 |
|----------|----------|
| 所有获取尝试均失败 | 使用第 1 阶段的摘要；标记为 `[snippet only]` |
| 搜索返回 0 个结果 | 重新尝试使用 `freshness: py`；如果仍然没有结果，则报错 |
| 未安装 Firecrawl | `firecrawl-wrap.sh` 输出 `FIRECRAWL_UNAVAILABLE`，并静默跳过该步骤 |
| 浏览器工具不可用 | 跳过第 3 阶段；使用可用的数据继续处理 |
| 大型语言模型生成的内容超出上下文限制 | 按比例裁剪数据源，优先选择得分较高的数据源 |
| Brave API 的请求速率限制 | 等待 2 秒后重试一次 |

---

## 📋 示例输出
完整的报告示例请参见 `examples/openclaw-acquisition.md`。

---

*Deep Scout v0.1.0 · OpenClaw 技能 · clawhub: deep-scout*