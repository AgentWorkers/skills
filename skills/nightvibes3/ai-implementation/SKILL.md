---
name: implementation-plan
version: 1.0.0
description: 为软件项目制定详细的实施计划——将功能分解为步骤、文件、任务和可执行代码。
metadata: {"clawdbot":{"emoji":"📋","tags":["planning","architecture","development"]}}
---
# 实施规划技能

为任何软件项目制定全面的实施计划。

## 适用场景

- 用户请求开发一个应用程序、功能或项目时  
- 用户希望在开始编码之前获得一个计划  
- 用户询问“如何实现某个功能”  
- 用户提到需要解决的问题  

## 需要澄清的问题  

如果未提及平台、技术栈或项目是新的还是现有的，在制定计划之前请先询问：  
- 使用什么平台？（iOS、Web、Android、CLI、API）  
- 这是一个新项目还是基于现有代码库的项目？  
- 有什么特定的技术栈偏好或限制吗？  
- 项目的时间线或复杂程度如何？  

## 计划类型  

### 快速计划（5分钟）  
- 项目概述 + 主要文件 + 关键步骤  
- 适用于简单功能或原型  
- 不包括风险分析、API文档和详细测试  

### 详细计划（15分钟以上）  
- 完整的架构设计 + 所有相关文件 + 测试方案 + 部署流程  
- 适用于生产环境的应用程序或复杂功能  
- 包括：依赖关系、API设计、测试计划和风险分析  

在生成计划之前，请务必询问：“需要快速计划还是详细计划？”  

## 实施计划模板  

### 级别1：快速计划  
```markdown
# [Project] - Quick Plan

## What
[One sentence]

## Stack
- Frontend: [X]
- Backend: [X]
- Data: [X]

## Files
- [file1.swift]: [purpose]
- [file2.swift]: [purpose]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
```  

### 级别2：详细计划  
```markdown
# [Project Name] Implementation Plan

## Overview
[1-2 sentence description]

## Architecture
- Frontend: [framework/libraries]
- Backend: [if needed]
- Data: [storage]

## Files to Create

### Core
1. **App.swift** - Entry point
2. **MainView.swift** - Root view
3. **Model.swift** - Data models

### Features
4. **FeatureXView.swift** - UI
5. **FeatureXModel.swift** - Logic

## Step-by-Step

### Phase 1: Foundation
**Step 1: Setup**
- What: Create project, add deps
- Code: [snippet]

**Step 2: Models**
- What: Define data structures
- Code: [snippet]

### Phase 2: Core Features

### Phase 3: Polish

## Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| [name] | [v] | [why] |

## API Design (if backend)
| Endpoint | Method | Params | Response |
|----------|--------|--------|----------|
| /users | GET | - | User[] |

## Testing Strategy
- Unit: [what to test]
- Integration: [what to test]

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [X] | Low | High | [Y] |

## Running
```bash  
[命令]  
```

## Next Steps
1. [Immediate action]
2. [After that]

## Plan Principles

1. **Ask level first** — ALWAYS ask "Quick plan or detailed plan?"
2. **Architecture before files** — Know the stack
3. **Files drive steps** — List files, then implement in order
4. **Dependencies first** — What must exist before X
5. **Code snippets, not dumps** — Show minimal working snippets for critical paths (e.g., key model, one core view), not full implementations
6. **Be specific** — Not "UI" but "LoginView with email/password fields"
7. **Include paths** — Sources/App/LoginView.swift

## Decision Criteria

Choose stack based on:
- **Mobile**: SwiftUI (iOS), Jetpack Compose (Android)
- **Web**: React, Vue, or server-side Swift
- **Backend**: Vapor, FastAPI, Express
- **Database**: SQLite (local), PostgreSQL (prod), Firebase (quick)

**If user just says "app" with no platform: ASK — do NOT assume mobile or web.**

If user context is iOS/macOS-heavy, you MAY suggest SwiftUI/Vapor/SQLite first, but still ASK before committing.

## Refinement Requests

- If user says "expand [phase]" → regenerate that phase in full detail
- If user says "redo with [X]" → re-emit only affected sections
- If user says "more details" → upgrade to Detailed plan

## Example Output (Quick Plan)

User: "Build me a todo app for iOS"

```markdown  
# 待办事项应用 - 快速计划  

## 项目概述  
一个简单的iOS待办事项应用，支持添加、完成和删除待办事项的功能。  

## 技术栈  
- 前端：SwiftUI  
- 后端：无（使用本地存储）  
- 数据存储：UserDefaults  

## 相关文件  
- TodoApp.swift：应用程序的入口文件  
- ContentView.swift：主列表视图  
- Todo.swift：数据模型  
- TodoStore.swift：状态管理类  

## 实施步骤  
1. 使用XcodeGen创建SwiftUI项目  
2. 定义待办事项数据模型（id、title、isCompleted）  
3. 使用List和TextField组件构建主列表视图  
4. 实现添加、删除和切换待办事项的功能  
5. 将数据持久化到UserDefaults中