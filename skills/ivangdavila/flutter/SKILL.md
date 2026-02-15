---
name: Flutter
slug: flutter
version: 1.0.1
description: 构建可靠的 Flutter 应用程序时，需要避免状态丢失、组件重建带来的问题以及异步编程中的陷阱。
metadata: {"clawdbot":{"emoji":"🐦","requires":{"bins":["flutter"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| `setState`、状态丢失、键（keys） | `state.md` |
| 构建方法（build method）、上下文（context）、` GlobalKey` | `widgets.md` |
| `FutureBuilder`、`dispose`、`mounted` | `async.md` |
`pop` 操作后的上下文（context after pop）、深度链接（deep linking） | `navigation.md` |
`const`、重新构建（rebuilds）、性能（performance） | `performance.md` |
| 平台通道（platform channels）、空值安全性（null safety） | `platform.md` |

## 重要规则

- 在调用 `setState` 之前，请确保 `dispose` 已执行完毕；否则会导致程序崩溃。
- 如果列表项缺少键（key），重新排序会破坏状态（state），请始终使用键（keys）。
- 当父组件重新构建（parent rebuild）时，`FutureBuilder` 会自动重新构建；请缓存相关的 `Future` 对象。
- 在异步操作（async operation）之后使用 `BuildContext`；此时上下文可能无效，请先检查 `mounted` 是否已触发。
- 使用 `const` 构造函数可以防止组件被重新构建，适用于静态组件（static widgets）。
- 当 `StatefulWidget` 被重新创建时（例如键（key）发生变化或父组件重新构建时），会生成新的状态（new state）。
- 使用 `PublicKey` 时请谨慎：不要仅仅为了访问状态而使用它，应通过回调函数（callbacks）来传递数据。
- 如果 `dispose` 没有完全执行，请取消定时器（timers）、订阅（subscriptions）和控制器（controllers）。
- 使用 `Navigator.pop` 时请处理返回的 `Future` 对象；不要忽略可能出现的错误。
- 如果 `ScrollController` 未被正确销毁，可能会导致内存泄漏（memory leak）。
- 图片缓存（image caching）请使用 `cached_network_image`；默认的缓存方式可能不会持久化数据。
- 如果没有捕获 `PlatformException`，平台相关的操作可能会引发异常（platform-related operations may throw exceptions）。