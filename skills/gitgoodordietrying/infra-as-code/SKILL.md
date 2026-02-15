---
name: infra-as-code
description: 使用代码来定义和管理云基础设施。这在编写 Terraform、CloudFormation 或 Pulumi 配置文件时非常有用，可以帮助你管理基础设施的状态、规划部署、配置网络/计算/存储资源，以及排查基础设施配置的差异（即基础设施与预期配置之间的不一致）。
metadata: {"clawdbot":{"emoji":"🏗️","requires":{"anyBins":["terraform","aws","pulumi"]},"os":["linux","darwin","win32"]}}
---

# 基础设施即代码（Infrastructure as Code）

通过声明式配置来定义、部署和管理云基础设施。涵盖Terraform（支持多云平台）、AWS CloudFormation和Pulumi（以代码为中心的基础设施管理工具），并提供了针对计算、网络、存储、数据库和状态管理的最佳实践。

## 使用场景

- 设置云基础设施（VPC、EC2实例、Lambda函数、S3存储、RDS数据库等）
- 编写或修改Terraform配置文件
- 管理Terraform的状态数据（远程存储、工作区设置、配置导入等）
- 创建CloudFormation模板
- 使用Pulumi进行TypeScript/Python/Go语言的基础设施管理
- 安全地规划和预览基础设施变更
- 查找声明状态与实际资源之间的差异
- 设置多环境部署（开发环境、测试环境、生产环境）

## Terraform

### 快速入门

```bash
# Install: https://developer.hashicorp.com/terraform/install

# Initialize a project
mkdir infra && cd infra
terraform init

# Core workflow
terraform plan        # Preview changes (safe, read-only)
terraform apply       # Apply changes (creates/modifies resources)
terraform destroy     # Tear down all resources

# Format and validate
terraform fmt -recursive    # Auto-format all .tf files
terraform validate          # Check syntax and config validity
```

### 项目结构

```
infra/
  main.tf              # Primary resources
  variables.tf         # Input variable declarations
  outputs.tf           # Output values
  providers.tf         # Provider configuration
  terraform.tfvars     # Variable values (don't commit secrets)
  backend.tf           # Remote state configuration
  modules/
    vpc/
      main.tf
      variables.tf
      outputs.tf
    compute/
      main.tf
      variables.tf
      outputs.tf
```

### 提供者配置（Provider Configuration）

```hcl
# providers.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
```

### 变量与输出（Variables and Outputs）

```hcl
# variables.tf
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for all resources"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "db_password" {
  type      = string
  sensitive = true
  description = "Database password (pass via TF_VAR_db_password env var)"
}

# outputs.tf
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}

output "api_endpoint" {
  value = aws_lb.api.dns_name
}
```

### VPC与网络配置（VPC + Networking）

```hcl
# Networking module
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true
  tags = { Name = "${var.project_name}-public-${count.index + 1}" }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "${var.project_name}-private-${count.index + 1}" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

### 计算资源管理（Compute Resources: EC2）

```hcl
resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_pair_name

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl start docker
    docker run -d -p 80:8080 ${var.docker_image}
  EOF

  tags = { Name = "${var.project_name}-app" }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-24.04-amd64-server-*"]
  }
}
```

### S3存储与静态网站（S3 Storage + Static Websites）

```hcl
resource "aws_s3_bucket" "website" {
  bucket = "${var.project_name}-website"
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document { suffix = "index.html" }
  error_document { key = "error.html" }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PublicRead"
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.website.arn}/*"
    }]
  })

  depends_on = [aws_s3_bucket_public_access_block.website]
}
```

### RDS数据库（RDS Databases）

```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_security_group" "db" {
  name_prefix = "${var.project_name}-db-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
}

resource "aws_db_instance" "main" {
  identifier        = "${var.project_name}-db"
  engine            = "postgres"
  engine_version    = "16.1"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = 7
  skip_final_snapshot     = var.environment != "prod"
  deletion_protection     = var.environment == "prod"
}
```

### Lambda函数（Lambda Functions）

```hcl
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "api" {
  function_name    = "${var.project_name}-api"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  handler          = "index.handler"
  runtime          = "nodejs20.x"
  timeout          = 30

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      DB_HOST     = aws_db_instance.main.endpoint
      ENVIRONMENT = var.environment
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
```

### 状态管理（State Management）

```hcl
# backend.tf - Remote state in S3
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### 多环境部署模式（Multi-Environment Deployment Patterns）

```hcl
# Use workspaces + tfvars files
# terraform.tfvars (default)
# env/dev.tfvars
# env/staging.tfvars
# env/prod.tfvars

# Apply for specific environment
# terraform apply -var-file=env/prod.tfvars
```

```bash
# Environment-specific apply
ENV=${1:-dev}
terraform workspace select "$ENV" || terraform workspace new "$ENV"
terraform apply -var-file="env/$ENV.tfvars"
```

## AWS CloudFormation

### 模板结构（Template Structure）

```yaml
# cloudformation.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: My application stack

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev
  InstanceType:
    Type: String
    Default: t3.micro

Conditions:
  IsProd: !Equals [!Ref Environment, prod]

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-vpc"

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub "${AWS::StackName}-public"

  AppInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      SubnetId: !Ref PublicSubnet
      ImageId: !FindInMap [RegionAMI, !Ref "AWS::Region", ubuntu]

  Database:
    Type: AWS::RDS::DBInstance
    Condition: IsProd
    DeletionPolicy: Snapshot
    Properties:
      Engine: postgres
      DBInstanceClass: db.t3.micro
      AllocatedStorage: 20
      MasterUsername: admin
      MasterUserPassword: !Ref DBPassword

Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}-VpcId"
  InstanceIP:
    Value: !GetAtt AppInstance.PublicIp
```

### CloudFormation命令行工具（CloudFormation CLI）

```bash
# Validate template
aws cloudformation validate-template --template-body file://cloudformation.yaml

# Create stack
aws cloudformation create-stack \
  --stack-name myapp-dev \
  --template-body file://cloudformation.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_IAM

# Update stack
aws cloudformation update-stack \
  --stack-name myapp-dev \
  --template-body file://cloudformation.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev

# Preview changes (changeset)
aws cloudformation create-change-set \
  --stack-name myapp-dev \
  --change-set-name update-1 \
  --template-body file://cloudformation.yaml

aws cloudformation describe-change-set \
  --stack-name myapp-dev \
  --change-set-name update-1

# Delete stack
aws cloudformation delete-stack --stack-name myapp-dev

# List stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE

# Stack events (debugging)
aws cloudformation describe-stack-events --stack-name myapp-dev | head -50
```

## Pulumi（基于代码的基础设施管理）

### TypeScript语言快速入门（Pulumi with TypeScript）

```bash
# Install: https://www.pulumi.com/docs/install/
pulumi new aws-typescript

# Core workflow
pulumi preview    # Preview changes
pulumi up         # Apply changes
pulumi destroy    # Tear down
pulumi stack ls   # List stacks
```

### TypeScript示例（TypeScript Example）

```typescript
// index.ts
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const environment = config.require("environment");

// VPC
const vpc = new aws.ec2.Vpc("main", {
  cidrBlock: "10.0.0.0/16",
  enableDnsSupport: true,
  enableDnsHostnames: true,
  tags: { Name: `myapp-${environment}-vpc` },
});

// Public subnet
const publicSubnet = new aws.ec2.Subnet("public", {
  vpcId: vpc.id,
  cidrBlock: "10.0.1.0/24",
  mapPublicIpOnLaunch: true,
  tags: { Name: `myapp-${environment}-public` },
});

// S3 bucket
const bucket = new aws.s3.Bucket("data", {
  bucket: `myapp-${environment}-data`,
  versioning: { enabled: true },
});

// Lambda function
const lambdaRole = new aws.iam.Role("lambda-role", {
  assumeRolePolicy: JSON.stringify({
    Version: "2012-10-17",
    Statement: [{
      Action: "sts:AssumeRole",
      Effect: "Allow",
      Principal: { Service: "lambda.amazonaws.com" },
    }],
  }),
});

const lambdaFunc = new aws.lambda.Function("api", {
  runtime: "nodejs20.x",
  handler: "index.handler",
  role: lambdaRole.arn,
  code: new pulumi.asset.FileArchive("./lambda"),
  environment: {
    variables: {
      BUCKET_NAME: bucket.id,
      ENVIRONMENT: environment,
    },
  },
});

// Outputs
export const vpcId = vpc.id;
export const bucketName = bucket.id;
export const lambdaArn = lambdaFunc.arn;
```

### Python示例（Python Example）

```python
# __main__.py
import pulumi
import pulumi_aws as aws

config = pulumi.Config()
environment = config.require("environment")

vpc = aws.ec2.Vpc("main",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": f"myapp-{environment}-vpc"})

bucket = aws.s3.Bucket("data",
    bucket=f"myapp-{environment}-data",
    versioning=aws.s3.BucketVersioningArgs(enabled=True))

pulumi.export("vpc_id", vpc.id)
pulumi.export("bucket_name", bucket.id)
```

### Pulumi的状态管理与资源堆栈（Pulumi State and Resource Stacks）

```bash
# Create per-environment stacks
pulumi stack init dev
pulumi stack init staging
pulumi stack init prod

# Switch stack
pulumi stack select dev

# Set config per stack
pulumi config set environment dev
pulumi config set aws:region us-east-1
pulumi config set --secret dbPassword 'my-secret-pass'

# Stack references (cross-stack)
# In consuming stack:
const infra = new pulumi.StackReference("org/infra/prod");
const vpcId = infra.getOutput("vpcId");
```

## 基础设施调试（Infrastructure Debugging）

### Terraform计划执行问题（Terraform Plan Execution Issues）

```bash
# Detailed plan output
terraform plan -out=plan.tfplan
terraform show plan.tfplan
terraform show -json plan.tfplan | jq '.resource_changes[] | {address, change: .change.actions}'

# Debug mode
TF_LOG=DEBUG terraform plan 2> debug.log

# Check for drift
terraform plan -refresh-only

# Force refresh state
terraform apply -refresh-only
```

### 常见问题与解决方法（Common Issues and Solutions）

```bash
# Resource stuck in "tainted" state
terraform untaint aws_instance.app

# State locked (another apply running or crashed)
terraform force-unlock LOCK_ID

# Provider version conflict
terraform providers lock    # Generate lock file
terraform init -upgrade     # Upgrade providers

# Circular dependency
# Error: "Cycle" in terraform plan
# Fix: use depends_on explicitly, or break the cycle with data sources
```

### 成本估算（Cost Estimation）

```bash
# Infracost (estimates monthly cost from Terraform plans)
# Install: https://www.infracost.io/docs/
infracost breakdown --path .
infracost diff --path . --compare-to infracost-base.json
```

## 使用技巧

- 在执行`terraform apply`之前，务必先运行`terraform plan`命令。仔细阅读计划输出结果，尤其是包含`destroy`或`replace`操作的行。
- 从项目开始就使用远程状态存储机制（remote state）。本地状态文件容易丢失、无法共享，且不具备锁定机制。
- 为所有资源添加标签（至少包括“项目”、“环境”和“管理者”等信息）。标签有助于成本追踪和资源清理。
- 绝不要将敏感信息存储在`.tf`文件或`terraform.tfvars`中，应使用环境变量（如`TF_VAR_NAME`）或专门的密钥管理工具（如Vault）。
- 为具有状态的数据资源（如数据库、包含数据的S3桶）设置`prevent_destroy`生命周期规则，以防意外删除。
- 固定提供者版本（使用`~> 5.0`而非`>= 5.0`），以避免版本升级带来的意外问题。
- 在多环境部署中，建议使用工作区（workspaces）和变量文件（var files）而非重复配置。
- CloudFormation的“变更集”（change sets）相当于Terraform的`terraform plan`功能——在更新资源堆栈前务必先创建变更集。
- 如果Terraform的HCL语法限制了你的开发需求，可以选择使用Pulumi（它支持循环、条件语句和类型检查等功能）。