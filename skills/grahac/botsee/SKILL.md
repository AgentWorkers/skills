---
name: botsee
description: 通过 BotSee API 监控您品牌在人工智能领域的可见度
version: 0.2.2
---
# BotSee 技能

该技能用于监控您的品牌在 ChatGPT、Claude、Perplexity 和 Gemini 中的 AI 可见度（AI SEO/GEO 数据）。该工具由 botsee.io 提供，适用于 Claude Code 和相关代理。

**命令：**

**工作流程：**
- /botsee                  - 获取快速状态和帮助
- /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY] - 使用信用卡注册
- /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email] - 使用 USDC 在 Base 平台上注册
- /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF] - 通过 x402 方式支付 USDC 注册费用
- /botsee signup-status [--token TOKEN]    - 检查注册是否完成并保存 API 密钥
- /botsee topup-usdc --amount-cents N [--payment PROOF] - 使用 USDC 在 Base 平台上充值
- /botsee create-site <domain> [--types N]   - 保存自定义配置
- /botsee config-show              - 显示保存的配置
- /botsee analyze              - 运行竞争分析
- /botsee content              - 根据分析结果生成博客文章

**站点相关命令：**
- /botsee list-sites             - 列出所有站点
- /botsee get-site [uuid]        - 查看站点详情
- /botsee create-site <domain>       - 创建新站点
- /botsee archive-site [uuid]        - 存档站点

**客户类型相关命令：**
- /botsee list-types             - 列出客户类型
- /botsee get-type [uuid]          - 查看类型详情
- /botsee create-type <name> [desc]       - 创建客户类型
- /botsee generate-types [count]       - 生成客户类型
- /botsee update-type [uuid] [name] [desc]     - 更新客户类型
- /botsee archive-type [uuid]        - 存档客户类型

**人物角色相关命令：**
- /botsee list-personas [type]         - 列出人物角色（全部或按类型）
- /botsee get-persona [uuid]          - 查看人物角色详情
- /botsee create-persona <type> [name] [desc]       - 创建人物角色
- /botsee generate-personas [type] [count]       - 为类型生成人物角色
- /botsee update-persona [uuid] [name] [desc]       - 更新人物角色
- /botsee archive-persona [uuid]        - 存档人物角色

**问题相关命令：**
- /botsee list-questions [persona]       - 列出问题（全部或按人物角色）
- /botsee get-question [uuid]          - 查看问题详情
- /botsee create-question [persona] [question_text]    - 创建问题
- /botsee generate-questions [persona] [count]       - 为人物角色生成问题
- /botsee update-question [uuid] [question_text]     - 更新问题内容
- /botsee delete-question [uuid]          - 删除问题

**结果相关命令：**
- /botsee results-competitors [analysis_uuid]   - 查看竞争对手结果
- /botsee results-keywords [analysis_uuid]    - 查看关键词结果
- /botsee results-sources [analysis_uuid]    - 查看来源信息
- /botsee results-responses [analysis_uuid]   - 查看所有 AI 回答

## 实现方式

当用户发起 BotSee 命令时，会运行相应的 Python 脚本。所有命令都使用同一个脚本来处理内部的 API 调用。

### /botsee (status)

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py status
```

### /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY]

**新用户注册流程（使用信用卡）：**

**步骤 1：获取注册链接**
```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py signup
```

系统会显示一个注册链接。告知用户：“请访问此链接完成注册并获取您的 API 密钥，然后在此处粘贴您的 API 密钥。”

**步骤 2：用户粘贴 API 密钥**

当用户提供 API 密钥时（例如：“我的 API 密钥是：bts_live_abc123”），提取并保存该密钥：

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py signup --api-key <extracted-key>
```

**重要提示：** 当用户粘贴 API 密钥时，代理的行为如下：**
- 自动运行 `signup --api-key <key>` 以保存密钥。
- 向用户确认：“✅ API 密钥已保存！现在您可以运行 /botsee create-site <domain>”。
- **请勿** 要求用户手动运行注册命令。

### /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email]

**使用 USDC 注册的流程（基于 x402 协议）：**

**步骤 1：在调用 API 之前询问用户**

当用户未指定注册方式时，询问用户：
> “您是否希望将电子邮件与此账户关联？
> - **是（需要电子邮件）** —— 您将收到一个设置链接来验证电子邮件并稍后访问控制面板。
> - **否（仅使用 API）** —— 直接进行支付。

**步骤 2a：处理电子邮件验证**

调用：
```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-usdc
```
（如果未使用 `--no-email` 标志）

响应中会包含一个 `setup_url`。告知用户：
> “请访问此链接来验证您的电子邮件并阅读设置说明：
> `<setup_url from response>`
>
> 完成验证后，请返回此处，我们将完成 USDC 支付。

**步骤 2b：处理无需电子邮件验证的情况**

直接进行支付操作。

**步骤 3：支付**

无论用户是否进行了电子邮件验证，都会执行以下支付流程：
```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-pay-usdc --amount-cents 250
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-status
```

**x402 支付流程细节：**
1. `signup-usdc` 通过 `POST /api/v1/signup/usdc` 创建一个 USDC 注册令牌。
2. `signup-pay-usdc --amount-cents N` 通过 `POST /api/v1/signup/:token/pay-usdc` 发起支付请求（无需提供支付头部信息），服务器会返回 402 错误代码，提示支付相关信息（网络信息、金额、`payTo` 地址）。
3. 使用钱包（如 Pinch 或 Coinbase CDP Agentic Wallet）将 USDC 支付到指定的地址。
4. 重新尝试支付，提供支付证明：`signup-pay-usdc --amount-cents N --payment <proof>`。
5. `signup-status` 会持续检查支付状态直至完成，并保存 API 密钥。

### /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF]

```bash
# Step 1: Get 402 challenge (no --payment → returns payment requirements)
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-pay-usdc --amount-cents 250

# Step 2: Retry with proof after wallet pays
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-pay-usdc --amount-cents 250 --payment <proof>
```

如果省略 `--payment` 参数，系统会返回一个包含支付信息的 402 错误。
在钱包完成支付后，再次尝试支付时需要提供 `--payment <base64-proof>` 参数。

### /botsee signup-status [--token TOKEN]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py signup-status
```

注册完成后，API 密钥会自动保存到 `~/.botsee/config.json` 文件中。

### /botsee topup-usdc --amount-cents N [--payment PROOF]

```bash
# Step 1: Get 402 challenge (no --payment → returns payment requirements)
python3 ~/.claude/skills/botsee/scripts/botsee.py topup-usdc --amount-cents 5000

# Step 2: Retry with proof after wallet pays
python3 ~/.claude/skills/botsee/scripts/botsee.py topup-usdc --amount-cents 5000 --payment <proof>
```

如果省略 `--payment` 参数，系统会返回一个包含支付信息的 402 错误。
在钱包完成支付后，再次尝试支付时需要提供 `--payment <base64-proof>` 参数。

### /botsee create-site <domain> [--types N] [--personas P] [--questions Q]

**使用说明：** 需要 `/botsee signup` 命令提供的 API 密钥。

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-site <domain>
```

**可选参数：**
- `--types`（默认值：2，范围：1-3）
- `--personas`（默认值：2，范围：1-3）
- `--questions`（默认值：5，范围：3-10）

**操作流程：**
1. 为指定域名创建站点。
2. 生成客户类型、人物角色和问题。
3. 将配置保存到工作区和用户配置文件中。

**自定义生成数量：**
```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-site <domain> --types 3 --personas 2 --questions 10
```

### /botsee config-show

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py config-show
```

### /botsee analyze

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py analyze
```

开始分析，等待分析完成，然后显示竞争对手信息、关键词和来源数据。

### /botsee content

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py content
```

根据最新分析结果生成博客文章，并自动保存到 `botsee-YYYYMMDD-HHMMSS.md` 文件中。

---

## 站点相关命令

### /botsee list-sites

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py list-sites
```

### /botsee get-site [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py get-site [uuid]
```

如果未提供 `uuid`，系统会使用 `~/.botsee/config.json` 中的默认站点信息。

### /botsee create-site <domain>

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-site <domain>
```

### /botsee archive-site [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py archive-site [uuid]
```

---

## 客户类型相关命令

### /botsee list-types

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py list-types
```

### /botsee get-type [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py get-type <uuid>
```

### /botsee create-type <name> [description]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-type "Enterprise Buyers" "Large companies seeking solutions"
```

### /botsee generate-types [count]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py generate-types 3
```

如果未指定 `count`，默认值为 2。

### /botsee update-type [uuid] [name] [description]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py update-type <uuid> --name "New Name" --description "New description"
```

### /botsee archive-type [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py archive-type <uuid>
```

---

## 人物角色相关命令

### /botsee list-personas [type_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py list-personas
python3 ~/.claude/skills/botsee/scripts/botsee.py list-personas <type_uuid>
```

### /botsee get-persona [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py get-persona <uuid>
```

### /botsee create-persona <type_uuid> [name] [description]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-persona <type_uuid> "Sarah Chen" "VP of Marketing at mid-sized SaaS company"
```

### /botsee generate-personas [type_uuid] [count]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py generate-personas <type_uuid> 3
```

如果未指定 `count`，默认值为 2。

### /botsee update-persona [uuid] [name] [description]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py update-persona <uuid> --name "New Name" --description "New description"
```

### /botsee archive-persona [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py archive-persona <uuid>
```

---

## 问题相关命令

### /botsee list-questions [persona_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py list-questions
python3 ~/.claude/skills/botsee/scripts/botsee.py list-questions <persona_uuid>
```

### /botsee get-question [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py get-question <uuid>
```

### /botsee create-question [persona_uuid] [question_text]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py create-question <persona_uuid> "What are the best email marketing tools?"
```

### /botsee generate-questions [persona_uuid] [count]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py generate-questions <persona_uuid> 5
```

如果未指定 `count`，默认值为 5。

### /botsee update-question [uuid] [question_text]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py update-question <uuid> "What are the best affordable email marketing tools?"
```

### /botsee delete-question [uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py delete-question <uuid>
```

---

## 结果相关命令

### /botsee results-competitors [analysis_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py results-competitors <analysis_uuid>
```

### /botsee results-keywords [analysis_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py results-keywords <analysis_uuid>
```

### /botsee results-sources [analysis_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py results-sources <analysis_uuid>
```

### /botsee results-responses [analysis_uuid]

```bash
python3 ~/.claude/skills/botsee/scripts/botsee.py results-responses <analysis_uuid>
```

**获取分析结果 UUID：**

运行 `/botsee analyze` 时，系统会显示分析结果的 UUID：
```
📊 Analysis started: abc-def-123
```
请复制该 UUID，并使用它来查看详细的分析数据。

---

## 代理使用说明

该技能专为 **非交互式代理** 设计。所有命令都通过命令行参数传递参数，无需用户输入。

### 代理使用时的关键注意事项：

**1. 注册流程需要人工干预**

对于没有 API 密钥的新用户，注册命令会生成一个注册令牌并显示一个注册链接。代理应：
- 如果有 API 密钥，请使用 `--api-key` 参数。
- 告知用户需要注册（代理无法完成注册操作）。
- 确保 API 密钥是代理自主运行的前提条件。

**2. 异步操作和等待**

部分命令需要等待结果（例如 `/botsee signup-status` 和 `/botsee analyze`），这些操作可能会阻塞直到完成或超时。

**3. 分析结果**

要查看分析结果，请执行 `/botsee analyze` 并获取分析结果的 UUID，然后使用该 UUID 来查看详细数据。

**推荐使用流程：**
```bash
# Run analysis
output=$(/botsee analyze)
# Extract UUID (line containing "Analysis started:")
uuid=$(echo "$output" | grep "Analysis started:" | awk '{print $NF}')
# View results
/botsee results-competitors "$uuid"
```

**4. 配置文件**

系统使用两个配置文件：
- **用户配置文件：`~/.botsee/config.json`（包含 API 密钥和站点 UUID）。
- **工作区配置文件：`.context/botsee-config.json`（包含生成配置的默认值，可选）。

代理可以通过以下命令查看状态：
- `/botsee`：显示账户状态。
- `/botsee config-show`：显示工作区配置。

**5. 费用**

所有消耗信用点的操作都会显示剩余信用量。代理应：
- 在执行高成本操作前检查信用量（例如 `/botsee` 命令）。
- 优雅地处理“信用不足”的错误。
- 监控信用使用情况（每次操作后都会显示信用量信息）。

**费用：**
- 注册：约 75 信用点（默认配置：2 个类型、2 个人角色、5 个问题）。
- 分析：每次运行约 660 信用点。
- 生成内容：15 信用点。

**6. 错误处理**

所有错误都会以代码 1 退出，并输出到标准错误流（stderr）。错误信息包括：
- 相关的 HTTP 状态码。
- 下一步的操作建议。
- 确保 API 密钥不会泄露。

**7. 幂等性**
- **状态查询、列表和获取操作** 是安全的（只读操作）。
- **创建操作** 不具有幂等性（可能会创建重复条目）。
- **更新操作** 需要特定的 UUID，可以安全地重新尝试。

**8. 输出格式**
- **CRUD 操作**：输出为 JSON 格式，便于解析。
- **工作流程相关命令**：以人类可读的格式输出结果。
- **状态/信用量**：在操作完成后始终显示。

### 代理使用示例流程

```bash
# 1. Check status (discover state)
/botsee

# 2. Save API key if provided by user
/botsee signup --api-key bts_live_abc123

# 3. Create a site
/botsee create-site https://example.com

# 4. Run analysis (captures UUID)
analysis_output=$(/botsee analyze)
uuid=$(echo "$analysis_output" | grep -oP '(?<=Analysis started: )\S+')

# 5. View results
/botsee results-competitors "$uuid"

# 6. Generate content
/botsee content

# 7. Check final balance
/botsee
```