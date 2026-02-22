# 测试基础

## 测试金字塔

```
        ╱╲
       ╱  ╲      E2E (few)
      ╱────╲
     ╱      ╲    Integration (some)
    ╱────────╲
   ╱          ╲  Unit (many)
  ╱────────────╲
```

## 单元测试

```typescript
// user.service.test.ts
import { describe, it, expect, vi } from 'vitest'
import { UserService } from './user.service'

describe('UserService', () => {
  it('should create user', async () => {
    const mockRepo = {
      create: vi.fn().mockResolvedValue({ id: '1', email: 'test@test.com' })
    }
    const service = new UserService(mockRepo)
    
    const user = await service.create({ email: 'test@test.com', name: 'Test' })
    
    expect(user.email).toBe('test@test.com')
    expect(mockRepo.create).toHaveBeenCalled()
  })
})
```

## 集成测试

```typescript
// api/users.test.ts
import { describe, it, expect, beforeAll } from 'vitest'
import request from 'supertest'
import { app } from '../src/index'

describe('POST /users', () => {
  it('should create user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@test.com', name: 'Test' })
    
    expect(res.status).toBe(201)
    expect(res.body.email).toBe('test@test.com')
  })
})
```

## 检查清单

- [ ] 设置测试框架（Vitest/Jest）
- [ ] 为服务编写单元测试
- [ ] 为 API 添加集成测试
- [ ] 使用测试 fixture（测试辅助工具）
- [ ] 对外部服务进行模拟（mock）
- [ ] 确保核心逻辑的覆盖率达到 80%