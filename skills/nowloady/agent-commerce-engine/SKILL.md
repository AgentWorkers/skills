---
name: standard-agentic-commerce-engine
version: 1.4.8
description: 这是一个专为“Agentic Commerce”设计的、可用于生产环境的通用引擎。该工具使自主代理能够通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互。它提供了开箱即用的发现功能、购物车操作以及安全用户管理功能。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["python3"],"tools":["web_search","web_fetch"],"env":[{"name":"COMMERCE_URL","description":"Target API base URL"},{"name":"COMMERCE_BRAND_ID","description":"Unique slug for the brand"}],"paths":["~/.clawdbot/credentials/agent-commerce-engine/"]},"install":[{"id":"python-deps","kind":"pip","package":"requests","label":"Install Python dependencies"}]}}
---
# 标准代理商业引擎（Standard Agentic Commerce Engine）

**标准代理商业引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理（agents）与现代电子商务后端系统无缝连接起来。通过提供统一、高精度的接口，该引擎可以让任何数字商店瞬间具备“原生代理支持”（Agent-Native）的能力。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 参考案例：Lafeitu

有关使用该引擎的生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一家真实的工匠食品品牌提供定制化的服务。

---

## 🔒 安全性与隐私保护

为了确保透明度和保护用户数据，标准代理商业引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.clawdbot/credentials/agent-commerce-engine/`
- **存储机制**：账户和会话令牌信息以 JSON 格式存储在本地，权限设置为 `0600`（仅限用户访问）。
- **安全升级**：从版本 1.4.0 开始，系统在用户首次登录后不再存储原始密码，而是将密码替换为经过加密处理的令牌。
- **访问范围**：这些数据仅对本地系统用户和正在运行的代理实例可见。
- **凭证管理**：用户可以通过运行 `logout` 命令随时清除自己的凭证。

### 2. 安全传输
- **基于令牌的身份验证**：使用 `x-api-token` 头部信息进行身份验证。原始密码仅在登录或注册过程中传输一次，之后会被替换为令牌。
- **HTTPS 强制要求**：从版本 1.4.7 开始，所有与后端的远程通信都必须使用 HTTPS 协议，以防止凭证被截获。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具使用优先级与备用策略

为了提供最准确、最高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终优先使用 `commerce.py` 脚本。该脚本能够提供结构化、高精度的数据。您可以通过环境变量 `COMMERCE_URL` 来配置它。
2. **无状态头部信息**：依赖引擎内置的头部信息管理功能（`x-user-account`、`x-visitor-id`）来维护会话的完整性，而无需使用 cookies。
3. **自动纠错**：如果浏览器请求的某个路径（slug）导致 API 返回 404 错误，优先以 API 返回的搜索结果作为后端数据的来源。

---

## 🧠 代理操作逻辑

遵循以下逻辑流程，以确保用户获得优质的购物体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在将商品添加到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑处理**：使用 API 来获取正确的商品路径（slug）以及有效的克重（gram）/变体（variant）信息。
- **细节处理**：如果找到多个结果，需要根据返回的属性让用户进行进一步选择。

### 2. 身份验证与用户资料管理
**目标**：管理用户的隐私和会话数据。
- **逻辑处理**：由于 API 是无状态的，如果用户未保存凭证，相关操作会返回 `401 Unauthorized` 错误。
- **相关命令**：
    - 查看用户资料：`python3 scripts/commerce.py get-profile`
    - 更新用户资料：`python3 scripts/commerce.py update-profile --name "Name" --address "..." --phone "..." --email "..."`
- **数据要求**：必须遵守特定品牌后端的数据格式要求。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到” 的提示时，引导用户访问品牌的注册页面（通常可以在品牌元数据中找到注册链接）。

### 4. 购物车管理
**目标**：精确地修改用户的购物车内容。
- **逻辑处理**：引擎支持增加商品数量或设置商品的数量。
- **相关命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --gram <G> --quantity <Q>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <slug> --gram <G> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --gram <G>`
- **验证要求**：选择的克重/变体值必须来自产品提供的选项列表中。

### 5. 品牌信息与品牌故事
**目标**：获取品牌的身份信息和支持资料。
- **操作步骤**：使用 `brand-info` 接口来获取品牌的相关内容。
- **相关命令**：
    - `python3 scripts/commerce.py brand-story`：获取品牌的故事或使命宣言。
    - `python3 scripts/commerce.py company-info`：获取公司的官方信息。
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道。

---

## 🚀 功能概览

- **`search` / `list`：用于发现产品并扫描库存信息。
- **`get`：深入查看产品的详细规格、变体及价格信息。
- **`promotions`：查看当前的销售规则、运费标准以及有效的促销活动。
- **cart`：提供完整的购物车信息，包括 VIP 折扣和税费/运费估算。
- **add-cart` / `update-cart` / `remove-cart`：实现对购物车的原子级操作（增加/修改/删除商品）。
- **get-profile` / `update-profile`：管理用户的个人资料和订单信息。
- **brand-story` / `company-info` / `contact-info`：获取品牌的相关信息和客户支持渠道。
- **orders`：实时跟踪订单状态和购买历史记录。

---

## 💻 命令行工具配置与使用示例

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

- **状态码 401**：表示凭证缺失或已过期。建议用户重新登录。
- **状态码 404**：表示资源未找到。请通过 `search` 操作验证商品路径（slug）是否正确。
- **连接错误**：请确认 `COMMERCE_URL` 环境变量的设置是否正确，并确保后端接口可访问。