---
name: Flutter
description: 使用 Flutter 小部件、状态管理以及平台集成功能，构建高性能的跨平台应用程序。
metadata: {"clawdbot":{"emoji":"🦋","requires":{"bins":["flutter"]},"os":["linux","darwin","win32"]}}
---

# Flutter 开发规范

## 组件构建
- 使用 `const` 构造函数可以避免不必要的重新构建：对于不依赖于运行时值的组件，应使用 `const`。
- 将较大的 `build()` 方法拆分为更小的组件；辅助方法会导致每次调用时都重新构建组件，而组件本身可以跳过重新构建。
- 对于长列表，应使用 `ListView.builder`，而不要使用带有 `children` 的 `Column`——`Column` 会将所有内容一次性加载到内存中，而 `ListView.builder` 是惰性加载的。
- 当组件的标识性很重要时（例如需要保持列表顺序或在组件树结构变化时仍保留状态），必须为组件设置唯一键。
- 避免在 `build()` 方法内部调用 `setState`——这可能导致无限循环的重新构建。

## 状态管理
- 对于单个组件的局部状态，使用 `setState` 是可以的；但对于简单的切换或表单字段，无需过度设计状态管理逻辑。
- 只将状态提升到最低级别的共同祖先组件；过度提升状态会导致更广泛的组件重新构建。
- 对于简单的情况，`ValueNotifier` 结合 `ValueListenableBuilder` 可以提供更轻量级的状态管理方案。
- 使用 `Provider` 或 `Riverpod` 时，要保持提供者的简洁性；过于复杂的提供者会导致不必要的组件重新构建。
- 避免在状态中存储派生数据；应在 `build()` 方法中根据源状态计算派生数据。

## 性能优化
- `RepaintBoundary` 可以隔离耗时的重绘操作；对于复杂的动画或频繁更新的组件，应使用该机制。
- 带有 `const` 标签的组件会被全局缓存；在整个应用程序中，相同的 `const Text('Hello')` 实例是相同的。
- 使用 `AnimatedOpacity` 或 `FadeTransition` 实现动画效果；对于静态内容，可以使用颜色透明度来控制透明度。
- 对于图片，使用 `cacheWidth`/`cacheHeight` 标签来根据显示尺寸解码图片；使用全分辨率会浪费内存。
- 使用 `flutter run --profile` 可以查看真实的性能数据；调试模式下的性能测试结果可能慢10倍，且不具有代表性。

## 常见错误
- `FutureBuilder` 会在父组件重新构建时被重新构建；应将 `Future` 对象缓存到 `initState` 中，避免在代码中直接创建。
- `MediaQuery.of(context)` 会在媒体环境发生变化时触发重新构建；应使用具体的查询方法（如 `MediaQuery.sizeOf(context)`）。
- 在使用 `await` 后调用 `setState` 之前，应先检查组件是否已成功挂载（`mounted`）；否则组件可能已被销毁。
- `TextEditingController` 需要在 `dispose` 方法中释放资源；应在 `initState` 中创建并在 `dispose` 方法中释放它，切勿在 `build` 方法中操作。
- 嵌套的 `SingleChildScrollView` 如果其子组件数量不受限制，可能会导致问题；应使用 `ConstrainedBox` 或 `shrinkWrap` 来限制子组件的大小。

## 导航
- 使用 Go Router 或 Navigator 2.0 来处理深度链接和网页导航；基础版本的 Navigator 无法正确处理 URL。
- 通过路由参数传递数据，而不是通过构造函数参数传递数据；这样可以在应用程序重启或共享 URL 时保持数据的一致性。
- 避免将导航状态存储在全局状态管理中；路由系统会自动处理导航状态，否则可能导致同步问题。
- 使用 `WillPopScope`（或在 Flutter 3.16 及更高版本中使用 `PopScope`）来处理返回按钮操作；在丢弃未保存的更改之前请先确认用户操作。

## 平台集成
- 平台相关的操作是异步的；在同步的组件生命周期方法中使用时，需要使用 `then` 或 `await` 来处理异步操作。
- 在使用平台功能之前，请先请求相应的权限；如果权限被拒绝，要优雅地处理这种情况，不要假设权限总是被授予。
- 平台特定的代码应放在带有 `.android.dart` 或 `.ios.dart` 后缀的单独文件中；通过条件导入来保持代码的整洁性。
- 在真实设备上进行测试；模拟器无法准确模拟权限对话框、性能特性和传感器行为。

## 构建与发布
- 使用 `flutter clean` 可以解决大多数无法解释的构建失败问题；派生文件经常会被损坏。
- 在 iOS 环境中，如果 CocoaPods 出现问题，可以使用 `pod deintegrate && pod install` 来重新安装依赖项；这比调试依赖项更快。
- 通过设置不同的 `flavors` 或 `schemes` 来切换开发环境；不要硬编码 API 地址，可以使用 `--dart-define` 或特定环境的配置文件。
- 对于发布版本，可以使用混淆选项（`--obfuscate --split-debug-info`）来保护业务逻辑；但为了生成崩溃报告，仍需要保留调试符号。
- `flutter build` 默认使用发布模式；虽然不需要 `--release` 标志，但调试版本需要使用 `--debug` 标志。

## 测试
- 组件测试比集成测试更快；对于 UI 逻辑，应优先使用组件测试；对于复杂的业务流程，可以使用集成测试。
- `pumpAndSettle` 方法会等待动画完成；但对于无限循环的动画，应使用 `pump(duration)` 方法。
- 使用 `TestDefaultBinaryMessengerBinding` 来模拟平台相关的操作；真实的平台通道在测试中可能会失败。
- 金标准测试（Golden Tests）可以检测视觉上的回归问题；当有意图的更改发生时，可以使用 `--update-goldens` 命令重新生成测试数据。