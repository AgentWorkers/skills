---
name: AWS | Amazon Web Services
slug: aws
version: 1.0.2
homepage: https://clawic.com/skills/aws
description: 负责设计、部署和优化 AWS 基础设施，以避免成本激增和安全漏洞。
changelog: Complete rewrite with cost traps, security hardening, service selection
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["aws"]},"install":[{"id":"brew","kind":"brew","formula":"awscli","bins":["aws"],"label":"Install AWS CLI (Homebrew)"}],"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解集成选项。该工具可立即使用，但设置过程（用于个性化配置）是可选的。

## 使用场景

当用户需要 AWS 基础设施相关指导时，可以使用该工具。该工具可协助制定架构方案、选择服务、优化成本、加强安全性以及配置部署模式。

## 架构

内存数据存储在 `~/aws/` 目录下。具体结构请参阅 `memory-template.md`。

```
~/aws/
├── memory.md        # Account context + preferences
├── resources.md     # Active infrastructure inventory
└── costs.md         # Cost tracking + alerts
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 服务模式 | `services.md` |
| 成本优化 | `costs.md` |
| 安全性强化 | `security.md` |

## 核心规则

### 1. 首先验证账户信息
在进行任何操作之前，请确认以下信息：
- 区域（默认为 us-east-1，但可另行指定）
- 账户类型（个人/初创企业/企业）
- 现有的基础设施（VPC、子网、安全组）

```bash
aws sts get-caller-identity
aws ec2 describe-vpcs --query 'Vpcs[].{ID:VpcId,CIDR:CidrBlock,Default:IsDefault}'
```

### 2. 以成本为导向的架构设计
所有建议都会考虑成本影响：

| 阶段 | 推荐的架构方案 | 月成本 |
|-------|-------------------|--------------|
| MVP 阶段（<1,000 名用户） | 单个 EC2 + RDS | 约 50 美元 |
| 成长阶段（1,000–10,000 名用户） | ALB + ASG + 多 AZ 的 RDS | 约 200 美元 |
| 扩展阶段（10,000 名用户以上） | ECS/EKS + Aurora + ElastiCache | 约 500 美元以上 |

**建议使用最小规模的可用实例。** 扩容容易，但缩减规模可能会导致资源浪费。

### 3. 默认采用安全策略
所有资源都遵循以下安全原则：
- 最小权限原则（IAM）
- 数据存储加密（使用 KMS 的默认密钥）
- VPC 隔离（数据库不使用公共子网）
- 安全组配置为“拒绝所有”入站流量

### 4. 代码化基础设施管理
使用 Terraform 或 CloudFormation 来生成可复制的基础设施配置文件：
```bash
# Prefer Terraform for multi-cloud portability
terraform init && terraform plan
```
切勿仅依赖控制台进行配置更改。

### 5. 标签管理
为所有资源添加标签以便进行成本分配：
```bash
--tags Key=Environment,Value=prod Key=Project,Value=myapp Key=Owner,Value=team
```

### 6. 从第一天开始进行监控
为基础设施配置 CloudWatch 警报：
- 账费提醒
- CPU/内存使用阈值
- 错误率异常情况

## 成本陷阱

**NAT 网关的数据处理费用（0.045 美元/GB）：**
对于 S3/DynamoDB，VPC 端点是免费的。但如果应用程序负载较高，仅 NAT 网关的费用每月就可能达到 500 美元。
```bash
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx \
  --service-name com.amazonaws.us-east-1.s3 --route-table-ids rtb-xxx
```

**EBS 快照会永久保存：**
自动备份会生成无法删除的快照。请设置合理的生命周期策略。
```bash
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[?StartTime<=`2024-01-01`].[SnapshotId,StartTime,VolumeSize]'
```

**CloudWatch 日志默认会永久保存：**
```bash
aws logs put-retention-policy --log-group-name /aws/lambda/fn --retention-in-days 14
```

**闲置的负载均衡器每月至少会产生 16 美元的费用：**
即使没有流量，ALB 也会产生费用。请及时删除未使用的负载均衡器。

**跨 AZ 的数据传输费用为 0.01 美元/GB：**
跨 AZ 的微服务之间的数据传输费用较高。尽可能将相关服务部署在同一 AZ 中。

## 安全陷阱

**S3 存储桶的策略会覆盖 ACL 设置：**
控制台可能显示 ACL 为“私有”，但实际上桶的策略可能会暴露所有数据。
```bash
aws s3api get-bucket-policy --bucket my-bucket 2>/dev/null || echo "No policy"
aws s3api get-public-access-block --bucket my-bucket
```

**默认情况下，VPC 安全组允许所有出站流量：**
攻击者可能通过出站流量进行数据泄露。请限制出站流量。

**同时具有控制台访问权限和编程访问权限的 IAM 用户：**
代码中的凭证可能会被泄露。请使用角色和临时凭证来管理访问权限。

**RDS 默认情况下允许公共访问：**
请务必检查并调整相关设置：
```bash
aws rds describe-db-instances --query 'DBInstances[].{ID:DBInstanceIdentifier,Public:PubliclyAccessible}'
```

## 性能优化建议

**Lambda 函数的冷启动问题：**
- 对于对延迟敏感的函数，使用预配置的并发数。
- 保持代码包大小较小（解压后不超过 50MB）。
- 在函数处理逻辑之外初始化 SDK 客户端。

**RDS 连接限制：**
| 实例类型 | 最大连接数 |
|----------|-----------------|
| db.t3.micro | 66 |
| db.t3.small | 150 |
| db.t3.medium | 300 |

建议使用 RDS Proxy 来避免连接资源耗尽。

**EBS 卷类型选择：**
| 类型 | 适用场景 | IOPS（每秒输入/输出操作次数） |
|------|----------|------|
| gp3 | 默认类型 | 基础性能 | 3,000 |
| io2 | 适用于数据库 | 最高可达 64,000 |
| st1 | 适用于大数据处理 | 500 MiB/s |

## 服务选择建议

| 需求 | 服务 | 选择理由 |
|------|---------|-----|
| 静态网站 | S3 + CloudFront | 低成本且支持全球 CDN |
| API 后端 | Lambda + API Gateway | 无空闲成本 |
| 容器应用 | ECS Fargate | 无需管理集群 |
| 数据库 | RDS PostgreSQL | 高可用性，支持多 AZ 部署 |
| 缓存 | ElastiCache Redis | 适用于会话缓存，性能优于 DynamoDB |
| 队列 | SQS | 大多数情况下比 SNS 更简单易用 |
| 搜索服务 | OpenSearch | 由 Elasticsearch 提供高效搜索功能 |

## 命令行工具基础

```bash
# Configure credentials
aws configure --profile myproject

# Always specify profile
export AWS_PROFILE=myproject

# Check current identity
aws sts get-caller-identity

# List all regions
aws ec2 describe-regions --query 'Regions[].RegionName'

# Estimate monthly cost
aws ce get-cost-forecast --time-period Start=$(date +%Y-%m-01),End=$(date -v+1m +%Y-%m-01) \
  --metric UNBLENDED_COST --granularity MONTHLY
```

## 安全性与隐私保护

**凭证管理：** 该工具使用 AWS CLI，凭证从 `~/.aws/credentials` 或环境变量中读取。工具不会存储、记录或传输 AWS 凭证信息。

**本地数据存储：** 配置信息和上下文数据存储在 `~/aws/` 目录中，确保数据不会离开用户的设备。

**命令行操作：** 所有命令默认为只读模式。执行删除或终止等破坏性操作前需要用户明确确认。

## 相关工具
如用户需要，可使用以下命令安装相关工具：
- `clawhub install <slug>`：安装基础工具（如 `infrastructure`、`cloud`、`docker`、`backend`）

## 反馈建议
- 如果觉得该工具有用，请给它打星评价（例如：`clawhub star aws`）。
- 保持更新：使用 `clawhub sync` 命令同步最新信息。