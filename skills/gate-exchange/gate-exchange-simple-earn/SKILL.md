---
name: gate-exchange-simpleearn
version: "2026.3.12-2"
updated: "2026-03-12"
description: >
  **Query Gate: Simple Earn (Uni)**  
  该功能具有高度灵活性，适用于用户咨询关于“Simple Earn”的任何信息，包括订阅、兑换、查询持仓、查询收益，或了解最高年化收益率（APY）等操作。  
  触发相关查询的关键词包括：“Simple Earn”、“Uni”、“subscribe”、“redeem”、“flexible earn”、“positions”、“interest”、“top APY”，以及任何与“Simple Earn”的订阅、兑换、持仓或收益相关的请求。
---
# Gate Exchange 的简单收益功能（Simple Earn Skill）

该功能提供了对 Gate 平台的简单收益（Simple Earn, Uni）服务的灵活读取操作，包括：查询单一货币或所有持仓情况、查询单一货币的利息情况，以及查询预估的年化收益率（APY）。**订阅（subscribe）、赎回（redeem）和更改简单收益设置（change_uni_lend）功能目前不可用**——请勿调用 `cex_earn_create_uni_lend` 或 `cex_earn_change_uni_lend`。当用户请求订阅、赎回或更改设置时，应告知他们该功能目前不支持。

## 触发条件

当用户表达以下意图时，激活此功能：
- 订阅简单收益服务
- 赎回投资
- 查询持仓情况
- 查询利息
- 查询最高年化收益率
- 一键订阅最高年化收益率

## 先决条件

- **依赖库**：需要安装 [gate-mcp](https://github.com/gate/gate-mcp)。
- **身份验证**：进行持仓和写入操作时需要 API 密钥进行身份验证；查询利率和货币信息时无需身份验证。
- **免责声明**：在显示年化收益率或利率时，务必附加以下提示：“此信息仅供参考，不构成投资建议。年化收益率可能会变动。请在订阅前了解产品条款。”

## 服务限制（当前有效）

- **严禁调用任何形式的订阅或赎回 API**：严禁使用 `cex_earn_create_uni_lend` 进行订阅（`type: lend`）或赎回（`type: redeem`）操作。无论用户是否确认，或提供了何种金额/货币，均禁止调用此 API。当用户请求订阅、赎回或一键订阅最高年化收益率时，只需回复：“简单收益服务的订阅和赎回功能目前不支持。”查询持仓情况、利息情况以及查询利率（仅限读取）不受此限制。
- **严禁调用任何形式的更改贷款设置 API**：严禁使用 `cex_earn_change_uni_lend`（例如更改最低利率）。无论用户是否确认，或提供了何种货币/最低利率，均禁止调用此 API。当用户请求更改简单收益设置（例如最低利率）时，应告知他们该操作不支持，并且不要调用 MCP 相关接口。

## 可用的 MCP 工具

| 工具 | 需要身份验证吗？ | 描述 | 参考文档 |
|------|-----------|-----------------|-----------|
| `cex_earn_list_uni_currencies` | 不需要 | 列出支持简单收益服务的货币（包括最低利率、最低借款金额等） | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_get_uni_currency` | 不需要 | 查询单一货币的详细信息（包括最低借款利率） | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_create_uni_lend` | 需要 | **禁止用于订阅或赎回操作**；仅用于 API 参考，切勿调用 | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_change_uni_lend` | 需要 | **严禁以任何形式调用**；仅用于 API 参考，切勿调用 | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_list_user_uni_lends` | 需要 | 查看用户的持仓情况（支持货币筛选） | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_get_uni_interest` | 需要 | 查询单一货币的累计利息 | [earn-uni-api.md](references/earn-uni-api.md) |
| `cex_earn_list_uni_rate` | 不需要 | 查询每种货币的预估年化收益率（用于选择最高年化收益率） | [earn-uni-api.md](references/earn-uni-api.md) |

## 路由规则

| 情况 | 用户意图 | 关键信号词 | 应执行的操作 |
|------|-------------|-----------------|--------|
| 1 | 订阅（借款） | “subscribe”, “lend to Simple Earn” | **禁止操作**：告知用户“简单收益服务的订阅和赎回功能目前不支持”。不要调用 MCP 相关接口。 |
| 2 | 赎回 | “redeem”, “redeem from Simple Earn” | **禁止操作**：告知用户“简单收益服务的订阅和赎回功能目前不支持”。不要调用 MCP 相关接口。 |
| 3 | 单一货币持仓 | “my USDT Simple Earn”, “查询某种货币的持仓情况” | 参见 [scenarios.md](references/scenarios.md) 中的情景 3 |
| 4 | 所有持仓 | “all Simple Earn positions”, “查询所有简单收益持仓” | 参见 [scenarios.md](references/scenarios.md) 中的情景 4 |
| 5 | 单一货币利息 | “interest”, “USDT interest” | 参见 [scenarios.md](references/scenarios.md) 中的情景 5 |
| 6 | 订阅最高年化收益率 | “top APY”, “一键订阅最高年化收益率” | **禁止操作**：告知用户“简单收益服务的订阅和赎回功能目前不支持”。不要调用 MCP 相关接口。 |
| 7 | 更改贷款设置（例如最低利率） | “change min_rate”, “change Simple Earn settings” | **禁止操作**：不要调用 `cex_earn_change_uni_lend`；告知用户该操作不支持。 |
| 8 | 身份验证失败（401/403） | MCP 返回 401/403 错误代码 | 不要向用户展示 API 密钥；提示用户配置 Gate CEX API 密钥。 |

## 执行流程

1. 根据上述路由规则判断用户的意图。
2. 对于情况 1、2、6（订阅/赎回/一键订阅最高年化收益率）：**禁止** 调用 `cex_earn_create_uni_lend`（无论用户是否确认）。只需回复：“简单收益服务的订阅和赎回功能目前不支持。”
3. 对于情况 7（更改贷款设置/最低利率）：**禁止** 调用 `cex_earn_change_uni_lend`（无论用户是否确认）。告知用户该操作不支持，并且不要调用 MCP 相关接口。
4. 对于情况 3、4、5：查阅 [scenarios.md](references/scenarios.md) 中对应的操作流程，并执行相应的读取操作（仅限于查询持仓情况和利息信息）。
5. 对于情况 8：不要向用户展示 API 密钥或原始错误信息；提示用户重新配置 API 密钥或登录。
6. 如果用户的意图不明确（例如未提供货币或金额），在处理之前请询问用户以获取更多信息。

## 相关领域知识

### 核心概念

- **订阅（借款）**：用户向简单收益池出借指定数量的某种货币。利息会在每次结算时支付；为了避免失败，必须提供该货币的最低利率信息。
- **赎回**：用户从收益池中赎回指定数量的货币。赎回的资金将在下一次结算时到账；当前期间的利息仍会计入用户的账户。
- **最低利率（min_rate）**：该货币的最低可接受每小时利率（仅作参考用途；此功能不支持借款操作，因此不要调用 `cex_earn_create_uni_lend`）。
- **预估年化收益率（est_rate）**：通过 `cex_earn_list_uni_rate` 获取的预估年化收益率；用于选择最高年化收益率的货币。该数据仅供参考。
- **利息（interest）**：通过 `cex_earn_get_uni_interest` 获取的某种货币的累计利息。
- **结算时间**：在每个整小时之前和之后的两分钟内，不允许进行借款和赎回操作；如果订阅失败，资金会立即退还。

### 订阅/赎回操作（情况 1、2、6）

**禁止调用订阅/赎回 API**。不要显示订阅/赎回的界面或请求；也不要调用 `cex_earn_create_uni_lend`（无论操作类型是借款还是赎回）。只需回复：“简单收益服务的订阅和赎回功能目前不支持。”

## 安全规则

- **订阅/赎回操作**：**禁止** 使用 `cex_earn_create_uni_lend` 进行订阅或赎回操作；回复“该功能不支持”。此功能不提供任何订阅/赎回相关的 API 调用。
- **更改贷款设置**：**禁止** 以任何形式调用 `cex_earn_change_uni_lend`（例如更改最低利率）；回复“该操作不支持”，并且不要调用 MCP 相关接口。
- **不提供投资建议**：不要推荐特定的货币或预测利率。仅向用户展示数据（例如通过 `list_uni_rate` 获取的最高年化收益率），由用户自行决定。
- **敏感信息保护**：严禁向用户展示 API 密钥、内部端点地址或原始错误信息。
- **金额和货币验证**：拒绝处理负数或零金额的请求；验证用户请求的货币是否在支持范围内（例如通过 `list_uni_currencies` 或 `get_uni_currency` 进行验证）。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 身份验证失败（返回 401/403 错误代码） | “请在 MCP 中配置您的 Gate CEX API 密钥，并确保具有 `earn/account` 权限。” 不要向用户展示 API 密钥或内部详细信息。 |
| 用户请求订阅/赎回 | 不要调用 API；回复“简单收益服务的订阅和赎回功能目前不支持。” |
| 用户请求更改贷款设置（例如最低利率） | 不要调用 `cex_earn_change_uni_lend`；回复“该操作不支持。” |
| `cex_earn_list_user_uni_lends` 或 `cex_earn_get_uni_interest` 失败 | “无法加载用户的持仓信息/利息数据。请检查您的 API 密钥是否具有 `earn/account` 读取权限。” |
| 没有持仓信息或利率数据 | “未找到相关持仓信息。” / “当前无法获取利率数据。” |

## 提示示例与使用场景

有关完整的提示示例和预期行为，请参阅 [scenarios.md](references/scenarios.md)，其中涵盖了所有六种情况（订阅、赎回、单一货币持仓、所有持仓、单一货币利息、订阅最高年化收益率）。