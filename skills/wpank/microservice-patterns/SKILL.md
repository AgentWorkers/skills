---
name: microservices-patterns
model: reasoning
---

# 微服务模式

## 定义
微服务模式是一系列用于构建分布式系统的设计原则，包括服务拆分、服务间通信、数据管理以及系统弹性等方面的解决方案。这些模式有助于避免“分布式单体”（即一个庞大的、难以维护的分布式系统）这一反模式。

## 适用场景
- 当你需要将一个庞大的单体应用拆分为多个微服务时
- 在设计服务边界和服务契约时
- 在实现服务间通信时
- 在构建具有弹性的分布式系统时

## 关键术语
- 微服务（Microservices）
- 服务网格（Service Mesh）
- 基于事件的架构（Event-Driven Architecture）
- 事务编排（Saga）
- 电路断路器（Circuit Breaker）
- API网关（API Gateway）
- 服务发现（Service Discovery）
- 分布式事务（Distributed Transactions）
- 最终一致性（Eventual Consistency）
- CQRS（Command-Query-Response-Support）

---

## 使用微服务的决策框架
| 如果你遇到以下情况 | 那么你应该考虑使用微服务 |
|----------------|-------------------------|
| 团队规模较小（<5名开发人员），业务领域简单 | 先从单体应用开始开发 |
| 需要独立部署或扩展服务 | 考虑使用微服务 |
| 团队较多，业务边界清晰 | 微服务是一个很好的选择 |
| 时间紧迫，需求不明确 | 先开发单体应用，之后再逐步拆分服务 |

**经验法则**：如果你无法明确定义服务之间的边界，那么你还没有准备好使用微服务。

---

## 服务拆分模式
### 模式1：按业务功能拆分
根据业务功能来组织服务，而不是根据技术层次结构。

```
E-commerce Example:
├── order-service       # Order lifecycle
├── payment-service     # Payment processing
├── inventory-service   # Stock management
├── shipping-service    # Fulfillment
└── notification-service # Emails, SMS
```

### 模式2：逐步迁移（Strangler Fig）
通过逐步添加新功能来从单体应用中拆分服务，避免大规模的重构。

```
1. Identify bounded context to extract
2. Create new microservice
3. Route new traffic to microservice
4. Gradually migrate existing functionality
5. Remove from monolith when complete
```

```python
# API Gateway routing during migration
async def route_orders(request):
    if request.path.startswith("/api/orders/v2"):
        return await new_order_service.forward(request)
    else:
        return await legacy_monolith.forward(request)
```

---

## 服务间通信模式
### 模式1：同步通信（REST/gRPC）
适用于需要立即响应的查询操作。

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=5.0)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def get(self, path: str):
        """GET with automatic retries."""
        response = await self.client.get(f"{self.base_url}{path}")
        response.raise_for_status()
        return response.json()

# Usage
payment_client = ServiceClient("http://payment-service:8001")
result = await payment_client.get(f"/payments/{payment_id}")
```

### 模式2：异步通信（基于事件）
适用于可以接受最终一致性的命令操作。

```python
from aiokafka import AIOKafkaProducer
import json

@dataclass
class DomainEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    occurred_at: datetime
    data: dict

class EventBus:
    def __init__(self, bootstrap_servers: List[str]):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
    
    async def publish(self, event: DomainEvent):
        await self.producer.send_and_wait(
            event.event_type,  # Topic = event type
            value=asdict(event),
            key=event.aggregate_id.encode()
        )

# Order service publishes
await event_bus.publish(DomainEvent(
    event_id=str(uuid.uuid4()),
    event_type="OrderCreated",
    aggregate_id=order.id,
    occurred_at=datetime.now(),
    data={"order_id": order.id, "customer_id": order.customer_id}
))

# Inventory service subscribes and reacts
async def handle_order_created(event_data: dict):
    order_id = event_data["data"]["order_id"]
    items = event_data["data"]["items"]
    await reserve_inventory(order_id, items)
```

## 各种通信方式的适用场景
| 通信方式 | 适用场景 |
|---------|-------------------------|
| 同步通信 | 需要立即响应的操作 |
| 异步通信 | 需要长时间运行的操作，或者可以接受最终一致性的场景 |

---

## 数据管理模式
### 每个服务拥有自己的数据库
每个服务都独立管理自己的数据，避免使用共享数据库。

```
order-service     → orders_db (PostgreSQL)
payment-service   → payments_db (PostgreSQL)
product-service   → products_db (MongoDB)
analytics-service → analytics_db (ClickHouse)
```

### 事务编排模式（Saga）
适用于涉及多个服务且需要回滚能力的操作。

```python
class SagaStep:
    def __init__(self, name: str, action: Callable, compensation: Callable):
        self.name = name
        self.action = action
        self.compensation = compensation

class OrderFulfillmentSaga:
    def __init__(self):
        self.steps = [
            SagaStep("create_order", self.create_order, self.cancel_order),
            SagaStep("reserve_inventory", self.reserve_inventory, self.release_inventory),
            SagaStep("process_payment", self.process_payment, self.refund_payment),
            SagaStep("confirm_order", self.confirm_order, self.cancel_confirmation),
        ]
    
    async def execute(self, order_data: dict) -> SagaResult:
        completed_steps = []
        context = {"order_data": order_data}
        
        for step in self.steps:
            try:
                result = await step.action(context)
                if not result.success:
                    await self.compensate(completed_steps, context)
                    return SagaResult(status="failed", error=result.error)
                completed_steps.append(step)
                context.update(result.data)
            except Exception as e:
                await self.compensate(completed_steps, context)
                return SagaResult(status="failed", error=str(e))
        
        return SagaResult(status="completed", data=context)
    
    async def compensate(self, completed_steps: List[SagaStep], context: dict):
        """Execute compensating actions in reverse order."""
        for step in reversed(completed_steps):
            try:
                await step.compensation(context)
            except Exception as e:
                # Log but continue compensating
                logger.error(f"Compensation failed for {step.name}: {e}")
```

---

## 系统弹性模式
### 电路断路器（Circuit Breaker）
当某个服务出现故障时，迅速将其从系统中隔离，防止故障扩散。

```python
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None
    
    async def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpen("Service unavailable")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
    
    def _should_attempt_reset(self) -> bool:
        return datetime.now() - self.opened_at > timedelta(seconds=self.recovery_timeout)

# Usage
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

async def call_payment_service(data: dict):
    return await breaker.call(payment_client.post, "/payments", json=data)
```

### 带指数退避机制的重试策略
用于处理暂时性的故障。

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError))
)
async def fetch_user(user_id: str):
    response = await client.get(f"/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

### 隔离资源（Bulkhead）
通过隔离资源来限制故障对整个系统的影响。

```python
import asyncio

class Bulkhead:
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def call(self, func: Callable, *args, **kwargs):
        async with self.semaphore:
            return await func(*args, **kwargs)

# Limit concurrent calls to each service
payment_bulkhead = Bulkhead(max_concurrent=10)
inventory_bulkhead = Bulkhead(max_concurrent=20)

result = await payment_bulkhead.call(payment_service.charge, amount)
```

## API网关模式
为所有客户端提供统一的访问入口。

```python
from fastapi import FastAPI, Depends, HTTPException
from circuitbreaker import circuit

app = FastAPI()

class APIGateway:
    def __init__(self):
        self.clients = {
            "orders": httpx.AsyncClient(base_url="http://order-service:8000"),
            "payments": httpx.AsyncClient(base_url="http://payment-service:8001"),
            "inventory": httpx.AsyncClient(base_url="http://inventory-service:8002"),
        }
    
    @circuit(failure_threshold=5, recovery_timeout=30)
    async def forward(self, service: str, path: str, **kwargs):
        client = self.clients[service]
        response = await client.request(**kwargs, url=path)
        response.raise_for_status()
        return response.json()
    
    async def aggregate(self, order_id: str) -> dict:
        """Aggregate data from multiple services."""
        results = await asyncio.gather(
            self.forward("orders", f"/orders/{order_id}", method="GET"),
            self.forward("payments", f"/payments/order/{order_id}", method="GET"),
            self.forward("inventory", f"/reservations/order/{order_id}", method="GET"),
            return_exceptions=True
        )
        
        return {
            "order": results[0] if not isinstance(results[0], Exception) else None,
            "payment": results[1] if not isinstance(results[1], Exception) else None,
            "inventory": results[2] if not isinstance(results[2], Exception) else None,
        }

gateway = APIGateway()

@app.get("/api/orders/{order_id}")
async def get_order_aggregate(order_id: str):
    return await gateway.aggregate(order_id)
```

## 服务健康检查
每个服务都需要进行活跃性和可用性检查。

```python
@app.get("/health/live")
async def liveness():
    """Is the process running?"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    """Can we serve traffic?"""
    checks = {
        "database": await check_database(),
        "cache": await check_redis(),
    }
    
    all_healthy = all(checks.values())
    status = "ready" if all_healthy else "not_ready"
    
    return {"status": status, "checks": checks}
```

---

**绝对禁止的做法**
- **使用共享数据库**：这会导致服务之间的紧密耦合，违背微服务的设计原则。
- **使用同步通信链式调用**：A → B → C → D 的结构容易出错且效率低下。
- **不使用电路断路器**：如果一个服务失败，可能会导致整个系统崩溃。
- **采用分布式单体架构**：微服务应该能够独立部署。
- **忽略网络故障**：网络故障是不可避免的，必须做好应对措施。
- **不使用补偿机制**：无法撤销失败的分布式事务。
- **直接从微服务开始开发**：在没有合理设计的基础上直接使用微服务可能会导致系统不稳定。
- **服务间频繁调用**：过多的服务间交互会增加系统延迟。