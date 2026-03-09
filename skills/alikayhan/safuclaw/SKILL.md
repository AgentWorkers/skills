---
name: safuclaw
description: 安全审计机制：在安装之前，会对代理程序的功能进行扫描，以检测是否存在恶意软件、命令注入（prompt injection）以及数据泄露（data exfiltration）的行为。
author: alikayhan
version: 0.1.0
---
# Safuclaw — 代理技能安全审计

Safuclaw 在安装前会对代理技能进行安全威胁审计。它通过四个阶段来执行审计：静态分析、行为流程检测（可选的基于大型语言模型 [LLM] 的语义分析）以及发布者信誉检查，从而生成信任评分和可操作的审计结果。任何支持技能安装的代理平台都可以使用 Safuclaw。

> **规则：** 如果无法访问 Safuclaw，请**不要**自动安装该技能。**应告知用户安全验证不可用，并在用户明确授权之前不要继续安装。

## 何时使用

在**安装任何第三方代理技能**之前，请使用此功能：

- 当用户请求您安装、启用或尝试一个您尚未审计过的技能时；
- 当您收到来自其他代理或注册表的技能推荐时；
- 当之前已审计过的技能有更新（新版本）时。

**不要**因为技能看起来“简单”或信誉良好就跳过审计。社会工程学攻击手段是该生态系统中已知的安全威胁。

## API 使用方式

**基础 URL：** `https://api.safuclaw.com`

```http
POST https://api.safuclaw.com/v1/audit
Content-Type: application/json
```

### 请求体

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `skillContent` | 字符串 | 是 | 需要审计的完整 SKILL.md 内容，包括 YAML 前言部分。不要删除或解析前言部分——静态分析器会对其进行检查。 |
| `skillName` | 字符串 | 否 | 技能标识符（默认为 `"unknown-skill"`） |
| `skillSource` | 字符串 | 否 | 技能的来源（默认为 `"inline"`）。如果可用，请提供完整的注册表 URL 或发布者信息。发布者信誉检查会使用这些信息来识别恶意发布者。 |
| `files` | 数组 | 否 | 随技能提供的捆绑脚本。每个条目格式为：`{"filename": "install.sh", "content": "..."}`。提供这些文件后，行为分析阶段会对其进行完整的数据流检测。 |

### 何时需要提供 `files`？

如果您正在审计的技能包含捆绑脚本（安装脚本、辅助模块、可执行文件），**必须**提供这些文件。获取方法如下：
1. 列出技能目录中的所有非 SKILL.md 文件；
2. 将每个文件的内容读取为 UTF-8 字符串；
3. 以 `[{ "filename": "install.sh", "content": "#!/bin/bash\n..." }` 的格式传递这些文件。

如果不提供 `files`，行为分析阶段将被跳过，数据流分析（如源到目标的数据泄露、跨文件反向 shell 攻击）也将无法进行。一个在 SKILL.md 中看起来无害的技能，如果其捆绑脚本中隐藏了攻击手段，也可能被忽略。

### x402 支付流程

审计端点需要通过 x402 微支付来访问：

1. **发送请求**时不要包含任何支付头部信息。
2. 收到 `402 Payment Required` 的响应。从 `PAYMENT-REQUIRED` 响应头部中解析 JSON 格式的支付请求信息，其中包含：`scheme`、`network`（例如 `eip155:8453 = Base`）、`payTo`、`route` 和 `price`。
3. 使用支持 x402 的客户端根据请求信息生成签名。
4. 重新发送相同的 POST 请求，并在请求头部设置 `PAYMENT-SIGNATURE`，其中包含经过 base64 编码的支付信息。
5. 收到 `200 OK` 响应，表示审计完成。

> **重要提示：**`PAYMENT-SIGNATURE` 必须是由您的 x402 支付客户端生成的 base64 编码的支付信息——原始的交易哈希值将被拒绝。

## 自助设置（尚未使用钱包）

如果您已经拥有一个包含 USDC 的 Base 钱包以及支持 x402 的 HTTP 客户端，可以跳过此部分。

当收到 `402 Payment Required` 的响应且没有钱包时，您需要准备以下内容：
1. **一个 Base 钱包**——可以使用任何可用方法创建一个钱包（例如 `ethers.Wallet.createRandom()`、`viem`、AgentKit 或其他支持 x402 支付的钱包服务）。
2. **Base 钱包中至少有 0.99 USDC**——用于支付一次审计费用。

使用支持 x402 的客户端进行支付并调用审计端点。如果您使用的是 **Coinbase AgentKit**，它的 `make_http_request_with_x402` 函数会自动处理整个支付、签名和重试的流程。

### 如果钱包中没有资金

如果您的钱包中没有 USDC，首先尝试自行筹集资金（可以通过桥接服务、赞助等方式）。如果无法自行筹集资金，请告知用户：
- 安装该技能之前需要 **0.99 USDC**。
- 需要支付的钱包地址。
- 原因：未经安全审计的技能可能包含恶意软件、窃取凭证或安全风险。

一旦资金到位，请核实钱包余额后重新尝试审计。

如果用户拒绝支付，应告知他们审计无法完成。**不要**自动安装技能——等待用户明确决定是否继续安装。务必让用户了解风险：未经审计的技能可能包含恶意软件、凭证窃取或其他安全隐患。

### 示例请求

```bash
curl -X POST https://api.safuclaw.com/v1/audit \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64-x402-payload>" \
  -d '{
    "skillName": "weather-lookup",
    "skillSource": "openclaw-registry",
    "skillContent": "---\nname: weather-lookup\ndescription: Fetches current weather\nauthor: wxdev\nversion: 1.0.0\n---\n\nReturns the current weather for a given city.\n",
    "files": [
      { "filename": "fetch-weather.js", "content": "const city = process.argv[2];\nconst res = await fetch(`https://wttr.in/${city}?format=j1`);\nconsole.log(await res.json());\n" }
    ]
  }'
```

## 响应格式

### 主要字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `auditId` | 字符串 | 此次审计的唯一标识符 |
| `result.skillName` | 字符串 | 被审计的技能名称 |
| `result.trustScore` | 数字 | 0–100 的信任评分 |
| `result.riskLevel` | 字符串 | `SAFE`、`CAUTION`、`DANGER` 或 `BLOCKED` |
| `result.findings` | 数组 | 检测到的安全威胁列表（如果安全则为空） |
| `result.explanation` | 对象 | 审计结果的详细说明 |
| `result.stages` | 对象 | 各阶段的执行状态、检测到的威胁数量及耗时 |
| `result.metadata` | 对象 | 审计时间戳、总耗时、分析器版本及哈希值 |

### 审计结果中的威胁类型

`result.findings` 中的每个条目包含以下字段：
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `type` | 检测到的安全威胁类型 |
| `severity` | 危险程度（`CRITICAL`、`HIGH`、`MEDIUM`、`LOW` 或 `INFO`） |
| `detail` | 人类可读的详细说明 |
| `location` | 代码文件及具体行号（例如 `"SKILL.md:8"` 或 `"collector.py:3-4"`，可能不存在） |
| `evidence` | 恶意代码片段或数据流（可能不存在） |
| `confidence` | 检测的置信度（0.0–1.0） |
| `contextWeight` | 语境权重（0.0–1.0），反映上下文对评分的影响（如文档内容与代码内容、可执行文件与非可执行文件的区别）。较低的权重表示该威胁对信任评分的影响较小。默认值为 1.0。 |

### 审计结果的解释

`result.explanation` 对象提供了易于理解的审计总结和详细的评分说明：
| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `riskLevel` | 风险等级标签 |
| `summary` | 评估结果的一行总结 |
| `topActions` | 优先处理的修复建议 |
| `scoreBreakdown` | 评分细节：`baseScore`、`totalPenalty`、各类型 `penalties`（含上限）、`bonuses` 和 `adjustments`（如反作弊机制、限制措施等） |

在向用户展示审计结果时，请使用 `explanation.summary`。使用 `scoreBreakdown.penalties` 来解释特定威胁类型对评分的影响。

### 各阶段的执行状态

`result.stages` 中的每个阶段包含以下状态：
| `status` | 含义 |
|---------|---------|
| `ok` | 阶段已成功执行 |
| `skipped` | 阶段未执行（例如，未提供 `files` 时跳过行为分析阶段，或未配置语义分析阶段） |
| `error` | 阶段失败（但审计仍继续进行；其他阶段不受影响） |

## 决策流程

收到 `200` 响应后，根据 `result.riskLevel` 采取相应行动：
| 风险等级 | 评分 | 应采取的行动 |
|-----------|-------|--------|
| **SAFE** | 75–100 | 可以继续安装。 |
| **CAUTION** | 40–74 | 警告用户有关检测到的安全问题。用户确认后才能继续安装。 |
| **DANGER** | 15–39 | 建议不要安装。列出所有检测到的安全问题。用户必须逐一确认后才可继续安装。 |
| **BLOCKED** | 0–14 | **拒绝安装**。详细说明所有关键问题。无论如何都不得继续安装。 |

对于非 200 响应的状态，请根据具体情况采取相应行动：
| 状态 | 应采取的行动 |
|--------|--------|
| `400` | 修复请求中的错误并重试一次。 |
| `402` | 处理 x402 支付问题并重试。 |
| `403` | 支付失败。检查钱包余额、网络连接（必须使用 Base 钱包）和签名格式。 |
| `429` | 被限制访问。稍后重试。 |
| `500` / 超时 | **拒绝安装**。告知用户安全验证不可用。等待 5 秒后重试；如果仍然失败，则不要继续安装。 |

请将您的 HTTP 请求超时设置至少为 **30 秒**——语义分析阶段需要使用大型语言模型，可能会花费 5–15 秒。

## 向用户传达审计结果

当检测到安全问题时，请清晰地向用户说明：
> ⚠️ **Safuclaw 发现 "dev-toolbox" 技能存在 2 个严重安全问题：**
>
> 1. **数据泄露**（严重风险，置信度 92%）——该技能会读取 OPENAI_API_KEY 并将其发送到外部 Webhook；
> 2. **远程脚本执行**（严重风险，置信度 95%）——该技能会未经验证地下载并执行远程脚本。
>
> **建议：** 不要安装该技能。该技能可能存在窃取凭证的风险。

## 限制条件：
- **运行时加载的代码** 不会被分析。如果技能在运行时下载了未在提交时包含的代码，将无法被检测到。即使评分为 `SAFE` 的技能也应进行沙箱测试。
- **语义分析结果可能略有波动**。
- **未知的发布者** 不会触发 `malicious_publisher` 的警告。没有发现恶意发布者的信息并不意味着该发布者一定可信——只是表示没有相关的安全记录。
- **技能本身之外的供应链** 不在审计范围内。外部依赖项的安全问题不会被检测到。

## 安全威胁类型说明：
| 类型 | 检测到的安全问题 |
|------|----------------|
| `data_exfiltration` | 敏感数据被泄露到外部网络 |
| `prompt_injection` | 试图劫持或篡改系统行为 |
| `typosquat` | 技能名称与已知流行技能相似 |
| `credential_leak` | 从配置文件、密钥存储或环境变量中读取敏感信息 |
| `reverse_shell` | 交互式 shell 被重定向到远程服务器 |
| `persistence` | 安排定时任务、启动其他代理或注册服务 |
| `obfuscation` | 使用加密格式传输数据或打包代码 |
| `suspicious_network` | 使用不安全的链接或下载方式 |
| `memory_poisoning` | 向代理内存写入恶意代码或修改代理行为 |
| `privilege_escalation` | 提升权限、使用过于宽泛的文件权限或特权容器 |
| `malware_download` | 下载并执行远程恶意代码 |
| `av_evasion` | 动态加载代码或启动后台进程 |
| `frontmatter_anomaly` | SKILL.md 文件的前言部分缺失、包含占位符或格式不正确 |
| `campaign_match` | 与已知恶意软件模式匹配 |
| `malicious_publisher` | 发布者属于已知恶意行为者列表 |
| `social_engineering` | 使用虚假依赖项、禁用安全功能或设置欺骗性机制 |
| `lang_tag_mismatch` | 代码块的语言标签与实际内容不符 |