---
name: fosmvvm-react-view-generator
description: 生成能够渲染 FOSMVVM 视图模型的 React 组件。这些组件遵循 ViewModelView 模式，使用 Hooks、加载状态管理以及 TypeScript 类型进行开发。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "⚛️", "os": ["darwin", "linux"]}}
---

# FOSMVVM React 视图生成器

该工具用于生成能够渲染 FOSMVVM 视图模型的 React 组件。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考文档]({baseDir}/references/FOSMVVMArchitecture.md)

在 FOSMVVM 中，**React 组件仅作为渲染层**，用于展示视图模型（ViewModels）：

```
┌─────────────────────────────────────────────────────────────┐
│                    ViewModelView Pattern                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ViewModel (Data)          React Component                  │
│  ┌──────────────────┐     ┌──────────────────┐             │
│  │ title: String    │────►│ <h1>{vm.title}   │             │
│  │ items: [Item]    │────►│ {vm.items.map()} │             │
│  │ isEnabled: Bool  │────►│ disabled={!...}  │             │
│  └──────────────────┘     └──────────────────┘             │
│                                                              │
│  ServerRequest (Actions)                                     │
│  ┌──────────────────┐     ┌──────────────────┐             │
│  │ processRequest() │◄────│ <Component.bind  │             │
│  │                  │     │   requestType={} │             │
│  └──────────────────┘     └──────────────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**关键原则：** 组件不负责数据的转换或计算，它们仅渲染视图模型提供的数据。

---

## 组件名称与视图模型的对应关系

**组件的文件名必须与其渲染的视图模型相匹配。**

```
src/
  viewmodels/
    {Feature}ViewModel.js           ←──┐
    {Entity}CardViewModel.js        ←──┼── Same names
                                        │
  components/                           │
    {Feature}/                          │
      {Feature}View.jsx             ────┤  (renders {Feature}ViewModel)
      {Entity}CardView.jsx          ────┘  (renders {Entity}CardViewModel)
```

这种对应关系具有以下优势：
- **易查找性**：可以立即找到对应于任何视图模型的组件。
- **一致性**：遵循与 SwiftUI 和 Leaf 相同的命名规范。
- **可维护性**：视图模型的更改会直接反映在组件文件的位置上。

---

## TDD 开发流程

使用该工具时，**首先生成测试代码，然后再编写实现代码**：

```
1. Reference ViewModel and ServerRequest details from conversation context
2. Generate .test.js file → Tests FAIL (no implementation yet)
3. Generate .jsx file → Tests PASS
4. Verify completeness (both files exist)
5. User runs `npm test` → All tests pass ✓
```

**上下文感知**：该工具能够根据对话内容理解需求，无需进行文件解析或问答操作。

---

## 核心组件

### 1. `viewModelComponent()` 包装器

所有 React 组件都会被 `viewModelComponent()` 包装：

```jsx
const MyView = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return <div>{viewModel.title}</div>;
});

export default MyView;
```

**要求：**
- 使用全局命名空间中的 `FOSMVVM(viewModelComponent()`（通过 `<script>` 标签加载）。
- 组件函数接收一个名为 `{viewModel}` 的属性。
- 无需导入其他库——FOSMVVM 的辅助函数已通过 `<script>` 标签加载。

### 2. `.bind()` 模式

父组件通过 `.bind()` 方法来发起服务器请求（ServerRequests）：

```jsx
// Parent component
function Dashboard() {
  return (
    <div>
      <TaskList.bind({
        requestType: 'GetTasksRequest',
        params: { status: 'active' }
      }) />
    </div>
  );
}
```

**.bind() 模式的运作方式：**
- 子组件通过服务器请求接收数据。
- 父组件指定请求类型（`requestType`）和参数（`params`）。
- WASM 桥接层负责处理请求并传递给视图模型，进而驱动组件渲染。
- 该过程不涉及 `fetch()` 方法的调用，也不使用硬编码的 URL。

### 3. 错误视图模型的处理

错误视图模型与其他视图模型一样被正常渲染：

```jsx
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  // Handle error ViewModels
  if (viewModel.errorType === 'NotFoundError') {
    return (
      <div className="error">
        <p>{viewModel.message}</p>
        <p>{viewModel.suggestedAction}</p>
      </div>
    );
  }

  if (viewModel.errorType === 'ValidationError') {
    return (
      <div className="validation-error">
        <h3>{viewModel.title}</h3>
        <ul>
          {viewModel.errors.map(err => (
            <li key={err.field}>{err.message}</li>
          ))}
        </ul>
      </div>
    );
  }

  // Render success ViewModel
  return (
    <div className="task-card">
      <h3>{viewModel.title}</h3>
      <p>{viewModel.description}</p>
    </div>
  );
});
```

**关键原则：**
- 不使用通用的错误处理机制。
- 每种错误类型都有对应的视图模型。
- 组件会根据 `errorType` 属性条件性地进行渲染。
- 错误渲染仅涉及数据的展示。

### 4. 使用导航意图（而非硬编码的路径）

**导航方式：**
- 使用全局命名空间中的 `FOSMVVM.Link`（通过 `<script>` 标签加载）。
- 通过 `intent` 属性来导航，而不是使用硬编码的路径。
- 路由器负责将导航意图映射到相应的路由。
- 支持跨平台的导航功能。

---

## 组件分类

### 仅用于显示数据的组件

这类组件仅用于渲染数据，不支持用户交互：

```jsx
const InfoCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return (
    <div className="info-card">
      <h2>{viewModel.title}</h2>
      <p>{viewModel.description}</p>

      {viewModel.isActive && (
        <span className="badge">{viewModel.activeLabel}</span>
      )}
    </div>
  );
});

export default InfoCard;
```

**特点：**
- 仅渲染视图模型的数据。
- 不包含事件处理函数（如 `onClick`、`onSubmit` 等）。
- 可能根据视图模型的状态进行条件性渲染。
- 不会对子组件调用 `.bind()` 方法。

### 交互式组件

这类组件允许用户执行操作并触发服务器请求：

```jsx
const ActionCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return (
    <div className="action-card">
      <h2>{viewModel.title}</h2>
      <p>{viewModel.description}</p>

      <div className="actions">
        <button
          onClick={() => viewModel.operations.performAction()}
          disabled={!viewModel.canPerformAction}
        >
          {viewModel.actionLabel}
        </button>

        <button onClick={() => viewModel.operations.cancel()}>
          {viewModel.cancelLabel}
        </button>
      </div>
    </div>
  );
});

export default ActionCard;
```

### 列表组件

用于渲染数据集合的组件：

```jsx
const TaskList = FOSMVVM.viewModelComponent(({ viewModel }) => {
  if (viewModel.isEmpty) {
    return <div className="empty">{viewModel.emptyMessage}</div>;
  }

  return (
    <div className="task-list">
      <h2>{viewModel.title}</h2>
      <p>{viewModel.totalCount}</p>

      {viewModel.tasks.map(task => (
        <TaskCard.bind({
          requestType: 'GetTaskRequest',
          params: { id: task.id }
        }) />
      ))}
    </div>
  );
});

export default TaskList;
```

### 表单组件

包含验证功能的输入字段的组件：

```jsx
const SignInForm = FOSMVVM.viewModelComponent(({ viewModel }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();

    const result = await viewModel.operations.submit({
      email,
      password
    });

    if (result.validationErrors) {
      setErrors(result.validationErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>{viewModel.emailLabel}</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder={viewModel.emailPlaceholder}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label>{viewModel.passwordLabel}</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder={viewModel.passwordPlaceholder}
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>

      <button type="submit" disabled={viewModel.submitDisabled}>
        {viewModel.submitLabel}
      </button>
    </form>
  );
});

export default SignInForm;
```

---

## 适用场景

- 为 FOSMVVM 应用程序创建新的 React 组件。
- 构建用于渲染视图模型的用户界面。
- 将 Leaf 模板迁移到 React。
- 根据需求实现新的视图结构。
- 创建带有验证功能的表单。
- 构建由子组件组成的列表视图。

---

## 生成的内容

每次调用该工具时，会生成以下两个文件：

| 文件名 | 文件位置 | 用途 |
|------|----------|---------|
| `{ViewName}View.test.js` | `src/components/{Feature}/` | 使用 Jest 和 React 测试库编写的测试文件 |
| `{ViewName}View.jsx` | `src/components/{Feature}/` | 实际的 React 组件代码 |

**注意：** 相应的视图模型（ViewModel）和服务器请求（ServerRequest）文件需要预先存在（可以使用其他 FOSMVVM 生成工具来创建）。

---

## 项目结构配置

| 占位符 | 说明 | 示例 |
|-------------|-------------|---------|
| `{ViewName}` | 组件名称（去掉 “View” 后缀） | `TaskList`、`SignIn` |
| `{Feature}` | 组件功能/模块分组 | `Tasks`、`Auth` |

---

## 模式实现方式

该工具会根据对话内容来确定组件的结构：

### 组件类型识别

根据对话内容，工具可以识别：
- **视图模型的结构**（来自之前的讨论或 Claude 读取的规范）。
- **服务器请求的详细信息**（已包含在对话中）。
- **组件类型**：仅用于显示数据的组件、交互式组件、表单组件或列表组件。
- 需要处理的错误视图模型。

### 测试代码的生成（首先进行）

根据组件类型，生成 `.test.js` 文件，其中包含以下测试内容：
- **所有组件**：成功渲染视图模型时的测试。
- **交互式组件**：按钮点击、操作验证等。
- **表单组件**：输入字段的变化、验证错误、表单提交等。
- **列表组件**：空状态、多个项目、子组件的绑定等。

### 组件代码的生成（其次进行）

生成 `.jsx` 文件，遵循以下步骤：
1. 导入 `viewModelComponent()` 包装器。
2. 处理错误视图模型，并实现条件渲染。
3. 渲染成功状态下的视图模型。
4. 如果组件具有交互功能，添加相应的交互逻辑。
5. 如果组件包含表单，添加表单状态处理。
6. 如果组件是容器组件，添加对子组件的 `.bind()` 调用。
7. 导出包装后的组件代码。

### 信息来源

该工具的信息来源包括：
- 与用户之前的对话内容。
- 规范文件（如果 Claude 已经读取了相关规范）。
- 代码库中的视图模型定义。

### 第五步：验证完整性

检查以下内容：
- 是否存在 `.test.js` 和 `.jsx` 文件。
- 组件是否使用了 `FOSMVVM(viewModelComponent()` 包装器。
- 组件是否从全局命名空间中调用了 FOSMVVM 的函数。
- 测试是否覆盖了成功状态和错误状态下的组件行为。
- 如果有交互逻辑，测试是否能够正确处理用户操作。

---

## 关键模式

### 规则：组件中不应包含业务逻辑

```jsx
// ❌ BAD - Component is transforming data
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  const daysLeft = Math.ceil((viewModel.dueDate - Date.now()) / 86400000);
  return <span>{daysLeft} days remaining</span>;
});

// ✅ GOOD - ViewModel provides shaped result
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return <span>{viewModel.daysRemainingText}</span>;
});
```

### 规则：禁止使用 `fetch()` 方法

```jsx
// ❌ BAD - Component making HTTP requests
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`/api/tasks/${viewModel.id}`)
      .then(r => r.json())
      .then(setData);
  }, [viewModel.id]);

  return <div>{data?.title}</div>;
});

// ✅ GOOD - Parent uses .bind() to invoke ServerRequest
<TaskCard.bind({
  requestType: 'GetTaskRequest',
  params: { id: taskId }
}) />
```

### 规则：错误视图模型仅用于展示数据

```jsx
// ❌ BAD - Generic error handling
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  if (viewModel.error) {
    return <div>Error: {viewModel.error.message}</div>;
  }
  return <div>{viewModel.title}</div>;
});

// ✅ GOOD - Specific error ViewModels
const TaskCard = FOSMVVM.viewModelComponent(({ viewModel }) => {
  if (viewModel.errorType === 'NotFoundError') {
    return (
      <div className="not-found">
        <h3>{viewModel.errorTitle}</h3>
        <p>{viewModel.errorMessage}</p>
        <p>{viewModel.suggestedAction}</p>
      </div>
    );
  }

  if (viewModel.errorType === 'ValidationError') {
    return (
      <div className="validation-error">
        <h3>{viewModel.errorTitle}</h3>
        <ul>
          {viewModel.validationErrors.map(err => (
            <li key={err.field}>{err.message}</li>
          ))}
        </ul>
      </div>
    );
  }

  return <div>{viewModel.title}</div>;
});
```

### 规则：使用导航意图进行导航

```jsx
// ❌ BAD - Hardcoded URLs
const TaskRow = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return (
    <div>
      <a href={`/tasks/${viewModel.id}`}>{viewModel.title}</a>
    </div>
  );
});

// ✅ GOOD - Navigation intents
// FOSMVVM utilities loaded via <script> tag, available on global namespace

const TaskRow = FOSMVVM.viewModelComponent(({ viewModel }) => {
  return (
    <div>
      <FOSMVVM.Link to={{ intent: 'viewTask', id: viewModel.id }}>
        {viewModel.title}
      </FOSMVVM.Link>
    </div>
  );
});
```

---

## 文件组织结构

```
src/components/
├── {Feature}/
│   ├── {Feature}View.jsx             # Full page → {Feature}ViewModel
│   ├── {Feature}View.test.js         # Tests for {Feature}View
│   ├── {Entity}CardView.jsx          # Child component → {Entity}CardViewModel
│   ├── {Entity}CardView.test.js      # Tests for {Entity}CardView
│   └── {Entity}RowView.jsx           # Child component → {Entity}RowViewModel
├── Shared/
│   ├── HeaderView.jsx                # Shared components
│   └── FooterView.jsx
```

---

## 常见错误

- **在组件中计算数据**  
- **直接发起 HTTP 请求**  
- **硬编码文本**  
- **使用硬编码的 URL**  
- **未使用 `viewModelComponent()` 对组件进行包装**  
- **组件文件名不匹配**  

---

## 文件模板

完整的文件模板请参阅 [reference.md](reference.md)。

---

## 命名规范

| 名称类型 | 命名规则 | 示例 |
|---------|------------|---------|
| 组件文件 | `{Name}View.jsx` | `TaskListView.jsx`、`SignInView.jsx` |
| 测试文件 | `{Name}View.test.js` | `TaskListView.test.js` |
- 组件函数 | `{Name}View` | `TaskListView`、`SignInView` |
- 视图模型属性 | `viewModel` | 始终使用 `viewModel` 作为属性名 |

---

## 测试规范

- **测试：成功状态下的渲染**  
- **测试：错误状态下的渲染**  
- **测试：用户交互行为**  

---

## 使用方法

**使用步骤：**
1. 与用户讨论并明确视图模型和服务器请求的详细信息。
2. （可选）将规范文件的内容加载到系统中。
3. 明确组件的类型（仅用于显示数据、交互式组件、表单组件或列表组件）。

**生成结果：**
- 首先生成 `.test.js` 文件（测试用例）。
- 然后生成 `.jsx` 文件（实际组件代码）。

**工作流程：**  
通常在讨论完需求或阅读规范文件后使用该工具。该工具会自动根据上下文生成所需的文件，无需手动指定文件路径或进行问答。

---

## 参考资料

- [架构模式](../shared/architecture-patterns.md) - 相关的设计模式和架构参考。
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - FOSMVVM 的完整架构文档。
- [fosmvvm-swiftui-view-generator](../fosmvvm-swiftui-view-generator/SKILL.md) - 相对应的 SwiftUI 生成工具。
- [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) - 相对应的 Leaf 组件生成工具。
- [reference.md](reference.md) - 完整的文件模板集合。

---

## 版本历史

| 版本号 | 更新日期 | 主要变更内容 |
|---------|------|---------|
| 1.0 | 2026-01-23 | 基于 Kairos 的需求首次开发出用于生成 React 视图的工具。 |