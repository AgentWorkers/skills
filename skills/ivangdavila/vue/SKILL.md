---
name: Vue
slug: vue
version: 1.0.1
description: 使用 Composition API、正确的反应式编程模式以及适用于生产环境的组件来构建 Vue 3 应用程序。
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要具备Vue相关的专业知识时，无论是组合API模式还是生产环境下的性能优化，都可以使用该工具。该工具负责处理数据的响应式更新、组件设计、状态管理以及性能优化等方面。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 数据响应式模式 | `reactivity.md` |
| 组件模式 | `components.md` |
| 可组合函数的设计 | `composables.md` |
| 性能优化 | `performance.md` |

## 组合API的设计理念

- 组合API的目的并非取代Options API，而是为了实现更清晰、更易于维护的代码结构。
- 应按功能对代码进行分组，而非按选项类型分组——相关逻辑应保持在一起。
- 将可复用的逻辑提取为可组合函数（composables），这是组合API的主要优势。
- 推荐使用`<script setup>`语法——代码更简洁，性能也更好。

## 常见的使用陷阱

- 对于基本数据类型（如字符串、数字等），应使用`ref`进行封装，并通过`.value`访问其值；在模板中可以直接使用该值。
- `reactive`函数不能用于重新赋值整个对象，否则会破坏数据的响应式特性。
- 对`reactive`对象进行解构操作会使其失去响应式特性，应使用`toRefs(state)`来保留响应性。
- 在Vue 3中，对数组索引的赋值是响应式的；而在Vue 2中则不行（例如：`arr[0] = x`）。
- 在`reactive`对象中嵌套`ref`时，需要特别注意：`reactive({count: ref(0)}).count`返回的是一个数字，而不是一个`ref`对象。

## `watch`与`computed`的区别

- `computed`用于计算属性，其值会被缓存，只有在依赖项发生变化时才会重新计算。
- `watch`用于处理副作用，当依赖项发生变化时需要执行某些操作。
- `computed`函数应该是纯函数（没有副作用，也不能包含异步操作）。
- `watchEffect`用于立即响应依赖项的变化，并自动跟踪依赖项的变化。

## 使用`watch`时的注意事项

- 如果需要监视一个响应式对象，必须设置`deep: true`；或者直接监视一个getter函数。
- `watch`默认是延迟执行的（lazy），如果需要在组件初始化时立即执行，应设置`immediate: true`。
- `watch`的回调函数会接收到旧值和新值，格式为`watch(source, (newVal, oldVal) => {}`。
- `watchEffect`无法访问旧值，如果需要比较新旧值，应使用`watch`。
- 可以通过返回的函数来停止监听：`const stop = watch(...); stop()`。

## 属性（props）与事件（emits）的注意事项

- 使用`defineProps`来定义类型安全的属性：`defineProps<{ msg: string }()`。
- 属性应该是只读的（不可被修改），需要时可以向父组件发送事件：`defineEmits<{ (e: 'update', val: string): void }()`。
- `v-model`实际上是`:modelValue`和`@update:modelValue`的组合；可以通过`defineModel()`来自定义`v-model`行为。
- 对于对象类型的属性，其默认值必须是一个工厂函数：`default: () => ({})`。

## 模板中的`ref`使用注意事项

- `ref="name"`和`const name = ref(null)`之间的写法是错误的，`ref`和`name`必须完全匹配。
- 模板中的`ref`在组件挂载（`mounted`）之后才能使用，不能在`setup`阶段访问。
- `ref`作用于组件时，返回的是组件的实例；作用于元素时，返回的是对应的DOM元素。
- 使用`v-for`遍历数组时，每个元素都会生成一个`ref`。

## 生命周期钩子（lifecycle hooks）的注意事项

- `onMounted`钩子在组件挂载到DOM后执行，用于访问DOM。
- `onUnmounted`钩子在组件卸载前执行，用于清理资源（如订阅、定时器、事件监听器等）。
- `onBeforeMount`钩子在DOM插入之前执行，虽然不常用，但确实存在。
- 所有的生命周期钩子都必须在`setup`阶段同步调用，不能在回调函数或条件语句内部调用。
- 如果`setup`函数包含异步操作，需要使用`<Suspense>`来确保代码的正确执行。

## 数据提供（provide）与注入（inject）的注意事项

- 在父组件中使用`provide('key', value)`来提供数据；在任何子组件中可以使用`inject('key')`来获取这些数据。
- 如果提供的值是`ref`或`reactive`类型的，那么这些数据也是响应式的；否则，它们只是静态的值。
- 属性的默认值可以通过工厂函数来定义：`inject('key', defaultVal)`。
- 使用符号作为键名可以避免键名冲突。

## Vue Router的使用注意事项

- 使用`useRoute`来获取当前路由信息，应在`setup`阶段使用。
- 使用`useRouter`来处理导航操作，例如`router.push('/path')`。
- 路由守卫（navigation guards）包括`beforeEach`、`beforeResolve`和`afterEach`；如果需要取消导航操作，可以返回`false`。
- 使用`<RouterView>`来展示多个路由对应的视图。

## 常见错误

- `v-if`用于条件渲染，会从DOM中移除元素；`v-show`用于切换元素的显示状态。
- 在`v-for`循环中，必须为每个元素指定`key`属性：`v-for="item in items" :key="item.id"`。
- 事件修饰器的顺序很重要：`.prevent.stop`和`.stop.prevent`的效果不同。
- 使用`<Teleport>`组件时，要注意其渲染位置（例如：`<Teleport to="body">`会在组件树之外渲染内容）。