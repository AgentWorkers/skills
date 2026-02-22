# API 开发

## 清晰的控制器架构

```typescript
// routes/user.ts
import { Router, Request, Response, NextFunction } from 'express'
import { UserService } from '../services/user.service'
import { validateRequest } from '../middleware/validation'

const router = Router()
const userService = new UserService()

router.get('/users', async (req, res, next) => {
  try {
    const users = await userService.findAll(req.query)
    res.json(users)
  } catch (err) {
    next(err)
  }
})

router.post('/users', 
  validateRequest(createUserSchema),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await userService.create(req.body)
      res.status(201).json(user)
    } catch (err) {
      next(err)
    }
  }
)
```

## 错误标准化

```typescript
// Standard error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Must be valid email" }
    ]
  }
}
```

## 检查清单

- [ ] 使用中间件进行验证
- [ ] 标准化错误响应
- [ ] 添加请求日志记录
- [ ] 实现速率限制
- [ ] 使用 OpenAPI/Swagger 进行文档编写
- [ ] 添加身份验证/授权机制