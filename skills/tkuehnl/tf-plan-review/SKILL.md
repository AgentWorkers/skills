---
name: tf-plan-review
description: 在应用 Terraform 计划之前，先对其进行风险分析。将每一项变更分为“安全”、“中等风险”、“危险”或“严重风险”三类。能够检测到对系统造成的破坏、与身份和访问管理（IAM）相关的变更、数据丢失风险以及潜在的破坏范围。该工具仅提供只读功能，绝不会执行任何应用（apply）操作。
version: 0.1.1
author: Anvil AI
tags: [terraform, opentofu, iac, infrastructure, devops, risk-assessment, plan-review, security, discord, discord-v2]
---
# Terraform 计划分析器与风险评估工具

本工具可分析 `terraform plan` 的输出结果，并在您执行 `apply` 操作之前，对每次基础设施变更进行基于人工智能的风险评估。

**请注意：** 本工具仅用于读取数据，**绝不** 执行任何会修改基础设施或状态的命令，例如 `terraform apply`、`terraform destroy`、`terraform import`、`terraform taint` 等。

## 激活方式

当用户输入以下关键词时，该工具将被激活：
- `terraform plan`、`tf plan`、`review plan`、`plan review`
- `is this plan safe`、`safe to apply`、`risk assessment`
- `what will be destroyed`、`what changes`、`terraform changes`
- `terraform state`、`state drift`、`drift detection`
- `terraform validate`、`validate config`、`tf validate`
- `IAM changes`、`security group changes`、`infrastructure changes`
- `blast radius`、`cascade effects`、`dependencies`
- `tofu plan`（使用不同的二进制文件）

## 示例提示：
1. “在应用之前，请先审查这个 Terraform 计划。”
2. “这个计划会删除哪些资源？”
3. “这个计划安全吗？”
4. “显示状态变化情况。”
5. “这个计划中有哪些 IAM 变更？”
6. “验证位于 ~/infra/prod 目录下的 Terraform 配置。”
7. “对 /deployments/staging 目录中的 Terraform 计划进行风险评估。”
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

### 变更类型（来自计划 JSON 文件）

| 变更类型 | 含义 | 风险等级 |
|--------|---------|-------------|
| `create` | 添加新资源 | 通常安全（除非涉及 IAM/安全设置） |
| `update` | 修改现有资源 | 中等风险（具体取决于修改内容） |
| `delete` | 永久删除资源 | **非常危险**——存在数据丢失的风险 |
| `replace`（`delete` + `create`） | 需要先删除再创建资源 | **非常危险**——会导致停机并可能丢失数据 |
| `read` | 刷新数据源 | 安全（仅读取操作） |
| `no-op` | 无需任何更改 | 安全 |

### 什么情况会导致高风险？

**严重风险（🔴）：**
- 删除或替换以下内容：IAM 角色/策略、安全组、KMS 密钥、秘密信息、数据库（RDS、DynamoDB、Cloud SQL、Azure SQL）、S3 存储桶、DNS 记录、WAF 规则、CloudTrail
- 修改 IAM 策略或安全组规则、加密设置
- 这些变更可能导致 **数据丢失**、**安全漏洞** 或 **服务中断**

**危险风险（🟠）：**
- 删除或替换以下内容：EC2 实例、负载均衡器、ECS/EKS 集群、VPC、子网、NAT 网关、Lambda 函数、API 网关
- 这些变更会导致 **停机**，并且可能需要手动干预才能恢复

**中等风险（🟡）：**
- 修改自动扩展策略、监控/警报规则、启动模板
- 创建敏感资源（如新的 IAM 角色、新的安全组）
- 影响 **容量** 或 **可观测性** 但不会影响数据完整性的变更

**安全风险（🟢）：**
- 仅修改标签的变更
- 创建新的非敏感资源
- 无操作或仅读取操作的变更

### 特别需要注意的 `replace` 操作

当 Terraform 命令提示需要 `replace` 资源时，意味着：
1. **必须** 删除现有资源（不可恢复）
2. **然后** 使用新配置创建新资源

这种情况通常发生在资源的不可变属性发生变化时（例如，修改 RDS 的 `engine_version`、EC2 的 `ami` 或子网的 AZ）。代理应 **特别强调` replace` 操作，因为：
- 旧资源及其数据会被删除
- 在删除和创建之间会有一段停机时间
- 依赖资源可能会在转换过程中出现故障

## 代理工作流程

根据用户的意图，严格按照以下步骤操作：

### 计划分析（“审查这个计划”、“这个计划安全吗”、“有哪些变更”）

#### 第一步：运行计划分析

```bash
bash <skill_dir>/scripts/tf-plan-review.sh plan <directory>
```

如果没有指定目录，将使用当前工作目录。
脚本输出：
- **stdout**：包含所有资源变更、风险分类和总结的结构化 JSON 数据
- **stderr**：格式精美的 Markdown 风险报告

#### 第二步：解析 JSON 数据

解析 JSON 输出。关键字段如下：
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

在 `stderr` 中显示 Markdown 报告，并添加您自己的分析：
1. **首先说明整体风险等级**，以便用户一目了然
2. **重点突出删除和严重风险**——这些变更可能会影响生产环境
3. **用通俗的语言解释每个严重风险的原因**
4. **评估影响范围**——哪些资源依赖于被删除的资源
5. **提供预应用检查清单**——用户需要验证哪些内容
6. **给出明确建议**：“可以安全应用” / “需要进一步审查” / “请勿在没有___的情况下执行应用”

**对于严重风险的计划，提示语应明确且直接：**
- 对于可能删除生产环境数据库的计划，要直言不讳。
- “此计划将 **永久删除** `prod-db` 数据库。所有数据都将丢失。您有备份吗？”
- 确保用户能够立即意识到问题的严重性。

### 状态检查（“显示状态”、“管理哪些资源”、“状态变化”）

```bash
bash <skill_dir>/scripts/tf-plan-review.sh state "<filter>" <directory>
```

过滤条件是可选的——它可以筛选特定类型的资源。示例：
- `bash <skill_dir>/scripts/tf-plan-review.sh state "iam" .` → 显示所有 IAM 资源
- `bash <skill_dir>/scripts/tf-plan-review.sh state "aws_instance" .` → 显示所有 EC2 实例
- `bash <skill_dir>/scripts/tf-plan-review.sh state "" .` → 显示所有资源

### 配置验证（“验证配置”、“检查语法”）

```bash
bash <skill_dir>/scripts/tf-plan-review.sh validate <directory>
```

在不执行计划的情况下，报告配置错误和警告。

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TF_binary` | 自动检测 | 可指定二进制文件：`terraform`、`tofu` 或其他路径 |
| `TF_PLAN_TIMEOUT` | `600` | `terraform plan` 的超时时间（以秒为单位）

脚本会优先尝试使用 `terraform`，如果找不到则使用 `tofu`。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 未找到 `terraform` 或 `tofu` | 显示安装链接的 JSON 错误 |
| 未找到 `jq` | 显示安装链接的 JSON 错误 |
| 目录中不存在 `.tf` 文件 | 显示错误：“未找到 Terraform 配置文件” |
| 未初始化 | 自动运行 `terraform init`（用于计划分析）或 `terraform init -backend=false`（用于配置验证） |
- 计划执行失败（由于提供程序错误） | 从计划 JSON 日志中提取错误信息并报告 |
- 计划超时 | 超过 `TF_PLAN_TIMEOUT` 后终止脚本 |
- 未找到状态信息 | 显示错误：“未找到状态信息” |
- 状态为空 | 显示“没有管理的资源”

## 安全注意事项（重要规则）：
1. **绝对禁止执行 `terraform apply`**——即使使用了 `-auto-approve` 或 `-target` 选项，也不允许。
2. **绝对禁止执行 `terraform destroy`**——在任何情况下都不允许。
3. **绝对禁止执行 `terraform import`**——该命令会修改状态。
4. **绝对禁止执行 `terraform taint` 或 `terraform untaint`**——这些命令也会修改状态。
5. **绝对禁止执行 `terraform state mv`、`terraform state rm` 或 `terraform state push`**——这些命令同样会修改状态。
6. **切勿泄露云服务凭证**——如果计划输出中包含凭证信息，请将其隐藏。
7. **处理敏感数据**——Terraform 会标记某些值为 `(sensitive)`；切勿泄露这些信息。
8. **切勿缓存或存储计划输出**——计划文件中可能包含敏感信息。
9. 本工具仅执行的 Terraform 命令包括：`plan`、`show`、`state list`、`state show`、`validate`、`init`、`providers`。

如果用户要求执行计划，请回答：
> “我可以分析并评估 Terraform 计划，但无法直接执行应用操作。在执行 `terraform apply` 之前，您需要先核实以下内容……”

## 常见问题及使用提示：

### “这个计划安全吗？”
运行计划分析。如果整体风险等级为 🟢（低风险）：
> “此计划看起来是安全的。它只会创建新的资源，不会删除任何资源或修改安全设置。预应用检查清单也很简单。”

如果整体风险等级为 🔴（严重风险）：
> “⚠️ 此计划存在严重风险。[具体说明风险]。强烈建议由其他团队成员再次审查后再执行。”

### “这个计划会删除哪些资源？”
运行计划，然后筛选出 `action == "delete"` 或 `action == "replace"` 的操作。对于每个被删除的资源，需提供：
- 资源地址
- 资源类型
- 该资源的重要性（是否具有数据）
- 有哪些资源依赖于它

### “这个计划中有哪些 IAM 变更？”
运行计划，然后筛选出涉及 IAM 设置的变更。对于每个变更，需说明：
- 哪些权限会被修改
- 是增加还是移除了访问权限
- 是否存在过于宽松的权限设置（例如，`Action: *`）

### “显示影响范围”
运行计划，找出所有被删除或替换的资源，然后解释：
- 哪些资源依赖于这些被删除的资源
- 删除这些资源后会导致哪些问题
- Terraform 是否会自动处理依赖关系，或者是否需要手动干预

### Discord v2 交付模式（OpenClaw v2026.2.14+）

在 Discord 频道中使用时：
- 先发送简要的总结信息（整体风险、被删除的资源数量、严重风险资源），然后询问用户是否需要查看完整报告。
- 第一条消息的长度控制在 1200 字符以内，并避免使用大型 Markdown 表格。
- 如果支持 Discord 的交互功能，可以提供以下操作：
  - `Show Critical Changes`（显示严重风险）
  - `Show Destroyed Resources`（显示被删除的资源）
  - `Show Pre-Apply Checklist`（显示预应用检查清单）
- 如果无法使用交互功能，可以提供详细的列表。
- 对于复杂的计划，每条消息的长度控制在 15 行以内。

## 敏感数据处理

Terraform 计划 JSON 文件可能包含敏感信息。脚本仅提取资源的地址、类型和操作类型，**不会** 提取属性值。在展示结果时：
- 绝不显示 Terraform 标记为 `(sensitive)` 的属性值
- 绝不显示提供程序的凭证信息或后端配置秘密
- 如果用户询问具体变更内容，可以说明可以看到变更类型，但敏感信息已被隐藏
- 绝不存储或缓存计划输出文件

## 由 Anvil AI 提供支持 🔍