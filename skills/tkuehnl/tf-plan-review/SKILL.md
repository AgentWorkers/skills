---
name: tf-plan-review
description: 在应用之前，先分析 Terraform 计划中的风险。将每个变更分为“安全”、“中等风险”、“危险”或“关键”三类。能够检测到数据损坏、身份与访问管理（IAM）变更、数据丢失风险以及潜在的破坏范围。该工具仅提供只读功能，绝不会执行任何应用（apply）操作。
version: 0.1.1
author: CacheForge
tags: [terraform, opentofu, iac, infrastructure, devops, risk-assessment, plan-review, security, discord, discord-v2]
---
# Terraform 计划分析器与风险评估工具

该工具能够分析 `terraform plan` 的输出结果，并在您执行 `apply` 命令之前，对每次基础设施变更进行基于人工智能的风险评估。

**请注意：** 该工具仅具有 **读取权限**，仅用于分析数据，**绝不会** 执行任何修改基础设施或状态的命令，例如 `terraform apply`、`terraform destroy`、`terraform import`、`terraform taint` 等。

## 激活条件

当用户输入以下关键词时，该工具将被激活：
- `terraform plan`、`tf plan`、`review plan`、`plan review`
- `is this plan safe`、`safe to apply`、`risk assessment`
- `what will be destroyed`、`what changes`、`terraform changes`
- `terraform state`、`state drift`、`drift detection`
- `terraform validate`、`validate config`、`tf validate`
- `IAM changes`、`security group changes`、`infrastructure changes`
- `blast radius`、`cascade effects`、`dependencies`
- `tofu plan`（使用不同的二进制文件）

## 示例使用场景

1. “在我执行 `apply` 命令之前，请先审查这个 Terraform 计划。”
2. “这个计划会删除哪些资源？”
3. “这个计划安全吗？”
4. “显示当前的状态变化情况。”
5. “这个计划中包含了哪些 IAM 变更？”
6. “验证位于 `~/infra/prod` 目录下的 Terraform 配置文件。”
7. “对 `/deployments/staging` 目录中的 Terraform 计划进行风险评估。”
8. “如果执行这个计划，会产生多大的影响范围？”

## 权限设置

```yaml
permissions:
  exec: true          # Required to run terraform/tofu CLI
  read: true          # Read .tf files and plan output
  write: false        # NEVER writes — strictly read-only analysis
  network: true       # terraform plan needs provider API access
```

## Terraform 变更类型——代理需要了解的信息

准确识别 Terraform 的变更类型对于进行风险评估至关重要：

### 变更类型（来自计划 JSON 数据）

| 变更类型 | 含义 | 风险等级 |
|--------|---------|-------------|
| `create` | 添加新资源 | 通常安全（除非涉及 IAM/安全配置） |
| `update` | 修改现有资源 | 中等风险（具体风险取决于变更内容） |
| `delete` | 永久删除资源 | **非常危险**——可能导致数据丢失 |
| `replace`（`delete` + `create`） | 需要先删除再创建资源 | **非常危险**——会导致停机并可能丢失数据 |
| `read` | 刷新数据源 | 安全（仅读取操作） |
| `no-op` | 无变更 | 安全 |

### 什么会导致高风险？

**严重风险（🔴）：**
- 删除或替换以下内容：IAM 角色/策略、安全组、KMS 密钥、秘密信息、数据库（RDS、DynamoDB、Cloud SQL、Azure SQL）、S3 存储桶、DNS 记录、WAF 规则、CloudTrail
- 修改 IAM 策略或安全组规则、加密设置
- 这些变更可能导致 **数据丢失**、**安全漏洞** 或 **服务中断**

**危险风险（🟠）：**
- 删除或替换以下内容：EC2 实例、负载均衡器、ECS/EKS 集群、VPC、子网、NAT 网关、Lambda 函数、API 网关
- 这些变更会导致 **停机**，并且可能需要手动干预才能恢复

**中等风险（🟡）：**
- 修改自动扩展策略、监控/警报规则、启动模板
- 创建敏感资源（如新的 IAM 角色或安全组）
- 变更影响 **容量** 或 **可观测性**，但不影响数据完整性

**安全风险（🟢）：**
- 仅修改标签
- 创建新的非敏感资源
- 无操作或仅读取操作

### 特别需要注意的 `replace` 操作

当 Terraform 建议执行 `replace` 操作时，意味着：
1. **必须** 先删除现有资源（不可逆操作）
2. **然后** 使用新配置创建新资源

这种情况通常发生在资源的不可变属性发生变化时（例如，修改 RDS 的 `engine_version`、EC2 的 `ami` 或子网的 AZ）。代理应 **特别强调`replace` 操作，因为：
- 旧资源及其数据将被删除
- 在删除和创建新资源之间存在时间间隔（导致停机）
- 依赖资源可能会在转换过程中出现问题

## 代理工作流程

根据用户的意图，严格按照以下步骤操作：

### 计划分析（例如：“审查这个计划”、“这个计划安全吗？”、“有哪些变更”）

#### 第一步：运行计划分析

```bash
bash <skill_dir>/scripts/tf-plan-review.sh plan <directory>
```

如果未指定目录，将使用当前工作目录。
脚本输出：
- **stdout**：包含所有资源变更、风险分类和总结的结构化 JSON 数据
- **stderr**：格式优美的 Markdown 风险报告

#### 第二步：解析 JSON 数据

解析 JSON 输出结果。关键字段如下：

```json
{
  "overall_risk": "🔴 CRITICAL | 🔴 HIGH | 🟡 MODERATE | 🟢 LOW",
  "summary": {
    "create": 5,
    "update": 3,
    "destroy": 1,
    "replace": 0
  },
  "risk_breakdown": {
    "critical": 1,
    "dangerous": 0,
    "moderate": 2,
    "safe": 5
  },
  "resources": [
    {
      "address": "aws_iam_role.admin",
      "action": "delete",
      "risk": "🔴 CRITICAL"
    }
  ]
}
```

#### 第三步：展示风险评估结果

从 `stderr` 中显示 Markdown 报告，并添加您自己的分析：
1. **首先说明总体风险等级**，以便用户直观了解风险情况
2. **重点突出删除和严重风险**——这些变更可能对生产环境造成严重影响
3. **用通俗的语言解释每个严重风险的原因**
4. **评估影响范围**——哪些资源会受到这些变更的影响
5. **提供预执行检查清单**——用户需要验证哪些内容
6. **给出明确建议**：“可以安全执行” / “需要进一步审查” / “请勿执行”

**对于严重风险计划的提示：**
- 对于可能破坏生产环境的变更，不要委婉表述。例如：“该计划将 **永久删除** `prod-db` 数据库。所有数据都将丢失。您有备份吗？”
- 确保用户能够立即意识到潜在的严重后果。

### 状态检查（例如：“显示当前状态”、“管理了哪些资源”、“状态变化”）

```bash
bash <skill_dir>/scripts/tf-plan-review.sh state "<filter>" <directory>
```

过滤条件是可选的——可用于筛选特定类型的资源。示例：
- `bash <skill_dir>/scripts/tf-plan-review.sh state "iam" .` → 显示所有 IAM 资源
- `bash <skill_dir>/scripts/tf-plan-review.sh state "aws_instance" .` → 显示所有 EC2 实例
- `bash <skill_dir>/scripts/tf-plan-review.sh state "" .` → 显示所有资源

### 配置验证（例如：“验证配置”、“检查语法”

```bash
bash <skill_dir>/scripts/tf-plan-review.sh validate <directory>
```

该工具会在不执行实际操作的情况下报告配置错误和警告。

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TF_BINARY` | 自动检测 | 可指定二进制文件：`terraform`、`tofu` 或其他路径 |
| `TF_PLAN_TIMEOUT` | `600` | `terraform plan` 的执行超时时间（以秒为单位） |

脚本会优先尝试使用默认的 `terraform` 工具，如果找不到则使用 `tofu`。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 未找到 `terraform` 或 `tofu` | 显示安装链接的 JSON 错误信息 |
| 未找到 `jq` | 显示安装链接的 JSON 错误信息 |
| 目录中不存在 `.tf` 文件 | 显示错误信息：“未找到 Terraform 配置文件” |
| 未初始化 | 自动运行 `terraform init`（用于计划分析）或 `terraform init -backend=false`（用于配置验证） |
| 计划执行失败 | 从计划 JSON 中提取错误信息并显示 |
| 计划执行超时 | 超时后终止脚本 |
| 未找到状态信息 | 显示错误信息：“未找到状态数据” |
| 状态为空 | 显示“未管理任何资源”

## 安全注意事项（重要规则）

1. **绝不要执行 `terraform apply`**——即使使用了 `-auto-approve` 或 `-target` 选项，也不允许执行。
2. **绝不要执行 `terraform destroy`**——在任何情况下都不允许。
3. **绝不要执行 `terraform import`**——该操作会修改基础设施状态。
4. **绝不要执行 `terraform taint` 或 `terraform untaint`**——这些操作也会修改状态。
5. **绝不要执行 `terraform state mv`、`terraform state rm` 或 `terraform state push`**——这些操作同样会修改状态。
6. **绝不要泄露云服务凭证**——如果计划输出中包含凭证信息，请对其进行隐藏处理。
7. **处理敏感数据**：Terraform 会标记某些值为 `(sensitive)`；切勿泄露这些敏感信息。
8. **不要缓存或存储计划输出**——计划文件中可能包含敏感数据。
9. 该工具仅允许执行的 Terraform 命令包括：`plan`、`show`、`state list`、`state show`、`validate`、`init`、`providers`。

如果用户要求执行计划，请回答：
> “我可以分析并评估 Terraform 计划，但不能直接执行它们。执行基础设施变更需要人工审核和明确操作。根据我的分析，以下是您在运行 `terraform apply` 之前需要验证的内容……”

## 常见问题及使用建议

### “这个计划安全吗？”
执行计划分析。如果总体风险等级为 🟢（低风险）：
> “这个计划看起来是安全的。它只会创建新的资源，不会删除任何资源或修改安全设置。预执行检查清单也很简单。”

如果总体风险等级为 🔴（严重风险）：
> “⚠️ 该计划存在严重风险。[具体说明风险内容]。强烈建议由其他团队成员再次审核后再执行。”

### “这个计划会删除哪些资源？”
执行计划后，筛选出 `action == "delete"` 或 `action == "replace"` 的操作。对于每个要删除的资源，需提供以下信息：
- 资源地址
- 资源类型
- 该资源的重要性（是否具有数据）
- 该资源依赖的其他资源

### “这个计划中包含了哪些 IAM 变更？”
执行计划后，筛选出涉及 IAM 配置变更的资源。对于每个变更，需提供以下信息：
- 更改的内容
- 是否会添加或移除访问权限
- 是否存在过度宽松的权限设置（例如 `Action: *`）

### “显示影响范围”
执行计划后，找出所有被删除或替换的资源，并解释：
- 哪些资源依赖于这些被删除的资源
- 删除这些资源后会导致哪些问题
- Terraform 是否会自动处理依赖关系，或者是否需要手动干预

### Discord v2 交付模式（OpenClaw v2026.2.14+）

在 Discord 频道中使用时：
- 先发送简要的总结信息（总体风险、删除的资源数量、严重风险资源），然后询问用户是否需要查看完整报告。
- 第一条消息的长度控制在 1200 字符以内，并避免使用复杂的 Markdown 表格。
- 如果支持 Discord 的相关功能，可以提供以下操作选项：
  - `Show Critical Changes`（显示严重风险）
  - `Show Destroyed Resources`（显示被删除的资源）
  - `Show Pre-Apply Checklist`（显示预执行检查清单）
- 如果相关功能不可用，可以提供详细的操作列表。
- 对于大型计划，每条消息的长度控制在 15 行以内。

## 敏感数据处理

Terraform 计划 JSON 文件中可能包含敏感信息。该工具不会提取资源的属性值，仅提取资源地址、类型和操作类型。但在展示结果时：
- 绝不要显示被标记为 `(sensitive)` 的属性值
- 绝不要显示提供商凭证或后端配置信息
- 如果用户询问具体变更内容，可以说明可以看到变更类型，但敏感信息已被隐藏
- 绝不要存储或缓存计划输出文件

## 技术支持：CacheForge 🔍