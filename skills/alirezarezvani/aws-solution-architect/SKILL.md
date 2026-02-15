---
name: aws-solution-architect
description: 为初创公司设计基于无服务器架构（serverless）和基础设施即代码（Infrastructure as Code, IaC）模板的AWS解决方案。具体工作内容包括：根据需求设计无服务器架构、创建CloudFormation模板、优化AWS成本、搭建持续集成/持续部署（CI/CD）流程，以及协助企业迁移到AWS平台。涉及的技术服务包括Lambda函数、API Gateway、DynamoDB、ECS（Elastic Container Service）、Aurora数据库等，同时提供成本优化方面的专业建议。
---

# AWS解决方案架构师

为初创企业提供可扩展且成本效益高的AWS架构设计，使用基础设施即代码（Infrastructure as Code, IaC）模板。

---

## 目录

- [相关术语](#trigger-terms)
- [工作流程](#workflow)
- [工具](#tools)
- [快速入门](#quick-start)
- [输入要求](#input-requirements)
- [输出格式](#output-formats)

---

## 相关术语

在遇到以下情况时使用此技能：

| 类别 | 术语 |
|----------|-------|
| **架构设计** | 无服务器架构（serverless architecture）、AWS架构、云设计、微服务（microservices）、三层架构（three-tier） |
| **基础设施即代码生成** | CloudFormation、CDK、Terraform、基础设施即代码（Infrastructure as Code）、部署模板（deploy template） |
| **无服务器架构** | Lambda、API Gateway、DynamoDB、Step Functions、EventBridge、AppSync |
| **容器** | ECS（Elastic Container Service）、Fargate、EKS（Elastic Kubernetes Service）、容器编排（container orchestration）、AWS上的Docker |
| **成本优化** | 降低AWS成本、优化支出、合理配置资源（right-sizing）、节省计划（Savings Plans） |
| **数据库** | Aurora、RDS（Relational Database Service）、DynamoDB设计、数据库迁移（database migration）、数据建模（data modeling） |
| **安全性** | IAM（Identity and Access Management）策略、VPC（Virtual Private Cloud）设计、加密（encryption）、Cognito、WAF（Web Application Firewall） |
| **持续集成/持续部署** | CodePipeline、CodeBuild、CodeDeploy、GitHub Actions for AWS |
| **监控** | CloudWatch、X-Ray、可观测性（observability）、警报（alarms）、仪表板（dashboards） |
| **迁移** | 迁移到AWS、迁移策略（migration strategies，如“lift and shift”或“replatform”） |

---

## 工作流程

### 第1步：收集需求

收集应用程序的详细规范：

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
```

### 第2步：设计架构

运行架构设计工具以获取设计建议：

```bash
python scripts/architecture_designer.py --input requirements.json
```

从推荐的设计模式中选择：
- **无服务器Web架构**：S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **事件驱动型微服务**：EventBridge + Lambda + SQS（Simple Queue Service）+ Step Functions
- **三层架构**：ALB（Application Load Balancer）+ ECS Fargate + Aurora + ElastiCache
- **GraphQL后端**：AppSync + Lambda + DynamoDB + Cognito

详细的设计模式规范请参阅 `references/architecture_patterns.md`。

### 第3步：生成基础设施即代码模板

为选定的架构模式创建相应的基础设施即代码模板：

```bash
# Serverless stack (CloudFormation)
python scripts/serverless_stack.py --app-name my-app --region us-east-1

# Output: CloudFormation YAML template ready to deploy
```

### 第4步：审查成本

分析预估成本及优化方案：

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

输出内容包括：
- 各服务的月度成本明细
- 资源配置优化建议
- 可能的月度成本节省方案

### 第5步：部署

部署生成的基础设施：

```bash
# CloudFormation
aws cloudformation create-stack \
  --stack-name my-app-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# CDK
cdk deploy

# Terraform
terraform init && terraform apply
```

### 第6步：验证

验证部署结果并设置监控机制：

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name my-app-stack

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name high-errors ...
```

---

## 工具

### architecture_designer.py

根据需求生成架构设计方案。

**输入：** 包含应用程序类型、规模、预算和合规性要求的JSON数据
**输出：** 推荐的设计模式、服务栈（service stack）、成本估算、优缺点分析

### serverless_stack.py

创建用于无服务器架构的CloudFormation模板。

**输出：** 可用于生产环境的CloudFormation YAML文件，包含：
- API Gateway + Lambda
- DynamoDB数据库
- Cognito用户池
- 最小权限的IAM角色
- CloudWatch日志记录功能

### costOptimizer.py

分析成本并提供建议的优化方案。

**输出：** 关于以下方面的优化建议：
- 闲置资源的清理
- 服务器实例的合理配置
- 预留容量的购买
- 存储级别的调整
- NAT Gateway的替代方案

---

## 快速入门

### 最小可行产品（MVP）架构（每月成本<100美元）

```
Ask: "Design a serverless MVP backend for a mobile app with 1000 users"

Result:
- Lambda + API Gateway for API
- DynamoDB pay-per-request for data
- Cognito for authentication
- S3 + CloudFront for static assets
- Estimated: $20-50/month
```

### 扩展架构（每月成本500-2000美元）

```
Ask: "Design a scalable architecture for a SaaS platform with 50k users"

Result:
- ECS Fargate for containerized API
- Aurora Serverless for relational data
- ElastiCache for session caching
- CloudFront for CDN
- CodePipeline for CI/CD
- Multi-AZ deployment
```

### 成本优化

```
Ask: "Optimize my AWS setup to reduce costs by 30%. Current spend: $3000/month"

Provide: Current resource inventory (EC2, RDS, S3, etc.)

Result:
- Idle resource identification
- Right-sizing recommendations
- Savings Plans analysis
- Storage lifecycle policies
- Target savings: $900/month
```

### 基础设施即代码生成

```
Ask: "Generate CloudFormation for a three-tier web app with auto-scaling"

Result:
- VPC with public/private subnets
- ALB with HTTPS
- ECS Fargate with auto-scaling
- Aurora with read replicas
- Security groups and IAM roles
```

---

## 输入要求

为架构设计提供以下详细信息：

| 需求 | 描述 | 例子 |
|-------------|-------------|---------|
| 应用程序类型 | 开发内容 | SaaS平台、移动应用后端 |
| 预计规模 | 用户数量/每秒请求数 | 1万用户，100 RPS（Requests Per Second） |
| 预算 | 每月AWS费用上限 | 最高500美元 |
| 团队情况 | 团队规模、AWS使用经验 | 3名开发人员，中级水平 |
| 合规性要求 | 法规遵从性 | HIPAA、GDPR、SOC 2 |
| 可用性要求 | 运行时间保证 | 99.9%的SLA（Service Level Agreement），1小时的RPO（Recovery Point Objective） |

**JSON格式：**

```json
{
  "application_type": "saas_platform",
  "expected_users": 10000,
  "requests_per_second": 100,
  "budget_monthly_usd": 500,
  "team_size": 3,
  "aws_experience": "intermediate",
  "compliance": ["SOC2"],
  "availability_sla": "99.9%"
}
```

---

## 输出格式

### 架构设计

- 建议的设计模式及理由
- 服务栈图（ASCII格式）
- 配置规范
- 月度成本估算
- 扩展特性
- 权衡因素与限制

### 基础设施即代码模板

- **CloudFormation YAML**：可用于生产的SAM（Serverless Application Model）/CFN（CloudFormation）模板
- **CDK TypeScript**：类型安全的基础设施代码
- **Terraform HCL**：支持多云环境的配置文件

### 成本分析

- 当前成本结构
- 成本优化建议及节省方案
- 优先行动事项列表（高/中/低优先级）
- 实施检查清单

---

## 参考文档

| 文档 | 内容 |
|----------|----------|
| `references/architecture_patterns.md` | 6种架构设计模式：无服务器架构、微服务、三层架构、数据处理、GraphQL、多区域部署 |
| `references/service_selection.md` | 计算资源、数据库、存储解决方案的选择指南 |
| `references/best_practices.md | 无服务器架构设计、成本优化、安全加固、可扩展性最佳实践 |

---

## 限制因素

- Lambda函数执行时间最长为15分钟，内存最大为10GB |
- API Gateway的请求超时时间为29秒，允许的请求负载大小为10MB |
- DynamoDB的单条数据记录最大大小为400KB，默认采用最终一致性（eventually consistent）存储方式 |
- 不同服务的区域可用性可能有所不同 |
- 部分服务存在特定的AWS使用限制（AWS-specific lock-ins）