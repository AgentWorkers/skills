---
name: standard-agentic-commerce-engine
version: 1.2.4
description: 这是一个适用于“Agentic Commerce”平台的、具备生产级功能的通用引擎。该工具支持自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供了开箱即用的发现功能、购物车管理功能以及安全用户管理功能。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
---

# 标准代理商业引擎（Standard Agentic Commerce Engine）

**标准代理商业引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理（agents）与现代电子商务后端系统连接起来。通过提供统一且高精度的接口，该引擎可以让任何数字商店瞬间具备“原生代理支持”（Agent-Native）的功能。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 参考案例：Lafeitu

有关使用该引擎的生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一家真实的工匠食品品牌提供定制化的服务。

---

## 🛠 工具优先级与回退策略

为了提供最准确、最高效的使用体验，请遵循以下优先级顺序：

1. **优先使用 API (Primary)**：始终尝试使用 `commerce.py` 脚本。该脚本能够提供结构化、高精度的数据。您可以通过环境变量 `COMMERCE_URL` 来配置它。
2. **无状态头部信息 (Stateless Headers)**：依赖引擎内置的头部信息管理功能（`x-user-account`、`x-visitor-id`），以在无需使用 Cookie 的情况下维护会话的完整性。
3. **自动纠错 (Self-Correction)**：如果 API 因浏览器请求的特定路径（slug）返回 404 错误，应以 API 返回的搜索结果作为后端数据的权威来源。

---

## 🧠 代理操作逻辑

请遵循以下逻辑流程，以确保用户获得高质量的体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确认产品存在并获取正确的规格信息。
- **操作**：在将产品添加到购物车之前，务必先运行 `search` 或 `list` 命令。
- **逻辑**：使用 API 来获取正确的产品路径（slug）以及有效的克重（gram）/变体（variant）信息。
- **优化**：如果找到多个结果，根据返回的属性让用户进行选择。

### 2. 认证与个人资料管理
**目标**：管理用户的隐私和会话数据。
- **逻辑**：由于 API 是无状态的，如果用户未保存登录凭证，相关操作会返回 `401 Unauthorized` 错误。
- **命令**：
    1. 查看个人资料：`python3 scripts/commerce.py get-profile`
    2. 更新个人资料：`python3 scripts/commerce.py update-profile --name "名称" --address "..."`
- **所需数据**：必须遵循特定品牌后端系统的数据结构要求。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到”（User Not Found）时，引导用户访问商店的注册页面（通常可以在品牌元数据中找到注册链接）。

### 4. 购物车管理
**目标**：精确地修改用户的购物会话信息。
- **逻辑**：该引擎支持增加商品数量或设置商品的数量。
- **命令**：
    - **添加商品**：`python3 scripts/commerce.py add-cart <slug> --gram <G> --quantity <Q>`
    - **更新商品数量**：`python3 scripts/commerce.py update-cart <slug> --gram <G> --quantity <Q>`
    - **删除商品**：`python3 scripts/commerce.py remove-cart <slug> --gram <G>`
- **验证**：商品的数量/变体必须严格从产品可用的选项列表中选择。

### 5. 品牌信息与品牌故事
**目标**：获取品牌的身份信息及相关支持数据。
- **逻辑**：使用 `brand-info` 接口来检索品牌的相关内容。
- **工具**：
    - `python3 scripts/commerce.py brand-story`：获取品牌的背景故事/使命声明。
    - `python3 scripts/commerce.py company-info`：获取公司的正式信息。
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道。

---

## 🚀 功能概览

- **`search` / `list`：产品发现与库存查询。
- **`get`：深入了解产品规格、变体及价格信息。
- **`promotions`：查看当前的促销活动、配送规则及有效优惠信息。
- **`cart`：查看包含 VIP 折扣及税费/配送费用的完整会话信息。
- **`add-cart` / `update-cart` / `remove-cart`：对购物车内容进行精确操作。
- **`get-profile` / `update-profile`：管理用户的个性化设置及订单信息。
- **`brand-story` / `company-info` / `contact-info`：获取品牌背景信息及支持渠道。
- **`orders`：实时跟踪订单状态及购买历史记录。

---

## 💻 命令行界面（CLI）配置与示例

```bash
# Setup
export COMMERCE_URL="https://api.yourbrand.com/v1"
export COMMERCE_BRAND_ID="brand_slug"

# Actions
python3 scripts/commerce.py list
python3 scripts/commerce.py search "item"
python3 scripts/commerce.py get <slug>
python3 scripts/commerce.py add-cart <slug> --gram <variant>
```

---

## 🤖 故障排除与调试

- **状态码 401**：表示凭证缺失或已过期。建议用户登录。
- **状态码 404**：表示资源未找到。请通过 `search` 命令验证产品路径（slug）是否正确。
- **连接错误**：请确认 `COMMERCE_URL` 环境变量设置正确，并且目标端点能够被访问。