---
name: standard-agentic-commerce-engine
version: 1.4.5
description: 这是一个专为“Agentic Commerce”设计的、具备生产环境适用性的通用引擎。该工具允许自主代理通过标准化的协议与任何兼容的无头（headless）电子商务后端进行交互，同时提供了开箱即用的发现功能、购物车操作以及安全用户管理支持。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata:
  clawdbot:
    emoji: 🛒
    requires:
      bins:
        - python3
      tools:
        - web_search
        - web_fetch
      env:
        - name: COMMERCE_URL
          description: Target API base URL (e.g. https://api.brand.com/v1)
        - name: COMMERCE_BRAND_ID
          description: Unique slug for the brand to differentiate credential storage
      paths:
        - ~/.clawdbot/credentials/agent-commerce-engine/
    install:
      - id: python-deps
        kind: pip
        package: requests
        label: "Install Python dependencies"
---
# 标准代理商业引擎（Standard Agentic Commerce Engine）

**标准代理商业引擎**是一款专为生产环境设计的工具，它能够将自主运行的代理程序（agents）与现代电子商务后端系统无缝连接。通过提供统一且高精度的接口，该引擎可以让任何数字店面立即具备“代理原生”（Agent-Native）的功能。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 参考案例：Lafeitu

有关使用该引擎的生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawdhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何为一个真实的工匠食品品牌提供定制化的服务。

---

## 🔒 安全性与隐私保护

为了确保透明度和保护用户数据，标准代理商业引擎遵循以下安全协议：

### 1. 本地凭证存储
- **存储位置**：`~/.clawdbot/credentials/agent-commerce-engine/`
- **存储方式**：账户和会话令牌（Token）信息以 JSON 格式存储在本地，权限设置为 `0600`（仅限用户访问）。
- **安全升级**：从版本 1.4.0 开始，系统在用户首次登录后不再存储原始密码，而是将密码替换为经过加密的令牌。
- **访问范围**：这些数据仅对本地系统用户和正在运行的代理程序实例可见。
- **凭证管理**：用户可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输
- **基于令牌的认证**：使用 `x-api-token` 标头来验证用户身份。原始密码仅在登录或注册过程中传输一次，用于生成令牌。
- **加密传输**：所有与后端的通信都必须通过 HTTPS 进行，以确保令牌在传输过程中的安全性。

### 3. 匿名跟踪（访客 ID）
- 为了支持未登录用户的购物车功能，系统会生成一个唯一的、不可识别的 `访客 ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具优先级与备用策略

为了提供最准确、高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终优先尝试使用 `commerce.py` 脚本。该脚本能够提供结构化、高精度的数据。您可以通过环境变量 `COMMERCE_URL` 来配置它。
2. **无状态请求头**：依赖引擎内置的请求头管理功能（`x-user-account`、`x-visitor-id`）来维护会话状态，而无需使用 cookies。
3. **错误处理**：如果 API 因浏览器请求的特定路径（slug）返回 404 错误，应以 API 返回的搜索结果作为后端数据的权威来源。

---

## 🧠 代理程序运行逻辑

遵循以下逻辑流程，以确保用户获得高质量的服务体验：

### 1. 产品发现与验证
**目标**：在采取任何操作之前，确保产品存在并获取正确的规格信息。
- **操作步骤**：在将商品添加到购物车之前，务必先执行 `search` 或 `list` 操作。
- **逻辑处理**：使用 API 获取正确的商品路径（slug）以及有效的克重（gram）/变体（variant）信息。
- **用户交互**：如果找到多个结果，根据返回的属性让用户进行进一步选择。

### 2. 认证与用户资料管理
**目标**：管理用户隐私和会话数据。
- **逻辑处理**：由于 API 是无状态的，如果用户未保存凭证，相关操作会返回 401 Unauthorized 错误。
- **命令示例**：
    - 查看用户资料：`python3 scripts/commerce.py get-profile`
    - 更新用户资料：`python3 scripts/commerce.py update-profile --name "Name" --address "..."`
- **数据要求**：必须遵守特定品牌后端的数据格式要求。

### 3. 注册流程
**目标**：处理新用户的注册请求。
- **触发条件**：当系统返回 “User Not Found” 错误时，引导用户访问品牌的注册页面。
- **操作提示**：提示用户访问品牌的注册链接（通常位于品牌元数据中）。

### 4. 购物车管理
**目标**：精确地修改用户的购物车内容。
- **逻辑处理**：引擎支持增加商品数量或设置商品数量。
- **命令示例**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --gram <G> --quantity <Q>`
    - 更新商品数量：`python3 scripts/commerce.py update-cart <slug> --gram <G> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --gram <G>`
- **验证要求**：商品的数量/变体必须从产品提供的选项列表中选择。

### 5. 品牌信息与品牌故事
**目标**：获取品牌的相关信息和故事内容。
- **操作步骤**：使用 `brand-info` 接口来检索品牌的故事和使命宣言。
- **工具示例**：
    - `python3 scripts/commerce.py brand-story`：获取品牌的故事内容。
    - `python3 scripts/commerce.py company-info`：获取品牌的基本信息。
    - `python3 scripts/commerce.py contact-info`：获取品牌联系方式。

---

## 🚀 功能概览

- **`search` / `list`：用于发现产品并扫描库存。
- **`get`：详细查看产品规格、变体及价格信息。
- **`promotions`：查看当前的促销活动、配送规则及有效优惠。
- **`cart`：提供完整的购物车信息，包括 VIP 折扣和税费/运费估算。
- **`add-cart` / `update-cart` / `remove-cart`：实现对购物车的原子级操作。
- **`get-profile` / `update-profile`：管理用户个人资料和订单信息。
- **`brand-story` / `company-info` / `contact-info`：获取品牌背景和支持信息。
- **`orders`：实时跟踪订单状态和购买历史。

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
- **状态码 404**：表示资源未找到。请通过 `search` 命令检查商品路径（slug）是否正确。
- **连接错误**：请确认 `COMMERCE_URL` 环境变量设置正确，并确保后端服务可访问。