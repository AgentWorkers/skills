---
name: shopify-bulk-upload
description: Bulk upload products to Shopify stores. Read product data from Excel/CSV, automatically create products, images, variants, prices and inventory. Use cases: (1) Batch list new products (2) Migrate products from other platforms to Shopify (3) Batch update existing product information. REQUIRES PAYMENT: $20 USD to use. Payment via [link to be added] or contact developer.
---

# Shopify 批量上传工具

## ⚠️ 需要支付费用 - 20 美元

**使用此工具前需先支付费用。**

- **价格**：20 美元（一次性支付）
- **支付方式**：请联系开发者获取支付详情
- **支付完成后**：您将收到可正常使用的脚本及配置指南

---

## 快速入门

### 1. 准备产品数据文件

将产品数据准备在 `assets/products.xlsx` 或 `assets/products.csv` 文件中：

| 字段 | 必填 | 说明 |
|-------|----------|-------------|
| title | ✅ | 产品标题 |
| description | ✅ | 产品描述（支持 HTML 格式） |
| vendor | ✅ | 品牌/供应商 |
| product_type | ✅ | 产品类型 |
| price | ✅ | 价格 |
| compare_at_price | ❌ | 原价（用于显示折扣） |
| sku | ✅ | SKU 代码 |
| inventory_quantity | ❌ | 库存数量 |
| weight | ❌ | 重量（单位：kg） |
| weight_unit | ❌ | 重量单位：kg、g、lb、oz |
| status | ❌ | 状态（active、draft、archived） |
| tags | ❌ | 标签（用逗号分隔） |
| images | ❌ | 图片链接（用逗号分隔，可有多张） |
| variant_title | ❌ | 变体名称（例如：颜色、尺寸） |
| option1_name | ❌ | 变体选项 1 的名称（例如：颜色） |
| option1_value | ❌ | 变体选项 1 的值（例如：红色） |
| option2_name | ❌ | 变体选项 2 的名称（例如：尺寸） |
| option2_value | ❌ | 变体选项 2 的值（例如：M） |

### 2. 配置 Shopify API

在 `.env` 文件中进行配置：

```bash
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token
SHOPIFY_API_VERSION=2024-01
```

**获取访问令牌的步骤：**
1. 登录 Shopify 管理后台
2. 转到设置 → 应用和销售渠道 → 开发应用
3. 创建应用 → 配置管理 API 的权限
4. 确保拥有 `write_products` 和 `write_inventory` 权限
5. 安装应用 → 获取访问令牌

### 3. 运行上传脚本

```bash
cd scripts
python shopify_bulk_upload.py
```

## 脚本功能

- ✅ 读取 Excel/CSV 格式的产品数据
- ✅ 创建产品（支持多张图片和多种变体）
- ✅ 自动处理图片上传
- ✅ 变体管理（颜色、尺寸等）
- ✅ 库存管理
- ✅ 错误日志记录
- ✅ 按 SKU 进行增量更新
- ✅ 显示上传进度

## 输出结果

完成上传后：
- `logs/upload.log` - 上传日志
- `logs/error.log` - 错误详情
- `output/products_created.json` - 成功创建的产品列表
- `output/products_failed.json` - 失败的产品列表

## 配置

编辑 `scripts/config.py` 文件以进行自定义设置：

```python
CONFIG = {
    "batch_size": 10,        # Products per batch
    "retry_count": 3,        # Retry attempts on failure
    "retry_delay": 2,        # Retry interval (seconds)
    "image_timeout": 30,     # Image upload timeout
    "default_status": "active",  # Default status
}
```

---

## 📝 支付信息

**价格**：20 美元（一次性支付）

**支付方式**：
- PayPal：[您的 PayPal 电子邮件地址]
- 加密货币：[钱包地址]
- 支付宝/微信：[二维码]

**支付完成后，请联系开发者获取：**
- 完整的可运行 Python 脚本
- 配置指南
- 技术支持（针对安装过程中遇到的问题）

---

## 更多详情

- Shopify API 文档：请参阅 [references/shopify-api.md](references/shopify-api.md)
- 模板示例：请参阅 [assets/products-template.xlsx](assets/products-template.xlsx)