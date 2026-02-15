---
name: amazon-asin-lookup-api-skill
description: 该技能帮助用户通过特定的ASIN（Amazon标准识别码）从亚马逊网站中提取结构化产品信息。当用户需要执行以下操作时，可以使用该技能：  
1. 根据ASIN获取亚马逊产品详情；  
2. 使用ASIN查询亚马逊产品标题和价格；  
3. 提取特定ASIN的产品评分和评论数量；  
4. 检查特定ASIN产品的库存情况和当前价格；  
5. 通过ASIN获取亚马逊产品描述和功能信息；  
6. 利用ASIN将产品信息添加到产品目录中；  
7. 监控特定ASIN产品的价格变化；  
8. 获取产品的品牌和材质信息；  
9. 根据ASIN获取产品的图片和规格信息；  
10. 验证ASIN的有效性并获取产品的元数据。
---

# 亚马逊ASIN查询技能

## 📖 介绍
该技能利用BrowserAct的亚马逊ASIN查询API模板，提供了一种从亚马逊获取产品信息的便捷方式。只需提供ASIN，即可将产品标题、价格、评分、品牌和详细描述等结构化数据直接提取到您的应用程序中，而无需进行手动抓取。

## ✨ 特点
1. **数据可靠，无错误**：采用预定义的工作流程，确保数据提取的准确性，避免AI生成错误。
2. **无需验证码**：内置机制可绕过reCAPTCHA和其他机器人检测系统。
3. **全球访问，无地域限制**：克服IP限制，确保从任何地点都能稳定访问。
4. **执行速度快**：比通用AI浏览器自动化工具更高效。
5. **成本效益高**：相比高token消耗的AI模型，降低了数据获取成本。

## 🔑 API密钥工作流程
在运行该技能之前，必须检查`BROWSERACT_API_KEY`环境变量。如果未设置，请先向用户获取API密钥。
**代理指令**：
> “由于您尚未配置BrowserAct API密钥，请访问[BrowserAct控制台](https://www.browseract.com/reception/integrations)获取密钥，并在此处输入。”

## 🛠️ 输入参数
代理应根据用户需求配置以下参数：

1. **ASIN（亚马逊标准识别码）**
   - **类型**：`string`
   - **说明**：产品的唯一标识符。
   - **是否必填**：是
   - **示例**：`B07TS6R1SF`

## 🚀 使用方法（推荐）
代理应执行以下脚本以一次性获取结果：

```bash
# Example Usage
python -u ./.cursor/skills/amazon-asin-lookup-api-skill/scripts/amazon_asin_lookup_api.py "ASIN_VALUE"
```

### ⏳ 进度监控
由于此任务涉及自动化浏览器操作，可能需要几分钟时间。脚本会输出实时时间戳的状态日志（例如：`[14:30:05] 任务状态：正在运行`）。
**代理注意事项**：
- 在等待结果时，请监控终端输出。
- 只有当状态日志持续出现时，任务才正常运行。
- 仅当状态长时间不变或脚本无输出时，才考虑重试。

## 📊 输出数据说明
成功执行后，脚本会解析并打印API响应中的结构化产品数据，包括：
- `product_title`：产品的完整标题。
- `ASIN`：提供的ASIN。
- `product_url`：亚马逊产品页面的URL。
- `brand`：品牌名称。
- `price_current_amount`：当前价格。
- `price_original_amount`：原价（如适用）。
- `price_discount_amount`：折扣金额（如适用）。
- `rating_average`：平均评分。
- `rating_count`：评分总数。
- `featured`：如“亚马逊精选”等标志。
- `color`：颜色版本（如适用）。
- `compatible_devices`：兼容设备列表（如适用）。
- `product_description`：产品描述。
- `special_features`：产品亮点。
- `style`：样式属性（如适用）。
- `material`：所用材料（如适用）。

## ⚠️ 错误处理与重试机制
如果在执行过程中出现错误，代理应按照以下逻辑处理：
1. **检查输出**：
   - 如果输出包含“Invalid authorization”，则API密钥无效。**不要重试**，请让用户提供有效的密钥。
   - 如果输出不包含“Invalid authorization”，但任务仍然失败（例如，输出以`Error:`开头或返回空结果），代理应**自动重试一次**。
2. **重试次数限制**：
   - 自动重试仅限于**一次**。如果再次失败，请停止并向用户报告错误。