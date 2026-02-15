---
name: meshguard
description: 管理 MeshGuard AI 代理的治理机制，包括代理、策略、审计日志以及监控功能。
metadata: {"clawdbot":{"requires":{"bins":["curl","jq"]}}}
---

# MeshGuard

这是一个AI代理治理平台，用于管理代理、策略、审计日志，并监控您的MeshGuard实例。

## 设置

首次设置时，请运行向导：
```bash
bash skills/meshguard/scripts/meshguard-setup.sh
```
该操作会将配置信息保存到`~/.meshguard/config`文件中（包括网关URL、API密钥和管理员令牌）。

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `MESHGUARD_URL` | 网关URL（默认值：`https://dashboard.meshguard.app`） |
| `MESHGUARD_API_KEY` | 用于身份验证请求的API密钥 |
| `MESHGUARD_ADMIN_TOKEN` | 用于组织管理和注册的管理员令牌 |

`~/.meshguard/config`配置文件会由CLI自动读取。

## CLI使用

所有命令都需要通过封装脚本来执行：
```bash
bash skills/meshguard/scripts/meshguard-cli.sh <command> [args...]
```

### 状态检查
```bash
meshguard-cli.sh status
```
返回网关的健康状况、版本信息以及连接状态。

### 代理管理
```bash
meshguard-cli.sh agents list                          # List all agents in org
meshguard-cli.sh agents create <name> --tier <tier>   # Create agent (tier: free|pro|enterprise)
meshguard-cli.sh agents get <agent-id>                # Get agent details
meshguard-cli.sh agents delete <agent-id>             # Delete agent
```

### 策略管理
```bash
meshguard-cli.sh policies list                        # List all policies
meshguard-cli.sh policies create <yaml-file>          # Create policy from YAML file
meshguard-cli.sh policies get <policy-id>             # Get policy details
meshguard-cli.sh policies delete <policy-id>          # Delete policy
```

策略的YAML格式如下：
```yaml
name: rate-limit-policy
description: Limit agent calls to 100/min
rules:
  - type: rate_limit
    max_requests: 100
    window_seconds: 60
  - type: content_filter
    block_categories: [pii, credentials]
```

### 审计日志
```bash
meshguard-cli.sh audit query                              # Recent audit events
meshguard-cli.sh audit query --agent <name>               # Filter by agent
meshguard-cli.sh audit query --action <action>            # Filter by action type
meshguard-cli.sh audit query --limit 50                   # Limit results
meshguard-cli.sh audit query --agent X --action Y --limit N  # Combined filters
```

支持的命令：`agent.create`、`agent.delete`、`policy.create`、`policy.update`、`policy.delete`、`auth.login`、`auth.revoke`

### 自助注册
```bash
meshguard-cli.sh signup --name "Acme Corp" --email admin@acme.com
```
创建一个新的组织并返回API凭据。需要`MESHGUARD_ADMIN_TOKEN`。

## 工作流程示例

**为新代理配置策略并启用其功能：**
1. 创建代理：`meshguard-cli.sh agents create my-agent --tier pro`
2. 创建策略：`meshguard-cli.sh policies create policy.yaml`
3. 验证代理状态：`meshguard-cli.sh agents list`

**查询代理活动：**
1. 查询日志：`meshguard-cli.sh audit query --agent my-agent --limit 20`
2. 检查代理状态：`meshguard-cli.sh agents get <id>`

## API参考

有关完整的端点文档，请参阅`skills/meshguard/references/api-reference.md`。