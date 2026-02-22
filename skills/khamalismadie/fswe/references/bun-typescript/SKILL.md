# Bun + TypeScript 后端架构

## Bun 项目结构

```
my-bun-app/
├── src/
│   ├── routes/        # API routes
│   ├── services/      # Business logic
│   ├── middleware/    # Express-style middleware
│   ├── db/           # Database clients
│   └── index.ts      # Entry point
├── tests/
├── package.json
└── tsconfig.json
```

## TypeScript 配置

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "skipLibCheck": true,
    "esModuleInterop": true
  }
}
```

## Bun HTTP 服务器

```typescript
// src/index.ts
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url)
    
    if (url.pathname === '/users' && req.method === 'GET') {
      return Response.json({ users: [] })
    }
    
    return new Response('Not Found', { status: 404 })
  },
})

console.log(`Server running on port ${server.port}`)
```

## 使用 Bun 连接数据库

```typescript
// Using Bun's built-in SQL client
const db = new Database('sqlite.db')

const users = db.query('SELECT * FROM users WHERE id = ?').get(userId)
```

## 检查清单

- [ ] 安装 Bun
- [ ] 设置 TypeScript
- [ ] 启用严格模式（strict mode）
- [ ] 配置路由
- [ ] 添加数据库客户端
- [ ] 配置构建输出
- [ ] 设置测试环境