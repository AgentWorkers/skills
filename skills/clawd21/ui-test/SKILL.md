---
name: ui-test
description: **简单的英语端到端（E2E）UI测试**：  
这种测试方法使用自然语言来描述测试流程，测试人员通过浏览器工具执行测试操作，随后将生成的Playwright测试脚本导出，以便用于持续集成（CI/CD）流程。当需要创建UI测试、测试网站或生成Playwright脚本时，可以采用这种方法。
metadata: {"clawdbot":{"emoji":"🧪"}}
---

# UI测试 — 使用自然语言进行端到端测试（🧪）

请用自然语言描述您的UI测试流程。测试代理会自动识别按钮、导航应用程序的各个步骤，并执行相应的操作，无需使用任何选择器或代码。它会为每个关键步骤生成截图，将这些截图拼接成演示视频，并通过私信向您发送测试结果（包含通过/失败的状态）。

*开发地点：🤠 德克萨斯州 ❤️ [PlebLab](https://pleblab.dev)*

![UI测试 — 请描述您的测试需求，我会为您执行测试。](https://files.catbox.moe/3yezuk.png)

## 工作流程

1. **创建测试**：用户为测试命名，并用自然语言描述测试步骤。
2. **运行测试**：测试代理会打开clawd浏览器，执行每个步骤，并为每个操作生成截图。
3. **导出测试脚本**：代理会根据已执行的步骤生成Playwright测试脚本（`.spec.ts`文件）。
4. **持续集成/持续部署（CI/CD）**：用户将生成的脚本添加到测试套件中，然后使用`npx playwright test`命令运行测试。

## 测试代理的执行流程

在运行测试时，代理会执行以下操作：

1. 加载测试定义：`node scripts/ui-test.js get "<name>"`
2. 启动clawd浏览器：`browser action=start profile=clawd`
3. 导航到测试指定的URL。
4. 对于每个测试步骤：
   a. 解析用户的指令（如点击、输入文本、验证等）。
   b. 使用`browser action=snapshot`来捕获当前页面的截图。
   c. 根据用户的指令执行相应的操作（如点击、输入等）。
   d. 在每个步骤完成后生成截图。
   e. 记录所使用的选择器以及操作是否成功。
5. 保存测试结果：`node scripts/ui-test.js save-run "<name>" passed=true/false`

在将测试结果导出为Playwright脚本时，代理会执行以下操作：

1. 加载测试定义和最近一次成功的测试结果。
2. 将每个测试步骤映射到相应的Playwright API调用。
3. 生成包含正确导入语句、测试结构和断言的`.spec.ts`文件。
4. 将生成的脚本保存到用户的项目中或指定的输出路径。

## 步骤解析指南

测试代理应按照以下规则解析用户的自然语言指令：

| 用户指令 | 浏览器操作 | Playwright等效操作 |
|-----------|---------------|----------------------|
| “点击‘登录’按钮” | `act: click ref="Sign In button"` | `page.getByRole('button', {name: 'Sign In'}).click()` |
| “在‘电子邮件’字段中输入‘hello@test.com’” | `act: type ref="email" text="hello@test.com"` | `page.getByLabel('Email').fill('hello@test.com')` |
| “验证仪表板是否显示‘欢迎’” | `snapshot` + `check text` | `expect(page.getByText('Welcome')).toBeVisible()` |
| “等待页面加载完成” | `act: wait` | `page.waitForLoadState('networkidle')` |
| “点击汉堡菜单” | `act: click` (找到菜单图标) | `page.getByRole('button', {name: 'menu'}).click()` |
| “向下滚动页面” | `act: evaluate fn="window.scrollBy(0,500)"` | `page.evaluate(() => window.scrollBy(0, 500))` |
| “勾选‘记住我’复选框” | `act: click ref="Remember Me"` | `page.getByLabel('Remember Me').check()` |
| “从货币下拉菜单中选择‘USD’” | `act: select values=["USD"]` | `page.getByLabel('Currency').selectOption('USD')` |
| “生成截图” | `browser action=screenshot` | `page.screenshot({path: 'step-N.png'})` |
| “验证URL是否包含‘/dashboard’” | `check current URL` | `expect(page).toHaveURL(/dashboard/)` |

## 命令说明

测试脚本可通过以下命令进行管理：

| 命令 | 功能 |
|---------|-------------|
| `create <name> [url]` | 创建新的测试 |
| `add-step <name> <step>` | 添加一个新的测试步骤 |
| `set-steps <name> <json>` | 替换所有测试步骤 |
| `set-url <name> <url>` | 设置测试的URL |
| `get <name>` | 查看测试定义 |
| `list` | 列出所有测试 |
| `remove <name>` | 删除指定的测试 |
| `save-run <name> ...` | 保存测试执行结果 |
| `runs [name]` | 查看测试运行历史 |
| `export <name> [outfile]` | 将测试脚本导出为Playwright格式 |

## 导出格式

生成的Playwright脚本包含以下内容：

- 正确的TypeScript导入语句。
- 包含测试名称的`test.describe`块。
- 包含初始页面导航操作的`test.beforeEach`块。
- 每个测试步骤都包含原始指令和注释。
- 包含用户指定的断言语句（如`verify`、`check`、`should`、`expect`）。
- 在测试失败时，会生成相应的截图。

## 截图与视频

在测试执行过程中，代理会执行以下操作：

- **每个步骤执行前**：生成截图并保存为`step-NN-before.jpg`。
- **每个步骤执行后**：生成截图并保存为`step-NN-after.jpg`。
- **测试失败时**：生成截图并保存为`step-NN-FAIL.jpg`。

截图文件保存路径：`~/.ui-tests/runs/<slug>-<timestamp>/`

测试完成后，代理会生成一个演示视频，并将其发送到指定的聊天频道。

## 数据存储位置

- 测试定义文件：`~/.ui-tests/<slug>.json`
- 测试运行记录：`~/.ui-tests/runs/<slug>-<timestamp>/run.json`
- 截图文件：`~/.ui-tests/runs/<slug>-<timestamp>/step-*.jpg`
- 视频文件：`~/.ui-tests/runs/<slug>-<timestamp>/walkthrough.mp4`
- 导出的测试脚本：保存在用户指定的路径或`./tests/<slug>.spec.ts`文件中。