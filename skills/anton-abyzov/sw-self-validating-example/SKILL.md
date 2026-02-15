---
name: self-validating-example
description: 示例技能：演示如何生成具有自动测试执行功能的自验证 REST API。该技能可用作创建包含预工具使用验证钩子的其他技能的模板。在生成 API 端点之前，该技能会验证 Node.js 环境及其依赖项是否满足要求。
hooks:
  pre_tool_use:
    - validate: file_exists
      path: package.json
      error: "Must be in a Node.js project"
    - validate: dependency
      package: express
      error: "Express must be installed: npm install express"
  post_tool_use:
    - validate: tests_pass
      command: npm test -- --testPathPattern="$OUTPUT"
      max_retries: 3
    - validate: lint
      command: npm run lint -- $OUTPUT
      auto_fix: true
    - validate: types
      command: npx tsc --noEmit $OUTPUT
---

# 自动验证的 API 端点生成器

您正在生成一个具有 **自动验证** 功能的 REST API 端点。

## 自动验证的工作原理

```
┌──────────────────────────────────────────────────────────────┐
│  YOUR CODE WILL BE AUTOMATICALLY VALIDATED                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PRE-CHECK: Verify project has Express installed          │
│                                                              │
│  2. GENERATE: You create the endpoint + tests                │
│                                                              │
│  3. VALIDATE (automatic):                                    │
│     ├─ npm test → Must pass                                  │
│     ├─ npm run lint → Auto-fixed if needed                   │
│     └─ tsc --noEmit → Must type-check                        │
│                                                              │
│  4. If validation fails:                                     │
│     └─ You get feedback and retry (max 3 times)              │
│                                                              │
│  5. If still failing after 3 attempts:                       │
│     └─ Pause for human review                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 必需的输出文件

### 1. API 端点（`src/routes/[name].ts`）

```typescript
import { Router, Request, Response } from 'express';

const router = Router();

// GET /api/[name]
router.get('/', async (req: Request, res: Response) => {
  // Implementation
});

// POST /api/[name]
router.post('/', async (req: Request, res: Response) => {
  // Implementation with validation
});

export default router;
```

### 2. 测试文件（`src/routes/[name].test.ts`） - 必须提供！

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import app from '../app';

describe('[Name] API', () => {
  describe('GET /api/[name]', () => {
    it('should return 200 with data', async () => {
      const res = await request(app).get('/api/[name]');
      expect(res.status).toBe(200);
      expect(res.body).toBeDefined();
    });
  });

  describe('POST /api/[name]', () => {
    it('should create resource with valid data', async () => {
      const res = await request(app)
        .post('/api/[name]')
        .send({ /* valid data */ });
      expect(res.status).toBe(201);
    });

    it('should return 400 for invalid data', async () => {
      const res = await request(app)
        .post('/api/[name]')
        .send({ /* invalid data */ });
      expect(res.status).toBe(400);
    });
  });
});
```

## 验证标准

| 验证项 | 命令 | 是否必需 |
|-------|---------|----------|
| 测试是否通过 | `npm test -- --testPathPattern="$OUTPUT"` | ✅ 是 |
| 代码格式是否整洁（lint） | `npm run lint -- $OUTPUT` | ✅ 是（会自动修复问题） |
| 类型是否正确 | `npx tsc --noEmit $OUTPUT` | ✅ 是 |

## 自动修复机制

如果测试失败，您将收到以下信息：
1. 显示哪些测试失败的测试输出结果
2. 修复失败测试的提示
3. 会自动尝试修复（最多尝试 3 次）

**测试失败时的反馈示例：**
```
🔴 VALIDATION FAILED (attempt 1/3)

Test Results:
  ✗ GET /api/users should return 200 with data
    Expected: 200
    Received: 404

Please fix the route handler and regenerate.
```

## 重要说明

1. **务必生成测试用例** —— 如果测试未通过，该功能将无法完成。
2. **使用正确的类型声明** —— TypeScript 的类型错误会阻止代码的生成。
3. **遵守代码格式规范** —— 代码会自动修复常见的问题。
4. **处理边缘情况** —— 需要测试成功和失败的各种情况。