# 网页构建技能

该技能使代理能够使用纯JavaScript、HTML和CSS来构建、测试和部署单页应用程序（SPAs）。它注重简洁性、可测试性和稳定性，而不依赖于复杂的构建工具或框架。

## 1. 开发流程：**“规范先行”的循环**

为确保质量和防止代码退化，请遵循以下严格的开发流程：

1. **规范定义**：在 `benchmarks/apps/<app-name>/spec.md` 中定义应用程序的需求，包括功能、用户界面状态和数据模型。
2. **测试**：使用 Node.js 的内置测试工具在 `apps/<app-name>/test.js` 中编写无头逻辑测试，并模拟浏览器 API（如 `localStorage`）。
3. **代码实现**：在 `apps/<app-name>/js/store.js` 中实现相应的逻辑，直到测试通过。
4. **用户界面开发**：在 `apps/<app-name>/index.html` 和 `apps/<app-name>/js/app.js` 中构建用户界面，并将其与已测试的存储模块（Store）连接起来。
5. **验证**：在浏览器中打开应用程序（或使用 `browser` 工具）来验证用户界面的正确性。

## 2. 架构：纯 MVC 模式

我们采用轻量级的“纯 MVC”架构：

### 存储模块（`store.js`）
- **功能**：管理数据状态和业务逻辑。
- **依赖关系**：完全不依赖于 DOM，使用 `localStorage` 进行数据持久化。
- **接口**：提供 `getItems()`、`addItem()`、`updateItem()` 等方法。
- **测试**：可以通过模拟 `localStorage` 在 Node.js 中进行测试。

### 路由器模块（`app.js`）
- **功能**：通过 URL 哈希值（例如 `#list`、`#detail:123`）处理导航。
- **工作原理**：监听 `hashchange` 事件并调用相应的渲染函数。

### 应用程序模块（`app.js`）
- **功能**：根据当前路由和存储模块的数据来渲染用户界面。
- **工作原理**：清空主容器（例如 `<div id="view">`），然后插入 HTML 内容。
- **交互性**：在渲染完成后为 DOM 元素绑定事件监听器。

## 3. 无头逻辑测试

由于存储模块不依赖于 DOM，我们可以使用 `node --test` 命令对其进行测试。

**测试示例（`test.js`）：**

```javascript
const test = require('node:test');
const assert = require('node:assert');
const Store = require('./js/store.js');

// Mock localStorage
class MockStorage {
    constructor() { this.store = {}; }
    getItem(key) { return this.store[key] || null; }
    setItem(key, value) { this.store[key] = value.toString(); }
    clear() { this.store = {}; }
}
global.localStorage = new MockStorage();

test('Store adds an item', (t) => {
    const store = new Store('test_key');
    store.addItem('New Item');
    assert.strictEqual(store.getItems().length, 1);
});
```

运行方式：`node apps/<app-name>/test.js`

## 4. 任务完成验证：`EVAL.md`

在将任务标记为完成之前，请在应用程序目录中创建或更新 `EVAL.md` 文件。该文件应包含用户界面的手动验证步骤列表，因为自动化测试仅覆盖逻辑部分。

**`EVAL.md` 示例：**
```markdown
# Evaluation Checklist

- [ ] App loads without console errors.
- [ ] Creating an item updates the list immediately.
- [ ] Refreshing the page persists the data.
- [ ] Clicking "Delete" removes the item.
```

## 5. 模板

使用 `skills/webpage_builder/templates/vanilla-app/` 目录中的模板来启动新项目。这些模板包含了存储模块、路由器和应用程序的基本目录结构和示例代码。