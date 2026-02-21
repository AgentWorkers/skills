---
name: Vincent - Brave Search for agents
description: 使用此技能，您可以通过 Brave Search 在网络上搜索信息或新闻。搜索服务采用按次计费的模式，费用通过 Vincent 信用系统进行结算。
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
# Vincent – 使用Brave Search进行代理搜索

使用此技能可通过Brave Search在网页和新闻中搜索信息。所有请求均通过Vincent后端进行代理处理，该后端负责与Brave Search API进行身份验证、执行速率限制、记录每次调用的费用，并自动从用户的信用余额中扣除费用。

**无需管理API密钥。** 代理通过一个属于`DATA_SOURCES`机密的Vincent API密钥进行身份验证。Vincent在服务器端处理与Brave Search API相关的认证信息——代理永远不会看到或管理Brave API密钥。

所有命令均使用`@vincentai/cli`包。API密钥的存储和解析过程是自动完成的——用户无需直接处理原始密钥或文件路径。

## 安全模型

此技能专为**具有按次计费功能且受人工监控的自主代理操作**而设计。

**无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用Vincent API来创建一个`DATA_SOURCES`机密，从而获得一个受限范围的API密钥。CLI会在创建过程中自动存储该API密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/datasources/` 或 `./datasources/`）在技能的元数据中进行了指定。

**代理的API密钥并非Brave Search的API密钥**，而是用于访问Vincent代理的受限范围令牌。Vincent服务器会代表代理与Brave Search进行身份验证。代理无法直接访问上游API，也无法绕过代理的信用限制和速率限制机制。

**故意启用了模型调用功能**。该技能的目的是让AI代理具备自主的网页搜索能力。代理应独立完成网页和新闻的搜索工作。用户可以通过`https://heyvincent.ai`管理信用余额和支付方式来控制代理的搜索行为。

**所有API请求均通过HTTPS/TLS协议发送至`heyvincent.ai`。**Vincent服务器随后会调用Brave Search API。代理不会直接与Brave Search进行通信。

**密钥生命周期：**
- **创建**：代理运行`secret create`命令并指定`--type DATA_SOURCES`参数——CLI会自动存储API密钥，并返回`keyId`和`claimUrl`。
- **认领**：操作员使用`claimUrl`在`https://heyvincent.ai`进行认领操作，以获取代理的使用权限并充值信用。
- **信用消耗**：每次API调用都会消耗少量信用（具体费用见下文定价信息）。用户需要通过前端界面进行充值。当信用余额耗尽且未设置支付方式时，调用将被拒绝。
- **撤销**：密钥的所有者可以随时通过Vincent前端撤销代理的API密钥。

## 定价

| API端点 | 每次调用费用 |
| --- | --- |
| 网页搜索 | 0.005美元 |
| 新闻搜索 | 0.005美元 |

每次调用都会自动扣除信用费用。响应中会包含 `_vincent.creditRemainingUsd`字段，以便代理能够实时了解剩余信用余额。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新密钥之前，请先检查是否已存在密钥：

```bash
npx @vincentai/cli@latest secret list --type DATA_SOURCES
```

如果找到密钥，请将其`id`作为后续命令的`--key-id`参数使用。如果不存在密钥，则创建一个新的密钥。

### 2. 创建数据源密钥

```bash
npx @vincentai/cli@latest secret create --type DATA_SOURCES --memo "My agent data sources"
```

创建完成后，需将生成的`keyId`（用于后续命令）和`claimUrl`（提供给用户）告知用户。

告知用户：
> “这是您的数据源认领URL：`<claimUrl>`。请使用此URL在`https://heyvincent.ai`进行认领操作并充值信用，以便使用Brave Search和其他数据源。”

**重要提示：** 在进行API调用之前，必须先完成认领操作并确保有足够的信用余额或已设置支付方式。

### 3. 网页搜索

```bash
npx @vincentai/cli@latest brave web --key-id <KEY_ID> --q "latest AI news" --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400个字符）
- `--count`（可选）：返回结果数量（1-20条，默认值：10条）
- `--offset`（可选）：分页偏移量（0-9）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）
- `--country`（可选）：用于显示本地化结果的2位国家代码（例如：`us`、`gb`、`de`）

返回包含标题、URL、描述和元数据的网页搜索结果。

### 4. 新闻搜索

```bash
npx @vincentai/cli@latest brave news --key-id <KEY_ID> --q bitcoin --count 10
```

参数：
- `--q`（必填）：搜索查询（1-400个字符）
- `--count`（可选）：返回结果数量（1-20条，默认值：10条）
- `--freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）

返回包含标题、URL、描述和发布日期的新闻文章。

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

请通过`creditRemainingUsd`字段提醒用户信用余额的剩余情况。

## 速率限制

- 每个API密钥每分钟最多可发起60次请求（涵盖Twitter和Brave Search的所有数据源）。
- 如果达到速率限制，系统会返回`429`错误代码。请稍后重试。

## 重新链接（恢复API访问权限）

如果代理丢失了API密钥，密钥的所有者可以通过前端界面生成一个**重新链接令牌**。代理可以使用该令牌获取新的API密钥。

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI会使用该令牌获取新的API密钥，并自动将其存储起来，同时返回新的`keyId`。重新链接令牌仅限一次性使用，有效期为10分钟。

## 重要注意事项：
- 一个`DATA_SOURCES` API密钥即可用于**所有**数据源（Twitter、Brave Search等）。无需为每个数据源单独配置密钥。
- 创建密钥后，请务必将认领URL告知用户。
- 如果因信用不足导致调用失败，请告知用户在`https://heyvincent.ai`进行充值。