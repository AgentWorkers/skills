---
name: Vue
description: 避免常见的 Vue 开发错误——比如反应式编程中的陷阱、`ref`与`reactive`属性的混淆、计算属性的时机选择不当，以及 Composition API 的使用误区。
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 反应式系统（Reactivity System）
- 对于基本数据类型（如字符串、数字等），使用 `ref`，在脚本中可以通过 `.value` 访问其值；在模板中会自动解包（即不需要使用 `.value`）。
- 对于对象，使用 `reactive`，虽然不能直接通过 `.value` 访问对象值，但也不能重新赋值整个对象。
- 对 `reactive` 对象进行解构操作会破坏其反应性（即不再响应状态变化），需要使用 `toRefs(state)` 来保持其反应性。
- 在 Vue 3 中，对数组索引的赋值是反应式的（例如 `arr[0] = x` 是有效的），这与 Vue 2 不同。

## `ref` 与 `reactive` 的区别：
- `ref` 可以存储任何类型的值（包括对象），在脚本中必须使用 `.value` 来访问其值。
- `reactive` 仅用于对象，返回的是一个 `Proxy` 对象，因此引用的是原始对象本身。
- `ref` 在模板中会自动解包，例如 `{{ count }}` 而不是 `{{ count.value }}`。
- 嵌套的 `ref` 也需要使用 `reactive` 来保持反应性，例如 `reactive({ count: ref(0) })`。

## 计算属性（Computed Properties）与观察者（Watchers）
- 计算属性会被缓存，只有在依赖项发生变化时才会重新计算。
- 计算属性应该是纯函数（即没有副作用），如果需要副作用，应该使用 `watch`。
- `watch` 默认是延迟执行的（异步的），可以通过 `immediate: true` 来使其在初始化时立即执行。
- `watchEffect` 会立即执行，并自动跟踪依赖项的变化，无需手动指定依赖项。

## 使用观察者时的注意事项：
- 如果需要观察一个反应式对象的所有属性，需要使用 `deep: true`：`watch(state, cb, { deep: true })` 或 `watch(() => state.prop, cb)`。
- 观察者回调会接收到新旧值：`watch(source, (newVal, oldVal) => {})`。
- `watchEffect` 无法访问旧值，如果需要访问旧值，应该使用 `watch`。
- 可以通过返回的函数来停止观察者：`const stop = watch(...); stop()`。

## 属性（Props）与事件（Emits）
- 使用 `defineProps` 来定义类型安全的属性：`defineProps<{ msg: string }()`。
- 属性是只读的，不能被修改，修改时需要向父组件发射事件。
- 使用 `defineEmits` 来定义类型安全的事件：`defineEmits<{ (e: 'update', val: string): void }()`。
- `v-model` 是 `:modelValue` 和 `@update:modelValue` 的组合，可以通过 `defineModel()` 来自定义。

## 模板中的引用（Template References）
- `ref="name"` 创建后，可以通过 `const name = ref(null)` 来获取该引用；该引用在组件挂载后（`onMounted` 之后）才可用。
- 组件上的 `ref` 指向的是组件实例，元素上的 `ref` 指向的是 DOM 元素。
- 在 `v-for` 循环中使用 `ref` 时，`ref` 会被转换为数组形式。

## 生命周期钩子（Lifecycle Hooks）：
- `onMounted`：组件挂载到 DOM 上时执行。
- `onUnmounted`：组件卸载时执行，用于清理订阅和定时器等资源。
- `onBeforeMount`：在 DOM 插入之前执行，但很少需要使用。
- 所有生命周期钩子都必须在 `setup` 函数中调用，不能在回调函数或条件语句中调用。

## 数据提供（Provide）与注入（Inject）
- 在父组件中使用 `provide('key', value)` 来提供数据；在子组件中使用 `inject('key')` 来获取数据。
- 如果提供的值是 `ref` 或 `reactive` 类型，那么数据是响应式的；否则是静态的。
- 可以通过第三个参数 `defaultVal` 来指定默认值。
- 使用符号作为键名可以避免键名冲突。

## Vue 路由（Vue Router）
- `useRoute` 用于获取当前路由信息，可以在 `setup` 函数中使用。
- `useRouter` 用于导航，例如 `router.push('/path')`。
- 路由守卫（Navigation Guards）：`beforeEach`、`beforeResolve`、`afterEach`，可以通过返回 `false` 来取消导航。
- 使用 `<RouterView>` 可以展示多个路由对应的视图。

## 常见错误：
- 异步的 `setup` 函数需要使用 `<Suspense>`，因为异步函数会导致组件挂载延迟。
- `v-if` 和 `v-show` 的区别：`v-if` 会从 DOM 中移除元素，而 `v-show` 只是切换元素的显示状态。
- 在 `v-for` 循环中，需要为每个元素指定唯一键：`v-for="item in items" :key="item.id"`。
- 事件修饰器的顺序很重要：`.prevent.stop` 应该放在 `.stop` 之前。
- 使用 `<Teleport>` 组件可以将元素传送到组件树之外的位置。