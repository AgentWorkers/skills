---
name: Electron
description: 使用安全的架构构建 Electron 桌面应用程序，并避免常见的陷阱。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["npm"]},"os":["linux","darwin","win32"]}}
---

## 安全性方面的不可妥协原则  
- 必须将 `nodeIntegration` 设置为 `false` — 允许 Node.js 访问的渲染器可能导致跨站脚本（XSS）攻击，从而危及整个系统安全。  
- 必须将 `contextIsolation` 设置为 `true` — 将预加载上下文与渲染器分离，以防止安全漏洞。  
- 明确允许使用的 IPC（Inter-Process Communication）通道必须被列入白名单；绝不能将任意通道名称从渲染器转发出去。  
- 必须验证所有 IPC 消息的内容 — 因为渲染器是不可信的，应将其视为外部 API 的输入。  
- 绝不要在渲染器中使用 `eval()` 或 `new Function()` — 这会破坏所有的安全防护机制。  

## 预加载脚本的相关规则  
- `contextBridge.exposeInMainWorld()` 是唯一安全的接口 — 直接使用原始的 `ipcRenderer` 会带来安全风险。  
- 在数据传递之前必须对其进行克隆，以防止原型污染攻击。  
- 应尽可能减少暴露的 API 接口数量，仅暴露特定的功能，而不是通用的发送/接收操作。  

## 架构方面的注意事项  
- `webPreferences` 在窗口创建后就不能被修改了，因此无法之后再启用 `nodeIntegration`。  
- 阻止主线程的执行会导致所有窗口冻结；所有操作都应该是异步的，不能进行同步的文件操作。  
- 每个 `BrowserWindow` 都运行在独立的渲染器进程中，因此无法直接共享 JavaScript 变量。  
- 如果先设置 `show: false`，再设置 `ready-to-show`，可以避免出现闪屏现象，使应用程序看起来更像原生应用。  

## 使用原生模块时的问题  
- 预编译好的原生模块可能无法直接使用，必须针对 Electron 的具体版本重新编译。  
- 每次升级 Electron 后都需要执行 `electron-rebuild`；版本不匹配可能会导致运行时崩溃。  
- N-API（Native Application Programming Interface）模块比基于 nan.js 的模块更稳定，更能适应 Electron 的升级。  

## 打包过程中的陷阱  
- 开发环境所需的依赖项默认会被包含在最终包中，如果不明确排除，生产环境的包会变得过于庞大。  
- 对于 macOS 的自动更新，代码签名是必需的；未签名的应用程序无法使用 Squirrel 这个打包工具。  
- 在 Windows 上，显示通知需要调用 `app.setAppUserModelId()`；如果不执行此操作，通知功能可能会失效。  
- ASAR（Archive Storage and Retrieval）格式并不提供加密保护，源代码可以用简单的工具查看，因此不要将其用于存储敏感信息。  

## 平台特定的问题  
- CORS（Cross-Origin Resource Sharing）策略会阻止使用 `file://` 协议；应使用自定义协议（如 `app://`）或本地服务器。  
- Windows 系统需要 NSIS 或 Squirrel 工具来进行自动更新；安装程序的格式非常重要。  
- macOS 的通用二进制文件需要使用 `--universal` 标志来同时支持 Intel 和 ARM 架构。  

## 内存与性能方面  
- 未关闭的窗口会占用内存；使用完窗口后应显式调用 `win.destroy()` 来释放内存。  
- 对于占用大量内存的模块，应采用延迟加载的方式；启动时间会直接影响用户的体验。  
- 如果定时器在窗口最小化后仍需要执行，应将 `backgroundThrottling` 设置为 `false`。  

## 调试技巧  
- 主进程可以通过 `--inspect` 标志进行调试，也可以通过 `chrome://inspect` 进行连接。  
- 可以使用 `webContents.openDevTools()` 或键盘快捷键来调试渲染器。  
- 使用 `electron-log` 来记录日志；`console.log` 的输出在应用程序重启后会消失，因此需要使用 `electron-log` 来保存日志。