---
name: "senior-devops"
description: 全面的 DevOps 技能，涵盖持续集成/持续交付（CI/CD）、基础设施自动化、容器化以及云平台（AWS、GCP、Azure）的相关内容。包括管道设置、基础设施即代码（Infrastructure as Code）的理念、部署自动化以及监控机制。适用于搭建管道、部署应用程序、管理基础设施、实施监控系统或优化部署流程等场景。
---
# 高级 DevOps

这是一套专为高级 DevOps 人员设计的完整工具包，涵盖了现代工具和最佳实践。

## 快速入门

### 主要功能

该技能通过自动化脚本提供了三项核心功能：

```bash
# Script 1: Pipeline Generator — scaffolds CI/CD pipelines for GitHub Actions or CircleCI
python scripts/pipeline_generator.py ./app --platform=github --stages=build,test,deploy

# Script 2: Terraform Scaffolder — generates and validates IaC modules for AWS/GCP/Azure
python scripts/terraform_scaffolder.py ./infra --provider=aws --module=ecs-service --verbose

# Script 3: Deployment Manager — orchestrates container deployments with rollback support
python scripts/deployment_manager.py deploy --env=production --image=app:1.2.3 --strategy=blue-green
```

## 核心功能

### 1. 管道生成器（Pipeline Generator）

为 GitHub Actions 或 CircleCI 生成 CI/CD 管道配置，包括构建、测试、安全扫描和部署等阶段。

**示例 — GitHub Actions 工作流程：**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  build-docker:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build-docker
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service app-service \
            --force-new-deployment
```

**使用方法：**
```bash
python scripts/pipeline_generator.py <project-path> --platform=github|circleci --stages=build,test,deploy
```

### 2. Terraform 模块生成器（Terraform Scaffolder）

生成、验证并规划 Terraform 模块。在应用任何更改之前，会强制执行 `terraform validate` 和 `terraform plan` 操作。

**示例 — AWS ECS 服务模块：**
```hcl
# modules/ecs-service/main.tf
resource "aws_ecs_task_definition" "app" {
  family                   = var.service_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory

  container_definitions = jsonencode([{
    name      = var.service_name
    image     = var.container_image
    essential = true
    portMappings = [{
      containerPort = var.container_port
      protocol      = "tcp"
    }]
    environment = [for k, v in var.env_vars : { name = k, value = v }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/${var.service_name}"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.service_name
    container_port   = var.container_port
  }
}
```

**使用方法：**
```bash
python scripts/terraform_scaffolder.py <target-path> --provider=aws|gcp|azure --module=ecs-service|gke-deployment|aks-service [--verbose]
```

### 3. 部署管理器（Deployment Manager）

支持蓝绿部署（blue/green deployment）或滚动部署（rolling deployment）策略，具备健康检查机制，并在失败时自动回滚。

**示例 — Kubernetes 蓝绿部署（特定于蓝色环境的配置元素）：**
```yaml
# k8s/deployment-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    slot: blue      # slot label distinguishes blue from green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      slot: blue
  template:
    metadata:
      labels:
        app: myapp
        slot: blue
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:1.2.3
          readinessProbe:       # gate: pod must pass before traffic switches
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

**使用方法：**
```bash
python scripts/deployment_manager.py deploy \
  --env=staging|production \
  --image=app:1.2.3 \
  --strategy=blue-green|rolling \
  --health-check-url=https://app.example.com/healthz

python scripts/deployment_manager.py rollback --env=production --to-version=1.2.2
python scripts/deployment_manager.py --analyze --env=production   # audit current state
```

## 资源

- 模式参考：`references/cicd_pipeline_guide.md` — 详细的 CI/CD 模式、最佳实践及反模式
- 工作流程指南：`references/infrastructure_as_code.md` — 基于代码的基础设施（IaC）的逐步操作流程、优化方法及故障排除技巧
- 技术指南：`references/deployment_strategies.md` — 部署策略配置、安全考虑因素及可扩展性指南
- 工具脚本：`scripts/` 目录

## 开发工作流程

### 1. 基础设施变更（Terraform）

```bash
# Scaffold or update module
python scripts/terraform_scaffolder.py ./infra --provider=aws --module=ecs-service --verbose

# Validate and plan — review diff before applying
terraform -chdir=infra init
terraform -chdir=infra validate
terraform -chdir=infra plan -out=tfplan

# Apply only after plan review
terraform -chdir=infra apply tfplan

# Verify resources are healthy
aws ecs describe-services --cluster production --services app-service \
  --query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount}'
```

### 2. 应用程序部署

```bash
# Generate or update pipeline config
python scripts/pipeline_generator.py . --platform=github --stages=build,test,security,deploy

# Build and tag image
docker build -t ghcr.io/org/app:$(git rev-parse --short HEAD) .
docker push ghcr.io/org/app:$(git rev-parse --short HEAD)

# Deploy with health-check gate
python scripts/deployment_manager.py deploy \
  --env=production \
  --image=app:$(git rev-parse --short HEAD) \
  --strategy=blue-green \
  --health-check-url=https://app.example.com/healthz

# Verify pods are running
kubectl get pods -n production -l app=myapp
kubectl rollout status deployment/app-blue -n production

# Switch traffic after verification
kubectl patch service app-svc -n production \
  -p '{"spec":{"selector":{"slot":"blue"}}}'
```

### 3. 回滚流程

**请参阅 `references/deployment_strategies.md` 中的全面故障排除指南。**