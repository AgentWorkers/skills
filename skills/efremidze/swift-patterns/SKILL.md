---
name: swift-patterns
description: 审查、重构或开发 SwiftUI 功能，确保具备正确的状态管理机制、现代的 API 使用方式、最佳的视图组合方式、合理的导航模式、性能优化措施以及符合测试最佳实践的设计。
---
# swift-patterns

本技能专注于使用正确的状态管理、现代的API、优化的视图组合以及性能导向的模式来审查、重构或开发SwiftUI功能。在开发过程中，应优先考虑使用原生的Apple API、遵循Apple的设计指南，并确保代码结构易于测试。本技能强调基于事实的最佳实践，而不强制使用特定的架构模式。

## 工作流程决策树

### 1) 审查现有的SwiftUI代码
→ 请参阅`references/workflows-review.md`以了解审查方法：
- 检查状态管理是否符合属性包装器的使用规则（参见`references/state.md`）
- 验证视图组合和提取模式（参见`references/view-composition.md`）
- 审计列表的性能和数据一致性（参见`references/lists-collections.md`）
- 确认是否正确使用了现代API（参见`references/modern-swiftui-apis.md`）
- 检查使用`.task`实现的异步操作（参见`references/concurrency.md`）
- 验证导航功能的实现（参见`references/navigation.md`）
- 使用以下审查回复模板

### 2) 重构现有的SwiftUI代码
→ 请参阅`references/workflows-refactor.md`以了解重构方法：
- 使用重构脚本（playbooks）来提取复杂的视图结构（参见`references/refactor-playbooks.md`）
- 将过时的API迁移到现代的替代方案（参见`references/modern-swiftui-apis.md`）
- 优化性能瓶颈（参见`references/performance.md`）
- 重新组织状态的所有权结构（参见`references/state.md`）
- 应用常见的设计模式（参见`references/patterns.md`）
- 使用以下重构回复模板

### 3) 实现新的SwiftUI功能
- 首先设计数据流：明确状态是内部拥有的还是外部注入的（参见`references/state.md`）
- 优化视图结构以实现最佳组合（参见`references/view-composition.md`）
- 仅使用现代API（参见`references/modern-swiftui-apis.md`）
- 使用`.task`修饰符处理异步操作（参见`references/concurrency.md`）
- 早期应用性能优化策略（参见`references/performance.md`）
- 实现导航逻辑（参见`references/navigation.md`）

### 4) 回答关于最佳实践的问题
- 根据问题内容加载相关的参考文件（参见下面的参考文件）
- 通过示例提供直接指导

**如果意图不明确，请询问：**“您只是希望了解问题所在（审查），还是希望我修改代码（重构）？”

## 回复模板

**审查回复：**
1. **审查范围** - 审查的内容
2. **问题发现** - 按严重程度分类，并附上可操作的改进建议
3. **证据** - 文件路径或代码位置
4. **风险与权衡** - 可能出现的问题或需要注意的事项
5. **下一步行动** - 需要首先修复或验证的内容

**重构回复：**
1. **目的与范围** - 说明修改的内容及其原因
2. **修改内容** - 以列表形式列出修改的文件路径
3. **保持原有行为** - 哪些部分应保持不变
4. **下一步行动** - 需要进行的测试或验证工作

## 快速参考：属性包装器的选择

| 包装器 | 使用场景 | 所有权 |
|---------|----------|-----------|
| `@State` | 用于表示内部视图状态（值类型或`@Observable`类） | 视图拥有该状态 |
| `@Binding` | 子视图需要修改父视图的状态 | 父视图拥有该状态 |
| `@Bindable` | 需要绑定的外部`@Observable`对象 | 外部注入 |
| `let` | 从父视图读取只读值 | 外部注入 |
| `var` + `.onChange()` | 需要响应式更新的只读值 | 外部注入 |

**关键规则：**
- 始终将`@State`标记为`private`（明确所有权）
- 不要将`@State`用于传递的值（仅接受初始值）
- `@State`应与`@Observable`类一起使用（而非`@StateObject`）

详细指导和权衡信息请参阅`references/state.md`。

## 快速参考：现代API的替代方案

| 过时API | 现代替代API | 备注 |
|------------|-------------------|-------|
| `foregroundColor()` | `foregroundStyle()` | 支持动态类型 |
| `cornerRadius()` | `.clipShape(.rect(cornerRadius:))` | 更灵活 |
| `NavigationView` | `NavigationStack` | 类型安全的导航方式 |
| `tabItem()` | `Tab` API | iOS 18及以上版本支持 |
| `onTapGesture()` | `Button` | 除非需要定位或计数功能 |
| `onChange(of:) { value in }` | `onChange(of:) { old, new in }` 或 `onChange(of:) { }` | 可接受两个或零个参数 |
| `UIScreen.main.bounds` | `GeometryReader` 或布局相关API | 避免使用硬编码的尺寸 |

完整的迁移指南请参阅`references/modern-swiftui-apis.md`。

## 审查检查清单

在审查SwiftUI代码时，请注意以下要点：

### 状态管理
- [ ] `@State`属性是否被标记为`private`
- [ ] 传递的值是否未声明为`@State`或`@StateObject`
- [ ] `@Binding`是否仅在子视图需要修改父视图状态时使用
- [ ] 属性包装器的选择是否符合所有权规则
- [ ] 状态的所有权是否清晰明确

### 现代API
- [ ] 是否使用了过时的修饰符（如`foregroundColor`, `cornerRadius`等）
- [ ] 是否使用`NavigationStack`代替`NavigationView`
- [ ] 在适当的情况下是否使用`Button`代替`onTapGesture`
- [ ] 是否使用了带参数或无参数的`onChange()`

### 视图组合
- [ ] 是否使用修饰符而不是条件语句来处理状态变化（以保持数据一致性）
- [ ] 是否将复杂的视图拆分为独立的子视图
- [ ] 视图是否保持简洁且专注
- [ ] 视图的`body`部分是否简单且无副作用

### 导航与表格
- [ ] 是否使用`navigationDestination(for:)`进行类型安全的导航
- [ ] 是否使用`.sheet(item:)`来创建基于模型的表格
- [ ] 表格是否拥有自己的关闭操作

### 列表与集合
- [ ] `ForEach`是否使用了稳定的数据标识（对于动态数据，不要使用`.indices`）
- [ ] 每个`ForEach`元素是否显示固定数量的视图
- [ ] `ForEach`中是否没有内联过滤（使用预过滤和缓存）
- [ ] 列表行中是否没有使用`AnyView`

### 性能
- [ ] 是否仅向视图传递必要的数据（避免传递大型配置对象）
- [ ] 是否消除了不必要的依赖关系
- [ ] 在状态赋值之前是否检查了值的变化
- [ ] 对于大型列表，是否使用了`LazyVStack`/`LazyHStack`
- [ ] 视图的`body`部分是否避免了对象创建

### 异步操作
- [ ] 是否使用`.task`来实现自动取消
- [ ] 是否使用`.task(id:)`来处理依赖于值的任务
- [ ] 是否避免了在`onAppear`回调中混合异步操作

有关每个检查点的详细说明，请参阅相应的参考文件。

## 限制条件

- **仅关注Swift/SwiftUI** - 除非需要桥接，否则不涉及服务器端的Swift或UIKit
- **不使用Swift并发模式** - 使用`.task`来处理SwiftUI的异步操作
- **不强制使用特定的架构模式** - 不要求必须使用MVVM/MVC/VIPER等架构
- **不涉及格式化或代码检查规则** - 重点关注代码的正确性和设计模式
- **不提供特定工具的指导** - 不包括Xcode、Instruments或IDE的使用说明
- **允许引用以下文档：`developer.apple.com/documentation/swiftui/`, `developer.apple.com/documentation/swift/`

所有工作流程都必须遵循这些限制条件。

## 设计理念

本技能遵循Apple文档中的**最佳实践**：
- 优先使用现代API而非过时的API
- 明确的状态所有权模式
- 优化视图组合以提高性能
- 代码结构应易于测试
- 不强制使用特定的架构模式（如MVVM/MVC/VIPER）
- 遵循Apple的人机界面指南

## 参考文件

所有参考文件位于`references/`目录下：
- `workflows-review.md` - 审查方法和问题发现分类
- `workflows-refactor.md` - 重构方法和不变量
- `refactor-playbooks.md` - 逐步重构指南
- `state.md` - 属性包装器和所有权模式
- `navigation.md` - 导航实现模式
- `view-composition.md` - 视图结构和提取方法
- `lists-collections.md` - 数据一致性和`ForEach`模式
- `scrolling.md` - 滚动处理和分页
- `concurrency.md` - 使用`.task`处理异步操作
- `performance.md` - 性能优化策略
- `testing-di.md` - 测试和依赖注入
- `patterns.md` - 常见的SwiftUI设计模式
- `modern-swiftui-apis.md` - 过时API的迁移指南
- `code-review-refactoring.md` - 代码质量检查