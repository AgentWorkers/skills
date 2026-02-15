---
name: odoo-manager
description: 通过官方的 External XML-RPC API 管理 Odoo（联系人、任何业务对象以及元数据）。支持使用 `execute_kw` 对任何模型执行通用的 CRUD 操作，并提供了针对 `res.partner` 和模型内省的现成流程。具备动态实例和数据库切换功能，能够根据上下文自动解析 URL、数据库和凭据信息。
homepage: https://www.odoo.com/documentation/
metadata: {"openclaw":{"emoji":"🏢","requires":{"env":["ODOO_URL","ODOO_DB","ODOO_USERNAME","ODOO_PASSWORD"]},"primaryEnv":"ODOO_PASSWORD"}}
---

# Odoo 管理技能

## 🔐 URL、数据库与凭证解析

### URL 解析

Odoo 服务器 URL 的优先级（从高到低）：

1. `temporary_url` — 用于特定操作的一次性 URL
2. `user_url` — 当前会话的用户自定义 URL
3. `ODOO_URL` — 环境默认 URL

这允许你：

- 在多个 Odoo 实例（生产环境、测试环境、特定客户环境）之间切换
- 在演示数据库上进行测试
- 在不更改全局配置的情况下使用不同的客户环境

**示例（概念性）：**

```text
// Default: uses ODOO_URL from environment
{{resolved_url}}/xmlrpc/2/common

// Override for one operation:
temporary_url = "https://staging.mycompany.odoo.com"
{{resolved_url}}/xmlrpc/2/common

// Override for session:
user_url = "https://client-xyz.odoo.com"
{{resolved_url}}/xmlrpc/2/common
```

### 数据库解析

数据库名称（`db`）的优先级：

1. `temporary_db`
2. `user_db`
3. `ODOO_DB`

使用这些数据库名称，你可以：

- 在同一 Odoo 服务器上处理多个数据库
- 在测试数据库和生产数据库之间切换

### 用户名与密码解析

用户名的优先级：

1. `temporary_username`
2. `user_username`
3. `ODOO_USERNAME`

密码（或 API 密钥）的优先级：

1. `temporary_api_key` 或 `temporary_password`
2. `user_api_key` 或 `user_password`
3. `ODOO_API_KEY`（如果已设置）或 `ODOO_PASSWORD`

**重要提示：**

- Odoo API 密钥用于替代密码进行登录。
- 请像处理真实密码一样保管密码/API 密钥；切勿泄露它们。

环境变量通过标准的 OpenClaw 元数据来管理：`requires.env` 声明 **必需** 的变量（`ODOO_URL`、`ODOO_DB`、`ODOO_USERNAME`、`ODOO_PASSWORD`）。`ODOO_API_KEY` 是一个 **可选** 的环境变量，在需要时可以在环境中设置，但它不包含在元数据中。

### 解析后的值

在运行时，该技能始终使用以下值：

- `{{resolved_url}}` — 最终 URL
- `{{resolved_db}}` — 最终数据库名称
- `{{resolved_username}}` — 最终用户名
- `{{resolved_secret}}` — 实际用于身份验证的密码 **或** API 密钥

这些值是根据上述优先级规则计算得出的。

---

## 🔄 上下文管理

> `temporary_*` 和 `user_*` 是 **由技能逻辑使用的运行时上下文变量**，而不是 OpenClaw 元数据字段。OpenClaw 没有 `optional.context` 元数据键；上下文是在运行时动态解析的，具体方式如下所述。

### 临时上下文（一次性使用）

**用户示例：**

- “对于此请求，使用 staging Odoo 实例”
- “仅在此操作中使用 odoo_demo 数据库”
- “仅为此操作使用该用户名进行连接”

**行为：**

- 设置 `temporary_*`（url、db、username、api_key/password）
- 仅用于 **一个逻辑操作**
- 使用后自动清除

这适用于：

- 在两个环境之间比较数据
- 在不同的数据库上执行单一检查

### 会话上下文（当前会话）

**用户示例：**

- “在客户 XYZ 的 Odoo 实例上工作”
- “在此会话中使用 clientx_prod 数据库”
- “使用我的管理员账户进行后续操作”

**行为：**

- 设置 `user_*`（url、db、username、api_key/password）
- 在整个当前会话中保持这些值
- 只有 `temporary_*` 或清除 `user_*` 时才会被覆盖

### 重置上下文

**用户示例：**

- “恢复到 Odoo 的默认配置”
- “清除我的 Odoo 用户上下文”

**操作：**

- 清除 `user_url`、`user_db`、`user_username`、`user_password`、`user_api_key`
- 技能将回退到环境变量（`ODOO_URL`、`ODOO_DB`、`ODOO_USERNAME`、`ODOO_PASSWORD` / `ODOO_API_KEY`）

### 查看当前上下文

**用户示例：**

- “你连接到了哪个 Odoo 实例？”
- “显示当前的 Odoo 配置”

**响应应显示（但不会显示完整密码）：**

```text
Current Odoo Context:
- URL: https://client-xyz.odoo.com (user_url)
- DB: clientxyz_prod (user_db)
- Username: api_integration (user_username)
- Secret: using API key (user_api_key)
- Fallback URL: https://default.odoo.com (ODOO_URL)
- Fallback DB: default_db (ODOO_DB)
```

---

## ⚙️ Odoo XML-RPC 基础

Odoo 通过 **XML-RPC**（而非 REST）暴露部分服务器框架。
外部 API 的文档位于：https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html

两个主要端点：

- `{{resolved_url}}/xmlrpc/2/common` — 身份验证和元数据调用
- `{{resolved_url}}/xmlrpc/2/object` — 通过 `execute_kw` 调用模型方法

### 1. 检查服务器版本

在 `common` 端点调用 `version()` 以验证 URL 和连接性：

```python
common = xmlrpc.client.ServerProxy(f"{resolved_url}/xmlrpc/2/common")
version_info = common.version()
```

示例结果：

```json
{
  "server_version": "18.0",
  "server_version_info": [18, 0, 0, "final", 0],
  "server_serie": "18.0",
  "protocol_version": 1
}
```

### 2. 身份验证

在 `common` 端点使用 `authenticate(db, username, password_or_api_key, {})` 进行身份验证：

```python
uid = common.authenticate(resolved_db, resolved_username, resolved_secret, {})
```

`uid` 是一个整数用户 ID，将在所有后续调用中使用。

如果身份验证失败，`uid` 为 `False` 或 `0` — 技能应：

- 告知用户凭证或数据库无效
- 建议检查 `ODOO_URL`、`ODOO_DB`、用户名和密码

### 3. 使用 execute_kw 调用模型方法

为 `object` 端点构建一个 XML-RPC 客户端：

```python
models = xmlrpc.client.ServerProxy(f"{resolved_url}/xmlrpc/2/object")
```

然后使用以下签名调用 `execute_kw`：

```python
models.execute_kw(
    resolved_db,
    uid,
    resolved_secret,
    "model.name",     # e.g. "res.partner"
    "method_name",    # e.g. "search_read"
    [positional_args],
    {keyword_args}
)
```

此技能中的所有 ORM 操作都是通过 `execute_kw` 来实现的。

---

## 🔍 域名与数据类型（Odoo ORM）

### 域名过滤器

域名是一组条件：

```python
domain = [["field_name", "operator", value], ...]
```

示例：

- 所有公司：`[['is_company', '=', True]]`
- 法国的合作伙伴：`[['country_id', '=', france_id]]`
- 概率大于 50% 的潜在客户：`[['probability', '>', 50]]`

常用操作符：

- `"="`, `"!="`, `">"`, `">="`, `"<"`, `"<="`
- `"like"`, `"ilike"`（不区分大小写）
- `"in"`, `"not in"`
- `"child_of"`（层次关系）

### 字段值约定

- **整数 / 浮点数 / 字符串 / 文本**：使用原生类型。
- **日期 / 时间日期**：字符串格式为 `YYYY-MM-DD` 或 ISO 8601。
- **Many2one**：写入时通常发送 **记录 ID`（`int`）；读取时通常返回 `[id, display_name]`。
- **One2many / Many2many**：写入时使用 Odoo 的 **命令列表** 协议（此处未详细说明；如需详细信息，请参阅 Odoo 文档）。

---

## 🧩 通用 ORM 操作（execute_kw）

以下每个小节展示了典型的用户查询及其对应的 `execute_kw` 使用方法。这些方法适用于 **任何** 模型（而不仅仅是 `res.partner`）。

### 列出/搜索记录（search）

**用户查询：**

- “列出所有公司合作伙伴”
- “查找已确认的销售订单”

**操作（通用）：**

```python
ids = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "search",
    [domain],
    {"offset": 0, "limit": 80}
)
```

注意：

- `domain` 是一个列表（可以为空 `[]` 以匹配所有记录）。
- 使用 `offset` 和 `limit` 进行分页。

### 统计记录数量（search_count）

**用户查询：**

- “有多少公司是公司？”
- “统计正在进行中的任务数量”

**操作：**

```python
count = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "search_count",
    [domain]
)
```

### 根据 ID 读取记录（read）

**用户查询：**

- “显示合作伙伴 7 的详细信息”
- “提供这些 ID 对应的 name 和 country_id 字段”

**操作：**

```python
records = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "read",
    [ids],
    {"fields": ["name", "country_id", "comment"]}
)
```

如果省略了 `fields`，Odoo 会返回所有可读字段（通常很多字段）。

### 一步搜索和读取（search_read）

`search()` 和 `read()` 的快捷方式。

**用户查询：**

- “列出公司（名称、国家）”
- “显示前 5 个合作伙伴及其国家”

**操作：**

```python
records = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "search_read",
    [domain],
    {
        "fields": ["name", "country_id", "comment"],
        "limit": 5,
        "offset": 0,
        # Optional: "order": "name asc"
    }
)
```

### 创建记录（create）

**用户查询：**

- “创建一个新的合作伙伴 ‘New Partner’”
- “在项目 X 中创建一个新的任务”

**操作：**

```python
new_id = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "create",
    [{
        "name": "New Partner"
        # other fields...
    }]
)
```

返回新创建的记录 ID。

### 更新记录（write）

**用户查询：**

- “更新合作伙伴 7 的信息，更改其名称”
- “降低这些潜在客户的概率”

**操作：**

```python
success = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "write",
    [ids, {"field": "new value", "other_field": 123}]
)
```

注意：

- `ids` 是记录 ID 的列表。
- `ids` 中的所有记录都会收到 **相同的** 更新值。

### 删除记录（unlink）

**用户查询：**

- “删除这个测试合作伙伴”
- “删除这些临时任务”

**操作：**

```python
success = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "model.name", "unlink",
    [ids]
)
```

### 基于名称的搜索（name_search）

适用于具有显示名称的模型（例如合作伙伴、产品）的快速查找。

**用户查询：**

- “查找名称包含 ‘Agrolait’ 的合作伙伴”

**操作：**

```python
results = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "name_search",
    ["Agrolait"],
    {"limit": 10}
)
```

结果是一个包含 `[id, display_name]` 的列表。

---

## 👥 联系人/合作伙伴（res.partner）

`res.partner` 是 Odoo 中联系人、公司和多种业务关系的核心模型。

### 列出公司合作伙伴

**用户查询：**

- “列出所有公司”
- “显示带有国家信息的公司”

**操作：**

```python
companies = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "search_read",
    [[["is_company", "=", True]]],
    {"fields": ["name", "country_id", "comment"], "limit": 80}
)
```

### 获取单个合作伙伴

**用户查询：**

- “显示合作伙伴 7”
- “提供合作伙伴 7 的国家信息和备注”

**操作：**

```python
[partner] = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "read",
    [[7]],
    {"fields": ["name", "country_id", "comment"]}
)
```

### 创建新合作伙伴

**用户查询：**

- “创建一个名为 ‘Agrolait 2’ 的新公司”
- “创建一个隶属于公司 X 的个人联系人”

**最小化代码示例：**

```python
partner_id = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "create",
    [{
        "name": "New Partner",
        "is_company": True
    }]
)
```

**其他字段示例：**

- `street`、`zip`、`city`、`country_id`
- `email`、`phone`、`mobile`
- `company_type`（`"person"` 或 `"company"`）

### 更新合作伙伴

**用户查询：**

- “更改合作伙伴 7 的地址”
- “更新国家和电话信息”

**操作：**

```python
models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "write",
    [[7], {
        "street": "New street 1",
        "phone": "+33 1 23 45 67 89"
    }]
)
```

### 删除合作伙伴

**用户查询：**

- “删除测试合作伙伴 999”

**操作：**

```python
models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "unlink",
    [[999]]
)
```

---

## 🧱 模型查询（ir.model, ir.model.fields, fields_get）

### 发现模型的字段（fields_get）

**用户查询：**

- “res.partner 模型有哪些字段？”
- “显示该模型的字段类型和标签”

**操作：**

```python
fields = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "res.partner", "fields_get",
    [],
    {"attributes": ["string", "help", "type"]}
)
```

结果是一个从字段名称到元数据的映射：

```json
{
  "name": {"type": "char", "string": "Name", "help": ""},
  "country_id": {"type": "many2one", "string": "Country", "help": ""},
  "is_company": {"type": "boolean", "string": "Is a Company", "help": ""}
}
```

### 列出所有模型（ir.model）

**用户查询：**

- “我的 Odoo 数据库中有哪些模型？”

**操作：**

```python
models_list = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "ir.model", "search_read",
    [[]],
    {"fields": ["model", "name", "state"], "limit": 200}
)
```

`state` 表示模型是在代码中定义的（`"base"`）还是动态创建的（`"manual"`）。

### 列出特定模型的字段（ir.model.fields）

**用户查询：**

- “通过 ir.model.fields 获取 res.partner 模型的字段列表”

**操作（简化版）：**

```python
partner_model_ids = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "ir.model", "search",
    [[["model", "=", "res.partner"]]]
)
fields_meta = models.execute_kw(
    resolved_db, uid, resolved_secret,
    "ir.model.fields", "search_read",
    [[["model_id", "in", partner_model_ids]]],
    {"fields": ["name", "field_description", "ttype", "required", "readonly"], "limit": 500}
)
```

---

## ⚠️ 错误处理与最佳实践

### 常见错误

- **身份验证失败**：URL、数据库、用户名或密码错误 → `authenticate` 返回 `False`，后续调用会失败。
- **访问权限/ACL**：用户没有对某个模型或记录的访问权限。
- **验证错误**：缺少必填字段或违反了约束条件。
- **连接问题**：无法连接到 `xmlrpc/2/common` 或 `xmlrpc/2/object`。

该技能应：

- 明确指出问题是在 **连接**、**凭证** 还是 **业务验证** 方面。
- 提出下一步操作建议（检查环境变量、上下文覆盖、用户权限）。

### 分页

- 在 `search` 和 `search_read` 中使用 `limit` / `offset` 来处理大量数据。
- 对于交互式使用，将默认的 `limit` 设置为一个合理的值（例如 80）。

### 字段选择

- 在可能的情况下，始终为 `read` / `search_read` 提供明确的 `fields` 列表。
- 这可以减少数据量并加快响应速度。

### 域名与性能

- 对于大型数据集，优先使用索引字段和简单的操作符（`=`, `in`）。
- 尽量避免在没有域名的情况下对非常大的表进行无限制的搜索。

---

## 🚀 快速端到端示例

### 示例 1：检查连接并列出公司合作伙伴

1. 解析上下文：`{{resolved_url}}`、`{{resolved_db}}`、`{{resolved_username}}`、`{{resolved_secret}}`
2. 在 `{{resolved_url}}/xmlrpc/2/common` 上调用 `version()`
3. 进行身份验证以获取 `uid`
4. 使用 `search_read` 和域名 `[['is_company', '=', True]]` 调用 `execute_kw` 在 `res.partner` 上

### 示例 2：创建合作伙伴，然后读取其信息

1. 通过 `common.authenticate` 进行身份验证
2. 使用 `{"name": "New Partner", "is_company": True}` 创建一个新的 `res.partner`
3. 使用 `["name", "is_company", "country_id"]` 读取该记录的详细信息

### 示例 3：在另一个数据库上执行操作

1. 设置 `temporary_url` 和/或 `temporary_db` 以指向另一个 Odoo 环境。
2. 进行身份验证并使用解析后的上下文执行所需操作。
3. 临时上下文会自动清除。

---

## 📚 参考资料与功能概述

- 官方 Odoo 外部 API 文档（XML-RPC）：https://www.odoo.com/documentation/18.0/fr/developer/reference/external_api.html
- 需要具有外部 API 访问权限的 Odoo 计划（自定义计划；One App Free / Standard 计划不包含此功能）。

**此技能可以：**

- 使用密码 **或** API 密钥通过 XML-RPC 连接到 Odoo。
- 通过上下文动态切换多个实例和数据库。
- 通过 `execute_kw` 对 **任何** Odoo 模型执行通用的 CRUD 操作（`search`、`search_count`、`read`、`search_read`、`create`、`write`、`unlink`）。
- 为 `res.partner`（联系人/公司）提供现成的操作流程。
- 使用 `fields_get`、`ir.model` 和 `ir.model.fields` 检查模型结构。
- 遵循分页、字段选择和错误处理的最佳实践。