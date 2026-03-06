---
name: Automated Product Onboarding + SEO/GEO Optimization
description: AutoList automates product onboarding for independent stores: AI-generated titles, descriptions, and images, plus built-in SEO & GEO (Generative Engine Optimization) so your pages are both user-friendly and easy for AIs to discover. Publish a ready product in minutes with one click.
---

# GEO Visual Opportunity Engine

## 概述

GEO Visual Opportunity Engine 是一款基于人工智能的电子商务自动化工具，它利用 Nano Banana 2（Google Gemini）生成产品图片，并自动将产品发布到 Shopify 和 WooCommerce 平台。

## 主要功能

- **产品数据生成**：自动生成产品标题、描述、SKU（库存单位）和价格。
- **AI 图像生成**：自动调用 Nano Banana 2 生成产品图片。
- **多平台支持**：同时支持将产品发布到 Shopify 和 WooCommerce。
- **多种图片样式**：为每个产品提供三种风格的图片：白色背景的信息图、生活场景图以及高画质的主图。
- **市场机会分析**：识别具有高优先级的视觉内容生成需求。

## 安装

### 一键安装（推荐）

```bash
# Download and install automatically
curl -sL https://clawhub.ai/GEO-SEO/geo-visual-opportunity-engine/archive/refs/heads/main.tar.gz | tar xz && cd geo-visual-opportunity-engine-* && pip install -r requirements.txt
```

或者使用 wget：

```bash
wget -qO- https://clawhub.ai/GEO-SEO/geo-visual-opportunity-engine/archive/refs/heads/main.tar.gz | tar xz && cd geo-visual-opportunity-engine-* && pip install -r requirements.txt
```

### 手动安装

```bash
# Clone the repository
git clone https://clawhub.ai/GEO-SEO/geo-visual-opportunity-engine.git
cd geo-visual-opportunity-engine

# Install dependencies
pip install -r requirements.txt
```

## 快速入门

### 基本用法

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

### 仅进行市场机会分析

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

### 创建产品并发布

```python
from src.main import EcommerceAutomator

automator = EcommerceAutomator(
    google_api_key="your-google-api-key",
    shopify_store_url="your-store.myshopify.com",
    shopify_access_token="your-access-token"
)

# Create and publish product
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

- **`__init__(google_api_key, shopify_store_url, shopify_access_token, woo_store_url, woo_consumer_key, woo_consumer_secret)**：使用 API 凭据初始化自动化工具。
- **`run_complete_workflow(product_input, country='us', language='en', generate_images=True, publish_to_shopify=False, publish_to_woocommerce=False, output_dir='output')**：执行完整的工作流程：
  1. 分析市场机会。
  2. 生成产品数据（标题、描述、SKU、价格）。
  3. 生成 AI 图片。
  4. 将产品发布到电子商务平台。
- **`run_geo_analysis(brand, product, core_keyword, country, language, competitors, platform_focus, generate_images)**：执行市场机会分析并生成图片。
- **`create_product(product_name, category, base_price, description, language, target_platforms, generate_images, image_style, publish_to_shopify, publish_to_woocommerce)**：完成产品的创建和发布流程。

## 配置

### 环境变量

- `GOOGLE_API_KEY`：用于 Nano Banana 2 生成图片的 Google API 密钥。
- `SHOPIFY_STORE_URL`：Shopify 商店 URL。
- `SHOPIFY_ACCESS_TOKEN`：Shopify 管理员 API 访问令牌。
- `WOOCOMMERCE_STORE_URL`：WooCommerce 商店 URL。
- `WOOCOMMERCE_CONSUMER_KEY`：WooCommerce API 消费者密钥。
- `WOOCOMMERCE_CONSUMER_SECRET`：WooCommerce API 消费者密钥。

## 图片样式

- **white_info**：纯白色背景的产品信息图。
- **lifestyle**：包含真实人物互动的、具有真实感效果的图片。
- **hero**：高质量的商业摄影风格的主图。

## 版本

1.0.5

## 开发者

Tim (sales@dageno.ai)