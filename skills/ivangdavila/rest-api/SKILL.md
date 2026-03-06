---
name: REST API
slug: rest-api
version: 1.0.0
homepage: https://clawic.com/skills/rest-api
description: 使用“以合约为先”的设计理念（contract-first design），构建可投入生产的 REST API；这些 API 需具备安全认证（secure auth）、强大的测试机制（robust testing）以及完善的部署流程（deployment runbooks）。
changelog: Initial release with end-to-end REST API build workflow from contract to deployment.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

首次使用时，请阅读 `setup.md` 以了解集成行为和内存初始化的详细信息。

## 使用场景（When to Use）

当用户需要从零开始设计、实现、保护、测试并发布 REST API，或者需要对现有 API 进行优化以适应生产环境时，请使用此技能。

该技能涵盖以下内容：契约优先设计（contract-first design）、端点规范（endpoint conventions）、认证与授权（authentication and authorization）、数据持久化策略（persistence strategy）、测试计划（test plans）、可观测性（observability）以及发布检查清单（release checklists）。

## 架构（Architecture）

工作相关的数据存储在 `~/rest-api/` 目录下。有关数据结构及状态管理的详细信息，请参阅 `memory-template.md`。

```
~/rest-api/
├── memory.md                     # HOT: active API project context
├── contracts/                    # WARM: OpenAPI specs and compatibility notes
├── decisions/                    # WARM: ADR-style technical decisions
├── tests/                        # WARM: test plans and quality gates
├── operations/                   # WARM: runbooks and incident notes
└── archive/                      # COLD: closed projects and old versions
```

## 快速参考（Quick Reference）

仅加载当前 API 任务所需的数据和文件：

| 主题 | 文件          |
|-------|--------------|
| 设置与激活行为 | `setup.md`       |
| 数据模型       | `memory-template.md`   |
| 契约优先设计    | `api-contract.md`     |
| 端点规范与错误处理 | `endpoint-design.md`   |
| 认证与安全控制    | `auth-and-security.md`   |
| 数据模型与迁移     | `persistence-and-migrations.md` |
| 测试策略与可观测性   | `testing-and-observability.md` |
| 发布前准备检查   | `deployment-checklist.md`   |

## 核心规则（Core Rules）

### 1. 从契约开始，而非控制器（Start from the Contract, not the Controller）

在编写处理程序之前，先在 OpenAPI 中定义资源、数据结构、状态码以及错误类型。  
如果契约定义不明确，可能会导致实现过程中出现重复工作，并影响客户端的使用体验。

### 2. 保持端点语义的一致性（Keep Endpoint Semantics Predictable）

使用稳定的命名规范、复数形式的资源名称，并使用正确的 HTTP 方法。对于 `PUT`、`DELETE` 操作以及可重试的 `POST` 操作，要明确指定其幂等性（idempotent behavior）。  
一致的语义有助于减少客户端错误，并支持更安全的重试机制。

### 3. 默认情况下强制执行安全措施（Enforce Security by Default）

对非公开端点实施认证；在资源访问边界处进行授权检查；严格验证输入数据，并对输出内容进行清洗。  
切勿依赖前端验证作为唯一的安全控制手段。

### 4. 先设计错误处理机制（Design for Failure Paths First）

在扩展正常业务流程之前，先明确错误类型、超时策略、速率限制规则以及故障处理方案。  
在实际生产环境中，API 通常会在边缘环节出现问题，而非在测试环境中。

### 5. 确保数据变更的向后兼容性（Make Data Changes Backward Compatible）

优先使用增量式的数据库迁移方案；安全地回填数据；仅在客户端迁移窗口关闭后删除旧字段。  
未经充分规划的数据或响应变更可能导致系统故障。

### 6. 测试契约、行为及操作流程（Test Contract, Behavior, and Operations）

确保 OpenAPI 合规性；针对实际基础设施进行集成测试；对关键用户流程进行端到端测试。  
仅依赖单元测试无法验证 API 的可靠性。

### 7. 配备可观测性和运维手册（Ship with Observability and Runbooks）

公开请求指标、结构化的错误信息、跟踪标识符以及系统健康状况。  
为已知的故障模式文档化相应的恢复步骤。  
如果无法监控 API 的运行状态，就无法确保其安全使用。

## 常见陷阱（Common Traps）

- 在定义响应和错误处理机制之前就构建端点 → 会导致客户端兼容性问题及频繁的修复工作。  
- 在处理程序中混合处理认证逻辑、业务逻辑和传输相关功能 → 代码变得脆弱且存在安全隐患。  
- 将分页和过滤功能视为可选选项 → 会导致列表端点不稳定及查询效率低下。  
- 在未制定迁移回滚计划的情况下发布 API → 一旦发布失败，修复工作将变得非常复杂。

## 安全性与隐私（Security & Privacy）

**离开您系统的数据：**  
默认情况下，不会传输任何数据。

**保留在本地的数据：**  
所有与 API 相关的项目信息和配置都存储在 `~/rest-api/` 目录下。

**本技能不包含以下功能：**  
- 默认情况下不会自动调用未声明的外部端点。  
- 不会自动存储敏感信息（如密码）。  
- 未经用户明确指令，不会修改基础设施配置。

## 相关技能（Related Skills）

用户可通过以下命令安装相关工具：  
`clawhub install <slug>`  
- `backend`：系统设计与后端架构相关内容。  
- `auth`：认证机制、会话管理及凭证安全。  
- `http`：HTTP 协议细节及请求/响应处理。  
- `api`：第三方 API 的集成指南。

## 反馈（Feedback）

- 如本文档对您有帮助，请点赞：`clawhub star rest-api`  
- 保持信息更新：`clawhub sync`