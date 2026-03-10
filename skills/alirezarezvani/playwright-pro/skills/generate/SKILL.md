---
name: "generate"
description: 生成 Playwright 测试用例。当用户输入“编写测试”、“生成测试”、“为……添加测试”、“测试这个组件”、“端到端测试”、“为……创建测试”、“测试这个页面”或“测试这个功能”时，请使用此命令。
  Generate Playwright tests. Use when user says "write tests", "generate tests",
  "add tests for", "test this component", "e2e test", "create test for",
  "test this page", or "test this feature".
---
# 生成 Playwright 测试用例

根据用户故事、URL、组件名称或功能描述，生成可用于生产环境的 Playwright 测试用例。

## 输入

`$ARGUMENTS` 包含了需要测试的内容。示例：
- `"用户可以使用电子邮件和密码登录"`
- `"结账流程"`
- `"src/components/UserProfile.tsx"`
- `"带有筛选功能的搜索页面"`

## 步骤

### 1. 理解测试目标

解析 `$ARGUMENTS` 以确定以下内容：
- **用户故事**：提取需要验证的行为
- **组件路径**：阅读组件的源代码
- **页面/URL**：确定页面的路由及其元素
- **功能名称**：将其映射到相应的应用程序模块

### 2. 探索代码库

使用 `Explore` 子代理来收集相关信息：
- 阅读 `playwright.config.ts` 文件中的 `testDir`、`baseURL` 和 `projects` 设置
- 检查 `testDir` 中现有的测试用例、测试 fixture 和编写规范
- 如果提供了组件路径，阅读该组件的源代码以了解其属性、状态和交互逻辑
- 检查 `pages/` 目录中是否存在相关的页面对象
- 检查 `fixtures/` 目录中是否存在现有的测试 fixture
- 检查认证设置（如 `auth.setup.ts` 或 `storageState` 配置）

### 3. 选择模板

查看插件中的 `templates/` 目录，选择合适的模板：
| 测试内容 | 模板路径 |
|---|---|
| 登录/认证流程 | `templates/auth/login.md` |
| 创建/读取/更新（CRUD）操作 | `templates/crud/` |
| 结账/支付 | `templates/checkout/` |
| 搜索/筛选界面 | `templates/search/` |
- 表单提交 | `templates/forms/` |
- 仪表板/数据 | `templates/dashboard/` |
- 新员工入职流程 | `templates/onboarding/` |
- API 端点 | `templates/api/` |
- 可访问性 | `templates/accessibility/` |

根据具体需求调整模板，将 `{{placeholders}}` 替换为实际的元素选择器、URL 和数据。

### 4. 生成测试用例

遵循以下规则：

**结构：**
```typescript
import { test, expect } from '@playwright/test';
// Import custom fixtures if the project uses them

test.describe('Feature Name', () => {
  // Group related behaviors

  test('should <expected behavior>', async ({ page }) => {
    // Arrange: navigate, set up state
    // Act: perform user action
    // Assert: verify outcome
  });
});
```

**元素定位优先级**（优先使用以下方法之一）：
1. `getByRole()` — 用于定位按钮、链接、标题和表单元素
2. `getByLabel()` — 用于定位带有标签的表单字段
3. `getByText()` — 用于定位非交互式的文本内容
4. `getByPlaceholder()` — 用于定位带有占位符的输入框
5. `getByTestId()` — 在其他方法无法定位元素时使用

**断言** — 始终优先使用基于 Web 的断言方法：
```typescript
// GOOD — auto-retries
await expect(page.getByRole('heading')).toBeVisible();
await expect(page.getByRole('alert')).toHaveText('Success');

// BAD — no retry
const text = await page.textContent('.msg');
expect(text).toBe('Success');
```

**禁止使用的方法：**
- `page.waitForTimeout()`
- `page.$(selector)` 或 `page.$$(selector)`
- 除非绝对必要，否则避免使用纯 CSS 选择器
- 对于可以通过元素定位器完成的操作，不要使用 `page.evaluate()`

**必须包含的内容：**
- 描述性强的测试名称，以说明测试的目的
- 正常流程测试以及边缘情况测试
- 每个 Playwright 调用都应使用 `await` 来确保异步操作完成
- 使用相对于 `baseURL` 的导航方式（例如 `page.goto('/')`，而不是 `page.goto('http://...')`

### 5. 遵循项目规范

- 如果项目使用 TypeScript，则生成 `.spec.ts` 文件
- 如果项目使用 JavaScript，则生成 `.spec.js` 文件，并使用 `require()` 进行模块导入
- 如果项目中存在页面对象，则使用这些对象代替硬编码的元素定位器
- 如果项目中存在自定义的测试 fixture，请导入并使用它们
- 如果项目中有一个测试数据目录，请在該目录中创建相应的测试数据文件

### 6. 生成辅助文件（如有需要）

- **页面对象**：如果一个测试用例涉及页面上的 5 个或更多不同的元素定位器，请创建一个对应的页面对象
- **测试 fixture**：如果测试需要共享的设置（如认证信息、数据等），请创建或扩展相应的测试 fixture
- **测试数据**：如果测试需要使用结构化数据，请在 `test-data/` 目录中创建 JSON 文件

### 7. 验证测试用例

运行生成的测试用例：
```bash
npx playwright test <generated-file> --reporter=list
```

如果测试失败：
1. 查看错误信息
2. 修复测试代码（而不是应用程序代码）
3. 重新运行测试
4. 如果问题出在应用程序本身，请将问题报告给相关人员

## 输出结果

- 生成的测试用例文件及其路径
- 所生成的辅助文件（页面对象、测试 fixture、测试数据）
- 测试运行结果
- 测试覆盖范围说明：哪些功能已经被测试到