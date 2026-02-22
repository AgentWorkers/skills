# 跨平台调试

## 调试工作流程

```
1. Reproduce          → Can you reliably trigger the bug?
2. Isolate           → Find the minimal failing case
3. Analyze           → Check logs, traces, metrics
4. Hypothesize       → Form a theory
5. Test              → Verify the theory
6. Fix               → Implement the solution
7. Verify            → Ensure fix works
8. Prevent           → Add test/monitoring
```

## 请求追踪

```typescript
// Add request ID
app.use(async (req, res, next) => {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID()
  res.setHeader('x-request-id', req.id)
  next()
})

// Log with request ID
app.use((req, res, next) => {
  const start = Date.now()
  res.on('finish', () => {
    logger.info({
      requestId: req.id,
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start,
    })
  })
  next()
})
```

## 生产环境调试注意事项

- [ ] 绝不在测试中使用生产环境的数据
- [ ] 暂时启用详细的日志记录功能
- [ ] 使用只读数据库连接
- [ ] 限制日志中显示的数据量
- [ ] 调试完成后回滚所有更改

## 需检查的事项

- [ ] 添加请求ID
- [ ] 设置集中式的日志记录系统
- [ ] 使用调试工具（如Chrome DevTools、curl）
- [ ] 检查网络请求相关的数据
- [ ] 查看服务器日志
- [ ] 使用断点（仅限本地开发环境）