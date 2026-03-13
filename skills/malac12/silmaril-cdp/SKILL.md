---
name: silmaril-cdp
description: 浏览器自动化、DOM元素检查、页面内容修改、等待操作协调、流程执行以及本地代理设置等功能都是通过 Silmaril Chrome DevTools 协议工具包来实现的。当需要使用 Chrome 浏览器并开启 CDP（Chrome DevTools Protocol）模式时，该工具包非常实用：它可以用于导航页面、读取 DOM 结构或源代码、提取结构化数据、对页面元素进行点击或输入操作、执行 JavaScript 代码、等待用户界面状态的变化，以及运行基于 Silmaril 的流程控制 JSON 文件，同时还能管理由 mitmproxy 提供的本地代理设置。
---
# Silmaril CDP

使用此技能可以通过 PowerShell 操作本地的 Silmaril 工具包。

## 定位工具包

- 在当前环境中，建议使用路径 `D:\silmairl cdp\silmaril.cmd`。
- 如果该路径不存在，请在 `PATH` 环境变量中或附近的代码库中查找 `silmaril.cmd` 文件。
- 通过 PowerShell 运行该命令：`& 'D:\silmairl cdp\silmaril.cmd' ...`。

## 如果工具包未安装，请进行安装

在 Windows 系统上，如果工具包尚未安装，请按照以下步骤进行安装：

只有在用户明确同意获取或安装远程代码后，才执行克隆或复制工具包的操作：

1. 克隆或复制仓库：
   `git clone https://github.com/Malac12/CDP-tools.git "D:\silmairl cdp"`

2. 确保已安装 Chrome、Chromium 或 Edge 浏览器。
   该工具包会检查 Windows 的标准安装路径，如果未找到所需浏览器，则会使用 `PATH` 中的 `chrome.exe`。

3. 通过 PowerShell 运行工具包：
   `& 'D:\silmairl cdp\silmaril.cmd' openbrowser --json`
   `& 'D:\silmairl cdp\silmaril.cmd' openUrl 'https://example.com' --json`
   `& 'D:\silmairl cdp\silmaril.cmd' get-text 'body' --json`

以上步骤即可完成 CDP 的核心工作流程。由于 `silmaril.cmd` 使用 `ExecutionPolicy Bypass` 来运行 PowerShell，因此无需更改系统的 PowerShell 执行策略。

## 默认工作流程

1. 使用 `openbrowser` 启动或关联一个 CDP 浏览器。
2. 使用 `openUrl` 导航到目标页面。
3. 使用 `exists`、`get-text`、`query` 或 `get-dom` 来读取页面内容。
4. 仅在验证了选择器后才能对页面内容进行修改。
5. 每次操作完成后，需要等待一个明确的同步信号。
6. 对于需要重复执行的简单操作，建议使用 `run` 命令。

## 操作规则

- 几乎所有命令都建议使用 `--json` 选项，以便后续步骤能够解析结构化输出。
- 在选择元素或检查页面渲染状态时，优先使用实时 DOM 操作（而非 `get-source`）。
- 建议使用稳定的选择器，如 `data-test`、`dataTestId`、语义 ID 和有意义的属性。
- 当存在多个标签页时，可以选择使用 `--target-id` 或 `--url-match`，但切勿同时使用两者。
- 对于诸如 `click`、`type`、`set-text`、`set-html` 和 `eval-js` 等页面操作，建议使用 `--yes` 选项。
- `eval-js`、`proxy-override`、`proxy-switch` 和 `openurl-proxy` 是高风险命令，请谨慎使用。
- 对于 `eval-js`，建议使用 `--allow-unsafe-js` 选项；只有在信任的本地会话中，才可以将 `SILMARIL_ALLOW_UNSAFE_JS` 设置为 1。
- 对于代理相关命令，建议使用 `--allow-mitm` 选项；同样，只有在信任的本地会话中，才可以将 `SILMARIL_ALLOW_MITM` 设置为 1。
- 除非用户明确要求使用 `--allow-nonlocal-bind`，否则代理监听器应绑定到回环地址（loopback address）。
- 如果 JavaScript 代码较长，建议将其保存在文件中，并使用 `eval-js --file` 来执行，而不是直接在命令行中输入。

## 命令选择

- 使用 `get-text` 获取单个文本值。
- 使用 `query` 提取结构化的数据（多行数据）。
- 使用 `get-dom` 来调试选择器或标记相关的问题。
- 仅在原始响应 HTML 对比渲染后的 DOM 更重要时，才使用 `get-source`。
- 使用 `wait-for`、`wait-for-any`、`wait-for-gone`、`wait-for-js` 或 `wait-for-mutation` 来实现同步操作。

## 参考资料

- 阅读 `references/command-patterns.md` 以了解常见的命令格式和安全的 PowerShell 使用示例。
- 在构建或编辑 `run` 流程之前，请阅读 `references/flows.md`。
- 在使用 `openurl-proxy`、`proxy-override` 或 `proxy-switch` 时，请参考 `references/proxy.md`。