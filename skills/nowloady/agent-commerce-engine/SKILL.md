---
name: agent-commerce-engine
version: 1.7.1
description: 这是一个适用于“代理式商务”（Agentic Commerce）的、具备生产级功能的通用引擎。该工具允许自主代理通过标准化协议与任何兼容的无头（headless）电子商务后端进行交互，并提供了开箱即用的发现功能、购物车操作以及安全用户管理功能。
tags: [ecommerce, shopping-agent, commerce-engine, standard-protocol, headless-commerce, agentic-web]
metadata: {"openclaw":{"emoji":"🛒","homepage":"https://github.com/NowLoadY/agent-commerce-engine","source":"https://github.com/NowLoadY/agent-commerce-engine","requires":{"bins":["python3"],"tools":[],"env":[],"optionalEnv":["COMMERCE_URL","COMMERCE_BRAND_ID"],"paths":["~/.openclaw/credentials/agent-commerce-engine/"]},"install":[{"id":"python-deps","kind":"pip","package":"requests","label":"Install Python dependencies"}]}}
---
# 标准代理商业引擎（Standard Agentic Commerce Engine）

**标准代理商业引擎**是一份标准的客户端和协议指南，用于将代理（agents）连接到兼容的电子商务后端（e-commerce backends）。它为代理提供了统一的方式来搜索产品、管理购物车、访问账户数据、创建订单，并将支付信息传递给用户。

GitHub 仓库：https://github.com/NowLoadY/agent-commerce-engine

## 快速入门：后端集成

`agent-commerce-engine` 包含了 `SERVER_SPEC.md` 文件，其中包含了为希望提供兼容商业 API 的网站所需的服务器规范。通过实现文档中规定的端点（endpoints），现有的商店就可以支持由代理驱动的产品发现、购物车操作、账户流程和订单创建功能，而无需为每个品牌都开发自定义工具。

## 参考案例：Lafeitu

有关使用该引擎的生产级实现示例，请参阅 [Lafeitu Gourmet Skill](https://clawhub.com/NowLoadY/agentic-spicy-food)。该案例展示了该引擎如何专门应用于一个真实的工匠食品品牌。

---

## 🔒 安全性与隐私保护

为了确保透明度并保护用户数据，标准代理商业引擎遵循以下安全协议：

### 1. 本地凭证存储（Local Credential Persistence）
- **存储位置**：`~/.openclaw/credentials/agent-commerce-engine/`
- **存储机制**：账户和会话令牌（Token）信息以 JSON 格式存储在本地。凭证文件的权限设置为 `0600`（仅限用户访问）。
- **安全升级**：从版本 1.4.0 开始，初次登录后不再存储原始密码。引擎会将密码替换为经过加密的令牌。
- **使用范围**：凭证存储在本地机器上，供当前用户环境重复使用。
- **生命周期**：可以通过运行 `logout` 命令随时清除凭证。

### 2. 安全传输（Secure Transmission）
- **基于令牌的认证（Token-based Auth）**：使用 `x-api-token` 标头来进行身份验证。原始密码仅在 `login` 或 `register` 阶段传输一次，用于换取令牌。
- **强制使用 HTTPS**：客户端会拒绝非 HTTPS 的远程端点。`localhost` 和 `127.0.0.1` 仍可用于本地开发。
- **加密传输**：生产环境中的数据传输必须使用 HTTPS，因此令牌不会通过明文 HTTP 发送。

### 3. 匿名跟踪（Anonymous Tracking）  
- 为了支持未认证用户的购物车功能，会生成一个唯一的、不可识别的 `Visitor ID`（UUID v4）并存储在本地。该 ID 不包含任何个人信息。

---

## 🛠 工具优先级与回退策略（Tool Priority & Fallback Strategy）

为了提供最准确和高效的体验，请遵循以下优先级顺序：

1. **优先使用 API**：始终尝试使用 `commerce.py` 脚本。它提供结构化、高精度的数据。可以通过 `--store <url>` 参数指定目标商店。
2. **无状态请求头（Stateless Headers）**：依赖引擎内置的请求头管理功能（`x-user-account`、`x-visitor-id`）来维护会话的完整性，而无需使用 cookies。
3. **自动纠错**：如果 API 因浏览器请求的特定路径（slug）返回 404 错误，优先以 API 返回的搜索结果作为后端的真实数据来源。

---

## 🧠 代理操作逻辑（Agent Operational Logic）

遵循以下逻辑流程，以确保高质量的用户体验：

### 1. 产品发现与验证（Product Discovery & Validation）
**目标**：在采取任何操作之前，确保产品存在并找到正确的规格信息。
- **操作**：在将商品添加到购物车之前，务必先运行 `search` 或 `list` 命令。
- **逻辑**：使用 API 查找正确的商品路径（slug）和有效的商品变体（variant）规格。通过 `--page` 和 `--limit` 参数安全地浏览大型产品目录，避免超出上下文限制。
- **细化搜索**：如果找到多个结果，根据返回的属性让用户进行进一步选择。如果结果中的 `totalPages` 大于 `page`，则考虑获取下一页或进一步细化搜索。

### 2. 认证与个人资料管理（Authentication & Profile Flow）
**目标**：管理用户隐私和会话数据。
- **逻辑**：API 是无状态的。如果未保存凭证，相关操作会返回 `401 Unauthorized` 错误。
- **命令**：
    - 查看个人资料：`python3 scripts/commerce.py get-profile`
    - 更新个人资料：`python3 scripts/commerce.py update-profile --name "Name" --address "..." --phone "..." --email "..."`
- **所需数据**：遵循特定品牌后端的规范。

### 3. 注册流程（Registration Flow）
**目标**：处理新用户的注册。
- **触发条件**：当用户需要新账户或后端返回 “用户未找到” 时。
- **操作建议**：如果后端支持 `send-code` 和 `register` 命令，请优先使用这些命令。如果后端仅返回注册链接，请引导用户完成注册流程。

### 4. 购物车管理（Shopping Cart Management）
**目标**：精确修改用户的购物车信息。
- **逻辑**：引擎支持增加商品数量或设置商品数量。
- **命令**：
    - 添加商品：`python3 scripts/commerce.py add-cart <slug> --variant <V> --quantity <Q>`
    - 更新商品：`python3 scripts/commerce.py update-cart <slug> --variant <V> --quantity <Q>`
    - 删除商品：`python3 scripts/commerce.py remove-cart <slug> --variant <V>`
    - 清空购物车：`python3 scripts/commerce.py clear-cart`
    - 结账 / 创建订单：`python3 scripts/commerce.py create-order --name <NAME> --phone <PHONE> --province <PROVINCE> --city <CITY> --address <ADDRESS>`
- **验证**：商品变体的选择必须来自产品提供的选项列表中。
- **支付流程（关键步骤）**：由于缺乏财务授权，代理目前无法直接执行消费者的支付操作（如使用信用卡或移动钱包）。一旦通过 `create-order` 创建订单，API 通常会返回一个支付链接。代理必须将该链接传递给用户以完成支付。

### 5. 品牌信息与品牌故事（Brand Information & Storytelling）
**目标**：获取品牌信息和支持数据。
- **逻辑**：使用 `brand-info` 接口来检索品牌的相关内容。
- **工具**：
    - `python3 scripts/commerce.py brand-story`：获取品牌的故事和使命声明。
    - `python3 scripts/commerce.py company-info`：获取公司的正式信息。
    - `python3 scripts/commerce.py contact-info`：获取客户支持渠道。

---

## 🚀 功能概览（Capabilities Summary）

- **`search` / `list`**：产品发现和库存查询。使用 `--page <N>` 和 `--limit <N>` 可安全地分页浏览大型产品目录。
- **`get`**：深入查看产品规格、变体信息和价格信息。
- **`promotions`：当前的业务规则、运费标准和促销活动。
- **`cart`：查看包含 VIP 折扣和税费/运费估算的完整购物车信息。
- **`add-cart` / `update-cart` / `remove-cart` / `clear-cart`：对购物车进行原子级别的操作。
- **create-order**：将购物车内容转换为待处理的订单，并提供安全的支付链接供用户完成支付。
- **get-profile` / `update-profile`：个性化设置和订单详情。
- **brand-story` / `company-info` / `contact-info`：获取品牌相关信息和支持资源。
- **orders`：实时跟踪订单状态和购买历史。

---

## 💻 命令行接口配置与示例（CLI Configuration & Examples）

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

## 🤖 故障排除与调试（Troubleshooting & Debugging）

- **`AUTH_REQUIRED`：令牌缺失或过期。运行 `login` 命令获取新令牌。
- **`AUTH_INVALID`：凭证错误。请验证账户信息和密码。
- **`PRODUCT_NOT_FOUND`：资源未找到。请通过 `search` 命令验证商品路径（slug）。
- **`VARIANT_UNAVAILABLE`：请求的变体无效或缺货。请查看 `instruction` 字段以获取可用替代品。
- **CART_EMPTY`：尝试结账时购物车为空。请先添加商品。
- **连接错误**：请确认 `--store` 参数指定的 URL 正确且端点可访问。