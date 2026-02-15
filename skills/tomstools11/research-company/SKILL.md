---
name: research-company
description: 这是一家专注于B2B企业研究的机构，专门提供专业的PDF报告服务。当客户需要对公司进行调研、分析其业务状况、创建公司资料档案，或根据公司网站URL生成市场情报时，我们能够提供相应的服务。我们出具的PDF报告格式精美、易于下载，能够满足客户的所有需求。
---

# 公司研究

从公司提供的网址生成格式规范的PDF账户研究报告。

## 工作流程

1. **研究** 公司信息（通过网页抓取和搜索）
2. **构建** JSON数据结构
3. **使用`scripts/generate_report.py`生成PDF文件
4. **将PDF文件交付给用户**

## 第一阶段：研究（并行执行）

同时执行以下搜索操作，以减少上下文信息的依赖：

```
WebFetch: [company URL]
WebSearch: "[company name] funding news 2024"
WebSearch: "[company name] competitors market"
WebSearch: "[company name] CEO founder leadership"
```

从网站中提取以下信息：公司名称、所属行业、总部所在地、成立时间、管理层信息、产品/服务、定价模式、目标客户群体、案例研究、用户评价以及最新新闻。

## 第二阶段：构建数据结构

创建符合以下JSON模式的数据结构（详细规范请参见`references/data-schema.md`）：

```json
{
  "company_name": "...",
  "source_url": "...",
  "report_date": "January 20, 2026",
  "executive_summary": "3-5 sentences...",
  "profile": { "name": "...", "industry": "...", ... },
  "products": { "offerings": [...], "differentiators": [...] },
  "target_market": { "segments": "...", "verticals": [...] },
  "use_cases": [{ "title": "...", "description": "..." }],
  "competitors": [{ "name": "...", "strengths": "...", "differentiation": "..." }],
  "industry": { "trends": [...], "opportunities": [...], "challenges": [...] },
  "developments": [{ "date": "...", "title": "...", "description": "..." }],
  "lead_gen": { "keywords": {...}, "outreach_angles": [...] },
  "info_gaps": ["..."]
}
```

## 第三阶段：生成PDF文件

```bash
# Install if needed
pip install reportlab

# Save JSON to temp file
cat > /tmp/research_data.json << 'EOF'
{...your JSON data...}
EOF

# Generate PDF
python3 scripts/generate_report.py /tmp/research_data.json /path/to/output/report.pdf
```

## 第四阶段：交付结果

将生成的PDF文件保存在工作区文件夹中，并提供下载链接：
```
[Download Company Research Report](computer:///sessions/.../report.pdf)
```

## 质量标准

- **准确性**：所有信息均基于可验证的证据；需引用来源。
- **具体性**：包含产品名称、关键指标以及客户案例。
- **完整性**：对于无法公开获取的信息，应标注为“未公开”。
- **严禁虚构**：绝不允许编造任何内容。

## 所需资源

- `scripts/generate_report.py`：PDF生成工具（使用reportlab库）
- `references/data-schema.md`：完整的JSON数据结构及示例