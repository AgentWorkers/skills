---
name: gemini-computer-use
description: 使用 Playwright 构建并运行 Gemini 2.5 的“Computer Use”浏览器控制代理。当用户希望通过 Gemini 的“Computer Use”模型自动化浏览器任务、需要代理循环（截图 → 函数调用 → 操作 → 函数响应），或者要求为高风险 UI 操作添加安全确认功能时，可以使用该代理。
---

# Gemini 计算机使用指南

## 快速入门

1. 下载环境文件（`env.txt`）并设置您的 API 密钥：

   ```bash
   cp env.example env.sh
   $EDITOR env.sh
   source env.sh
   ```

2. 创建虚拟环境并安装所需依赖项：

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install google-genai playwright
   playwright install chromium
   ```

3. 通过命令行运行代理脚本：

   ```bash
   python scripts/computer_use_agent.py \
     --prompt "Find the latest blog post title on example.com" \
     --start-url "https://example.com" \
     --turn-limit 6
   ```

## 浏览器选择

- 默认浏览器：Playwright 自带的 Chromium（无需设置环境变量）。
- 可通过 `COMPUTER_USE_BROWSER_CHANNEL` 选择 Chrome 或 Edge 浏览器。
- 如果您希望使用自定义的 Chromium 基础浏览器（例如 Brave），请通过 `COMPUTER_USE_BROWSER_EXECUTABLE` 进行配置。
- 当这两个参数都设置时，`COMPUTER_USE_BROWSER_EXECUTABLE` 的设置将优先生效。

## 核心工作流程（代理循环）

1. 捕获屏幕截图，并将用户操作内容及截图发送给模型。
2. 解析模型返回的 `function_call` 指令。
3. 在 Playwright 中执行相应的操作。
4. 如果模型要求用户确认操作（`safety_decision` 为 `requireconfirmation`），在执行操作前会提示用户确认。
5. 将包含最新页面链接及截图的 `function_response` 对象发送给模型。
6. 重复此过程，直到模型仅返回文本（表示操作已完成）或达到操作次数上限。

## 运行指南

- 请在沙箱环境或容器中运行脚本。
- 使用 `--exclude` 参数来阻止模型执行某些风险操作。
- 保持视口大小为 1440x900 像素，除非有特殊需求需要调整。

## 参考资源

- 脚本：`scripts/computer_use_agent.py`
- 参考文档：`references/google-computer-use.md`
- 环境配置模板：`env.example`