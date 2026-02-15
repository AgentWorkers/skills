---
name: ant_design_skill
description: 使用 Ant Design (antd) 构建 React UI 的前端设计技能：组件模式、布局、表单、表格，以及通过 ConfigProvider 实现的主题/样式管理。
---

# Ant Design (React) — 实用的前端设计技能

当您使用 **Ant Design (antd)** 构建 React UI 时，如果希望快速获得一致且美观的界面布局，可以使用这项技能。

## 适用场景
- 项目基于 **React** + **Ant Design** 开发。
- 需要设计或实现包含以下组件的页面：**布局（Layout）**、**菜单（Menu）**、**表单（Form）**、**表格（Table）**、**模态框（Modal）**、**侧边栏（Drawer）**、**步骤流程（Steps）**、**标签页（Tabs）**、**分页（Pagination）**。
- 需要自定义 **主题样式**（如颜色、圆角、字体样式、间距等）。
- 希望界面遵循统一的模式（例如 CRUD 界面、仪表盘、设置页面等）。

## 默认工作流程（按此顺序操作）
1. 确认所使用的组件库及 Ant Design 的版本（假设为 v5 或更高版本）。
2. 选择页面类型：
   - CRUD 界面（表格 + 表单 + 操作按钮，通常位于模态框或侧边栏中）
   - 向导式界面（包含多个步骤）
   - 设置页面（表单 + 卡片布局）
   - 仪表盘界面（网格布局 + 图表）
3. 首先构建页面的基本结构：
   - **布局**：`Layout` + **侧边栏（Sider）** + **页眉（Header）** + **主要内容区域（Content）**
   - 使用 **菜单** 实现导航功能。
4. 构建主要的交互组件：
   - **表单组件**：`Form`、`Form.Item`、`Input`、`Select`、`DatePicker`、`Switch`
   - **表格组件**：`Table`（包含列定义和行操作按钮）
5. 添加反馈机制：
   - 显示错误信息、通知提示或确认提示（`message`、`notification`、`Modal.confirm`）
6. 通过 `ConfigProvider`（全局配置）和组件级别的样式覆盖来应用主题样式。
7. 验证页面在不同状态下的显示效果：
   - 空页面状态
   - 加载状态
   - 错误状态
   - 移动设备上的响应式布局（至少保证在 360px 宽度下正常显示）

## 组件设计模式（可直接复制使用）
### 布局
- 使用 `Layout` 结构，搭配可折叠的 **侧边栏（Sider）** 和用于顶部操作的 **页眉（Header）**，确保主要内容区域可滚动。
- 将页面标题和主要操作按钮放在一个 `Flex` 或 `Space` 元素中。

### 表单
- 保持表单元素的垂直排列；统一对齐标签的位置。
- 使用 `Form` 和 `Form.Item` 来处理表单验证逻辑；除非必要，否则避免自定义验证逻辑。
- 使用 `Form.useForm()` 和 `form.setFieldsValue()` 来管理表单数据的编辑流程。

### 表格（CRUD 功能）
- 表格列的布局：
  - 左侧：标识符/名称
  - 中间：重要属性
  - 右侧：操作按钮（编辑/删除）
- 必须使用 `rowKey` 来唯一标识每行数据。
- 对于实际应用，建议使用服务器端分页功能。

### 模态框/侧边栏
- 使用 **Modal** 来展示简短的表单内容。
- 使用 **Drawer** 来展示较长的表单内容，或者当需要保持上下文信息时。

## 主题样式 / 设计元素（AntD v5）
Ant Design v5 支持 **设计元素（Design Tokens）** 和 **CSS-in-JS** 的方式来定制样式。

### 全局主题设置
使用 `ConfigProvider` 来统一应用整个应用程序的主题样式：

```tsx
import { ConfigProvider, theme } from 'antd';

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1677ff',
          borderRadius: 10,
          fontSize: 14,
        },
        components: {
          Button: { controlHeight: 40 },
          Layout: { headerBg: '#ffffff' },
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
}
```

### 暗黑模式
启用 `theme.darkAlgorithm` 并确保所有相关样式的一致性：

```tsx
const isDark = true;

<ConfigProvider
  theme={{
    algorithm: isDark ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: { colorPrimary: '#7c3aed' },
  }}
/>
```

### 组件级别的样式覆盖
通过 `components.<ComponentName>` 来对特定组件（如按钮、输入框、表格等）进行个性化定制。

## 参考资源
- 阅读 **README.md** 以获取完整的使用指南（包括配置方法、设计模式和示例代码）。
- 如果需要基于大型语言模型（LLM）自动生成 UI 代码，可以参考 `protocols/` 目录。
- 了解各种主题样式的详细信息，请查阅 `references/tokens.md`。
- 查看实用的页面设计示例（如 CRUD 界面、设置页面、向导界面等），请参考 `references/components.md`。
- 如果需要一个可立即使用的 Vite + React + Ant Design 模板项目，请使用 `starter/` 目录。

## 注意事项
- 建议使用 Ant Design v5 及更高版本；如果项目使用的是 v4 版本（样式变量较少），请暂停使用并咨询相关团队。
- 尽量使用内置的组件和设计模式，避免过度自定义 CSS。
- 避免过度自定义主题样式：仅在实际需要时才对特定组件进行样式覆盖。