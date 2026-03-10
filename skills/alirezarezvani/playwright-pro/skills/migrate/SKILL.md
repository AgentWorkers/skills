---
name: "migrate"
description: 从 Cypress 或 Selenium 迁移到 Playwright。当用户提到 “cypress”、“selenium”、“migrate tests”（迁移测试）、“convert tests”（转换测试）、“switch to playwright”（切换到 Playwright）、“move from cypress”（从 Cypress 迁移）或 “replace selenium”（替换 Selenium）时，请使用此指南。
  Migrate from Cypress or Selenium to Playwright. Use when user mentions
  "cypress", "selenium", "migrate tests", "convert tests", "switch to
  playwright", "move from cypress", or "replace selenium".
---
# 迁移到 Playwright

这是一个将测试框架从 Cypress 或 Selenium 自动迁移到 Playwright 的过程，支持逐个文件的转换。

## 输入参数

`$ARGUMENTS` 可以是：
- `"from cypress"` — 迁移 Cypress 测试套件
- `"from selenium"` — 迁移 Selenium/WebDriver 测试
- 一个文件路径：转换特定的测试文件
- 空值：自动检测源测试框架

## 步骤

### 1. 检测源测试框架

使用 `Explore` 子代理来扫描：
- `cypress/` 目录或 `cypress.config.ts` 文件 → Cypress
- `package.json` 中的 `dependencies` 中包含 `selenium` 或 `webdriver` → Selenium
- 包含 `selenium` 导入的 `.py` 测试文件 → Selenium（Python）

### 2. 评估迁移范围

统计文件数量并分类：

```
Migration Assessment:
- Total test files: X
- Cypress custom commands: Y
- Cypress fixtures: Z
- Estimated effort: [small|medium|large]
```

| 文件数量 | 文件类型 | 迁移方式 |
|---|---|---|
| 少量（1-10个） | 依次转换 | 直接转换 |
| 中等数量（11-30个） | 每组5个文件批量转换 | 使用子代理 |
| 大量（31个以上） | 使用 `/batch` 命令进行并行转换 |

### 3. 如果尚未配置 Playwright，请进行设置

如果 Playwright 未配置，请先运行 `/pw:init` 命令进行初始化。

### 4. 转换文件

对于每个文件，应用相应的转换规则：

#### 从 Cypress 迁移到 Playwright

请参考 `cypress-mapping.md` 文件以获取完整的转换规则。

**Cypress 的自定义命令** → Playwright 的测试 fixture 或辅助函数
**Cypress 的插件** → Playwright 的配置文件或测试 fixture
**`before`/`beforeEach` ** → Playwright 的 `test.beforeAll()` 或 `test.beforeEach()`

#### 从 Selenium 迁移到 Playwright

请参考 `selenium-mapping.md` 文件以获取完整的转换规则。

**Cypress 的自定义命令** → Playwright 的测试 fixture 或辅助函数
**Selenium 的页面对象** → Playwright 的页面对象（保持结构，更新 API）

### 5. 升级选择器

在转换过程中，将选择器升级为 Playwright 的最佳实践：
- `#id` → `getByTestId()` 或 `getByRole()`
- `.class` → `getByRole()` 或 `getByText()`
- `[dataTestId]` → `getByTestId()`
- XPath → 基于角色的选择器

### 6. 转换自定义命令/工具函数

- Cypress 的自定义命令 → 通过 `test.extend()` 将其转换为 Playwright 的自定义 fixture
- Selenium 的页面对象 → Playwright 的页面对象（保持结构，更新 API）
- 公用的辅助函数 → 转换为 TypeScript 编写的辅助函数

### 7. 验证每个转换后的文件

转换每个文件后，请检查是否存在编译或运行时错误。

### 8. 清理

所有文件转换完成后：
- 从 `package.json` 中删除 Cypress/Selenium 的依赖项
- 删除旧的配置文件（如 `cypress.config.ts` 等）
- 更新持续集成（CI）工作流程以使用 Playwright
- 更新 README 文件中的测试命令说明

在删除任何文件之前，请先征得用户同意。

## 输出结果

- 转换总结：已转换的文件数量、迁移的总测试数量
- 无法自动转换的测试（需要手动处理）
- 更新后的持续集成配置
- 测试运行结果的对比（转换前后）