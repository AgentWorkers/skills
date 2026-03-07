---
name: browser-use
description: "一种基于人工智能的浏览器自动化工具，适用于复杂的、多步骤的网页工作流程。当 OpenClaw 内置的浏览器工具无法处理登录流程、反机器人网站或需要超过 5 个步骤的操作序列时，该工具会使用 Browser-Use 框架来完成任务。"
---
# 浏览器使用——AI浏览器自动化

## 安全与隐私

- **不记录凭证信息**：密码通过 `Browser-Use` 的 `sensitive_data` 参数进行处理——大型语言模型（LLM）从未看到真实的凭证信息，仅看到占位符令牌。
- **用户主动启动的 Chrome 连接**：CDP 模式（连接到真实的 Chrome 浏览器）是可选的，需要用户手动以调试模式启动 Chrome。该工具不会在用户不知情的情况下连接到正在运行的浏览器。
- **所有软件包均为开源**：依赖项包括 `browser-use`（在 GitHub 上有 3.8 万星评分）、`playwright`（由微软开发）和 `langchain-openai`——这些都是经过广泛审计的开源工具。
- **仅在本机执行**：脚本仅在用户的机器上运行。除了用于逐步推理的配置好的 LLM API 外，不会向任何服务器发送数据。
- **支持域名限制**：可以使用 `allowed_domains` 参数来限制代理可以访问的网站。
- **不收集使用数据**：该工具不会收集、存储或传输任何使用数据。

## 何时使用 Browser-Use 与内置工具

| 场景 | 内置工具 | Browser-Use |
|----------|:-:|:-:|
| 截图/点击一个按钮 | ✅ 免费且快速 | ❌ 过于复杂 |
| 多步骤工作流程（登录→导航→填写→提交） | ❌ 容易出错 | ✅ |
| 防机器人网站（需要使用真实的 Chrome） | ❌ | ✅ |
| 批量重复操作 | ❌ | ✅ |

**成本**：Browser-Use 在每个步骤都会调用外部 LLM（需要付费且速度较慢）。对于简单操作，建议使用内置工具。

## 执行流程

### 1. 检查环境
```bash
test -d ~/browser-use-env && echo "Installed" || echo "Need install"
```

### 2. 首次设置（仅一次）
```bash
python3 -m venv ~/browser-use-env
source ~/browser-use-env/bin/activate
pip install browser-use playwright langchain-openai
playwright install chromium
```

### 3. 选择模式
- **模式 A — 内置 Chromium**：适用于简单的自动化任务，或者当检测结果不重要时。立即执行。
- **模式 B — 真实 Chrome CDP**：适用于需要使用真实 Chrome 浏览器的防机器人网站，或者当需要用户的登录会话时。需要用户操作。

模式 B 的设置流程：
> 请完全关闭 Chrome（Mac：Cmd+Q），然后告诉我“done”。

用户确认后：
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```
验证：`curl -s http://127.0.0.1:9222/json/version`

### 4. 编写脚本并运行
将脚本写入用户的工作区，然后：
```bash
source ~/browser-use-env/bin/activate
python3 script_path.py
```

### 5. 返回结果
将结果返回给用户。如果失败，请按照以下故障排除步骤进行处理。

## 脚本模板
```python
import asyncio
from browser_use import Agent, ChatOpenAI, Browser

async def main():
    # LLM — any OpenAI-compatible API
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key="<YOUR_API_KEY>",  # From env var or user config
        base_url="https://api.openai.com/v1",
    )

    # Mode A: Built-in Chromium
    browser = Browser(headless=False, user_data_dir="~/.browser-use/task-profile")
    # Mode B: Real Chrome (user must launch with --remote-debugging-port=9222)
    # browser = Browser(cdp_url="http://127.0.0.1:9222")

    agent = Agent(
        task="Detailed step-by-step task description (see guide below)",
        llm=llm, browser=browser,
        use_vision=True, max_steps=25,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## 任务编写指南

### ✅ 正确的写法：具体步骤
```python
task = """
1. Open https://www.reddit.com/login
2. Enter username: x_user
3. Enter password: x_pass
4. Click login button
5. If CAPTCHA appears, wait 30s for user to complete
6. Navigate to https://www.reddit.com/r/xxx/submit
7. Enter title: xxx
8. Enter body: xxx
9. Click submit
"""
```

### ❌ 错误的写法：表述模糊
```python
task = "Post something on Reddit"
```

### 提示：
- **键盘替代方案**：添加 “如果按钮无法点击，可以使用 Tab+Enter”。
- **错误处理**：添加 “如果页面加载失败，刷新后重试”。
- **敏感数据**：使用占位符和 `sensitive_data` 参数。

## 凭证安全
```python
agent = Agent(
    task="Login with x_user and x_pass",
    sensitive_data={"x_user": "real@email.com", "x_pass": "S3cret!"},
    use_vision=False,  # Disable screenshots when handling passwords
    llm=llm, browser=browser,
)
```

## 关键参数

| 参数 | 用途 | 推荐值 |
|-----------|---------|-------------|
| `use_vision` | 是否让 AI 查看截图 | 通常设置为 True，处理密码时设置为 False |
| `max_steps` | 最大操作步骤数 | 20-30 |
| `max_failures` | 最大重试次数 | 3（默认值） |
| `flash_mode` | 是否跳过推理 | 对于简单任务，设置为 True |
| `extend_system_message` | 自定义指令 | 添加具体的操作指导 |
| `allowed_domains` | 限制可访问的域名 | 用于安全目的 |
| `fallback_llm` | 备用 LLM | 当主 LLM 不稳定时使用 |

## 故障排除
```
Detected as automation?
  └→ Switch to Mode B (real Chrome)

CAPTCHA / human verification?
  └→ Prompt user to complete manually, add wait time in task

LLM timeout?
  └→ Set fallback_llm or use faster model

Action succeeded but no effect (e.g. post not published)?
  └→ 1. Check if platform anti-spam blocked it (common with new accounts)
     2. Add explicit confirmation steps to task

Website UI changed, can't find elements?
  └→ Browser-Use auto-adapts, but add fallback paths in task
```

## LLM 兼容性

| LLM | 是否兼容 | 备注 |
|-----|:---:|-------|
| GPT-4o / 4o-mini | ✅ | 最佳选择，推荐使用 |
| Claude | ✅ | 运行良好 |
| Gemini | ❌ | 结构化输出不兼容 |