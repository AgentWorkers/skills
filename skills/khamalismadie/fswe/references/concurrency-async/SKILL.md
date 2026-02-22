# 并发与异步编程

## 事件循环模型

```
┌─────────────┐
ers    ││   Tim ← setTimeout, setInterval
├─────────────┤
│   Pending   │ ← I/O callbacks
├─────────────┤
│   Idle      │ ← node internal
├─────────────┤
│   Poll      │ ← I/O
├─────────────┤
│   Check     │ ← setImmediate
├─────────────┤
│  Close CB   │ ← socket.close
└─────────────┘
```

## Promise 模式

```typescript
// Parallel execution
const [users, posts, comments] = await Promise.all([
  getUsers(),
  getPosts(),
  getComments(),
])

// Race condition prevention
async function fetchWithTimeout(url: string, ms: number) {
  const timeout = new Promise((_, reject) => 
    setTimeout(() => reject(new Error('Timeout')), ms)
  )
  return Promise.race([fetch(url), timeout])
}

// Retry with backoff
async function retry<T>(
  fn: () => Promise<T>,
  attempts = 3,
  delay = 1000
): Promise<T> {
  try {
    return await fn()
  } catch (err) {
    if (attempts <= 1) throw err
    await new Promise(r => setTimeout(r, delay))
    return retry(fn, attempts - 1, delay * 2)
  }
}
```

## 异步错误处理

```typescript
// Always catch async errors
app.get('/users', async (req, res, next) => {
  try {
    const users = await getUsers()
    res.json(users)
  } catch (err) {
    next(err) // Pass to error middleware
  }
})
```

## 检查清单

- [ ] 理解事件循环的各个阶段
- [ ] 使用 `Promise.all` 来执行并行操作
- [ ] 处理 Promise 的拒绝（reject）情况
- [ ] 实现超时功能
- [ ] 添加重试逻辑