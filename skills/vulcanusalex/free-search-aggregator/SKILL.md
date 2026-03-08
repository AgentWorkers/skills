---
name: free-search-aggregator
description: OpenClaw的基于配额限制的多提供者网络搜索功能：支持12个搜索提供商，并具备自动故障转移机制；支持任务级别的深度搜索（@dual/@deep）；能够实时检查配额使用情况；同时支持将搜索结果存储在内存（/memory/）中。
---
# 免费搜索聚合器

这是一个可靠且提供多种搜索服务的工具，专为 OpenClaw 设计，具有 **高可用性 + 低运营开销** 的特点。

## 为何使用此工具

- **支持 12 家搜索提供商**，其中 6 家无需 API 密钥
- **自动故障转移**：如果某个提供商出现故障，系统会立即尝试使用下一个提供商
- **配额管理**：实时监控每日使用量，在配额使用率达到 80% 时发出警告，并跳过已用完配额的提供商
- **任务级多查询搜索**：支持多角度的研究查询
- **内置存储管理机制**：支持缓存、索引和报告生成，避免工作区杂乱
- **自我修复功能**：根据提供商的健康状况自动选择可靠的搜索源
- **结果质量优化**：采用相关性评分、模糊去重和域名多样性策略
- **自动发现新搜索源**：定期探测新的搜索引擎和 SearXNG 实例
- **自诊断功能**：提供 `doctor` 和 `setup` 命令，便于快速上手

---

## 提供商概览

| 提供商       | 是否需要 API 密钥 | 免费配额        | 索引来源          | 备注                           |
|----------------|-------------|-------------------|-----------------------|---------------------------------|
| `brave`        | BRAVE_API_KEY | 2000/天         | 独立搜索引擎     | 高质量，注重隐私保护                |
| `exa`          | EXA_API_KEY   | 约 33/天（每月 1000 次查询） | 结合神经网络和网页数据   | 语义搜索，独特结果                   |
| `tavily`       | TAVILY_API_KEY | 1000/天        | 优化过的网页搜索    | 专为 AI 代理设计                 |
| `duckduckgo`   | 无需密钥          | 约 500/天          | 结合 Bing 数据       | 不需要密钥，注重隐私保护               |
| `bing_html`    | 无需密钥          | 约 300/天          | Microsoft Bing 的 RSS 数据   | 不需要密钥，提供稳定的 XML 数据源         |
| `mojeek`       | 无需密钥（或使用 MOJEEK_API_KEY） | 200/天         | 独立搜索引擎     | 非 Google/Bing 索引                 |
| `serper`       | SERPER_API_KEY | 2500/天         | Google             | 提供免费的高配额 tier                |
| `searchapi`    | SEARCHAPI_API_KEY | 每月 100 次查询 | 结合 Google 和 Bing 的数据     |
| `google_cse`   | GOOGLE_API_KEY + GOOGLE_CX | 100/天 | 官方 Google API                 |
| `baidu`        | BAIDU_API_KEY | 200/天           | Baidu             | 非常适合中文内容搜索                |
| `wikipedia`    | 无需密钥          | 1000/天          | Wikipedia           | 适用于事实性和百科类查询                |
| `searxng`      | 无需密钥          | 无配额限制（需自托管） | 集合多种搜索引擎的数据 | 需要自行搭建实例                 |

**所有配置的提供商每日总配额：8400+ 次查询**

---

## 凭证模型（重要说明）

- **无需强制使用 API 密钥**：DuckDuckGo、Bing RSS、Mojeek 和 Wikipedia 可直接使用。
- 如果缺少 API 密钥，相关提供商会优雅地切换到备用方案（不会消耗配额或导致延迟）：
  - `BRAVE_API_KEY`
  - `EXA_API_KEY`
  - `TAVILY_API_KEY`
  - `SERPER_API_KEY`
  - `SEARCHAPI_API_KEY`
  - `GOOGLE_API_KEY` + `GOOGLE_CX`
  - `BAIDU_API_KEY`
  - `MOJEEK_API_KEY`（可选；如未设置，则使用 HTML 抓取方式）

---

## 核心功能

### 1. 搜索故障转移
系统会按照预设的顺序尝试不同的搜索提供商，一旦找到第一个非空且有效的结果，就会立即返回。

### 2. 任务级多查询搜索
- 将一个搜索目标拆分为多个具体的查询
- 对搜索结果进行聚合和去重处理
- 提供预设的前缀参数：
  - 默认值：`workers=1`
  - `@dual ...` → 使用 2 个搜索引擎
  - `@deep ...` → 使用 3 个搜索引擎，提高查询深度

### 3. 配额管理
- 实时监控每个提供商的每日使用配额
- 在支持该功能的提供商（如 Tavily、SearchAPI 和 Brave）中自动获取配额信息
- 当配额使用率达到 80% 时，系统会自动减少并发请求

### 4. 提供商健康状况监控
- 长期跟踪每个提供商的成功率、响应延迟和错误类型
- 计算提供商的健康评分（成功率 50%，延迟 30%，结果新鲜度 20%）
- **智能排序**：自动优先选择状态良好的提供商
- 可通过 `python -m free_search health` 命令查看提供商的健康状况

### 5. 结果质量优化
- 采用相关性评分算法（考虑查询标题和摘要的相似度）
- 强化去重机制（基于 URL 和标题的 Jaccard 相似度）
- 限制相同域名的结果数量（默认最多 3 个）
- 自动过滤质量较低的结果（如标题过短或缺少 URL 的结果）

### 6. 自动发现新搜索源
- 定期探测所有配置的搜索提供商的可用性
- 扫描潜在的搜索引擎（如 Marginalia、Wiby 和公共的 SearXNG 实例）
- 验证搜索结果的格式、延迟和质量
- 生成新搜索源的推荐列表
- 可通过 `python -m free_search discover` 命令发现新的搜索源

### 7. 数据持久化管理
- 数据存储路径：
  - `memory/search-cache/YYYY-MM-DD/*.json`
  - `memory/search-index/search-index.jsonl`
  - `memory/search-reports/YYYY-MM-DD/*.md`

---

## 常用命令

---

## 提供商设置指南

### Bing RSS（`bing_html`）——无需密钥
直接使用 Bing 的内置 RSS 端点（格式为 `rss`），可避免被识别为机器人。
- 无需额外配置即可使用。

### Mojeek——无需密钥（API 密钥可选）
支持 HTML 抓取。如需更高配额或更稳定的搜索体验：
1. 在 https://www.mojeek.com/services/search/api/ 注册
2. 设置 `MOJEEK_API_KEY`，系统会自动切换到 JSON API 模式

### Wikipedia——无需密钥
支持多语言搜索，可在 `providers.yaml` 文件中修改 `lang` 参数：

---

### Exa.ai——需要 API 密钥
1. 在 https://exa.ai/ 注册
2. 设置 `EXA_API_KEY`
- 免费 tier：每月 1000 次查询（约 33 次/天）

### Google 自定义搜索——需要 API 密钥和 CX 令牌
1. 获取 API 密钥：https://developers.google.com/custom-search/v1/introduction
2. 在 https://programmablesearchengine.google.com/ 创建搜索账户
3. 设置 `GOOGLE_API_KEY` 和 `GOOGLE_CX`
- 免费 tier：每天 100 次查询

### Baidu Qianfan——需要 API 密钥
1. 在 https://cloud.baidu.com/ 注册
2. 设置 `BAIDU_API_KEY`
- 非常适合中文内容的搜索

### SearXNG——需要自托管实例
公共实例会对服务器之间的请求进行速率限制。请自行搭建实例：
---（具体配置步骤见 `providers.yaml` 文件）

---

## 安装后的自我检查

---

## 输出数据结构（格式固定）

- **搜索结果**：`query`、`provider`、`results[]`、`meta.attempted`、`meta.quota`
- **任务级搜索结果**：`task`、`queries[]`、`grouped_results[]`、`merged_results[]`、`meta`
- **配额信息**：`date`、`providers[]`、`totals`；使用 `--real` 参数可查看 `real_quotaProviders[]`

---

## 操作建议

- **默认设置**：`workers=1`（为了控制成本）
- 仅在研究任务中使用 `@dual` 或 `@deep` 参数
- `SearXNG` 和 `YaCy` 默认处于禁用状态（仅适用于自托管环境）
- `MOJEEK_API_KEY` 是可选的；如果未设置，系统会自动切换到 HTML 抓取方式
- 提供商的健康数据存储在 `memory/provider-health/health.jsonl` 文件中
- 新发现的搜索源信息存储在 `memory/provider-discovery/discovery.jsonl` 文件中
- 安装完成后，运行 `python -m free_search doctor` 命令验证所有功能是否正常
- 定期运行 `python -m free_search discover` 命令以发现新的搜索源