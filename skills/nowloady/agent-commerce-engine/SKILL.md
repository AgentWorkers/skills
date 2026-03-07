---
name: standard-agentic-commerce-engine
version: 1.6.2
description: 这是一个专为“Agentic Commerce”设计的、可用于生产环境的通用引擎。该工具允许自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供了开箱即用的发现功能、购物车操作以及安全用户管理支持。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata: {"clawdbot":{"emoji":"🛒","homepage":"https://github.com/NowLoadY/agent-commerce-engine","source":"https://github.com/NowLoadY/agent-commerce-engine","requires":{"bins":["python3"],"tools":[],"env":[],"optionalEnv":["COMMERCE_URL","COMMERCE_BRAND_ID","COMMERCE_BRAND_NAME"],"paths":["~/.clawdbot/credentials/agent-commerce-engine/"]},"install":[{"id":"python-deps","kind":"pip","package":"requests","label":"Install Python dependencies"}]}}
---
# 标准代理商业引擎（Standard Agentic Commerce Engine）

**标准代理商业引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理（agents）与现代电子商务后端系统无缝连接。通过提供统一、高精度的接口，该引擎能够让任何数字商店立即具备“代理原生”（Agent-Native）的功能。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 快速入门：开箱即用的后端配置

`agent-commerce-engine` 提供了一个标准规范（`SERVER_SPEC.md`），该规范能够将任何现有的网站快速转换为“代理原生”格式。开发者只需查看并复制提供的最小可行 Python/FastAPI 服务器模板，便能在几分钟内搭建出符合要求的后端接口。

## 参考案例：Lafeitu

有关使用该引擎进行生产级实现的示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何应用于一个真实的工匠食品品牌。

---

## 🔒 安全性与隐私保护

为了确保透明度和保护用户数据，标准代理商业引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.clawdbot/credentials/agent-commerce-engine/`
- **存储方式**：账户和会话令牌信息以 JSON 格式存储在本地，仅限用户本人访问（权限设置为 `0600`）。
- **安全升级**：从版本 1.4.0 开始，系统在用户首次登录后不会再存储原始密码，而是将密码替换为加密令牌。
- **访问范围**：这些数据仅对本地系统用户和正在运行的代理实例可见。
- **凭证管理**：用户可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输
- **基于令牌的身份验证**：使用 `x-api-token` 标头进行身份验证。原始密码仅在登录或注册过程中传输一次，用于生成令牌。
- **HTTPS 强制使用**：从版本 1.4.7 开始，所有与后端的通信都必须使用 HTTPS 协议，以防止凭证被截获。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具使用优先级与备用策略

为了提供最准确、最高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终尝试使用 `commerce.py` 脚本。该脚本能够提供结构化、高精度的数据。通过 `--store <url>` 参数指定目标商店。
2. **无状态头部信息**：利用引擎内置的头部信息管理功能（`x-user-account`、`x-visitor-id`）来维护会话状态，而无需依赖 cookies。
3. **自动纠错**：如果 API 因浏览器原因返回 404 错误，应以 API 返回的搜索结果作为后端数据的来源。

---

## 🧠 代理操作逻辑

遵循以下逻辑流程，以确保用户获得高质量的体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在将商品添加到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑**：使用 API 查找正确的商品标识符（`slug`）和有效的商品变体信息。通过 `--page` 和 `--limit` 参数安全地浏览大量商品信息，避免超出系统限制。
- **优化处理**：如果找到多个结果，根据返回的属性引导用户进行进一步选择。如果结果中的 `totalPages` 大于当前页面数，建议用户选择查看下一页或进一步细化搜索条件。

### 2. 身份验证与个人资料管理
**目标**：管理用户隐私和会话数据。
- **逻辑**：由于 API 是无状态的，如果未保存凭证，相关操作会返回 `401 Unauthorized` 错误。
- **相关命令**：
    - 查看个人资料：`python3 scripts/commerce.py get-profile`
    - 更新个人资料：`python3 scripts/commerce.py update-profile --name "姓名" --address "..." --phone "..." --email "..."`
- **数据要求**：操作时必须遵循特定品牌后端的规范。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到” 的提示时，引导用户访问商店的注册页面（通常可以在品牌元数据中找到注册链接）。

### 4. 购物车管理
**目标**：精确地修改用户的购物车内容。
- **逻辑**：引擎支持增加商品数量或设置商品数量。
- **相关命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --variant <V> --quantity <Q>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <slug> --variant <V> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --variant <V>`
    - 清空购物车：`python3 scripts/commerce.py clear-cart`
    - 结账/创建订单：`python3 scripts/commerce.py create-order --name <姓名> --phone <电话> --province <省份> --city <城市> --address <地址>`
- **验证要求**：选择的商品变体必须来自产品提供的有效选项列表。
- **支付流程**：目前代理无法直接执行消费者支付（如信用卡/移动支付）操作。用户需要通过 `create-order` 创建订单后，API 会返回一个支付链接，由用户手动完成支付。

### 5. 品牌信息与品牌故事展示
**目标**：获取品牌相关信息和支持数据。
- **操作步骤**：使用 `brand-info` 接口获取品牌故事、公司信息等详细内容。
- **相关命令**：
    - `python3 scripts/commerce.py brand-story`：获取品牌故事
    - `python3 scripts/commerce.py company-info`：获取公司详细信息
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道

---

## 🚀 功能概览

- **`search` / `list`：用于发现产品并扫描库存。使用 `--page <N>` 和 `--limit <N>` 参数安全地分页浏览大量商品信息。
- **`get`：深入了解产品规格、变体信息及价格详情。
- **`promotions`：查看当前的促销活动、配送规则和有效优惠。
- **cart`：查看购物车内容，包括 VIP 折扣及税费/运费估算。
- **add-cart` / `update-cart` / `remove-cart` / `clear-cart`：对购物车内容进行精确操作。
- **create-order`：将购物车内容转换为待处理订单，并提供安全的支付链接供用户完成支付。
- **get-profile` / `update-profile`：管理用户个人资料和订单信息。
- **brand-story` / `company-info` / `contact-info`：获取品牌相关信息和客户支持渠道。

---

## 💻 命令行工具配置与示例

```bash
# Target a store directly via --store (preferred)
python3 scripts/commerce.py --store https://api.yourbrand.com/v1 list --page 1 --limit 20
python3 scripts/commerce.py --store https://api.yourbrand.com/v1 search "item"
python3 scripts/commerce.py --store https://api.yourbrand.com/v1 add-cart <slug> --variant <variant_id>

# Or use environment variable (deprecated, will be removed in a future version)
export COMMERCE_URL="https://api.yourbrand.com/v1"
python3 scripts/commerce.py list
```

凭证会自动按域名存储在 `~/.clawdbot/credentials/agent-commerce-engine/<domain>/` 目录下。

---

## 🤖 故障排除与调试

- **`AUTH_REQUIRED`：令牌缺失或过期。运行 `login` 命令获取新令牌。
- **`AUTH_INVALID`：提供的凭证错误。请核对账户信息和密码。
- **`PRODUCT_NOT_FOUND`：资源未找到。请使用 `search` 命令确认商品是否存在。
- **`VARIANT_UNAVAILABLE`：请求的商品变体无效或已售罄。请查看提示信息中的替代选项。
- **CART_EMPTY`：尝试结账时购物车为空。请先添加商品。
- **连接错误**：请确认 `--store` 参数指定的 URL 正确且后端服务可访问。