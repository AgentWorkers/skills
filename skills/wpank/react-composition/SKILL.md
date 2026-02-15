---
name: react-composition
model: standard
description:
  React composition patterns for scalable component architecture. Use when
  refactoring components with boolean prop proliferation, building flexible
  component libraries, designing reusable component APIs, or working with
  compound components and context providers.
version: "1.0"
---

# React 组合模式

这些组合模式用于构建灵活且易于维护的 React 组件。通过使用复合组件、提取状态（state lifting）以及组合内部逻辑（composing internals），可以避免布尔属性（boolean props）的过度使用。这些模式有助于提升代码库的可维护性，尤其是在组件规模扩大时。

## 适用场景

- 重构具有多个布尔属性的组件
- 构建可重用的组件库
- 设计灵活的组件 API
- 使用复合组件或上下文提供者（context providers）

## 模式概述

| 编号 | 模式                          | 影响程度   |
|---|----------------------------|----------|
| 1   | 避免使用布尔属性                  | 非常重要   |
| 2   | 使用复合组件                      | 非常重要   |
| 3   | 上下文接口（依赖注入，Dependency Injection）   | 非常重要   |
| 4   | 提取状态                        | 非常重要   |
| 5   | 明确的组件变体                    | 一般重要   |
| 6   | 使用 `children` 而非 `renderX` 属性       | 一般重要   |

## 安装说明

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-composition
```


---

## 1. 避免使用布尔属性

不要为了自定义组件行为而添加诸如 `isThread`、`isEditing`、`isDMThread` 等布尔属性。每个布尔属性都会导致状态数量翻倍，并引发难以维护的条件逻辑。应优先使用组合模式来解决问题。

```tsx
// BAD — boolean props create exponential complexity
function Composer({ isThread, isDMThread, isEditing, isForwarding }: Props) {
  return (
    <form>
      <Input />
      {isDMThread ? <AlsoSendToDMField /> : isThread ? <AlsoSendToChannelField /> : null}
      {isEditing ? <EditActions /> : isForwarding ? <ForwardActions /> : <DefaultActions />}
    </form>
  )
}

// GOOD — composition eliminates conditionals
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer><Composer.Attachments /><Composer.Submit /></Composer.Footer>
    </Composer.Frame>
  )
}

function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer><Composer.Submit /></Composer.Footer>
    </Composer.Frame>
  )
}
```

每个组件变体都明确地说明了它应该渲染什么内容。组件内部逻辑是共享的，但不需要依赖于一个庞大的父组件。

## 2. 使用复合组件

使用复合组件来构建复杂的组件结构。每个子组件通过上下文（context）来访问状态，而不是通过属性（props）。可以将这些复合组件导出为一个命名空间对象（namespace object）。

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return <ComposerContext value={{ state, actions, meta }}>{children}</ComposerContext>
}
function ComposerInput() {
  const { state, actions: { update }, meta: { inputRef } } = use(ComposerContext)
  return <TextInput ref={inputRef} value={state.input}
    onChangeText={(t) => update((s) => ({ ...s, input: t }))} />
}

const Composer = {
  Provider: ComposerProvider, Frame: ComposerFrame,
  Input: ComposerInput, Submit: ComposerSubmit, Footer: ComposerFooter,
}

// Consumers compose exactly what they need
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Footer><Composer.Formatting /><Composer.Submit /></Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

## 3. 通用上下文接口（依赖注入）

定义一个包含 `state`、`actions` 和 `meta` 的通用接口。任何提供者（provider）都必须实现这个接口，这样相同的 UI 就可以适应不同的状态实现。只有提供者知道状态是如何被管理的。

```tsx
interface ComposerContextValue {
  state: { input: string; attachments: Attachment[]; isSubmitting: boolean }
  actions: { update: (fn: (s: ComposerState) => ComposerState) => void; submit: () => void }
  meta: { inputRef: React.RefObject<TextInput> }
}

// Provider A: Local state for ephemeral forms
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  return (
    <ComposerContext value={{ state, actions: { update: setState, submit: useForwardMessage() },
      meta: { inputRef: useRef(null) } }}>{children}</ComposerContext>
  )
}

// Provider B: Global synced state for channels
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  return (
    <ComposerContext value={{ state, actions: { update, submit },
      meta: { inputRef: useRef(null) } }}>{children}</ComposerContext>
  )
}
```

更换提供者（provider）后，UI 仍然可以正常使用。相同的 `Composer.Input` 可以适用于不同的提供者。

## 4. 将状态提取到提供者中

将状态移至专门的提供者组件中，这样主 UI 之外的兄弟组件就可以直接访问和修改状态，而无需通过属性或引用（refs）进行传递。

**关键点：** 需要共享状态的组件并不一定需要在视觉上嵌套在一起——它们只需要位于同一个提供者的范围内即可。

## 5. 明确的组件变体

不要使用一个包含多个布尔属性的组件，而是创建多个明确的组件变体。每个变体只包含它所需的功能，从而实现自文档化（self-documentation），避免出现无法处理的状态组合。

```tsx
// BAD — what does this render?
<Composer isThread isEditing={false} channelId="abc" showAttachments showFormatting={false} />

// GOOD — immediately clear
<ThreadComposer channelId="abc" />
<EditMessageComposer messageId="xyz" />
<ForwardMessageComposer messageId="123" />
```

每个组件变体都明确指定了它所依赖的提供者（provider）、状态（state）、UI 元素（UI elements）以及可执行的操作（actions）。

## 6. 使用 `children` 而非 `renderX` 属性

在组合组件时，应使用 `children` 而不是 `renderX` 属性。这样代码更易于阅读，也更符合 React 的设计原则。

**使用 `renderX` 属性的情况：** 当父组件需要将数据传递给子组件时（例如：`renderItem(({ item, index }) => ...}`）。

## 决策指南

1. **组件具有 3 个或更多布尔属性？** → 创建明确的组件变体（模式 1 和 5）
2. **组件具有 `render` 属性？** → 将其转换为复合组件（模式 2 和 6）
3. **兄弟组件需要共享状态？** → 将状态提取到提供者中（模式 4）
4. **相同的 UI，但数据来源不同？** → 使用通用上下文接口（模式 3）
5. **正在构建组件库？** → 将所有这些模式结合使用