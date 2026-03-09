---
name: standard-agentic-commerce-engine
version: 1.6.4
description: 这是一个适用于“Agentic Commerce”框架的、具备生产级功能的通用引擎。该工具允许自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供开箱即用的发现功能、购物车操作以及安全用户管理支持。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata: {"openclaw":{"emoji":"🛒","homepage":"https://github.com/NowLoadY/agent-commerce-engine","source":"https://github.com/NowLoadY/agent-commerce-engine","requires":{"bins":["python3"],"tools":[],"env":[],"optionalEnv":["COMMERCE_URL","COMMERCE_BRAND_ID","COMMERCE_BRAND_NAME"],"paths":["~/.openclaw/credentials/agent-commerce-engine/"]},"install":[{"id":"python-deps","kind":"pip","package":"requests","label":"Install Python dependencies"}]}}
---
# 标准代理商务引擎（Standard Agentic Commerce Engine）

**标准代理商务引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理（agents）与现代电子商务后端系统无缝连接。通过提供统一、高精度的接口，该引擎可以让任何数字店铺瞬间具备“代理原生”（Agent-Native）的特性。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 快速入门：开箱即用的后端配置

`agent-commerce-engine` 提供了一套标准规范（`SERVER_SPEC.md`），能够快速将任何现有的网站适配为“代理原生”格式。开发者只需按照提供的 Python/FastAPI 服务器模板进行配置，即可在几分钟内搭建出符合要求的后端接口。

## 参考案例：Lafeitu

有关使用该引擎的实际生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一家真实的工匠食品品牌提供定制化的服务。

---

## 🔒 安全性与隐私保护

为了确保透明度和保护用户数据，标准代理商务引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.openclaw/credentials/agent-commerce-engine/`
- **存储方式**：账户和会话令牌信息以 JSON 格式存储在本地，权限设置为 `0600`（仅限用户访问）。
- **安全升级**：从版本 1.4.0 开始，系统在用户首次登录后不再存储原始密码，而是用加密令牌替换密码。
- **访问范围**：数据仅对本地系统用户和正在运行的代理实例可见。
- **凭证管理**：用户可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输
- **基于令牌的认证**：使用 `x-api-token` 标头进行身份验证。原始密码仅在登录或注册过程中传输一次，之后会被替换为加密令牌。
- **强制使用 HTTPS**：从版本 1.4.7 开始，所有与后端的通信都强制使用 HTTPS，以防止凭证被截获。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具使用优先级与备用策略

为了提供最准确、高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终优先使用 `commerce.py` 脚本。它能够提供结构化、高精度的数据。使用 `--store <url>` 参数指定目标店铺。
2. **无状态请求**：依赖引擎内置的请求头（`x-user-account`、`x-visitor-id`）来维护会话状态，无需依赖 cookies。
3. **错误处理**：如果 API 因浏览器原因返回 404 错误，应以 API 的搜索结果作为后端数据的来源。

---

## 🧠 代理操作逻辑

遵循以下逻辑流程，以确保用户获得优质的购物体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在添加商品到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑**：使用 API 查找正确的商品标识符（`slug`）和有效的产品变体信息。通过 `--page` 和 `--limit` 参数安全地浏览大量商品信息，避免超出系统限制。
- **优化流程**：如果找到多个结果，让用户根据返回的属性进行选择。如果结果中的 `totalPages` 大于当前页面数，建议用户继续搜索或细化搜索条件。

### 2. 认证与用户资料管理
**目标**：管理用户隐私和会话数据。
- **逻辑**：由于 API 是无状态的，如果用户未登录，相关操作会返回 `401 Unauthorized` 错误。
- **相关命令**：
    - 查看用户资料：`python3 scripts/commerce.py get-profile`
    - 更新用户资料：`python3 scripts/commerce.py update-profile --name "Name" --address "..." --phone "..." --email "..."`
- **数据要求**：操作时需遵循特定品牌后端的规范。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到” 的提示时，引导用户访问店铺的注册页面（通常位于品牌元数据中）。

### 4. 购物车管理
**目标**：精确地修改用户的购物车内容。
- **操作步骤**：支持增加商品数量或设置商品数量。
- **相关命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --variant <V> --quantity <Q>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <slug> --variant <V> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --variant <V>`
    - 清空购物车：`python3 scripts/commerce.py clear-cart`
    - 结账/创建订单：`python3 scripts/commerce.py create-order --name <NAME> --phone <PHONE> --province <PROVINCE> --city <CITY> --address <ADDRESS>`
- **验证要求**：商品变体必须从产品提供的选项列表中选择。
- **支付流程**：由于缺乏财务授权，代理目前无法直接处理用户的支付（如信用卡/移动钱包）。创建订单后，API 会返回一个支付链接，代理需要将该链接提供给用户完成支付。

### 5. 品牌信息与品牌故事
**目标**：获取品牌相关信息。
- **操作步骤**：使用 `brand-info` 接口获取品牌的故事和信息。
- **相关命令**：
    - `python3 scripts/commerce.py brand-story`：获取品牌故事
    - `python3 scripts/commerce.py company-info`：获取公司详细信息
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道

---

## 🚀 功能概览

- **`search` / `list`：用于发现产品并扫描库存。使用 `--page <N>` 和 `--limit <N>` 参数安全地分页浏览商品信息。
- **`get`：详细查看产品规格、变体及价格信息。
- **`promotions`：查看当前的销售规则、运费标准及优惠活动。
- **cart`：查看购物车内容，包括 VIP 优惠和税费/运费估算。
- **add-cart` / `update-cart` / `remove-cart` / `clear-cart`：对购物车内容进行操作。
- **create-order`：将购物车内容转换为待处理订单，并提供安全的支付链接供用户完成支付。
- **get-profile` / `update-profile`：个性化设置用户资料。
- **brand-story` / `company-info` / `contact-info`：获取品牌相关信息和客服渠道。

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

凭证会自动按域名存储在 `~/.openclaw/credentials/agent-commerce-engine/<domain>/` 目录下。

---

## 🤖 故障排除与调试

- **`AUTH_REQUIRED`：令牌缺失或过期。请运行 `login` 命令获取新令牌。
- **`AUTH_INVALID`：提供的凭证错误。请核对账户和密码。
- **`PRODUCT_NOT_FOUND`：资源未找到。请使用 `search` 命令确认商品存在。
- **`VARIANT_UNAVAILABLE`：请求的变体无效或已售罄。请查看提示信息中的替代选项。
- **CART_EMPTY`：尝试结账时购物车为空。请先添加商品。
- **连接错误**：请确认 `--store` 参数正确无误，并确保后端服务可用。