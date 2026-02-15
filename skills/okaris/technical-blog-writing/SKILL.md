---
name: technical-blog-writing
description: |
  Technical blog post writing with structure, code examples, and developer audience conventions.
  Covers post types, code formatting, explanation depth, and developer-specific engagement patterns.
  Use for: engineering blogs, dev tutorials, technical writing, developer content, documentation posts.
  Triggers: technical blog, dev blog, engineering blog, technical writing, developer tutorial,
  tech post, code tutorial, programming blog, developer content, technical article,
  engineering post, coding tutorial, technical content
allowed-tools: Bash(infsh *)
---

# 技术博客写作

通过 [inference.sh](https://inference.sh) 命令行工具撰写以开发者为中心的技术博客文章。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research topic depth
infsh app run exa/search --input '{
  "query": "building REST API Node.js best practices 2024 tutorial"
}'

# Generate header image
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:630px;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;padding:60px;font-family:ui-monospace,monospace;color:white\"><div><p style=\"font-size:18px;color:#38bdf8;margin:0\">// engineering blog</p><h1 style=\"font-size:48px;margin:16px 0;font-weight:800;font-family:system-ui;line-height:1.2\">How We Reduced API Latency by 90% with Edge Caching</h1><p style=\"font-size:20px;opacity:0.6;font-family:system-ui\">A deep dive into our CDN architecture</p></div></div>"
}'
```

## 文章类型

### 1. 教程 / 操作指南

提供逐步的指导。读者应该能够按照这些指导来实际操作并完成某个任务。

```
Structure:
1. What we're building (with screenshot/demo)
2. Prerequisites
3. Step 1: Setup
4. Step 2: Core implementation
5. Step 3: ...
6. Complete code (GitHub link)
7. Next steps / extensions
```

| 规则 | 原因 |
|------|-----|
| 首先展示最终结果 | 让读者知道继续阅读是否值得 |
| 明确列出先决条件 | 避免浪费不相关读者的时间 |
| 每个代码块都必须能够运行 | 可以直接复制、粘贴并运行 |
| 不仅解释“如何做”，还要解释“为什么这样做” | 解释背后原理的教程更容易被分享 |
| 包含错误处理 | 真实代码中总会遇到错误 |
| 提供完整的代码仓库链接 | 教程结束后可供参考 |

### 2. 深度探讨 / 解释性文章

深入讲解某个概念、技术或架构决策。

```
Structure:
1. What is [concept] and why should you care?
2. How it works (simplified mental model)
3. How it works (detailed mechanics)
4. Real-world example
5. Trade-offs and when NOT to use it
6. Further reading
```

### 3. 事后分析 / 事件报告

描述问题出在哪里、原因是什么以及如何解决的。

```
Structure:
1. Summary (what happened, impact, duration)
2. Timeline of events
3. Root cause analysis
4. Fix implemented
5. What we're doing to prevent recurrence
6. Lessons learned
```

### 4. 基准测试 / 对比分析

对工具、方法或架构进行数据驱动的比较。

```
Structure:
1. What we compared and why
2. Methodology (so results are reproducible)
3. Results with charts/tables
4. Analysis (what the numbers mean)
5. Recommendation (with caveats)
6. Raw data / reproducibility instructions
```

### 5. 架构 / 系统设计

解释系统的构建方式以及做出这些决策的原因。

```
Structure:
1. Problem we needed to solve
2. Constraints and requirements
3. Options considered
4. Architecture chosen (with diagram)
5. Trade-offs we accepted
6. Results and lessons
```

## 针对开发者的写作规则

### 语言风格和语气

| 应该 | 不应该 |
|----|-------|
| 直截了当：使用“连接池” | 使用“你可以考虑使用...” |
| 承认存在的权衡 | 假装你的解决方案是完美的 |
| 使用“我们”来指代团队决策 | 使用“我独自设计了...” |
| 使用具体的数字：将 p99 响应时间从 800 毫秒缩短到 90 毫秒 | 使用“显著提升了性能” |
| 引用来源和基准测试数据 | 做出没有依据的声明 |
| 承认其他替代方案 | 假装你的方法是唯一的解决方案 |

### 开发者讨厌的内容

```
❌ "In today's fast-paced world of technology..." (filler)
❌ "As we all know..." (if we all know, why are you writing it?)
❌ "Simply do X" (nothing is simple if you're reading a tutorial)
❌ "It's easy to..." (dismissive of reader's experience)
❌ "Obviously..." (if it's obvious, don't write it)
❌ Marketing language in technical content
❌ Burying the lede under 3 paragraphs of context
```

### 代码示例

| 规则 | 原因 |
|------|-----|
| 每个代码块都必须能够运行 | 有错误的示例会破坏读者的信任 |
| 提供完整的、可运行的示例 | 没有上下文的代码片段毫无用处 |
| 在代码块中包含语言标识 | 以便语法高亮显示 |
| 在代码后展示输出/结果 | 让读者验证自己的理解是否正确 |
| 使用实际的变量名 | 使用 `calculateTotalRevenue` 而不是 `foo` |
| 在示例中包含错误处理 | 真实代码中会处理错误 |
| 明确指出依赖的版本 | 例如“兼容 React 18.2”而不是“兼容 React” |

```
Good code block format:

```python
# 这段代码的作用（一行代码）
def calculate_retry_delay(attempt: int, base_delay: float = 1.0) -> float:
    """采用指数退避算法，并加入随机抖动效果。」
    delay = base_delay * (2 ** attempt)
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter

# 使用方法
delay = calculate_retry_delay(attempt=3)  # 大约 8.0-8.8 秒
```
```

### 解释的深度

| 目标读者群体 | 解释的深度 |
|----------------|-------|
| “X 的入门指南” | 从零开始讲解，假设读者没有任何基础知识 |
| “高级 X 模式” | 跳过基础知识，深入探讨细节 |
| “X 与 Y 的比较” | 假设读者对两者都熟悉，重点讨论差异 |
| “我们是如何实现 X 的” | 面向技术读者的内容，可以省略基础部分 |

**在文章开头明确说明你假设的目标读者群体水平**：

```
"This post assumes familiarity with Docker and basic Kubernetes concepts.
If you're new to containers, start with [our intro post]."
```

## 博文结构

### 理想的结构

```markdown
# Title (contains primary keyword, states outcome)

[Hero image or diagram]

**TL;DR:** [2-3 sentence summary with key takeaway]

## The Problem / Why This Matters
[Set up why the reader should care — specific, not generic]

## The Solution / How We Did It
[Core content — code, architecture, explanation]

### Step 1: [First thing]
[Explanation + code + output]

### Step 2: [Second thing]
[Explanation + code + output]

## Results
[Numbers, benchmarks, outcomes — be specific]

## Trade-offs and Limitations
[Honest about downsides — builds trust]

## Conclusion
[Key takeaway + what to do next]

## Further Reading
[3-5 relevant links]
```

### 不同类型的文章字数要求

| 文章类型 | 字数 | 原因 |
|------|-----------|-----|
| 快速提示 | 500-800 字 | 一个概念，一个示例 |
| 教程 | 1,500-3,000 字 | 需要详细的步骤说明 |
| 深度探讨 | 2,000-4,000 字 | 全面深入的讲解 |
| 架构文章 | 2,000-3,500 字 | 需要图表来辅助说明 |
| 基准测试文章 | 1,500-2,500 字 | 需要数据和图表来支持观点 |

## 图表和可视化元素

### 何时使用图表

| 场景 | 图表类型 |
|----------|-------------|
| 请求流程 | 序列图 |
| 系统架构 | 方框箭头图 |
| 决策逻辑 | 流程图 |
| 数据模型 | 实体关系图 |
| 性能对比 | 条形图/折线图 |
| 对比前后变化 | 并排对比图 |

```bash
# Generate architecture diagram
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:600px;background:#0f172a;display:flex;align-items:center;justify-content:center;padding:40px;font-family:system-ui;color:white\"><div style=\"display:flex;gap:40px;align-items:center\"><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Client</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">React App</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #3b82f6;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Edge</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">CDN Cache</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">API</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">Node.js</p></div><div style=\"color:#64748b;font-size:32px\">→</div><div style=\"background:#1e293b;border:2px solid #334155;border-radius:8px;padding:24px;text-align:center;width:160px\"><p style=\"font-size:14px;color:#94a3b8;margin:0\">Database</p><p style=\"font-size:18px;font-weight:bold;margin:8px 0 0\">PostgreSQL</p></div></div></div>"
}'

# Generate benchmark chart
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(12, 6))\nfig.patch.set_facecolor(\"#0f172a\")\nax.set_facecolor(\"#0f172a\")\n\ntools = [\"Express\", \"Fastify\", \"Hono\", \"Elysia\"]\nrps = [15000, 45000, 62000, 78000]\ncolors = [\"#64748b\", \"#64748b\", \"#3b82f6\", \"#64748b\"]\n\nax.barh(tools, rps, color=colors, height=0.5)\nfor i, v in enumerate(rps):\n    ax.text(v + 1000, i, f\"{v:,} req/s\", va=\"center\", color=\"white\", fontsize=14)\n\nax.set_xlabel(\"Requests per second\", color=\"white\", fontsize=14)\nax.set_title(\"HTTP Framework Benchmark (Hello World)\", color=\"white\", fontsize=18, fontweight=\"bold\")\nax.tick_params(colors=\"white\", labelsize=12)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.spines[\"bottom\"].set_color(\"#334155\")\nax.spines[\"left\"].set_color(\"#334155\")\nplt.tight_layout()\nplt.savefig(\"benchmark.png\", dpi=150, facecolor=\"#0f172a\")\nprint(\"Saved\")"
}'
```

## 文章的传播方式

### 开发者阅读文章的渠道

| 平台 | 格式 | 发布方式 |
|----------|--------|-------------|
| 你的个人博客 | 完整的文章 | 主要发布渠道 |
| Dev.to | 跨平台发布（将你的博客链接作为引用） | 使用 Markdown 格式 |
| Hashnode | 跨平台发布（提供你的博客链接） | 使用 Markdown 格式 |
| Hacker News | 提供链接 | 对于项目内容可以链接到 Hacker News，对于故事内容需要手动提交 |
| Reddit（r/programming, r/webdev 等） | 提供链接或参与讨论 | 遵守相关子版块的规则 |
| Twitter/X | 发布简短总结并附上链接 | 学习如何在 Twitter 上发布文章 |
| LinkedIn | 适配后的版本并附上链接 | 学习如何在 LinkedIn 上分享内容 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 没有总结 | 忙碌的开发者可能看不完就离开了 | 在文章开头用 2-3 句话总结核心内容 |
| 代码示例有错误 | 会破坏可信度 | 发布前测试每个代码块 |
| 没有明确指出代码版本 | 代码可能在几个月后不再适用 | 明确指出代码兼容的版本 |
| 用“只需做 X”这样的表述 | 语气居高临下 | 应避免使用这类表述 |
| 架构部分没有图表 | 仅用文字描述系统结构 | 一张图表比 500 字的文字描述更有用 |
| 采用营销式的语言 | 开发者会立即失去兴趣 | 保持语言的直接性和技术性 |
| 没有讨论权衡因素 | 会让文章显得有偏见 | 必须讨论所有的优缺点 |
| 内容前有冗长的介绍 | 读者会直接跳过 | 用 2-3 段落直接切入主题 |
| 依赖版本没有固定 | 未来的读者可能无法运行代码 | 明确指出依赖的版本并注明编写日期 |
| 没有“进一步阅读”部分 | 读者无法深入了解 | 提供 3-5 个链接供读者进一步学习 |

## 相关技能

```bash
npx skills add inferencesh/skills@seo-content-brief
npx skills add inferencesh/skills@content-repurposing
npx skills add inferencesh/skills@og-image-design
```

浏览所有应用程序：`infsh app list`