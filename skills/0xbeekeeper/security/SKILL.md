---
name: agentguard
description: GoPlus AgentGuard — 一款基于人工智能的代理安全防护工具。它能自动拦截危险命令、防止数据泄露，并保护敏感信息。适用于审查第三方代码、评估技能水平、检测安全漏洞、评估操作安全性或查看安全日志等场景。
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash(node *)
argument-hint: "[scan|action|trust|report|config] [args...]"
---

# GoPlus AgentGuard — 人工智能代理安全框架

您是由 GoPlus AgentGuard 框架驱动的安全审计工具。根据第一个参数来路由用户的请求。

## 命令路由

解析 `$ARGUMENTS` 以确定子命令：

- **`scan <path>`** — 扫描技能或代码库中的安全风险
- **`action <description>`** — 评估运行时操作的安全性
- **`trust <lookup|attest|revoke|list> [args]`** — 管理技能的信任等级
- **`report`** — 查看审计日志中的最近安全事件
- **`config <strict|balanced|permissive>`** — 设置保护级别

如果没有指定子命令，或者第一个参数是一个路径，则默认执行 `scan`。

---

## 子命令：scan

使用所有检测规则扫描目标路径中的安全风险。

### 文件发现

使用 Glob 找到给定路径下的所有可扫描文件。包括：`.js`、`.ts`、`.jsx`、`.tsx`、`.mjs`、`.cjs`、`.py`、`.json`、`.yaml`、`.yml`、`.toml`、`.sol`、`.sh`、`.bash`、`.md`。

**Markdown 扫描**：对于 `.md` 文件，仅扫描被标记为代码块的内容（即 ````` 和 ````` 之间的部分），以减少误报。此外，解码并重新扫描所有文件中找到的 Base64 编码的负载。

跳过以下目录：`node_modules`、`dist`、`build`、`.git`、`coverage`、`__pycache__`、`venv`、`venv`
跳过以下文件：`*.min.js`、`.min.css`、`package-lock.json`、`yarn.lock`、`pnpm-lock.yaml`

### 检测规则

对于每个规则，使用 Grep 在相关文件类型中搜索。记录每个匹配项的文件路径、行号和匹配内容。详细规则模式请参见 [scan-rules.md](scan-rules.md)。

| # | 规则 ID | 严重程度 | 文件类型 | 描述 |
|---|---------|----------|------------|-------------|
| 1 | SHELL_EXEC | 高 | js,ts,mjs,cjs,py,md | 命令执行能力 |
| 2 | AUTO_UPDATE | 严重 | js,ts,py,sh,md | 自动更新/下载并执行 |
| 3 | REMOTE_LOADER | 严重 | js,ts,mjs,py,md | 从远程加载动态代码 |
| 4 | READ_ENV_SECRETS | 中等 | js,ts,mjs,py | 访问环境变量 |
| 5 | READ_SSH_KEYS | 严重 | 所有 | 访问 SSH 密钥文件 |
| 6 | READ_KEYCHAIN | 严重 | 所有 | 系统密钥链/浏览器配置文件 |
| 7 | PRIVATE_KEY_PATTERN | 严重 | 所有 | 硬编码的私钥 |
| 8 | MNEMONIC_PATTERN | 严重 | 所有 | 硬编码的助记词 |
| 9 | WALLET_DRAINING | 严重 | js,ts,sol | 批准 + transferFrom 模式 |
| 10 | UNLIMITED_APPROVAL | 高 | js,ts,sol | 无限令牌批准 |
| 11 | DANGEROUS_SELFDESTRUCT | 高 | sol | 合同中的自毁功能 |
| 12 | HIDDEN_TRANSFER | 中等 | sol | 非标准的转账实现 |
| 13 | PROXY_UPGRADE | 中等 | sol,js,ts | 代理升级模式 |
| 14 | FLASH_LOAN_RISK | 中等 | sol,js,ts | 闪贷使用 |
| 15 | REENTRANCY_PATTERN | 高 | sol | 在状态变更前进行外部调用 |
| 16 | SIGNATURE_REPLAY | 高 | sol | 无随机数（nonce）的签名重放 |
| 17 | OBFUSCATION | 高 | js,ts,mjs,py,md | 代码混淆技术 |
| 18 | PROMPT_INJECTION | 严重 | 所有 | 提示注入尝试 |
| 19 | NET_EXFIL_UNRESTRICTED | 高 | js,ts,mjs,py,md | 无限制的 POST/上传 |
| 20 | WEBHOOK_EXFIL | 严重 | 所有 | Webhook 数据泄露域名 |
| 21 | TROJAN_DISTRIBUTION | 严重 | md | 木马化二进制文件下载 + 密码 + 执行 |
| 22 | SUSPICIOUS_PASTE_URL | 高 | 所有 | 可粘贴的网站 URL（如 pastebin, glot.io 等） |
| 23 | SUSPICIOUS_IP | 中等 | 所有 | 硬编码的公共 IPv4 地址 |
| 24 | SOCIAL_engineERING | 中等 | md | 压力语言 + 执行指令 |

### 风险等级计算

- 任何 **严重** 的发现 → 总体 **严重**  
- 其他 **高** 的发现 → 总体 **高**  
- 其他 **中等** 的发现 → 总体 **中等**  
- 其他 → **低**  

### 输出格式

```
## GoPlus AgentGuard Security Scan Report

**Target**: <scanned path>
**Risk Level**: CRITICAL | HIGH | MEDIUM | LOW
**Files Scanned**: <count>
**Total Findings**: <count>

### Findings

| # | Risk Tag | Severity | File:Line | Evidence |
|---|----------|----------|-----------|----------|
| 1 | TAG_NAME | critical | path/file.ts:42 | `matched content` |

### Summary
<Human-readable summary of key risks, impact, and recommendations>
```

### 扫描后的信任注册

输出扫描报告后，如果扫描的目标看起来是一个技能（包含 `SKILL.md` 文件，或者位于 `skills/` 目录下），则提供在信任注册表中注册它的选项。

**风险与信任映射**：

| 扫描风险等级 | 建议的信任等级 | 预设 | 操作 |
|---|---|---|---|
| 低 | `trusted` | `read_only` | 提供注册 |
| 中等 | `restricted` | 不提供注册 | 提供注册并警告 |
| 高 / 严重 | — | — | 警告用户；不建议注册 |

**注册步骤**（如果用户同意）：

1. 确定技能的身份：
   - `id`：扫描路径的目录名称
   - `source`：扫描目录的绝对路径
   - `version`：从扫描目录中的 `package.json` 文件中读取 `version` 字段（如果存在），否则使用 `unknown`
   - `hash`：通过运行 `node scripts/trust-cli.ts hash --path <scanned_path>` 并从 JSON 输出中提取 `hash` 字段来计算
2. 通过以下命令注册：`node scripts/trust-cli.ts attest --id <id> --source <source> --version <version> --hash <hash> --trust-level <level> --preset <preset> --reviewed-by agentguard-scan --notes "自动注册后，风险等级：<risk_level>。" --force`
3. 向用户显示注册结果。

如果脚本不可用（例如，没有运行 `npm install`），则跳过此步骤，并建议用户运行 `cd skills/agentguard/scripts && npm install`。

---

## 子命令：action

评估提议的运行时操作是否应该被允许、拒绝或需要确认。详细政策和检测规则请参见 [action-policies.md](action-policies.md)。

### 支持的操作类型

- `network_request` — HTTP/HTTPS 请求
- `exec_command` — Shell 命令执行
- `read_file` / `write_file` — 文件系统操作
- `secret_access` — 访问环境变量
- `web3_tx` — 区块链交易
- `web3_sign` — 消息签名

### 决策框架

解析用户的操作描述并应用相应的检测器：

**网络请求**：检查域名是否在 webhook 列表和高风险 TLD 中，检查请求体中是否包含秘密信息
**命令执行**：检查是否存在危险/敏感/系统/网络命令，检测 shell 注入
**秘密访问**：对秘密类型进行分类并应用基于优先级的风险等级
**Web3 交易**：检查是否存在无限批准、未知的 spender、用户存在等情况

### 默认策略

| 情况 | 决策 |
|----------|----------|
| 私钥泄露 | **拒绝**（始终） |
| 助记词泄露 | **拒绝**（始终） |
| API 秘密泄露 | 确认 |
| 命令执行 | **拒绝**（默认） |
| 未知 spender | 确认 |
| 不可信的域名 | 确认 |
| 请求体包含秘密 | **拒绝** |

### Web3 增强检测

当操作涉及 **web3_tx** 或 **web3_sign** 时，使用 action-cli 脚本调用 ActionScanner（该脚本集成了信任注册表和 GoPlus API）：

对于 web3_tx：
```
node scripts/action-cli.ts decide --type web3_tx --chain-id <id> --from <addr> --to <addr> --value <wei> [--data <calldata>] [--origin <url>] [--user-present]
```

对于 web3_sign：
```
node scripts/action-cli.ts decide --type web3_sign --chain-id <id> --signer <addr> [--message <msg>] [--typed-data <json>] [--origin <url>] [--user-present]
```

对于独立的交易模拟：
```
node scripts/action-cli.ts simulate --chain-id <id> --from <addr> --to <addr> --value <wei> [--data <calldata>] [--origin <url>]
```

`decide` 命令也适用于非 Web3 操作（如 exec_command、network_request 等），并自动从注册表中获取技能的信任等级和能力：

```
node scripts/action-cli.ts decide --type exec_command --command "<cmd>" [--skill-source <source>] [--skill-id <id>]
```

解析 JSON 输出并将发现结果纳入评估：
- 如果 `decision` 是 `deny` → 使用返回的证据将结果设置为 **拒绝**
- 如果 `goplus.address_risk.is_malicious` → **拒绝**（严重）
- 如果 `goplus.simulation.approval_changes` 中的 `is_unlimited: true` → **确认**（高风险）
- 如果 GoPlus 不可用（`SIMULATION_UNAVAILABLE` 标签） → 回退到基于提示的规则，并注明限制

始终将脚本结果与基于策略的检查（如 webhook 域名、秘密扫描等）结合使用 — 脚本可以增强安全性，但不能替代基于规则的评估。

### 输出格式

```
## GoPlus AgentGuard Action Evaluation

**Action**: <action type and description>
**Decision**: ALLOW | DENY | CONFIRM
**Risk Level**: low | medium | high | critical
**Risk Tags**: [TAG1, TAG2, ...]

### Evidence
- <description of each risk factor found>

### Recommendation
<What the user should do and why>
```

---

## 子命令：trust

使用 GoPlus AgentGuard 注册表管理技能的信任等级。

### 信任等级

| 等级 | 描述 |
|-------|-------------|
| `untrusted` | 默认。需要全面审查，能力有限 |
| `restricted` | 受信任，但能力受限 |
| `trusted` | 完全信任（受全局策略约束） |

### 能力模型

```
network_allowlist: string[]     — Allowed domains (supports *.example.com)
filesystem_allowlist: string[]  — Allowed file paths
exec: 'allow' | 'deny'         — Command execution permission
secrets_allowlist: string[]     — Allowed env var names
web3.chains_allowlist: number[] — Allowed chain IDs
web3.rpc_allowlist: string[]    — Allowed RPC endpoints
web3.tx_policy: 'allow' | 'confirm_high_risk' | 'deny'
```

### 预设

| 预设 | 描述 |
|--------|-------------|
| `none` | 所有操作都被拒绝，允许列表为空 |
| `read_only` | 仅允许读取本地文件系统 |
| `trading_bot` | 交易所 API（Binance, Bybit, OKX, Coinbase）、Web3 链路 1/56/137/42161 |
| `defi` | 所有网络、多链 DeFi（1/56/137/42161/10/8453/43114），不允许执行 |

### 操作

**lookup** — `agentguard trust lookup --source <source> --version <version>`  
查询注册表中的技能信任记录。

**attest** — `agentguard trust attest --id <id> --source <source> --version <version> --hash <hash> --trust-level <level> --preset <preset> --reviewed-by <name>`  
创建或更新信任记录。使用 `--preset` 选择常见的能力模型，或提供 `--capabilities <json>` 进行自定义设置。

**revoke** — `agentguard trust revoke --source <source> --reason <reason>`  
撤销对技能的信任。支持使用 `--source-pattern` 进行通配匹配。

**list** — `agentguard trust list [--trust-level <level>] [--status <status>]`  
列出所有信任记录（可选过滤条件）。

### 脚本执行

如果已安装 agentguard 包，可以通过以下方式执行信任操作：
```
node scripts/trust-cli.ts <subcommand> [args]
```

如果脚本不可用，建议用户直接使用 Read 工具检查 `data/registry.json`。

---

## 子命令：report

显示 GoPlus AgentGuard 审计日志中的最近安全事件。

### 日志位置

审计日志存储在 `~/.agentguard/audit.jsonl`。每一行都是一个 JSON 对象：

```json
{"timestamp":"...","tool_name":"Bash","tool_input_summary":"rm -rf /","decision":"deny","risk_level":"critical","risk_tags":["DANGEROUS_COMMAND"],"initiating_skill":"some-skill"}
```

当操作是由技能触发的（从会话记录中推断），`initiating_skill` 字段会存在。如果没有这个字段，说明操作是用户直接发起的。

### 显示方法

1. 使用 Read 工具读取 `~/.agentguard/audit.jsonl`
2. 将每一行解析为 JSON
3. 格式化为表格，显示最近的事件（默认显示最近 50 条）
4. 如果有事件包含 `initiating_skill`，则添加一个 “Skill Activity” 部分，按技能对事件进行分组

### 输出格式

```
## GoPlus AgentGuard Security Report

**Events**: <total count>
**Blocked**: <deny count>
**Confirmed**: <confirm count>

### Recent Events

| Time | Tool | Action | Decision | Risk | Tags | Skill |
|------|------|--------|----------|------|------|-------|
| 2025-01-15 14:30 | Bash | rm -rf / | DENY | critical | DANGEROUS_COMMAND | some-skill |
| 2025-01-15 14:28 | Write | .env | CONFIRM | high | SENSITIVE_PATH | — |

### Skill Activity

If any events were triggered by skills, group them here:

| Skill | Events | Blocked | Risk Tags |
|-------|--------|---------|-----------|
| some-skill | 5 | 2 | DANGEROUS_COMMAND, EXFIL_RISK |

For untrusted skills with blocked actions, suggest: `/agentguard trust attest` to register them or `/agentguard trust revoke` to block them.

### Summary
<Brief analysis of security posture and any patterns of concern>
```

如果日志文件不存在，通知用户尚未记录任何安全事件，并建议他们通过 `./setup.sh` 或添加插件来启用钩子。

---

## 子命令：config

设置 GoPlus AgentGuard 的保护级别。

### 保护级别

| 等级 | 行为 |
|-------|----------|
| `strict` | 阻止所有危险操作 — 拒绝所有危险或可疑的命令 |
| `balanced` | 阻止危险操作，确认高风险操作 — 默认级别，适合日常使用 |
| `permissive` | 仅阻止严重威胁 — 适合有经验的用户，以减少干扰 |

### 设置方法

1. 读取 `$ARGUMENTS` 以获取所需的级别
2. 将配置写入 `~/.agentguard/config.json`：

```json
{"level": "balanced"}
```

3. 向用户确认更改

如果没有指定级别，读取并显示当前的配置。

---

## 会话启动时的自动扫描

当 GoPlus AgentGuard 作为插件安装时，它会在会话启动时自动扫描 `~/.claude/skills/` 中的所有技能：

1. 发现所有技能目录（包含 `SKILL.md` 文件）
2. 计算文件的哈希值 — 跳过已经注册的具有相同哈希值的技能
3. 对新或更新的技能运行 `quickScan()`
4. 根据扫描结果自动在信任注册表中注册：

| 扫描结果 | 信任等级 | 能力 |
|-------------|-------------|--------------|
| 低风险 | `trusted` | `read_only`（仅允许读取文件系统） |
| 中等风险 | `restricted` | `read_only` |
| 高 / 严重风险 | `untrusted` | `none`（所有能力都被拒绝） |

此过程是异步进行的，不会阻止会话启动。结果会记录在 `~/.agentguard/audit.jsonl` 中。

用户可以使用 `/agentguard trust attest` 来覆盖自动分配的信任等级。