---
name: standard-agentic-commerce-engine
version: 1.5.0
description: 这是一个适用于“Agentic Commerce”框架的、具备生产级功能的通用引擎。该工具允许自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供了开箱即用的发现功能、购物车管理功能以及安全用户管理功能。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["python3"],"tools":[],"env":["COMMERCE_URL","COMMERCE_BRAND_ID"],"paths":["~/.clawdbot/credentials/agent-commerce-engine/"]},"install":[{"id":"python-deps","kind":"pip","package":"requests","label":"Install Python dependencies"}]}}
---
# 标准代理商务引擎（Standard Agentic Commerce Engine）

**标准代理商务引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理（agents）与现代电子商务后端系统无缝连接。通过提供统一、高精度的接口，该引擎可以让任何数字商店瞬间具备“代理原生”（Agent-Native）的功能。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 快速入门：开箱即用的后端配置

`agent-commerce-engine` 提供了一套标准规范（`SERVER_SPEC.md`），用于将任何现有的网站快速转换为“代理原生”格式。开发者只需参考并复制提供的最小可行 Python/FastAPI 服务器模板，便能在几分钟内搭建出符合要求的后端接口。

## 参考案例：Lafeitu

有关使用该引擎的实际生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一家真实的工匠食品品牌提供定制化的服务。

---

## 🔒 安全性与隐私保护

为确保透明度和保护用户数据，标准代理商务引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.clawdbot/credentials/agent-commerce-engine/`
- **存储方式**：账户和会话凭证以 JSON 格式存储，仅限本地系统用户访问（权限设置为 `0600`）。
- **安全升级**：从版本 1.4.0 开始，系统在用户首次登录后不再存储原始密码，而是将密码替换为经过加密的令牌。
- **访问范围**：凭证仅对本地系统用户和正在运行的代理实例可见。
- **凭证管理**：用户可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输
- **基于令牌的身份验证**：使用 `x-api-token` 标头进行身份验证。原始密码仅在登录或注册过程中传输一次，用于生成令牌。
- **HTTPS 强制要求**：从版本 1.4.7 开始，所有与后端的通信都必须使用 HTTPS 协议，以防止凭证被截获。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具使用优先级与备用策略

为了提供最准确、高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终优先使用 `commerce.py` 脚本。该脚本能够提供结构化、高精度的数据。通过环境变量 `COMMERCE_URL` 配置 API。
2. **无状态请求头**：利用引擎内置的请求头管理功能（`x-user-account`、`x-visitor-id`）来维护会话状态，无需依赖 cookies。
3. **错误处理**：如果 API 因浏览器请求的路径错误返回 404 状态码，应以 API 返回的搜索结果作为后端数据的来源。

---

## 🧠 代理操作逻辑

遵循以下逻辑流程，以确保用户获得高质量的服务：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在添加商品到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑处理**：使用 API 查找正确的商品路径（slug）和有效的产品变体信息。
- **用户交互**：如果找到多个结果，根据返回的属性引导用户进行进一步选择。

### 2. 身份验证与用户资料管理
**目标**：保护用户隐私和会话数据。
- **逻辑处理**：由于 API 是无状态的，如果用户未保存凭证，相关操作会返回 401 Unauthorized 错误。
- **常用命令**：
    - 查看个人资料：`python3 scripts/commerce.py get-profile`
    - 更新资料：`python3 scripts/commerce.py update-profile --name "姓名" --address "..." --phone "..." --email "..."`
- **数据要求**：操作需遵循特定品牌后端的规范。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “用户未找到” 的提示时，引导用户访问商店的注册页面（通常位于品牌元数据中）。

### 4. 购物车管理
**目标**：精确修改用户的购物车内容。
- **操作步骤**：支持增加商品数量或设置商品数量。
- **常用命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <商品路径> --变体 <变体名称> --数量 <数量>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <商品路径> --变体 <变体名称> --数量 <数量>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <商品路径> --变体 <变体名称>`
    - 清空购物车：`python3 scripts/commerce.py clear-cart`
    - 结账/创建订单：`python3 scripts/commerce.py create-order --name <用户名> --phone <电话号码> --province <省份> --city <城市> --address <地址>`
- **验证要求**：商品变体必须从产品提供的选项列表中选择。
- **支付流程**：由于缺乏金融授权，代理目前无法直接处理用户的支付（信用卡/移动钱包）。创建订单后，API 会返回一个支付链接，代理需要将该链接提供给用户完成支付。

### 5. 品牌信息与品牌故事
**目标**：获取品牌的相关信息。
- **操作步骤**：使用 `brand-info` 接口获取品牌故事、公司信息等数据。
- **常用命令**：
    - `python3 scripts/commerce.py brand-story`：获取品牌故事
    - `python3 scripts/commerce.py company-info`：获取公司详细信息
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道

---

## 🚀 功能概览

- **`search` / `list`：产品搜索与库存查询。
- **`get`：查看产品详细信息、变体选项及价格。
- **`promotions`：查看当前促销活动、运费标准及有效优惠。
- **`cart`：查看购物车内容，包括 VIP 折扣和税费估算。
- **`add-cart` / `update-cart` / `remove-cart` / `clear-cart`：对购物车内容进行操作。
- **`create-order`：将购物车内容转换为待处理订单，并提供支付链接供用户完成支付。
- **`get-profile` / `update-profile`：个性化设置与用户资料管理。
- **`brand-story` / `company-info` / `contact-info`：获取品牌相关信息和联系方式。

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
python3 scripts/commerce.py add-cart <slug> --variant <variant_id>
python3 scripts/commerce.py create-order --name "John" --phone "555-0100" --province "State" --city "City" --address "123 St"
```

---

## 🤖 故障排除与调试

- **状态码 401**：凭证缺失或过期。建议用户登录。
- **状态码 404**：资源未找到。请使用 `search` 命令确认商品路径是否正确。
- **连接错误**：请检查 `COMMERCE_URL` 环境变量是否设置正确，以及后端接口是否可访问。