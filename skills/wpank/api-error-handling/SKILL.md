---
name: error-handling
model: standard
description: 跨语言和层次的错误处理模式——包括操作错误与程序错误、重试策略、断路器机制、错误边界处理、HTTP响应、优雅降级以及结构化日志记录。这些内容在设计错误处理策略、构建具有弹性的API或审查错误管理机制时非常有用。
---

# 错误处理模式

> 提供具备弹性的软件。在系统边界处处理错误，快速且明确地报告错误，绝不要默默地吞咽异常。

## 错误处理原则

| 原则 | 描述 |
|-----------|-------------|
| **快速失败** | 尽早发现错误——在系统边界处验证输入，而不在业务逻辑深处 |
| **明确显示错误** | 错误必须被记录、呈现出来，并触发警报 |
| **在边界处处理错误** | 在各层边界（控制器、中间件、网关）捕获并处理错误 |
| **允许系统崩溃** | 对于无法恢复的状态，直接崩溃并重启（Erlang/OTP的设计理念） |
| **具体处理错误类型** | 只捕获特定的错误类型，避免使用通用的 `catch` 或 `except` |
| **提供足够上下文** | 每个错误都应包含足够的上下文，以便在不重现错误的情况下进行诊断 |

---

## 错误类型

**操作错误** — 网络超时、无效的用户输入、文件未找到、数据库连接丢失。应优雅地处理这些错误。

**程序错误** — `TypeError`、空指针引用、断言失败。应修复代码，而不是简单地捕获并忽略这些错误。

```javascript
// Operational — handle gracefully
try {
  const data = await fetch('/api/users');
} catch (err) {
  if (err.code === 'ECONNREFUSED') return fallbackData;
  throw err; // re-throw unexpected errors
}

// Programmer — let it crash, fix the bug
const user = null;
user.name; // TypeError — don't try/catch this
```

---

## 各编程语言的错误处理模式

| 编程语言 | 处理机制 | 应避免的做法 |
|----------|-----------|-------------|
| **JavaScript** | `try/catch`、`Promise.catch`、错误子类 | 使用 `.catch()` 来吞咽错误 |
| **Python** | 异常处理、上下文管理器（`with`） | 使用通用的 `except:` 来捕获所有错误 |
| **Go** | 使用 `error` 返回值、`errors.Is/As`、`fmt.Errorf` 来包装错误 | 直接调用 `riskyFunction()` 而忽略错误 |
| **Rust** | 使用 `Result<T, E>`、`Option<T>`、`?` 操作符 | 在生产代码中直接使用 `.unwrap()` 来处理错误 |

### JavaScript — 错误子类

```javascript
class AppError extends Error {
  constructor(message, code, statusCode, details = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
    this.isOperational = true;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} not found`, 'NOT_FOUND', 404, { resource, id });
  }
}

class ValidationError extends AppError {
  constructor(errors) {
    super('Validation failed', 'VALIDATION_ERROR', 422, { errors });
  }
}
```

### Go — 错误包装

```go
func GetUser(id string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE id = $1", id)
    var user User
    if err := row.Scan(&user.ID, &user.Name); err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("querying user %s: %w", id, err)
    }
    return &user, nil
}
```

---

## 错误处理边界

### Express 错误中间件

```javascript
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const response = {
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.isOperational ? err.message : 'Something went wrong',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
      requestId: req.id,
    },
  };

  logger.error('Request failed', {
    err, requestId: req.id, method: req.method, path: req.path,
  });

  res.status(statusCode).json(response);
});
```

### React 错误处理边界

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => queryClient.clear()}>
  <App />
</ErrorBoundary>
```

---

## 重试策略

| 策略 | 使用场景 | 配置参数 |
|---------|-------------|--------|
| **指数级退避** | 临时性故障（如网络问题、503错误） | 基础退避时间1秒，最大30秒，每次退避时间翻倍 |
| **退避加抖动** | 多个客户端同时尝试请求 | 每次延迟时间随机增加30% |
| **断路器** | 下游服务频繁失败 | 失败5次后关闭连接，30秒后部分恢复连接 |
| **隔离故障** | 防止故障扩散 | 限制每个服务的并发请求数量 |
| **超时机制** | 防止系统无限期挂起 | 连接尝试5秒，读取数据30秒，总时间不超过60秒 |

### 带有抖动的指数级退避策略

```javascript
async function withRetry(fn, { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = {}) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries || !isRetryable(err)) throw err;
      const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      const jitter = delay * (0.7 + Math.random() * 0.6);
      await new Promise((r) => setTimeout(r, jitter));
    }
  }
}

function isRetryable(err) {
  return [408, 429, 500, 502, 503, 504].includes(err.statusCode) || err.code === 'ECONNRESET';
}
```

### 断路器机制

```javascript
class CircuitBreaker {
  constructor({ threshold = 5, resetTimeout = 30000 } = {}) {
    this.state = 'CLOSED';       // CLOSED → OPEN → HALF_OPEN → CLOSED
    this.failureCount = 0;
    this.threshold = threshold;
    this.resetTimeout = resetTimeout;
    this.nextAttempt = 0;
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) throw new Error('Circuit is OPEN');
      this.state = 'HALF_OPEN';
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }

  onSuccess() { this.failureCount = 0; this.state = 'CLOSED'; }
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.resetTimeout;
    }
  }
}
```

---

## HTTP 错误响应

| 状态码 | 名称 | 使用场景 |
|--------|------|-------------|
| **400** | 错误请求 | 请求语法错误或JSON格式无效 |
| **401** | 未经授权 | 未提供有效的认证信息 |
| **403** | 禁止访问 | 虽已认证但权限不足 |
| **404** | 资源未找到 | 请求的资源不存在 |
| **409** | 冲突 | 请求与当前系统状态冲突 |
| **422** | 实体无法处理 | 请求语法正确但存在语义错误 |
| **429** | 请求过多 | 超过请求速率限制（可附加 `Retry-After` 头信息） |
| **500** | 服务器内部错误 | 服务器出现意外故障 |
| **502** | 网关错误 | 上游服务返回了无效响应 |
| **503** | 服务暂时不可用 | 服务正在维护或过载 |

### 标准错误响应格式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid fields.",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ],
    "requestId": "req_abc123xyz"
  }
}
```

---

## 优雅降级策略

| 策略 | 示例 |
|----------|---------|
| **备用方案** | 当图片服务不可用时，显示缓存中的头像 |
| **功能开关** | 关闭不稳定的推荐系统 |
| **缓存响应** | 使用 `X-Cache: STALE` 头部字段返回过时的数据 |
| **部分响应** | 返回可用数据，并附带 `warnings` 数组 |

```javascript
async function getProductPage(productId) {
  const product = await productService.get(productId); // critical — propagate errors

  const [reviews, recommendations] = await Promise.allSettled([
    reviewService.getForProduct(productId),
    recommendationService.getForProduct(productId),
  ]);

  return {
    product,
    reviews: reviews.status === 'fulfilled' ? reviews.value : [],
    recommendations: recommendations.status === 'fulfilled' ? recommendations.value : [],
    warnings: [reviews, recommendations]
      .filter((r) => r.status === 'rejected')
      .map((r) => ({ service: 'degraded', reason: r.reason.message })),
  };
}
```

## 日志记录与监控

| 实践方法 | 实现方式 |
|----------|---------------|
| **结构化日志记录** | 使用 JSON 格式记录日志：`level`、`message`、`error`、`requestId`、`userId`、`timestamp` |
| **错误跟踪** | 使用 Sentry、Datadog、Bugsnag 等工具自动捕获错误，并关联源代码信息 |
| **设置警报阈值** | 当错误率超过1%、99百分位延迟超过2秒或出现5xx错误时触发警报 |
| **关联请求ID** | 在所有服务调用中传递 `requestId` 以追踪错误来源 |
| **日志级别** | `error` 表示需要关注，`warn` 表示系统降级，`info` 表示正常运行，`debug` 表示开发调试阶段 |

---

## 应避免的错误处理实践

| 应避免的做法 | 应采取的修复措施 |
|-------------|-----|
| **默默吞咽错误** | 使用 `catch (e) {}` 来隐藏错误，这会导致数据损坏 |
| **在所有层级使用通用的错误处理机制** | 应捕获特定类型的错误，避免意外错误被忽略 |
| **将错误作为控制流程的一部分** | 应使用条件判断、返回具体值或使用选项类型来处理错误 |
| **使用字符串类型的错误对象** | 应使用包含错误代码和上下文的 `Error` 对象来抛出错误 |
| **仅在边界处记录日志** | 应在系统边界处记录错误，或对错误进行包装后再抛出 |
| **捕获错误后直接返回 `null` | 应返回 `Result` 类型，或者抛出错误对象 |
| **忽略 Promise 的拒绝** | 必须使用 `await` 或添加 `.catch()` 来处理 Promise 的拒绝 |
| **暴露系统内部细节** | 应对响应进行清洗处理，仅在服务器端记录错误细节 |

---

## 绝对禁止的行为

1. **绝不要默默地吞咽错误** — 使用 `catch (e) {}` 会隐藏错误并导致数据损坏。
2. **绝不要在 API 响应中暴露堆栈跟踪信息、SQL 错误或文件路径** — 应仅在服务器端记录错误细节。
3. **绝不要使用字符串类型的错误对象进行错误抛出** — 使用 `throw 'error'` 会导致无法获取堆栈跟踪、错误类型和上下文信息。
4. **绝不要在没有任何说明的情况下捕获错误后直接返回 `null` — 调用者将无法了解操作失败的原因。
5. **绝不要忽略未处理的 Promise 拒绝** — 必须使用 `await` 或添加 `.catch()` 来处理 Promise 的拒绝。
6. **绝不要缓存错误响应** — 5xx 错误和临时性错误不应被缓存并重新提供。
7. **绝不要将异常用于正常的控制流程** — 异常用于处理异常情况。
8. **绝不要仅返回“出了问题”这样的模糊信息而不记录具体的错误原因** — 必须在服务器端记录完整的错误信息及请求上下文。