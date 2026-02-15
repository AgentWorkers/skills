---
name: kirk-content-pipeline
description: >
  根据 KSVC 的验证标准，从研究 PDF 文件中生成适合在 Twitter 上发布的文本内容。内容类型包括：长篇帖子、简短总结、突发新闻、搞笑帖子、个人评论等。触发条件包括：执行“create content”、“write thread”、“make a post”命令，或者在 /Users/Shared/ksvc/pdfs 目录下处理 PDF 文件时。所需步骤如下：  
  (1a) 选择合适的工具来扫描 PDF 文件；  
  (1b) 使用 RLM 进行深度内容提取；  
  (1c) 结合 rlm-multi 工具进行跨文档内容整合；  
  (2) 对提取的内容进行初步的 KSVC 标准验证；  
  (3) 构建数据框架；  
  (4a) 使用 RLM 对内容进行审核；  
  (4a.5) 通过 Gemini 网络服务对内容进行二次验证（检查内容是否可靠或来源不明）；  
  (4b) 对所有模型生成的结果进行最终验证；  
  (4c) 使用 kirk-mode 工具对内容进行格式化处理；  
  (4d) 由人工审核员对内容进行质量检查；  
  (5) 保存草稿；  
  (6) 根据审核结果生成最终发布的推文。
---
# Kirk内容管道

根据分析师研究PDF创建Twitter内容，并与KSVC的持股情况进行了验证。

## 管道步骤（必须执行）

```
1a.   Scan PDFs (Explore agents for broad screening)
1b.   Extract insights (RLM for deep extraction - text, tables, AND charts)
1c.   Cross-doc synthesis (rlm-multi for insights across sources)
2.    Check KSVC holdings (preliminary - with known tickers)
3.    Write content (data backbone, Serenity-heavy)
4a.   AUDIT (verify draft claims against source PDFs with RLM)
4a.5. GEMINI CROSS-VALIDATION (web-verify FAIL/UNSOURCED inferences)
4b.   Final Holdings Verification (check ALL 7 models with discovered tickers)
4c.   Stylize (invoke kirk-mode skill for voice/character)
4d.   Humanize (remove AI patterns)
5.    Save draft for approval
6.    Chart decision & generation (after draft crystallizes thesis)
7.    PUBLISH to final folder (clean version for posting)
```

**请勿跳过步骤4a-4d。使用1a进行多PDF筛选，使用1b进行深度提取，使用1c进行跨文档综合，使用4a进行验证，使用4a.5进行网络交叉验证，使用4b进行最终持股检查，使用4c进行人物风格调整。**

**⚠️ 重要提示：**步骤1b用于提取数据；步骤1c用于跨文档综合；步骤4a用于验证文本内容；步骤4a.5用于网络交叉验证。**

**步骤1b：**每份PDF讲述了什么？**
**步骤1c：**不同PDF中出现了哪些共同点？**
**步骤4a：**我的草稿是否准确反映了来源信息？**
**步骤4a.5：**标记出的推断是否在公开来源中得到验证？**
**步骤4c：**哪种Kirk风格适合这种情况？**

---

## 子代理权限（重要）

**子代理******不得读取项目目录之外的文件。**`/Users/Shared/ksvc/pdfs/`中的PDF被禁止访问。**解决方法是在启动子代理之前，将PDF创建符号链接到项目目录中。

**主代理******必须在步骤1a之前创建符号链接：**
```bash
ln -sf "/Users/Shared/ksvc/pdfs/YYYYMMDD" ".claude/pdfs-scan"
```

这样子代理就可以从`.claude/pdfs-scan/filename.pdf`中读取文件——因为路径是在项目内部解析的。

| 访问方法 | `/Users/Shared/` 路径 | 符号链接后的项目路径 |
|--------------|----------------------|----------------------|
| 子代理读取工具（PDF） | ❌ 自动拒绝 | ✅ 可以读取 |
| 子代理读取工具（图片） | ❌ 自动拒绝 | ✅ 可以读取 |
| 主代理读取工具 | ✅ 用户批准 | ✅ 可以读取 |
| Bash → RLM | ✅ 任何路径 | ✅ 任何路径 |

**2026-02-07发现的问题：**子代理在尝试访问`/Users/Shared/`路径时遇到“读取权限被自动拒绝”错误。将PDF创建符号链接到项目目录可以解决此问题。测试了19份PDF，详细程度中等，共125,000个标记，没有出现错误。**

---

## 内容类型与风格混合

**完整指南：**`references/kirk-voice.md` —— 请参阅此文件以获取模板和示例。

Kirk的风格 = Serenity的数据 + Citrini7的简洁表达 + Jukan的怀疑态度 + Zephyr的活力。

| 类型 | 适用场景 | 风格混合 | 关键要素 |
|------|------|-------|-------------|
| **长篇分析** | 深度挖掘，多来源信息 | Serenity + Jukan | 简洁总结 + 怀疑态度 |
| **快速总结** | 单一观点，一份报告 | Citrini7 + Serenity | 简洁明了 + 一个数字 |
| **突发新闻** | 新闻发布时 | Zephyr + Jukan | 反应性语言 + 数字 |
| **搞笑帖子** | 市场荒谬内容 | Citrini7 + Zephyr | 模因格式 |
| **个人评论** | 观点表达，疑问提出 | 纯粹使用Jukan的风格 | 采用第一人称 + 表达不确定性 |

## 快速公式

**长篇分析：** 引入 → 简洁总结 → 数字 → 怀疑态度 → 立场表达 |

**快速总结：** 标题数字 → 背景信息 → “如果你现在正在看...” |

**突发新闻：** “非常重大。” / “好吧好吧...” → 关键数字 → 来源信息 |

**胜利总结：** “自KSVC发布以来，$TICKER上涨了X%” → 发布内容 + 当前情况 |

---

## 步骤1a：使用Explore代理扫描PDF

当你有很多PDF需要审核时，使用Explore代理进行**初步筛选**。这比RLM更快，有助于快速发现内容。

### 步骤1a.0：检查已发布的帖子（必须执行）

```
1a.   Scan PDFs (Explore agents for broad screening)
1b.   Extract insights (RLM for deep extraction - text, tables, AND charts)
1c.   Cross-doc synthesis (rlm-multi for insights across sources)
2.    Check KSVC holdings (preliminary - with known tickers)
3.    Write content (data backbone, Serenity-heavy)
4a.   AUDIT (verify draft claims against source PDFs with RLM)
4a.5. GEMINI CROSS-VALIDATION (web-verify FAIL/UNSOURCED inferences)
4b.   Final Holdings Verification (check ALL 7 models with discovered tickers)
4c.   Stylize (invoke kirk-mode skill for voice/character)
4d.   Humanize (remove AI patterns)
5.    Save draft for approval
6.    Chart decision & generation (after draft crystallizes thesis)
7.    PUBLISH to final folder (clean version for posting)
```

**⚠️ 在扫描任何PDF之前，请先查看Kirk已经发布了哪些内容。**

```bash
# List all published threads
ls /Users/Shared/ksvc/threads/

# Read recent thread.md files to understand what topics are covered
```

对于每个已发布的帖子，请记录：
- **主题**（论点是什么？）
- **使用的来源PDF**（查看 `_metadata.md`）
- **日期**（更新程度如何？）

**然后在选择主题时，拒绝以下任何主题：**
- 使用与已发布帖子相同的原始来源PDF
- 涉及相同论点/角度（即使来自不同来源）
- 会让Kirk的粉丝觉得重复

**允许的重叠情况：**
- 对之前帖子的跟进/更新，包含新数据（例如，收益确认了论点）
- 对同一行业的不同角度的报道（例如，之前报道了ABF的短缺情况，现在报道了特定公司的收益）
- 明确标注为“更新：自我上次发布以来发生了哪些变化”

**为什么会有这个步骤（案例研究——ABF基板，2026-02-07）：**

Kirk在2月5日发布了一条包含10条推文的帖子，讨论了高盛关于ABF短缺的报告（从10%增加到21%，Kinsus/NYPCB/Unimicron）。2月7日，管道使用了相同的高盛报告，生成了一条包含相同数字、相同公司和相同角度的3条推文。如果我们没有先查看已发布的帖子，就会在有其他10个新鲜主题角度的情况下浪费了一次管道运行时间。**

---

## 何时使用
- 筛选10份以上的PDF以找到相关内容
- 寻找跨文档之间的联系
- 从多个来源构建论点
- 尚不清楚哪些PDF重要

## 如何扫描
```
1. Check published threads (Step 1a.0 above)

2. List recent PDF folders and count PDFs
   ls /Users/Shared/ksvc/pdfs/ | tail -5
   ls /Users/Shared/ksvc/pdfs/YYYYMMDD/ | wc -l

3. Symlink PDFs into project directory (REQUIRED for subagent access)
   ln -sf "/Users/Shared/ksvc/pdfs/YYYYMMDD" ".claude/pdfs-scan"

4. Split PDFs into groups and spawn parallel Explore agents
   TARGET: ~5 PDFs per agent. Spawn ALL agents in a single message.
   - Each agent gets a specific list of filenames to scan
   - All agents run simultaneously → total time = slowest agent
   - Haiku is cheap — more agents = faster with no meaningful cost increase
```

## 代理数量分配

| PDF数量 | 代理数量 | 每个代理处理的PDF数量 | 预计时间 |
|------|--------|-----------|---------------|
| ≤5 | 1 | 所有PDF | 约25秒 |
| 6-10 | 2 | 每个代理约5份PDF | 约25秒 |
| 11-15 | 3 | 每个代理约5份PDF | 约25秒 |
| 16-20 | 4 | 每个代理约5份PDF | 约25秒 |
| 21-30 | 5-6 | 每个代理约5份PDF | 约30秒 |

**为什么每个代理处理5份PDF是最佳选择？** 这是速度的平衡点。每份PDF的阅读和总结大约需要4-8秒。每个代理处理5份PDF大约需要25秒。增加每个代理处理的PDF数量并不会节省时间（总标记数量不变），但会延长处理时间。

**成本：** Haiku工具成本较低。4个代理 × 5份PDF × 每份PDF约4,000个标记 = 总共约80,000个输入标记 —— 与1个代理处理所有20份PDF的成本相同。并行处理是免费的。**

**跨文档综合的权衡：** 每个代理只能看到自己的批次，因此跨批次的主题分析是主代理的工作。这没关系——主代理会合并所有结果。**

### 示例：启动Explore代理

**步骤1：主代理创建符号链接并列出PDF文件：**
```bash
ln -sf "/Users/Shared/ksvc/pdfs/20260205" ".claude/pdfs-scan"
/bin/ls ".claude/pdfs-scan/"
```

**步骤2：将文件名分组并并行启动代理（单条消息，多个Task调用）：**
```
# Agent 1 — first batch
Task(subagent_type="Explore", prompt="""
**THOROUGHNESS: medium**

Scan these specific PDFs for content angles:
- file1.pdf
- file2.pdf
- file3.pdf
- file4.pdf
- file5.pdf
- file6.pdf
- file7.pdf

For each PDF, Read enough pages to understand the full thesis (use judgment — some need 1-2 pages, others 1-5):

Read(file_path="/Users/dydo/Documents/agent/ksvc-intern/.claude/pdfs-scan/FILENAME.pdf", pages="1-5")

For each PDF extract:
- Company/sector, ticker, rating, price target
- Key thesis and supporting numbers
- Supply chain connections
- Potential content angles

After scanning your batch, provide:
1. Per-PDF summary (2-3 sentences each)
2. Cross-document themes within your batch
3. Which PDFs are most relevant for deep extraction
""")

# Agent 2 — second batch (SPAWN IN SAME MESSAGE as Agent 1)
Task(subagent_type="Explore", prompt="""
... same prompt with file8.pdf through file14.pdf ...
""")

# Agent 3 — third batch (SPAWN IN SAME MESSAGE)
Task(subagent_type="Explore", prompt="""
... same prompt with file15.pdf through file20.pdf ...
""")
```

**步骤3：主代理整合所有代理的结果：**
所有代理返回后，主代理：
1. 合并每份PDF的总结
2. 识别代理1和代理2发现的共同主题
3. 选择2-5份PDF进行步骤1b的深度提取

### 输出：确定哪些PDF重要
扫描完成后，你将知道：
- 哪些报告的数据最准确
- 跨文档之间的联系（例如，“3份报告确认了内存短缺”）
- **论点推荐**（2-3个值得深入探讨的角度）
- 哪些PDF需要使用RLM进行深度提取

**⚠️ 警告：** Explore代理可能会产生错误的数字。在RLM验证之前，将Explore总结中的所有数字视为“未经验证的声明”。组件数量、百分比和市场规模尤其容易出错。**

**容量（2026-02-07测试结果）：** 单个Explore代理（haiku）在83秒内处理了19份PDF，详细程度中等，使用了125,000个标记（第1-5页每页约4,000个标记）。3个代理并行处理相同批次大约需要30-40秒。**

---

## 步骤1b：使用RLM进行深度提取

使用RLM从步骤1a中识别出的特定PDF进行**深度提取**。

**对于你将要发布的任何内容，这一步都是必须执行的。** Explore代理负责总结；RLM负责验证。

## 何时使用
- 你知道哪些2-5份PDF最重要
- 需要具体的数字、图表、表格
- 构建跨文档的验证表格
- 提取技术细节（如fab产量、产量、WPM）

### 单份PDF
```bash
cd ~/.claude/skills/rlm-repl/scripts
python3 rlm_repl.py init "/Users/Shared/ksvc/pdfs/YYYYMMDD/file.pdf" --extract-images
python3 rlm_repl.py exec -c "print(grep('revenue|growth|target|price', max_matches=20, window=200))"
```

### 多份PDF（综合处理）
```bash
cd ~/.claude/skills/rlm-repl-multi/scripts
python3 rlm_repl.py init "/path/to/report1.pdf" --name report1 --extract-images
python3 rlm_repl.py init "/path/to/report2.pdf" --name report2 --extract-images
python3 rlm_repl.py exec -c "results = grep_all('keyword', max_matches_per_context=20)"
```

### 查看提取的图表/图片
```bash
# List images from a context
python3 rlm_repl.py exec --name report1 -c "print(list_images())"

# Get image path, then use Read tool to view
python3 rlm_repl.py exec --name report1 -c "print(get_image(0))"
```

图表通常包含关键数据（产量/价格趋势、利润率历史、产能时间线），这些数据是文本提取无法捕捉到的。

### 提取验证（必须执行）

**⚠️ 在每次`rlm_repl.py init`之后，验证提取是否成功。**

RLM在初始化后会报告`chars_extracted`。一份多页的分析师报告应该包含数千个字符。如果提取的字符数量异常少，那么该PDF很可能是基于图片的，RLM可能只提取了元数据和标题。

**验证规则：**

| 提取的字符数量 | 预期的报告类型 | 应采取的行动 |
|----------------|---------------------|--------|
| > 5,000 | 多页报告 | ✅ 继续使用grep进行验证 |
| 1,000 - 5,000 | 短篇笔记/部分内容 | ⚠️ 查看`list_images()` —— 如果有很多图片，触发备用方法 |
| < 1,000 | 基于图片的PDF | ❌ **必须使用读取工具进行备用处理** |

**这个阈值取决于上下文。** 一份20页的高盛报告如果只提取了666个字符，显然是有问题的。一份1页的定价表如果提取了800个字符，可能是正常的。需要根据实际情况判断，但如果有疑问，请使用备用方法。**

**当RLM提取结果较少时，必须执行的备用方法：**

```bash
# Step 1: RLM init (always try first)
python3 rlm_repl.py init "/path/to/report.pdf" --extract-images
# Output: "Extracted 666 chars from 15 pages, saved 9 images"

# Step 2: Check - is 666 chars enough for a 15-page report? NO.
# → Trigger fallback

# Step 3: Check extracted images first (they may contain the data)
python3 rlm_repl.py exec -c "print(list_images())"
# View extracted images with Read tool
# Read(file_path="/path/to/extracted/image-0.png")

# Step 4: Read the PDF directly (use symlinked path for subagents)
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="1-10")
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="11-20")
```

**⚠️ 路径规则：** 子代理必须通过符号链接的项目路径（`.claude/pdfs-scan/`）读取PDF，****不得从`/Users/Shared/`路径读取。**请参阅上面的“子代理权限”部分。

**为什么会有这个步骤（案例研究——ABF基板，2026-02-07）：**

高盛发布了两份报告：一份是关于ABF产能上升的报告（71K字符，提取正常），另一份是关于Kinsus的升级报告（15页，但只提取了666个字符）。我们跳过了Kinsus的报告，因为“主要报告包含了我们需要的所有信息”。但实际上Kinsus的报告包含了独特的数据（公司特定的产能计划、利润率指导、订单簿细节），这些数据本可以增强帖子的内容。跳过这份报告是偷懒的行为——使用读取工具的备用方法只需要30秒就可以获取到这些数据。**

**规则：**
1. **切勿因为RLM提取结果较少就忽略相关的PDF。** 使用备用方法。
2. **检查提取的图片。** 使用`--extract-images`选项时，RLM通常可以提取图表/表格图片。**
3. **记录备用方法的使用情况。** 在提取缓存中记录`"extraction_method": "read_fallback"，以便审计人员知道数据来源。**
4. **如果备用方法也失败了**（PDF损坏或受数字版权管理保护）：** **记录下来并继续处理。**但你必须尝试。**

### RLM缓存：包含视觉数据

在提取数据时，捕获**所有**可能用于后续图表生成的数据类型：

| 数据类型 | 需要提取的内容 | 缓存格式 |
|-------------|-----------------|--------------|
| 文本数字 | 带有页码引用的确切引用 | `{"value": 5.3, "unit": "B", "source": "p.3", "quote": "規模約53億美元"}` |
| 表格 | 完整的表格作为结构化JSON | `{"columns": [...], "rows": [...]`, "source": "p.20"}` |
| 图表 | 数据点 + 图表来源路径 | `{"data": {...}, "source_image": "pdf-3-1.png", "page": 3}` |

**为什么需要缓存视觉数据？** 第6步（图表生成）需要这些数据。如果你只缓存文本，就会丢失表格结构和图表数据点。**

## 跨文档推理
通过跨多个报告对比观点来构建论点：
```bash
# Find where multiple reports discuss the same topic
python3 rlm_repl.py exec -c "results = grep_all('DRAM.*price|ASP', max_matches_per_context=5)"

# Compare forecasts across sources
python3 rlm_repl.py exec -c "results = grep_all('2026|2027|growth|demand', max_matches_per_context=5)"
```

使用跨文档方法来验证：
- 多个来源是否对价格预测达成一致？
- 供应限制的时间线是否一致？
- 报告之间是否存在矛盾？

---

## 步骤1b.5：构建提取缓存（必须执行）

**⚠️ 为什么会有这个步骤：** RLM在提取过程中会创建`state.pkl`文件，但在写作阶段（步骤3）无法访问它。如果没有持久的缓存，编写者会依赖内存，从而导致错误，例如产品类型错误、时间段缺失或来源归属错误。

**这个步骤的作用：** 从`state.pkl`（RLM的内部格式）中提取数据，并将其转换为带有上下文标签的结构化JSON格式，以便写作阶段可以使用。

**何时执行**
**在步骤1b（RLM提取）之后和步骤3（写作）之前。**

| 工作流程 | 何时缓存 |
|----------|---------------|
| 单份PDF（rlm-repl） | 在`rlm_repl.py init`完成后 |
| 多份PDF（rlm-repl-multi） | 在所有`init`命令完成后 |

## 如何构建缓存

**v2的新功能：** 自动从PDF文件名生成来源标签和归属映射！**

**单份PDF（rlm-repl）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Auto-extracts from default rlm-repl state location
python3 build_extraction_cache.py \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**多份PDF（rlm-repl-multi）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Use --multi flag to load from rlm-repl-multi state
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**在跨文档综合时（可选）：**
```bash
# Add manual synthesis descriptions for cross-doc insights
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json \
  --synthesis /path/to/cross-doc-synthesis.json
```

**综合格式**（针对复杂的多来源帖子，可选）：
```json
{
  "dual_squeeze_thesis": {
    "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
    "components": [
      {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
      {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
    ]
  }
}
```

**自动生成的内容：**
- ✅ 从PDF文件名生成来源标签（例如："GFHK - Memory.pdf" → 标签："GFHK"）
- ✅ 包含主要来源、关键指标和来源上下文的标签**
- ✅ 包含完整上下文的提取条目（产品类型、时间周期、单位）

### 缓存格式

缓存包括**上下文标签**和**归属映射**，以防止常见错误：

```json
{
  "cache_version": "1.0",
  "generated_at": "2026-02-05T14:00:00",
  "sources": [
    {
      "source_id": "gfhk_memory",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/GFHK - Memory.pdf",
      "pdf_name": "GFHK - Memory price impact.pdf",
      "tag": "GFHK",
      "chars_extracted": 13199
    },
    {
      "source_id": "goldman_abf",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/Goldman ABF shortage.pdf",
      "pdf_name": "Goldman Sachs ABF shortage report.pdf",
      "tag": "Goldman Sachs",
      "chars_extracted": 25000
    }
  ],
  "extractions": [
    {
      "entry_id": "mem_001",
      "source_id": "gfhk_memory",
      "figure": "Figure 2",
      "page": 3,
      "metric": "Total BOM",
      "product_type": "HGX B300 8-GPU server",
      "time_period": "3Q25 → 1Q26E",
      "units": "dollars per server",
      "scope": "single HGX B300 8-GPU server",
      "values": {
        "before": "$369k",
        "after": "$408k",
        "change": "+$39k"
      },
      "context": "Memory price impact on AI server BOM",
      "source_quote": "Figure 2: HGX B300 8-GPU server BOM...",
      "verification": "RLM grep + visual inspection"
    }
  ],
  "source_attribution_map": {
    "topics": {
      "Memory Pricing": {
        "primary_source": "gfhk_memory",
        "tag": "GFHK",
        "key_metrics": ["HBM3e ASP", "DDR5-6400 (128GB)", "NVMe SSD (3.84TB)", "Total BOM"],
        "source_context": "Figures: Figure 2; Time periods: 3Q25 → 1Q26E",
        "notes": "4 extractions from this source"
      },
      "Abf Shortage": {
        "primary_source": "goldman_abf",
        "tag": "Goldman Sachs",
        "key_metrics": ["ABF shortage ratio", "Kinsus PT", "NYPCB PT", "Unimicron PT"],
        "source_context": "Time periods: 2H26, 2027, 2028",
        "notes": "5 extractions from this source"
      }
    },
    "cross_doc_synthesis": {
      "dual_squeeze_thesis": {
        "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
        "components": [
          {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
          {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
        ]
      }
    }
  }
}
```

**防止错误的关键字段：**
- `product_type`：当来源提到“HGX B300服务器”时，防止显示为“GB300机架”
- `time_period`：当来源提到“3Q25 → 1Q26E”时，防止时间段错误
- `source_id`：当数据来自GFHK时，防止显示为“Goldman的BOM”
- `tag`：从PDF文件名自动提取，以便快速归属

**归属映射的好处：**
- `topics`：显示哪个来源是主要信息来源的层级映射
- `key_metrics`：快速查找每个来源涵盖的内容
- `source_context`：总结各个来源涵盖的时间段
- `cross_doc_synthesis`：手动连接多个来源的见解

### 与步骤3（写作）的集成

**必须执行：** 在写作时引用缓存。**

**步骤3a：加载缓存和归属映射：**
```python
cache = load_json('rlm-extraction-cache.json')
attr_map = cache['source_attribution_map']

# Get topic attribution
topic = "Memory Pricing"
source_tag = attr_map['topics'][topic]['tag']  # "GFHK"
key_metrics = attr_map['topics'][topic]['key_metrics']
```

**步骤3b：使用缓存标签和归属信息进行写作：**
```markdown
## Content

3/ Memory squeeze is already here. GFHK's BOM breakdown (3Q25 → 1Q26E):
- HBM3e ASP: $3,756 → $4,378 (+17%)
- DDR5-6400 (128GB): $563 → $1,920 (+241%)
- HGX B300 8-GPU server BOM: $369k → $408k
```

**来源：** `rlm-extraction-cache.json`，条目`mem_001`，`mem_002`，`mem_003`

**缓存中的上下文标签：**
- 产品类型：HGX B300 8-GPU服务器（而不是GB300机架）
- 时间周期：3Q25 → 1Q26E（季度变化）
- 来源：GFHK图2（通过归属映射）

**归属映射的使用：**
- 使用`topics["Memory Pricing"]["tag"]` → “GFHK”
- 根据`key_metrics`列表验证

### 强制执行**
**在保存草稿之前（步骤5）：** **验证以下内容：**
- [ ] 每个发布的数字都有缓存条目
- [ ] 产品类型与缓存标签匹配
- [ ] 时间周期包含在缓存中
- [ ] 来源归属与缓存中的`source_id`和归属映射中的`tag`匹配
- [ ] 单位与缓存中的单位匹配（美元 vs 架数 vs 数据中心）
- [ ] 如果适用，引用`cross_doc_synthesis`中的交叉文档声明**

**警告标志 - 如果发现以下情况，请停止：**
- 从内存中而不是缓存中写入数字
- 产品类型与缓存中的不同（`product_type`字段）
- 当缓存中有时间周期时，时间周期缺失
- 将来源归属错误地归因于缓存中的`source_id`
- 使用错误的标签（例如，将GFHK的数据归因于“Goldman”）
- 在连接多个来源时缺少跨文档综合

### 手动构建缓存

如果自动提取失败，手动创建缓存条目：

```json
{
  "entry_id": "manual_001",
  "source_id": "report_name",
  "metric": "Component count",
  "product_type": "Humanoid robot (dexterous hand)",
  "values": {"count": 22},
  "units": "DOF (degrees of freedom)",
  "context": "Dexterous hand articulation",
  "source_quote": "22自由度靈巧手",
  "verification": "Manual extraction from p.15",
  "notes": "Summed from finger joints (20) + wrist (2)"
}
```

**详细信息请参阅：** `~/.claude/skills/kirk-content-pipeline/scripts/README-extraction-cache.md`以获取完整文档。**

---

## 步骤1c：跨文档综合（推荐）

**为什么会有这个步骤：** 步骤1a和步骤1b生成的是每份文档的事实。** 如果没有明确的综合，管道可能会偏向于单一来源的声明（例如，“KHGEARS的市盈率是20倍”），而不是跨文档的见解（例如，“台湾经纪人对人形机器人的看法比西方分析师更乐观”）。

## 何时使用

| 情景 | 是否使用1c？ |
|----------|---------|
| 多份PDF讨论同一主题 | **是** |
| 比较不同经纪人的观点 | **是** |
| 寻找共识/分歧 | **是** |
| 单份PDF的深入分析 | **否**（跳到步骤2） |
| 突发新闻（速度很重要） | **否**（跳到步骤2） |

## 1c的输出类型 | 示例 | 审计要求 |
|-------------|---------|-------------------|
| **共识声明** | “4家经纪中有3家认为2H26年的DRAM ASP在上升” | 跨文档（rlm-multi） |
| **比较性见解** | “HIWIN的市盈率为38倍，而KHGEARS为20倍——市场定价是否合理” | 跨文档（rlm-multi） |
| **分歧标志** | “微软表示中立，当地经纪人建议买入——谁是对的？” | 跨文档（rlm-multi） |
| **综合论点** | “台湾供应链被低估，与中国同行相比” | 跨文档（rlm-multi） |

## 如何运行跨文档综合

```bash
cd ~/.claude/skills/rlm-repl-multi/scripts

# Initialize all relevant PDFs
python3 rlm_repl.py init "/path/to/broker1.pdf" --name broker1
python3 rlm_repl.py init "/path/to/broker2.pdf" --name broker2
python3 rlm_repl.py init "/path/to/broker3.pdf" --name broker3

# Ask synthesis questions (not just extraction)
python3 rlm_repl.py exec -c "
# Question 1: Do they agree on market sizing?
market_data = grep_all('market size|TAM|規模|billion|億', max_matches_per_context=10)
print('=== MARKET SIZE ACROSS SOURCES ===')
print(market_data)
"

python3 rlm_repl.py exec -c "
# Question 2: Compare recommendations
ratings = grep_all('BUY|SELL|NEUTRAL|買進|賣出|中立|rating|recommendation', max_matches_per_context=10)
print('=== RATINGS COMPARISON ===')
print(ratings)
"

python3 rlm_repl.py exec -c "
# Question 3: Find disagreements
pe_data = grep_all('P/E|PE|本益比|target price|目標價', max_matches_per_context=10)
print('=== VALUATION COMPARISON ===')
print(pe_data)
"
```

### 需要提出的综合问题**

| 类别 | 问题 |
|----------|-----------|
| **共识** | 来源是否对[市场规模 / 时间线 / 关键风险]达成一致？ |
| **比较** | [经纪人A]的观点与[经纪人B]有何不同？ |
| **估值** | 当地分析师和外国分析师的定价是否一致？ |
| **时间线** | 来源是否对[催化剂 / 转折点]达成一致？ |
| **风险** | 一个来源提到了哪些其他来源没有提到的风险？ |

## 输出格式：综合缓存

运行步骤1c后，记录步骤3（写作）所需的综合见解：

```markdown
## Cross-Doc Synthesis (Step 1c)

**Sources:** broker1 (永豐), broker2 (MS), broker3 (Citi)

### Consensus
- Market size: All 3 agree on $5-6B (2025) → $30-35B (2029)
- CAGR: 55-60% range across all sources

### Disagreements
- HIWIN: MS says NEUTRAL (38x too rich), 永豐 silent, Citi no coverage
- Timeline: 永豐 more bullish on 2026 ramp, MS cautious until 2027

### Comparative Insights (use in thread)
- "Taiwan brokers (永豐) bullish on KHGEARS; Western analysts (MS) more cautious on HIWIN"
- "Local coverage sees 2026 inflection; foreign houses waiting for 2027 proof points"

### Audit Flag
These synthesized claims require cross-doc verification in Step 4b:
- [ ] "3 sources agree on market size" → verify all 3 sources
- [ ] "Local vs foreign view divergence" → verify specific ratings from each
```

## 与审计的集成（步骤4a）

**⚠️ 重要提示：** 步骤1c中的综合声明必须在步骤4a中进行跨文档审计。**

在审计清单中，用`cross-doc: true`标记这些声明：

```markdown
## Claims to Verify

| # | Claim | Type | Source ID | Cross-Doc? |
|---|-------|------|-----------|------------|
| 1 | KHGEARS P/E 20x | P/E | src1 | No |
| 2 | Market consensus $5.3B | Consensus | src1, src2, src3 | **Yes** |
| 3 | Local vs foreign view divergence | Synthesis | src1, src2 | **Yes** |
```

跨文档声明使用`rlm-repl-multi`进行验证，而不是使用并行的单个文档代理。

---

### 提取技术细节
深入挖掘特定PDF时，使用RLM进行**深度提取**。

**对于你将要发布的任何内容，这一步都是必须执行的。** Explore代理负责总结；RLM负责验证。

## 何时使用
- 你知道哪些2-5份PDF最重要
- 需要具体的数字、图表、表格
- 构建跨文档的验证表格
- 提取技术细节（如fab产量、产量、WPM）

### 单份PDF
```bash
cd ~/.claude/skills/rlm-repl/scripts
python3 rlm_repl.py init "/Users/Shared/ksvc/pdfs/YYYYMMDD/file.pdf" --extract-images
python3 rlm_repl.py exec -c "print(grep('revenue|growth|target|price', max_matches=20, window=200))"
```

### 多份PDF（综合处理）
```bash
cd ~/.claude/skills/rlm-repl-multi/scripts
python3 rlm_repl.py init "/path/to/report1.pdf" --name report1 --extract-images
python3 rlm_repl.py init "/path/to/report2.pdf" --name report2 --extract-images
python3 rlm_repl.py exec -c "results = grep_all('keyword', max_matches_per_context=20)"
```

### 查看提取的图表/图片
```bash
# List images from a context
python3 rlm_repl.py exec --name report1 -c "print(list_images())"

# Get image path, then use Read tool to view
python3 rlm_repl.py exec --name report1 -c "print(get_image(0))"
```

图表通常包含关键数据（产量/价格趋势、利润率历史、产能时间线），这些数据是文本提取无法捕捉到的。

### 提取验证（必须执行）

**⚠️ 在每次`rlm_repl.py init`之后，验证提取是否成功。**

RLM在初始化后会报告`chars_extracted`。一份多页的分析师报告应该包含数千个字符。如果提取的字符数量异常少，那么该PDF很可能是基于图片的，RLM可能只提取了元数据和标题。

**验证规则：**

| 提取的字符数量 | 预期的报告类型 | 应采取的行动 |
|----------------|---------------------|--------|
| > 5,000 | 多页报告 | ✅ 继续使用grep进行验证 |
| 1,000 - 5,000 | 短篇笔记/部分内容 | ⚠️ 查看`list_images()` —— 如果有很多图片，触发备用方法 |
| < 1,000 | 基于图片的PDF | ❌ **必须使用读取工具进行备用处理** |

**阈值取决于上下文。** 一份20页的高盛报告如果只提取了666个字符，显然是有问题的。一份1页的定价表如果提取了800个字符，可能是正常的。需要根据实际情况判断，但如果有疑问，请使用备用方法。**

**当RLM提取结果较少时，必须执行的备用方法：**

```bash
# Step 1: RLM init (always try first)
python3 rlm_repl.py init "/path/to/report.pdf" --extract-images
# Output: "Extracted 666 chars from 15 pages, saved 9 images"

# Step 2: Check - is 666 chars enough for a 15-page report? NO.
# → Trigger fallback

# Step 3: Check extracted images first (they may contain the data)
python3 rlm_repl.py exec -c "print(list_images())"
# View extracted images with Read tool
# Read(file_path="/path/to/extracted/image-0.png")

# Step 4: Read the PDF directly (use symlinked path for subagents)
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="1-10")
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="11-20")
```

**⚠️ 路径规则：** 子代理必须通过符号链接的项目路径（`.claude/pdfs-scan/`）读取PDF，****不得从`/Users/Shared/`路径读取。**请参阅上面的“子代理权限”部分。**

**为什么会有这个步骤（案例研究——ABF基板短缺，2026-02-07）：**

高盛发布了两份报告：一份是关于ABF产能上升的报告（71K字符，提取正常），另一份是关于Kinsus的升级报告（15页，但只提取了666个字符）。我们跳过了Kinsus的报告，因为“主要报告包含了我们需要的所有信息”。但实际上Kinsus的报告包含了独特的数据（公司特定的产能计划、利润率指导、订单簿细节），这些数据本可以增强帖子的内容。跳过这份报告是偷懒的行为——使用读取工具的备用方法只需要30秒就可以获取到这些数据。**

**规则：**
1. **切勿仅仅因为RLM提取结果较少就忽略相关的PDF。** 使用备用方法。
2. **检查提取的图片。** 使用`--extract-images`选项时，RLM通常可以提取图表/表格图片。**
3. **记录备用方法的使用情况。** 在提取缓存中记录`"extraction_method": "read_fallback"，以便审计人员知道数据来源。**
4. **如果备用方法也失败了**（PDF损坏或受数字版权管理保护）：** **记录下来并继续处理。**但你必须尝试。**

### RLM缓存：包含视觉数据

在提取数据时，捕获**所有**可能用于后续图表生成的数据类型：

| 数据类型 | 需要提取的内容 | 缓存格式 |
|-------------|-----------------|--------------|
| 文本数字 | 带有页码引用的确切引用 | `{"value": 5.3, "unit": "B", "source": "p.3", "quote": "規模約53億美元"}` |
| 表格 | 完整的表格作为结构化JSON | `{"columns": [...]], "rows": [...]`, "source": "p.20"}` |
| 图表 | 数据点 + 图表来源路径 | `{"data": {...}, "source_image": "pdf-3-1.png", "page": 3}` |

**为什么需要缓存视觉数据？** 第6步（图表生成）需要这些数据。如果你只缓存文本，就会丢失表格结构和图表数据点。**

## 跨文档推理
通过跨多个报告对比观点来构建论点：
```bash
# Find where multiple reports discuss the same topic
python3 rlm_repl.py exec -c "results = grep_all('DRAM.*price|ASP', max_matches_per_context=5)"

# Compare forecasts across sources
python3 rlm_repl.py exec -c "results = grep_all('2026|2027|growth|demand', max_matches_per_context=5)"
```

使用跨文档方法来验证：
- 多个来源是否对价格预测达成一致？
- 供应限制的时间线是否一致？
- 报告之间是否存在矛盾？**

---

## 步骤1b.5：构建提取缓存（必须执行）

**⚠️ 为什么会有这个步骤：** RLM在提取过程中会创建`state.pkl`文件，但在写作阶段（步骤3）无法访问它。如果没有持久的缓存，编写者会依赖内存，从而导致错误，例如产品类型错误、时间段缺失或来源归属错误。

**这个步骤的作用：** 从`state.pkl`（RLM的内部格式）中提取数据，并将其转换为带有上下文标签的结构化JSON格式，以便写作阶段可以使用。

**何时执行**
**在步骤1b（RLM提取）之后和步骤3（写作）之前。**

| 工作流程 | 何时缓存 |
|----------|---------------|
| 单份PDF（rlm-repl） | 在`rlm_repl.py init`完成后 |
| 多份PDF（rlm-repl-multi） | 在所有`init`命令完成后 |

## 如何构建缓存

**v2的新功能：** 自动从PDF文件名生成来源标签和归属映射！**

**单份PDF（rlm-repl）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Auto-extracts from default rlm-repl state location
python3 build_extraction_cache.py \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**多份PDF（rlm-repl-multi）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Use --multi flag to load from rlm-repl-multi state
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**在跨文档综合时（可选）：**
```bash
# Add manual synthesis descriptions for cross-doc insights
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json \
  --synthesis /path/to/cross-doc-synthesis.json
```

**综合格式**（针对复杂的多来源帖子，可选）：
```json
{
  "dual_squeeze_thesis": {
    "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
    "components": [
      {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
      {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
    ]
  }
}
```

**自动生成的内容：**
- ✅ 从PDF文件名生成来源标签（例如："GFHK - Memory.pdf" → 标签："GFHK"）
- ✅ 包含主要来源、关键指标和来源上下文的标签**
- ✅ 包含完整上下文的提取条目（产品类型、时间周期、单位）

### 缓存格式

缓存包括**上下文标签**和**归属映射**，以防止常见错误：

```json
{
  "cache_version": "1.0",
  "generated_at": "2026-02-05T14:00:00",
  "sources": [
    {
      "source_id": "gfhk_memory",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/GFHK - Memory.pdf",
      "pdf_name": "GFHK - Memory price impact.pdf",
      "tag": "GFHK",
      "chars_extracted": 13199
    },
    {
      "source_id": "goldman_abf",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/Goldman ABF shortage.pdf",
      "pdf_name": "Goldman Sachs ABF shortage report.pdf",
      "tag": "Goldman Sachs",
      "chars_extracted": 25000
    }
  ],
  "extractions": [
    {
      "entry_id": "mem_001",
      "source_id": "gfhk_memory",
      "figure": "Figure 2",
      "page": 3,
      "metric": "Total BOM",
      "product_type": "HGX B300 8-GPU server",
      "time_period": "3Q25 → 1Q26E",
      "units": "dollars per server",
      "scope": "single HGX B300 8-GPU server",
      "values": {
        "before": "$369k",
        "after": "$408k",
        "change": "+$39k"
      },
      "context": "Memory price impact on AI server BOM",
      "source_quote": "Figure 2: HGX B300 8-GPU server BOM...",
      "verification": "RLM grep + visual inspection"
    }
  ],
  "source_attribution_map": {
    "topics": {
      "Memory Pricing": {
        "primary_source": "gfhk_memory",
        "tag": "GFHK",
        "key_metrics": ["HBM3e ASP", "DDR5-6400 (128GB)", "NVMe SSD (3.84TB)", "Total BOM"],
        "source_context": "Figures: Figure 2; Time periods: 3Q25 → 1Q26E",
        "notes": "4 extractions from this source"
      },
      "Abf Shortage": {
        "primary_source": "goldman_abf",
        "tag": "Goldman Sachs",
        "key_metrics": ["ABF shortage ratio", "Kinsus PT", "NYPCB PT", "Unimicron PT"],
        "source_context": "Time periods: 2H26, 2027, 2028",
        "notes": "5 extractions from this source"
      }
    },
    "cross_doc_synthesis": {
      "dual_squeeze_thesis": {
        "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
        "components": [
          {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
          {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
        ]
      }
    }
  }
}
```

**防止错误的关键字段：**
- `product_type`：当来源提到“HGX B300机架”时，防止显示为“GB300 rack”
- `time_period`：当来源提到“3Q25 → 1Q26E”时，防止时间段缺失
- `source_id`：当数据来自GFHK时，防止显示为“Goldman的BOM”
- `tag`：从PDF文件名自动提取，以便快速归属
- `units`：当来源表示“22.5B机架”时，防止显示为“22.5bn美元”
- `scope`：当来源表示“per rack”时，防止显示为“per server”

**归属映射的好处：**
- `topics`：显示哪个来源是主要信息来源的层级映射
- `key_metrics`：快速查找每个来源涵盖的内容
- `source_context`：总结各个来源涵盖的时间段
- `cross_doc_synthesis`：手动连接多个来源的见解

### 与步骤3（写作）的集成

**必须执行：** 在写作时引用缓存。**

**步骤3a：加载缓存和归属映射：**
```python
cache = load_json('rlm-extraction-cache.json')
attr_map = cache['source_attribution_map']

# Get topic attribution
topic = "Memory Pricing"
source_tag = attr_map['topics'][topic]['tag']  # "GFHK"
key_metrics = attr_map['topics'][topic]['key_metrics']
```

**步骤3b：使用缓存标签和归属信息进行写作：**
```markdown
## Content

3/ Memory squeeze is already here. GFHK's BOM breakdown (3Q25 → 1Q26E):
- HBM3e ASP: $3,756 → $4,378 (+17%)
- DDR5-6400 (128GB): $563 → $1,920 (+241%)
- HGX B300 8-GPU server BOM: $369k → $408k
```

**来源：** `rlm-extraction-cache.json`，条目`mem_001`，`mem_002`，`mem_003`

**缓存中的上下文标签：**
- 产品类型：HGX B300 8-GPU服务器（而不是GB300机架）
- 时间周期：3Q25 → 1Q26E（季度变化）
- 来源：GFHK图2（通过归属映射标签）

**归属映射的使用：**
- 使用`topics["Memory Pricing"]["tag"] → “GFHK”
- 根据`key_metrics`列表验证

### 强制执行**
**在保存草稿之前（步骤5）：** **验证以下内容：**
- [ ] 每个发布的数字都有缓存条目
- [ ] 产品类型与缓存标签匹配
- [ ] 时间周期包含在缓存中
- [ ] 来源归属与缓存中的`source_id`和归属映射中的`tag`匹配
- [ ] 单位与缓存中的单位匹配（美元 vs 架数 vs 数据中心）
- [ ] 如果适用，引用`cross_doc_synthesis`中的交叉文档声明**

**警告标志 - 如果发现以下情况，请停止：**
- 从内存中而不是缓存中写入数字
- 产品类型与缓存中的不同（`product_type`字段）
- 当缓存中有时间周期时，时间周期缺失
- 将来源归属错误地归因于缓存中的`source_id`
- 使用错误的标签（例如，将GFHK的数据归因于“Goldman”）
- 在连接多个来源时缺少跨文档综合

### 手动构建缓存

如果自动提取失败，手动创建缓存条目：

```json
{
  "entry_id": "manual_001",
  "source_id": "report_name",
  "metric": "Component count",
  "product_type": "Humanoid robot (dexterous hand)",
  "values": {"count": 22},
  "units": "DOF (degrees of freedom)",
  "context": "Dexterous hand articulation",
  "source_quote": "22自由度靈巧手",
  "verification": "Manual extraction from p.15",
  "notes": "Summed from finger joints (20) + wrist (2)"
}
```

**详细信息请参阅：** `~/.claude/skills/kirk-content-pipeline/scripts/README-extraction-cache.md`以获取完整文档。**

---

## 步骤1c：跨文档综合（推荐）

**为什么会有这个步骤：** 步骤1a和步骤1b生成的是每份文档的事实。** 如果没有明确的综合，管道可能会倾向于单一来源的声明（例如，“KHGEARS的市盈率为20倍”），而不是跨文档的见解（例如，“台湾经纪人对人形机器人的看法比西方分析师更乐观”）。

## 何时使用

| 情景 | 是否使用1c？ |
|----------|---------|
| 多份PDF讨论同一主题 | **是** |
| 比较不同经纪人的观点 | **是** |
| 寻找共识/分歧 | **是** |
| 单份PDF的深入分析 | **否**（跳到步骤2） |
| 突发新闻（速度很重要） | **否**（跳到步骤2） |

## 1c的输出类型 | 示例 | 审计要求 |
|-------------|---------|-------------------|
| **共识声明** | “4家经纪中有3家认为2H26年的DRAM ASP在上升” | 跨文档（rlm-multi） |
| **比较性见解** | “HIWIN的市盈率为38倍，而KHGEARS为20倍——市场定价是否合理” | 跨文档（rlm-multi） |
| **分歧标志** | “微软表示中立，当地经纪人建议买入——谁是对的？” | 跨文档（rlm-multi） |
| **综合论点** | “台湾供应链被低估，与中国同行相比” | 跨文档（rlm-multi） |

## 如何运行跨文档综合

```bash
cd ~/.claude/skills/rlm-repl-multi/scripts

# Initialize all relevant PDFs
python3 rlm_repl.py init "/path/to/broker1.pdf" --name broker1
python3 rlm_repl.py init "/path/to/broker2.pdf" --name broker2
python3 rlm_repl.py init "/path/to/broker3.pdf" --name broker3

# Ask synthesis questions (not just extraction)
python3 rlm_repl.py exec -c "
# Question 1: Do they agree on market sizing?
market_data = grep_all('market size|TAM|規模|billion|億', max_matches_per_context=10)
print('=== MARKET SIZE ACROSS SOURCES ===')
print(market_data)
"

python3 rlm_repl.py exec -c "
# Question 2: Compare recommendations
ratings = grep_all('BUY|SELL|NEUTRAL|買進|賣出|中立|rating|recommendation', max_matches_per_context=10)
print('=== RATINGS COMPARISON ===')
print(ratings)
"

python3 rlm_repl.py exec -c "
# Question 3: Find disagreements
pe_data = grep_all('P/E|PE|本益比|target price|目標價', max_matches_per_context=10)
print('=== VALUATION COMPARISON ===')
print(pe_data)
"
```

### 需要提出的综合问题**

| 类别 | 问题 |
|----------|-----------|
| **共识** | 来源是否对[市场规模 / 时间线 / 关键风险]达成一致？ |
| **比较** | [经纪人A]的观点与[经纪人B]有何不同？ |
| **估值** | 当地分析师和外国分析师的定价是否一致？ |
| **时间线** | 来源是否对[催化剂 / 转折点]达成一致？ |
| **风险** | 一个来源提到了哪些其他来源没有提到的风险？ |

## 输出格式：综合缓存

运行步骤1c后，记录步骤3（写作）所需的综合见解：

```markdown
## Cross-Doc Synthesis (Step 1c)

**Sources:** broker1 (永豐), broker2 (MS), broker3 (Citi)

### Consensus
- Market size: All 3 agree on $5-6B (2025) → $30-35B (2029)
- CAGR: 55-60% range across all sources

### Disagreements
- HIWIN: MS says NEUTRAL (38x too rich), 永豐 silent, Citi no coverage
- Timeline: 永豐 more bullish on 2026 ramp, MS cautious until 2027

### Comparative Insights (use in thread)
- "Taiwan brokers (永豐) bullish on KHGEARS; Western analysts (MS) more cautious on HIWIN"
- "Local coverage sees 2026 inflection; foreign houses waiting for 2027 proof points"

### Audit Flag
These synthesized claims require cross-doc verification in Step 4b:
- [ ] "3 sources agree on market size" → verify all 3 sources
- [ ] "Local vs foreign view divergence" → verify specific ratings from each
```

## 与审计的集成（步骤4a）

**⚠️ 重要提示：** 步骤1c中的综合声明必须在步骤4a中进行跨文档审计。**

在审计清单中，用`cross-doc: true`标记这些声明：

```markdown
## Claims to Verify

| # | Claim | Type | Source ID | Cross-Doc? |
|---|-------|------|-----------|------------|
| 1 | KHGEARS P/E 20x | P/E | src1 | No |
| 2 | Market consensus $5.3B | Consensus | src1, src2, src3 | **Yes** |
| 3 | Local vs foreign view divergence | Synthesis | src1, src2 | **Yes** |
```

跨文档声明使用`rlm-repl-multi`进行验证，而不是使用并行的单个文档代理。

---

### 提取技术细节
深入挖掘特定PDF时，提取以下内容：
- 晶圆产能（WPM）
- 制造厂名称（M15X, P4L, X2）
- 产量百分比
- 工艺节点（1b, 1c）
- 每个单位的组件数量

| 问题 | 提取内容 |
|----------|---------|
| 什么 | 一句话的总结 |
| 为什么 | 为什么读者应该关心 |
| 谁 | 受影响的公司/股票代码 |
| 何时 | 时间段（具体季度） |
| 在哪里 | 制造厂位置、地理位置 |
| 如何 | 带有技术细节的机制 |

---

## 步骤2：初步检查KSVC的持股情况**

**⚠️ 重要提示：** 这只是一个初步检查。在编写内容之后，你必须执行步骤4c（最终持股情况验证），以确保在提取过程中发现的任何股票代码都是正确的。**

### 所有模型（共7个）
- **美国模型：** usa-model1 ~ usa-model5（5个模型）
- **台湾（TWSE）模型：** twse-model1 ~ twse-model2（2个模型）

### 步骤2a：识别所有可能的股票代码**

**在查询API之前，** **识别该公司的所有可能标识符：**

```bash
# Example: Global Unichip Corp
# Identifiers to search:
# - US ticker: N/A (not US-listed)
# - Taiwan ticker: 3443
# - Chinese name: 創意 or 全球晶圓科技
# - English name: Global Unichip, GUC
# - Stock code: 3443 TW (TWSE format)

# For Taiwan stocks, verify ticker via TWSE API first:
curl -s "https://www.twse.com.tw/en/api/codeQuery?query=3443"
# Returns: {"query":"3443","suggestions":["3443\tGUC"]}
```

**规则：**
1. **美国股票：** 仅通过股票代码搜索（例如，“MU”，“AMD”，“NVDA”）
2. **台湾股票：** 通过股票代码搜索（例如，“3443”）——在API中可能显示为“3443 創意”
3. **如果不确定：** 同时检查美国和TWSE的模型**

**步骤2b：查询所有7个模型**

****切勿在没有检查所有7个模型的情况下假设某只股票未被持有。**

**推荐：** 使用tradebook获取准确的入场价格和当前状态**

```bash
# FASTEST METHOD: Check tradebook for entry price + status
# (Works for all models - US and TWSE)
curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285 or .ticker == 3491) |
  {ticker, enterDate, enterPrice, todayPrice, profitPercent, exitDate}'

# Returns:
# {
#   "ticker": 6285,
#   "enterDate": "Wed, 28 Jan 2026 00:00:00 GMT",
#   "enterPrice": 162.0,
#   "todayPrice": 207.5,  # ⚠️ May be stale! Use Yahoo Finance for current
#   "profitPercent": 28.09,  # ⚠️ Based on stale todayPrice
#   "exitDate": null  # null = still holding
# }
```

**⚠️ 重要提示：** API的`todayPrice`和`profitPercent`可能会过时（几小时或几天之前的数据）。**始终使用Yahoo Finance API（步骤2d）验证当前价格。**

**备用方法：** 使用equitySeries（速度较慢，数据较少）**

```bash
# Check ALL 5 US models
for i in 1 2 3 4 5; do
  echo "=== USA-Model $i ==="
  curl -s "https://kicksvc.online/api/usa-model$i" | \
    jq --arg t "MU" '.equitySeries[0].series[] | select(.Ticker == $t) |
    {ticker: .Ticker, return: .data[-1].value}'
done

# Check ALL 2 TWSE models (search by stock code)
for i in 1 2; do
  echo "=== TWSE-Model $i ==="
  curl -s "https://kicksvc.online/api/twse-model$i" | \
    jq '.equitySeries[0].series[] | select(.Ticker | contains("3443")) |
    {ticker: .Ticker, return: .data[-1].value}'
done
```

**为什么仍然使用equitySeries？**
1. **历史追踪：** 显示随时间的回报百分比变化（`.data[]`数组）
2. **验证：** 确认持仓是否仍然有效
3. **备用方法：** 如果tradebook不可用或为空**
4. **入场日期的确定：** 第一个数据点（回报约为0）表示入场日期

**示例：从equitySeries中查找入场日期**
```bash
# Get all data points to find entry date
curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285")) | .data[0]'
# Returns: {"date": "2026-01-28 00:00:00", "value": 0}
# Entry date: Jan 28, 2026
```

## 步骤2c：验证和备用策略**

**使用所有三个数据来源以确保准确性：**

| 数据来源 | 何时使用 | 显示什么 | 限制 |
|-------------|-------------|---------------|------------|
| **tradebook** | 主要来源 | 入场日期、入场价格、退出状态 | `todayPrice`可能过时 |
| **equitySeries** | 验证 | 随时间的回报百分比 | 没有入场价格/日期 |
| **filledOrders** | 备用方法 | 实际交易订单、价格 | 如果模型未重新设置，则为空 |

**推荐的工作流程：**

```bash
# 1. PRIMARY: Get entry details from tradebook
TRADEBOOK=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285)')

# 2. VERIFY: Cross-check with equitySeries
EQUITY=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285"))')

# 3. FALLBACK: If tradebook empty, check filledOrders
if [ -z "$TRADEBOOK" ]; then
  curl -s "https://kicksvc.online/api/twse-model2" | \
    jq '.filledOrders[] | select(.ticker | contains("6285"))'
fi
```

**跨验证示例：**

```bash
# Check if tradebook and equitySeries agree on position status
TRADEBOOK_HELD=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285 and .exitDate == null) | .ticker')

EQUITY_HELD=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285")) | .Ticker')

# If both show position, high confidence
# If only one shows position, investigate discrepancy
```

**备用方法：** 如果tradebook为空****

如果equitySeries为空或tradebook为空（虽然罕见，但在模型重置后可能发生）：

```bash
# Check ALL US models - filledOrders
for i in 1 2 3 4 5; do
  echo "=== USA-Model $i filledOrders ==="
  curl -s "https://kicksvc.online/api/usa-model$i" | \
    jq '.filledOrders[] | select(.ticker == "MU") | {ticker, price, quantity}'
done

# Check ALL TWSE models - filledOrders
for i in 1 2; do
  echo "=== TWSE-Model $i filledOrders ==="
  curl -s "https://kicksvc.online/api/twse-model$i" | \
    jq '.filledOrders[] | select(.ticker | contains("3443")) | {ticker, price, quantity}'
done
```

**当数据来源不一致时：**

| 情况 | 行动 |
|----------|--------|
| tradebook显示持仓，equitySeries未显示持仓 | 信任tradebook（equitySeries可能会延迟） |
| equitySeries显示持仓，tradebook未显示持仓 | 调查——检查filledOrders |
| filledOrders显示买入但当前无持仓 | 持仓已关闭——检查tradebook.exitDate |
| 三个数据来源都为空 | 该模型中未持有该股票 |

### 步骤2e：使用准确的回报记录持股情况**

**重要提示：** 始终使用以下方法计算实际回报：**
1. **入场价格** 来自`tradebook.enterPrice`
2. **当前价格** 来自Yahoo Finance API（不要使用KSVC API的过时`todayPrice`）

**输出格式（使用准确数据）：**
```markdown
**KSVC Holdings Check:**
- ✅ WNC (6285.TW) - Held in TWSE Model 2
  - Entry: Jan 28, 2026 @ NT$162
  - Current: NT$187 (Yahoo Finance)
  - Gain: +15.4% (actual, not API's stale 28%)
- ✅ UMT (3491.TWO) - Held in TWSE Model 2
  - Entry: Jan 28, 2026 @ NT$1,120
  - Current: NT$1,280 (Yahoo Finance)
  - Gain: +14.3% (actual, not API's stale 23%)
- ❌ Not held in TWSE Model 1 or USA Models 1-5

**Note:** API's equitySeries and tradebook.todayPrice can lag hours/days behind market.
Always use Yahoo Finance for current prices.
```

**如果在任何模型中都没有持有该股票：**
```markdown
**KSVC Holdings Check:**
- ❌ Not held in any of 7 models (checked USA 1-5, TWSE 1-2)
- Content angle: Industry analysis / Market observation
```

### 集成策略**

| 情况 | 方法 | 示例 |
|-----------|----------|---------|
| **持有（美国股票）** | 显示持仓情况 | “KSVC Model1以$412的价格持有MU” |
| **持有（台湾股票）** | 显示持仓情况 | “KSVC台股Model1持有台積電 (2330)” |
| **未持有** | 行业说明 | “Memory cycle使MU的回报增加了$MU” |

### 步骤2d：当前价格检查（Yahoo Finance API - 必须执行）**

**⚠️ 重要提示：** 始终使用Yahoo Finance获取当前价格。** KSVC API的`todayPrice`可能会过时。**

**美国股票：**
```bash
# Get current price
TICKER="MU"
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | \
  jq '.chart.result[0].meta.regularMarketPrice'

# Get full market data
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'
```

**台湾股票（使用.TW或.TWO后缀）：**
```bash
# WNC (6285.TW)
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/6285.TW?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'

# UMT (3491.TWO - OTC stocks use .TWO)
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/3491.TWO?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'
```

**台湾股票的后缀：**
- `.TW` - 在台湾证券交易所（TWSE）上市 |
- `.TWO` - 在台北证券交易所（TPEx/OTC）上市 |

**计算实际收益（不要使用API的过时利润%）：**
```bash
# Example: WNC
TICKER="6285.TW"
ENTRY=162  # From tradebook.enterPrice
CURRENT=$(curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | jq '.chart.result[0].meta.regularMarketPrice')
echo "$TICKER: NT\$$CURRENT | Entry: NT\$$ENTRY | Gain: $(awk "BEGIN {printf \"%.1f\", ($CURRENT - $ENTRY) / $ENTRY * 100}")%"

# Output: 6285.TW: NT$187 | Entry: NT$162 | Gain: +15.4%
```

**完整的工作流程（tradebook + Yahoo Finance）：**
```bash
# 1. Get entry price from tradebook
ENTRY=$(curl -s "https://kicksvc.online/api/twse-model2" | jq '.tradebook[] | select(.ticker == 6285) | .enterPrice')

# 2. Get current price from Yahoo Finance
CURRENT=$(curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/6285.TW?interval=1d&range=1d" | jq '.chart.result[0].meta.regularMarketPrice')

# 3. Calculate actual gain
echo "Entry: NT\$$ENTRY | Current: NT\$$CURRENT | Gain: $(awk "BEGIN {printf \"%.1f\", ($CURRENT - $ENTRY) / $ENTRY * 100}")%"
```

---

## 步骤3：编写内容**

**有关完整模板和示例，请参阅`references/kirk-voice.md`。**

### 帖子编号规范

| 格式 | 适用场景 |
|--------|-------------|
| 推文1中没有编号 | 建议使用——这样更容易吸引注意力，如果被引用或分享则可以独立显示 |
| `2/`, `3/`, etc. | 标准的帖子格式——表示“2中的第N个” |
| 推文1中使用`1/` | 可选——明确表示“即将发布新的帖子” |

**为什么在推文1中不使用编号：**
- 吸引注意力的推文经常被单独分享
- “1/”在上下文中看起来不完整
- 更清晰的视觉呈现

**格式偏好：** 使用`/`而不是`)`——这是Twitter帖子的约定格式。**

```
✅ Recommended:
Humanoid robots going from science fair to factory floor. Taiwan supply chain getting interesting.

2/ TLDR:
- Market: $5.3B (2025) to $32.4B (2029)...

❌ Avoid:
1/ Humanoid robots going from science fair...
```

### 选择内容类型
1. 内容类型是什么？（长篇分析 / 快速总结 / 突发新闻 / 恶搞帖子 / 评论 / 胜利总结）
2. 在kirk-voice.md中查找相应的格式
3. 应用相应的风格混合

### 技术细节

❌ 含糊的表述：**“NAND供应紧张”**
✅ 具体的表述：**“YMTC在武汉的工厂3增加了135k WPM的产能。但仍然无法缩小差距——三星的X2转换推迟到第二季度。”**

❌ 含糊的表述：**“HBM的利润率很好”**
✅ 具体的表述：**“SK Hynix的HBM利润率在80-90%。三星在1c DRAM的利润率仅为60%。”**

始终包括：具体的数字、时间框架、制造厂名称、比较内容。

### 参考文献的清晰性（2026-02-08学习）

**在引用对象尚未介绍时，** **切勿使用含糊的代词或缩写。**

在帖子格式中，每条推文可能可以独立阅读。如果之前的推文将某个概念作为一个类别讨论（例如，“ASIC收入”），在后面的推文中突然将其称为“该项目”，读者可能不知道这个“项目”指的是什么。

❌ 含糊的表述：**“微软认为该项目是3nm的Google TPU”**
（哪个项目？帖子中从未提到过“该项目”。）

✅ 清晰的表述：**“微软认为主要客户/项目是3nm的Google TPU”**
（明确指出微软认为的是哪个项目以及他们在做什么。）

**规则：** 当使用缩写（如“该项目”、“这个交易”、“这个策略”）可以节省文字，但可能会影响清晰度。直接说明具体内容总是值得的。即使多几个词，也能避免读者需要重新阅读。**

**在从一般类别转向具体内容时：** 如果帖子首先讨论一个抽象类别（如ASIC收入），然后转向一个具体的实体（如Google TPU、三星的工厂），需要建立过渡。**

---

## 步骤4a：使用Explore代理进行初步筛选（必须执行）

**当有很多PDF需要审核时，使用Explore代理进行** **广泛筛选**。这比RLM更快，有助于快速发现内容。**

### 步骤1a.0：检查已发布的帖子（必须执行——先执行）

**⚠️ 在扫描任何PDF之前，请先查看Kirk已经发布了哪些内容。**

```bash
# List all published threads
ls /Users/Shared/ksvc/threads/

# Read recent thread.md files to understand what topics are covered
```

对于每个已发布的帖子，请记录：
- **主题**（论点是什么？）
- **使用的来源PDF**（查看 `_metadata.md`）
- **日期**（更新程度如何？）

**然后在选择主题时，拒绝以下任何主题：**
- 使用与已发布帖子相同的原始来源PDF
- 涉及相同的论点/角度（即使来自不同的来源）
- 会让Kirk的粉丝觉得重复

**允许的重叠情况：**
- 对之前帖子的跟进/更新，包含新数据（例如，收益确认了论点）
- 对同一行业的不同角度的报道（例如，之前报道了ABF的短缺情况，现在报道了特定公司的收益）
- 明确标注为“更新：这是我上次发布以来发生的变化”

**为什么会有这个步骤（案例研究——ABF基板，2026-02-07）：**

Kirk在2月5日发布了一条包含10条推文的帖子，讨论了高盛关于ABF短缺的报告（从10%增加到21%，Kinsus/NYPCB/Unimicron）。2月7日，管道使用了相同的高盛报告，生成了一条包含相同数字、相同公司和相同角度的3条推文。如果我们没有先查看已发布的帖子，就会在有其他10个新鲜主题角度的情况下浪费了一次管道运行时间。**

### 何时使用
- 筛选10份以上的PDF以找到相关内容
- 寻找跨文档之间的联系
- 从多个来源构建论点
- 尚不清楚哪些PDF重要

### 如何扫描
```
1. Check published threads (Step 1a.0 above)

2. List recent PDF folders and count PDFs
   ls /Users/Shared/ksvc/pdfs/ | tail -5
   ls /Users/Shared/ksvc/pdfs/YYYYMMDD/ | wc -l

3. Symlink PDFs into project directory (REQUIRED for subagent access)
   ln -sf "/Users/Shared/ksvc/pdfs/YYYYMMDD" ".claude/pdfs-scan"

4. Split PDFs into groups and spawn parallel Explore agents
   TARGET: ~5 PDFs per agent. Spawn ALL agents in a single message.
   - Each agent gets a specific list of filenames to scan
   - All agents run simultaneously → total time = slowest agent
   - Haiku is cheap — more agents = faster with no meaningful cost increase
```

### 代理数量分配

| PDF数量 | 代理数量 | 每个代理处理的PDF数量 | 预计时间 |
|------|--------|-----------|---------------|
| ≤5 | 1 | 所有PDF | 约25秒 |
| 6-10 | 2 | 每个代理约5份PDF | 约25秒 |
| 11-15 | 3 | 每个代理约5份PDF | 约25秒 |
| 16-20 | 4 | 每个代理约5份PDF | 约25秒 |
| 21-30 | 5-6 | 每个代理约5份PDF | 约30秒 |

**为什么每个代理处理5份PDF是最佳选择？** 这是速度的平衡点。每份PDF的阅读和总结大约需要4-8秒。每个代理处理5份PDF大约需要25秒。增加每个代理处理的PDF数量并不会节省时间（总标记数量不变），但会延长处理时间。

**成本：** Haiku工具成本较低。4个代理 × 5份PDF × 每份PDF约4,000个标记 = 总共约80,000个输入标记——与1个代理处理所有20份PDF的成本相同。并行处理是免费的。**

**跨文档综合的权衡：** 每个代理只能看到自己的批次，因此跨批次的主题分析是主代理的工作。这没关系——主代理无论如何都会合并所有结果。**

### 示例：启动Explore代理

**步骤1：主代理创建符号链接并列出PDF文件：**
```bash
ln -sf "/Users/Shared/ksvc/pdfs/20260205" ".claude/pdfs-scan"
/bin/ls ".claude/pdfs-scan/"
```

**步骤2：将文件名分组并并行启动代理（单条消息，多个Task调用）：**
```
# Agent 1 — first batch
Task(subagent_type="Explore", prompt="""
**THOROUGHNESS: medium**

Scan these specific PDFs for content angles:
- file1.pdf
- file2.pdf
- file3.pdf
- file4.pdf
- file5.pdf
- file6.pdf
- file7.pdf

For each PDF, Read enough pages to understand the full thesis (use judgment — some need 1-2 pages, others 1-5):

Read(file_path="/Users/dydo/Documents/agent/ksvc-intern/.claude/pdfs-scan/FILENAME.pdf", pages="1-5")

For each PDF extract:
- Company/sector, ticker, rating, price target
- Key thesis and supporting numbers
- Supply chain connections
- Potential content angles

After scanning your batch, provide:
1. Per-PDF summary (2-3 sentences each)
2. Cross-document themes within your batch
3. Which PDFs are most relevant for deep extraction
""")

# Agent 2 — second batch (SPAWN IN SAME MESSAGE as Agent 1)
Task(subagent_type="Explore", prompt="""
... same prompt with file8.pdf through file14.pdf ...
""")

# Agent 3 — third batch (SPAWN IN SAME MESSAGE)
Task(subagent_type="Explore", prompt="""
... same prompt with file15.pdf through file20.pdf ...
""")
```

**步骤3：主代理整合所有代理的结果：**
所有代理返回后，主代理：
1. 合并每份PDF的总结
2. 识别代理1和代理2发现的共同主题
3. 选择所有PDF中的前3个内容角度
4. 选择2-5份PDF进行步骤1b的深度提取

### 输出：确定哪些PDF重要
扫描完成后，你将知道：
- 哪些报告的数据最准确
- 跨文档之间的联系（例如，“3份报告确认了内存短缺”）
- **论点推荐**（2-3个值得深入探讨的角度）
- 哪些PDF需要使用RLM进行深度提取

**⚠️ 警告：** Explore代理可能会产生错误的数字。** 在RLM验证之前，将Explore总结中的所有数字视为“未经验证的声明”。组件数量、百分比和市场规模尤其容易出错。**

**容量（2026-02-07测试结果）：** 单个Explore代理（haiku）在83秒内处理了19份PDF，详细程度中等，使用了125,000个标记（第1-5页每页约4,000个标记）。3个代理并行处理相同批次大约需要30-40秒。**

---

## 步骤1b：使用RLM进行深度提取

使用RLM从步骤1a中识别出的特定PDF进行**深度提取**。

**对于你将要发布的任何内容，这一步都是必须执行的。** Explore代理负责总结；RLM负责验证。**

**何时使用**
- 你知道哪些2-5份PDF最重要
- 需要具体的数字、图表、表格
- 构建跨文档的验证表格
- 提取技术细节（如fab产量、收益率、WPM）

### 单份PDF
```bash
cd ~/.claude/skills/rlm-repl/scripts
python3 rlm_repl.py init "/Users/Shared/ksvc/pdfs/YYYYMMDD/file.pdf" --extract-images
python3 rlm_repl.py exec -c "print(grep('revenue|growth|target|price', max_matches=20, window=200))"
```

### 多份PDF（综合处理）
```bash
cd ~/.claude/skills/rlm-repl-multi/scripts
python3 rlm_repl.py init "/path/to/report1.pdf" --name report1 --extract-images
python3 rlm_repl.py init "/path/to/report2.pdf" --name report2 --extract-images
python3 rlm_repl.py exec -c "results = grep_all('keyword', max_matches_per_context=20)"
```

### 查看提取的图表/图片
```bash
# List images from a context
python3 rlm_repl.py exec --name report1 -c "print(list_images())"

# Get image path, then use Read tool to view
python3 rlm_repl.py exec --name report1 -c "print(get_image(0))"
```

图表通常包含关键数据（产量/价格趋势、利润率历史、产能时间线），这些数据是文本提取无法捕捉到的。

### 提取验证（必须执行）

**⚠️ 在每次`rlm_repl.py init`之后，验证提取是否成功。**

RLM在初始化后会报告`chars_extracted`。一份多页的分析师报告应该包含数千个字符。如果提取的字符数量异常少，那么该PDF很可能是基于图片的，RLM可能只提取了元数据和标题。

**验证规则：**

| 提取的字符数量 | 预期的报告类型 | 应采取的行动 |
|----------------|---------------------|--------|
| > 5,000 | 多页报告 | ✅ 继续使用grep进行验证 |
| 1,000 - 5,000 | 短篇笔记/部分内容 | ⚠️ 查看`list_images()` —— 如果有很多图片，触发备用方法 |
| < 1,000 | 基于图片的PDF | ❌ **必须使用读取工具进行备用处理** |

**阈值取决于上下文。** 一份20页的高盛报告如果只提取了666个字符，显然是有问题的。一份1页的定价表如果提取了800个字符，可能是正常的。需要根据实际情况判断，但如果有疑问，请使用备用方法。**

**当RLM提取结果较少时，必须执行的备用方法：**

```bash
# Step 1: RLM init (always try first)
python3 rlm_repl.py init "/path/to/report.pdf" --extract-images
# Output: "Extracted 666 chars from 15 pages, saved 9 images"

# Step 2: Check - is 666 chars enough for a 15-page report? NO.
# → Trigger fallback

# Step 3: Check extracted images first (they may contain the data)
python3 rlm_repl.py exec -c "print(list_images())"
# View extracted images with Read tool
# Read(file_path="/path/to/extracted/image-0.png")

# Step 4: Read the PDF directly (use symlinked path for subagents)
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="1-10")
# Read(file_path=".claude/pdfs-scan/report.pdf", pages="11-20")
```

**⚠️ 路径规则：** 子代理必须通过符号链接的项目路径（`.claude/pdfs-scan/`）读取PDF，** **不得从`/Users/Shared/`路径读取。**请参阅上面的“子代理权限”部分。**

**为什么会有这个步骤（案例研究——ABF基板短缺，2026-02-07）：**

高盛发布了两份报告：一份是关于ABF产能上升的报告（71K字符，提取正常），另一份是关于Kinsus的升级报告（15页，但只提取了666个字符）。我们跳过了Kinsus的报告，因为“主要报告包含了我们需要的所有信息”。但实际上Kinsus的报告包含了独特的数据（公司特定的产能计划、利润率指导、订单簿细节），这些数据本可以增强帖子的内容。跳过这份报告是偷懒的行为——使用读取工具的备用方法只需要30秒就可以获取到这些数据。**

**规则：**
1. **切勿仅仅因为RLM提取结果较少就忽略相关的PDF。** 使用备用方法。
2. **检查提取的图片。** 使用`--extract-images`选项时，RLM通常可以提取图表/表格图片。**
3. **记录备用方法的使用情况。** 在提取缓存中记录`"extraction_method": "read_fallback"，以便审计人员知道数据来源。**
4. **如果备用方法也失败了**（PDF损坏或受数字版权管理保护）：** **记录下来并继续处理。**但你必须尝试。**

### RLM缓存：包含视觉数据

在提取数据时，捕获**所有**可能用于后续图表生成的数据类型：

| 数据类型 | 需要提取的内容 | 缓存格式 |
|-------------|-----------------|--------------|
| 文本数字 | 带有页码引用的确切引用 | `{"value": 5.3, "unit": "B", "source": "p.3", "quote": "規模約53億美元"}` |
| 表格 | 完整的表格作为结构化JSON | `{"columns": [...]], "rows": [...]`, "source": "p.20"}` |
| 图表 | 数据点 + 图表来源路径 | `{"data": {...}, "source_image": "pdf-3-1.png", "page": 3}` |

**为什么需要缓存视觉数据？** 第6步（图表生成）需要这些数据。如果你只缓存文本，就会丢失表格结构和图表数据点。**

## 跨文档推理
通过跨多个报告对比观点来构建论点：
```bash
# Find where multiple reports discuss the same topic
python3 rlm_repl.py exec -c "results = grep_all('DRAM.*price|ASP', max_matches_per_context=5)"

# Compare forecasts across sources
python3 rlm_repl.py exec -c "results = grep_all('2026|2027|growth|demand', max_matches_per_context=5)"
```

使用跨文档方法来验证：
- 多个来源是否对价格预测达成一致？
- 供应限制的时间线是否一致？
- 报告之间是否存在矛盾？**

---

## 步骤1b.5：构建提取缓存（必须执行）

**⚠️ 为什么会有这个步骤：** RLM在提取过程中会创建`state.pkl`文件，但在写作阶段（步骤3）无法访问它。如果没有持久的缓存，编写者会依赖内存，从而导致错误，例如产品类型错误、时间段缺失或来源归属错误。**

**这个步骤的作用：** 从`state.pkl`（RLM的内部格式）中提取数据，并将其转换为带有上下文标签的结构化JSON格式，以便写作阶段可以使用。**

**何时执行**
**在步骤1b（RLM提取）之后和步骤3（写作）之前。**

| 工作流程 | 何时缓存 |
|----------|---------------|
| 单份PDF（rlm-repl） | 在`rlm_repl.py init`完成后 |
| 多份PDF（rlm-repl-multi） | 在所有`init`命令完成后 |

## 如何构建缓存

**v2的新功能：** 自动从PDF文件名生成来源标签和归属映射！**

**单份PDF（rlm-repl）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Auto-extracts from default rlm-repl state location
python3 build_extraction_cache.py \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**多份PDF（rlm-repl-multi）：**
```bash
cd ~/.claude/skills/kirk-content-pipeline/scripts

# Use --multi flag to load from rlm-repl-multi state
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json
```

**在跨文档综合时（可选）：**
```bash
# Add manual synthesis descriptions for cross-doc insights
python3 build_extraction_cache.py \
  --multi \
  --output /path/to/draft-assets/rlm-extraction-cache.json \
  --synthesis /path/to/cross-doc-synthesis.json
```

**综合格式**（针对复杂的多来源帖子，可选）：
```json
{
  "dual_squeeze_thesis": {
    "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
    "components": [
      {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
      {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
    ]
  }
}
```

**自动生成的内容：**
- ✅ 从PDF文件名生成来源标签（例如：“GFHK - Memory.pdf” → 标签：“GFHK”）
- ✅ 包含主要来源、关键指标和来源上下文的标签 |
- ✅ 包含完整上下文的提取条目（产品类型、时间周期、单位）**

### 缓存格式

缓存包括**上下文标签**和**归属映射**，以防止常见错误：

```json
{
  "cache_version": "1.0",
  "generated_at": "2026-02-05T14:00:00",
  "sources": [
    {
      "source_id": "gfhk_memory",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/GFHK - Memory.pdf",
      "pdf_name": "GFHK - Memory price impact.pdf",
      "tag": "GFHK",
      "chars_extracted": 13199
    },
    {
      "source_id": "goldman_abf",
      "pdf_path": "/Users/Shared/ksvc/pdfs/20260204/Goldman ABF shortage.pdf",
      "pdf_name": "Goldman Sachs ABF shortage report.pdf",
      "tag": "Goldman Sachs",
      "chars_extracted": 25000
    }
  ],
  "extractions": [
    {
      "entry_id": "mem_001",
      "source_id": "gfhk_memory",
      "figure": "Figure 2",
      "page": 3,
      "metric": "Total BOM",
      "product_type": "HGX B300 8-GPU server",
      "time_period": "3Q25 → 1Q26E",
      "units": "dollars per server",
      "scope": "single HGX B300 8-GPU server",
      "values": {
        "before": "$369k",
        "after": "$408k",
        "change": "+$39k"
      },
      "context": "Memory price impact on AI server BOM",
      "source_quote": "Figure 2: HGX B300 8-GPU server BOM...",
      "verification": "RLM grep + visual inspection"
    }
  ],
  "source_attribution_map": {
    "topics": {
      "Memory Pricing": {
        "primary_source": "gfhk_memory",
        "tag": "GFHK",
        "key_metrics": ["HBM3e ASP", "DDR5-6400 (128GB)", "NVMe SSD (3.84TB)", "Total BOM"],
        "source_context": "Figures: Figure 2; Time periods: 3Q25 → 1Q26E",
        "notes": "4 extractions from this source"
      },
      "Abf Shortage": {
        "primary_source": "goldman_abf",
        "tag": "Goldman Sachs",
        "key_metrics": ["ABF shortage ratio", "Kinsus PT", "NYPCB PT", "Unimicron PT"],
        "source_context": "Time periods: 2H26, 2027, 2028",
        "notes": "5 extractions from this source"
      }
    },
    "cross_doc_synthesis": {
      "dual_squeeze_thesis": {
        "description": "Memory shortage (1Q26) + ABF substrate shortage (2H26) = compounding AI server bottleneck",
        "components": [
          {"topic": "Memory Pricing", "source": "gfhk_memory", "timeframe": "1Q26"},
          {"topic": "Abf Shortage", "source": "goldman_abf", "timeframe": "2H26-2028"}
        ]
      }
    }
  }
}
```

**防止错误的关键字段：**
- `product_type`：当来源提到“HGX B300机架”时，防止显示为“GB300 rack”
- `time_period`：当来源提到“3Q25 → 1Q26E”时，防止时间段缺失
- `source_id**：当数据来自GFHK时，防止显示为“Goldman的BOM”
- `tag`：从PDF文件名自动提取，以便快速归属
- `units**：当来源表示“22.5B racks”时，防止显示为“22.5bn dollars”
- `scope`：当来源表示“per rack”时，防止显示为“per server”**

**归属映射的好处：**
- `topics`：显示哪个来源是主要信息来源的层级映射
- `key_metrics`：快速查找每个来源涵盖的内容
- `source_context`：总结各个来源涵盖的时间段
- `cross_doc_synthesis**：手动连接多个来源的见解

### 与步骤3（写作）的集成**

**必须执行：** 在写作时引用缓存。**

**步骤3a：加载缓存和归属映射：**
```python
cache = load_json('rlm-extraction-cache.json')
attr_map = cache['source_attribution_map']

# Get topic attribution
topic = "Memory Pricing"
source_tag = attr_map['topics'][topic]['tag']  # "GFHK"
key_metrics = attr_map['topics'][topic]['key_metrics']
```

**步骤3b：使用缓存标签和归属信息进行写作：**
```markdown
## Content

3/ Memory squeeze is already here. GFHK's BOM breakdown (3Q25 → 1Q26E):
- HBM3e ASP: $3,756 → $4,378 (+17%)
- DDR5-6400 (128GB): $563 → $1,920 (+241%)
- HGX B300 8-GPU server BOM: $369k → $408k
```

**来源：** `rlm-extraction-cache.json`，条目`mem_001`，`mem_002`，`mem_003`

**缓存中的上下文标签：**
- 产品类型：HGX B300 8-GPU服务器（而不是GB300机架）
- 时间周期：3Q25 → 1Q26E（季度变化）
- 来源：GFHK图2（通过归属映射标签）

**归属映射的使用：**
- 使用`topics["Memory Pricing"]["tag"] → “GFHK”**
- 根据`key_metrics`列表验证

### 强制执行**
**在保存草稿之前（步骤5）：** **验证以下内容：**
- [ ] 每个发布的数字都有缓存条目
- [ ] 产品类型与缓存标签匹配
- [ ] 时间周期包含在缓存中
- [ ] 来源归属与缓存中的`source_id`和归属映射中的`tag`匹配
- [ ] 单位与缓存中的单位匹配（美元 vs 架数 vs 数据中心）
- [ ] 如果适用，引用`cross_doc_synthesis`中的交叉文档声明**

**警告标志 - 如果发现以下情况，请停止：**
- 从内存中而不是缓存中写入数字
- 产品类型与缓存中的不同（`product_type`字段）
- 当缓存中有时间周期时，时间周期缺失
- 将来源归属错误地归因于缓存中的`source_id`
- 使用错误的标签（例如，将GFHK的数据归因于“Goldman”）
- 在连接多个来源时缺少跨文档综合**

### 手动构建缓存

如果自动提取失败，手动创建缓存条目：

```json
{
  "entry_id": "manual_001",
  "source_id": "report_name",
  "metric": "Component count",
  "product_type": "Humanoid robot (dexterous hand)",
  "values": {"count": 22},
  "units": "DOF (degrees of freedom)",
  "context": "Dexterous hand articulation",
  "source_quote": "22自由度靈巧手",
  "verification": "Manual extraction from p.15",
  "notes": "Summed from finger joints (20) + wrist (2)"
}
```

**详细信息请参阅：** `~/.claude/skills/kirk-content-pipeline/scripts/README-extraction-cache.md`以获取完整文档。**

---

## 步骤1c：跨文档综合（推荐）

**为什么会有这个步骤：** 步骤1a和步骤1b生成的是每份文档的事实。** 如果没有明确的综合，管道可能会倾向于单一来源的声明（例如，“KHGEARS的市盈率为20倍”），而不是跨文档的见解（例如，“台湾经纪人对人形机器人的看法比西方分析师更乐观”）。**

## 何时使用

| 情景 | 是否使用1c？ |
|----------|---------|
| 多份PDF讨论同一主题 | **是** |
| 比较不同经纪人的观点 | **是** |
| 寻找共识/分歧 | **是** |
| 单份PDF的深入分析 | **否**（跳到步骤2） |
| 突发新闻（速度很重要） | **否**（跳到步骤2） |

## 1c的输出类型 | 示例 | 审计要求 |
|-------------|---------|-------------------|
| **共识声明** | “3家经纪人都认为2H26年的DRAM ASP在上升” | 跨文档（rlm-multi） |
| **比较性见解** | “HIWIN的市盈率为38倍，而KHGEARS为20倍——市场定价是否合理” | 跨文档（rlm-multi） |
| **分歧标志** | “微软表示中立，当地经纪人建议买入——谁是对的？” | 跨文档（rlm-multi） |
| **综合论点** | “台湾供应链被低估，与中国同行相比” | 跨文档（rlm-multi） |

## 如何运行跨文档综合

```bash
cd ~/.claude/skills/rlm-repl-multi/scripts

# Initialize all relevant PDFs
python3 rlm_repl.py init "/path/to/broker1.pdf" --name broker1
python3 rlm_repl.py init "/path/to/broker2.pdf" --name broker2
python3 rlm_repl.py init "/path/to/broker3.pdf" --name broker3

# Ask synthesis questions (not just extraction)
python3 rlm_repl.py exec -c "
# Question 1: Do they agree on market sizing?
market_data = grep_all('market size|TAM|規模|billion|億', max_matches_per_context=10)
print('=== MARKET SIZE ACROSS SOURCES ===')
print(market_data)
"

python3 rlm_repl.py exec -c "
# Question 2: Compare recommendations
ratings = grep_all('BUY|SELL|NEUTRAL|買進|賣出|中立|rating|recommendation', max_matches_per_context=10)
print('=== RATINGS COMPARISON ===')
print(ratings)
"

python3 rlm_repl.py exec -c "
# Question 3: Find disagreements
pe_data = grep_all('P/E|PE|本益比|target price|目標價', max_matches_per_context=10)
print('=== VALUATION COMPARISON ===')
print(pe_data)
"
```

### 需要提出的综合问题**

| 类别 | 问题 |
|----------|-----------|
| **共识** | 来源是否对[市场规模 / 时间线 / 关键风险]达成一致？ |
| **比较** | [经纪人A]的观点与[经纪人B]有何不同？ |
| **估值** | 当地分析师和外国分析师的定价是否一致？ |
| **时间线** | 来源是否对[催化剂 / 转折点]达成一致？ |
| **风险** | 一个来源提到了哪些其他来源没有提到的风险？ |

## 输出格式：综合缓存

运行步骤1c后，记录步骤3（写作）所需的综合见解：

```markdown
## Cross-Doc Synthesis (Step 1c)

**Sources:** broker1 (永豐), broker2 (MS), broker3 (Citi)

### Consensus
- Market size: All 3 agree on $5-6B (2025) → $30-35B (2029)
- CAGR: 55-60% range across all sources

### Disagreements
- HIWIN: MS says NEUTRAL (38x too rich), 永豐 silent, Citi no coverage
- Timeline: 永豐 more bullish on 2026 ramp, MS cautious until 2027

### Comparative Insights (use in thread)
- "Taiwan brokers (永豐) bullish on KHGEARS; Western analysts (MS) more cautious on HIWIN"
- "Local coverage sees 2026 inflection; foreign houses waiting for 2027 proof points"

### Audit Flag
These synthesized claims require cross-doc verification in Step 4b:
- [ ] "3 sources agree on market size" → verify all 3 sources
- [ ] "Local vs foreign view divergence" → verify specific ratings from each
```

## 与审计的集成（步骤4a）

**⚠️ 重要提示：** 步骤1c中的综合声明必须在步骤4a中进行跨文档审计。**

在审计清单中，用`cross-doc: true`标记这些声明：

```markdown
## Claims to Verify

| # | Claim | Type | Source ID | Cross-Doc? |
|---|-------|------|-----------|------------|
| 1 | KHGEARS P/E 20x | P/E | src1 | No |
| 2 | Market consensus $5.3B | Consensus | src1, src2, src3 | **Yes** |
| 3 | Local vs foreign view divergence | Synthesis | src1, src2 | **Yes** |
```

跨文档声明使用`rlm-repl-multi`进行验证，而不是使用并行的单个文档代理。**

---

### 提取技术细节
深入挖掘特定PDF时，提取以下内容：
- 晶圆产能（WPM）
- 制造厂名称（M15X, P4L, X2）
- 产量百分比
- 工艺节点（1b, 1c）
- 每个单位的组件数量

| 问题 | 提取内容 |
|----------|---------|
| 什么 | 一句话的总结 |
| 为什么 | 为什么读者应该关心 |
| 谁 | 受影响的公司/股票代码 |
| 何时 | 时间段（具体季度） |
| 在哪里 | 制造厂位置、地理位置 |
| 如何 | 带有技术细节的机制 |

---

## 步骤2：初步检查KSVC的持股情况**

**⚠️ 重要提示：** 这只是一个初步检查。在编写内容之后，你必须执行步骤4c（最终持股情况验证），以确保在提取过程中发现的任何股票代码都是正确的。**

### 所有模型（共7个）
- **美国模型：** usa-model1 ~ usa-model5（5个模型）
- **台湾（TWSE）模型：** twse-model1 ~ twse-model2（2个模型）

### 步骤2a：识别所有可能的股票代码**

**在查询API之前，** **识别该公司的所有可能标识符：**

```bash
# Example: Global Unichip Corp
# Identifiers to search:
# - US ticker: N/A (not US-listed)
# - Taiwan ticker: 3443
# - Chinese name: 創意 or 全球晶圓科技
# - English name: Global Unichip, GUC
# - Stock code: 3443 TW (TWSE format)

# For Taiwan stocks, verify ticker via TWSE API first:
curl -s "https://www.twse.com.tw/en/api/codeQuery?query=3443"
# Returns: {"query":"3443","suggestions":["3443\tGUC"]}
```

**规则：**
1. **美国股票：** 仅通过股票代码搜索（例如，“MU”，“AMD”，“NVDA”）
2. **台湾股票：** 通过股票代码搜索（例如，“3443”）——在API中可能显示为“3443 創意”**
3. **如果不确定：** 同时检查美国和TWSE的模型**

### 步骤2b：查询所有7个模型**

**切勿在没有检查所有7个模型的情况下假设某只股票未被持有。**

**推荐：** 使用tradebook获取准确的入场价格和当前状态**

```bash
# FASTEST METHOD: Check tradebook for entry price + status
# (Works for all models - US and TWSE)
curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285 or .ticker == 3491) |
  {ticker, enterDate, enterPrice, todayPrice, profitPercent, exitDate}'

# Returns:
# {
#   "ticker": 6285,
#   "enterDate": "Wed, 28 Jan 2026 00:00:00 GMT",
#   "enterPrice": 162.0,
#   "todayPrice": 207.5,  # ⚠️ May be stale! Use Yahoo Finance for current
#   "profitPercent": 28.09,  # ⚠️ Based on stale todayPrice
#   "exitDate": null  # null = still holding
# }
```

**⚠️ 重要提示：** API的`todayPrice`和`profitPercent`可能会过时（几小时或几天之前的数据）。**始终使用Yahoo Finance API（步骤2d）验证当前价格。**

**备用方法：** 使用equitySeries（速度较慢，数据较少）**

```bash
# Check ALL 5 US models
for i in 1 2 3 4 5; do
  echo "=== USA-Model $i ==="
  curl -s "https://kicksvc.online/api/usa-model$i" | \
    jq --arg t "MU" '.equitySeries[0].series[] | select(.Ticker == $t) |
    {ticker: .Ticker, return: .data[-1].value}'
done

# Check ALL 2 TWSE models (search by stock code)
for i in 1 2; do
  echo "=== TWSE-Model $i ==="
  curl -s "https://kicksvc.online/api/twse-model$i" | \
    jq '.equitySeries[0].series[] | select(.Ticker | contains("3443")) |
    {ticker: .Ticker, return: .data[-1].value}'
done
```

**为什么仍然使用equitySeries？**
1. **历史追踪：** 显示随时间的回报百分比变化（`.data[]`数组）
2. **验证：** 确认持仓是否仍然有效
3. **备用方法：** 如果tradebook不可用或为空**
4. **入场日期的确定：** 第一个数据点（回报约为0）表示入场日期

**示例：从equitySeries中查找入场日期**
```bash
# Get all data points to find entry date
curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285")) | .data[0]'
# Returns: {"date": "2026-01-28 00:00:00", "value": 0}
# Entry date: Jan 28, 2026
```

### 步骤2c：验证和备用策略**

**使用所有三个数据来源以确保准确性：**

| 数据来源 | 何时使用 | 显示什么 | 限制 |
|-------------|-------------|---------------|------------|
| **tradebook** | 主要来源 | 入场日期、入场价格、退出状态 | `todayPrice`可能过时 |
| **equitySeries** | 验证 | 随时间的回报百分比，持仓状态 | 没有入场价格/日期 |
| **filledOrders** | 备用方法 | 实际交易订单、价格 | 如果模型未重新设置，则为空 |

**推荐的工作流程：**

```bash
# 1. PRIMARY: Get entry details from tradebook
TRADEBOOK=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285)')

# 2. VERIFY: Cross-check with equitySeries
EQUITY=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285"))')

# 3. FALLBACK: If tradebook empty, check filledOrders
if [ -z "$TRADEBOOK" ]; then
  curl -s "https://kicksvc.online/api/twse-model2" | \
    jq '.filledOrders[] | select(.ticker | contains("6285"))'
fi
```

**跨验证示例：**

```bash
# Check if tradebook and equitySeries agree on position status
TRADEBOOK_HELD=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.tradebook[] | select(.ticker == 6285 and .exitDate == null) | .ticker')

EQUITY_HELD=$(curl -s "https://kicksvc.online/api/twse-model2" | \
  jq '.equitySeries[0].series[] | select(.Ticker | contains("6285")) | .Ticker')

# If both show position, high confidence
# If only one shows position, investigate discrepancy
```

**备用方法：** 如果tradebook为空****

如果equitySeries为空或tradebook为空（虽然罕见，但在模型重置后可能发生）：

```bash
# Check ALL US models - filledOrders
for i in 1 2 3 4 5; do
  echo "=== USA-Model $i filledOrders ==="
  curl -s "https://kicksvc.online/api/usa-model$i" | \
    jq '.filledOrders[] | select(.ticker == "MU") | {ticker, price, quantity}'
done

# Check ALL TWSE models - filledOrders
for i in 1 2; do
  echo "=== TWSE-Model $i filledOrders ==="
  curl -s "https://kicksvc.online/api/twse-model$i" | \
    jq '.filledOrders[] | select(.ticker | contains("3443")) | {ticker, price, quantity}'
done
```

**当数据来源不一致时：**

| 情况 | 行动 |
|----------|--------|
| tradebook显示持仓，equitySeries未显示持仓 | 信任tradebook（equitySeries可能延迟） |
| equitySeries显示持仓，tradebook未显示持仓 | 调查——检查filledOrders |
| filledOrders显示买入但当前无持仓 | 持仓已关闭——检查tradebook.exitDate |
| 三个数据来源都为空 | 该模型中未持有该股票 |

### 步骤2e：使用准确的回报记录持股情况**

**重要提示：** 始终使用以下方法计算实际回报：**
1. **入场价格** 来自`tradebook.enterPrice`
2. **当前价格** 来自Yahoo Finance API（不要使用KSVC API的过时`todayPrice`）

**输出格式（使用准确数据）：**
```markdown
**KSVC Holdings Check:**
- ✅ WNC (6285.TW) - Held in TWSE Model 2
  - Entry: Jan 28, 2026 @ NT$162
  - Current: NT$187 (Yahoo Finance)
  - Gain: +15.4% (actual, not API's stale 28%)
- ✅ UMT (3491.TWO) - Held in TWSE Model 2
  - Entry: Jan 28, 2026 @ NT$1,120
  - Current: NT$1,280 (Yahoo Finance)
  - Gain: +14.3% (actual, not API's stale 23%)
- ❌ Not held in TWSE Model 1 or USA Models 1-5

**Note:** API's equitySeries and tradebook.todayPrice can lag hours/days behind market.
Always use Yahoo Finance for current prices.
```

**如果在任何模型中都没有持有该股票：**
```markdown
**KSVC Holdings Check:**
- ❌ Not held in any of 7 models (checked USA 1-5, TWSE 1-2)
- Content angle: Industry analysis / Market observation
```

### 集成策略**

| 情况 | 方法 | 示例 |
|-----------|----------|---------|
| **持有（美国股票）** | 显示持仓情况 | “KSVC Model1以$412的价格持有MU” |
| **持有（台湾股票）** | 显示持仓情况 | “KSVC台股Model1持有台積電 (2330)” |
| **未持有** | 行业说明 | “Memory cycle使MU的回报增加了$MU” |
| **胜利总结** | “自从Model1添加MU以来，$MU上涨了15%” |

### 步骤2d：当前价格检查（Yahoo Finance API - 必须执行）**

**⚠️ 重要提示：** 始终使用Yahoo Finance获取当前价格。** KSVC API的`todayPrice`可能会过时。**

**美国股票：**
```bash
# Get current price
TICKER="MU"
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | \
  jq '.chart.result[0].meta.regularMarketPrice'

# Get full market data
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'
```

**台湾股票（使用.TW或.TWO后缀）：**
```bash
# WNC (6285.TW)
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/6285.TW?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'

# UMT (3491.TWO - OTC stocks use .TWO)
curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/3491.TWO?interval=1d&range=1d" | \
  jq '.chart.result[0].meta | {symbol, regularMarketPrice, currency, regularMarketTime}'
```

**台湾股票的后缀：**
- `.TW` - 在台湾证券交易所（TWSE）上市 |
- `.TWO` - 在台北证券交易所（TPEx/OTC）上市 |

**计算实际收益（不要使用API的过时利润%）：**
```bash
# Example: WNC
TICKER="6285.TW"
ENTRY=162  # From tradebook.enterPrice
CURRENT=$(curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/$TICKER?interval=1d&range=1d" | jq '.chart.result[0].meta.regularMarketPrice')
echo "$TICKER: NT\$$CURRENT | Entry: NT\$$ENTRY | Gain: $(awk "BEGIN {printf \"%.1f\", ($CURRENT - $ENTRY) / $ENTRY * 100}")%"

# Output: 6285.TW: NT$187 | Entry: NT$162 | Gain: +15.4%
```

**完整的工作流程（tradebook + Yahoo Finance）：**
```bash
# 1. Get entry price from tradebook
ENTRY=$(curl -s "https://kicksvc.online/api/twse-model2" | jq '.tradebook[] | select(.ticker == 6285) | .enterPrice')

# 2. Get current price from Yahoo Finance
CURRENT=$(curl -s -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/6285.TW?interval=1d&range=1d" | jq '.chart.result[0].meta.regularMarketPrice')

# 3. Calculate actual gain
echo "Entry: NT\$$ENTRY | Current: NT\$$CURRENT | Gain: $(awk "BEGIN {printf \"%.1f\", ($CURRENT - $ENTRY) / $ENTRY * 100}")%"
```

---

## 步骤3：编写内容**

**有关完整模板和示例，请参阅`references/kirk-voice.md`。**

### 帖子编号规范

| 格式 | 适用场景 |
|--------|-------------|
| 推文1中没有编号 | 建议使用——这样更容易吸引注意力，如果被引用或分享则可以独立显示 |
| `2/`, `3/`, etc. | 标准的帖子格式——表示“2中的第N个” |
| 推文1中使用`1/` | 可选——明确表示“即将发布新的帖子” |

**为什么在推文1中不使用编号：**
- 吸引注意力的推文经常被单独分享
- “1/”在上下文中看起来不完整
- 更清晰的视觉呈现

**格式偏好：** 使用`/`而不是`)`——这是Twitter帖子的约定格式。**

```
✅ Recommended:
Humanoid robots going from science fair to factory floor. Taiwan supply chain getting interesting.

2/ TLDR:
- Market: $5.3B (2025) to $32.4B (2029)...

❌ Avoid:
1/ Humanoid robots going from science fair...
```

### 选择内容类型
1. 内容类型是什么？（长篇分析 / 快速总结 / 突发新闻 / 恶搞帖子 / 评论 / 胜利总结）
2. 在kirk-voice.md中查找相应的格式
3. 应用相应的风格混合

### 技术细节

❌ 含糊的表述：**“NAND供应紧张”**

✅ 具体的表述：**“YMTC在武汉的工厂3增加了135k WPM的产能。但仍然无法缩小差距——三星的X2转换推迟到第二季度。”**

❌ 含糊的表述：**“HBM的利润率很好”**

✅ 具体的表述：**“SK Hynix的HBM利润率在80-90%。三星在1c DRAM的利润率仅为60%。”**

始终包括：具体的数字、时间框架、制造厂名称、比较内容。

### 参考文献的清晰性（2026-02-08学习）

**在引用对象尚未介绍时，** **切勿使用含糊的代词或缩写。**

在帖子格式中，每条推文可能可以独立阅读。如果之前的推文将某个概念作为一个类别讨论（例如，“ASIC收入”），在后面的推文中突然将其称为“该项目”，读者可能不知道“该项目”指的是什么。

❌ 含糊的表述：**“微软认为该项目是3nm的Google TPU”**
（哪个项目？帖子中从未提到过“该项目”。）

✅ 清晰的表述：**“微软认为主要客户/项目是3nm的Google TPU”**
（明确指出微软认为的是哪个项目以及他们在做什么。）

**规则：** 当使用缩写（如“该项目”、“这个交易”、“这个策略”）可以节省文字，但可能会影响清晰度。直接说明具体内容总是值得的。即使多几个词，也可以避免读者需要重新阅读。**

**在从一般类别转向具体内容时：** 如果帖子首先讨论一个抽象类别（如ASIC收入、内存供应），然后转向一个具体的实体（如Google TPU、三星的工厂），需要建立过渡。不要假设读者已经知道具体的内容。**

---

## 步骤4a：审计（必须执行——必须使用子代理）

**⚠️ 为什么会有这个步骤：** 我们发现RLM提取（步骤1b）和验证不同。** Explore代理可能会产生错误的数字。编写者会进行推断。这个步骤可以在发布之前发现错误。**

**⚠️ 结构性限制：** 你（主代理）是编写者。你不能同时担任审计者。你必须将审计任务委托给处于新上下文的子代理。有关原因，请参阅审计内容技能中的“WARM STATE TRAP”部分。**

### 步骤4a的流程（3个步骤，按顺序执行）

**步骤1：生成审计清单**
```
Write audit-manifest.md with all claims, sources, and search hints.
This is the handoff document for the audit agents.
```

**步骤2：启动Explore代理（必须执行——不要跳过这一步）**
```
Spawn 1 Explore agent per source PDF via Task tool.
Each agent gets: the manifest + its assigned PDF path + claim list.
Each agent returns: JSON with PASS/FAIL/UNSOURCED per claim.
```

**⚠️ WARM STATE TRAP：** 如果在步骤1b之后已经加载了RLM，你可能会想“自己直接进行grep”。** **不要这样做。** 审计内容技能解释了原因：是你编写了草稿，所以你已经“知道”答案。自我审计是一种确认偏见，而不是真正的验证。**

**自我检查：** 如果你在步骤4a中准备输入`rlm_repl.py exec`，请停止。**你正在跳过这个步骤。**

**步骤3：收集结果并编写审计报告**
```
Aggregate agent results into audit-report.md.
MUST include audit_agent_ids from the Task tool responses.
If audit_agent_ids is empty, the audit is invalid.
```

### 调用审计内容技能以获取完整流程细节：**
```
/audit-content
```

### 需要验证的内容**

| 声明类型 | 示例 | 如何验证 |
|------------|---------|---------------|
| 公司名称 | “KHGEARS” | RLM grep + TWSE API |
| 股票代码格式 | “4571 TW” | TWSE API |
| 数字 | “62 harmonic reducers” | RLM grep精确计数 |
| 百分比 | “19%成本” | RLM在来源中grep确认 |
| 市盈率 | “20x” | RLM grep分析师目标 |
| 评级 | “BUY” | RLM grep推荐 |
| 时间线 | “2H27” | RLM grep + 核实上下文 |
| 归属 | “运输到X” | 必须在来源中明确说明，不能推断 |

**何时继续**
- **所有通过**：保存草稿（步骤5） |
- **任何失败**：修正声明，重新审计 |
- **未确认的来源**：要么删除声明，添加备注（“据报道”），或者找到来源**

**不要保存状态为FAIL的草稿。** 未确认的声明需要明确的决定。**

## 步骤4a.5：使用Gemini进行网络交叉验证（推荐）

**