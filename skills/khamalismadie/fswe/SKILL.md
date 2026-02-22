# 全栈Web工程师（微服务与现代前端）

**所有者：** 私有  
**分发范围：** 仅限内部使用  
**状态：** 已准备好在ClawHub上发布  

---

## 摘要  
这是一个包含18个工程模块的技能包，专为以下领域的全栈工程师设计：  
- 现代TypeScript生态系统  
- API与分布式系统  
- 微服务迁移  
- 前端现代化（Vue 3）  
- 旧代码重构（PHP → TypeScript/Bun）  
- 从开发到部署的完整功能管理  

## 核心职责  
**角色级别：** 中级 → 高级  
**关注领域：** 全栈架构、性能优化、可扩展性  
**技术栈偏好：** 以TypeScript为核心，使用Vue 3和API驱动的系统  

## 模块分类  

### 🏗️ 架构  
| 模块 | 描述 |  
|--------|-------------|  
| system-design | 单体应用与微服务对比、服务边界划分 |  
| bun-typescript | Bun运行时环境、TypeScript后端架构 |  

### 🌐 API与网络  
| 模块 | 描述 |  
|--------|-------------|  
| http-grpc | REST、gRPC、幂等性、版本控制 |  
| api-development | 规范化的控制器设计、数据验证、身份验证 |  

### ⚡ 性能与弹性  
| 模块 | 描述 |  
|--------|-------------|  
| performance | 瓶颈识别、缓存机制、性能优化 |  
| fault-tolerance | 重试机制、断路器、优雅降级策略 |  

### 📊 运维  
| 模块 | 描述 |  
|--------|-------------|  
| monitoring-observability | 日志记录、指标监控、警报系统 |  
| feature-flags | 安全的部署策略、A/B测试机制 |  

### 💾 数据管理  
| 模块 | 描述 |  
|--------|-------------|  
| sql-database | 数据库设计、索引优化、迁移管理 |  
| concurrency-async | 事件循环、Promise处理、后台任务调度 |  

### 🧪 质量控制  
| 模块 | 描述 |  
|--------|-------------|  
| testing-fundamentals | 单元测试、集成测试、契约测试 |  
| code-quality | 代码规范、代码审查标准、重构实践 |  

### 🔄 现代化改造  
| 模块 | 描述 |  
|--------|-------------|  
| vue3-modernization | Vue 3组合式API、状态管理 |  
| legacy-migration | 旧代码向TypeScript的迁移 |  

### 🔧 工程实践  
| 模块 | 描述 |  
|--------|-------------|  
| debugging | 跨层调试、生产环境下的代码安全性 |  
| scrum-agile | 整合计划、任务拆分 |  
| cross-functional | 跨部门沟通、技术规范制定 |  
| feature-ownership | 完整功能的交付流程 |  

---

## 工程标准  
使用该技能包编写的所有代码必须满足以下要求：  
- **清晰易懂**：结构简洁，易于理解  
- **简洁高效**：避免不必要的复杂性  
- **性能优化**：代码经过优化，运行速度快  
- **全面测试**：所有代码都经过测试  
- **可监控**：具备完善的日志记录和指标体系  
- **易于维护**：代码结构良好，易于维护  
- **向后兼容**：在可能的情况下保持兼容性  

## 默认原则  
1. **类型安全优先**：严格使用TypeScript  
2. **尽早发现错误**：尽早进行验证，避免严重问题  
3. **优化可读性**：简洁的代码比复杂的代码更易理解  
4. **明确优于隐含**：明确的设计优于模糊的表达  
5. **面向未来**：设计时考虑代码的可扩展性  
6. **安全发布**：使用功能开关（feature flags）进行渐进式部署  

## 使用方法  
1. **识别** 需要解决的工程问题  
2. 从 `references/<module>/SKILL.md` 中加载相关模块  
3. 遵循相应的检查清单  
4. 实施相应的开发框架  
5. 根据标准对代码进行验证  

## 模块路由（模块内容请参见下方代码块）  
```
references/system-design/SKILL.md
references/http-grpc/SKILL.md
references/concurrency-async/SKILL.md
references/fault-tolerance/SKILL.md
references/performance/SKILL.md
references/monitoring-observability/SKILL.md
references/feature-flags/SKILL.md
references/api-development/SKILL.md
references/sql-database/SKILL.md
references/testing-fundamentals/SKILL.md
references/vue3-modernization/SKILL.md
references/legacy-migration/SKILL.md
references/bun-typescript/SKILL.md
references/debugging/SKILL.md
references/code-quality/SKILL.md
references/scrum-agile/SKILL.md
references/cross-functional/SKILL.md
references/feature-ownership/SKILL.md
```