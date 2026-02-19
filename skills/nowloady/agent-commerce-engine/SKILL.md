---
name: standard-agentic-commerce-engine
version: 1.4.2
description: 这是一个专为“Agentic Commerce”设计的、可用于生产环境的通用引擎。该工具支持自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供了开箱即用的发现功能、购物车操作以及安全用户管理功能。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata:
  clawdbot:
    emoji: 🛒
    requires:
      bins: [python3, curl]
      paths:
        - ~/.clawdbot/credentials/agent-commerce-engine/
    env:
      - name: COMMERCE_URL
        description: Target API base URL (e.g. https://api.brand.com/v1)
      - name: COMMERCE_BRAND_ID
        description: Unique slug for the brand to differentiate credential storage
---
# 标准代理商务引擎（Standard Agentic Commerce Engine）

**标准代理商务引擎**是一款专为生产环境设计的解决方案，它能够将自主运行的代理（agents）与现代电子商务后端系统无缝连接起来。通过提供统一、高精度的接口，该引擎能够让任何数字商店立即具备“代理原生”（Agent-Native）的功能。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 参考案例：Lafeitu

有关使用该引擎的生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一家真实的工匠食品品牌提供定制化的服务。

---

## 🔒 安全性与隐私保护

为确保透明度并保护用户数据，标准代理商务引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.clawdbot/credentials/agent-commerce-engine/`
- **存储方式**：账户和会话令牌信息以 JSON 格式存储在本地，仅具有 `0600` 权限（仅限用户访问）。
- **安全升级**：从版本 1.4.0 开始，初次登录后原始密码将不再被存储。引擎会用加密令牌替换原始密码。
- **访问范围**：数据仅对本地系统用户和正在运行的代理实例可见。
- **凭证管理**：可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输
- **基于令牌的身份验证**：使用 `x-api-token` 标头进行身份验证。在 `login` 或 `register` 阶段，原始密码仅传输一次，随后会被替换为加密令牌。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具优先级与回退策略

为了提供最准确、高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终尝试使用 `commerce.py` 脚本。该脚本提供结构化、高精度的数据。通过环境变量 `COMMERCE_URL` 进行配置。
2. **无状态请求头**：依赖引擎内置的请求头管理功能（`x-user-account`、`x-visitor-id`）来维护会话状态，无需使用 cookies。
3. **错误处理**：如果 API 因浏览器请求的特定路径（slug）返回 404 错误，优先使用 API 的搜索结果作为后端数据的来源。

---

## 🧠 代理操作逻辑

遵循以下逻辑流程，以确保用户获得高质量的服务体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在将商品添加到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑处理**：使用 API 查找正确的产品路径（slug）以及有效的克重（gram）/变体（variant）信息。
- **进一步处理**：如果找到多个结果，根据返回的属性让用户进行选择。

### 2. 身份验证与用户资料管理
**目标**：管理用户隐私和会话数据。
- **逻辑处理**：由于 API 是无状态的，如果未保存凭证，相关操作会返回 `401 Unauthorized` 错误。
- **相关命令**：
    - 查看个人资料：`python3 scripts/commerce.py get-profile`
    - 更新资料：`python3 scripts/commerce.py update-profile --name "Name" --address "..."`
- **数据要求**：遵循特定品牌后端的数据格式要求。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到” 的提示时，引导用户访问商店的注册页面（通常位于品牌元数据中）。

### 4. 购物车管理
**目标**：精确修改用户的购物车内容。
- **逻辑处理**：引擎支持增加商品数量或设置固定数量。
- **相关命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --gram <G> --quantity <Q>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <slug> --gram <G> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --gram <G>`
- **验证要求**：克重/变体值必须从产品可用选项列表中选择。

### 5. 品牌信息与品牌故事
**目标**：获取品牌相关信息。
- **操作步骤**：使用 `brand-info` 接口获取品牌故事和品牌使命等信息。
- **相关工具**：
    - `python3 scripts/commerce.py brand-story`：获取品牌故事
    - `python3 scripts/commerce.py company-info`：获取公司详细信息
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道

---

## 🚀 功能概览

- **`search` / `list`：产品发现与库存查询。
- **`get`：深入了解产品规格、变体及价格信息。
- **`promotions`：查看当前促销活动、配送门槛及有效优惠。
- **`cart`：查看购物车详情，包括 VIP 折扣及税费/运费估算。
- **`add-cart` / `update-cart` / `remove-cart`：对购物车内容进行原子级操作。
- **`get-profile` / `update-profile`：个性化设置与用户资料管理。
- **`brand-story` / `company-info` / `contact-info`：获取品牌背景信息及支持资源。
- **`orders`：实时跟踪订单状态及购买历史。

---

## 💻 命令行接口（CLI）配置与示例

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

- **状态码 401**：凭证缺失或已过期。建议用户登录。
- **状态码 404**：资源未找到。请通过 `search` 命令验证产品路径（slug）是否正确。
- **连接错误**：请确认 `COMMERCE_URL` 环境变量设置正确，并确保后端服务可用。