---
name: geo-visual-opportunity-engine
description: >
  **使用场景：**  
  当用户希望将产品信息及关键词转化为AI生成的视觉内容、结构化的产品数据、本地化的商业文案，或适用于Shopify和WooCommerce的发布-ready输出时，可使用此功能。该功能可用于触发产品图片生成、产品列表自动化更新、基于地理位置的商务内容生成、Shopify发布流程、WooCommerce发布流程，以及基于AI技术的视觉内容创作工作流程。
metadata:
  author: GEO-SEO
  version: "3.0.4"
  homepage: https://github.com/GEO-SEO/geo-visual-opportunity-engine
  primaryEnv: GOOGLE_API_KEY
  requires:
    env:
      - GOOGLE_API_KEY
      - SHOPIFY_STORE_URL
      - SHOPIFY_ACCESS_TOKEN
      - WOOCOMMERCE_STORE_URL
      - WOOCOMMERCE_CONSUMER_KEY
      - WOOCOMMERCE_CONSUMER_SECRET
    bins:
      - python3
---
# GEO 视觉化机会引擎（GEO Visual Opportunity Engine）

使用此技能，您可以将产品及关键词相关的机会转化为由人工智能生成的视觉内容、结构化产品数据、本地化商业文案，并可选择将产品发布到 Shopify 或 WooCommerce 平台。

## 概述

该技能将地理机会分析（GEO opportunity analysis）、图像生成（image generation）、产品数据合成（product-data synthesis）、本地化（localization）以及商业发布（commerce publishing）整合到一个工作流程中。

## 适用场景

- 需大规模生成人工智能产品内容的直接面向消费者（DTC）团队及 Shopify 团队
- 需测试产品描述以优化搜索效果及提升人工智能发现功能的商业运营者
- 负责管理跨市场视觉内容及产品列表发布流程的机构
- 希望在一个系统中完成产品分析、视觉内容制作及发布的团队

## 入门步骤

```text
Generate AI product visuals and commerce copy for this product opportunity
```

```text
Run GEO analysis for this product and keyword before generating assets
```

```text
Create publish-ready Shopify or WooCommerce assets for this product
```

## 核心工作流程

GEO 视觉化机会引擎是一个基于人工智能的商业工作流程，它能够利用 Nano Banana 2（Google Gemini）生成产品图片，并在明确启用发布功能的情况下，将产品发布到 Shopify 或 WooCommerce 平台。

## 外部服务及所需凭证

该工作流程依赖于外部服务，所需凭证取决于您启用的具体功能：

- `GOOGLE_API_KEY`：用于 Nano Banana 2 / Gemini 图像生成
- `SHOPIFY_STORE_URL` 和 `SHOPIFY_ACCESS_TOKEN`：仅在向 Shopify 发布产品时需要
- `WOOCOMMERCE_STORE_URL`、`WOOCOMMERCE_CONSUMER_KEY` 和 `WOOCOMMERCE_CONSUMER_SECRET`：仅在向 WooCommerce 发布产品时需要
- `python3`：用于运行自动化脚本

如果未提供发布凭证：

- 该技能仍可仅完成机会分析、产品数据合成及图像生成
- 请确保具备相应的凭证，否则不要尝试进行实时发布或平台写入操作

## 访问权限政策

默认情况下，该技能仅执行分析、资源生成及产品数据输出，除非明确启用了产品发布功能：
- 图像生成可以独立于商业发布进行
- Shopify 发布是可选的，必须明确启用
- WooCommerce 发布也是可选的，必须明确启用
- 请确保具备相应的凭证并启用发布功能，否则不要尝试进行平台写入操作

## 主要特性

- **产品数据合成**：自动生成产品标题、描述、SKU、价格及库存信息
- **人工智能图像生成**：自动调用 Nano Banana 2 生成产品图片
- **多平台支持**：同时支持向 Shopify 和 WooCommerce 发布产品
- **三种图像样式**：每种产品提供白色背景信息图、生活场景图及高画质主图
- **地理机会分析**：识别具有高优先级的视觉化内容需求

## 安装说明

```bash
pip install -r requirements.txt
```

## 快速入门

### 基本使用方法

```python
from src.main import EcommerceAutomator

# Initialize with API key
automator = EcommerceAutomator(google_api_key="your-google-api-key")

# Run complete workflow - one input to finish everything
result = automator.run_complete_workflow(
    product_input="wireless bluetooth headphones",
    country="us",
    language="en",
    generate_images=True,
    publish_to_shopify=False,
    publish_to_woocommerce=False
)

print(result['product_data']['title'])
print(result['status'])
```

### 仅进行地理机会分析

```python
from src.main import EcommerceAutomator

automator = EcommerceAutomator()

# Run GEO opportunity analysis
result = automator.run_geo_analysis(
    brand="AcmeWatch",
    product="Acme DivePro 5",
    core_keyword="smartwatch water resistance",
    country="us",
    language="en",
    generate_images=True
)

print(f"Found {len(result['opportunities'])} opportunities")
```

### 创建并发布产品

```python
from src.main import EcommerceAutomator

automator = EcommerceAutomator(
    google_api_key="your-google-api-key",
    shopify_store_url="your-store.myshopify.com",
    shopify_access_token="your-access-token"
)

# Create a product package and optionally publish it
result = automator.create_product(
    product_name="Wireless Bluetooth Headphones Pro",
    category="Electronics",
    base_price=79.99,
    generate_images=True,
    image_style="white_info",
    publish_to_shopify=True,
    publish_to_woocommerce=False
)
```

## API 参考

### EcommerceAutomator

- **`__init__(google_api_key, shopify_store_url, shopify_access_token, woo_store_url, woo_consumer_key, woo_consumer_secret)`**：使用 API 凭证初始化自动化工具。
- **`run_complete_workflow(product_input, country='us', language='en', generate_images=True, publish_to_shopify=False, publish_to_woocommerce=False, output_dir='output')**：执行完整的工作流程：
  1. 分析地理机会
  2. 合成产品数据（标题、描述、SKU、价格）
  3. 生成人工智能图片
  4. 将产品发布到电子商务平台
- **`run_geo_analysis(brand, product, core_keyword, country, language, competitors, platform_focus, generate_images)`**：执行地理机会分析并生成相关图片。
- **`create_product(product_name, category, base_price, description, language, target_platforms, generate_images, image_style, publish_to_shopify, publish_to_woocommerce)`**：完成产品的创建及发布流程。

## 配置参数

- **环境变量**：
  - `GOOGLE_API_KEY`：用于 Nano Banana 2 图像生成的 Google API 密钥
  - `SHOPIFY_STORE_URL`：Shopify 商店 URL
  - `SHOPIFY_ACCESS_TOKEN`：Shopify 管理员 API 访问令牌
  - `WOOCOMMERCE_STORE_URL`：WooCommerce 商店 URL
  - `WOOCOMMERCE_CONSUMER_KEY`：WooCommerce API 消费者密钥
  - `WOOCOMMERCE_CONSUMER_SECRET`：WooCommerce API 消费者密钥

## 图像样式

- **white_info**：纯白色背景的产品信息图
- **lifestyle**：包含真实人物互动的逼真场景图
- **hero**：高质量的商业摄影风格的主图

## 版本信息

3.0.0

## 开发者

Tim (sales@dageno.ai)