---
name: FastAPI
description: 使用类型提示、数据验证以及异步支持，快速构建可用于生产环境的 Python API。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# FastAPI 模式

## 异步相关问题
- 在异步端点中混合使用同步数据库驱动程序（如 psycopg2、PyMySQL）会阻塞事件循环——应使用异步驱动程序（如 asyncpg、aiomysql），或将同步代码放在 `run_inexecutor` 中执行。
- 在异步端点中使用 `time.sleep()` 会阻塞所有其他操作——应使用 `await asyncio.sleep()` 代替。
- 异步端点中的 CPU 密集型操作会占用过多资源，导致其他请求无法执行——可以将这些任务卸载到 `ProcessPoolExecutor` 或后台工作线程中处理。
- 异步端点调用执行 I/O 操作的同步函数时仍会阻塞整个调用链——此时整个函数链都必须是异步的。

## Pydantic 验证
- 模型中的默认值会成为共享的可变状态：例如 `items: list = []` 会在多个请求之间共享同一个列表——应使用 `Field(default_factory=list)` 来避免这种情况。
- `Optional[str]` 并不会使字段在请求中变为可选状态——需要添加 `= None` 或使用 `Field(default=None)`。
- Pydantic v2 使用 `model_validate()` 而不是 `parse_obj()`，`model_dump()` 而不是 `.dict()`——v1 的方法已被弃用。
- 对于需要重复验证的类型，应使用 `Annotated[str, Field(min_length=1)]` 来明确指定验证规则。

## 依赖注入
- 默认情况下，所有依赖项都会在每次请求时被加载——对于资源消耗较大的依赖项，可以使用 `lru_cache` 进行缓存；对于单例依赖项，可以将其缓存到 `app.state` 中。
- `Depends()` 函数如果没有参数，会直接使用类型提示作为依赖项——虽然简洁，但可能会让读者感到困惑。
- 嵌套依赖关系会形成有向无环图（DAG）——如果 A 依赖于 B 和 C，而 B 和 C 又都依赖于 D，那么 D 只会被加载一次（每次请求都会重新缓存）。
- 对于需要清理的资源（如数据库会话、文件句柄），应使用 `yield` 来释放它们——即使端点抛出异常，`yield` 之后的代码仍然会执行。

## 生命周期与启动
- `@app.on_event("startup")` 已被弃用——应使用 `lifespan` 异步上下文管理器来管理应用程序的生命周期。
- 共享资源（如数据库连接池、HTTP 客户端）应存储在 `app.state` 中，而不是作为全局变量。
- `lifespan` 管理器会在每个工作进程中只执行一次——如果有 4 个 Uvicorn 工作进程，那么就会创建 4 个数据库连接池。

```python
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app):
    app.state.db = await create_pool()
    yield
    await app.state.db.close()
app = FastAPI(lifespan=lifespan)
```

## 请求/响应
- 端点应返回 `dict` 类型的数据，而不是直接返回 Pydantic 模型对象——FastAPI 会自动处理序列化，这样更快。
- 在返回创建资源的 POST 端点中，应设置 `status_code=201`——虽然 200 是默认值，但语义上并不准确。
- 对于非 JSON 类型的响应，应使用 `Response` 并设置 `media_type="text/plain"`——否则即使返回字符串，也会被自动编码为 JSON。
- 设置 `response_model_excludeunset=True` 可以避免在响应中包含 `None` 字段——使 API 输出更加清晰。

## 错误处理
- 应使用 `raise HTTPException(status_code=404)` 来处理错误——不要直接返回 `Response` 对象，因为这样会绕过中间件。
- 可以使用 `@app.exception_handler(CustomError)` 定义自定义异常处理器——但请注意，这些处理器无法捕获 `HTTPException`。
- 应为用户提供详细的错误信息，同时单独记录实际的错误日志——避免泄露堆栈跟踪。

## 后台任务
- `BackgroundTasks` 会在响应发送后执行，但仍在同一个进程中运行——不适合处理耗时较长的任务。
- 任务会按照添加的顺序依次执行——不要假设它们会并行执行。
- 如果后台任务失败，客户端可能无法察觉——需要自行添加错误处理和警报机制。

## 安全性
- `OAuth2PasswordBearer` 仅用于文档说明——它不会验证令牌，实际应用中需要自行实现令牌验证逻辑。
- CORS 中间件必须位于异常处理器的后面——否则错误请求将无法正确处理 CORS 标头。
- 路由中的依赖项（如 `Depends(get_current_user)` 会影响所有路由，包括健康检查路由。

## 测试
- `TestClient` 对于异步端点也会执行同步操作——应使用 `httpx.AsyncClient` 并搭配 `ASGITransport` 来进行真正的异步测试。
- 可以通过 `app.dependency_overrides[get_db] = mock_db` 来覆盖依赖项的实现——这样比直接修改代码更简洁。
- `TestClient` 的上下文管理器可以确保生命周期管理器被正确执行——否则使用 `with TestClient(app) as client:` 会阻止启动/关闭钩子被触发。