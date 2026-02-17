---
name: lead-scorer
description: >
  **Score Leads 0-100**  
  该工具通过分析网站的域名信息（DNS）、站点地图（sitemap）以及社交媒体影响力来对潜在客户进行评分（0-100分）。  
  - **支持自定义评分规则**：用户可以自定义哪些指标对他们的品牌至关重要，从而制定个性化的评分标准。  
  - **适用于多种场景**：适用于筛选潜在客户、确定优先联系对象或评估合作伙伴时使用。  
  - **灵活的数据处理方式**：支持单个域名、多个域名的评分，同时也支持批量处理（CSV格式导入）。  
  **主要功能：**  
  1. **全面评估**：综合考虑网站的域名信息、DNS设置、站点地图结构以及社交媒体表现。  
  2. **高度可定制**：允许用户根据自身需求调整评分权重和规则。  
  3. **高效管理**：便于快速筛选和优先处理潜在客户。  
  4. **多平台支持**：适用于多种平台或数据源。  
  **适用场景：**  
  - **潜在客户筛选**：帮助企业快速识别有价值的潜在客户。  
  - **资源分配**：根据评分结果合理分配营销资源。  
  - **合作伙伴评估**：评估潜在合作伙伴的资质。  
  **技术优势：**  
  - **精确性**：基于客观数据进行分析，确保评分结果的准确性。  
  - **灵活性**：用户可根据实际需求灵活调整评分策略。  
  - **批量处理**：支持高效处理大量数据。
---
# 领先评分器（Lead Scorer）

该工具用于分析域名并返回0-100的领先评分，同时提供详细的评分明细。其主要特点是支持**可定制的评分配置文件**——这些配置文件以JSON格式定义了哪些评估指标重要以及它们的权重。

## 工作原理

1. **DNS分析**：检查MX记录（适用于Google Workspace/M365等企业环境），以及SPF/DMARC设置。
2. **站点地图解析**：统计URL数量、最后修改时间以及网站内容量。
3. **网站抓取**：检测是否存在博客、分析技术栈、元标签、社交链接和联系方式。
4. **指标评分**：根据预设的权重对各项指标进行评分。
5. **评分等级划分**：A（80-100分）、B（60-79分）、C（40-59分）、D（20-39分）、F（0-19分）。

## 依赖项
```bash
pip3 install dnspython
```

## 使用方法

### 单个域名（使用默认配置文件）
```bash
python3 scripts/score_lead.py example.com
```

### 使用自定义配置文件
```bash
python3 scripts/score_lead.py example.com --profile clearscope.json
```

### 多个域名
```bash
python3 scripts/score_lead.py domain1.com domain2.com domain3.com
```

### 从CSV文件批量处理
```bash
python3 scripts/score_lead.py --csv leads.csv --domain-column "Website"
```

### 命令行参数
- `--profile FILE`：评分配置文件的路径（默认为`default.json`，位于`scripts/profiles/`目录下）
- `--csv FILE`：包含域名的CSV文件
- `--domain-column NAME`：CSV文件中域名的列名（默认为`domain`）
- `--scrape-delay SECONDS`：HTTP请求之间的延迟时间（默认为0.5秒）
- `--output FILE`：将结果写入指定文件而非标准输出（stdout）

## 输出结果

输出结果为JSON格式，包含总体评分、各指标的详细得分、原始数据以及总结信息：
```json
{
  "domain": "example.com",
  "score": 72,
  "grade": "B",
  "profile": "default",
  "signals": {
    "has_blog": {"score": 20, "max": 20, "evidence": "Blog found at /blog; 234 URLs in sitemap"},
    "business_legitimacy": {"score": 15, "max": 20, "evidence": "MX: Google Workspace; SPF configured"}
  },
  "raw_data": {
    "sitemap_urls": 234,
    "mx_provider": "Google Workspace",
    "tech_stack": ["WordPress", "Cloudflare"]
  },
  "summary": "Strong in: has blog, business legitimacy. Good lead, worth pursuing."
}
```

## 评分配置文件

评分配置文件是该工具的核心功能。通过这些文件，您可以定义**哪些评估指标对您的需求最为重要**。

### 配置文件格式
```json
{
  "name": "my-profile",
  "description": "What this profile scores for",
  "signals": {
    "signal_name": {
      "weight": 25,
      "description": "What this signal measures",
      "keywords": ["optional", "keyword", "list"]
    }
  }
}
```

### 内置评估指标

| 指标            | 评估内容                                                                 |
|-----------------|-------------------------------------------------------------------------------------------------------------------------|
| `has_blog`       | 是否存在博客或内容部分；站点地图的更新频率                                                                                         |
| `business_legitimacy`    | MX提供商、SPF/DMARC设置、关于页面内容、元标签                                                                                         |
| `content_velocity`    | 站点地图的更新日期（最近性和频率）                                                                                         |
| `tech_stack`       | 页面源代码中检测到的内容管理系统（CMS）、分析工具（analytics）、聊天工具（chat tools）                                                                                   |
| `audience_size`     | 网站上的社交媒体链接（Twitter、LinkedIn、YouTube、Facebook）                                                                                   |
| `contact_findability` | 是否有联系页面、网站上的电子邮件地址以及LinkedIn链接                                                                                   |
| `seo_tools`       | 主页文本中是否包含关键词（需要`keywords`参数）                                                                                         |

### 自定义关键词评估指标

任何带有`keywords`参数的指标都会将指定关键词与首页文本进行匹配。通过这种方式，您可以识别竞争对手、相关工具或行业术语。

### 提供的配置文件示例

- `default.json`：适用于所有SaaS或内容相关公司的通用评分配置文件。
- `clearscope.json`：专为SEO工具合作项目设计的示例配置文件。

您可以在`scripts/profiles/`目录下创建自己的配置文件，或通过`--profile`参数指定配置文件的路径。

## 速率限制

该脚本默认采用较为温和的请求策略：
- `--scrape-delay 0.5`：每次HTTP请求之间的延迟为500毫秒（默认值）。
- 每个域名大约会发送5-8次请求（包括首页、博客、关于页面、联系页面、站点地图和DNS信息）。
- 批量处理时，不同域名之间会有额外的延迟。
- 对于大量域名，可以增加延迟时间：`--scrape-delay 2`。
- 所有请求均使用统一的User-Agent字符串。

### 推荐的延迟设置

| 批量处理规模 | 延迟时间（秒） | 大约处理时间（分钟）                                                                 |
|-------------|-------------|-------------------------------------------------------------------------------------------------------------------------|
| 1-10个域名    | 0.5秒（默认）      | 约30秒至2分钟                                                                                   |
| 10-50个域名    | 1.0秒        | 约5至15分钟                                                                                   |
| 50个以上域名    | 2.0秒        | 约30分钟以上                                                                                   |

## 错误处理

如果某个指标无法获取数据（例如网站无法访问、DNS请求超时等），该指标的得分将为0，并在日志中说明原因。即使某个域名处理失败，脚本也不会崩溃，而是会将错误信息记录到标准错误输出（stderr）并继续执行其他域名。

## 使用建议

- **先使用默认配置文件进行测试，根据结果再自定义配置**。
- 为了便于理解评分结果，各指标的权重之和应等于100（虽然不是强制要求，系统会自动进行归一化处理）。
- **关键词非常有用**：可以添加竞争对手名称、行业术语或技术相关词汇。
- **使用jq进行快速数据过滤**：例如：`python3 scripts/score_lead.py domain.com | jq '.score'`。
- **批量处理后进行排序**：先对结果进行评分，再按评分顺序排序，以便优先处理重点域名。