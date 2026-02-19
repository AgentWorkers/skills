---
name: Authorization
slug: authorization
version: 1.0.0
homepage: https://clawic.com/skills/authorization
description: 通过 RBAC（角色基访问控制）、ABAC（属性基访问控制）、权限设置以及基于范围的授权机制，构建安全的访问控制体系。
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要控制其他用户可以执行的操作。Agent 负责权限设计、角色层级管理、策略评估以及访问控制中间件的实现。

## 快速参考

| 主题 | 文件 |
|-------|------|
| RBAC 与 ABAC 的比较 | `models.md` |
| 实现模式 | `patterns.md` |
| 框架中间件 | `middleware.md` |

## 核心规则

### 1. **认证（Authentication）≠ 授权（Authorization）**
- **认证：** 用户的身份验证方式（登录、OAuth、令牌）
- **授权：** 用户可以执行的操作（权限、角色、策略）
- **切勿混淆这两个概念**——认证发生在授权之前

### 2. **最小权限原则（Principle of Least Privilege）**
- 默认拒绝所有请求——仅授予明确允许的权限
- 用户根据工作需求获得最低必要的权限
- 定期审核权限（撤销未使用的权限）
- 在必要时临时提升用户的权限，而非永久性授予

### 3. 选择合适的权限模型
| 模型 | 适用场景 | 复杂度 |
|-------|----------|------------|
| **ACL（Access Control List）** | 简单的资源所有权管理 | 低 |
| **RBAC（Role-Based Access Control）** | 组织层级管理 | 中等 |
| **ABAC（Attribute-Based Access Control）** | 基于动态上下文的权限管理 | 高 |
| **ReBAC（Reversible Role-Based Access Control）** | 社交网络、数据共享场景 | 高 |

**建议从简单模型开始，根据需求逐步升级。**

### 4. **角色设计模式**
- 角色代表工作职责，而非具体的权限
- 最多允许 3 层继承关系（管理员 → 经理 → 用户）
- 避免角色数量过多导致的复杂性——在特殊情况下结合 ABAC 来处理
- 明确记录角色的职责（该角色可以执行哪些操作）

### 5. **权限命名规范**
```
resource:action:scope
documents:write:own     ← Can edit own documents
documents:write:team    ← Can edit team documents
documents:delete:all    ← Can delete any document
```
**统一的权限命名规则有助于避免歧义。**

### 6. **策略评估顺序**
1. 明确拒绝所有请求 → 总是优先执行
2. 明确允许的请求 → 接下来进行判断
3. 如果没有匹配的规则 → 默认拒绝请求
4. 记录所有被拒绝的请求以供调试

### 7. **切勿硬编码权限**
```javascript
// ❌ Bad — hardcoded role check
if (user.role === 'admin') { ... }

// ✅ Good — permission check
if (can(user, 'settings:update')) { ... }
```
**权限设置应避免硬编码，因为角色和权限可能会发生变化。**

## 常见错误

- **错误地检查角色而非权限**：当角色发生变化时，这种做法会导致系统变得脆弱
- **权限设置中使用 OR 逻辑**：例如“可以编辑或具有管理员权限”可能会创建安全隐患
- **权限缓存时间过长**：角色变更后，旧的权限设置可能仍然有效
- **仅在前端进行权限检查**：必须始终在服务器端进行权限验证
- **设置“万能角色”**：应将“管理员”拆分为具体的权限集合
- **循环继承关系**：如果 A 继承了 B，而 B 又继承了 A，可能会导致系统崩溃

## 安全性与隐私保护

**数据存储原则：**
- 所有文档和实现模式仅用于参考，不收集任何用户数据，也不发送外部请求

**本技能不会：**
- 自动访问用户的代码库
- 发送网络请求
- 存储任何用户数据

## 反馈方式

- 如果觉得本文档有用，请给 `clawhub` 评分（例如：给文档添加星标）
- 保持更新：通过 `clawhub sync` 功能获取最新内容