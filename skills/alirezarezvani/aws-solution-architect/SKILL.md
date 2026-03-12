---
name: "aws-solution-architect"
description: 为初创公司设计基于无服务器（serverless）模式和基础设施即代码（Infrastructure as Code, IaC）模板的AWS架构。当需要设计无服务器架构、创建CloudFormation模板、优化AWS成本、设置持续集成/持续部署（CI/CD）流程或迁移至AWS时，可参考本指南。内容涵盖Lambda函数、API Gateway、DynamoDB、ECS、Aurora数据库以及成本优化等方面的知识。
---
# AWS解决方案架构师

为初创企业提供可扩展且成本效益高的AWS架构设计，使用基础设施即代码（Infrastructure as Code, IaC）模板。

---

## 工作流程

### 第1步：收集需求

收集应用程序的详细规格：

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
```

### 第2步：设计架构

运行架构设计工具以获取模式建议：

```bash
python scripts/architecture_designer.py --input requirements.json
```

**示例输出：**

```json
{
  "recommended_pattern": "serverless_web",
  "service_stack": ["S3", "CloudFront", "API Gateway", "Lambda", "DynamoDB", "Cognito"],
  "estimated_monthly_cost_usd": 35,
  "pros": ["Low ops overhead", "Pay-per-use", "Auto-scaling"],
  "cons": ["Cold starts", "15-min Lambda limit", "Eventual consistency"]
}
```

从推荐的模式中选择一种：
- **无服务器架构（Serverless）**：S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **事件驱动型微服务（Event-Driven Microservices）**：EventBridge + Lambda + SQS + Step Functions
- **三层架构（Three-Tier）**：ALB + ECS Fargate + Aurora + ElastiCache
- **GraphQL后端（GraphQL Backend）**：AppSync + Lambda + DynamoDB + Cognito

有关详细模式规格，请参阅 `references/architecture_patterns.md`。

**验证步骤：** 在进入第3步之前，确认所选模式符合团队的运营成熟度和合规性要求。

### 第3步：生成基础设施即代码模板

为选定的模式创建基础设施即代码模板：

```bash
# Serverless stack (CloudFormation)
python scripts/serverless_stack.py --app-name my-app --region us-east-1
```

**示例CloudFormation YAML输出（无服务器架构核心资源）：**

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Parameters:
  AppName:
    Type: String
    Default: my-app

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs20.x
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          TABLE_NAME: !Ref DataTable
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY

  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
```

> 完整的模板（包括API Gateway、Cognito、IAM角色和CloudWatch日志）由 `serverless_stack.py` 生成，也可在 `references/architecture_patterns.md` 中找到。

**示例CDK TypeScript代码片段（三层架构模式）：**

```typescript
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

const vpc = new ec2.Vpc(this, 'AppVpc', { maxAzs: 2 });

const cluster = new ecs.Cluster(this, 'AppCluster', { vpc });

const db = new rds.ServerlessCluster(this, 'AppDb', {
  engine: rds.DatabaseClusterEngine.auroraPostgres({
    version: rds.AuroraPostgresEngineVersion.VER_15_2,
  }),
  vpc,
  scaling: { minCapacity: 0.5, maxCapacity: 4 },
});
```

### 第4步：审查成本

分析预估成本及优化方案：

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

**示例输出：**

```json
{
  "current_monthly_usd": 2000,
  "recommendations": [
    { "action": "Right-size RDS db.r5.2xlarge → db.r5.large", "savings_usd": 420, "priority": "high" },
    { "action": "Purchase 1-yr Compute Savings Plan at 40% utilization", "savings_usd": 310, "priority": "high" },
    { "action": "Move S3 objects >90 days to Glacier Instant Retrieval", "savings_usd": 85, "priority": "medium" }
  ],
  "total_potential_savings_usd": 815
}
```

输出内容包括：
- 各服务的月度成本明细
- 资源优化建议
- 节省成本的机会
- 潜在的月度节省金额

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

### 第6步：验证并处理故障

验证部署结果并设置监控：

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name my-app-stack

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name high-errors ...
```

**如果堆栈创建失败：**

1. 检查失败原因：
   ```bash
   aws cloudformation describe-stack-events \
     --stack-name my-app-stack \
     --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'
   ```
2. 查看CloudWatch日志以查找Lambda或ECS的错误。
3. 修复模板或资源配置。
4. 在重试之前删除失败的堆栈：
   ```bash
   aws cloudformation delete-stack --stack-name my-app-stack
   # Wait for deletion
   aws cloudformation wait stack-delete-complete --stack-name my-app-stack
   # Redeploy
   aws cloudformation create-stack ...
   ```

**常见故障原因：**
- IAM权限错误 → 检查 `--capabilities CAPABILITY_IAM` 和角色信任策略
- 资源限制超出 → 通过服务配额控制台申请增加配额
- 模板语法无效 → 在部署前运行 `aws cloudformation validate-template --template-body file://template.yaml`

---

## 工具

### architecture_designer.py

根据需求生成架构模式。

```bash
python scripts/architecture_designer.py --input requirements.json --output design.json
```

**输入：** 包含应用程序类型、规模、预算和合规性要求的JSON数据
**输出：** 推荐的模式、服务堆栈、成本估算以及优缺点

### serverless_stack.py

生成用于无服务器架构的CloudFormation模板。

```bash
python scripts/serverless_stack.py --app-name my-app --region us-east-1
```

**输出：** 可用于生产的CloudFormation YAML文件，包含：
- API Gateway + Lambda
- DynamoDB表
- 最小权限的IAM角色
- CloudWatch日志功能

### costOptimizer.py

分析成本并提供建议的优化方案。

```bash
python scripts/cost_optimizer.py --resources inventory.json --monthly-spend 5000
```

**输出：** 关于以下方面的优化建议：
- 移除闲置资源
- 调整实例配置
- 购买预留容量
- 更改存储层级
- 选择其他NAT Gateway选项

---

## 快速入门

### 最小可行产品（MVP）架构（每月成本< $100）

```
Ask: "Design a serverless MVP backend for a mobile app with 1000 users"

Result:
- Lambda + API Gateway for API
- DynamoDB pay-per-request for data
- Cognito for authentication
- S3 + CloudFront for static assets
- Estimated: $20-50/month
```

### 扩展架构（每月成本$500-2000）

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

请提供以下详细信息以进行架构设计：

| 需求 | 描述 | 示例 |
|-------------|-------------|---------|
| 应用程序类型 | 开发内容 | SaaS平台、移动后端 |
| 预期规模 | 用户数量/每秒请求数 | 10,000名用户，100 RPS |
| 预算 | 每月AWS费用上限 | 最高$500 |
| 团队背景 | 团队规模及AWS使用经验 | 3名开发人员，中级水平 |
| 合规性 | 需遵守的法规 | HIPAA、GDPR、SOC 2 |
| 可用性 | 运行时间要求 | 99.9%的SLA，1小时的RPO |

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

- 带有理由的模式推荐
- 服务堆栈图（ASCII格式）
- 每月成本估算及权衡因素

### 基础设施即代码模板

- **CloudFormation YAML**：可用于生产的SAM/CFN模板
- **CDK TypeScript**：类型安全的基础设施代码
- **Terraform HCL**：支持多云环境的配置文件

### 成本分析

- 当前成本明细及优化建议
- 优先行动事项列表（高/中/低）及实施检查清单

---

## 参考文档

| 文档 | 内容 |
|----------|----------|
| `references/architecture_patterns.md` | 6种架构模式：无服务器架构、微服务、三层架构、数据处理、GraphQL、多区域部署 |
| `references/service_selection.md` | 计算、数据库、存储和消息传递服务的选择指南 |
| `references/best_practices.md | 无服务器架构设计、成本优化、安全加固和可扩展性最佳实践 |