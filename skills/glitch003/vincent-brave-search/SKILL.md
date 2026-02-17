---
name: Vincent - Brave Search for agents
description: 使用此技能，可以通过 Brave Search 在网页和新闻中搜索信息。搜索服务采用按次计费的模式，费用通过 Vincent 信用系统进行结算。
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ~/.openclaw/credentials/datasources
        - ./datasources
---
# Vincent – 使用Brave Search进行代理搜索

使用此技能，您可以通过Brave Search在网页和新闻中搜索信息。所有请求都会通过Vincent后端进行代理处理，该后端负责与Brave Search API进行身份验证、实施请求速率限制，并自动从您的信用余额中扣除费用。

**无需管理API密钥。** 代理使用由Vincent分配的、具有`DATA_SOURCES`权限范围的API密钥进行身份验证。Vincent在服务器端处理与Brave Search API相关的认证信息——代理本身既看不到也无法管理这些API密钥。

## 安全模型

此技能专为**具有按次计费功能且需人工监督的自主代理操作**而设计。

**无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用Vincent API来创建一个`DATA_SOURCES`权限范围的API密钥。代理将此API密钥保存在指定的配置路径中（`~/.openclaw/credentials/datasources/`或`./datasources/`）。

**代理的API密钥并非Brave Search的API密钥**，而是用于访问Vincent代理的权限令牌。Vincent服务器会代表代理与Brave Search进行身份验证。代理无法直接访问上游API，也无法绕过代理的信用限制和速率限制。

**故意启用了模型调用功能**。该技能的目的是让AI代理具备自主的网页搜索能力。代理应自行执行搜索任务，而人工则通过`https://heyvincent.ai`来控制消费情况（包括信用余额和支付方式的管理）。

**所有API请求均通过HTTPS/TLS协议发送至`heyvincent.ai`**，随后Vincent服务器会调用Brave Search API。代理不会直接与Brave Search进行交互。

**密钥生命周期：**
- **创建**：代理通过发送`POST /api/secrets`请求（`type: "DATA_SOURCES"`）来创建数据源权限密钥。API会返回一个权限范围的API密钥以及一个用于声明所有权的URL。
- **声明所有权**：操作员需要使用该URL在`https://heyvincent.ai`上声明所有权、添加信用并管理支付。
- **费用**：每次API调用都会产生少量费用（详见下方价格信息）。当信用余额不足且未设置支付方式时，请求将被拒绝。
- **撤销**：密钥所有者可以随时通过Vincent的前端界面撤销代理的API密钥。

## 价格信息

| API端点 | 每次调用费用 |
| --- | --- |
| 网页搜索 | 0.005美元 |
| 新闻搜索 | 0.005美元 |

费用会自动从您的信用余额中扣除。响应中会包含 `_vincent.creditRemainingUsd`字段，以便代理能够实时了解剩余余额。

## 配置要求

所有API请求都必须使用权限令牌（即在创建`DATA_SOURCES`密钥时获得的API密钥）。

创建密钥后，请将其保存在指定的配置路径中。如果是OpenClaw实例，请将其保存在`~/.openclaw/credentials/datasources/<API_KEY_ID>.json`文件中；否则，请保存在当前工作目录下的`datasources/<API_KEY_ID>.json`文件中。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建数据源权限密钥

如果您还没有`DATA_SOURCES` API密钥，请先创建一个：

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "DATA_SOURCES",
    "memo": "My agent data sources"
  }'
```

响应内容包括：
- `apiKey`：一个权限范围的API密钥，请妥善保管，并将其用作所有数据源请求的权限令牌。
- `claimUrl`：分享给用户，以便其声明所有权并添加信用。

创建完成后，告知用户：
> “这是您的数据源声明URL：`<claimUrl>`。请使用此URL在`https://heyvincent.ai`上声明所有权并添加信用。”

**重要提示：** 在进行API调用之前，必须先声明所有权并确保有足够的信用余额或已设置有效的支付方式。

### 2. 网页搜索

通过关键词在网页上搜索信息。

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/brave/web?q=latest+AI+news&count=10" \
  -H "Authorization: Bearer <API_KEY>"
```

参数：
- `q`（必填）：搜索查询（1-400个字符）
- `count`（可选）：返回结果数量（1-20条，默认为10条）
- `offset`（可选）：分页偏移量（0-9）
- `freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）
- `country`（可选）：用于获取本地化结果的国家代码（例如`us`、`gb`、`de`）

返回包含标题、URL、描述和元数据的网页结果。

### 3. 新闻搜索

搜索最新的新闻文章。

```bash
curl -X GET "https://heyvincent.ai/api/data-sources/brave/news?q=bitcoin&count=10" \
  -H "Authorization: Bearer <API_KEY>"
```

参数：
- `q`（必填）：搜索查询（1-400个字符）
- `count`（可选）：返回结果数量（1-20条，默认为10条）
- `freshness`（可选）：时间筛选条件（`pd`：过去一天；`pw`：过去一周；`pm`：过去一个月；`py`：过去一年）

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

当信用余额较低时，可以使用`creditRemainingUsd`字段来提醒用户。

## 速率限制

- 每个API密钥每分钟最多允许60次请求（包括Twitter和Brave Search的请求）。
- 如果超出速率限制，系统会返回`429`错误代码。请稍后再试。

## 重新链接（恢复API访问权限）

如果代理丢失了API密钥，密钥所有者可以通过前端界面生成一个新的**重新链接令牌**。代理可以使用该令牌获取新的API密钥。

```bash
curl -X POST "https://heyvincent.ai/api/secrets/relink" \
  -H "Content-Type: application/json" \
  -d '{
    "relinkToken": "<TOKEN_FROM_USER>",
    "apiKeyName": "Re-linked API Key"
  }'
```

重新链接令牌为一次性使用，有效期为10分钟。

## 重要注意事项：
- 在创建新的数据源权限密钥之前，请务必先在指定的配置路径中查找现有的API密钥。如果是OpenClaw实例，请在`~/.openclaw/credentials/datasources/`中查找；否则，请在`./datasources/`中查找。
- 一个`DATA_SOURCES` API密钥即可用于所有数据源（Twitter、Brave Search等）。无需为每个数据源单独配置密钥。
- 创建权限密钥后，请务必将声明URL分享给用户。
- 如果请求因信用不足而被拒绝，请告知用户在`https://heyvincent.ai`上添加信用余额。