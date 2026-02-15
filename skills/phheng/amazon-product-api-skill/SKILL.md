---
name: amazon-product-api-skill
description: 从亚马逊提取结构化产品列表，包括产品标题、ASIN（Amazon商品编号）、价格、评分和规格信息。当用户需要执行以下操作时，可以使用此功能：  
1) 在亚马逊上搜索[产品名称]；  
2) 查找[品牌名称]的热销产品；  
3) 监控[商品名称]的价格变化；  
4) 获取评分较高的[产品类别]列表；  
5) 在亚马逊上比较[品牌A]和[品牌B]的产品；  
6) 提取亚马逊产品数据用于市场研究；  
7) 在特定语言/市场平台上查找[产品名称]；  
8) 分析[关键词]相关产品的竞争对手定价情况；  
9) 查找[搜索词]的推荐产品；  
10) 获取[产品列表]的技术规格（如材质、颜色等）。
---

# Amazon 产品 API 技能

该技能允许您通过一次 API 请求从亚马逊搜索结果中提取结构化产品数据，无需使用复杂的爬虫或手动输入数据。

## ✨ 主要特点

- **一站式集成**：可通过 API 将产品结果直接导入您的定价数据库、商业智能仪表板、竞争对手跟踪系统或自动化工作流程中。
- **零维护成本**：无需编写爬虫脚本、设置代理或处理反爬虫机制。
- **适用于生产环境的输出**：返回一致且结构化的数据，便于自动化处理和监控。
- **专为工作流程设计**：非常适合用于价格比较、产品研究、目录监控和商品营销分析。

## 🔑 API 密钥设置

使用此技能需要一个 `BROWSERACT_API_KEY`。

### 环境变量检查
相关脚本会自动检查 `BROWSERACT_API_KEY` 环境变量的是否存在。

### 如何获取 API 密钥
1. 在 [BrowserAct](https://www.browseract.com/) 注册/登录。
2. 转到 [API 与集成](https://www.browseract.com/reception/integrations) 部分以获取您的 API 密钥。
3. 将密钥设置到您的环境变量中：
   ```powershell
   $env:BROWSERACT_API_KEY = "your-api-key-here"
   ```

## 📥 输入参数

| 参数 | 类型 | 描述 | 示例 |
|-----------|------|-------------|---------|
| `KeyWords` | 字符串 | 用于在亚马逊上搜索产品的关键词。 | `phone`, `wireless earbuds` |
| `Brand` | 字符串 | 按品牌名称筛选产品。 | `Apple`, `Samsung`, `Sony` |
| `Maximum_number_of_page_turns` | 数字 | 要分页显示的搜索结果页数。 | `1`, `3` |
| `language` | 字符串 | 亚马逊浏览会话的用户界面语言。 | `en`, `de`, `zh-CN` |

## 🚀 调用方法

您可以使用提供的 Python 脚本来触发此技能：

```bash
python -u .cursor/skills/amazon-product-api-skill/scripts/amazon_product_api.py --keywords "laptop" --brand "Dell" --pages 1 --lang "en"
```

## 📊 输出数据

脚本返回一个包含以下字段的产品 JSON 数组：

- `product_title`：产品名称。
- `asin`：亚马逊标准识别码（唯一标识符）。
- `product_url`：产品详情页面的 URL。
- `brand`：品牌名称。
- `price_current_amount`：当前售价。
- `price_original_amount`：原价（如有）。
- `rating_average`：平均评分。
- `rating_count`：评分总数。
- `featured`：是否为推广/特色商品。
- `color`, `material`, `style`：产品属性（如有）。

## 🛠 错误处理与重试机制

- **授权无效**：如果 API 密钥错误或已过期，脚本会捕获“授权无效”的错误，并提示您检查配置。
- **网络问题**：脚本内置了针对常见网络超时的重试逻辑。
- **任务失败**：如果服务器端出现故障，脚本会报告失败状态及任何可用的错误详情。