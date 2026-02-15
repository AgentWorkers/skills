---
name: Storybook
description: 使用正确的参数（args）、控制机制（controls）、装饰器（decorators）以及测试模式（testing patterns）来构建组件相关的故事（component stories）。
metadata: {"clawdbot":{"emoji":"📖","requires":{"bins":["npx"]},"os":["linux","darwin","win32"]}}
---

## CSF 格式（Component Story Format）

- 默认导出的是组件的元数据，包括标题、组件名称、参数以及装饰器。
- 带有名称的导出内容会被视为独立的故事（stories），并显示在侧边栏中。
- 使用 `satisfies Meta<typeof Component>` 进行 TypeScript 类型检查。
- CSF3 使用对象语法进行定义，而不是函数语法（例如：`export const Primary = { args: {...} `）。

## 参数（Args）与参数类型（ArgTypes）

- `args` 是传递给组件的实际属性值（例如：`args: { label: 'Click me' }`）。
- `argTypes` 用于配置控件的用户界面（例如：`argTypes: { size: { control: 'select', options: ['sm', 'lg'] }`）。
- 元数据中的默认参数会应用于所有相关故事；可以在个别故事中对其进行覆盖。
- `argTypes: { onClick: { action: 'clicked' } }` 会自动将点击事件记录到 Actions 面板中。

## 控件（Controls）

- 控件的类型会由 TypeScript 的属性自动推断：布尔值会被转换为切换按钮（toggle），字符串会被转换为文本输入框。
- 可以自定义控件类型（例如：`argTypes: { color: { control: 'color' }`）。
- 可以禁用某个控件（例如：`argTypes: { children: { control: false }`）。
- 选择框的选项配置（例如：`control: { type: 'select', options: ['a', 'b', 'c']`）。

## 装饰器（Decorators）

- 用于为故事添加额外的功能或上下文（例如：提供数据源、布局框架、主题样式）。
- 在组件的元数据中定义装饰器：`decorators: [(Story) => <Provider><Story /></Provider>]`。
- 在 `.storybook/preview.js` 文件中定义全局装饰器，这些装饰器会应用于所有故事。
- 装饰器的应用顺序很重要：后面的装饰器会覆盖前面的装饰器。

## 播放功能（Play Functions）

- 在故事内部实现交互式测试：`play: async ({ canvasElement }) => {...}`。
- 使用 `@storybook/testing-library` 进行查询（例如：`within(canvasElement).getByRole()`）。
- 通过 `await userEvent.click(button)` 模拟用户操作。
- 使用 `expect(element).toBeVisible()` 进行断言（测试在浏览器中执行）。

## 动作（Actions）

- `argTypes: { onClick: { action: 'clicked' }` 会自动将点击事件记录到 Actions 面板中。
- 也可以从外部导入动作功能（例如：`import { action } from '@storybook/addon-actions'`）。
- 在 Storybook 8 及更高版本中，可以使用 `@storybook/test` 提供的 `fn()` 函数来监视播放过程中的事件。

## 故事组织结构（Story Organization）

- 故事的标题路径决定了其层级结构（例如：`title: 'Components/Forms/Button'`）。
- 故事按照导出的顺序显示，通常将主要组件（Primary）放在最前面。
- 使用 `tags: ['autodocs']` 可以自动生成文档页面。
- `parameters: { docs: { description: { story: 'text' } }` 可以为故事添加描述信息。

## 常见模式（Common Patterns）

- **默认状态（Default State）**：`export const Default = {}`。
- **包含所有属性的状态（With All Props）**：`export const WithIcon = { args: { icon: <Icon /> }`。
- **边缘情况（Edge Cases）**：将空状态、加载状态、错误状态、禁用状态分别作为独立的故事来处理。
- **响应式布局（Responsive Layout）**：根据需要为每个故事配置 viewport 插件参数。

## 渲染功能（Render Functions）

- 自定义渲染逻辑：`render: (args) => <Wrapper><Component {...args} />`。
- 在渲染函数中可以访问上下文数据（例如：`render: (args, { globals }) => ...`）。
- 当故事需要与默认渲染逻辑不同的 JSX 结构时，可以使用这种方式。
- 通常建议使用装饰器来添加额外功能，而使用 `render` 函数来进行结构调整。

## 配置（Configuration）

- `.storybook/main.js` 文件用于配置插件、框架以及故事文件的查找规则。
- `.storybook/preview.js` 文件用于定义全局装饰器、参数类型（argTypes）。
- 故事文件的查找路径：`stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)']`。
- 静态资源（如图片、字体文件）存储在 `staticDirs: ['../public']` 中。

## 常见错误（Common Mistakes）

- 忘记安装插件并将其添加到 `.storybook/main.js` 文件的插件数组中。
- 使用已被弃用的 `storiesOf` API，应改用 CSF 格式的导出方式。
- 如果元数据中缺少组件信息，相关控件将无法自动生成。
- 装饰器在返回故事对象时，应确保调用 `Story` 构造函数（例如：`(Story) => <Story />` 而不是 `(Story) => `）。