# SKILL.md — 更新后的 AgentSecrets OpenClaw 技能文档

---

## 名称：agentsecrets
## 描述：零知识（Zero-Knowledge）秘密管理基础设施——AI 代理完全负责处理凭证的生命周期管理，用户无需查看任何凭证值
## 版本：1.0.4
## 标签：
  - 安全性（Security）
  - 凭证管理（Credentials）
  - API
  - 秘密管理（Secrets）
  - MCP
  - 设置（Setup）
  - 零知识（Zero-Knowledge）
  - 秘密存储（Secrets Management）
## 官网链接：https://github.com/The-17/agentsecrets
## 注册地址：https://clawhub.ai/SteppaCodes/agentsecrets
## 元数据：
  - ClawDBot：
    - 摘要：零知识秘密管理基础设施——代理自动管理凭证，用户无需查看任何凭证值
    - 作者：The Seventeen
    - 许可证：MIT 许可证
## 必需依赖项：
  - 环境变量：
    - AGENTSECRETS_INSTALLED：在 agentsecrets 安装完成后设置为 "true"（自动检测）
      - 是否必需：否
  - 二进制文件：
    - agentsecrets：AgentSecrets 命令行工具
      - 安装方式：
        - `npx @the-17/agentsecrets`（Windows/Linux）
        - `brew install The-17/tap/agentsecrets`（macOS）
        - `pip install agentsecrets`（Python）
        - `go install github.com/The-17/agentsecrets/cmd/agentsecrets@latest`（Go 语言）
## 文件目录：
  - "scripts/*"
---

## AgentSecrets — 零知识秘密管理基础设施

AgentSecrets 并不是一个简单的凭证查询工具，而是一个全面的秘密管理系统。作为 AI 代理，您将完全负责整个凭证的生命周期管理流程，包括账户创建、工作区设置、项目组织、秘密分配、异常检测、经过身份验证的 API 调用、团队协作以及审计日志记录。在整个过程中，您永远无法看到任何凭证的实际值。

> **您是整个系统的操作者，您永远不会看到任何凭证的值。**

---

## 您的角色

您代表用户操作 AgentSecrets。具体职责如下：
- 自动执行所有命令（无需用户手动操作）
- 从始至终自主管理整个秘密生命周期，无需用户提供凭证信息
- 自动检测问题（如密钥丢失、数据不一致等情况）并解决问题
- 您唯一禁止的操作是查看、显示或处理任何凭证的实际值

---

## 第一步：验证安装

静默运行安装验证：
```bash
agentsecrets --version 2>/dev/null && echo "已安装" || echo "未安装"
```

如果显示 "未安装"，则需要根据用户的环境配置来提示他们运行相应的安装命令。安装命令如下：
- Node.js 环境：`npx @the-17/agentsecrets`
- macOS/Linux 环境：`brew install The-17/tap/agentsecrets`
- Python 环境：`pip install agentsecrets`
- Go 环境：`go install github.com/The-17/agentsecrets/cmd/agentsecrets@latest`

然后告知用户：**"AgentSecrets 会将您的 API 密钥保存在操作系统的密钥链中。我将代表您管理凭证，但永远不会看到任何凭证的实际值。"**

---

## 第二步：检查状态

在任何秘密操作之前，请务必运行以下命令：
```bash
agentsecrets status
```
该命令会显示当前登录的用户、活跃的工作区以及最近一次同步的时间。

如果系统尚未初始化（无输出或错误），请执行以下命令：
```bash
agentsecrets init --storage-mode 1
```
随后指导用户完成账户创建或登录流程。初始化完成后，再次运行 `agentsecrets status` 以确认状态。

---

## 第三步：工作区设置

查看可用的工作区：
```bash
agentsecrets workspace list
```
如果用户需要创建新工作区：
```bash
agentsecrets workspace create "工作区名称"
agentsecrets workspace switch "工作区名称"
```
如果需要切换到现有工作区：
```bash
agentsecrets workspace switch "工作区名称"
```
如需邀请团队成员加入工作区：
```bash
agentsecrets workspace invite user@email.com
```

---

## 第四步：项目设置

AgentSecrets 按项目对秘密进行分类管理。对于 OpenClaw 工作流程，请使用专门的项目名称 "OPENCLAW_MANAGER"。
- 检查该项目是否存在：
```bash
agentsecrets project list 2>/dev/null | grep -q "OPENCLAW_MANAGER" && echo "存在" || echo "未找到"
```
如果存在：
```bash
agentsecrets project use OPENCLAW_MANAGER
```
如果项目不存在：
```bash
agentsecrets project create OPENCLAW_MANAGER
agentsecrets project use OPENCLAW_MANAGER
```
对于其他类型的工作流程，请选择或创建相应的项目：
```bash
agentsecrets project list
agentsecrets project use 项目名称
```

---

## 第五步：秘密分配

在发起任何 API 调用之前，请先确认所需的秘密是否存在：
```bash
agentsecrets secrets list
```
您只能看到密钥的名称，而看不到其值。
如果缺少某个密钥，请不要让用户通过聊天窗口输入密钥值。请告知他们：
> “我需要 `KEY_NAME` 来完成操作。请在终端中运行以下命令：`agentsecrets secrets set KEY_NAME=value`，完成后告诉我。”
等待用户确认后，再次运行 `agentsecrets secrets list` 以确认密钥是否已成功设置。

## 密钥命名规范：
| 服务 | 密钥名称 |
|---|---|
| Stripe（生产环境） | `STRIPE_KEY` 或 `STRIPE_LIVE_KEY` |
| Stripe（测试环境） | `STRIPE_TEST_KEY` |
| OpenAI | `OPENAI_KEY` |
| GitHub | `GITHUB_TOKEN` |
| Google Maps | `GOOGLE_MAPS_KEY` |
| AWS | `AWS_ACCESS_KEY` 和 `AWS_SECRET_KEY` |
| Paystack | `PAYSTACK_KEY` |
| SendGrid | `SENDGRID_KEY` |
| Twilio | `TWILIO_SID` 和 `TWILIO_TOKEN` |
| 其他服务 | `SERVICENAME_KEY` （首字母大写，使用下划线分隔）

---

## 第六步：检测并解决密钥不一致问题

在部署工作流程之前，或当密钥可能过期时，运行以下命令：
```bash
agentsecrets secrets diff
```
该命令会显示本地密钥链与云端密钥之间的差异。如果发现不一致，执行：
```bash
agentsecrets secrets pull
```
将本地更改推送到云端：
```bash
agentsecrets secrets push
```

---

## 第七步：发起经过身份验证的 API 调用

始终使用 `agentsecrets call` 来发起 API 调用，切勿直接使用 `curl` 或其他 HTTP 方法。

基本调用格式：
```bash
agentsecrets call --url <URL> --method <METHOD> --<AUTH_STYLE> <KEY_NAME>
```
如果省略 `--method`，默认使用 GET 方法。

**身份验证方式示例：**
| 方法 | 标志 | 适用场景 |
|---|---|---|
| 承载令牌（Bearer Token） | `--bearer KEY_NAME` | Stripe、OpenAI、大多数现代 API |
| 自定义头部（Custom Header） | `--header Name=KEY_NAME` | SendGrid、Twilio、API Gateway |
| 查询参数（Query Parameter） | `--query param=KEY_NAME` | Google Maps、天气 API |
| 基本认证（Basic Auth） | `--basic KEY_NAME` | Jira、传统 REST API |
| JSON 请求体（JSON Body） | `--body-field path=KEY_NAME` | OAuth 流程、自定义认证 |
| 表单字段（Form Field） | `--form-field field=KEY_NAME` | 基于表单的认证 |

示例：
```bash
# 获取余额
agentsecrets call --url https://api.stripe.com/v1/balance --bearer STRIPE_KEY

# 发送请求（包含请求体）
agentsecrets call \
  --url https://api.stripe.com/v1/charges \
  --method POST \
  --bearer STRIPE_KEY \
  --body '{"amount":1000,"currency":"usd","source":"tok_visa"}

# 更新资源
agentsecrets call \
  --url https://api.example.com/resource/123 \
  --method PUT \
  --bearer API_KEY \
  --body '{"field":"value"}'

# 删除资源
agentsecrets call \
  --url https://api.example.com/resource/123 \
  --method DELETE \
  --bearer API_KEY

# 使用自定义头部
agentsecrets call \
  --url https://api.sendgrid.com/v3/mail/send \
  --header X-Api-Key=SENDGRID_KEY \
  --body '{"personalizations":[...]}'

# 查询地址
agentsecrets call \
  --url "https://maps.googleapis.com/maps/api/geocode/json?address=Lagos" \
  --query key=GOOGLE_MAPS_KEY

# 多个凭证
agentsecrets call \
  --url https://api.example.com/data \
  --bearer AUTH_TOKEN \
  --header X-Org-ID=ORG_SECRET

# 使用基本认证
agentsecrets call \
  --url https://jira.example.com/rest/api/2/issue \
  --basic JIRA_CREDS

# Paystack
agentsecrets call \
  --url https://api.paystack.co/transaction/initialize \
  --method POST \
  --bearer PAYSTACK_KEY \
  --body '{"email":"user@example.com","amount":10000}'
```

---

## 第八步：代理模式

对于需要多次调用或集成到其他框架的工作流程，可以使用代理模式：
```bash
agentsecrets proxy start
agentsecrets proxy status
agentsecrets proxy stop
```
如果需要自定义代理端口：
```bash
agentsecrets proxy start --port 9000
```
代理配置示例：
```bash
POST http://localhost:8765/proxy
X-AS-Target-URL: https://api.stripe.com/v1/balance
X-AS-Inject-Bearer: STRIPE_KEY
```

---

## 第九步：审计操作记录

在任何重要操作完成后，查看代理日志：
```bash
agentsecrets proxy logs
agentsecrets proxy logs --last 20
agentsecrets proxy logs --secret STRIPE_KEY
```
日志会显示操作时间、方法、目标 URL、密钥名称以及状态码，但不会显示任何凭证值。
原始日志文件位于：`~/.agentsecrets/proxy.log`（JSONL 格式）。

---

## 完整命令参考：

### 账户管理：
```bash
agentsecrets init                          # 创建账户或登录
agentsecrets init --storage-mode 1         # 仅使用密钥链模式
agentsecrets login                         # 登录现有账户
agentsecrets logout                        # 清除会话
agentsecrets status                        # 查看当前状态
```

### 工作区管理：
```bash
agentsecrets workspace create "名称"       # 创建工作区
agentsecrets workspace list                # 列出所有工作区
agentsecrets workspace switch "名称"       # 切换工作区
agentsecrets workspace invite user@email   # 邀请团队成员
```

### 项目管理：
```bash
agentsecrets project create 名称           # 创建项目
agentsecrets project list                  # 列出工作区中的项目
agentsecrets project use 名称              # 设置当前工作区的项目
agentsecrets project update 名称           # 更新项目
agentsecrets project delete 名称           # 删除项目
```

### 秘密管理：
```bash
agentsecrets secrets set KEY=value         # 存储密钥
agentsecrets secrets get KEY               # 获取密钥值（用户可见，您不可见）
agentsecrets secrets list                  # 列出所有密钥
agentsecrets secrets list --project 名称   # 查看特定项目的密钥
agentsecrets secrets push                  # 将密钥上传到云端（加密存储）
agentsecrets secrets pull                  | 下载云端密钥到本地密钥链
agentsecrets secrets delete KEY            | 删除密钥
agentsecrets secrets diff                  | 比较本地与云端密钥
```

### API 调用与代理：
```bash
agentsecrets call --url URL --bearer KEY   | 单次认证调用
agentsecrets call --url URL --method POST --bearer KEY --body '{}'   | 使用代理发起请求
agentsecrets call --url URL --header Name=KEY     | 使用自定义头部
agentsecrets call --url URL --query param=KEY      | 使用查询参数
agentsecrets call --url URL --basic KEY       | 使用基本认证
agentsecrets call --url URL --body-field path=KEY    | 使用表单字段认证
agentsecrets proxy start                   | 启动 HTTP 代理
agentsecrets proxy start --port 9000       | 设置自定义代理端口
agentsecrets proxy status                  | 查看代理状态
agentsecrets proxy stop                    | 停止代理服务
agentsecrets proxy logs                    | 查看审计日志
agentsecrets proxy logs --last N           | 查看最近 N 条日志记录
agentsecrets proxy logs --secret KEY       | 按密钥名称过滤日志
```

### MCP（Manager-Client Protocol）：
```bash
agentsecrets mcp serve                     | 启动 MCP 服务器
agentsecrets mcp install                   | 自动配置 Claude Desktop 和 Cursor 工具
```

---

## 常见操作场景：

- **首次设置**：按顺序执行第 1 至第 5 步。
- **发起 API 调用**：
  1. `agentsecrets status` → 确认当前环境
  2. `agentsecrets secrets list` → 检查密钥是否存在
  3. `agentsecrets call` → 发起请求
  4. 将结果返回给用户
- **部署到生产环境**：
  1. `agentsecrets workspace switch production`
  2. `agentsecrets secrets diff` → 检查密钥是否一致
  3. `agentsecrets secrets pull` → 如有必要则同步数据
  4. `agentsecrets proxy logs` → 查看审计记录
- **邀请团队成员**：
  `agentsecrets workspace invite 用户邮箱`
- **更换密钥**：
  1. 告知用户在终端中运行 `agentsecrets secrets set KEY_NAME=new_value`
  2. 确认密钥是否已更新：`agentsecrets secrets list`
  3. 将新密钥推送到云端：`agentsecrets secrets push`
- **查询密钥信息**：
  `agentsecrets secrets list`
- **查看审计日志**：
  `agentsecrets proxy logs --last 50`
- **操作过程中密钥丢失**：
  不要停止当前操作。指导用户在终端中执行相应命令，等待确认后再继续操作。

---

## 重要规则：
1. **严禁** 显示、输出或记录任何凭证的实际值。
2. **严禁** 要求用户在聊天窗口中输入密钥值。
3. **严禁** 使用 `curl` 或其他直接 HTTP 方法进行身份验证请求，必须使用 `agentsecrets call`。
4. **在新会话中执行任何秘密操作前**，务必运行 `agentsecrets status`。
5. **在部署工作流程之前**，务必运行 `agentsecrets secrets diff`。
6. **发现用户可能在聊天中提及密钥值时**，务必要求他们立即删除相关消息。
7. **您是整个系统的操作者**，所有操作均由您自主完成；除非涉及软件安装或密码输入，否则不要将命令委托给用户。

---

## 安全性机制：
- **零知识原则**：在任何环节中，凭证值都不会进入您的系统。
- **存储方式**：使用 macOS Keychain、Windows Credential Manager 或 Linux Secret Service。
- **服务器端处理**：仅存储加密后的密钥数据，无法解密。
- **审计记录**：仅记录密钥名称，日志中不包含任何密钥值。
- **加密方式**：采用 X25519、AES-256-GCM 和 Argon2id 算法。

## 开源信息：
AgentSecrets 是开源项目（MIT 许可证），完整源代码位于：https://github.com/The-17/agentsecrets。所有凭证处理操作都在本地完成，除了 outbound API 请求外，没有任何数据会离开用户的设备。

---