---
name: iOS
description: 使用 Swift、Xcode 以及 App Store 的最佳实践来构建、测试和发布 iOS 应用程序。
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["xcodebuild"]},"os":["darwin"]}}
---

# iOS 开发规范

## Xcode 与构建
- 清理构建文件夹（Cmd+Shift+K）可以解决大多数“无法构建”的问题——派生数据经常会损坏。
- 重置模拟器（设备 > 删除所有内容和设置）可以清除在重新安装后仍然存在的缓存应用状态。
- 归档构建应使用“发布”（Release）配置文件——仅在生产环境中出现的错误通常源于优化差异。
- 使用 `xcodebuild -showsdks` 可以列出可用的 SDK——当构建失败并提示“找不到 SDK”时非常有用。
- 并行构建可能会导致脚本执行过程中的竞争条件（race conditions）——需要添加输入/输出文件列表来确保执行顺序正确。

## 代码签名
- “没有签名证书”通常意味着证书已过期或被撤销——请在 Keychain Access 中检查证书状态，而不仅仅是 Xcode。
- 配置文件（provisioning profiles）中会嵌入设备的 UDID——新的测试设备需要重新生成配置文件并重新安装应用。
- 在持续集成（CI）环境中自动签名可能会失败——请始终使用手动签名，并使用导出的凭据进行构建。
- 每个账户只能使用 3 个分发证书（distribution certificates）——不要创建新的证书，而是导出并共享现有的证书。
- 证书更新后，需要更新所有使用旧证书的配置文件。

## SwiftUI 开发模式
- `@State` 用于视图本地数据，`@StateObject` 用于可观察对象（ObservableObjects），`@ObservedObject` 用于传入的对象——错误使用这些属性会导致程序崩溃或状态丢失。
- 在非哈希类型（non-Hashable types）上使用 `List` 与 `id: \.self` 会导致程序无声崩溃——请始终使用明确的 `id` 参数和稳定的标识符。
- `task` 修饰符会在视图消失时自动取消任务——无需手动取消任务，但需要在循环中检查 `Task.isCancelled` 的值。
- 预览模式下的网络请求可能会导致程序无声崩溃——请使用模拟数据或依赖注入（dependency injection）来处理网络请求。
- 在预览模式下，`@Environment` 的值默认为 `nil`——请确保在预览环境中设置相应的环境变量。

## App Store 提交规范
- 应用程序必须支持离线使用或能够清晰地显示离线状态——无声的错误会导致应用被拒绝。
- 如果应用程序包含非账户相关的功能，登录功能应该是可选的——审核者会拒绝强制要求用户登录的应用程序。
- 如果应用程序提供第三方社交登录功能，必须使用“使用 Apple 登录”（Sign in with Apple）——没有例外。
- 隐私标签必须与实际的数据收集方式一致——Apple 会验证标签的准确性，不匹配的情况会导致应用被拒绝。
- 应用内购买必须使用 StoreKit 来处理数字商品——外部支付链接会导致应用被拒绝。

## Info.plist 文件要求
- 设置 `ITSAppUsesNonExemptEncryption = NO` 可以避免大多数应用程序的合规性问题——这可以避免每天的麻烦。
- 必须提供相机、麦克风和位置功能的用途说明——缺少这些说明会导致应用程序在尝试使用这些功能时崩溃。
- 在调用 `canOpenURL` 之前，必须先在 `LSApplicationQueriesSchemes` 中列出可用的 URL 方式——这是 iOS 9 及更高版本的安全要求。
- 在 iPad 上设置 `UIRequiresFullScreen = YES` 可以避免应用程序进入多任务模式——只有在应用程序确实无法支持分屏显示时才使用此设置。

## 性能优化
- 使用 `Instruments > Time Profiler` 可以找到实际的性能瓶颈——不要猜测，而是通过测量来找出问题。
- Assets.xcassets 文件中的图片会自动进行优化——而捆绑包中的图片则不会被优化。
- 使用 `@MainActor` 注解可以确保 UI 更新在主线程（main thread）上执行——缺少此注解会导致应用程序在负载情况下随机崩溃。
- 内存泄漏通常隐藏在闭包（closures）中——对于引用 `self` 的闭包，请使用 `[weak self]` 来避免内存泄漏。
- 包含数千条数据的 `List` 显示速度较快，而在 `ScrollView` 中使用 `ForEach` 时速度较慢——`List` 会复用列表项，而 `ScrollView` 会一次性加载所有数据。

## 调试技巧
- 在 LLDB 中使用 `po` 可以打印对象描述，使用 `p` 可以打印原始值——大多数调试场景下建议使用 `po`。
- 控制台中的紫色警告表示主线程出现了问题——请修复这些问题，否则会导致应用程序运行不稳定。
- 在启动参数中添加 `-com.apple.CoreData.SQLDebug 1` 可以显示所有的 Core Data 查询操作——这对于调试数据获取性能至关重要。
- 没有符号的崩溃日志毫无用处——请为每个发布版本保留 dSYM 文件。
- TestFlight 中的崩溃信息会显示在 Xcode Organizer 中——请在那里查看错误信息，而不仅仅是 App Store Connect 中。