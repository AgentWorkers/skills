---
name: Playwright (Automation + MCP + Scraper)
slug: playwright
version: 1.0.3
homepage: https://clawic.com/skills/playwright
description: "通过 Playwright MCP 实现浏览器自动化。可以执行以下操作：导航网站、点击页面元素、填写表单、截图、提取数据以及调试真实的浏览器工作流程。适用场景包括：  
1. 当您需要使用真实的浏览器（而非静态数据获取方式）时；  
2. 当任务涉及 Playwright MCP、浏览器工具、Playwright 测试脚本或由 JavaScript 渲染的页面时；  
3. 当用户希望将浏览器的导航操作、表单填写、截图功能、PDF 生成、文件下载等功能转化为可靠的结果时。"
changelog: Clarified the MCP-first browser automation flow and improved quick-start guidance for forms, screenshots, and extraction.
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":["node","npx"]},"os":["linux","darwin","win32"],"install":[{"id":"npm-playwright","kind":"npm","package":"playwright","bins":["playwright"],"label":"Install Playwright"},{"id":"npm-playwright-mcp","kind":"npm","package":"@playwright/mcp","bins":["playwright-mcp"],"label":"Install Playwright MCP (optional)"}]}}
---
## 适用场景

此技能适用于以下实际浏览器操作场景：JS渲染的页面、多步骤表单处理、截图或PDF生成、用户界面（UI）调试、Playwright测试编写、通过MCP（Media Control Protocol）实现浏览器控制，以及从渲染后的页面中提取结构化数据。

当静态数据获取无法满足需求时，或者任务依赖于浏览器事件、可见的DOM状态、认证信息、文件上传/下载，或者需要用户交互式的页面渲染时，建议使用此技能。

如果用户主要希望代理执行简单的浏览器操作（如导航、点击、填写表单、截图、下载数据或提取信息），则MCP是一个理想的选择。

对于脚本和测试，建议直接使用Playwright；而当浏览器工具已经集成到自动化流程中，或者用户明确要求使用MCP，或者使用浏览器操作比编写新的自动化代码更高效时，也可以选择MCP。

此技能主要适用于由仓库管理的浏览器相关任务，包括测试、调试、问题重现、截图生成以及需要确定性自动化处理的场景。从渲染后的页面中提取数据属于次要用途。

## 架构说明

此技能仅提供指令性指导，不会默认创建本地内存文件、设置文件夹或持久化用户会话信息。

仅加载完成任务所需的最小参考文件。除非仓库已对认证状态进行了标准化处理，或者用户明确要求重用浏览器会话，否则认证状态将保持临时状态。

## 快速入门

### 使用MCP的浏览器操作路径
```bash
npx @playwright/mcp --headless
```

当代理已经具备浏览器工具，或者用户希望进行浏览器自动化操作而无需编写新的Playwright代码时，可以使用此路径。

### 常见的MCP操作

Playwright提供的常见MCP操作包括：
- `browser_navigate`：打开页面
- `browser_click` 和 `browser_press`：进行交互
- `browser_type` 和 `browser_select_option`：操作表单
- `browser_snapshot` 和 `browser_evaluate`：用于查看和提取数据
- `browser_choose_file`：执行文件上传操作
- 通过当前浏览器的工作流程生成截图、PDF文件或进行其他操作

### 常见的浏览器操作结果

| 操作目标 | 对应的MCP操作 |
|------|--------------------------|
| 打开并查看网站 | navigate, wait, inspect, screenshot |
| 完成表单填写 | navigate, click, fill, select, submit |
| 捕获操作证据 | screenshot, PDF, download, trace |
| 提取结构化页面数据 | navigate, wait for rendered state, extract |
| 重现UI错误 | headed run, trace, console or network inspection |

### 现有的测试套件
```bash
npx playwright test
npx playwright test --headed
npx playwright test --trace on
```

### 常用的选择器与操作流程
```bash
npx playwright codegen https://example.com
```

### 直接使用Playwright API的路径
```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  await page.screenshot({ path: 'page.png', fullPage: true });
  await browser.close();
})();
```

## 快速参考

| 相关内容 | 对应文件 |
|------|------|
| 选择器策略与框架处理 | `selectors.md` |
| 错误分析、日志记录与调试方法 | `debugging.md` |
| 测试架构、模拟对象、认证机制与断言方法 | `testing.md` |
| 持续集成（CI）配置、重试机制与故障处理 | `ci-cd.md` |
| 从渲染页面中提取数据、分页处理及流量控制 | `scraping.md` |

## 方法选择指南

| 情况 | 最佳方案 | 原因 |
|----------|-----------|-----|
| 需要处理的只是静态HTML或简单的HTTP响应 | 先尝试更简单的获取方式 | 更快速、成本更低、更稳定 |
| 需要可靠的元素选择器或操作流程 | 使用`codegen`或探索性测试 | 比从源代码或过时的DOM中猜测选择器更快 |
| 需要处理本地应用、测试环境或仓库管理的E2E测试 | 使用`@playwright/test` | 更适合重复性测试和断言 |
| 一次性浏览器自动化操作（如截图、下载数据或提取数据） | 直接使用Playwright API | 更简单、直观，便于代码调试 |
| 代理/浏览器工具的工作流程已经依赖于`browser_*`系列函数，或者用户不希望编写代码 | 使用Playwright MCP | 实现导航-点击-填写-截图的自动化流程最快捷 |
| 遇到CI失败、系统不稳定或环境变化 | 先参考`debugging.md`和`ci-cd.md` | 在这种情况下，日志和故障记录更为重要 |

## 核心规则

### 1. 测试用户可见的行为及真实的浏览器交互逻辑
- 不要将Playwright用于那些可以通过单元测试或API测试更高效处理的细节性实现。
- 当成功依赖于渲染后的UI界面、可操作性、认证流程、文件上传/下载、导航逻辑或仅依赖浏览器本身的行为时，才使用Playwright。

### 2. 先确保测试独立运行
- 保持测试和脚本的独立性，以避免重试、并行执行或重新运行时继承隐藏的状态。
- 在从头开始设计并行测试方案之前，先扩展仓库现有的Playwright框架、配置和测试用例。
- 除非测试框架明确支持，否则不要在并行测试之间共享可变账户信息、浏览器状态或服务器端数据。

### 3. 先进行探索性操作
- 在锁定元素选择器或进行断言之前，先打开页面、等待并查看渲染后的状态。
- 使用`codegen`、headed模式或日志记录来获取稳定的元素定位方式，而不是从源代码或过时的DOM中猜测。
- 对于易出错的测试或仅用于CI环境的测试，先捕获日志记录，再修改选择器或等待条件。

### 4. 优先使用可靠的元素定位方式及基于Web的断言方法
- 在使用CSS或XPath之前，优先考虑使用角色（role）、标签（label）、文本（text）、替代文本（alt text）、标题（title）或测试ID（test ID）等元素属性。
- 使用Playwright的断言功能来验证用户可见的结果，而不仅仅是检查点击或填写操作是否执行。
- 如果元素定位存在歧义，需明确区分其位置；除非实际测试需求确实需要使用`first()`、`last()`或`nth()`等函数，否则不要忽略定位的准确性。

### 5. 等待元素可操作的状态或应用程序的实际状态，而非随意设置等待时间
- 在使用强制等待（如`sleep()`）或执行其他强制操作之前，先让Playwright的断言机制完成必要的检查。
- 优先使用`expect()`函数、基于URL的等待条件、响应状态检查，以及明确的应用程序就绪信号，而不是依赖模糊的等待时间设置。

### 6. 控制那些无法直接控制的部分
- 当目标是验证应用程序本身时，需要对第三方服务、不可靠的API、分析工具或跨源依赖进行模拟或隔离处理。
- 对于从渲染页面中提取数据的需求，优先使用官方文档提供的API或简单的HTTP请求方式，而不是直接启动完整的浏览器。
- 除非用户明确要求验证特定的第三方组件或集成，否则不要让这些组件成为测试失败的原因。

### 7. 明确处理认证状态、生产环境访问权限及数据持久化
- 默认情况下，不要持久化用户的浏览器会话状态。
- 仅在仓库已对会话状态进行标准化处理，或者用户明确要求重用会话时，才允许持久化会话状态。
- 对于涉及高风险的场景（如金融、医疗等），建议使用测试环境或本地环境，并在继续操作前获取用户的明确确认。

## Playwright使用中的常见陷阱

- 从源代码中猜测元素选择器，或使用`first()`、`last()`、`nth()`等函数来处理定位歧义问题 → 自动化操作可能一次成功，但后续会出现问题。
- 在仓库已有配置、测试用例、认证设置或使用习惯的情况下，重新设计Playwright的架构 → 新的测试流程可能与现有框架不兼容，导致效率降低。
- 专注于测试内部实现细节而非用户可见的结果 → 测试可能通过，但用户的实际操作流程仍然存在问题。
- 在并行测试之间共享认证状态或服务器端数据 → 可能导致测试结果不稳定。
- 在未充分了解页面状态或功能限制之前，就使用`force: true`选项 → 可能掩盖真正的故障。
- 在处理响应缓慢的第三方服务时，依赖`networkidle`等待 → 实际上页面可能已经准备好，但等待操作仍会浪费时间。
- 在可以通过HTTP或API直接解决问题的情况下，仍然启动完整的浏览器 → 增加成本、降低测试稳定性。

## 外部接口说明

| 接口 | 发送的数据 | 目的 |
|----------|-----------|---------|
| 用户请求的Web地址 | 浏览器请求、表单输入数据、cookies、上传文件以及任务所需的页面交互信息 | 用于自动化操作、测试、截图生成、PDF提取等 |
| `https://registry.npmjs.org` | 在可选的安装过程中提供Playwright或Playwright MCP的包元数据和安装文件 | 用于安装Playwright或相关工具 |

**注意：** 不会发送任何其他数据到外部。

## 安全性与隐私保护

- 用户请求的数据：仅发送到用户指定的目标网站。
- 在安装Playwright工具时，可能会通过npm发送一些可选的包安装相关数据。

**数据存储方式：**
- 所有数据均存储在本地：源代码、日志记录、截图、视频文件、PDF文件以及临时浏览器状态，均保存在工作区或系统临时文件夹中。

**注意事项：**
- 本技能不会创建隐藏的内存文件或本地文件夹。
- 不推荐使用任何可能泄露浏览器指纹信息的方法，也不提供任何绕过安全限制的解决方案。
- 默认情况下，不会持久化用户的会话状态或凭证信息。
- 除非仓库有明确要求，否则不会在任务范围之外发送额外的网络请求。
- 对于高风险的生产环境，除非用户明确授权，否则不会自动执行任何操作。

## 信任机制

使用此技能时，所有浏览器请求都会发送到用户指定的目标网站；如果需要安装第三方包，数据会通过npm进行传输。

**相关技能：**
- 根据用户需求，可以使用以下命令安装相关工具：`clawhub install <slug>`：
  - `web`：在启动实际浏览器操作之前，先进行基于HTTP的初步探索。
  - `scrape`：当浏览器自动化不是主要任务时，提供更全面的数据提取功能。
  - `screenshots`：在浏览器操作完成后，用于捕获和优化视觉结果。
  - `multi-engine-web-search`：在自动化之前，用于查找和筛选目标页面。

## 反馈方式：
- 如果觉得本技能有用，请给`clawhub`项目点赞（star）。
- 如需保持信息更新，请使用`clawhub sync`命令。