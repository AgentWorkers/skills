---
name: Angular
slug: angular
version: 1.0.1
description: 构建可靠的 Angular 应用程序时，需要避免 RxJS 数据泄漏、变更检测陷阱（change detection traps）以及依赖注入（Dependency Injection, DI）中的常见错误。
---

## 使用场景

当用户需要具备 Angular 相关的专业知识时，例如组件架构、RxJS 模式、变更检测、依赖注入、路由以及表单处理等。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 组件与变更检测 | `components.md` |
| RxJS 与订阅 | `rxjs.md` |
| 表单与验证 | `forms.md` |
| 依赖注入 | `di.md` |
| 路由与守卫 | `routing.md` |
| HTTP 与拦截器 | `http.md` |

## 常见错误

- 使用被修改的对象调用 `onPush` 时，变更检测可能不会触发；请始终创建新的引用：`{...obj}` 或 `[...arr]`
- 在构造函数或 `ngOnInit` 中，`@ViewChild` 变量可能未定义；请在 `ngAfterViewInit` 或之后再访问它
- 如果不使用 `trackBy`，`*ngFor` 会在任何数据变化时重新渲染整个列表；请添加 `trackBy` 并返回一个稳定的标识符
- 手动调用 `subscribe()` 且不进行取消订阅会导致内存泄漏；请使用 `async` 管道、`takeUntilDestroyed()`，或在 `ngOnDestroy` 中取消订阅
- `HttpClient` 返回的是“冷 Observables”（不可缓存的 Observable）；每次调用 `subscribe()` 都会发起新的 HTTP 请求
- 如果在 `NgZone` 之外使用 `setTimeout`/`setInterval`，变更检测可能不会触发；请使用 `NgZone.run()` 或相关信号机制
- 循环依赖注入可能导致应用程序崩溃；请使用 `forwardRef()` 或重新设计服务结构
- 直接使用 `ElementRef.nativeElement` 访问 DOM 会破坏服务器端渲染（SSR）；请使用 `Renderer2` 或 `@defer`
- 通过 `snapshot` 获取路由参数时可能会错过导航变化；请使用 `paramMap` Observable 来处理同一组件内的导航变化
- 对 `FormGroup` 使用 `setValue()` 时需要更新所有字段；请使用 `patchValue()` 进行部分更新