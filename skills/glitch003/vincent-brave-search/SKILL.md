---
name: Vincent - Brave Search for agents
description: 该技能支持网页搜索和新闻搜索功能，由 Brave Search 提供技术支持。当用户需要浏览网页、查找新闻文章或查询最新信息时，可以使用此技能。搜索服务采用按次计费的方式，通过 Vincent 信用系统进行收费。触发该技能的指令包括：“search the web”、“web search”、“brave search”、“search news”、“find information”以及“look up”和“current events”。
allowed-tools: Read, Write, Bash(npx:*, curl:*)
version: 1.0.0
author: HeyVincent <contact@heyvincent.ai>
license: MIT
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources
        - ./datasources
---
# Vincent – 使用 Brave Search 进行代理搜索

使用此技能可以通过 Brave Search 在网页和新闻中搜索信息。所有请求都会通过 Vincent 后端进行代理处理，该后端负责与 Brave Search API 进行身份验证、执行请求速率限制，并自动从用户的信用余额中扣除费用。

**无需管理 API 密钥。** 代理使用由 Vincent API 密钥进行身份验证，该密钥的权限范围被限定为 `DATA_SOURCES` 秘密信息。Vincent 在服务器端处理与 Brave Search API 相关的认证信息——代理本身既看不到也无法管理这些 API 密钥。

所有命令都依赖于 `@vincentai/cli` 包。API 密钥的存储和解析过程是自动完成的——用户无需直接处理原始密钥或文件路径。

## 安全模型

此技能专为**具有按次计费功能且受人工监控的自主代理操作**而设计。

**无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 来创建一个 `DATA_SOURCES` 秘密信息，从而获取一个权限受限的 API 密钥。CLI 会在创建过程中自动保存该 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）在技能的元数据中进行了指定。

**代理的 API 密钥并非 Brave Search 的 API 密钥**，而是用于访问 Vincent 代理的权限受限的令牌。Vincent 服务器会代表代理与 Brave Search 进行身份验证。代理无法直接访问上游的 API，也无法绕过代理的信用限制和速率限制机制。

**故意启用了模型调用功能**。该技能的目的是为了让 AI 代理具备自主的网页搜索能力。代理应自行执行网页和新闻搜索操作，而人工则通过 `https://heyvincent.ai` 来控制代理的信用使用和支付方式。

**所有 API 请求均通过 HTTPS/TLS 协议发送至 `heyvincent.ai`**，之后 Vincent 服务器才会调用 Brave Search API。代理本身不会直接与 Brave Search 交互。

**密钥生命周期：**
- **创建**：代理通过 `secret create` 命令（参数为 `--type DATA_SOURCES`）来创建密钥，CLI 会自动保存 API 密钥，并返回一个 `keyId` 和 `claimUrl`。
- **认领**：操作员需要使用 `claimUrl` 在 `https://heyvincent.ai` 进行认领操作，以获取代理的使用权并添加信用。
- **信用消耗**：每次 API 请求都会消耗一定金额的信用（具体费用见下文定价信息）。当信用余额耗尽且未设置支付方式时，请求将被拒绝。
- **撤销**：密钥的所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。

## 定价

| API 端点 | 每次请求费用 |
| --- | --- |
| 网页搜索 | 0.005 美元 |
| 新闻搜索 | 0.005 美元 |

每次请求都会自动扣除相应的信用费用。响应中会包含 `_vincent.creditRemainingUsd` 字段，以便代理可以随时查看剩余信用余额。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新的秘密信息之前，请先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果找到了密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用；如果不存在密钥，则需要创建一个新的秘密信息。

### 2. 创建数据源秘密信息

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

创建完成后，需要将 `keyId`（用于后续命令）和 `claimUrl`（提供给用户）告知用户。

完成后，告诉用户：
> “这是您的数据源认领 URL：`<claimUrl>`。请使用该 URL 在 `https://heyvincent.ai` 进行认领操作，以获取使用权限并添加用于 Brave Search 和其他数据源的信用。”

**重要提示：** 在进行 API 请求之前，必须先完成认领操作并确保有足够的信用余额或已设置支付方式。

### 3. 网页搜索

```bash
npx @vincentai/cli@latest brave web --key-id <KEY_ID> --q "latest AI news" --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400 个字符）
- `--count`（可选）：返回结果数量（1-20 条，默认值：10 条）
- `--offset`（可选）：分页偏移量（0-9）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）
- `--country`（可选）：用于显示本地化结果的 2 位国家代码（例如：`us`、`gb`、`de`）

返回包含标题、URL、描述和元数据的网页搜索结果。

### 4. 新闻搜索

```bash
npx @vincentai/cli@latest brave news --key-id <KEY_ID> --q bitcoin --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400 个字符）
- `--count`（可选）：返回结果数量（1-20 条，默认值：10 条）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）

返回包含标题、URL、描述、发布日期和来源信息的新闻文章。

## 响应元数据

每个成功的响应都会包含一个 `_vincent` 对象，其中包含以下信息：

```json
{
  "_vincent": {
    "costUsd": 0.005,
    "creditRemainingUsd": 4.99
  }
}
```

可以通过 `_vincent.creditRemainingUsd` 字段来提醒用户剩余的信用余额。

## 输出格式

网页搜索结果的输出格式如下：

```json
{
  "web": {
    "results": [
      {
        "title": "Article Title",
        "url": "https://example.com/article",
        "description": "A brief description of the article content."
      }
    ]
  },
  "_vincent": {
    "costUsd": 0.005,
    "creditRemainingUsd": 4.99
  }
}
```

新闻搜索结果的输出格式与此相同，但每条结果还会包含 `age`（发布时间）和 `source`（来源）字段。

## 错误处理

| 错误代码 | 原因 | 解决方案 |
| ------- | ------- | ------------ |
| `401 Unauthorized` | API 密钥无效或缺失 | 确认 `key-id` 是否正确；如有必要，请重新获取密钥 |
| `402 Insufficient Credit` | 信用余额为零且未设置支付方式 | 用户需在 `heyvincent.ai` 添加信用 |
| `429 Rate Limited` | 每分钟请求次数超过限制（60 次） | 等待片刻后重试 |
| `Key not found` | API 密钥已被撤销或从未创建 | 请向密钥所有者请求新的令牌 |

## 速率限制

- 每个 API 密钥每分钟允许的请求次数为 60 次（涵盖所有数据源，包括 Twitter 和 Brave Search）。
- 如果达到速率限制，系统会返回 `429` 错误代码。请稍后重试。

## 重新获取 API 访问权限

如果代理丢失了 API 密钥，密钥所有者可以通过前端生成一个新的 **令牌**。代理可以使用该令牌获取新的 API 密钥：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，并自动将其保存，同时返回新的 `keyId`。重新获取的令牌仅限一次性使用，有效期为 10 分钟。

## 重要说明：
- 单个 `DATA_SOURCES` API 密钥适用于 **所有** 数据源（Twitter、Brave Search 等）。无需为每个数据源分别配置密钥。
- 创建秘密信息后，务必将认领 URL 提供给用户。
- 如果请求因信用不足而被拒绝，请告知用户在 `https://heyvincent.ai` 添加信用余额。