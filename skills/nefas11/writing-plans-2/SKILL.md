---
name: writing-plans
description: 将设计任务分解为每段2到5分钟可以完成的任务，并为每个任务设置相应的验证步骤。
---
# 编写计划技能

## 使用时机

在设计获得批准后（头脑风暴环节结束）。

## 任务结构

每个任务必须包含以下内容：
1. **目标**（1句话）
2. **文件**（文件的具体路径）
3. **实现方式**（代码片段或伪代码）
4. **验证方法**（需要运行的命令及预期输出）
5. **预计耗时**（理想情况下为2-5分钟）

## 计划模板

```markdown
```markdown
# Implementation Plan: [Feature Name]

## Tasks

### Task 1: [Goal]
**Files:** `src/file.js`
**Implementation:**
```javascript
// 在此处添加函数
function cacheFetch(key) {
  // ...
}
```
**Verification:**
```bash
npm test -- cache.test.js
# 预期输出：1个测试用例通过
```
**Estimated Time:** 3 min

### Task 2: [Goal]
[... repeat]
```
```

保存文件至：`docs/plans/YYYY-MM-DD-feature-name.md`

## 质量检查清单

在最终确定计划之前，请确保：
- [ ] 每个任务都指定了具体的文件路径
- [ ] 每个任务都包含验证步骤
- [ ] 没有耗时超过5分钟的任务（如果超过5分钟，请拆分为多个任务）
- [ ] 任务按顺序排列（依赖项相关的任务应放在前面）
- [ ] 计划内容具体明确，不模糊不清

## 避免的错误做法：
- ✌ 任务描述模糊不清（例如：“改进缓存机制”）
- ✌ 没有验证步骤
- ✌ 任务没有文件路径
- ✌ 任务耗时过长（超过10分钟）

## 示例

**错误的任务示例：**
```
Task 1: Add caching
- Implement cache layer
```

**正确的任务示例：**
```markdown
```
Task 1: Add in-memory cache for API responses
**Files:** `src/cache.js` (new), `src/api.js` (modify)
**Implementation:**
```javascript
// cache.js
const cache = new Map();
export function get(key) { return cache.get(key); }
export function set(key, val, ttl) { 
  cache.set(key, val);
  setTimeout(() => cache.delete(key), ttl);
}

// api.js（修改fetchUser函数）
const cached = cache.get(`user:${id}`);
if (cached) return cached;
// ... 原有的获取用户信息的逻辑
cache.set(`user:${id}`, result, 60000);
```

```bash
node -e "const c = require('./src/cache'); c.set('test', 42, 1000); console.log(c.get('test'));"
# 预期输出：42
```
**Verification:**
```
```

**注释：**  
- 在`cache.js`文件中定义了缓存功能。
- 在`api.js`文件中使用了缓存机制来优化用户信息的获取过程。
- 使用`npm test`命令验证`cache.test.js`文件的测试用例是否通过。

**保存文件路径：**  
`docs/plans/2023-01-15-feature-name.md`