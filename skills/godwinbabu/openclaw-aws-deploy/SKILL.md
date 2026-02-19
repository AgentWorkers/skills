---
name: openclaw-aws-deploy
description: 通过一条命令，即可安全地在 AWS 上部署 OpenClaw。该命令会创建一个虚拟私有云（VPC）、一台运行 ARM64 架构的 EC2 实例、一个 Telegram 频道，以及一个可配置的 AI 模型（支持 Bedrock、Gemini 或其他提供商）。整个部署过程仅支持 SSM（System Managed Service）访问方式，不使用 SSH。适用于在 AWS 上设置 OpenClaw、向 EC2 部署新的代理实例或销毁现有的 AWS 部署环境。
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["aws", "jq", "openssl"] },
      },
  }
---
# OpenClaw AWS 部署技能

## 快速入门（最低配置，每月费用约 30 美元）

### 先决条件
- **AWS 凭据**：可以通过以下任意一种方式获取：
  - 使用 `--profile <name>` 标志指定 AWS CLI 配置文件
  - 在工作区根目录或技能目录中创建 `.env.aws` 文件（可选）：
    ```
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_DEFAULT_REGION=us-east-1
    ```
  - 使用现有的环境变量、AWS SSO 会话或 IAM 角色
- 在工作区根目录或技能目录中创建 `.env.starfish` 文件（推荐）：
    ```
  TELEGRAM_BOT_TOKEN=...     # from @BotFather (required)
  TELEGRAM_USER_ID=...       # your Telegram user ID (optional, enables auto-approve pairing)
  GEMINI_API_KEY=...         # from aistudio.google.com (optional, for Gemini models)
  ```
- 已安装 `aws` CLI，或使用 Docker 进行沙箱环境访问
- 确保系统上安装了 `jq` 和 `openssl` 工具

### 一次性部署

执行以下命令即可完成所有部署步骤：
1. 创建 VPC、子网、IGW 和路由表
2. 创建安全组（仅允许 SSM 连接）
3. 创建具有最小权限的 IAM 角色（支持 SSM、参数存储和 Bedrock 功能）
4. 将配置信息存储在 SSM 参数存储中（每次服务启动时都会从参数存储中获取配置信息，不会保存在代码仓库或静态镜像中）
5. 启动一个 `t4g.medium` 类型的 ARM64 实例，并使用用户数据自定义安装环境
6. 使用用户数据安装 Node.js 22，并配置 OpenClaw
7. 通过 SSM 运行测试用例
8. 将所有资源 ID 保存到 `deploy-output.json` 文件中

### 部署完成后
1. 向 Telegram 机器人发送消息，您将收到配对代码
2. 通过 SSM 完成配对操作：
   ```bash
   aws ssm start-session --target <INSTANCE_ID> --region us-east-1
   sudo -u openclaw bash
   export HOME=/home/openclaw
   openclaw pairing approve telegram <CODE>
   ```
3. 机器人即可正常使用！

### 卸载部署环境

```bash
# Using saved output:
./scripts/teardown.sh --from-output ./deploy-output.json --env-dir /path/to/workspace --yes

# Or by name (discovers via tags):
./scripts/teardown.sh --name starfish --region us-east-1 --env-dir /path/to/workspace --yes
```

## 模型支持

### `--model` 标志
您可以传递任何模型名称，该名称会直接添加到 `openclaw.json` 文件的 `model.primary` 字段中：
```bash
# Default (MiniMax M2.1 on Bedrock — no API key needed, uses IAM role)
./scripts/deploy_minimal.sh --name starfish --region us-east-1

# Gemini Flash (needs GEMINI_API_KEY in .env.starfish)
./scripts/deploy_minimal.sh --name starfish --region us-east-1 \
  --model google/gemini-2.0-flash
```

### AWS Bedrock
无论您选择哪种模型，系统都会自动为实例角色添加以下 Bedrock 权限：
`bedrock:InvokeModel` 和 `bedrock:InvokeModelWithResponseStream`。这意味着任何已部署的实例都可以通过 IAM 角色直接使用 Bedrock 模型，无需额外的 API 密钥。

**支持的 Bedrock 模型 ID：**
| 模型名称 | 描述 |
|------------|-------------|
| `amazon-bedrock/minimax.minimax-m2.1` | MiniMax M2.1 |
| `amazon-bedrock/minimax.minimax-m2` | MiniMax M2 |
| `amazon-bedrock/deepseek.deepseek-r1` | DeepSeek R1 |
| `amazon-bedrock/moonshotai.kimi-k2.5` | Kimi K2.5 |

> **注意：** 在使用 Bedrock 模型之前，必须在 AWS 控制台中启用相应的模型功能。

### Gemini
如果 `.env.starfish` 文件中包含 `GEMINI_API_KEY`，该密钥会存储在 SSM 中并写入 `auth-profiles.json` 文件中；如果未设置此密钥，则系统会忽略该参数。

### `.env.starfish` 文件的内容
```
TELEGRAM_BOT_TOKEN=...     # Required — from @BotFather
GEMINI_API_KEY=...         # Optional — from aistudio.google.com (needed for Gemini models)
```

## 架构（最低配置）
```
┌─────────────────────────────────────────────────────┐
│                      VPC (10.50.0.0/16)             │
│  ┌───────────────────────────────────────────────┐  │
│  │           Public Subnet (10.50.0.0/24)        │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │      EC2 t4g.medium (ARM64, 4GB)        │  │  │
│  │  │  ┌───────────────────────────────────┐  │  │  │
│  │  │  │       OpenClaw Gateway             │  │  │  │
│  │  │  │  • Node.js 22.14.0                 │  │  │  │
│  │  │  │  • Any model (Bedrock/Gemini/etc)   │  │  │  │
│  │  │  │  • Telegram channel                │  │  │  │
│  │  │  │  • Encrypted EBS (gp3, 20GB)       │  │  │  │
│  │  │  └───────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         ↑                              ↓
    SSM (no SSH/inbound)      Outbound HTTPS only
```

## 部署过程中需要注意的问题（共 22 个）
详细信息请参阅 `references/TROUBLESHOOTING.md` 文件。

### 实例配置
- **建议使用 `t4g.medium` 实例（4GB 内存）**：`t4g.small` 实例在安装 npm 包或启动网关时可能会出现内存不足（OOM）的问题
- **选择 ARM64 架构**：相比 x86 架构，ARM64 在性能和成本上更具优势

### Node.js
- **必须使用 Node.js 22 或更高版本**：OpenClaw 2026.x 版本要求 Node.js 版本不低于 22.12.0
- **建议使用官方提供的 Node.js 安装包**：在 AL2023 ARM64 环境中，使用 NodeSource 提供的 `setup_22.x` 安装包可能会导致问题
- **必须安装 git**：OpenClaw 的 npm 安装过程依赖于 git

### npm
- **请使用 `openclaw@latest` 版本**：使用原始的 `openclaw` 包可能会导致依赖项版本过低（例如 0.0.1）

### 网关配置
- **使用 `openclaw gateway run --allow-unconfigured` 命令启动网关**：不要使用 `gateway start` 命令（该命令会尝试使用 `systemctl --user`，但可能会失败）
- **配置文件必须命名为 `openclaw.json`，而不是 `config.yaml`**
- **必须设置 `gateway.mode: "local"`，否则会出现 “Missing config” 错误**
- **`gateway.auth.mode` 必须设置为 “token”；设置为 “none” 会导致错误**

### Telegram 配置
- **必须明确设置 `plugins.entriesTelegram.enabled: true`**
- **`dmPolicy` 应设置为 “pairing”，而不是 “allowlist”（否则会阻止所有未授权的连接）
- **`streamMode` 应设置为 “partial”；某些模型不支持流式交互，此时可以设置为 “off” 作为备用选项**

### 模型选择
- **推荐使用 Gemini 2.0 Flash 模型**：免费 tier 提供 15 个 RPM 许可证/天，支持流式交互功能
- **需要创建 `auth-profiles.json` 文件**：用于存储用户认证信息
- **Bedrock 模型的路径格式为 `amazon-bedrock/MODEL_ID`（而非 `bedrock/`）
- **使用 Bedrock 模型前需要在 AWS 控制台中启用相应模型**

### systemd 服务配置
- 为了提高系统的稳定性，简化了服务配置文件；移除了 `ProtectHome`、`ReadWritePaths=/tmp/openclaw` 和 `PrivateTmp` 等设置
- **设置 `NODE_OPTIONS="--max-old-space-size=1024"` 以减少内存使用量**

### 安全性注意事项
- **仅允许 SSM（Session Manager）进行连接**
- **配置信息在运行时从 SSM 中获取**：每次服务启动时都会重新获取配置信息，不会保存在代码仓库或静态镜像中
- **默认启用加密的 EBS 卷**：部署脚本会自动配置加密功能
- **必须使用 IMDSv2 协议**：`HttpTokens=required` 是必要的配置项

## 文件结构
```
scripts/
  deploy_minimal.sh        # One-shot deploy (VPC + EC2 + OpenClaw)
  teardown.sh              # Clean teardown of all resources
  setup_deployer_role.sh   # Create IAM role/user with minimum permissions
  preflight.sh             # Pre-deploy validation checks
  smoke_test.sh            # Post-deploy health verification

references/
  TROUBLESHOOTING.md   # All 22 issues + solutions
  config-templates/    # Ready-to-use config files
    gemini-flash.json  # OpenClaw config for Gemini Flash
    auth-profiles-gemini.json  # Auth profile template
    openclaw.service.txt  # Systemd unit file template
    startup.sh         # Startup script template
```

## 配置模板
- **OpenClaw 配置文件（gemini-flash.json）**：详见 `references/config-templates/gemini-flash.json`，包含所有必需的配置项
- **用户认证配置文件（auth-profiles-gemini.json）**：请创建于 `~/.openclaw/agents/main/agent/auth-profiles.json`
- **Systemd 服务配置文件（openclaw.service）**：为提高稳定性进行了简化处理；部分安全配置已被移除

## 成本估算（每月约 30 美元）
| 资源          | 成本         |
|----------------|--------------|
| t4g.medium (4GB ARM64)   | 约 24.53 美元/月   |
| EBS gp3 20GB       | 约 1.60 美元/月     |
| 公共 IP          | 约 3.65 美元/月     |
| Gemini Flash      | 免费 tier / 每 100 万令牌 0.30 美元 |
| **总计**        | 约 29.78 美元/月     |

## 常见问题及解决方法
- **“找不到 amazon-bedrock 的 API 密钥”**：请确保 `openclaw.json` 文件中包含 `modelsProviders` 配置项，且 `auth` 字段的值为 “aws-sdk”
- **“达到 API 使用率限制”**：建议切换到 Bedrock 模型，或使用 `--model amazon-bedrock/minimax.minimax-m2.1` 重新部署
- **Bedrock 模型返回错误**：请确保在 AWS 控制台中启用了相应的模型
- **部署后机器人无响应**：请在 `.env.starfish` 文件中设置 `TELEGRAM_USER_ID` 以完成自动配对，或通过 SSM 执行 `openclaw pairing approve telegram <ID>` 命令

## 安全规则
- **切勿在日志中输出敏感信息**
- **严禁打开 SSH 连接或开放任何 inbound 端口**：仅使用 SSM 进行通信
- **采用最小权限的 IAM 角色配置**  
- **所有资源需标记 `Project=<名称>` 和 `DeployId=<唯一 ID>`，以便后续统一清理**
- **始终使用加密的 EBS 卷**