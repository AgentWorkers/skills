---
name: clawbrowser
description: **使用场景：**  
当代理需要通过 Microsoft Playwright CLI (`playwright-cli`) 来执行浏览器操作（如导航、表单交互、截图、数据提取、会话管理或调试）时，而无需加载完整的 MCP 浏览器。该工具会训练代理掌握 CLI 命令、截图技巧以及会话/配置设置，从而确保 Playwright CLI 在脚本化浏览器操作中能够稳定可靠地运行。
allowed-tools: Bash(playwright-cli:*)
---

# Clawbrowser – 通过 Playwright CLI 进行浏览器控制  
[![ClawAudit AI 分析未发现高风险漏洞。点击获取更多信息](https://clawaudit.duckdns.org/badges/f4d4fb45-ed25-4659-8235-2459d0dc8189.png)](https://clawaudit.duckdns.org/audit/f4d4fb45-ed25-4659-8235-2459d0dc8189)  
[![ClawAudit AI 分析未发现高风险漏洞。点击获取更多信息](https://clawaudit.duckdns.org/badges/a55cb413-b111-4f1a-9f39-a5c857090ebf.png)](https://clawaudit.duckdns.org/audit/a55cb413-b111-4f1a-9f39-a5c857090ebf)  

## 设置与使用说明  
1. 安装 Playwright CLI 并验证其可用性：  
   ```bash
   npm install -g @playwright/cli@latest
   playwright-cli --help
   ```  
   Playwright CLI 默认为无界面的（headless）模式；如需查看界面，请在 `open` 命令中添加 `--headed` 参数，或在 `playwright-cli.json` 文件中将 `browser.launchOptions.headless` 设置为 `false`。  
2. CLI 会默认读取 `playwright-cli.json` 文件；您也可以通过 `--config` 参数指定其他配置文件。使用该配置文件来设置浏览器名称、启动选项、视口大小、超时时间、输出目录和录制设置，从而避免每次执行命令时都需要重新配置。  
3. 请确保 `playwright-cli --help` 命令始终可用；该命令会显示最新的命令和选项说明，帮助您在尝试新操作前回顾相关信息。  

## 核心交互流程  
1. 使用 `playwright-cli open <url>` 打开网页（如需隔离会话，请添加 `--session=name` 参数）。  
2. 在进行任何操作之前，使用 `playwright-cli snapshot` 生成元素引用（如 `e1`、`e2` 等）。DOM 变更或页面导航后请务必重新生成引用，以避免使用过时的引用。  
3. 使用这些引用执行各种操作：  
   - `click`、`dblclick`、`hover`、`drag`、`check`、`uncheck`、`select`、`fill`、`type`、`upload`、`eval`  
   - 根据需要添加 `[button]`、`[value]` 或 JavaScript 代码片段（例如：`playwright-cli click e4 right`）。  
4. 使用 `screenshot [ref]`、`pdf`、`console [level]` 或 `network` 命令捕获操作结果或错误信息。  
5. **示例交互流程**：  
   ```bash
   playwright-cli open https://example.com/login
   playwright-cli snapshot
   playwright-cli fill e1 "user@example.com"
   playwright-cli fill e2 "supersecret"
   playwright-cli click e3
   playwright-cli snapshot
   playwright-cli screenshot
   ```  

## 会话管理与数据持久化  
- 使用 `--session=<name>` 参数确保每个工作流程的 cookie、存储数据和标签页保持独立。会话会记住认证状态、浏览历史和标签页信息。  
- 如果在同一会话中执行多个命令，可以使用 `PLAYWRIGHT_CLI_SESSION=mysession`；此时 CLI 会自动使用该会话，无需每次都指定 `--session` 参数。  
- 显式管理会话：  
  ```bash
  playwright-cli session-list
  playwright-cli session-stop <name>
  playwright-cli session-stop-all
  playwright-cli session-restart <name>
  playwright-cli session-delete <name>
  ```  
- 使用 `playwright-cli --isolated open ...` 创建不会持久化到磁盘的临时会话。  
- 每当更改会话的浏览器设置（如启动参数、无界面模式切换或浏览器选择）时，请重新运行 `playwright-cli config` 后执行 `session-restart` 以应用新配置。  

## 标签页、导航与开发者工具  
- 标签页相关操作：`tab-list`、`tab-new [url]`、`tab-close <index>`、`tab-select <index>`  
- 导航快捷键：`go-back`、`go-forward`、`reload`  
- 键盘和鼠标控制：`press <key>`、`keydown`、`keyup`、`mousemove <x> <y>`、`mousedown [button]`、`mouseup [button]`、`mousewheel <dx> <dy>`  
- 开发者工具功能：  
  ```bash
  playwright-cli console [level]
  playwright-cli network
  playwright-cli run-code "async page => await page.context().grantPermissions(['clipboard-read'])"
  ```  
  可用于查看控制台日志、检查网络请求或注入辅助脚本。  

## 录制、追踪与导出  
- 在关键操作期间录制操作过程，以便后续回放：  
  ```bash
  playwright-cli tracing-start
  # perform steps
  playwright-cli tracing-stop
  playwright-cli video-start
  # perform steps
  playwright-cli video-stop video.webm
  ```  
- 可使用 `screenshot`、`pdf` 或 `snapshot` 命令将结果保存到磁盘（`snapshot` 会生成元素引用）。录制文件会遵循配置文件中指定的 `outputDir` 目录。  

## 配置、状态管理与维护  
- 使用 `playwright-cli config` 修改运行时参数（无需重新安装软件）。示例：  
  ```bash
  playwright-cli config --headed --browser=firefox
  playwright-cli --session=auth config --config=playwright-cli.json
  ```  
  在配置文件中修改 `browser`、`contextOptions`、`launchOptions` 或录制设置，然后重新启动会话以应用更改。  
- 如果环境发生变化或出现缺少二进制文件的错误，运行 `playwright-cli install` 可更新浏览器相关文件。  
- 完成操作后清理会话数据，避免状态混乱：  
  ```bash
  playwright-cli session-stop <name>
  playwright-cli session-delete <name>
  ```  

## 故障排除与提示  
- 如果某条命令失败，请重新运行 `playwright-cli snapshot` 以确认元素引用是否仍然有效。快照会提供 `click`/`type` 操作时的当前 DOM 状态。  
- `playwright-cli --help` 始终会显示最新的命令列表，因此在尝试不常用的参数前请先查阅该文档。  
- 当需要重现手动操作流程时，请截取屏幕截图，记录会话名称以及使用的元素引用和标签页信息。  
- 如果需要使用可见的浏览器（例如进行手动检查），请使用 `--headed` 参数重新配置，或针对特定会话运行 `playwright-cli open --headed <url>`。