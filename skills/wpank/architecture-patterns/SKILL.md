---
name: architecture-patterns
model: reasoning
---

# 架构模式

## 什么是架构模式？
用于构建可维护、可测试的后端系统的架构模式包括：清晰架构（Clean Architecture）、六边形架构（Hexagonal Architecture）和领域驱动设计（Domain-Driven Design）。

## 适用场景：
- 从零开始设计新的后端系统
- 重构单体应用以提高可维护性
- 为团队建立统一的架构标准
- 创建可测试、可模拟的代码库
- 规划微服务的分解

## 关键术语：
- 清晰架构（Clean Architecture）
- 六边形架构（Hexagonal Architecture）
- 端口与适配器（Ports and Adapters）
- 领域驱动设计（Domain-Driven Design）
- 层（Layers）
- 实体（Entities）
- 用例（Use Cases）
- 仓库（Repositories）
- 聚合（Aggregates）
- 有界上下文（Bounded Contexts）

---

## 决策框架：选择哪种模式？
| 情况 | 推荐模式 |
|---------|-------------------|
| 简单的CRUD应用程序 | 不推荐（过度设计） |
| 复杂度中等，需要团队标准化 | 清晰架构（Clean Architecture） |
| 需要频繁更改的外部集成 | 六边形架构（六边形架构与适配器） |
| 拥有大量规则的复杂业务领域 | 领域驱动设计（Domain-Driven Design） |
| 大型系统，涉及多个团队 | 领域驱动设计 + 有界上下文（Domain-Driven Design + Bounded Contexts） |

## 快速参考

### 清晰架构（Clean Architecture）的层次结构
```
┌──────────────────────────────────────┐
│      Frameworks & Drivers (UI, DB)   │  ← Outer: Can change
├──────────────────────────────────────┤
│      Interface Adapters              │  ← Controllers, Gateways
├──────────────────────────────────────┤
│      Use Cases                       │  ← Application Logic
├──────────────────────────────────────┤
│      Entities                        │  ← Core Business Rules
└──────────────────────────────────────┘
```

**依赖规则**：依赖关系只能朝内部方向（INWARD）指向。内部层永远不能导入外部层。

---

### 六边形架构（Hexagonal Architecture）
```
         ┌─────────────┐
    ┌────│   Adapter   │────┐    (REST API)
    │    └─────────────┘    │
    ▼                       ▼
┌──────┐              ┌──────────┐
│ Port │◄────────────►│  Domain  │
└──────┘              └──────────┘
    ▲                       ▲
    │    ┌─────────────┐    │
    └────│   Adapter   │────┘    (Database)
         └─────────────┘
```

**端口（Ports）**：定义领域需求的接口
**适配器（Adapters）**：实现层（可替换以便进行测试）

---

## 目录结构
```
app/
├── domain/           # Entities & business rules (innermost)
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   └── interfaces/   # Ports
│       └── user_repository.py
├── use_cases/        # Application business rules
│   └── create_user.py
├── adapters/         # Interface implementations
│   ├── repositories/
│   │   └── postgres_user_repository.py
│   └── controllers/
│       └── user_controller.py
└── infrastructure/   # Framework & external concerns
    ├── database.py
    └── config.py
```

---

## 模式1：清晰架构（Clean Architecture）
### 实体（领域层，Domain Layer）
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Core entity - NO framework dependencies."""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """Business rule in entity."""
        self.is_active = False

    def can_place_order(self) -> bool:
        return self.is_active
```

### 端口（接口，Port）**
```python
from abc import ABC, abstractmethod
from typing import Optional

class IUserRepository(ABC):
    """Port: defines contract, no implementation."""
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

### 用例（应用层，Application Layer）
```python
@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass  
class CreateUserResponse:
    user: Optional[User]
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """Use case: orchestrates business logic."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository  # Injected dependency
    
    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # Business validation
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(user=None, success=False, error="Email exists")
        
        # Create entity
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now()
        )
        
        saved = await self.user_repository.save(user)
        return CreateUserResponse(user=saved, success=True)
```

### 适配器（实现层，Adapter）**
```python
class PostgresUserRepository(IUserRepository):
    """Adapter: PostgreSQL implementation of the port."""
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None
    
    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO users (id, email, name, created_at, is_active)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT (id) DO UPDATE SET email=$2, name=$3, is_active=$5""",
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user
```

---

## 模式2：六边形架构（六边形架构与适配器，Hexagonal Architecture with Adapters）
**适用场景**：当存在多个可能频繁变化的外部集成时。

```python
# Domain Service (Core)
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryPort,      # Port
        payment: PaymentGatewayPort,          # Port
        notifications: NotificationPort       # Port
    ):
        self.orders = order_repo
        self.payments = payment
        self.notifications = notifications
    
    async def place_order(self, order: Order) -> OrderResult:
        # Pure business logic - no infrastructure details
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")
        
        payment = await self.payments.charge(order.total, order.customer_id)
        if not payment.success:
            return OrderResult(success=False, error="Payment failed")
        
        order.mark_as_paid()
        saved = await self.orders.save(order)
        await self.notifications.send(order.customer_email, "Order confirmed")
        
        return OrderResult(success=True, order=saved)

# Adapters (swap these for testing or changing providers)
class StripePaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        # Real Stripe implementation
        ...

class MockPaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

---

## 模式3：领域驱动设计（Domain-Driven Design）
**适用场景**：处理具有大量规则的复杂业务领域。

### 值对象（不可变对象，Value Objects）**
```python
@dataclass(frozen=True)
class Email:
    """Value object: validated, immutable."""
    value: str
    
    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")

@dataclass(frozen=True)
class Money:
    amount: int  # cents
    currency: str
    
    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

### 聚合（保持数据一致性，Aggregates for Consistency）**
```python
class Order:
    """Aggregate root: enforces invariants."""
    
    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []
    
    def add_item(self, product: Product, quantity: int):
        """Business logic in aggregate."""
        if quantity > product.max_quantity:
            raise ValueError(f"Max {product.max_quantity} allowed")
        
        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))
    
    def submit(self):
        """State transition with invariant enforcement."""
        if not self.items:
            raise ValueError("Cannot submit empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")
        
        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))
```

### 仓库模式（Repository Pattern）**
```python
class OrderRepository:
    """Persist/retrieve aggregates, publish domain events."""
    
    async def save(self, order: Order):
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

---

## 测试优势
所有这些模式都支持相同的测试方法：

```python
# Test with mock adapter
async def test_create_user():
    mock_repo = MockUserRepository()
    use_case = CreateUserUseCase(user_repository=mock_repo)
    
    result = await use_case.execute(CreateUserRequest(
        email="test@example.com",
        name="Test User"
    ))
    
    assert result.success
    assert result.user.email == "test@example.com"
```

---

**绝对禁止的做法**：
- **“贫血的领域模型”（Anemic Domain Models）**：仅包含数据、没有行为的实体（应将逻辑放入实体中）
- **框架耦合**：业务逻辑依赖于特定的框架（如Flask、FastAPI、Django ORM）
- **臃肿的控制器**：将业务逻辑放在HTTP处理函数中
- **“漏风的抽象”**：仓库返回ORM对象而非领域实体
- **跳过架构层次**：控制器直接访问数据库
- **过度设计**：在简单的CRUD应用程序中使用清晰架构
- **循环依赖**：用例直接导入控制器