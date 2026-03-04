---
name: execute-plan
description: 根据实施计划执行各个阶段。
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 执行计划

根据复杂度对实施计划中的各个阶段进行执行。

## 功能介绍

1. 读取计划文件并识别各个阶段。
2. 根据复杂度评分对阶段进行分组。
3. 在执行前展示各阶段的详细信息。
4. 按照项目规范实现每个阶段。
5. 将任务标记为已完成。
6. 运行构建验证。

## 使用方法

```
/execute-plan <plan_file> [phase]
```

**参数：**
- `plan_file`（必填）：计划文件的路径。
- `phase`（可选）：阶段编号、范围或“next”。默认值：下一个未完成的阶段。

**阶段选项：**
- `1` - 执行第1阶段。
- `1-3` - 执行第1至第3阶段。
- `next` - 执行下一个未完成的阶段。
- `all` - 执行所有剩余的阶段。

## 执行策略

根据综合复杂度评分来决定执行策略：

| 综合评分 | 执行策略 |
|----------------|----------|
| ≤ 6 | **批量执行**：同时执行多个阶段。 |
| 7-10 | **谨慎执行**：先执行1-2个阶段，然后进行验证。 |
| > 10 | **顺序执行**：一次执行一个阶段。 |

## 阶段执行流程

对于每个阶段：
1. **展示**：显示该阶段的详细信息和执行方法。
2. **实现**：按照项目规范编写代码。
3. **更新**：在计划文件中标记任务为已完成。
4. **验证**：运行构建验证。

## 示例

```
/execute-plan @flow/plans/plan_user_auth_v1.md phase:1
```

**输出：**
```
Executing Phase 1: Types and Schemas
Complexity: 3/10

Tasks:
- [ ] Create User type definitions
- [ ] Create Zod validation schemas

Implementing...

✓ Phase 1 Complete
- Created src/types/user.ts
- Created src/schemas/user.ts

Build verification: npm run build ✓
```

## 重要规则

- **遵循项目规范**：始终遵循现有的项目规范。
- **每个阶段后进行构建验证**：在继续执行之前，确保构建成功。
- **更新计划文件**：在计划文件中标记已完成的任务。
- **最后执行测试阶段**：只有在所有其他阶段完成后，才执行测试阶段。

## 下一步命令

在执行完所有阶段后，运行 `/review-code` 命令来审查所做的更改，然后再提交代码。