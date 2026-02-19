---
name: bind-mcp
description: Bind协议MCP服务器用于凭证验证、策略制定以及零知识证明（zero-knowledge proof）的生成。
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - BIND_API_KEY
      bins:
        - node
        - npx
    primaryEnv: BIND_API_KEY
    homepage: https://docs.bindprotocol.xyz/mcp/overview
    install:
      - kind: node
        package: "@bind-protocol/mcp-server"
        bins: []
---
# 绑定MCP服务器——代理技能指南

您可以使用Bind Protocol的MCP服务器。本文档将指导您如何使用它。

## 先决条件与安装

### 要求

- **Node.js >= 18** — 运行服务器所必需（`npx`会自动处理包安装）
- **Bind账户** — API支持的工具需要此账户。请在https://dashboard.bindprotocol.xyz创建一个账户
- **代理密钥** (`idbr_agent_...`) — API支持的工具需要此密钥。普通的API密钥（`idbr_`）不支持MCP

### 凭据设置

Bind使用**代理密钥**进行MCP身份验证。代理密钥是具有特定权限的API密钥，允许组织管理员控制哪些工具可用、设置每日使用限制以及获取审计日志。

| 密钥类型 | 格式 | MCP支持 |
|----------|--------|---------------|
| **代理密钥** | `idbr_agent_<keyId>_<secret>` | 是 — API支持的工具必需 |
| **普通API密钥** | `idbr_<keyId>_<secret>` | 否 — MCP服务器会拒绝 |

要创建代理密钥：
1. 登录https://dashboard.bindprotocol.xyz
2. 转到**设置 > 代理密钥**
3. 选择密钥可以访问的工具类别（例如，仅限凭证验证，或包括策略制定和验证）
4. 复制密钥 — 密钥仅显示一次

### MCP服务器配置

将服务器添加到您的MCP客户端配置中。具体文件取决于您使用的工具：

| 工具 | 配置文件 |
|------|------------|
| Claude Code | 项目根目录下的`.mcp.json`，或`~/.claude/claude_desktop_config.json` |
| Claude Desktop | 设置 > 开发者 > 编辑配置 |
| Cursor | 项目根目录下的`.cursor/mcp.json` |
| Windsurf | MCP设置 |

**配置JSON：**

```json
{
  "mcpServers": {
    "bind": {
      "command": "npx",
      "args": ["@bind-protocol/mcp-server"],
      "env": {
        "BIND_API_KEY": "${BIND_API_KEY}"
      }
    }
  }
}
```

在启动AI工具之前，必须在shell中设置`BIND_API_KEY`环境变量为代理密钥。**切勿直接在配置文件中硬编码密钥** — 始终使用环境变量引用，以避免在共享配置或仓库中意外泄露凭证。

**环境变量：**

| 变量 | 是否必需 | 默认值 | 描述 |
|----------|----------|---------|-------------|
| `BIND_API_KEY` | 对于API支持的工具 | — | 代理密钥（`idbr_agent_...`）。如果没有此密钥，只能使用本地工具。 |
| `BIND_API_URL` | 否 | `https://api.bindprotocol.xyz` | API调用的基础URL |
| `BIND_RECEIPTS_PATH` | 否 | `~/.bind/receipts` | 收据链数据的目录 |
| `LOG_LEVEL` | 否 | `info` | 日志详细程度（`debug`, `info`, `warn`, `error`）

### 验证设置

如果您没有`bind`工具，提示用户完成上述设置。您可以通过调用`bind_whoami`来测试连接性 — 如果返回组织信息，则表示代理密钥已通过身份验证。如果没有`BIND_API_KEY`，则只能使用本地工具（解析、验证、哈希）。

---

## 架构与数据流

服务器通过`npx`在本地运行，并通过标准输入/输出（stdio）与您的AI工具通信。它提供了本地工具（始终可用）和基于API的工具（需要代理密钥）。您只需按名称调用工具 — 路由会自动处理。

| 工具类型 | 身份验证 | 功能 |
|-----------|------|---------|
| **本地工具** | 无 | 在设备上解析、验证和哈希VC-JWT |
| **基于API的工具** | 通过`BIND_API_KEY`使用代理密钥 | 支持策略制定、证明、颁发机构、撤销等操作 |

### 什么数据保留在本地，什么数据会发送到API

了解隐私模型非常重要：

**本地数据（凭证数据永远不会离开机器）：**
- `bind_parse_credential` — 在您的机器上完全解码JWT
- `bind_verify_credential` — 从Bind API获取发行机构的公钥JWKS（仅获取公钥），然后在本地验证签名。凭证本身永远不会被发送。
- `bind_hash_credential` — 在本地计算SHA-256哈希值。仅使用不可逆的哈希值进行撤销检查。

**基于API的工具（向`api.bindprotocol.xyz`发送请求）：**
- `bind_check_revocation` — 仅发送凭证的**哈希值**（不发送凭证本身）。哈希值是不可逆的。
- `bindResolveIssuer` — 获取组织的公钥。不涉及凭证数据。
- `bind_explain_policy`, `bind_list_policies`, `bind_list_circuits` — 仅读取公共元数据。不涉及凭证数据。
- `bind_submit_prove_job` — 将电路输入发送到Bind证明服务。这些是正在被证明的原始值（例如，收入金额、里程数）。
- `bind_issue_credential` — 请求Bind API根据完成的证明签署并颁发VC-JWT。
- `bind_create_policy`, `bind_validate_policy` — 将策略规范JSON发送到Bind进行验证/存储。
- `bind_share_proof` — 通过Bind API与验证组织共享证明记录。

**简而言之：** 原始凭证数据仅保留在本地。哈希值、策略规范、证明输入和元数据会发送到API。

---

## 工具清单

### 本地工具（无需身份验证，凭证数据保留在机器上）

| 工具 | 功能 |
|------|-------------|
| `bind_parse_credential` | 解码VC-JWT，提取头部、负载和签名（不进行验证） |
| `bind_verify_credential` | 完整验证：解析、获取发行机构的JWKS、验证ES256签名、检查有效期。不检查撤销状态。 |
| `bind_hash_credential` | 对VC-JWT进行SHA-256哈希处理。使用哈希值与`bind_check_revocation`一起使用。 |

### 基于API的工具（需要通过`BIND_API_KEY`使用代理密钥）

**发现与检查**

| 工具 | 功能 |
|------|-------------|
| `bindResolveIssuer` | 根据组织ID获取组织的公钥JWKS |
| `bind_explain_policy` | 根据策略ID获取策略的公共规范 |
| `bind_check_revocation` | 通过哈希值检查凭证是否已被撤销（仅检查哈希值，不检查凭证本身） |
| `bind_list_policies` | 列出可用的策略（支持`limit`/`offset`分页） |
| `bind_list_circuits` | 列出可用的ZK电路 |

**证明生成与凭证颁发**

| 工具 | 功能 |
|------|-------------|
| `bind_submit_prove_job` | 提交带有电路ID和输入的ZK证明生成任务 |
| `bind_get_prove_job` | 根据任务ID查询证明任务的状态 |
| `bind_list_prove_jobs` | 列出证明任务（可选地按状态过滤） |
| `bind_issue_credential` | 根据完成的证明颁发可验证的凭证 |
| `bind_share_proof` | 通过Bind API与验证组织共享证明记录 |

**策略制定**

| 工具 | 功能 |
|------|-------------|
| `bind_whoami` | 获取经过身份验证的组织信息、层级、策略限制和代理密钥权限 |
| `bind_validate_policy` | 预运行策略规范的验证（在创建前捕获错误） |
| `bind_create_policy` | 创建新的验证策略 |
| `bind_generate_circuit` | 触发保存策略的ZK电路编译 |
| `bind_get_circuit_status` | 查询电路编译任务的状态 |

---

## 工作流程1：完整凭证验证

**使用场景：** 用户提供一条VC-JWT字符串（以`eyJ...`开头）并希望知道其是否有效。

**步骤：**

1. `bind_parse_credential` — 解码JWT以检查声明内容
2. `bind_verify_credential` — 验证签名和有效期
3. `bind_hash_credential` — 计算SHA-256哈希值
4. `bind_check_revocation` — 发送哈希值（不发送凭证本身）以检查撤销状态

步骤1和2可以合并（验证包含解析），但先进行解析可以让用户在完整验证之前了解凭证的内容。步骤1-3在本地执行；步骤4仅将哈希值发送到API。

**重要提示：** `bind_verify_credential`不检查撤销状态。您必须始终结合哈希值和撤销检查来进行完整验证。

```
parse → verify → hash → check_revocation
```

## 工作流程2：查询发行机构

**使用场景：** 用户想要了解某个组织的密钥或策略信息。

1. `bindResolveIssuer-orgId)` — 获取他们的JWKS
2. `bind_list_policies` 或 `bind_explain_policy` — 查找他们的策略

## 工作流程3：创建策略

**使用场景：** 用户想要定义一个新的验证策略。

**步骤：**

1. `bind_whoami` — 检查组织名称、层级和限制。**您需要组织名称来设置命名空间。**
2. 构建策略规范（详见下面的策略规范参考）
3. `bind_validate_policy` | 预运行验证以捕获错误 |
4. 修复所有验证错误并重新验证 |
5. `bind_create_policy` | 保存策略 |
6. `bind_generate_circuit` | 提交ZK电路编译请求 |
7. `bind_get_circuit_status` | 查询电路编译任务的状态，直到状态变为`completed`或`failed`

**关键规则：**
- `metadata.namespace`必须以您组织的缩写名称开头（来自`bind_whoami`）。`bind`和`system`是保留的命名空间。
- 策略`id`必须以命名空间开头（例如，`acme.finance.creditCheck`表示命名空间`acme`）。
- 在创建之前必须进行验证。先修复所有错误。
- 字符串输入必须包含`encoding`块，将值映射为数字（ZK电路仅支持数字）。

## 工作流程4：生成证明并颁发凭证

**使用场景：** 用户想要生成ZK证明并获得可验证的凭证。

1. `bind_list_policies` 或 `bind_explain_policy` — 查找合适的策略/电路 |
2. `bind_submit_prove_job(circuitId, inputs)` — 提交证明任务 |
3. `bind_get_prove_job(jobId)` | 查询证明任务的状态，直到状态变为`completed` |
4. `bind_issue_credential(proveJobId)` — 根据完成的证明颁发凭证 |
5. （可选）：`bind_share_proof(proveJobId, verifierOrgId)` — 与验证组织共享证明 |

## 策略规范参考

策略是一个具有以下结构的JSON对象。除非标记为可选，否则所有字段都是必需的。

```json
{
  "id": "<namespace>.<category>.<name>",
  "version": "0.1.0",
  "metadata": {
    "title": "Human-readable title",
    "description": "What this policy verifies",
    "category": "finance|mobility|identity|demo",
    "namespace": "your-org-name"
  },
  "subject": {
    "type": "individual|organization|vehicle|device",
    "identifier": "wallet_address|did|vin|vehicleTokenId"
  },

  "inputs": [
    {
      "id": "input_name",
      "source": { "kind": "static|api", "api": "optional_api_name" },
      "signal": "input_name",
      "valueType": "number|boolean|string",
      "unit": "USD|count|months",
      "time": { "mode": "point|range|relative", "lookback": "30d" },
      "aggregation": { "op": "latest|sum|mean|count" },
      "encoding": {
        "type": "enum",
        "values": { "label1": 1, "label2": 2 }
      }
    }
  ],

  "rules": [
    {
      "id": "rule_name",
      "description": "Human-readable description",
      "assert": { /* expression — see below */ },
      "severity": "fail|warn|info"
    }
  ],

  "evaluation": {
    "kind": "PASS_FAIL|SCORE",
    "scoreRange": { "min": 0, "max": 100 },
    "baseline": 50,
    "contributions": [
      { "ruleId": "rule_name", "points": 30, "whenPasses": true }
    ]
  },

  "outputs": [
    {
      "name": "output_name",
      "type": "boolean|enum|number",
      "derive": {
        "kind": "PASS_FAIL|SCORE|BAND|CONST",
        "from": "SCORE|input_id",
        "bands": [
          { "label": "LOW", "minInclusive": 0, "maxExclusive": 40 },
          { "label": "HIGH", "minInclusive": 40, "maxExclusive": 101 }
        ],
        "value": 42
      },
      "disclosed": true
    }
  ],

  "validity": { "ttl": "P30D" },
  "disclosure": {
    "default": "SELECTIVE",
    "exposeClaims": ["output_name"]
  },

  "proving": {
    "circuitId": "<namespace>.<name>.v<version>",
    "inputTypes": { "input_name": "u32" },
    "outputType": "u8"
  }
}
```

### 表达式类型（用于`rules[].assert`）

| 类型 | 形式 | 示例 |
|------|-------|---------|
| `ref` | `{ "type": "ref", "inputId": "<input_id>" }` | 引用输入值 |
| `const` | `{ "type": "const", "value": <number\|boolean> }` | 字面数字或布尔值（不能是字符串） |
| `cmp` | `{ "type": "cmp", "cmp": ">=\|<=\|>\|<\|==\|!=", "left": <expr>, "right": <expr> }` | 比较操作 |
| `op` | `{ "type": "op", "op": "+\|-\|*\|/", "args": [<expr>, ...] }` | 算术运算 |
| `and` | `{ "type": "and", "args": [<expr>, ...] }` | 逻辑AND |
| `or` | `{ "type": "or", "args": [<expr>, ...] }` | 逻辑OR |
| `not` | `{ "type": "not", "arg": <expr> }` | 逻辑NOT |

**字段名称注意事项：**
- 在引用表达式中使用`"inputId"`，而不是`"path"` |
- 使用`"cmp"`作为比较运算符，而不是`"operator"` |
- 使用`"args`作为操作数列表，而不是`"children"` |
- 使用`"arg`（单数形式）表示`not`操作，而不是`"expr"` |
- `const`值必须是数字或布尔值，不能是字符串

### 评估类型

**PASS_FAIL：** 所有`severity: "fail"`类型的规则都必须通过。不进行评分。

**SCORE：** 从`baseline`开始，根据规则贡献值增加/减少`points`。

```json
{
  "kind": "SCORE",
  "scoreRange": { "min": 0, "max": 100 },
  "baseline": 50,
  "contributions": [
    { "ruleId": "has_high_income", "points": 25, "whenPasses": true },
    { "ruleId": "has_delinquencies", "points": -20, "whenPasses": true }
  ]
}
```

### 输出类型

| 类型 | 用途 | 必需字段 |
|------|---------|----------------|
| `PASS_FAIL` | 评估后的布尔结果（通过/失败） | 无 |
| `SCORE` | 原始数值分数 | `from: "SCORE"` |
| `BAND` | 将分数映射到相应的等级 | `from: "SCORE", `bands`数组 |
| `CONST` | 固定值 | `value` |

### 处理字符串输入

ZK电路仅支持数字输入。当策略使用字符串输入（如雇主名称、国家代码等）时，必须包含`encoding`块：

```json
{
  "id": "employer",
  "source": { "kind": "static" },
  "signal": "employer",
  "valueType": "string",
  "encoding": {
    "type": "enum",
    "values": {
      "Acme Corp": 1,
      "Globex Inc": 2,
      "Initech": 3
    }
  }
}
```

### 证明部分

`proving`部分将输入映射到ZK电路的Noir类型：

```json
{
  "proving": {
    "circuitId": "acme.safe_driver.v0_1_0",
    "inputTypes": {
      "miles_driven": "u32",
      "hard_brake_pct": "u8",
      "is_commercial": "bool"
    },
    "outputType": "u8"
  }
}
```

可用的Noir类型：`u8`, `u16`, `u32`, `u64`, `i8`, `i16`, `i32`, `i64`, `bool`, `Field`

---

## 权限层级

策略制定受组织层级的限制。在使用之前，请务必先调用`bind_whoami`来检查权限限制。

| 层级 | 是否可以创建策略 | 备注 |
|------|-------------------|-------|
| Basic | 否 | 仅支持验证 |
| Premium | 是 | 输入/规则/输出有限 |
| Scale | 是 | 权限更广泛，可以创建提取器 |
| Enterprise | 是 | 无限制 |
| Verifier | 否 | 无法创建证明或策略 |

## 常见错误及解决方法

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `NAMESPACE_MISMATCH` | 策略命名空间与您的组织不符 | 使用`bind_whoami`中获取的组织名称作为命名空间前缀 |
| `TIER_LIMIT_EXCEEDED` | 您的层级不允许此操作 | 查看`bind_whoami`中的限制 |
| `INVALID_EXPRESSION` | 规则表达式格式错误 | 检查表达式字段名称（`inputId`, `cmp`, `args`, `arg`） |
| `MISSING_encoding` | 字符串输入缺少编码信息 | 添加`encoding.type: "enum"`并指定值映射 |
| `CIRCUIT_COMPILATION_FAILED` | 电路编译失败 | 查看`bind_get_circuit_status`中的错误，修复策略后重新生成 |

## 示例：创建信用评分策略

以下是为您的组织`acme`创建信用评分策略的完整示例：

```json
{
  "id": "acme.finance.credit-check",
  "version": "0.1.0",
  "metadata": {
    "title": "Credit Eligibility Check",
    "description": "Evaluates creditworthiness based on income and debt ratio",
    "category": "finance",
    "namespace": "acme"
  },
  "subject": {
    "type": "individual",
    "identifier": "wallet_address"
  },
  "inputs": [
    {
      "id": "annual_income",
      "source": { "kind": "static" },
      "signal": "annual_income",
      "valueType": "number",
      "unit": "USD"
    },
    {
      "id": "debt_ratio",
      "source": { "kind": "static" },
      "signal": "debt_ratio",
      "valueType": "number",
      "unit": "percent"
    }
  ],
  "rules": [
    {
      "id": "min_income",
      "description": "Annual income must be at least $30,000",
      "assert": {
        "type": "cmp",
        "cmp": ">=",
        "left": { "type": "ref", "inputId": "annual_income" },
        "right": { "type": "const", "value": 30000 }
      },
      "severity": "fail"
    },
    {
      "id": "max_debt_ratio",
      "description": "Debt-to-income ratio must be under 40%",
      "assert": {
        "type": "cmp",
        "cmp": "<",
        "left": { "type": "ref", "inputId": "debt_ratio" },
        "right": { "type": "const", "value": 40 }
      },
      "severity": "fail"
    }
  ],
  "evaluation": {
    "kind": "PASS_FAIL"
  },
  "outputs": [
    {
      "name": "eligible",
      "type": "boolean",
      "derive": { "kind": "PASS_FAIL" },
      "disclosed": true
    }
  ],
  "validity": { "ttl": "P30D" },
  "disclosure": {
    "default": "SELECTIVE",
    "exposeClaims": ["eligible"]
  },
  "proving": {
    "circuitId": "acme.credit_check.v0_1_0",
    "inputTypes": {
      "annual_income": "u32",
      "debt_ratio": "u8"
    },
    "outputType": "u8"
  }
}
```

代理的工作流程如下：
1. `bind_whoami` — 确认组织是`acme`且层级允许创建策略 |
2. `bind_validate_policy(policy)` | 预运行验证 |
3. `bind_create_policy(policy)` | 创建策略 |
4. `bind_generate_circuit("acme.finance.credit-check")` | 编译电路 |
5. `bind_get_circuit_status(jobId)` | 查询编译状态，直到完成