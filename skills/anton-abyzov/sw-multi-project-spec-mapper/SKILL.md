---
name: multi-project-spec-mapper
description: 智能的多项目规范分割功能，能够将用户故事自动分配到对应的项目中（前端开发、后端开发、移动应用开发、基础设施维护）。适用于处理多个 JIRA/GitHub 项目、微服务架构，或由多个团队共同开发的旧有项目（brownfield projects）的场景。该功能通过分析项目内容和所使用的技术栈来实现自动分类。
---

# 多项目规范映射器 - 智能项目组织

**功能**：自动检测 SpecWeave 设置中的多个项目，分析用户故事并将其映射到相应的项目（前端、后端、移动端、基础设施），并将规范文件组织到特定项目的文件夹中，并实现与 JIRA/GitHub 的双向同步。

**适用场景**：
- 用户配置了多个 JIRA 项目（例如前端、后端、移动端项目）
- 需要同步多个 GitHub 仓库
- 涉及多个团队/服务的旧项目（Brownfield projects）
- 采用微服务架构，具有独立的前端/后端/移动端代码库
- 需要将单一的规范文件拆分为针对不同项目的文件

**核心功能**：
1. ✅ **智能项目检测**：分析 `config.json` 文件以识别多项目设置
2. ✅ **用户故事分类**：根据关键词、技术栈和组件将用户故事映射到相应项目
3. ✅ **规范文件拆分**：将单一的规范文件拆分为针对特定项目的文件
4. ✅ **文件夹组织**：创建 `specs/FE/`, `specs/BE/`, `specs/MOBILE/` 等文件夹结构
5. ✅ **JIRA 项目类型映射**：根据项目范围建议使用 Epic/Story/Task 等项目类型
6. ✅ **双向同步**：为每个项目配置 GitHub/JIRA 的同步规则

---

## 工作原理

### 第一步：检测多项目设置

检查 `config.json` 文件中的配置：
```json
{
  "sync": {
    "profiles": {
      "jira-default": {
        "provider": "jira",
        "config": {
          "domain": "company.atlassian.net",
          "projects": ["FE", "BE", "MOBILE"]  // ← Multiple projects!
        }
      }
    }
  }
}
```

**如果检测到多个项目** → 启用多项目模式

---

### 第二步：分析用户故事

对每个用户故事进行分析：
- **关键词**：如 “UI”、“chart”、“API”、“mobile”、“database”、“deployment”
- **技术栈**：如 “React”、“Node.js”、“React Native”、“PostgreSQL”、“Kubernetes”
- **组件**：如 “component”、“service”、“screen”、“controller”、“pipeline”

**示例**：
```
US-001: Log a Workout (Web UI)
→ Keywords: "UI", "web", "chart"
→ Tech: "React"
→ Project: FE (90% confidence)

US-002: View Workout History (API)
→ Keywords: "API", "endpoint", "database"
→ Tech: "Node.js", "PostgreSQL"
→ Project: BE (95% confidence)

US-005: Cross-Platform Data Sync (Mobile)
→ Keywords: "mobile", "offline", "sync"
→ Tech: "React Native"
→ Project: MOBILE (100% confidence)
```

---

### 第三步：创建特定项目的规范文件

**文件夹结构**：
```
.specweave/docs/internal/specs/
├── FE/
│   ├── spec-0001-fitness-tracker-web.md
│   └── README.md
├── BE/
│   ├── spec-0001-fitness-tracker-api.md
│   └── README.md
├── MOBILE/
│   ├── spec-0001-fitness-tracker-mobile.md
│   └── README.md
└── SHARED/
    ├── spec-0001-fitness-tracker-shared.md  (cross-cutting concerns)
    └── README.md
```

**spec.md 文件的 YAML 前言（必填）**：
```yaml
# For 1-level structure (projects only)
---
increment: 0001-fitness-tracker-web
project: FE                      # REQUIRED
title: "Fitness Tracker Web UI"
status: planned
---

# For 2-level structure (projects + boards)
---
increment: 0001-fitness-tracker-web
project: acme-corp               # REQUIRED
board: digital-operations        # REQUIRED for 2-level
title: "Fitness Tracker Web UI"
status: planned
---
```

**检测过程**：使用 `src/utils/structure-level-detector.ts` 中的 `detectStructureLevel()` 函数

**每个规范文件包含**：
- 必填的 YAML 前言，其中包含 `project:`（以及二级分类的 `board:`）字段
- 映射到该项目的用户故事
- 该项目特定的验收标准
- 链接到共享的基础设施/需求文档

---

### 第四步：实现与 JIRA 的同步

**JIRA 的项目层次结构**：
```
JIRA Project: FE
├── Epic: Fitness Tracker Web UI (SPEC-0001)
│   ├── Story: US-001: Log a Workout
│   │   ├── Task: T-001: Create Workout Form Component
│   │   ├── Task: T-002: Implement Exercise Search
│   │   └── Task: T-003: Add Set Logging UI
│   └── Story: US-004: Track Progress with Charts
│       ├── Task: T-010: Integrate Recharts Library
│       └── Task: T-011: Create Chart Components

JIRA Project: BE
├── Epic: Fitness Tracker API Backend (SPEC-0001)
│   ├── Story: US-002: View Workout History (API)
│   │   ├── Task: T-004: Create GET /api/workouts Endpoint
│   │   ├── Task: T-005: Implement Filtering Logic
│   │   └── Task: T-006: Add Pagination
│   └── Story: US-003: Manage Exercise Library (API)
│       ├── Task: T-007: Create Exercise CRUD Endpoints
│       └── Task: T-008: Implement Search

JIRA Project: MOBILE
├── Epic: Fitness Tracker Mobile App (SPEC-0001)
    └── Story: US-005: Cross-Platform Data Sync
        ├── Task: T-012: Implement Offline Mode (AsyncStorage)
        ├── Task: T-013: Create Sync Queue
        └── Task: T-014: Handle Conflict Resolution
```

---

### 第五步：配置双向同步

**GitHub 同步配置**（位于 `.specweave/config.json` 文件中）：
```json
{
  "hooks": {
    "post_task_completion": {
      "sync_living_docs": true,
      "external_tracker_sync": true
    }
  },
  "sync": {
    "enabled": true,
    "activeProfile": "jira-default",
    "settings": {
      "autoCreateIssue": true,
      "syncDirection": "bidirectional",
      "projectMapping": {
        "FE": {
          "jiraProject": "FE",
          "jiraBoards": [123],
          "githubRepo": "company/frontend-web"
        },
        "BE": {
          "jiraProject": "BE",
          "jiraBoards": [456],
          "githubRepo": "company/backend-api"
        },
        "MOBILE": {
          "jiraProject": "MOBILE",
          "jiraBoards": [789],
          "githubRepo": "company/mobile-app"
        }
      }
    }
  }
}
```

---

## 项目分类规则

### 前端（FE）

**关键词**：
- UI/UX：按钮、表单、输入框、页面、视图、模态框、下拉菜单
- 可视化：图表、图形、仪表盘、小部件
- 样式：CSS、主题、暗黑模式、响应式布局
- 状态管理：Redux、Zustand、上下文管理

**技术栈**：
- React、Vue、Angular、Next.js、Svelte
- TypeScript、JavaScript
- Tailwind CSS、Material-UI、Chakra UI、Ant Design
- Recharts、D3、Chart.js

**组件**：
- 组件、钩子、上下文管理、页面布局相关组件

**匹配要求**：关键词匹配度达到 30% 以上

---

### 后端（BE）

**关键词**：
- API：端点、REST、GraphQL、路由
- 数据库：查询、迁移、数据库模式、模型
- 认证：身份验证、JWT、会话、令牌
- 处理流程：队列、作业、工作进程、定时任务、批量处理

**技术栈**：
- Node.js（Express、Fastify、NestJS）
- Python（FastAPI、Django、Flask）
- Java（Spring Boot）、.NET（ASP.NET）
- PostgreSQL、MySQL、MongoDB、Redis

**组件**：
- 控制器、服务、数据仓库、中间件、处理程序

**匹配要求**：关键词匹配度达到 30% 以上

---

### 移动端（MOBILE）

**关键词**：
- 移动端开发：原生应用、iOS、Android、跨平台应用
- 设备相关：摄像头、GPS、推送通知、离线功能
- 导航：标签栏、抽屉菜单、页面切换
- 数据存储：LocalStorage、本地数据库

**技术栈**：
- React Native、Expo、Flutter
- Swift、Kotlin
- React Navigation 库

**注意事项**：排除 “web” 关键词（会降低匹配准确性）

**匹配要求**：关键词匹配度达到 30% 以上

---

### 基础设施（INFRA）

**关键词**：
- DevOps：部署、持续集成/持续部署（CI/CD）、Docker、Kubernetes
- 监控：日志记录、指标监控、警报系统、服务水平协议（SLO）
- 安全性：SSL、TLS、防火墙、虚拟私有网络（VPC）
- 可扩展性：负载均衡、内容分发网络（CDN）、数据备份

**技术栈**：
- AWS、Azure、GCP
- Kubernetes、Docker、Terraform
- Jenkins、GitHub Actions、GitLab CI
- Prometheus、Grafana、Datadog

**组件**：部署流程、配置文件（manifest）、Terraform 模块

**匹配要求**：关键词匹配度达到 30% 以上

---

## JIRA 项目类型分类

- **Epic**（大于 13 个故事点）：涵盖多个用户故事的大型功能模块
  **示例**：“健身追踪器 MVP”（总故事点数 29）

- **Story**（3-13 个故事点）：具有明确价值的常规用户故事
  **示例**：“US-001：记录锻炼记录”（8 个故事点）

- **Task**（1-2 个故事点）：小型实现任务
  **示例**：“T-001：创建锻炼记录表单组件”（2 个故事点）

- **Subtask**（小于 1 个故事点）：细粒度的工作任务
  **示例**：“创建 /api/workouts 端点”（0.5 个故事点）

---

## 使用示例

### 示例 1：健身追踪器（多项目场景）

**输入**：包含 35 个用户故事的单一规范文件

**检测结果**：
```
✓ Multi-project setup detected:
  - FE (Frontend Web)
  - BE (Backend API)
  - MOBILE (React Native)
```

**分类结果**：
```
Analyzing 35 user stories...
✓ US-001: Log a Workout → FE (90% confidence: React, UI, chart)
✓ US-002: View Workout History → BE (95% confidence: API, database, query)
✓ US-004: Track Progress with Charts → FE (100% confidence: Recharts, visualization)
✓ US-005: Cross-Platform Data Sync → MOBILE (100% confidence: React Native, offline)

Project Distribution:
- FE: 12 user stories (34%)
- BE: 15 user stories (43%)
- MOBILE: 6 user stories (17%)
- SHARED: 2 user stories (6%)
```

**最终输出**：
```
Creating project-specific specs...
✓ specs/FE/spec-0001-fitness-tracker-web.md (12 user stories)
✓ specs/BE/spec-0001-fitness-tracker-api.md (15 user stories)
✓ specs/MOBILE/spec-0001-fitness-tracker-mobile.md (6 user stories)
✓ specs/SHARED/spec-0001-fitness-tracker-shared.md (2 user stories)

JIRA Sync Configuration:
✓ FE → JIRA Project FE (Board 123)
✓ BE → JIRA Project BE (Board 456)
✓ MOBILE → JIRA Project MOBILE (Board 789)
```

---

### 示例 2：微服务电商平台

**输入**：针对多服务平台的规范文件

**检测结果**：
```
✓ Multi-project setup detected:
  - FRONTEND (Web storefront)
  - PRODUCT-SVC (Product service)
  - ORDER-SVC (Order service)
  - PAYMENT-SVC (Payment service)
  - INFRA (Kubernetes + monitoring)
```

**分类结果**：
```
Analyzing 50 user stories...
✓ US-010: Product Catalog UI → FRONTEND (95%)
✓ US-011: Product Search API → PRODUCT-SVC (100%)
✓ US-020: Shopping Cart → ORDER-SVC (90%)
✓ US-030: Stripe Integration → PAYMENT-SVC (100%)
✓ US-040: Kubernetes Deployment → INFRA (100%)

Project Distribution:
- FRONTEND: 15 user stories
- PRODUCT-SVC: 12 user stories
- ORDER-SVC: 10 user stories
- PAYMENT-SVC: 8 user stories
- INFRA: 5 user stories
```

---

## 配置说明

在 `.specweave/config.json` 文件中启用多项目模式：
```json
{
  "multiProject": {
    "enabled": true,
    "autoDetect": true,
    "customRules": {
      "FE": {
        "keywords": ["react", "ui", "chart"],
        "techStack": ["react", "typescript", "recharts"],
        "confidenceThreshold": 0.3
      }
    }
  }
}
```

---

**相关技能**：
- **spec-generator**：用于生成完整的规范文件（用于规范文件的分割）
- **increment-planner**：用于规划开发计划（将任务分配到相应项目）
- **jira-sync**：用于与 JIRA 进行同步（利用项目分类信息）
- **github-sync**：用于与 GitHub 进行同步（利用项目分类信息）

---

---

基于：Increment 0020-multi-project-intelligent-sync