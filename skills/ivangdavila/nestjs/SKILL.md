---
name: NestJS
description: 避免常见的 NestJS 错误：依赖注入（DI）的作用域问题、循环依赖、验证流程（validation pipes）以及模块组织上的陷阱。
metadata: {"clawdbot":{"emoji":"🐱","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 依赖注入（Dependency Injection）
- 如果某个提供者（provider）未被其他模块使用，它必须同时存在于 `providers` 数组和 `exports` 中。
- 如果存在循环依赖关系，会导致程序崩溃；在这种情况下，两个模块都应使用 `forwardRef(() => Module)` 来解决依赖问题。
- 默认的依赖注入范围是单例（singleton）模式：同一个请求会使用相同的提供者实例，因此需要谨慎处理状态管理。
- 如果提供者仅在当前请求的范围内使用，可以使用 `@Injectable({ scope: Scope_REQUEST })` 来指定其作用域，这样该提供者只会被当前请求的依赖组件使用。

## 模块组织（Module Organization）
- 应导入模块本身，而不是直接导入其提供的服务（provider）：例如，应写 `imports: [UserModule]` 而不是 `providers: [UserService]`。
- `exports` 属性用于公开提供的服务，使其可以被其他模块导入；否则，这些服务将保持私有状态。
- 全局模块需要使用 `@Global()` 装饰器，仅用于那些真正需要在整个应用程序中共享的资源（如配置、日志记录等）。
- `forRoot()` 和 `forRootAsync()` 方法的区别在于：`forRootAsync()` 适用于那些依赖其他提供者的配置模块。

## 验证（Validation）
- `ValidationPipe` 需要 `class-validator` 装饰器才能正常工作；普通的类无法进行验证。
- 如果需要自动转换数据（例如将字符串 “1” 转换为数字 1），请将 `transform` 属性设置为 `true`。
- `whitelist: true` 用于过滤掉未知的属性；如果允许使用未知属性，则将 `forbidNonWhitelisted` 设置为 `true` 以触发错误。
- 对于嵌套对象，需要同时使用 `@ValidateNested()` 和 `@Type(() => NestedDto)` 装饰器。

## 执行顺序（Execution Order）
- 执行顺序为：中间件（middleware）→ 安全检查（guards）→ 拦截器（interceptors, pre）→ 验证管道（pipes）→ 处理器（handler）→ 拦截器（interceptors, post）→ 过滤器（filters）。
- 安全检查在验证管道之前执行。
- 全局验证管道在路由相关的验证管道之前执行，但在安全检查之后执行。
- 异常过滤器会捕获整个处理链中的错误，包括安全检查和验证管道产生的错误。

## 异常处理（Exception Handling）
- 在处理异常时，应使用 `throw new HttpException()` 而不是直接返回错误；这样其他组件才能捕获到异常。
- 自定义异常应继承自 `HttpException`，或者实现 `ExceptionFilter` 接口。
- 未处理的异常会导致 500 错误；对于外部调用，应使用 `try/catch` 语句进行异常处理。
- 内置的异常类型包括 `BadRequestException`、`NotFoundException` 等，应优先使用这些异常类型，而不是通用的 `HttpException`。

## 测试（Testing）
- `createTestingModule` 方法不会自动创建模拟对象（mocks）；需要通过 `.overrideProvider(X).useValue(mock)` 在 `providers` 中显式提供模拟对象。
- 在调用 `.compile()` 之前，可以使用 `.overrideProvider(X).useValue(mock)` 来覆盖默认的提供者实现。
- 端到端（E2E）测试需要调用 `app.init()`，并在 `afterAll` 中调用 `app.close()` 来清理测试环境。
- 如果提供者仅在当前请求的范围内使用，可以考虑将其设置为单例模式，以简化单元测试。

## 常见错误（Common Mistakes）
- 如果使用了 `@Body()` 装饰器但没有定义对应的 `DTO` 类型，系统将返回一个普通对象，此时既不会进行验证也不会进行数据转换。
- `@Param('id')` 注解默认将参数视为字符串类型；如果参数需要转换为数字类型，应使用 `ParseIntPipe`：`@Param('id', ParseIntPipe)`。
- 如果安全检查返回 `false`，系统会返回 403 错误；应抛出具体的异常类型以提供更详细的错误信息。
- 异步提供者需要使用工厂函数进行实例化：`useFactory: async () => await createConnection()`。
- 如果在异步服务方法中忘记使用 `await` 关键字，该方法将返回一个 `Promise` 而不是具体的值。