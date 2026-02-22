---
name: Terraform & Infrastructure as Code Production Engineering
description: 完整的 Terraform 与 Infrastructure as Code (IaC) 生产方法论——包括项目结构、模块设计、状态管理、多环境部署、安全加固、测试、持续集成/持续交付（CI/CD）流程、成本优化以及配置漂移管理。适用于基础设施设计、Terraform 编写、IaC 代码审查或云环境管理等工作场景。
---
# Terraform与代码即基础设施的生产工程

这是一个包含14个阶段的系统，用于构建生产级别的代码即基础设施解决方案。该方案完全不依赖任何第三方库或工具，适用于任何云服务提供商和任何版本的Terraform。

---

## 第1阶段：快速健康检查

对任何Terraform项目执行以下8项检查：

| 编号 | 检查项 | 是否正常 | 是否需要立即修复 |
|--------|---------|-----------|-----------|
| 1    | 远程状态存储后端 | 使用S3/GCS/Azure Blob并启用锁定机制 | 使用本地状态或未启用锁定机制 |
| 2    | 状态数据加密 | 静态数据已加密且访问受限 | 状态数据未加密且访问权限广泛 |
| 3    | 模块版本固定 | 所有模块的版本都被固定 | 模块版本未被固定或使用`ref=main` |
| 4    | 提供商版本固定 | 使用`required_providers`并设置版本约束 | 无版本约束 |
| 5    | 环境隔离 | 每个环境（开发/测试/生产）的状态数据是独立的 | 状态数据在多个环境中共享 |
| 6    | 应用前先进行计划 | 编译器集成（CI）执行`plan`步骤，人工审核后执行`apply`步骤 | 本地直接执行`apply`步骤，无审核 |
| 7    | 秘密信息管理 | `.tf`文件中不包含秘密信息；使用密钥库或SSM等工具管理 | 在`.tf`文件中硬编码秘密信息 |
| 8    | 状态数据漂移检测 | 定期检测状态数据漂移（至少每周一次） | 未启用状态数据漂移检测 |

**总分：/16**（每项检查2分）。得分低于10分时，应停止当前操作并先修复基础问题。 |

---

## 第2阶段：项目结构

### 推荐的代码布局

```
infrastructure/
├── modules/                    # Reusable modules (internal registry)
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── README.md
│   ├── compute/
│   ├── database/
│   └── monitoring/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf            # Module calls with dev params
│   │   ├── backend.tf         # Dev state backend
│   │   ├── terraform.tfvars   # Dev variable values
│   │   └── versions.tf
│   ├── staging/
│   └── prod/
├── global/                     # Shared resources (IAM, DNS, etc.)
│   ├── iam/
│   ├── dns/
│   └── networking/
├── scripts/                    # Helper scripts (import, migration)
├── policies/                   # OPA/Sentinel policies
└── .github/workflows/          # CI/CD pipelines
```

### 7条架构规则

1. **每个模块只负责一项功能**——网络模块不应负责创建计算资源。
2. **环境配置应简洁**——通过传递不同参数来调用模块，避免代码重复。
3. **状态数据应隔离**——每个环境及每个逻辑组件（如网络和计算）都有独立的状态文件。
4. **模块中不应包含硬编码的值**——所有配置项都应设置为变量，并提供合理的默认值。
5. **模块的输出结果应作为API接口**——如果其他模块或团队需要某个值，该值应通过API获取。
6. **每个模块都应有`README`文件**——说明输入参数、输出结果、使用方法及依赖关系。
7. `terraform.lock.hcl`文件应被提交到版本控制系统中——确保所有Terraform提供商的版本都能被一致地使用。

### 文件命名规范

| 文件名 | 用途 |
|------|---------|
| `main.tf` | 主要资源定义文件 |
| `variables.tf` | 所有输入变量文件 |
| `outputs.tf` | 所有输出结果文件 |
| `versions.tf` | `terraform`和`required_providers`配置文件 |
| `backend.tf` | 状态数据存储后端配置文件 |
| `locals.tf` | 本地变量和计算表达式文件 |
| `data.tf` | 数据源配置文件 |
| `providers.tf` | 提供商配置文件（针对复杂情况） |

---

## 第3阶段：状态数据管理

### 远程后端设置（以AWS为例）

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "environments/prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    kms_key_id     = "alias/terraform-state"
  }
}
```

### 状态数据存储策略

```
{org}/{environment}/{component}/terraform.tfstate
```

示例：
- `acme/prod/networking/terraform.tfstate`
- `acme/prod/compute/terraform.tfstate`
- `acme/global/iam/terraform.tfstate`

### 状态数据操作的安全规则

| 操作 | 风险等级 | 安全建议 |
|--------|---------|-------------------|
| `terraform state mv` | 中等风险 | 应在操作前执行`plan`步骤以确保没有变化 |
| `terraform state rm` | 高风险 | 仅用于将资源导入其他地方 |
| `terraform import` | 中等风险 | 先写入配置文件，再执行导入操作，之后执行`plan`步骤进行验证 |
| `terraform state pull` | 低风险 | 仅用于检查状态数据 |
| `terraform state push` | 高风险 | 几乎禁止使用，可能导致状态数据不一致 |
| `moved`块 | 低风险 | 相比`state mv`更推荐使用，因为配置内容可被审核 |

### 6条状态数据管理规则

1. **严禁手动编辑状态数据JSON文件**——仅使用命令行工具（CLI）进行操作。
2. **严禁在不同环境中共享状态数据**——每个环境都应使用独立的存储后端。
3. **必须启用状态数据锁定机制**——例如使用DynamoDB（AWS）、Cloud Storage（GCP）或Azure的Blob存储服务。
4. **为状态数据存储桶启用版本控制**——以便能够回滚数据。
5. **限制对状态数据的访问权限**——仅允许CI/CD服务账户访问，禁止开发人员直接访问。
6. **状态数据中包含敏感信息**——对状态数据文件进行加密处理，无论是存储时还是传输过程中。

---

## 第4阶段：模块设计

### 模块接口模板

```hcl
# variables.tf — Module inputs
variable "name" {
  description = "Name prefix for all resources"
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,28}[a-z0-9]$", var.name))
    error_message = "Name must be 4-30 chars, lowercase alphanumeric + hyphens."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {}
}
```

### 模块组合模式

```hcl
# outputs.tf — Module contract
output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### 8条模块设计规则

1. **仅暴露必要的信息**——尽量减少变量数量。
2. **优先使用`for_each`而非`count`进行循环操作**——确保资源地址的稳定性。
3. **对输入参数进行验证**——在`plan`阶段捕获错误。
4. **默认设置为安全状态**——启用加密功能，关闭公共访问权限，限制权限等级。
5. **为所有配置项设置版本号**——模块使用semver格式进行版本控制，提供商使用`~>`进行版本约束。
6. **模块中不应包含提供商配置信息**——所有提供商配置信息应在项目根目录下统一管理。
7. **使用`moved`块进行重构**——避免使用`state mv`操作。
8. **为模块提供测试用例**——在`examples/`目录中提供可运行的配置示例。

---

## 第5阶段：多环境策略

### 环境配置对比

| 特征 | 开发环境 | 测试环境 | 生产环境 |
|--------|---------|---------|------|
| 实例规模 | 小型/微型 | 与生产环境类型匹配 | 适当调整规模 |
| 复制实例数量 | 1个 | 2个 | 3个或更多（高可用性配置） |
| 多区域部署 | 可选 | 必须 | 必须 |
| 备份保留时间 | 1天 | 7天 | 30天或更长时间 |
| 监控机制 | 基础监控 | 全面监控 | 全面监控，并集成PagerDuty |
| 自动扩展 | 关闭 | 开启 | 开启 |
| WAF/安全防护 | 关闭 | 开启 | 开启，并启用高级安全策略 |
| 状态数据访问权限 | 开发团队访问 | DevOps团队访问 | 仅限DevOps团队访问 |

### 变量层级结构

```hcl
# modules/compute/variables.tf
variable "instance_type" {
  type    = string
  default = "t3.micro"  # Safe default
}

variable "min_size" {
  type    = number
  default = 1
}

variable "enable_deletion_protection" {
  type    = bool
  default = true  # Safe default — must explicitly disable for dev
}
```

### 模块升级策略

```
dev → staging → prod
 │       │        │
 │       │        └─ Manual approval required
 │       └─ Auto-apply after plan review
 └─ Auto-apply on merge to dev branch
```

---

## 第6阶段：安全加固

### 15项安全检查清单

**P0（强制要求）：**
- `.tf`文件、`.tfvars`文件或状态数据文件中不得包含秘密信息（使用密钥库或SSM等工具进行管理）。
- 状态数据存储后端必须使用客户管理的密钥进行加密。
- 状态数据访问权限仅限于CI/CD服务账户。
- 对关键资源（如数据库、存储桶）启用`prevent_destroy`保护机制。
- 提供商凭证应通过环境变量或OIDC进行管理，严禁在配置文件中直接写入。
- `.gitignore`文件中应包含包含秘密信息的文件（如`.tfvars`、`.terraform/`、`*.tfstate*`）。

**P1（推荐要求）：**
- 使用OIDC进行CI/CD认证（避免使用长期有效的访问凭证）。
- 为Terraform服务账户设置最低权限的IAM角色。
- 明确配置安全组规则（除了ALB在443端口上的访问请求外，禁止所有其他访问请求）。
- 所有数据存储服务（如RDS、S3、EBS、ElasticCache）都必须启用加密功能。
- 启用CloudTrail/审计日志记录功能，记录所有API调用。

**P2（推荐）：**
- 在CI流程中实施OPA/Sentinel安全策略。
- 在CI流程中集成`tfsec`或`checkov`工具进行安全检查。
- 为每个环境创建独立的AWS账户（使用AWS Organizations功能）。

### 秘密信息管理决策树

```
Need a secret in Terraform?
├── Runtime secret (app needs at runtime)
│   └── Use AWS Secrets Manager / HashiCorp Vault
│       └── Reference via data source, pass ARN to app
├── Terraform-time secret (provider needs it)
│   └── Environment variable (TF_VAR_xxx) or OIDC
└── Generated secret (Terraform creates it)
    └── random_password resource → store in Secrets Manager
        └── Mark output as sensitive = true
```

### OIDC认证（适用于GitHub Actions和AWS）

```hcl
# No access keys needed
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

resource "aws_iam_role" "terraform_ci" {
  name = "terraform-ci"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Federated = data.aws_iam_openid_connect_provider.github.arn }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:org/infra:*"
        }
      }
    }]
  })
}
```

---

## 第7阶段：测试策略

### 四层测试体系

| 测试层次 | 使用工具 | 测试内容 | 测试时机 |
|-------|------|---------------|------|
| **静态测试** | `terraform validate`、`tflint`、`tfsec`、`checkov` | 检查语法、最佳实践及安全配置 | 每次提交代码时 |
| **计划阶段测试** | `terraform plan` + 安全策略检查 | 确保预期的变更不会发生 | 每个Pull Request（PR）提交时 |
| **合约验证测试** | `terratest` / `tftest`（Terraform 1.6及以上版本） | 检查模块的输入参数和输出结果，验证模块行为 | 每个PR提交时及夜间自动执行 |
| **集成测试** | 在真实云环境中进行测试 | 确保模块能够正常工作 | 每晚或每周自动执行 |

### Terraform内置的测试功能（Terraform 1.6及以上版本）

```hcl
# tests/networking.tftest.hcl
run "creates_vpc_with_correct_cidr" {
  command = plan

  variables {
    name        = "test"
    environment = "dev"
    vpc_cidr    = "10.0.0.0/16"
    azs         = ["us-east-1a"]
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR doesn't match input"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "rejects_invalid_environment" {
  command = plan
  expect_failures = [var.environment]

  variables {
    name        = "test"
    environment = "invalid"
    vpc_cidr    = "10.0.0.0/16"
    azs         = ["us-east-1a"]
  }
}
```

### 静态分析的CI流程

```yaml
- name: Terraform Lint & Security
  run: |
    terraform fmt -check -recursive
    terraform validate
    tflint --recursive
    tfsec .
    checkov -d . --framework terraform
```

### 7条测试规则

1. **每次提交代码时都进行静态分析**——可以免费捕获80%的潜在问题。
2. **每个PR提交时都进行人工审核**——确保基础设施配置变更符合预期。
3. **为每个模块编写内置的测试脚本**——利用`terraform test`功能。
4. **集成测试完成后执行清理操作**——避免产生不必要的资源残留。
5. **在隔离环境中进行测试**——避免使用生产环境的状态数据进行测试。
6. **为测试依赖项设置版本约束**——确保测试时使用的模块和提供商版本都是最新的。
7. **在CI过程中进行成本估算**——使用`infracost`工具避免不必要的成本支出。

---

## 第8阶段：CI/CD流程

### GitHub Actions流程

```yaml
name: Terraform
on:
  pull_request:
    paths: ['infrastructure/**']
  push:
    branches: [main]
    paths: ['infrastructure/**']

permissions:
  id-token: write    # OIDC
  contents: read
  pull-requests: write  # PR comments

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.7.x"
      - run: terraform fmt -check -recursive
      - run: terraform init -backend=false
      - run: terraform validate
      - run: tflint --recursive
      - run: tfsec . --soft-fail

  plan:
    needs: validate
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: |
          terraform init
          terraform plan -out=tfplan -no-color
      - uses: actions/upload-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}/tfplan

  apply:
    if: github.ref == 'refs/heads/main'
    needs: plan
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    strategy:
      matrix:
        environment: [dev, staging, prod]
      max-parallel: 1  # Sequential: dev → staging → prod
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - uses: actions/download-artifact@v4
        with:
          name: tfplan-${{ matrix.environment }}
          path: infrastructure/environments/${{ matrix.environment }}
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: terraform apply tfplan
```

### CI/CD规则

1. **严禁从本地机器执行`apply`操作**——必须通过CI/CD流程进行部署。
2. **应用的配置应与审核过的计划内容一致**——确保实际应用的配置与审核过的计划内容相同。
3. **环境升级应依次进行**——先在开发环境，再在测试环境，最后在生产环境。
4. **生产环境中的部署操作需要审批**——遵循GitHub的环境安全规则。
5. **定期检测状态数据漂移**——每周执行`plan`步骤以检测手动修改的情况。
6. **在PR提交时进行成本估算**——使用`infracost`工具进行成本预估。

---

## 第9阶段：资源管理策略

### 标签管理策略

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Team        = var.team
    CostCenter  = var.cost_center
    Repository  = "github.com/org/infrastructure"
  }
}

# Apply to all resources
resource "aws_instance" "app" {
  # ...
  tags = merge(local.common_tags, {
    Name = "${var.name}-app"
    Role = "application"
  })
}
```

### 文件命名规范

```
{project}-{environment}-{component}-{qualifier}
```

示例：`acme-prod-vpc-main`、`acme-staging-rds-primary`、`acme-prod-alb-api`

### 常见的资源管理策略

**条件性资源创建：**
```hcl
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.environment == "prod" ? 1 : 0
  # Only create alarms in prod
}
```

**动态配置块：**
```hcl
resource "aws_security_group" "app" {
  name   = "${var.name}-app"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
      description = ingress.value.description
    }
  }
}
```

**跨堆栈引用的数据源：**
```hcl
# Instead of hardcoding VPC ID
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "environments/prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use: data.terraform_remote_state.networking.outputs.vpc_id
```

---

## 第10阶段：状态数据漂移管理

### 状态数据漂移检测机制

```yaml
# .github/workflows/drift-detection.yml
name: Drift Detection
on:
  schedule:
    - cron: '0 8 * * 1'  # Weekly Monday 8 AM UTC

jobs:
  detect:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::role/terraform-ci
          aws-region: us-east-1
      - uses: hashicorp/setup-terraform@v3
      - working-directory: infrastructure/environments/${{ matrix.environment }}
        run: |
          terraform init
          terraform plan -detailed-exitcode -no-color 2>&1 | tee plan.txt
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "::warning::Drift detected in ${{ matrix.environment }}"
            # Send Slack alert
          fi
```

### 状态数据漂移响应流程

| 漂移类型 | 应对措施 |
|-----------|----------|
| 通过控制台进行的非关键性修改 | 导入或更新配置以匹配新的状态 |
| 通过控制台进行的重大修改 | 调查修改原因，并进行相应调整 |
| 自动扩展或自动配置组（ASG）引起的修改 | 如果是预期内的修改，可以使用`ignore_changes`功能 |
| AWS服务更新 | 更新对应的提供商版本，并查看变更日志 |
| 安全组被手动修改 | 立即启动安全事件调查 |

### `ignore_changes`的使用指南

仅在使用`ignore_changes`时，请确保：
- 修改的内容是由应用程序在运行时动态生成的（例如ASG配置的实例数量）。
- 修改的内容由外部系统管理（例如AWS备份标签）。
- 修改的内容是由于API行为导致的（例如默认的安全组规则）。

**严禁在以下情况下使用`ignore_changes`：**
- 安全配置的修改。
- 网络规则的修改。
- IAM策略的修改。
- 加密设置的修改。

---

## 第11阶段：成本优化

### 在CI过程中进行成本优化

### 成本优化策略

| 优化方法 | 可节省的成本 | 实施方式 |
|---------|---------|----------------|
| 预留实例/节省计划 | 30-60% | 适用于稳定的工作负载 |
| 适当调整实例规模 | 20-40% | 监控CPU和内存使用情况，减少过度配置的资源 |
| 对非关键资源使用弹性实例或可抢占实例 | 60-90% | 适用于批量任务或开发环境 |
| 使用S3生命周期策略 | 20-50% | 优化存储空间使用 |
| 选择合适的NAT Gateway类型 | 每月节省30-100美元 | 适用于开发环境 |
| 根据需求安排开发环境的资源调度 | 60-70% | 根据需求在夜间或周末销毁资源 |
| 清理未使用的资源 | 根据资源标签设置过期时间，7天后自动删除 |

### 标签管理用于成本分配

**必须设置的成本标签（通过策略强制使用）：**
- `CostCenter`：用于关联业务部门。
- `Environment`：区分开发环境、测试环境和生产环境。
- `Project`：标识资源所属的项目。
- `Team`：指定负责该资源的团队。
- `ManagedBy`：记录资源的管理员或工具（如Terraform或手动管理）。

---

## 第12阶段：高级实践

### 使用Terragrunt简化代码重复

当有多个环境且模块结构相同时，可以使用Terragrunt来避免代码重复：

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "s3"
  generate = { path = "backend.tf", if_exists = "overwrite_terragrunt" }
  config = {
    bucket         = "company-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### 多区域配置的提供商别名设置

```hcl
# Declarative import — reviewable in PR
import {
  to = aws_s3_bucket.existing
  id = "my-existing-bucket"
}

resource "aws_s3_bucket" "existing" {
  bucket = "my-existing-bucket"
  # Write config to match existing resource
}
```

### 用于重构的`moved`块

```hcl
# Rename without destroy+create
moved {
  from = aws_instance.app
  to   = aws_instance.application
}

# Move into module
moved {
  from = aws_instance.app
  to   = module.compute.aws_instance.app
}
```

---

## 第13阶段：灾难恢复与迁移

### 状态数据恢复

```bash
# Enable versioning on state bucket (BEFORE you need it)
aws s3api put-bucket-versioning \
  --bucket company-terraform-state \
  --versioning-configuration Status=Enabled

# List state versions
aws s3api list-object-versions \
  --bucket company-terraform-state \
  --prefix environments/prod/networking/terraform.tfstate

# Restore previous version
aws s3api get-object \
  --bucket company-terraform-state \
  --key environments/prod/networking/terraform.tfstate \
  --version-id "versionId123" \
  restored-state.tfstate
```

### 迁移流程

1. 执行`terraform state pull`以备份当前状态数据。
2. 更新`backend.tf`文件中的后端配置。
3. 使用`terraform init -migrate-state`命令复制状态数据。
4. 执行`terraform plan`以确认状态数据没有变化。
5. 在非关键资源上测试新的配置。
6. 在验证通过后删除旧的状态数据（通常为7天后）。

### 升级过程中的注意事项

在升级Terraform或提供商版本时：
1. 阅读官方变更日志，了解可能导致的兼容性问题。
2. 先在开发环境中测试新的配置。
3. 更新`.terraform.lock.hcl`文件。
4. 在所有环境中依次执行`terraform plan`操作。
5. 依次在开发环境、测试环境和生产环境中应用新的配置，每次之间间隔24小时。

---

## 第14阶段：质量评估

### Terraform项目质量评估标准（100分制）

| 评估维度 | 权重 | 分数范围 |
|-----------|--------|-------------|
| 状态数据管理 | 20% | 0-20分 |
| 安全性 | 20% | 0-20分 |
| 模块设计 | 15% | 0-15分 |
| 测试覆盖范围 | 15% | 0-15分 |
| CI/CD自动化 | 10% | 0-10分 |
| 文档编写 | 10% | 0-10分 |
| 成本管理 | 5% | 0-5分 |
| 状态数据漂移管理 | 5% | 0-5分 |

**评分标准说明：**
- **90-100分**：达到生产级标准，自动化程度高，经过充分测试。
- **70-89分**：基础架构较为完善，但仍存在一些需要改进的地方。
- **50-69分**：功能基本满足需求，但存在安全隐患，需重点关注安全性和状态数据管理。
- **低于50分**：建议停止部署，先修复基础问题。

### Terraform使用的10条重要原则

1. **必须使用带有锁定机制的远程状态存储后端**。
2. **严禁硬编码秘密信息——无论是代码中还是状态数据中，只要可以避免就避免这样做**。
3. **每个部署计划都必须经过仔细审核**——仅应用经过审核的计划。
4. **模块应被视为“契约”——为每个模块设置版本号，进行测试，并编写相应的文档。
5. **环境应相互隔离**——理想情况下，每个环境都有独立的状态数据和访问权限。
6. **优先使用`for_each`循环而非`count`循环**——这有助于确保资源地址的稳定性。
7. **CI/CD流程应自动执行部署操作**——严禁在生产环境中直接执行`terraform apply`命令。
8. **为所有资源设置标签**——以便进行成本分配、明确资源的所有权和生命周期管理。
9. **必须及时检测状态数据漂移**——每周进行检测，并立即处理异常情况。
10. **升级操作必须谨慎进行**——在开发环境中进行测试，阅读官方变更日志，并在部署前锁定相关配置。

### 10个常见的错误

| 错误类型 | 影响 | 应对措施 |
|---------|--------|-----|
| 在团队项目中使用本地状态数据 | 可能导致状态数据冲突或数据丢失 | 必须使用远程状态存储后端。 |
| 将秘密信息硬编码到`.tfvars`文件中并提交到版本控制系统中 | 会导致凭证泄露 | 应使用密钥库或SSM等工具进行管理。 |
| 对非必要资源使用`count`循环 | 可能导致索引冲突 | 应优先使用`for_each`循环并根据条件进行判断。 |
| 使用单一的状态文件 | 会导致测试效率低下 | 应将状态数据按组件（如网络、计算等）分开存储。 |
| 未为关键资源启用`prevent_destroy`保护机制 | 可能导致数据丢失 | 必须为关键资源启用`prevent_destroy`保护机制。 |
| 在生产环境中直接使用`terraform apply -auto-approve`命令 | 可能导致未经审核的配置变更被应用 | 必须先进行人工审核，再执行部署。 |
| 将开发环境中的工作目录视为独立的环境 | 可能导致状态数据在多个环境中共享 | 应为每个环境创建独立的目录和存储后端。 |
| 未在CI过程中进行成本估算 | 可能导致意外的高额费用 | 必须在每次提交代码时进行成本估算。 |
| 临时性的手动修改 | 可能导致永久性的状态数据漂移 | 所有修改都应通过正式的流程进行处理。 |

---

## 常用的命令操作

- “Review this Terraform code”：执行第1阶段的健康检查及静态分析建议。
- “Design infrastructure for [服务名称]”：执行第2阶段的代码结构设计和第4阶段的模块设计。
- “Set up remote state”：执行第3阶段的远程状态存储后端配置。
- “Create a module for [资源名称]”：根据需求创建模块，并设置相应的输入参数和输出结果。
- “Compare environments”：执行第5阶段的环境配置对比。
- “Security audit my Terraform”：执行第6阶段的安全性检查。
- “Add tests to this module”：为模块添加测试用例。
- “Set up CI/CD for Terraform”：配置CI/CD流程。
- “Check for drift”：执行第10阶段的漂移检测。
- “Estimate infrastructure costs”：执行第11阶段的成本估算。
- “Migrate state to new backend”：执行第13阶段的资源迁移操作。
- “Score this Terraform project”：执行第14阶段的全面质量评估。

---

## ⚡ 进阶内容

本文档介绍了Terraform的最佳实践和配置方法。针对特定行业的基础设施需求，还可以参考以下附加资源：

- **SaaS基础设施**：[AfrexAI SaaS Context Pack（价格：47美元）](https://afrexai-cto.github.io/context-packs/)
- **金融行业合规性基础设施**：[AfrexAI Fintech Context Pack（价格：47美元）](https://afrexai-cto.github.io/context-packs/)
- **医疗行业HIPAA合规性基础设施**：[AfrexAI Healthcare Context Pack（价格：47美元）](https://afrexai-cto.github.io/context-packs/)

## 🔗 AfrexAI提供的其他免费工具

- `clawhub install afrexai-devops-engine`：用于完整的DevOps和平台工程管理。
- `clawhub install afrexai-cybersecurity-engine`：用于安全加固和合规性管理。
- `clawhub install afrexai-system-architect`：用于系统架构设计。
- `clawhub install afrexai-api-architect`：用于API设计和生命周期管理。
- `clawhub install afrexai-cicd-engineering`：用于CI/CD流程的自动化配置。

查看AfrexAI提供的所有工具：[clawhub.com](https://clawhub.com) → 搜索“afrexai”

购买相关工具：[afrexai-cto.github.io/context-packs](https://afrexai-cto.github.io/context-packs/)