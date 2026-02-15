---
name: docker-containerization
description: 此技能适用于使用 Docker 对应用程序进行容器化处理、创建 Dockerfile、编写 docker-compose 配置文件，或将容器部署到各种平台。特别适合 Next.js、React、Node.js 等需要容器化支持的开发、生产环境或持续集成/持续交付（CI/CD）流程的应用程序。当用户需要 Docker 配置、多阶段构建、容器编排，或者将容器部署到 Kubernetes、ECS、Cloud Run 等平台时，可优先使用此技能。
---

# Docker容器化技能

## 概述

本技能专注于为现代Web应用程序（尤其是Next.js和Node.js项目）生成适用于生产环境的Docker配置。包括Dockerfile、docker-compose设置、用于容器管理的bash脚本，以及针对多种编排平台的全面部署指南。

## 核心能力

### 1. Dockerfile生成

为不同环境生成优化的Dockerfile：

- **生产环境**（`assets/Dockerfile.production`）：
  - 多阶段构建，可将镜像大小减少85%
  - 基于Alpine Linux（最终镜像大小约180MB）
  - 以非root用户身份运行，确保安全性
  - 包含健康检查机制和资源限制

- **开发环境**（`assets/Dockerfile.development`）：
  - 支持热重载
  - 包含所有开发依赖项
  - 支持通过卷挂载实时更新代码

- **Nginx静态服务**（`assets/Dockerfile.nginx`）：
  - 优化静态资源输出
  - 集成Nginx反向代理
  - 镜像体积最小化

### 2. Docker Compose配置

使用`assets/docker-compose.yml`进行多容器编排：
- 管理开发环境和生产环境的服务
- 网络和卷管理
- 实施健康检查与日志记录
- 定义容器重启策略

### 3. 容器管理的bash脚本

- `docker-build.sh`：具有丰富选项的镜像构建脚本
- `docker-run.sh`：以完整配置运行容器
- `docker-push.sh`：将容器推送到注册中心（Docker Hub、ECR、GCR、ACR）
- `docker-cleanup.sh`：清理磁盘空间

### 4. 配置文件

- `.dockerignore`：排除不必要的文件（如node_modules、.git、日志文件）
- `nginx.conf`：适用于生产环境的Nginx配置文件，包含压缩、缓存和安全设置

### 5. 参考文档

- `docker-best-practices.md`：
  - 介绍多阶段构建方法
  - 镜像优化技巧（减少85%的镜像大小）
  - 安全最佳实践（使用非root用户、进行漏洞扫描）
  - 性能优化方法
  - 健康检查与日志记录方案
  - 故障排除指南

- `container-orchestration.md`：
  - 提供针对以下平台的部署指南：
    - Docker Compose（本地开发）
    - Kubernetes（支持自动扩展的企业级部署）
    - Amazon ECS（AWS原生编排）
    - Google Cloud Run（无服务器容器）
    - Azure Container Instances
    - Digital Ocean App Platform
  - 包含配置示例、命令、自动扩展设置和监控方案

## 工作流程决策树

### 1. 选择何种环境？
- **开发环境** → 使用`Dockerfile.development`（支持热重载和所有依赖项）
- **生产环境** → 使用`Dockerfile.production`（精简且安全）
- **静态服务** → 使用`Dockerfile.nginx`（镜像体积最小）

### 2. 使用单个容器还是多个容器？
- **单个容器** → 仅生成Dockerfile
- **多个容器** → 生成`docker-compose.yml`（包含应用程序和数据库）

### 3. 选择哪个注册中心？
- **Docker Hub** → `docker.io/username/image`
- **AWS ECR** → `123456789012.dkr.ecr.region.amazonaws.com/image`
- **Google GCR** → `gcr.io/project-id/image`
- **Azure ACR** → `registry.azurecr.io/image`

### 4. 选择部署平台？
- **Kubernetes** → 参考`container-orchestration.md`中的Kubernetes部分
- **ECS** → 参考ECS任务定义示例
- **Cloud Run** → 参考相应的部署命令
- **Docker Compose** → 使用提供的`docker-compose.yml`文件

### 5. 是否需要优化？
- **镜像大小** → 使用多阶段构建和Alpine Linux基底
- **构建速度** → 优化层缓存和BuildKit
- **安全性** → 以非root用户身份运行并扫描漏洞
- **性能** → 设置资源限制和健康检查

## 使用示例

### 示例1：为生产环境容器化Next.js应用程序

**用户**：“将我的Next.js应用程序容器化以适应生产环境”

**步骤**：
1. 将`assets/Dockerfile.production`复制到项目根目录，并命名为`Dockerfile`
2. 将`assets/.dockerignore`复制到项目根目录
3. 构建镜像：`./docker-build.sh -e prod -n my-app -t v1.0.0`
4. 测试：`./docker-run.sh -i my-app -t v1.0.0 -p 3000:3000 -d`
5. 推送镜像：`./docker-push.sh -n my-app -t v1.0.0 --repo username/my-app`

### 示例2：使用Docker Compose进行开发

**用户**：“为本地开发环境设置Docker Compose”

**步骤**：
1. 将`assets/Dockerfile.development`和`assets/docker-compose.yml`复制到项目目录
2. 在`docker-compose.yml`中自定义服务配置
3. 启动容器：`docker-compose up -d`
4. 查看日志：`docker-compose logs -f app-dev`

### 示例3：将应用程序部署到Kubernetes

**用户**：“将容器化应用程序部署到Kubernetes”

**步骤**：
1. 构建镜像并将其推送到注册中心
2. 查阅`container-orchestration.md`中的Kubernetes相关内容
3. 创建Kubernetes配置文件（deployment、service、ingress）
4. 应用配置：`kubectl apply -f deployment.yaml`
5. 验证部署结果：`kubectl get pods && kubectl logs -f deployment/app`

### 示例4：将应用程序部署到AWS ECS

**用户**：“将应用程序部署到AWS ECS Fargate**

**步骤**：
1. 构建镜像并将其推送到ECR
2. 查阅`container-orchestration.md`中的ECS相关内容
3. 创建任务定义文件（JSON格式）
4. 注册任务定义：`aws ecs register-task-definition --cli-input-json file://task-def.json`
5. 创建服务：`aws ecs create-service --cluster my-cluster --service-name app --desired-count 3`

## 最佳实践

### 安全性
- **生产环境**：使用多阶段构建
- **以非root用户身份运行容器**
- **使用特定的镜像标签（而非`latest`）**
- **定期扫描应用程序中的漏洞**
- **避免硬编码敏感信息**
- **实施健康检查机制**

### 性能优化
- **优化层缓存顺序**
- **使用Alpine Linux镜像（镜像体积通常较小）**
- **启用BuildKit以加速构建过程**
- **设置合理的资源限制**
- **使用压缩技术**

### 可维护性
- **为复杂步骤添加注释**
- **使用构建参数以增加灵活性**
- **保持Dockerfile的简洁性**
- **对所有配置文件进行版本控制**
- **详细记录环境变量设置**

## 故障排除

- **镜像过大（>500MB）**：使用多阶段构建和Alpine Linux基底
- **构建速度缓慢**：优化层缓存和BuildKit配置
- **容器立即退出**：检查日志文件（`docker logs container-name`），确认CMD/ENTRYPOINT设置是否正确，检查端口冲突
- **更改未生效**：清除缓存后重新构建，检查`.dockerignore`文件和卷挂载设置

## 快速参考

### 与CI/CD工具的集成

- **GitHub Actions**：[相关集成方案](___CODE_BLOCK_5_)
- **GitLab CI**：[相关集成方案](```yaml
build:
  script:
    - chmod +x docker-build.sh
    - ./docker-build.sh -e prod -t $CI_COMMIT_SHA
```

## 资源

- **脚本文件夹（`scripts/`）**：包含适用于生产环境的bash脚本：
  - `docker-build.sh`：用于构建镜像（400多行代码，支持彩色输出）
  - `docker-run.sh`：用于运行容器（400多行代码，具备自动冲突解决功能）
  - `docker-push.sh`：用于将镜像推送到多个注册中心
  - `docker-cleanup.sh`：用于清理资源（支持干运行模式和选择性清理）

- **参考文档（`references/`）**：根据需要查阅详细文档：
  - `docker-best-practices.md`：全面的Docker最佳实践指南（约500行）
  - `container-orchestration.md`：针对6种以上平台的部署指南（约600行）

- **资源文件（`assets/`）**：提供可直接使用的模板：
  - `Dockerfile.production`：适用于生产环境的Dockerfile
  - `Dockerfile.development`：适用于开发环境的Dockerfile
  - `Dockerfile.nginx`：用于Nginx静态服务的Dockerfile
  - `docker-compose.yml`：用于多容器编排的配置文件
  - `.dockerignore`：优化后的文件排除规则
  - `nginx.conf`：适用于生产环境的Nginx配置文件