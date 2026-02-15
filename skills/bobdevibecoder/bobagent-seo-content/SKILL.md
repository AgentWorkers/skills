---
name: seo-content
description: "为已部署的微SaaS产品生成SEO优化过的博客文章和 landing 页面。进行关键词研究，撰写相关内容，并将这些内容发布到产品的博客上。这些内容可以每周通过cron作业自动发布，也可以根据需要手动发布。"
metadata: { "openclaw": { "emoji": "📝" } }
---

# SEO内容生成引擎

该工具专为microsaas-factory skill开发的微SaaS产品生成高质量、经过SEO优化的博客文章和登录页面。内容是吸引自然流量（即通过Google搜索获得的流量）的主要途径，也是产品增长的关键驱动力。

## 执行模式

### 生成模式（默认模式）
为特定产品生成新的博客文章。
**触发命令**：`"write content for [产品名称]"` 或 `"generate blog posts for [产品名称]"`

### 关键词研究模式
为产品的目标用户群体研究高价值关键词。
**触发命令**：`"find keywords for [产品名称]"`

### 批量模式（通过cron任务执行）
每周为每个产品自动生成2-3篇博客文章。
**触发条件**：每周自动执行的cron作业

---

## 内容策略

针对每个产品，按优先级生成以下类型的内容：

### 第一层：转化型内容（优先生成）
1. **“如何[完成某项操作]”**——使用该产品的逐步教程
   - 例如：《如何将JSON转换为CSV——免费在线工具》
2. **“2026年最佳[工具类型]工具”**——以我们的产品作为首选的列表文章
   - 例如：《2026年最佳JSON到CSV转换工具（免费和付费版）》
3. **“[我们的产品] vs [竞争对手]”**——对比文章
   - 例如：《ConvertFlow vs Zamzar：哪个JSON转换工具更优秀？`

### 第二层：教育型内容（次优先生成）
4. **“[格式/概念]是什么？”**——科普性内容
   - 例如：《什么是JSON？初学者指南》
5. **“[格式A] vs [格式B]”**——格式对比
   - 例如：《JSON vs CSV：何时使用哪种格式？`

### 第三层：吸引型内容（最后生成）
6. **“[目标受众]的工作流程技巧”**——工作流程指南
   - 例如：《开发人员的数据转换技巧》

---

## 内容生成流程

### 第1步：读取产品信息
从`/home/node/.openclaw/workspace/skills/microsaas-factory/data/products.json`文件中读取产品详情。

### 第2步：研究关键词
通过网络搜索找到：
- 主关键词（具有明确购买意图的关键词，例如：“json to csv converter”）
- 3-5个相关关键词
- 2-3个长尾关键词（例如：“convert json to csv online free”）
- 竞争产品的名称以供对比

运行关键词辅助工具：
```bash
node /home/node/.openclaw/workspace/skills/seo-content/scripts/keyword_research.js "[product-type]"
```

### 第3步：生成博客文章
按照以下结构创建JSON文件：
```json
{
  "title": "How to Convert JSON to CSV: Complete Guide (2026)",
  "description": "Learn the fastest ways to convert JSON data to CSV format. Free online tool, API access, and step-by-step instructions.",
  "date": "2026-02-03",
  "tags": ["guide", "json", "csv"],
  "sections": [
    {
      "heading": "Section Title with Keywords",
      "content": "2-4 paragraphs of genuinely useful content. Not fluff. Not keyword-stuffed. Write like a developer explaining to another developer."
    }
  ]
}
```

### 第4步：保存到产品目录
将生成的JSON文件保存到产品的博客内容目录中：
```bash
node /home/node/.openclaw/workspace/skills/seo-content/scripts/save_blog_post.js [product-slug] [post-slug] '[post-json]'
```

### 第5步：重新部署产品
添加内容后，触发重新部署操作：
```bash
cd /home/milad/[product-slug] && source ~/.nvm/nvm.sh && vercel --prod --yes 2>&1
```

### 第6步：发送通知
通过Telegram发送通知：
```
📝 New blog post published!

Product: [name]
Title: [post title]
URL: [product-url]/blog/[post-slug]
Keywords: [primary], [secondary1], [secondary2]

Posts for this product: [total count]
```

---

## 内容规则

### SEO规则
1. 标题中必须自然包含主关键词
2. 标题长度应在50-65个字符之间
3. 描述（meta标签）长度应在140-160个字符之间
4. 在第一节中使用主关键词
5. 在子标题中使用次要关键词
6. 每个段落长度应在100-200个单词之间
7. 整篇文章字数应在800-1500字之间（包含5-7个段落）
8. 包含一个引导用户返回产品的行动号召（CTA）

### 质量规则
1. 写出真正有用的内容，避免SEO垃圾信息
2. 在适当的地方添加具体的示例和代码片段
3. 保证技术内容的准确性
4. 避免冗长或无意义的段落
5. 以资深开发者的角度向新手解释相关内容
6. 每个段落都应提供可操作的信息
7. 绝不生成虚假的推荐或评价

### 格式规则
1. 内容以JSON格式存储，而非Markdown格式
2. 每个段落都应有标题和正文
3. 使用`\n`进行换行
4. 标签数量控制在3-5个相关术语以内
5. 日期应显示为YYYY-MM-DD格式

---

## 关键词研究指南

在研究关键词时，请遵循以下原则：
- **意图匹配**：例如，“convert json to csv”比“what is json”更具购买意图
- **关键词的搜索量与竞争程度**：选择搜索量适中、竞争较小的关键词
- **优先选择长尾关键词**：例如，“convert json to csv online free”比“json converter”更容易被搜索引擎收录
- **结合信息性和交易性内容**：同时发布“如何操作”类文章和“最佳工具”类文章

---

## 内容发布计划

为每个产品制定以下发布计划：
- **第1周**：发布“如何[完成某项操作”指南和“2026年最佳[工具]”列表文章
- **第2周**：发布“[产品] vs [竞争对手]”对比文章
- **第3周**：发布“[格式A] vs [格式B]”科普文章
- **第4周**：发布“[目标受众]的工作流程技巧”指南

之后根据新的关键词和主题重复上述流程。

---

## 错误处理机制
- 如果在`products.json`中找不到相关产品：报告错误并列出可用的产品
- 如果网络搜索失败：仅根据产品配置生成内容（跳过关键词研究步骤）
- 如果部署失败：将内容保存到本地并报告错误——这些内容可以手动重新部署
- 如果博客目录不存在：创建相应的目录