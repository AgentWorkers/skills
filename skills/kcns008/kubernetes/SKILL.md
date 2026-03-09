---
name: cluster-agent-swarm
description: >
  **Complete Platform Agent Swarm** — 一个专为 Kubernetes 和 OpenShift 平台操作设计的多代理协调系统。该系统包含以下组件：  
  - **Orchestrator (Jarvis)**：负责系统的整体协调和管理；  
  - **Cluster Ops (Atlas)**：用于集群运维；  
  - **GitOps (Flow)**：实现代码的自动化部署和管理；  
  - **Security (Shield)**：提供安全防护功能；  
  - **Observability (Pulse)**：支持系统监控与性能分析；  
  - **Artifacts (Cache)**：用于存储和管理开发过程中的各种工件；  
  - **Developer Experience (Desk)**：优化开发者的工作体验。
metadata:
  author: cluster-agent-swarm
  version: 1.0.0
  agent_name: Swarm
  agent_role: Platform Agent Swarm (All Agents)
  session_key: "agent:platform:swarm"
  heartbeat: "*/5 * * * *"
  platforms:
    - openshift
    - kubernetes
    - eks
    - aks
    - gke
    - rosa
    - aro
  tools:
    - kubectl
    - oc
    - argocd
    - helm
    - kustomize
    - az
    - aws
    - gcloud
    - rosa
    - jq
    - curl
    - git
---
## Cluster Agent Swarm — 完整的集群管理平台

这是一个包含所有集群管理功能的技能包。安装此技能后，您将能够使用这7个协同工作的代理来执行各种任务。

### 安装选项

#### 安装所有技能（推荐）
通过以下命令安装所有7个代理：
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/
```
这样您就可以使用所有这些代理的功能。

#### 单独安装代理
每个代理也可以通过GitHub的树形路径或`--skill`标志单独安装：
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/gitops  # GitOps代理
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/security  # 安全代理
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/observability  # 可观测性代理
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/artifacts  # 文档管理代理
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/developer-experience  # 开发者体验代理
```

### 安全性管理 — Shield（基于角色的访问控制、策略管理、漏洞管理）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/security
```
在继续操作之前，请先审查`payment-service v3.2`的RBAC（基于角色的访问控制）配置。

### 可观测性管理 — Pulse（性能监控、警报处理）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/observability
```
请注意：CPU使用率的突然增加是否与部署操作或外部流量有关？

### 集群扩展 — Atlas（需要快速响应的事件处理）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/cluster-ops
```
测试集群需要增加2个工作节点。

### 任务调度 — Flow（GitOps）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/gitops
```
GitOps任务的部署可以稍后进行。

### 文档管理 — Cache（版本控制与发布管理）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/artifacts
```
文档的版本控制和发布管理功能由`Cache`代理负责。

### 开发者支持 — Desk（开发者协助）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/developer-experience
```
开发者请求通常不需要紧急处理。

### 系统协调 — Orchestrator（整体监控与沟通）
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/orchestrator
```
`Orchestrator`负责整个系统的协调和监控。

### 文件结构
整个技能包的结构如下：
```bash
cluster-agent-swarm-skills/
├── SKILL.md          # 本文件包含了所有代理的完整文档
├── AGENTS.md         # 各代理的配置和协议
├── skills/
│   ├── orchestrator/        # 任务调度代理（Jarvis）
│       ├── SKILL.md         # 相关文档
│   ├── cluster-ops/        # 集群管理代理（Atlas）
│       ├── SKILL.md         # 相关文档
│   ├── gitops/          # GitOps代理（Flow）
│       ├── SKILL.md         # 相关文档
│   ├── security/         # 安全代理（Shield）
│       ├── SKILL.md         | 
│   ├── observability/      | 
│       ├── SKILL.md         | 
│   ├── artifacts/        | 
│       ├── SKILL.md         | 
│   └── developer-experience/  | 
│           └── SKILL.md         | 
├── scripts/          # 共享脚本
└── references/        | 
    |          | 共享文档
```

### 各代理的详细文档
有关每个代理的详细功能，请参阅相应的`SKILL.md`文件：
- `skills/orchestrator/SKILL.md`：Orchestrator代理的完整文档
- `skills/cluster-ops/SKILL.md`：Cluster Ops代理的完整文档
- `skills/gitops/SKILL.md`：GitOps代理的完整文档
- `skills/security/SKILL.md`：安全代理的完整文档
- `skills/observability/SKILL.md`：可观测性代理的完整文档
- `skills/artifacts/SKILL.md`：文档管理代理的完整文档
- `skills/developer-experience/SKILL.md`：开发者支持代理的完整文档