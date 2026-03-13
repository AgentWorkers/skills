---
name: geo-visual-opportunity-engine
description: >
  **使用场景：**  
  当用户希望将产品信息及关键词转化为人工智能生成的视觉内容、结构化产品数据、本地化商业文案，或可直接用于销售的商业素材时，可使用该功能。该功能适用于产品图片生成、产品列表制作、具有地理位置信息的商业内容生成，以及基于人工智能技术的视觉内容创作工作流程。
metadata:
  author: GEO-SEO
  version: "3.0.5"
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
# GEO 视觉机会引擎（GEO Visual Opportunity Engine）

使用此技能，您可以将产品和关键词相关的机会转化为由 AI 生成的视觉内容、结构化产品数据、本地化商业文案以及可直接导出的商业资产。

## 概述

该技能将地理机会分析（GEO opportunity analysis）、图像生成（image generation）、产品数据合成（product-data synthesis）、内容本地化（localization）以及商业资产准备（commerce asset preparation）整合到一个工作流程中。

## 适用场景

- 需要大规模生成 AI 产品资产的 DTC（直接面向消费者）团队和 Shopify 团队
- 需要测试产品描述以优化搜索体验或利用 AI 功能进行产品发现的商业运营者
- 负责管理跨市场视觉内容和商品列表工作流程的机构
- 希望在一个工作流程中完成产品分析、视觉内容制作及资产导出的团队

## 入门步骤

```text
Generate AI product visuals and commerce copy for this product opportunity
```

```text
Run GEO analysis for this product and keyword before generating assets
```

```text
Create export-ready Shopify or WooCommerce assets for this product
```

## 核心工作流程

GEO 视觉机会引擎是一个基于 AI 的商业工作流程，它可以使用 Nano Banana 2（Google Gemini）生成产品图片，并为 Shopify 或 WooCommerce 准备可直接使用的商业资产。

## 外部服务及所需凭证

该工作流程依赖于外部服务，所需凭证取决于您启用的功能：

- `GOOGLE_API_KEY`：用于 Nano Banana 2/Gemini 图像生成
- `SHOPIFY_STORE_URL` 和 `SHOPIFY_ACCESS_TOKEN`：仅在直接导出到 Shopify 时需要
- `WOOCOMMERCE_STORE_URL`、`WOOCOMMERCE_CONSUMER_KEY` 和 `WOOCOMMERCE_CONSUMER_SECRET`：仅在直接导出到 WooCommerce 时需要
- `python3`：用于运行自动化脚本

如果缺少店铺凭证：

- 该技能将仅完成机会分析、产品数据合成、图像生成及导出打包步骤
- 除非用户明确请求直接导出并提供了相应的凭证，否则不会尝试进行实时发布或平台写入操作

## 访问权限政策

默认情况下，该技能仅限于分析、资产生成、产品数据输出及导出打包。直接进行平台发布需要用户明确启用相关权限：

- 图像生成可以独立于商业发布流程运行
- 直接导出到 Shopify 或 WooCommerce 是可选功能，必须用户明确启用
- 除非用户提供了相应的凭证并启用了直接导出功能，否则不会尝试进行店铺写入操作或完成产品发布

## 主要功能

- **产品数据合成**：自动生成产品标题、描述、SKU、价格及库存信息
- **AI 图像生成**：自动调用 Nano Banana 2 生成产品图片
- **多平台支持**：为 Shopify 和 WooCommerce 准备所需资产
- **三种图像样式**：白色背景的信息图、真实场景图（包含人物互动）以及高画质的产品主图
- **地理机会分析**：识别具有高优先级的视觉内容生成机会

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

### 创建产品包

```python
from src.main import EcommerceAutomator

automator = EcommerceAutomator(
    google_api_key="your-google-api-key",
    shopify_store_url="your-store.myshopify.com",
    shopify_access_token="your-access-token"
)

# Create a product package and optionally export it
result = automator.create_product(
    product_name="Wireless Bluetooth Headphones Pro",
    category="Electronics",
    base_price=79.99,
    generate_images=True,
    image_style="white_info",
    publish_to_shopify=False,
    publish_to_woocommerce=False
)
```

## API 参考

### EcommerceAutomator

- **`__init__(google_api_key, shopify_store_url, shopify_access_token, woo_store_url, woo_consumer_key, woo_consumer_secret)`**：使用 API 凭证初始化自动化工具。
- **`run_complete_workflow(product_input, country='us', language='en', generate_images=True, publish_to_shopify=False, publish_to_woocommerce=False, output_dir='output')**：执行完整工作流程：
  - 分析地理机会
  - 合成产品数据（标题、描述、SKU、价格）
  - 生成 AI 图像
  - 导出平台可用资产（或根据用户设置直接导出）
- **`run_geo_analysis(brand, product, core_keyword, country, language, competitors, platform_focus, generate_images)`**：执行地理机会分析并生成图像。
- **`create_product(product_name, category, base_price, description, language, target_platforms, generate_images, image_style, publish_to_shopify, publish_to_woocommerce)`**：完成产品创建的整个工作流程。

## 配置参数

- **环境变量**：
  - `GOOGLE_API_KEY`：用于 Nano Banana 2 图像生成的 Google API 密钥
  - `SHOPIFY_STORE_URL`：Shopify 店铺 URL
  - `SHOPIFY_ACCESS_TOKEN`：Shopify 管理员 API 访问令牌
  - `WOOCOMMERCE_STORE_URL`：WooCommerce 店铺 URL
  - `WOOCOMMERCE_CONSUMER_KEY`：WooCommerce API 消费者密钥
  - `WOOCOMMERCE_CONSUMER_SECRET`：WooCommerce API 消费者密钥

## 图像样式选项

- **white_info**：纯白色背景的产品信息图
- **lifestyle**：包含真实人物互动的场景图（高度写实）
- **hero**：高质量的商业摄影风格的产品主图

## 版本信息

3.0.0

## 开发者

Tim (sales@dageno.ai)