---
author: "@canbirlik"
dependencies:
  python:
  - playwright
description: 一个专为 OpenClaw 代理设计的、外观类似人类使用的网页浏览器。支持阅读网页内容、截图功能以及可视化显示模式。
emoji: 🌐
name: claw-browser
platforms:
- darwin
- linux
- win32
---
# 🌐 Claw Browser 技能

该技能为代理程序提供了“眼睛”，使其能够使用真实的 Chromium 浏览器来浏览网页。

与简单的 HTTP 请求不同，`claw-browser` 具有以下特点：

- **渲染 JavaScript**  
- **处理动态内容**  
- **加载单页应用程序（SPA）**  
- **生成真实截图**  
- **支持可视化（非无头模式）运行**  

------------------------------------------------------------------------

# 🛠️ 安装与设置（请先阅读）

⚠️ **在使用此工具之前，代理程序必须先设置 Python 环境并下载浏览器二进制文件。**

如果 `venv` 不存在，请自动运行以下设置命令：

``` bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖项
pip install -r requirements.txt

# 4. 下载 Chromium 二进制文件（关键步骤）
playwright install chromium
```

> ⚠️ `playwright install chromium` 这一步骤至关重要。  
> 如果没有这一步，浏览器将无法启动。

------------------------------------------------------------------------

# 🔧 工具与使用方法

## `browser.py`

### 参数

| 参数                                      | 描述                                      |
|-----------------------------------|-----------------------------------------|
| `--url`                                  | 要访问的网站（**必填**）                            |
| `--action`                               | 执行的操作：`read` 或 `screenshot`                    |
| `--visible`                             | （可选）以可视化模式运行浏览器（非无头模式）。如果用户希望看到浏览器界面，请使用此参数。 |

------------------------------------------------------------------------

# 🚀 执行示例

⚠️ 请始终先激活虚拟环境。

------------------------------------------------------------------------

## 1️⃣ 阅读页面（无头模式 - 默认）

``` bash
source venv/bin/activate && python browser.py --url "https://github.com/trending" --action read
```

------------------------------------------------------------------------

## 2️⃣ 为新闻网站生成截图

``` bash
source venv/bin/activate && python browser.py --url "https://news.ycombinator.com" --action screenshot
```

生成的截图将保存为 `evidence.png`。

------------------------------------------------------------------------

## 3️⃣ 可视化模式（显示浏览器界面 - 适用于演示）

``` bash
source venv/bin/activate && python browser.py --url "https://google.com" --action read --visible
```

这将在一个真实的 Chromium 窗口中显示网页内容。

------------------------------------------------------------------------

## 4️⃣ 可视化模式（WSL / Linux 环境下的解决方法）⭐️

**如果遇到“缺少 X 服务器”或“显示设备未找到”的错误，请使用以下命令：**

``` bash
export DISPLAY=:0 && source venv/bin/activate && python browser.py --url "[https://google.com](https://google.com)" --action read --visible
```

此命令会设置 `DISPLAY` 变量，使浏览器能够在您的屏幕上显示。

------------------------------------------------------------------------

# 🧠 代理程序何时应使用此技能？

在以下情况下使用 `claw-browser`：

- 页面需要 JavaScript 渲染  
- 网站内容是动态的（如 React、Vue、Angular 等）  
- 需要生成截图  
- 用户明确要求“打开”或“查看”某个网站  
- 传统的 HTTP 请求失败  

------------------------------------------------------------------------

# ⚡ 总结

`claw-browser` 将您的 OpenClaw 代理程序从一个简单的 API 调用者，转变为一个具备可视化功能的**真正基于浏览器的辅助工具**。

它支持：

- **动态页面交互**  
- **可视化验证**  
- **适用于演示的浏览体验**  
- **真实世界的自动化操作**  

------------------------------------------------------------------------

由 @canbirlik 制作 ❤️