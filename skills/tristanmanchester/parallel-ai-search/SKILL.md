---
name: parallel-ai-search
description: 使用 Parallel Search + Extract API 在实时网页中搜索，并从 URL（包括 PDF 文件和 JavaScript 内容较多的页面）中提取干净、适合用于大型语言模型（LLM）的文本片段（以 Markdown 格式呈现）。这些提取的文本可用于最新的研究工作、特定领域或时间范围内的信息收集（支持 `include_domains` 和 `after_date` 参数），同时还能将特定的 URL 转换为可引用的格式。
compatibility: Requires Node.js 18+ (global fetch), network access to https://api.parallel.ai, and the PARALLEL_API_KEY environment variable.
metadata:
  author: "openclaw"
  version: "1.1.1"
  homepage: "https://docs.parallel.ai/search/search-quickstart"
  openclaw: "{\"emoji\":\"🔎\",\"primaryEnv\":\"PARALLEL_API_KEY\"}"
---
# 并行AI搜索

使用此技能通过**并行搜索**（基于LLM优化的摘录）和**并行提取**（从特定URL中提取干净的Markdown内容，包括包含大量JavaScript的页面和PDF文件）来执行网络研究。

该技能遵循Agent Skills的格式：保持`SKILL.md`文件的结构简洁，并根据需要从`references/`目录加载额外细节。

## 何时使用此技能

当用户需要以下功能时，请使用此技能：

- **最新的网络研究**（“查找这个信息”、“找到最新的内容”、“最近发生了什么变化”）。
- **源代码控制**（“仅使用官方文档”、“仅限于这些域名”、“在2025-01-01之后的内容”）。
- **从URL中提取可读的摘录**（将URL或PDF转换为适合引用/引用的干净文本）。
- **可重复的研究流程**（搜索 → 筛选结果 → 提取内容 → 带有引用的回答）。

## 先决条件

- 环境中必须包含`PARALLEL_API_KEY`。
- 需要Node.js 18及以上版本（脚本依赖于内置的`fetch`函数）。

关于OpenClaw的特定设置说明，请参阅`references/openclaw-config.md`。

## 可用的脚本

使用**技能根目录下的相对路径**来运行脚本（例如：`node scripts/parallel-search.mjs ...`）。

- **`scripts/parallel-search.mjs`** — 调用并行搜索（`POST /v1beta/search`）以发现来源。
- **`scripts/parallel-extract.mjs`** — 调用并行提取（`POST /v1beta/extract`）以从URL中提取干净的摘录/Markdown内容。
- **`scripts/parallel-search-extract.mjs`** — 便捷的流程：先搜索再提取前N个结果。

提示：每个脚本默认支持`--help`、`--dry-run`选项以及JSON格式的输出。

## 工作流程（推荐）

### 1) 编写目标与查询

- 目标：用1-3句话描述问题、首选的来源类型以及任何关于内容新鲜度的要求。
- 查询：包含3-8个关键词，可以包括同义词、版本号、日期或确切的错误信息。

如果您不确定如何编写查询，请参考`references/prompting.md`中的模板。

### 2) 搜索（发现结果）

```bash
node scripts/parallel-search.mjs \
  --objective "Find official documentation explaining how X works. Prefer sources after 2025-01-01." \
  --query "X official documentation" \
  --query "X changelog 2025" \
  --max-results 8
```

然后检查`results[].url`、`results[].title`以及`results[].publish_date`（如果存在的话），并选择最合适的来源。

### 3) 提取内容（阅读）

仅提取您实际需要的URL内容：

```bash
node scripts/parallel-extract.mjs \
  --url "https://example.com/docs/x" \
  --objective "How does X work? Include the most important constraints." \
  --excerpts \
  --no-full-content
```

注意：
- 每次请求最多支持提取**10个URL**；如果传递的URL数量超过限制，脚本会自动分批处理。
- 除非确实需要全部内容，否则建议使用`--excerpts`选项。

### 4) 提供答案（附带引用）

- 尽可能使用官方或主要来源。
- 仅引用/改写您需要的摘录内容。
- 包括URL和发布日期（如果有的话），以确保透明度。
- 如果来源之间存在分歧，请同时列出所有来源并解释原因。

## 高效的使用方法

### 方法A：限定域名的研究（仅使用官方来源）

```bash
node scripts/parallel-search.mjs \
  --objective "Answer the question using official sources only." \
  --query "X authentication guide" \
  --include-domain "docs.vendor.com" \
  --include-domain "github.com" \
  --max-results 10
```

### 方法B：限制内容新鲜度

```bash
node scripts/parallel-search.mjs \
  --objective "I need the latest info; prefer sources after 2026-01-01." \
  --query "X release notes" \
  --after-date "2026-01-01" \
  --fetch-max-age-seconds 3600
```

### 方法C：一键完成搜索与提取（前3个结果）

```bash
node scripts/parallel-search-extract.mjs \
  --objective "Find the latest guidance on Y and extract citeable passages." \
  --query "Y documentation" \
  --query "Y 2026 update" \
  --max-results 8 \
  --top 3 \
  --excerpts
```

## 故障排除

### API密钥缺失/身份验证失败
- 症状：出现提示“缺少PARALLEL_API_KEY”或HTTP 401/403错误。
- 解决方法：在环境中设置`PARALLEL_API_KEY`。关于OpenClaw的详细信息，请参阅`references/openclaw-config.md`。

### 未找到合适的结果
- 增加或优化查询条件（包括同义词、产品名称、日期或确切的错误信息）。
- 使用`--include-domain`选项将来源限制在已验证的域名范围内。
- 通过`--after-date`或`--fetch-max-age-seconds`参数调整内容的新鲜度。

### 提取过程中出现超时/页面加载缓慢
- 使用`--fetch-timeout-seconds`参数延长API端的爬取超时时间。
- 如果需要更新内容，请设置`--fetch-max-age-seconds`（提取操作至少需要600秒）。
- 如果可以接受缓存内容，请取消`--disable-cache-fallback`选项。

### 在使用`npx skills add`后辅助文件丢失
- 避免使用以“_”开头的文件名（例如`scripts/_lib.mjs`）。
- 有些安装工具会排除以“_”开头的文件路径；请将辅助文件重命名为`scripts/lib.mjs`或`scripts/common.mjs`等。
- 根据需要更新所有相对导入路径。

## 参考资料（按需加载）

- `references/parallel-api.md` — 有关搜索/提取请求和响应的详细说明。
- `references/prompting.md` — 提供目标设定和查询模板。
- `references/openclaw-config.md` — OpenClaw配置信息及沙箱环境设置说明。