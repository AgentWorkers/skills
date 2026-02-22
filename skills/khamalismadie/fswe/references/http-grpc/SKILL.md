# HTTP与gRPC的深入理解

## REST最佳实践

### URL设计
```
GET    /api/v1/users          → List
POST   /api/v1/users          → Create
GET    /api/v1/users/:id      → Read
PATCH  /api/v1/users/:id      → Update
DELETE /api/v1/users/:id      → Delete
```

### 状态码
| 代码 | 用途 |
|------|-------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 无内容 |
| 400 | 请求错误 |
| 401 | 未经授权 |
| 403 | 禁止访问 |
| 404 | 未找到 |
| 409 | 冲突 |
| 422 | 验证错误 |
| 429 | 请求速率限制 |
| 500 | 服务器错误 |

## gRPC与REST的对比

| 对比项 | REST | gRPC |
|--------|------|------|
| 格式 | JSON | 协议缓冲区（Protocol Buffers） |
| 性能 | 中等 | 快速 |
| 浏览器支持 | 原生支持 | 需要gRPC-Web插件 |
| 流式传输 | 支持有限 | 完全支持 |
| 代码生成 | 使用OpenAPI生成 | 内置代码生成机制 |

## 幂等性（Idempotency）

```typescript
// Idempotent POST with idempotency key
app.post('/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key']
  
  // Check if already processed
  const existing = await cache.get(`idempotency:${idempotencyKey}`)
  if (existing) return existing
  
  // Process payment
  const result = await processPayment(req.body)
  
  // Cache result
  await cache.set(`idempotency:${idempotencyKey}`, result, { ttl: 86400 })
  
  return result
})
```

## 检查清单：
- [ ] 使用正确的HTTP方法
- [ ] 返回正确的状态码
- [ ] 对数据修改操作实现幂等性
- [ ] 将API版本从v1升级
- [ ] 使用OpenAPI进行文档编写