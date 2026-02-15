---
name: notebooklm
description: 使用此技能，您可以通过 Google NotebookLM 的 AI 功能分析您的本地文件。上传业务文档、报告和策略，以获得基于数据的洞察、风险分析以及可操作的建议。该工具非常适合用于商业智能、文档分析和决策支持。
license: Complete terms in LICENSE.txt
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# NotebookLM 本地文件分析工具

使用 Google NotebookLM 的人工智能功能分析您的本地文档，以获取基于数据的洞察、风险评估和可操作的建议。只需上传一次文件，之后便可多次从不同角度进行查询。

## 适用场景

当用户需要以下情况时，可以使用此工具：
- 拥有本地业务文档（如战略计划、财务报告、提案等）
- 希望对特定文档进行带有数据支持的 AI 分析
- 需要风险评估、竞争分析或业务洞察
- 希望同时分析多个相关文档
- 需要从业务文档中提取可操作的见解

## 快速入门

### 第一步：一次性设置
```bash
python scripts/setup_notebooklm.py
```

### 第二步：分析文件

**批量分析（推荐）：**
```bash
python scripts/batch_analyzer.py "your/folder" --pattern "*.md"
```

**单文件分析：**
```bash
python scripts/local_analyzer.py "file.md" --upload
```

**查询已上传的文档：**
```bash
python scripts/quick_query.py "What are the key risks in this business plan?" --notebook-url "notebook-url"
```

## 核心工作流程

### 工作流程 1：业务文档分析
上传业务文档以获取战略洞察：
```bash
# Analyze business strategy files
python scripts/batch_analyzer.py "Business/Strategy" --pattern "*.md"

# Upload high-priority files to NotebookLM
python scripts/local_analyzer.py "strategy_plan.md" --upload

# Get strategic insights
python scripts/quick_query.py "Identify 3 competitive advantages and implementation challenges" --notebook-url "url"
```

### 工作流程 2：财务分析
分析财务文档以识别风险和机会：
```bash
# Find financial documents
python scripts/batch_analyzer.py "Finance" --pattern "*.md"

# Query for financial insights
python scripts/quick_query.py "What are the key financial risks and ROI projections?" --notebook-url "url"
```

### 工作流程 3：风险与合规性分析
获取风险评估和合规性洞察：
```bash
python scripts/quick_query.py "What compliance or regulatory issues should be addressed?" --notebook-url "url"
python scripts/quick_query.py "Identify top 5 risks and mitigation strategies" --notebook-url "url"
```

## 辅助脚本（黑盒使用）

### `scripts/batch_analyzer.py`
分析整个目录并识别高价值文件：
```bash
python scripts/batch_analyzer.py "directory" --pattern "*.md" --output "analysis_report.md"
```

**功能：**
- **文件分类**：业务策略、财务、技术、法律、营销
- **优先级识别**：突出显示需要上传的高价值文件
- **工作流程指导**：提供分步分析建议
- **报告生成**：创建结构化的分析报告

### `scripts/local_analyzer.py`
上传并分析单个文件：
```bash
python scripts/local_analyzer.py "file.md" --upload
python scripts/local_analyzer.py "file.md" --notebook-url "url" --question "Custom question"
```

**功能：**
- **上传指南**：提供逐步的 NotebookLM 上传说明
- **文件分析**：提供元数据和文件大小信息
- **自定义查询**：支持针对性的分析问题

### `scripts/quick_query.py`
查询已上传的文档：
```bash
python scripts/quick_query.py "question" --notebook-url "url"
```

**功能：**
- **直接查询**：针对已上传的文档提出具体问题
- **数据支持**：从文件中获取有依据的答案
- **Unicode 处理**：支持多种操作系统

## 强大的应用场景

### 业务策略分析
```bash
# Upload strategy documents
python scripts/local_analyzer.py "strategy_document.md" --upload

# Get strategic insights
python scripts/quick_query.py "What competitive advantages does this strategy establish?" --notebook-url "url"
python scripts/quick_query.py "Identify 3-5 actionable insights and implementation timeline" --notebook-url "url"
```

### 财务风险评估
```bash
# Upload financial documents
python scripts/local_analyzer.py "financial_report.md" --upload

# Get financial analysis
python scripts/quick_query.py "Summarize financial implications and ROI projections" --notebook-url "url"
python scripts/quick_query.py "What are the top financial risks and mitigation strategies?" --notebook-url "url"
```

### 提案与合同分析
```bash
# Upload legal/business documents
python scripts/local_analyzer.py "proposal_document.md" --upload

# Get compliance insights
python scripts/quick_query.py "What compliance or regulatory issues should be addressed?" --notebook-url "url"
python scripts/quick_query.py "Identify potential legal risks and recommended safeguards" --notebook-url "url"
```

## 标准操作流程 (SOP)

### 第一步：文档发现
1. 对文档目录执行批量分析：
   ```bash
   python scripts/batch_analyzer.py "your/document/folder" --pattern "*.md"
   ```
2. 查看文件分类——按类别识别高价值文件
3. 选择优先级文档——重点关注战略、财务和法律文档

### 第二步：文档上传
1. 访问 NotebookLM（https://notebooklm.google.com）
2. 创建一个描述性强的新笔记本（例如：“Q4 业务分析”）
3. 上传第一步中识别出的优先级文档
4. 将相关文档分组（战略、财务、法律）以获得更好的分析背景
5. 复制笔记本 URL 以供后续查询

### 第三步：提取洞察
根据文档类型提出具体问题：

**战略文档：**
- “主要的竞争优势和市场机会是什么？”
- “识别实施挑战及建议的解决方案”
- “成功的衡量标准和里程碑是什么？”

**财务文档：**
- “总结关键财务指标和预测”
- “主要财务风险及应对策略是什么？”
- “投资回报率（ROI）和增长机会有哪些？”

**法律/合规文档：**
- “必须满足哪些合规要求和截止日期？”
- “识别潜在的法律风险及建议的防范措施”
- “哪些监管问题需要立即关注？”

**提案/合同：**
- “主要的责任和义务是什么？”
- “识别潜在风险和谈判要点”
- “成功的标准和绩效指标是什么？”

### 第四步：行动计划制定
1. 综合相关文档的洞察
2. 根据分析结果制定行动事项清单
3. 为识别出的风险制定应对策略
4. 对关键指标和里程碑进行监控

## 常见误区

❌ **不要仅用于简单阅读文档**——请使用专门的阅读工具
❌ **不要上传敏感的个人信息**——NotebookLM 是 Google 服务
❌ **不要期望实时结果**——分析基于上传的文档
❌ **不要忽略文件大小限制**——请检查 NotebookLM 的上传限制
❌ **不要忘记整理文档**——将相关文件分组以便更好地进行分析

✅ **始终将相关文档一起上传**——以便更好地进行分析
✅ **提出具体、有针对性的问题**——比泛化查询更有效
✅ **先进行批量分析**——在上传前识别高价值文件
✅ **创建单独的笔记本**——按项目或文档类型进行分类
✅ **通过后续问题深入挖掘洞察**

## 最佳实践

1. **先进行批量分析**——确定哪些文档适合进行 AI 分析
2. **将相关文档分组**——将战略、财务和法律文档一起上传
3. **提出具体问题**——例如“有哪些风险？”而不是“分析这个文件”
4. **创建专注的笔记本**——每个项目或业务领域一个笔记本
5. **使用后续问题**——每次查询都基于之前的分析结果
6. **提取可操作的见解**——关注可采取的行动
7. **记录分析结果**——保存关键见解以供将来参考

## 文件类型支持

**推荐格式：**
- Markdown (.md)——最适合结构化文档
- PDF——报告、合同、正式文件
- Word (.docx)——业务文档和提案
- 普通文本 (.txt)——笔记和文档

**最适合分析的文档类型：**
- 业务计划和战略文档
- 财务报告和预算
- 法律协议和合同
- 项目提案和规范
- 市场研究和分析报告

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 找到太多文件 | 使用特定模式：`--pattern "*strategy*.md"` |
| 上传失败 | 检查文件大小限制和格式兼容性 |
| 回答过于笼统 | 提出更具体的关于业务影响的问题 |
| 分析范围太广 | 专注于特定方面（风险、机会、合规性） |
| 缺少背景信息 | 将相关文档一起上传以获得更好的分析结果 |
| 编码错误 | 脚本会自动处理 Unicode 问题 |

## 集成说明

- **Claude Code**：用于分析本地文档库
- **Claude API**：自动化文档分析工作流程
- **Claude.ai**：手动文档上传和分析界面
- **企业版**：与文档管理系统集成以实现自动化分析