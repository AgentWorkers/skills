---
name: rate-limiting
model: standard
description: 限速算法、实现策略、HTTP规范、分层限速机制、分布式处理模式以及客户端处理方式。这些技术可用于保护API免受滥用、实现不同的使用等级（如免费/高级用户），或配置网关级别的流量控制。
---

# 限流模式

## 算法

| 算法 | 准确率 | 突发处理 | 适用场景 |
|-----------|----------|----------------|----------|
| **令牌桶（Token Bucket）** | 高 | 允许控制突发流量 | API限流、流量整形 |
| **漏桶（Leaky Bucket）** | 高 | 完全平滑突发流量 | 稳定速率处理、排队场景 |
| **固定窗口（Fixed Window）** | 低 | 允许短暂的高峰流量（最高两倍） | 简单使用场景、原型设计 |
| **滑动窗口日志（Sliding Window Log）** | 非常高 | 精确控制 | 需要严格合规性的场景、计费关键场景 |
| **滑动窗口计数器（Sliding Window Counter）** | 高 | 较好的折中方案 | **生产环境API** |

**固定窗口问题：** 用户在11:59和12:01同时发送大量请求，导致实际请求率翻倍。滑动窗口可以解决这个问题。

### 令牌桶（Token Bucket）

令牌桶最多存储一定数量的令牌，令牌以固定速率补充。每个请求会消耗一个令牌。

```python
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

### 滑动窗口计数器（Sliding Window Counter）

结合了固定窗口和滑动窗口日志的机制，根据窗口重叠比例来计算当前请求量：

```python
def sliding_window_allow(key: str, limit: int, window_sec: int) -> bool:
    now = time.time()
    current_window = int(now // window_sec)
    position_in_window = (now % window_sec) / window_sec

    prev_count = get_count(key, current_window - 1)
    curr_count = get_count(key, current_window)

    estimated = prev_count * (1 - position_in_window) + curr_count
    if estimated >= limit:
        return False
    increment_count(key, current_window)
    return True
```

---

## 实现选项

| 方法 | 适用范围 | 适用场景 |
|----------|-------|----------|
| **内存限制（In-memory）** | 单个服务器 | 零延迟、无依赖性 |
| **Redis**（`INCR` + `EXPIRE`） | 分布式系统 | **多实例部署** |
| **API网关（API Gateway）** | 边缘节点 | 无需编写代码，内置监控面板 |
| **中间件（Middleware）** | 按服务级别控制 | 提供细粒度的用户/端点控制 |

建议在网关层面设置全局限流规则，并在应用层面实现更细粒度的控制。

---

## HTTP头部信息

即使在请求成功的情况下，也必须返回限流相关信息：

```
RateLimit-Limit: 1000
RateLimit-Remaining: 742
RateLimit-Reset: 1625097600
Retry-After: 30
```

| 头部字段 | 返回时机 |
|--------|-----------------|
| `RateLimit-Limit` | 每个响应 |
| `RateLimit-Remaining` | 每个响应 |
| `RateLimit-Reset` | 每个响应 |
| `Retry-After` | 仅在返回429状态码时返回 |

### 429状态码响应

当请求超过限流限制时，应返回429状态码，而不是500或503：

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Maximum 1000 requests per hour.",
    "retry_after": 30,
    "limit": 1000,
    "reset_at": "2025-07-01T12:00:00Z"
  }
}
```

---

## 限流级别

可以设置不同粒度的限流规则：

| 适用范围 | 限流键 | 示例限值 | 目的 |
|-------|-----|---------------|---------|
| **按IP限制** | 客户端IP | 每分钟100次请求 | 防止滥用 |
| **按用户限制** | 用户ID | 每小时1000次请求 | 公平使用 |
| **按API密钥限制** | API密钥 | 每小时5000次请求 | 服务间通信 |
| **按端点限制** | 路由+密钥 | `/search`接口每分钟60次请求 | 保护资源密集型操作 |

**分层定价方案：**

| 级别 | 限流次数 | 突发次数 | 费用 |
|------|-----------|-------|------|
| 免费 | 每小时100次请求 | 10次 | $0 |
| 专业版 | 每小时5000次请求 | 100次 | $49/月 |
| 企业版 | 每小时100,000次请求 | 2,000次 | 自定义 |

建议从最具体的限制级别开始设置：按端点 > 按用户 > 按IP。

---

## 分布式限流

基于Redis的分布式限流方案，确保所有实例的限流规则一致：

```python
def redis_rate_limit(redis, key: str, limit: int, window: int) -> bool:
    pipe = redis.pipeline()
    now = time.time()
    window_key = f"rl:{key}:{int(now // window)}"
    pipe.incr(window_key)
    pipe.expire(window_key, window * 2)
    results = pipe.execute()
    return results[0] <= limit
```

**原子Lua脚本**（防止竞态条件）：

```lua
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, window)
end
return current <= limit and 1 or 0
```

请避免先执行`GET`操作再执行`SET`操作，因为这可能导致计数错误。

---

## API网关配置

**NGINX**：

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
        }
    }
}
```

**Kong**：

```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 60
      hour: 1000
      policy: redis
      redis_host: redis.internal
```

---

## 客户端处理

客户端必须正确处理429状态码：

```typescript
async function fetchWithRetry(url: string, maxRetries = 3): Promise<Response> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const res = await fetch(url);
    if (res.status !== 429) return res;

    const retryAfter = res.headers.get('Retry-After');
    const delay = retryAfter
      ? parseInt(retryAfter, 10) * 1000
      : Math.min(1000 * 2 ** attempt, 30000);
    await new Promise(r => setTimeout(r, delay));
  }
  throw new Error('Rate limit exceeded after retries');
}
```

- 当`Retry-After`头部字段存在时，必须遵守其规定的重试间隔；
- 如果该字段不存在，应使用指数级退避策略；
- 对批量请求进行排队处理。

---

## 监控指标

需要监控以下指标：

- **限流命中率**：返回429状态码的请求比例（持续超过5%时触发警报）；
- **接近限流阈值的通知**：剩余请求量低于限值10%的请求；
- **频繁违规的来源**：最常超出限流的IP或用户；
- **限流余量**：正常流量与上限的差距；
- **误判情况**：合法用户被错误地限制了请求。

---

## 避免的错误做法

| 错误做法 | 应对措施 |
|-------------|-----|
| **仅在应用层面实施限流** | 必须结合基础设施层面的限流策略 |
| **不提供重试提示** | 在返回429状态码时必须包含`Retry-After`头部字段 |
| **不同服务使用相同的限流规则** | 同一端点在不同服务中应使用不同的限流策略 |
| **禁止突发流量** | 应允许合法流量出现短暂的高峰 |
| **直接返回429状态码而不做任何提示** | 客户端需要知道请求被限制了 |
| **使用硬编码的限值** | 应通过配置文件设置限值，而非代码常量 |

---

**绝对禁止的行为：**

1. **绝对禁止对健康检查接口实施限流**——这会导致监控系统误报；
2. **绝对禁止仅使用客户端提供的标识符作为限流依据**——这些标识符容易被伪造；
3. **在实施限流时绝对禁止返回200状态码**——客户端需要知道自己的请求被限制了；
4. **在未测量实际流量的情况下设置限值**——这可能会误封合法用户或设置过高的限值；
5. **绝对禁止在不同租户之间共享限流计数器**——这可能导致相邻租户之间的干扰；
6. **绝对禁止对内部API实施限流**——异常的内部服务可能会影响整个系统的稳定性；
7. **实施限流时绝对禁止不进行日志记录**——日志记录对于调整限值和检测滥用行为至关重要。