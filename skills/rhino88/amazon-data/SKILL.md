---
name: amazon-data
description: 使用 Python 通过 Canopy API 的 REST 端点检索 Amazon 产品数据，包括价格、评论、销售预测、库存水平、搜索结果、优惠信息等。
---
# Amazon Data Skill

使用此技能，您可以通过Python通过Canopy API的REST端点检索亚马逊产品数据。

Canopy API可实时访问超过25,000个类别中的3.5亿种亚马逊产品。利用此技能，您可以获取：

- **产品详情**：标题、描述、价格、图片、产品特性以及品牌信息
- **销售和库存估算**：每周、每月和每年的销量以及当前库存水平
- **评论**：评分、评论文本、经过验证的购买状态以及有帮助的投票数
- **搜索**：通过关键词查找产品，并可设置价格、状况、类别等筛选条件以及排序方式
- **优惠信息**：比较多个卖家的价格和配送详情
- **促销活动**：浏览12个国际域名下的当前亚马逊促销活动和折扣
- **类别信息**：浏览完整的亚马逊类别分类结构
- **卖家和作者信息**：查询卖家资料、评分以及作者的出版物列表

## 设置

1. 在 [canopyapi.co](https://canopyapi.co) 注册并创建账户
2. 从您的仪表板中获取API密钥
3. 将API密钥设置到您的环境中：

```bash
export API_KEY="your_api_key_here"
```

## 基本URL

```
https://rest.canopyapi.co
```

## 认证

所有请求都需要包含 `API-KEY` 请求头：

```python
import os
import requests

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://rest.canopyapi.co"
HEADERS = {"API-KEY": API_KEY}
```

## 端点

### 获取产品信息

```python
response = requests.get(f"{BASE_URL}/api/amazon/product", headers=HEADERS, params={
    "asin": "B01HY0JA3G",  # or use "url" or "gtin"
    "domain": "US",         # optional, defaults to "US"
})
```

返回产品标题、品牌、价格、评分、图片、产品特性、类别以及卖家信息。

### 获取产品变体

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/variants", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### 获取库存估算

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/stock", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### 获取销售估算

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/sales", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

返回每周、每月和每年的销量估算。

### 获取产品评论

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/reviews", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
})
```

### 获取产品优惠信息

```python
response = requests.get(f"{BASE_URL}/api/amazon/product/offers", headers=HEADERS, params={
    "asin": "B01HY0JA3G",
    "page": 1,  # optional
})
```

### 搜索产品

```python
response = requests.get(f"{BASE_URL}/api/amazon/search", headers=HEADERS, params={
    "searchTerm": "wireless headphones",
    "domain": "US",          # optional
    "page": 1,               # optional
    "limit": 20,             # optional, 20-40
    "minPrice": 10,          # optional
    "maxPrice": 100,         # optional
    "conditions": "NEW",     # optional: NEW, USED, RENEWED (comma-separated)
    "sort": "FEATURED",      # optional: FEATURED, MOST_RECENT, PRICE_ASCENDING, PRICE_DESCENDING, AVERAGE_CUSTOMER_REVIEW
})
```

### 获取自动完成建议

```python
response = requests.get(f"{BASE_URL}/api/amazon/autocomplete", headers=HEADERS, params={
    "searchTerm": "wireless",
})
```

### 获取类别分类结构

```python
response = requests.get(f"{BASE_URL}/api/amazon/categories", headers=HEADERS, params={
    "domain": "US",  # optional
})
```

### 获取类别信息

```python
response = requests.get(f"{BASE_URL}/api/amazon/category", headers=HEADERS, params={
    "categoryId": "1234567890",
    "domain": "US",          # optional
    "page": 1,               # optional
    "sort": "FEATURED",      # optional
})
```

### 获取卖家信息

```python
response = requests.get(f"{BASE_URL}/api/amazon/seller", headers=HEADERS, params={
    "sellerId": "A2R2RITDJNW1Q6",
    "domain": "US",  # optional
    "page": 1,       # optional
})
```

### 获取作者信息

```python
response = requests.get(f"{BASE_URL}/api/amazon/author", headers=HEADERS, params={
    "asin": "B000AQ5RM0",
    "domain": "US",  # optional
    "page": 1,       # optional
})
```

### 获取促销活动

```python
response = requests.get(f"{BASE_URL}/api/amazon/deals", headers=HEADERS, params={
    "domain": "US",  # optional: US, UK, CA, DE, FR, IT, ES, AU, IN, MX, BR, JP
    "page": 1,       # optional
    "limit": 20,     # optional
})
```

## 产品查询选项

产品端点支持以下标识符之一进行查询：

| 参数 | 描述                          | 示例                                      |
| --------- | -------------------------------------- | ------------------------------------------- |
| `asin`  | 亚马逊产品ASIN                    | `B01HY0JA3G`                              |
| `url`   | 完整的亚马逊产品URL                | `https://amazon.com/dp/B01HY0JA3G`                   |
| `gtin`  | ISBN、UPC或EAN代码                | `9780141036144`                         |

## 支持的域名

美国（默认）、英国、加拿大、德国、法国、意大利、西班牙、澳大利亚、印度、墨西哥、巴西、日本

## 错误处理

| 状态码 | 含义                                      |
| ------ | ----------------------------------------- |
| 400    | 参数无效                          |
| 401    | API密钥无效或缺失                    |
| 402    | 需要支付                        |
| 500    | 服务器错误                          |

```python
response = requests.get(f"{BASE_URL}/api/amazon/product", headers=HEADERS, params={"asin": "B01HY0JA3G"})
if response.ok:
    data = response.json()
else:
    print(f"Error {response.status_code}: {response.text}")
```