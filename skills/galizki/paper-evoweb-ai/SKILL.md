---
name: Scientific Article PDF Generator
description: 使用基于人工智能的研究方法和引用机制，生成可供发表的科学论文，并将其转换为PDF格式。
homepage: https://paper.evoweb.ai/?utm_source=claw&utm_medium=skill&utm_campaign=paper&utm_content=v1.0.0
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":[],"env":["EVOWEB_API_KEY"]}}}
---

# Paper.EvoWeb.ai 科学论文 PDF 生成器

使用人工智能技术，生成包含丰富内容、引用和专业格式的科学论文 PDF 文件。

## 概述

Paper.EvoWeb.ai 能将草稿文本和产品信息转化为可供发表的科学论文。该系统会为内容添加研究资料、正确的引用，并生成格式规范的 PDF 文件。

**适用场景：**科学论文、产品研究文章、白皮书、技术文档

**API 基本地址：**`https://paper.evoweb.ai`

## 认证

请在 [https://hub.oto.dev/app/register?utm_source=claw&utm_medium=skill&utm_campaign=paper&utm_content=v1.0.0](https://hub.oto.dev/app/register?utm_source=claw&utm_medium=skill&utm_campaign=paper&utm_content=v1.0.0) 获取您的 API 密钥。

**重要提示：**注册完成后，用户必须确认电子邮件地址。

API 密钥将显示在控制台的“API 密钥设置”部分。

在所有请求中都需要包含以下头部信息：
```
Access-Token: your-api-key-here
```

## 工作流程

工作流程非常简单：

1. **提交** - 提交文章参数，包括标题、产品信息和草稿文本
2. **生成** - 人工智能会根据研究资料、引用和格式要求对内容进行优化
3. **下载** - 自动接收 PDF 文件

**典型生成时间：**2-5 分钟

## API 端点

### 生成科学论文 PDF

**POST** `/`

根据提供的文本和产品信息生成科学论文 PDF。PDF 文件将以二进制格式返回，并可自动在浏览器中下载。

**请求头部信息：**
```
Access-Token: your-api-key-here
Content-Type: application/x-www-form-urlencoded
```

**请求体（form-urlencoded）：**

| 字段 | 类型 | 是否必填 | 默认值 | 说明 |
|-------|------|----------|---------|-------------|
| `article_title` | string | 是 | - | PDF 顶部的主标题（最多 200 个字符） |
| `article_subtitle` | string | 否 | - | 可选的副标题或作者/所属机构信息（最多 300 个字符） |
| `product_name` | string | 是 | - | 文章中会提及的目标产品名称（最多 120 个字符） |
| `product_url` | string (URL) | 否 | - | 产品官方页面的链接（将在引用中显示） |
| `product_url_priority` | boolean | 否 | 是 | 如果选中，该产品链接将作为主要参考来源 |
| `product_facts` | string (text) | 是 | - | 客户提供的关键事实、描述和数据 |
| `source_text` | string (text) | 是 | - | 需要扩展的基础文本草稿，支持自由格式输入 |
| `research_focus` | string | 否 | - | 用于指导输出的科研重点方向 |
| `include_sources` | boolean | 否 | 是 | 是否在文章中包含引用和来源 |
| `enable_research` | boolean | 否 | 否 | 如果启用，系统会在撰写文章前收集相关来源和引用 |
| `include_charts` | boolean | 否 | 否 | 根据研究结果生成 1-3 个数据可视化图表 |

**示例请求：**
```json
{
  "article_title": "Effects of Hyaluronic Acid on Skin Hydration",
  "article_subtitle": "A Comprehensive Review",
  "product_name": "HydraGlow Serum",
  "product_url": "https://example.com/hydraglow-serum",
  "product_url_priority": true,
  "product_facts": "Contains 2% hyaluronic acid, clinically tested on 100 participants, showed 45% improvement in skin hydration after 4 weeks, dermatologist approved, suitable for all skin types",
  "source_text": "Hyaluronic acid is a naturally occurring substance in the human body that plays a crucial role in skin hydration. This study examines the effectiveness of topical hyaluronic acid applications in improving skin moisture levels and overall skin health.",
  "research_focus": "impact on skin health and hydration levels",
  "include_sources": true,
  "enable_research": true,
  "include_charts": true
}
```

**响应（200 OK）：**
- **Content-Type:** `application/pdf`
- **Content-Disposition:** `attachment; filename="article-title.pdf"`
- **Body:** 二进制 PDF 文件数据

PDF 文件将自动在浏览器中下载。

**错误响应：**
- `400 Bad Request` - 缺少必填字段或数据无效
- `401 Unauthorized` - API 密钥无效或未提供
- `402 Payment Required` - 账户余额不足
- `500 Internal Server Error` - 生成失败

## 人工智能助手的使用说明

当用户请求生成科学论文 PDF 时，请按照以下步骤操作：

### 第一步：收集所需信息

确保收集到所有必填字段：
- **文章标题** - 清晰、描述性的论文标题
- **产品名称** - 讨论的产品名称
- **产品事实** - 关于产品的经过验证的信息和数据
- **源文本** - 需要扩展的基础文本草稿

向用户询问任何缺失的必填信息。

### 第二步：补充可选字段

鼓励用户提供以下信息：
- **文章副标题** - 添加作者姓名、所属机构或副标题
- **产品 URL** - 用于引用的产品官方页面链接
- **科研重点** - 需要强调的具体研究方向

### 第三步：配置生成选项

询问用户的偏好设置：
- **启用深度研究模式** (`enable_research`) - 收集外部来源和引用（耗时较长但内容更全面）
- **包含图表** (`include_charts`) - 添加 1-3 个数据可视化图表
- **包含来源** (`include_sources`) - 在文章中添加参考文献部分

**默认推荐设置：**
- `include_sources: true` - 始终包含引用
- `enable_research: true` - 适用于全面的文章
- `include_charts: false` - 仅在数据可视化有价值时使用

### 第四步：提交请求

使用 `POST /` 方法，将所有参数以表单编码（form-urlencoded）的形式发送。

**重要提示：**响应结果是一个二进制 PDF 文件。请妥善处理：
- 告知用户 PDF 正在生成中
- 文件将在浏览器中自动下载
- 生成通常需要 2-5 分钟

### 第五步：通知用户

告知用户：
- PDF 生成已经开始
- 预计完成时间（2-5 分钟）
- 文件完成后会自动下载

**示例消息：**
```
📄 Generating your scientific article PDF now!

Title: "Effects of Hyaluronic Acid on Skin Hydration"
Product: HydraGlow Serum
Options: Deep research mode enabled, charts included

⏱️ This typically takes 3-5 minutes. The PDF will download automatically when ready.
```

### 第六步：处理错误

如果请求失败：
- 明确显示错误信息
- 对于 `400 Bad Request` - 检查必填字段和数据格式
- 对于 `401 Unauthorized` - 验证 API 密钥
- 对于 `402 Payment Required` - 用户需要通过 [https://paper.evoweb.ai/](https://paper.evoweb.ai/) 添加积分
- 对于 `500 Internal Server Error` - 建议重新尝试或简化请求

## 示例用法

### 产品研究文章
```
User: "Create a scientific paper about our new anti-aging cream"

Required info:
- Article title: "Clinical Evaluation of Advanced Retinol Complex in Anti-Aging Treatment"
- Article subtitle: "A 12-Week Study on Wrinkle Reduction and Skin Elasticity"
- Product name: "AgeLess Retinol Cream"
- Product facts: "Contains 0.5% retinol, tested on 150 participants aged 35-65, showed 38% reduction in fine lines, 42% improvement in skin elasticity, dermatologically tested"
- Source text: "Retinol has been recognized as one of the most effective anti-aging ingredients in skincare. This clinical study evaluates the effectiveness of a novel retinol formulation..."
- Research focus: "anti-aging effects and wrinkle reduction"
- Enable research: true
- Include charts: true
```

### 产品对比研究
```
User: "Need a paper comparing different protein supplements"

Required info:
- Article title: "Comparative Analysis of Whey Protein Isolate Formulations"
- Product name: "PureFit Whey Protein"
- Product facts: "99% protein purity, 25g protein per serving, contains all essential amino acids, lactose-free, tested for heavy metals"
- Source text: "Protein supplementation is crucial for muscle recovery and growth. This paper examines various protein sources and their bioavailability..."
- Research focus: "protein absorption rates and muscle recovery"
- Enable research: true
```

### B2B 白皮书
```
User: "Write a white paper about our enterprise software solution"

Required info:
- Article title: "Improving Enterprise Productivity Through AI-Powered Workflow Automation"
- Article subtitle: "A Technical White Paper"
- Product name: "WorkflowPro AI"
- Product url: "https://example.com/workflowpro"
- Product facts: "Reduces manual task processing by 65%, integrates with 200+ enterprise tools, processes 1M+ tasks monthly, 99.9% uptime SLA"
- Source text: "Modern enterprises face increasing pressure to optimize workflows and reduce operational costs. This white paper presents a comprehensive analysis..."
- Research focus: "workflow automation and ROI in enterprise environments"
- Enable research: true
- Include charts: true
```

## 最佳实践

### 撰写有效的文章内容

✅ **应该做到：**
- 提供清晰、基于事实的产品信息
- 包含具体的数字和经过验证的数据
- 撰写包含关键点的全面源文本
- 为特定内容指定科研重点
- 对于全面的文章，启用深度研究模式

❌ **不应该这样做：**
- 提交模糊或未经验证的信息
- 提供极少量的源文本
- 忽略重要的产品细节
- 期望人工智能编造数据或事实

### 产品事实编写指南

请包含具体、可衡量的信息：
- （如有）临床试验结果
- 成分和浓度
- 目标受众或使用场景
- 认证或批准信息
- 性能指标
- 安全性信息

**示例：**
```
Good: "Contains 10% vitamin C, clinically tested on 200 participants, showed 52% improvement in skin brightness after 8 weeks, dermatologically approved, suitable for sensitive skin"

Poor: "Good vitamin C product that works well"
```

### 选择生成选项

**在以下情况下启用深度研究模式：**
- 创建全面的科研论文
- 需要外部引用和参考文献
- 主题需要科学依据支持
- 更注重内容质量而非速度

**在以下情况下包含图表：**
- 展示统计数据
- 比较多个产品或研究结果
- 可视化趋势或结果
- 数据有助于增强理解

**在以下情况下包含来源：**
- 面向学术或专业读者
- 需要保证可信度
- 需要引用外部研究
- 增强声明的可信度

### 标题编写技巧

创建清晰、专业的标题：
- 使用描述性、具体的语言
- 包含关键词（产品类型、好处、研究类型）
- 保持 200 个字符以内
- 遵循学术标题的编写规范

**示例：**
- “局部维生素 C 在治疗色素沉着中的临床疗效：一项为期 12 周的研究”
- “植物蛋白来源对运动表现的比较分析”
- “益生菌在消化健康中的作用：综述”

## 技术细节

- **协议：** HTTPS REST API
- **格式：** 表单编码输入，PDF 二进制输出
- **认证：** 基于头部的 API 密钥
- **响应：** 二进制 PDF 文件，支持自动下载
- **生成时间：** 通常为 2-5 分钟
- **字段长度限制：** 见上述参数表
- **费用：** 每次生成需要消耗积分（详情请参见 [https://paper.evoweb.ai/](https://paper.evoweb.ai/)）

## 文件下载处理

PDF 响应中包含以下头部信息：
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="sanitized-article-title.pdf"
```

文件名会根据文章标题自动生成：
- 首字母大写
- 空格会转换为连字符
- 无效字符会被删除
- 名称长度限制在 100 个字符以内
- 如果标题为空，文件名默认为 `article-config.pdf`

## 支持与资源

- **获取 API 密钥：** [https://hub.oto.dev/app/register?utm_source=claw&utm_medium=skill&utm_campaign=paper&utm_content=v1.0.0](https://hub.oto.dev/app/register?utm_source=claw&utm_medium=skill&utm_campaign=paper&utm_content=v1.0.0)
- **官方网站：** [https://paper.evoweb.ai/](https://paper.evoweb.ai/)
- **API 相关问题：** 联系 Paper.EvoWeb.ai 客服
- **账户/计费：** 访问 [https://paper.evoweb.ai/](https://paper.evoweb.ai/)

## 注意事项

- 每次生成都会消耗账户中的积分
- PDF 的质量取决于输入内容的质量（详细的事实和源文本会产生更好的效果）
- 深度研究模式耗时较长，但内容更全面
- 图表会根据产品事实和研究结果生成
- 所有内容均为人工智能生成，发布前需进行审核
- 当 `product_url_priority` 为 `true` 时，系统会优先使用产品链接作为参考来源

---

**准备好生成可供发表的科学论文了！** 📄✨