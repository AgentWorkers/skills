---
name: resilient-connections
model: standard
description: 用于构建具有弹性功能的API客户端和实时连接的技术模式，这些模式包含了重试逻辑、断路器（circuit breaker）以及优雅的降级（graceful degradation）机制。适用于需要处理故障的生产系统开发。这些技术模式涵盖了重试逻辑（retry logic）、断路器（circuit breaker）的应用、连接稳定性（connection resilience）、指数级退避策略（exponential backoff）、API客户端（API client）以及容错性（fault tolerance）等方面的实现。
---

# 弹性连接

构建能够优雅地处理故障的 API 客户端和实时连接机制，通过重试、断路器和备用方案来实现这一目标。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install resilient-connections
```


---

## 使用场景

- 需要处理临时性故障的 API 客户端开发
- 需要自动重新连接的实时连接
- 需要实现优雅降级的系统
- 任何调用外部服务的生产系统

---

## 模式 1：指数退避（Exponential Backoff）

```typescript
interface RetryOptions {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  jitter?: boolean;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const { maxRetries, baseDelay, maxDelay, jitter = true } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;

      // Calculate delay with exponential backoff
      let delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      
      // Add jitter to prevent thundering herd
      if (jitter) {
        delay = delay * (0.5 + Math.random());
      }

      await sleep(delay);
    }
  }

  throw new Error('Unreachable');
}

// Usage
const data = await withRetry(
  () => fetch('/api/data').then(r => r.json()),
  { maxRetries: 3, baseDelay: 1000, maxDelay: 30000 }
);
```

---

## 模式 2：断路器（Circuit Breaker）

```typescript
enum CircuitState {
  Closed,    // Normal operation
  Open,      // Failing, reject requests
  HalfOpen,  // Testing if recovered
}

class CircuitBreaker {
  private state = CircuitState.Closed;
  private failures = 0;
  private lastFailure = 0;
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 30000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.Open) {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = CircuitState.HalfOpen;
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = CircuitState.Closed;
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    
    if (this.failures >= this.threshold) {
      this.state = CircuitState.Open;
    }
  }
}
```

---

## 模式 3：弹性数据获取封装器（Resilient Fetch Wrapper）

```typescript
interface FetchOptions extends RequestInit {
  timeout?: number;
  retries?: number;
}

async function resilientFetch(
  url: string,
  options: FetchOptions = {}
): Promise<Response> {
  const { timeout = 10000, retries = 3, ...fetchOptions } = options;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  const fetchWithTimeout = async () => {
    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal,
      });

      if (!response.ok && response.status >= 500) {
        throw new Error(`Server error: ${response.status}`);
      }

      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  };

  return withRetry(fetchWithTimeout, {
    maxRetries: retries,
    baseDelay: 1000,
    maxDelay: 10000,
  });
}
```

---

## 模式 4：重新连接 WebSocket

```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private retries = 0;
  private maxRetries = 10;

  constructor(
    private url: string,
    private onMessage: (data: unknown) => void
  ) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.retries = 0;
    };

    this.ws.onmessage = (event) => {
      this.onMessage(JSON.parse(event.data));
    };

    this.ws.onclose = () => {
      if (this.retries < this.maxRetries) {
        const delay = Math.min(1000 * 2 ** this.retries, 30000);
        this.retries++;
        setTimeout(() => this.connect(), delay);
      }
    };
  }

  send(data: unknown) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    this.maxRetries = 0; // Prevent reconnection
    this.ws?.close();
  }
}
```

---

## 模式 5：优雅降级（Graceful Degradation）

```typescript
async function fetchWithFallback<T>(
  primary: () => Promise<T>,
  fallback: () => Promise<T>,
  cache?: T
): Promise<T> {
  try {
    return await primary();
  } catch (primaryError) {
    console.warn('Primary failed, trying fallback:', primaryError);
    
    try {
      return await fallback();
    } catch (fallbackError) {
      console.warn('Fallback failed:', fallbackError);
      
      if (cache !== undefined) {
        console.warn('Using cached data');
        return cache;
      }
      
      throw fallbackError;
    }
  }
}

// Usage
const data = await fetchWithFallback(
  () => fetchFromPrimaryAPI(),
  () => fetchFromBackupAPI(),
  cachedData
);
```

---

## 相关技能

- **元技能：** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — 完整的实时仪表盘指南
- [realtime-react-hooks](../realtime-react-hooks/) — 钩子（Hook）的使用方法
- [websocket-hub-patterns](../websocket-hub-patterns/) — 服务器端模式

---

## 绝对不要做的事情

- **绝对不要重试非幂等请求** — POST/PUT 请求可能成功，但无法响应
- **绝对不要使用固定的延迟时间** — 总是添加随机延迟以避免大量请求同时发送
- **绝对不要重试 4xx 错误** — 客户端错误无法自行解决
- **绝对不要让连接永远保持开启状态** — 必须设置超时机制以控制连接状态
- **绝对不要隐藏连接故障** — 向用户显示系统的降级状态

---

## 快速参考

```typescript
// Exponential backoff
const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);

// With jitter
const jitteredDelay = delay * (0.5 + Math.random());

// Retry check
const shouldRetry = 
  error.status >= 500 || 
  error.code === 'ETIMEDOUT' ||
  error.code === 'ECONNRESET';

// Circuit breaker states
Closed -> (failures >= threshold) -> Open
Open -> (timeout elapsed) -> HalfOpen
HalfOpen -> (success) -> Closed
HalfOpen -> (failure) -> Open
```