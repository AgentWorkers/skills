# SKILL.md — 更新后的 AgentSecrets OpenClaw 技能

---

## 名称：agentsecrets
## 描述：零知识（Zero-Knowledge）秘密管理基础设施 — AI 代理负责整个凭证生命周期的管理，用户无需查看凭证的实际值
## 版本：1.1.0
## 标签：
  - 安全（Security）
  - 凭证（Credentials）
  - API（API）
  - 秘密（Secrets）
  - MCP（MCP）
  - 设置（Setup）
  - 零知识（Zero-Knowledge）
  - 秘密管理（Secrets Management）
## 主页：https://github.com/The-17/agentsecrets
## 注册库：https://clawhub.ai/SteppaCodes/agentsecrets
## 元数据：
  ```
  clawdbot:
    摘要：零知识秘密管理基础设施 — 代理自动管理凭证，用户无需查看凭证的实际值
    作者：The Seventeen
    许可证：MIT
## 必需依赖：
  ```
  **环境变量（Environment Variables）**：
    - 名称：AGENTSECRETS_INSTALLED
      描述：在 agentsecrets 安装完成后设置为 "true"（自动检测）
      是否必需：否
  **二进制文件（Binaries）**：
    - 名称：agentsecrets
      描述：AgentSecrets 命令行工具二进制文件
      安装方式：
        - `npx @the-17/agentsecrets` （无需安装即可运行）
        - `brew install The-17/tap/agentsecrets` （macOS/Linux）
        - `pip install agentsecrets` （Python/通用版本）
        - `go install github.com/The-17/agentsecrets/cmd/agentsecrets@latest` （Go 开发者）
  ```
## 文件（Files）：
  - "scripts/*"
---

## AgentSecrets — 零知识秘密管理基础设施

AgentSecrets 并不是一个简单的凭证查询工具，而是一个完整的秘密管理系统。作为 AI 代理，您将负责整个凭证生命周期的管理，包括账户设置、工作区创建、项目组织、秘密分配、异常检测、经过身份验证的 API 调用、团队管理以及审计日志记录。在整个过程中，您永远无法看到任何凭证的实际值。

> **您是操作者。您永远不会看到凭证的实际值。**

---

## 您的角色

您代表用户操作 AgentSecrets。这意味着：
- 您可以自主运行命令（无需用户协助）
- 您无需用户提供凭证信息即可完成整个秘密管理流程
- 您可以自动检测问题（如密钥丢失、数据不一致等情况并解决问题）
- 您唯一不能做的事情就是查看、显示或处理凭证的实际值

---

## 第一步：验证安装

静默运行以下命令以检查是否已安装：
```bash
agentsecrets --version 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```

如果显示 "NOT_INSTALLED"，则需要根据用户的环境配置来提示他们运行相应的安装命令。用户需要自己控制安装哪些二进制文件：

```bash
which npx   # 是否安装了 Node.js
which brew  # 是否安装了 Homebrew
which pip   # 是否安装了 Python
which go    # 是否安装了 Go
```

根据不同的环境，安装命令如下：
- Node.js：`npx @the-17/agentsecrets`
- Homebrew：`brew install The-17/tap/agentsecrets`
- Python：`pip install agentsecrets`
- Go：`go install github.com/The-17/agentsecrets/cmd/agentsecrets@latest`

然后告知用户：`AgentSecrets 会将您的 API 密钥保存在操作系统的密钥链中。我将代表您管理凭证，但永远不会看到凭证的实际值。`

---

## 第二步：检查状态

在任何秘密操作之前，请始终运行以下命令：
```bash
agentsecrets status
```

该命令会显示当前登录的用户、活跃的工作区以及最后同步的时间。

如果系统尚未初始化（没有输出或出现错误），请运行：
```bash
agentsecrets init --storage-mode 1
```

随后指导用户完成账户创建或登录操作。初始化完成后，再次运行：
```bash
agentsecrets status
```

---

## 第三步：工作区设置

查看可用的工作区：
```bash
agentsecrets workspace list
```

如果用户需要创建新的工作区：
```bash
agentsecrets workspace create "工作区名称"
agentsecrets workspace switch "工作区名称"
```

如果需要切换到现有的工作区：
```bash
agentsecrets workspace switch "工作区名称"
```

根据用户需求，可以邀请团队成员加入工作区：
```bash
agentsecrets workspace invite user@email.com
```

---

## 第四步：项目设置

AgentSecrets 按项目对秘密进行分类管理。对于 OpenClaw 工作流程，请使用专门的 `OPENCLAW_MANAGER` 项目。

检查该项目是否存在：
```bash
agentsecrets project list 2>/dev/null | grep -q "OPENCLAW_MANAGER" && echo "存在" || echo "未找到"
```

如果项目存在：
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

在进行任何 API 调用之前，请先检查所需的秘密是否存在：
```bash
agentsecrets secrets list
```

您只能看到密钥的名称，而看不到实际值。

如果缺少所需的密钥，请不要让用户将密钥值输入聊天框。请告知他们：
> “我需要 `密钥名称` 来完成操作。请在终端中运行：`agentsecrets secrets set 密钥名称=值`，完成后告诉我，然后我将继续操作。”

等待用户确认后，再次检查：
```bash
agentsecrets secrets list
```

**密钥命名规范：**
| 服务 | 密钥名称 |
|---|---|
| Stripe（实时）| `STRIPE_KEY` 或 `STRIPE_LIVE_KEY` |
| Stripe（测试）| `STRIPE_TEST_KEY` |
| OpenAI | `OPENAI_KEY` |
| GitHub | `GITHUB_TOKEN` |
| Google Maps | `GOOGLE_MAPS_KEY` |
| AWS | `AWS_ACCESS_KEY` 和 `AWS_SECRET_KEY` |
| Paystack | `PAYSTACK_KEY` |
| SendGrid | `SENDGRID_KEY` |
| Twilio | `TWILIO_SID` 和 `TWILIO_TOKEN` |
| 其他服务 | `服务名称_KEY` （首字母大写，使用下划线分隔）

---

## 第六步：检测并解决数据不一致问题

在部署工作流程之前，或者当秘密可能过时时，运行以下命令：
```bash
agentsecrets secrets diff
```

该命令会显示本地密钥链与云端密钥之间的不一致之处。如果发现不一致：
```bash
agentsecrets secrets pull
```

要将本地更改推送到云端：
```bash
agentsecrets secrets push
```

---

## 第七步：进行经过身份验证的 API 调用

始终使用 `agentsecrets call` 进行 API 调用，切勿直接使用 `curl` 或其他非代理方式。

**基本调用格式：**
```bash
agentsecrets call --url <URL> --method <方法> --<认证方式> <密钥名称>
```

如果省略了 `--method`，默认使用 `GET` 方法。

**常见的认证方式：**
| 方式 | 标志 | 适用场景 |
|---|---|---|
| 承载令牌（Bearer Token）| `--bearer 密钥名称` | Stripe、OpenAI、大多数现代 API |
| 自定义头部（Custom Header）| `--header 名称=密钥名称` | SendGrid、Twilio、API Gateway |
| 查询参数（Query Parameter）| `--query param=密钥名称` | Google Maps、天气 API |
| 基本认证（Basic Auth）| `--basic 密钥名称` | Jira、传统 REST API |
| JSON 标记（JSON Body）| `--body-field 路径=密钥名称` | OAuth 流程、自定义认证 |
| 表单字段（Form Field）| `--form-field 字段=密钥名称` | 基于表单的认证 |

**示例：**
```bash
# 获取请求
agentsecrets call --url https://api.stripe.com/v1/balance --bearer STRIPE_KEY

# 带参数的 POST 请求
agentsecrets call \
  --url https://api.stripe.com/v1/charges \
  --method POST \
  --bearer STRIPE_KEY \
  --body '{"amount":1000,"currency":"usd","source":"tok_visa"}'

# PUT 请求
agentsecrets call \
  --url https://api.example.com/resource/123 \
  --method PUT \
  --bearer API_KEY \
  --body '{"field":"value"}'

# 删除请求
agentsecrets call \
  --url https://api.example.com/resource/123 \
  --method DELETE \
  --bearer API_KEY

# 自定义头部
agentsecrets call \
  --url https://api.sendgrid.com/v3/mail/send \
  --method POST \
  --header X-Api-Key=SENDGRID_KEY \
  --body '{"personalizations":[...]}'

# 查询参数
agentsecrets call \
  --url "https://maps.googleapis.com/maps/api/geocode/json?address=Lagos" \
  --query key=GOOGLE_MAPS_KEY

# 多个凭证
agentsecrets call \
  --url https://api.example.com/data \
  --bearer AUTH_TOKEN \
  --header X-Org-ID=ORG_SECRET

# 基本认证
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

对于需要多次调用或集成到其他框架的工作流程，可以使用以下命令：
```bash
agentsecrets proxy start
agentsecrets proxy status
agentsecrets proxy stop
```

**自定义端口：**
```bash
agentsecrets proxy start --port 9000
```

**HTTP 代理示例：**
```bash
POST http://localhost:8765/proxy
X-AS-Target-URL: https://api.stripe.com/v1/balance
X-AS-Inject-Bearer: STRIPE_KEY
```

---

## 第九步：审计操作记录

在任何重要操作之后，运行以下命令查看审计日志：
```bash
agentsecrets proxy logs
agentsecrets proxy logs --last 20
agentsecrets proxy logs --secret STRIPE_KEY
```

日志会显示时间戳、方法、目标 URL、密钥名称、状态码、执行时长以及日志是否已被屏蔽（如显示为 `(REDACTED)`）。日志中显示的 `(REDACTED)` 表示 AgentSecrets 检测到 API 返回了原始凭证值，并在响应到达您之前自动将其替换为 `[REDACTED_BY_AGENTSECRETS]`。这是预期的安全行为。

**原始日志文件位置：`~/.agentsecrets/proxy.log`（JSONL 格式）`

---

## 第十步：环境变量注入

当某些工具需要将秘密作为环境变量使用时（例如 Stripe CLI、Node.js、开发服务器、SDK 等），请使用以下命令：
```bash
agentsecrets env -- stripe mcp
agentsecrets env -- node server.js
agentsecrets env -- npm run dev
```

这些命令会从当前项目的密钥链中提取秘密，并将其作为环境变量注入到子进程中。这些变量仅存在于子进程的内存中，不会被写入磁盘。

**使用场景：**
- 用户需要运行从环境变量中读取凭证的 CLI 工具
- 需要为原生 MCP 服务器（如 Stripe MCP）提供凭证支持
- 用户请求将凭证注入到应用程序中

---

## 完整命令参考

### 账户管理（Account Management）
```bash
agentsecrets init                          # 创建账户或登录
agentsecrets init --storage-mode 1         # 仅使用密钥链的模式
agentsecrets login                         # 登录到现有账户
agentsecrets logout                        # 清除会话
agentsecrets status                        # 查看当前上下文
```

### 工作区管理（Workspace Management）
```bash
agentsecrets workspace create "名称"       # 创建工作区
agentsecrets workspace list                # 列出所有工作区
agentsecrets workspace switch "名称"       # 切换活跃工作区
agentsecrets workspace invite user@email   # 邀请团队成员加入工作区
```

### 项目管理（Project Management）
```bash
agentsecrets project create 名称           # 创建项目
agentsecrets project list                  # 列出工作区中的项目
agentsecrets project use 名称              # 设置当前工作区的项目
agentsecrets project update 名称           # 更新项目
agentsecrets project delete 名称           # 删除项目
```

### 秘密管理（Secret Management）
```bash
agentsecrets secrets set 密钥=值         # 存储秘密
agentsecrets secrets get 密钥               # 获取密钥值（用户可见，您看不到）
agentsecrets secrets list                  # 仅列出密钥名称
agentsecrets secrets list --project 名称   # 列出特定项目的密钥
agentsecrets secrets push                  # 将密钥上传到云端（加密存储）
agentsecrets secrets pull                  | 下载云端的密钥到密钥链
agentsecrets secrets delete 密钥            | 删除密钥
agentsecrets secrets diff                  | 比较本地和云端的密钥
```

### 调用与代理（Calls and Proxy）
```bash
agentsecrets call --url URL --bearer 密钥   | 单次认证调用
agentsecrets call --url URL --method POST --bearer 密钥 --body '{}' | 使用代理进行 POST 请求
agentsecrets call --url URL --header 名称=密钥    | 使用自定义头部进行请求
agentsecrets call --url URL --query param=密钥    | 使用查询参数
agentsecrets call --url URL --basic 密钥    | 使用基本认证
agentsecrets call --url URL --body-field 路径=密钥 | 使用表单字段进行请求
agentsecrets proxy start                   | 启动 HTTP 代理
agentsecrets proxy start --port 9000       | 设置自定义端口
agentsecrets proxy status                  | 查看代理状态
agentsecrets proxy stop                    | 停止代理
agentsecrets proxy logs                    | 查看审计日志
agentsecrets proxy logs --last N           | 查看最近 N 条日志
agentsecrets proxy logs --secret 密钥       | 按密钥名称过滤日志
```

### MCP（Secrets Management Platform）
```bash
agentsecrets mcp serve                     | 启动 MCP 服务器
agentsecrets mcp install                   | 自动配置 Claude Desktop 和 Cursor
```

### 环境变量注入（Environment Variables）
```bash
agentsecrets env -- <命令> [参数...]     | 将秘密作为环境变量注入子进程
agentsecrets env -- stripe mcp              | 为 Stripe MCP 提供凭证支持
agentsecrets env -- node server.js          | 为 Node.js 提供凭证支持
agentsecrets env -- npm run dev             | 为开发服务器提供凭证支持
```

### 工作区安全设置（Workspace Security）
```bash
agentsecrets workspace allowlist add <域名> [域名...]  | 授权域名访问
agentsecrets workspace allowlist list                | 查看允许的域名列表
agentsecrets workspace allowlist log               | 查看被阻止的访问尝试
agentsecrets workspace promote user@email.com              | 授予管理员权限
agentsecrets workspace demote user@email.com               | 取消管理员权限
```

---

## 常见场景的处理方式

- **首次设置：** 按顺序执行步骤 1 至 5。
- **执行 API 调用：** 先运行 `agentsecrets status` 确认上下文，然后检查密钥是否存在，再执行 `agentsecrets secrets call`。
- **部署到生产环境：** 先切换到生产工作区（`agentsecrets workspace switch production`），然后检查密钥是否一致（`agentsecrets secrets diff`），如有需要则同步数据（`agentsecrets secrets pull`），最后执行部署操作（`agentsecrets proxy logs`）。
- **邀请团队成员：** 使用 `agentsecrets workspace invite` 邀请团队成员加入工作区。
- **密钥更新：** 告诉用户在终端中运行 `agentsecrets secrets set 密钥名称=新值`，然后检查密钥是否已更新（`agentsecrets secrets list`），最后将更新后的密钥推送到云端（`agentsecrets secrets push`）。
- **查询密钥：** 使用 `agentsecrets secrets list` 查看密钥列表。
- **查看审计日志：** 使用 `agentsecrets proxy logs --last 50` 查看最近的审计记录。

---

## 常见问题处理：

- **API 被阻止：** 如果 API 返回 403 错误，表示请求的域名不在允许的域名列表中，请不要直接访问该域名。指导用户在终端中运行 `agentsecrets workspace allowlist add <域名>`，或者一次性添加多个域名（`agentsecrets workspace allowlist add api.stripe.com api.openai.com`），等待用户确认密码并添加域名后重新尝试请求。
- **需要将秘密作为环境变量：** 先使用 `agentsecrets status` 确认上下文，然后使用 `agentsecrets env` 将密钥注入到相应的命令中。

---

## 重要规则：

1. **严禁** 显示、输出或记录任何凭证的实际值。
2. **严禁** 要求用户在聊天框中输入密钥值。
3. **严禁** 直接使用 `curl` 或其他非代理方式发送请求，必须使用 `agentsecrets call`。
4. **在新会话中执行任何秘密操作之前，务必运行 `agentsecrets status`。
5. **在部署工作流程之前，务必运行 `agentsecrets secrets diff`。
6. **如果用户在工作聊天中提到了密钥值，请要求他们删除相关消息。**
7. **您是操作者，需自主管理整个流程；除非涉及安装软件、输入密码或修改允许的域名列表，否则不要将命令委托给用户。**
8. **严格遵守零信任策略**：如果某个域名被阻止，请指导用户运行 `agentsecrets workspace allowlist add <域名>`。
9. **当需要将凭证传递给 CLI 工具时，使用 `agentsecrets env` 而不是手动输出密钥值。**
10. 如果在代理日志中看到 `(REDACTED)`，说明 AgentSecrets 已检测到原始凭证值并将其替换为 `[REDACTED_BY_AGENTSECRETS]`，这是正常的安全处理方式。

---

## 安全模型：

- **零知识（Zero-Knowledge）**：在任何环节中，凭证值都不会进入您的系统。
- **零信任（Zero-Trust）**：默认情况下，系统会拒绝来自未授权域名的请求。
- **响应内容屏蔽**：如果 API 返回了原始凭证值，代理会将其替换为 `[REDACTED_BY_AGENTSECRETS]`。
- **存储方式**：使用 macOS Keychain、Windows Credential Manager 或 Linux Secret Service 进行存储（仅保存加密后的数据）。
- **审计记录**：日志中仅记录密钥名称，不包含密钥值。
- **加密方式**：使用 X25519 + AES-256-GCM + Argon2id 进行加密。
- **权限管理**：仅工作区管理员可以修改允许的域名列表（需要输入密码）。

## 开源信息

AgentSecrets 是开源项目（许可证：MIT）。完整源代码位于：https://github.com/The-17/agentsecrets。所有凭证处理操作都在本地完成，除了 outbound API 请求外，没有任何数据会离开用户的设备。

---