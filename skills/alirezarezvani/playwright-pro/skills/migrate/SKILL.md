---
name: migrate
description: 从 Cypress 或 Selenium 迁移到 Playwright。当用户提到 “cypress”、“selenium”、“migrate tests”、“convert tests”、“switch to playwright”、“move from cypress” 或 “replace selenium” 时，请使用此指南。
  Migrate from Cypress or Selenium to Playwright. Use when user mentions
  "cypress", "selenium", "migrate tests", "convert tests", "switch to
  playwright", "move from cypress", or "replace selenium".
---
# 迁移到 Playwright

这是一个将 Cypress 或 Selenium 自动迁移到 Playwright 的过程，支持逐个文件的转换。

## 输入参数

`$ARGUMENTS` 可以是：
- `"from cypress"` — 迁移 Cypress 测试套件
- `"from selenium"` — 迁移 Selenium/WebDriver 测试
- 文件路径：转换特定的测试文件
- 空值：自动检测源框架

## 步骤

### 1. 检测源框架

使用 `Explore` 子代理进行扫描：
- 如果存在 `cypress/` 目录或 `cypress.config.ts` 文件，则为 Cypress 框架；
- 如果 `package.json` 中有 `selenium` 或 `webdriver` 依赖项，则为 Selenium 框架；
- 如果存在导入 `selenium` 的 `.py` 测试文件，则为 Selenium（Python）框架。

### 2. 评估迁移范围

统计文件数量并进行分类：

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
| 中等数量（11-30个） | 每组5个文件进行批量转换 | 使用子代理 |
| 大量（31个以上） | 使用 `/batch` 命令进行并行转换 |

### 3. （如果尚未安装）设置 Playwright

如果尚未安装 Playwright，请先运行 `/pw:init` 命令进行配置。

### 4. 转换文件

对于每个文件，应用相应的转换规则：

#### 从 Cypress 迁移到 Playwright

请参考 `cypress-mapping.md` 文件以获取完整的转换规则。

**Cypress 的自定义命令** → 在 Playwright 中使用相应的固定装置（fixtures）或辅助函数
**Cypress 的插件** → 在 Playwright 中配置相应的设置或使用固定装置
**`before`/`beforeEach` 代码块** → 在 Playwright 中使用 `test.beforeAll()` 或 `test.beforeEach()`

#### 从 Selenium 迁移到 Playwright

请参考 `selenium-mapping.md` 文件以获取完整的转换规则。

**注意：** 由于 Selenium 和 Playwright 在某些功能上的差异，部分代码可能需要手动调整。

### 5. 升级选择器

在转换过程中，将原有的选择器升级为 Playwright 推荐的用法：
- `#id` → 使用 `getByTestId()` 或 `getByRole()`
- `.class` → 使用 `getByRole()` 或 `getByText()`
- `[dataTestId]` → 使用 `getByTestId()`
- XPath 选择器 → 使用基于角色的选择器

### 6. 转换自定义命令/工具函数

- Cypress 的自定义命令 → 通过 `test.extend()` 方法在 Playwright 中实现相应的功能
- Selenium 的页面对象 → 在 Playwright 中使用对应的页面对象（保持结构，但更新 API）
- 共用的辅助函数 → 将它们转换为 TypeScript 编写的实用函数

### 7. 验证每个转换后的文件

在转换每个文件后，检查是否存在编译或运行时错误。

### 8. 清理

所有文件转换完成后：
- 从 `package.json` 中删除与 Cypress/Selenium 相关的依赖项
- 删除旧的配置文件（如 `cypress.config.ts` 等）
- 更新持续集成（CI）工作流程以使用 Playwright
- 更新项目中的 `README.md` 文件，说明新的测试命令

在删除任何文件之前，请先征得用户同意。

## 输出结果

- 转换总结：已转换的文件数量、迁移的测试数量
- 需要手动处理的无法自动转换的测试
- 更新后的持续集成配置
- 测试运行结果的对比结果（转换前后）