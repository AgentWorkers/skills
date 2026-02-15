---
name: helm-chart-scaffolding
description: 设计、组织和管理 Helm 图表，以便为 Kubernetes 应用程序提供可重用的配置模板和打包方案。在创建 Helm 图表、打包 Kubernetes 应用程序或实现模板化部署时，请使用这些工具。
---

# Helm 图表框架

本指南提供了关于如何创建、组织和管理 Helm 图表的综合指导，这些图表用于打包和部署 Kubernetes 应用程序。

## 目的

本技能提供了构建可用于生产环境的 Helm 图表的详细步骤，包括图表结构、模板模式、值管理以及验证策略。

## 适用场景

当您需要以下操作时，请使用本技能：
- 从零开始创建新的 Helm 图表
- 打包 Kubernetes 应用程序以供分发
- 使用 Helm 管理多环境部署
- 实现可重用的 Kubernetes 配置文件的模板化
- 设置 Helm 图表仓库
- 遵循 Helm 的最佳实践和约定

## Helm 概述

**Helm** 是 Kubernetes 的包管理器，它具备以下功能：
- 为 Kubernetes 配置文件提供模板化支持，以实现代码复用
- 管理应用程序的发布和回滚
- 处理图表之间的依赖关系
- 为部署提供版本控制
- 简化跨环境的配置管理

## 逐步工作流程

### 1. 初始化图表结构

**创建新图表：**
```bash
helm create my-app
```

**标准图表结构：**
```
my-app/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration values
├── charts/              # Chart dependencies
├── templates/           # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install notes
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   └── tests/
│       └── test-connection.yaml
└── .helmignore         # Files to ignore
```

### 2. 配置 Chart.yaml

**Chart metadata 定义了图表的包信息：**

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for My Application
type: application
version: 1.0.0      # Chart version
appVersion: "2.1.0" # Application version

# Keywords for chart discovery
keywords:
  - web
  - api
  - backend

# Maintainer information
maintainers:
  - name: DevOps Team
    email: devops@example.com
    url: https://github.com/example/my-app

# Source code repository
sources:
  - https://github.com/example/my-app

# Homepage
home: https://example.com

# Chart icon
icon: https://example.com/icon.png

# Dependencies
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

**参考：**请查看 `assets/Chart.yaml.template` 以获取完整示例

### 3. 设计 values.yaml 结构

**以层次结构组织配置值：**

```yaml
# Image configuration
image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

# Number of replicas
replicaCount: 3

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8080

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

# Resources
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

# Environment variables
env:
  - name: LOG_LEVEL
    value: "info"

# ConfigMap data
configMap:
  data:
    APP_MODE: production

# Dependencies
postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp

redis:
  enabled: false
```

**参考：**请查看 `assets/values.yaml.template` 以获取完整结构

### 4. 创建模板文件

**使用 Go 模板和 Helm 函数进行模板编写：**

**templates/deployment.yaml：**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        env:
          {{- toYaml .Values.env | nindent 12 }}
```

### 5. 创建模板辅助文件

**templates/_helpers.tpl：**
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
{{ include "my-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### 6. 管理依赖关系

**在 Chart.yaml 中添加依赖关系：**
```yaml
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

**更新依赖关系：**
```bash
helm dependency update
helm dependency build
```

**覆盖依赖关系的值：**
```yaml
# values.yaml
postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp
    password: changeme
  primary:
    persistence:
      enabled: true
      size: 10Gi
```

### 7. 测试和验证

**验证命令：**
```bash
# Lint the chart
helm lint my-app/

# Dry-run installation
helm install my-app ./my-app --dry-run --debug

# Template rendering
helm template my-app ./my-app

# Template with values
helm template my-app ./my-app -f values-prod.yaml

# Show computed values
helm show values ./my-app
```

**验证脚本：**
```bash
#!/bin/bash
set -e

echo "Linting chart..."
helm lint .

echo "Testing template rendering..."
helm template test-release . --dry-run

echo "Checking for required values..."
helm template test-release . --validate

echo "All validations passed!"
```

**参考：**请查看 `scripts/validate-chart.sh`

### 8. 打包和分发

**打包图表：**
```bash
helm package my-app/
# Creates: my-app-1.0.0.tgz
```

**创建图表仓库：**
```bash
# Create index
helm repo index .

# Upload to repository
# AWS S3 example
aws s3 sync . s3://my-helm-charts/ --exclude "*" --include "*.tgz" --include "index.yaml"
```

**使用图表：**
```bash
helm repo add my-repo https://charts.example.com
helm repo update
helm install my-app my-repo/my-app
```

### 9. 多环境配置

**针对不同环境的配置文件：**

```
my-app/
├── values.yaml          # Defaults
├── values-dev.yaml      # Development
├── values-staging.yaml  # Staging
└── values-prod.yaml     # Production
```

**values-prod.yaml：**
```yaml
replicaCount: 5

image:
  tag: "2.1.0"

resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20

ingress:
  enabled: true
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

postgresql:
  enabled: true
  primary:
    persistence:
      size: 100Gi
```

**根据环境安装图表：**
```bash
helm install my-app ./my-app -f values-prod.yaml --namespace production
```

### 10. 实现钩子（Hooks）和测试

**预安装钩子：**
```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "my-app.fullname" . }}-db-setup
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: db-setup
        image: postgres:15
        command: ["psql", "-c", "CREATE DATABASE myapp"]
      restartPolicy: Never
```

**测试连接：**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ include "my-app.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

**运行测试：**
```bash
helm test my-app
```

## 常见模式

### 模式 1：条件性资源（Conditional Resources）
```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  # ...
{{- end }}
```

### 模式 2：遍历列表（Iterating Over Lists）
```yaml
env:
{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}
```

### 模式 3：包含文件（Including Files）
```yaml
data:
  config.yaml: |
    {{- .Files.Get "config/application.yaml" | nindent 4 }}
```

### 模式 4：全局配置值（Global Values）
```yaml
global:
  imageRegistry: docker.io
  imagePullSecrets:
    - name: regcred

# Use in templates:
image: {{ .Values.global.imageRegistry }}/{{ .Values.image.repository }}
```

## 最佳实践

1. 为图表和应用程序版本使用语义化版本控制
2. 在 `values.yaml` 中使用注释详细记录所有配置值
3. 使用模板辅助文件处理重复逻辑
4. 在打包前验证图表
5. 明确指定依赖关系的版本
6. 对于可选资源使用条件判断
7. 遵循命名规范（使用小写字母和连字符）
8. 附带 `NOTES.txt` 文件以提供使用说明
9. 一致地使用辅助文件添加标签
10. 在所有环境中测试图表的安装效果

## 故障排除

**模板渲染错误：**
```bash
helm template my-app ./my-app --debug
```

**依赖关系问题：**
```bash
helm dependency update
helm dependency list
```

**安装失败：**
```bash
helm install my-app ./my-app --dry-run --debug
kubectl get events --sort-by='.lastTimestamp'
```

## 参考文件

- `assets/Chart.yaml.template` - 图表元数据模板
- `assets/values.yaml.template` - 配置值结构模板
- `scripts/validate-chart.sh` - 验证脚本
- `references/chart-structure.md` - 图表组织结构详细说明

## 相关技能

- `k8s-manifest-generator` - 用于创建基础的 Kubernetes 配置文件
- `gitops-workflow` - 用于自动化 Helm 图表的部署过程