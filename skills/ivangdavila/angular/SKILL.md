---
name: Angular
description: 避免常见的 Angular 错误：订阅泄漏（subscription leaks）、变更检测（change detection）问题、依赖注入（dependency injection）问题以及模块组织（module organization）问题。
metadata: {"clawdbot":{"emoji":"🅰️","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 订阅管理
- 手动订阅需要手动取消订阅：在 `ngOnDestroy` 中执行，或使用 `takeUntilDestroyed()` 方法。
- 使用 `async` 管道可以实现自动取消订阅——在模板中推荐使用这种方式，比手动订阅更简洁。
- 在注入上下文中使用 `takeUntilDestroyed()` 方法——比 `Subject` 和 `takeUntil` 的组合更易于维护。

## 数据变化检测
- 默认情况下，Angular 会检查整个组件树——对于大型应用来说效率较低。
- 可以使用 `OnPush` 仅在输入值发生变化或特定事件发生时触发检测——通过设置 `changeDetection: ChangeDetectionStrategy.OnPush` 来实现。
- 对象的修改不会自动触发 `OnPush`——需要创建新的对象引用（例如：`{...obj}` 或 `[...arr]`）。
- 可以使用 `markForCheck()` 方法手动触发数据变化检测——尤其是在 Angular 之外的地方发生了异步数据变化时。

## 依赖注入
- 对于单例服务，使用 `providedIn: 'root'` 进行注入——这样可以在应用程序启动时仅加载一次服务实例，无需在各个模块中重复注册。
- 组件级别的 `providers` 会为每个组件创建新的服务实例——不会在组件之间共享服务。
- 使用 `@Optional()` 注解标记可选依赖项——如果依赖项未提供，可以避免错误。
- 使用 `@Inject(TOKEN)` 注解来注入特定类型的依赖项（不仅仅是类）。

## 生命周期钩子
- `ngOnInit` 在输入值设置完成后调用——用于初始化操作，而不是在构造函数中执行。
- `ngOnChanges` 在 `ngOnInit` 之前调用——每当输入值发生变化时都会被触发，接收 `SimpleChanges` 对象。
- `ngAfterViewInit` 在 `ngOnInit` 之后调用——此时可以访问 DOM 元素（例如：使用 `@ViewChild`）。
- `ngOnDestroy` 用于清理资源——取消订阅、清除定时器、解除事件监听器等。

## 模板
- 使用 `*ngFor` 遍历列表时，需要使用 `trackBy` 函数来提高性能——避免重新渲染整个列表。
- `trackBy` 函数应返回一个唯一的标识符，例如：`trackByFn = (i, item) => item.id`。
- 从 Angular 1.7 开始，`@if` 和 `@for` 可以替代 `*ngIf` 和 `*ngFor`——性能更好，语法更简洁。
- 使用 `ng-container` 指令来包裹结构化内容——这样可以避免在模板中生成额外的 DOM 元素。

## 反应式表单
- `FormGroup` 和 `FormControl` 用于创建反应式表单控件——它们不支持双向数据绑定。
- 控件级别可以使用验证器（例如：`Validators.required`, `Validators.email`）。
- `valueChanges` 是一个 Observable 对象——可以对其进行订阅，或者使用 `async` 管道来处理数据变化。
- 使用 `patchValue` 方法进行部分更新——而 `setValue` 方法则需要更新所有字段。

## 模块与独立组件
- 独立组件不需要依赖其他模块——在组件装饰器中设置 `standalone: true` 即可。
- 可以直接在其他独立组件中导入独立组件——无需声明依赖关系。
- 新项目通常推荐使用独立组件——对于旧项目或依赖关系复杂的场景，可以使用模块结构。

## 路由管理
- 使用 `loadComponent` 或 `loadChildren` 实现懒加载——可以减少初始加载时的资源消耗。
- 路由守卫（guards）可以返回 `boolean`、`UrlTree` 或 `Observable` 类型——`UrlTree` 可用于处理重定向。
- 路由解析器（resolvers）可以预先获取数据——这些数据可以通过 `ActivatedRoute.data` 访问。
- 路由参数：`snapshot` 用于存储一次性的路由状态，`paramMap` 是一个 Observable 对象——用于在导航过程中保持参数的持久性。

## 常见错误
- 直接使用 `ElementRef.nativeElement` 进行 DOM 操作——这可能会导致服务器端渲染（SSR）出现问题，应使用 `Renderer2` 来处理 DOM 操作。
- 在 Angular 区域之外使用 `setTimeout`——应该使用 `NgZone.run()` 来确保定时器在 Angular 的作用域内执行，否则变化检测可能不会被触发。
- 依赖注入中存在循环依赖——可以使用 `forwardRef()` 来解决这个问题，或者重新设计代码结构。
- `HttpClient` 的方法返回的是“冷”Observable 对象（即不会自动更新数据）——每次订阅都会发起新的请求。