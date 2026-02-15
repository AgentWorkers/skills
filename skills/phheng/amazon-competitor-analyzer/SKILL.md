---
name: amazon-competitor-analyzer
description: 使用 browseract.com 的自动化 API 从 ASIN（Amazon 商品编号）中抓取 Amazon 产品数据，并进行深入的竞争分析。通过比较产品规格、价格、用户评价以及产品展示策略，来识别竞争对手的优势和潜在弱点。
---

# 亚马逊竞争对手分析工具

该工具利用 browseract.com 的浏览器自动化 API 从用户提供的 ASIN（Amazon 商品唯一标识符）中抓取产品数据，并进行深入的竞争分析。它比较产品的规格、价格、评论质量以及视觉策略，以识别竞争对手的优势和劣势。

## 适用场景

- **竞争研究**：输入多个 ASIN 以了解市场格局
- **定价策略分析**：比较类似产品的价格区间
- **规格基准测试**：深入分析技术规格和功能差异
- **评论分析**：分析评论的质量、数量和情感倾向
- **视觉策略研究**：评估产品的主图片、A+ 评价内容以及品牌视觉效果
- **市场机会发现**：识别市场空白和潜在威胁
- **产品优化**：基于竞争分析制定优化策略
- **新产品研究**：利用市场数据支持新产品开发

## 功能概述

1. **ASIN 数据收集**：使用 BrowserAct 的工作流程模板自动提取产品标题、价格、评分、评论数量、图片等核心信息
2. **规格提取**：深入提取技术规格、功能和材料信息
3. **评论质量分析**：分析评论模式、关键词和情感倾向
4. **视觉策略评估**：评估主图片、A+ 评价页面的设计以及品牌一致性
5. **多维度比较**：并列展示产品的关键指标
6. **竞争优势识别**：找出核心竞争优势和劣势
7. **市场机会发现**：发现竞争对手的弱点和市场机会
8. **结构化输出**：生成 JSON 或 Markdown 格式的分析报告

## 特点

- **数据准确性**：预设置的工作流程确保数据提取的稳定性和准确性，避免 AI 生成的不准确信息
- **无需验证码**：内置绕过机制，无需处理 reCAPTCHA 等验证问题
- **无地理限制**：克服 IP 地理限制，实现全球稳定访问
- **执行速度快**：比纯 AI 驱动的浏览器自动化解决方案执行速度更快
- **成本效益高**：相比依赖令牌的 AI 解决方案，显著降低数据采集成本

## 先决条件

### 1. 注册 BrowserAct.com 账户并获取 API 密钥

- 访问 [browseract.com](https://browseract.com)
- 注册账户
- 进入 API 设置
- 生成 API 密钥
- 将 API 密钥安全存储（建议使用环境变量）

### 2. 配置环境变量

将 API 密钥设置为环境变量：

```bash
export BROWSERACT_API_KEY="your-api-key-here"
```

或创建一个 `.env` 文件：

```
BROWSERACT_API_KEY=your-api-key-here
```

## 使用方法

- **基本竞争分析**
- [具体步骤]

- **深入规格比较**
- [具体步骤]

- **评论质量分析**
- [具体步骤]

- **视觉策略研究**
- [具体步骤]

- **完整竞争分析**
- [具体步骤]

## 操作说明

当用户请求亚马逊竞争对手分析时：

1. **ASIN 识别与验证**：
   - 从用户输入中识别 ASIN
   - 确认 ASIN 格式符合亚马逊标准
   - 从亚马逊产品链接中提取 ASIN
   - 处理无效 ASIN 并提示用户修正

2. **调用 BrowserAct API**

3. **任务输出数据结构**

BrowserAct API 以以下格式返回结构化数据：

```json
{
  "id": "task_id_12345",
  "status": "finished",
  "created_at": "2026-02-06T10:00:00Z",
  "completed_at": "2026-02-06T10:05:00Z",
  "results": {
    "products": [
      {
        "asin": "B09XYZ12345",
        "url": "https://www.amazon.com/dp/B09XYZ12345",
        "product_info": {
          "title": "Complete product title",
          "brand": "Brand name",
          "manufacturer": "Manufacturer",
          "model": "Model"
        },
        "pricing": {
          "current_price": 29.99,
          "original_price": 39.99,
          "discount_percent": 25,
          "currency": "USD"
        },
        "reviews": {
          "average_rating": 4.5,
          "total_count": 1234,
          "rating_distribution": {
            "5_star": 65,
            "4_star": 20,
            "3_star": 10,
            "2_star": 3,
            "1_star": 2
          }
        },
        "specifications": {
          "weight": "1.5 lbs",
          "dimensions": "10 x 5 x 3 inches",
          "material": "Plastic/Metal",
          "features": ["Feature 1", "Feature 2"]
        },
        "media": {
          "main_image": "https://example.com/image.jpg",
          "thumbnails": ["url1", "url2"],
          "has_video": true,
          "has_a_plus": true
        },
        "seller": {
          "type": "Amazon",
          "fulfillment": "FBA",
          "availability": "InStock"
        }
      }
    ]
  }
}
```

### 参数配置

| 参数 | 类型 | 是否必填 | 说明 |
|---------|------|----------|-------------|
| ASIN | 字符串 | 是 | 亚马逊标准商品标识符（10 位） |
| output_format | 字符串 | 否 | 输出格式：json 或 markdown（默认：json） |
| include_reviews | 布尔值 | 否 | 是否包含评论分析（默认：true） |
| include_images | 布尔值 | 否 | 是否包含图片链接（默认：true） |
| include_specs | 布尔值 | 否 | 是否包含产品规格（默认：true） |

### 错误处理

```python
import requests

def safe_api_call(api_func, max_retries=3, delay=5):
    """Execute API call with retry logic"""
    for attempt in range(max_retries):
        try:
            result = api_func()
            if result is not None:
                return result
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    raise Exception(f"API call failed after {max_retries} attempts")


def handle_api_error(response):
    """Handle API error responses"""
    error_messages = {
        400: "Invalid request parameters",
        401: "Authentication failed - check API key",
        403: "Access denied - insufficient permissions",
        404: "Resource not found",
        429: "Rate limit exceeded - slow down",
        500: "Internal server error",
        503: "Service temporarily unavailable"
    }
    
    status_code = response.status_code
    message = error_messages.get(status_code, f"Unknown error (status: {status_code})")
    
    return {
        "error": message,
        "status_code": status_code,
        "details": response.json() if response.content else None
    }
```

### 避免请求频率过高

#### 设置请求频率限制

#### 数据提取与结构化

```json
{
  "asin": "B09XYZ12345",
  "url": "https://www.amazon.com/dp/B09XYZ12345",
  "scraped_at": "2026-02-06T10:00:00Z",
  "status": "success",
  "product_info": {
    "title": "[产品标题]",
    "brand": "[品牌名称]",
    "manufacturer": "[制造商]",
    "model": "[型号]"
  },
  "pricing": {
    "current_price": XX.XX,
    "original_price": XX.XX,
    "discount_percent": XX,
    "currency": "USD",
    "price_range": {
      "min": XX.XX,
      "max": XX.XX
    }
  },
  "reviews": {
    "average_rating": X.X,
    "total_count": XXXX,
    "rating_distribution": {
      "5_star": XX,
      "4_star": XX,
      "3_star": XX,
      "2_star": XX,
      "1_star": XX
    }
  },
  "specifications": {
    "weight": "[重量]",
    "dimensions": "[尺寸]",
    "material": "[材料]",
    "country_of_origin": "[原产地]"
  },
  "media": {
    "main_image": "[图片链接]",
    "thumbnails": ["[图片1链接]", "[图片2链接]",
    "has_video": true,
    "has_a_plus": true
  },
  "seller": {
    "type": "[亚马逊/第三方]",
    "name": "[卖家名称]",
    "fulfillment": "[FBA/自发货]",
    "availability": "[有货/缺货]"
  },
  "bestseller_rank": [
    {
      "category": "[类别]",
      "rank": XXX
    }
  ]
}
```

## 竞争分析示例

### 1. 价格维度分析

| 产品 | ASIN | 价格 | 定位 | 价格优势 |
|---------|------|-------|----------|----------------|
| [产品 A] | B09XXX | $XX.XX | 高端/中端/经济型 | 高/中/低 |
| [产品 B] | B09YYY | $XX.XX | 高端/中端/经济型 | 高/中/低 |
| [产品 C] | B09ZZZ | $XX.XX | 高端/中端/经济型 | 高/中/低 |

**价格策略分析**：
- 最低价：$XX.XX（[产品名称]）
- 最高价：$XX.XX（[产品名称]）
- 中位数价格：$XX.XX
- 价格差距：XX%

### 2. 规格比较

#### 核心参数对比

| 参数 | [产品 A] | [产品 B] | [产品 C] | 行业基准 |
|---------|-------------|-------------|-------------|-------------------|
| [参数 1] | [值] | [值] | [值] | [值] |
| [参数 2] | [值] | [值] | [值] | [值] |
| [参数 3] | [值] | [值] | [值] | [值] |

### 3. 评论分析

#### 评论质量评估

| 产品 | 总评论数 | 平均评分 | 正面评论百分比 | 负面评论百分比 | 评分指数 |
|---------|---------------|------------|------------|------------|---------------|
| [产品 A] | X,XXX | X.X | XX% | XX% | X.X |
| [产品 B] | X,XXX | X.X | XX% | XX% | X.X |
| [产品 C] | X,XXX | X.X | XX% | XX% | X.X |

#### 4. 视觉策略分析

#### 主图片评估

| 产品 | 图片风格 | 背景 | 信息密度 | 视觉吸引力 | 转化潜力 |
|---------|-------|------------|---------------------|---------------|---------------------|
| [产品 A] | [描述] | 固定/场景/透明 | 高/中/低 | 分数 | 高/中/低 |
| [产品 B] | [描述] | 固定/场景/透明 | 高/中/低 | 分数 | 高/中/低 |
| [产品 C] | [描述] | 固定/场景/透明 | 高/中/低 | 分数 | 高/中/低 |

### 5. 竞争格局总结

#### 市场定位

| 维度 | 领先者 | 挑战者 | 跟随者 | 小众市场 |
|---------|--------|------------|----------|-------|
| 销量 | [产品] | [产品] | [产品] | [产品] |
| 价格 | [产品] | [产品] | [产品] | [产品] |
| 评分 | [产品] | [产品] | [产品] | [产品] |
| 功能 | [产品] | [产品] | [产品] | [产品] |

#### 竞争优势与劣势

#### 竞争策略建议

- [产品 A] 的竞争优势
- [产品 B] 的竞争优势
- [产品 C] 的竞争优势

#### 潜在机会与风险

- [机会 1]：[描述]
- [机会 2]：[描述]
- [机会 3]：[描述]

### 报告示例

#### 分析完成时间**

**分析的产品数量**: X
**数据来源**: Amazon.com
**分析方法**: LLM 深度语义分析

```

## Best Practices

### 1. Data Collection Optimization

- **Batch Processing**: Maximum 10 ASINs per analysis to avoid rate limits
- **Delay Strategy**: 3-5 second delay between ASIN requests
- **Retry Logic**: Automatic retry, 30-second delay on failure
- **Caching**: No duplicate collection within 24 hours for same ASIN

### 2. Analysis Quality Assurance

- **Cross-Validation**: Multi-dimensional data corroboration
- **Outlier Detection**: Identify and handle anomalous data points
- **Time Dimension**: Consider product age effects
- **Market Trends**: Combine with category trend analysis

### 3. Strategy Implementation

- **Priority Ranking**: Rank recommendations by impact and feasibility
- **Resource Assessment**: Define required resources for implementation
- **ROI Estimation**: Quantify expected benefits and costs
- **Risk Assessment**: Identify potential implementation risks

### 4. Compliance and Ethics

- **Data Use Compliance**: Only for legitimate business analysis purposes
- **Platform Rules**: Respect Amazon's Terms of Service
- **Data Security**: Protect collected data appropriately
- **Information Discretion**: Do not disclose sensitive business intelligence

## Example Usage

**User Request**:
```
分析竞争对手，比较市场格局：
B09XYZ12345, B07ABC11111, B07DEF22222, B09JKL44444

```

**Output**:
```
## 竞争分析报告

### 分析概览

| 产品 | ASIN | 价格 | 评分 | 评论数 | 品牌 |
|---------|------|-------|--------|---------|-------|
| [产品 A] | B09XYZ12345 | $XX.XX | X.X | X,XXX | [品牌] |
| [产品 B] | B07ABC11111 | $XX.XX | X.X | X,XXX | [品牌] |
| [产品 C] | B07DEF22222 | $XX.XX | X.X | X,XXX | [品牌] |
| [产品 D] | B09JKL44444 | $XX.XX | X.X | X,XXX | [品牌] |

[... 完整的分析报告 ...]

---

**技能版本**: 1.0.0
**最后更新**: 2026-02-06
**兼容性**: BrowserAct API v2+
**支持网站**: Amazon.com（美国站）

---

**注意事项**

1. **数据时效性**: 亚马逊页面数据实时更新，分析结果的有效期有限
2. 可能触发亚马逊的反爬虫机制
3. 亚马逊页面布局变更可能导致数据采集失败
4. 仅支持美国站的数据
5. 评论分析基于样本，可能存在偏差
6. 部分 A+ 评价内容可能需要特殊权限
7. 实时购买框信息可能受限制
8. 无法直接获取历史价格和排名数据

## 常见问题及解决方法

- **API 调用失败**：检查 API 密钥配置和账户权限
- **任务超时**：调整 MAX_WAIT_TIME 设置
- **数据提取不完整**：延长页面加载时间或更新模板
- **分析结果异常**：检查数据完整性和比较维度合理性

## 相关技能

- `browseract-integration`：BrowserAct API 集成
- `web-scraper`：通用网页抓取工具
- `data-analyzer`：数据分析工具
- `competitor-research`：竞争对手研究工具
- `market-researcher`：市场研究工具
- `amazon-rank-tracker`：亚马逊排名跟踪工具

## 资源链接

- [BrowserAct 文档](https://browseract.com/docs)
- [BrowserAct 工作流程模板](https://www.browseract.com/template?platformType=0)
- [亚马逊产品页面最佳实践](https://developer.amazon.com/docs)
- [亚马逊卖家中心](https://sellercentral.amazon.com)
- [竞争分析框架](https://www.business.com/articles/competitive-analysis/)
- [电子商务数据分析方法](https://www.ecommerceted.com/guides/competitive-analysis/)

---

**技能版本**: 1.0.0
**最后更新**: 2026-02-06