---
name: browser-use
description: >
  基于AI的浏览器自动化工具，使用 `browser-use` 库（版本 0.11 及以上）。该工具通过集成大型语言模型（LLM）代理来控制真实的 Chromium 浏览器，实现网页导航、表单填写、点击操作、数据抓取以及从任何网站中提取结构化数据的功能。适用场景包括：  
  1. 完整自动化网页任务（登录、表单提交、多步骤流程）；  
  2. 抓取动态生成的 JavaScript 页面内容；  
  3. 以“Alex Chen”身份注册互联网服务；  
  4. 解决验证码问题并绕过浏览器安全检查；  
  5. 从网页用户界面中提取结构化数据；  
  6. 任何需要与真实浏览器交互的任务。  
  **不适用场景：**  
  - 静态 HTML 页面的获取（请使用 `web_fetch`）；  
  - 简单的 API 调用；  
  - 被 Cloudflare 保护的 API（除非拥有有效的访问令牌）。
---
# 浏览器使用指南

## 快速入门

```python
import asyncio
from browser_use import Agent, BrowserSession, BrowserProfile
from langchain_anthropic import ChatAnthropic

async def run(task: str):
    llm = ChatAnthropic(model="claude-sonnet-4-5")
    session = BrowserSession(headless=True)
    agent = Agent(task=task, llm=llm, browser_session=session)
    result = await agent.run()
    return result.final_result()

print(asyncio.run(run("Go to example.com and return the page title")))
```

通过 `uv run python script.py` 命令来运行脚本（切勿直接使用 `python3`）。

## LLM（大型语言模型）设置

推荐使用 Anthropic（已通过环境变量配置）：

```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-5", timeout=60)
```

其他可选模型：`ChatOpenAI`、`ChatGroq`、`ChatOllama`——均可通过 `browser_use` 模块导入。

## 浏览器会话选项

```python
session = BrowserSession(
    headless=True,           # True for server; False to watch locally
    executable_path="/usr/bin/chromium-browser",  # system chromium
)
```

在多次运行代理时重用会话，以保持 cookie 和认证状态的一致性。

## 结构化输出

使用 `output_model_schema` 提取输入的数据：

```python
from pydantic import BaseModel

class Result(BaseModel):
    title: str
    price: float

agent = Agent(task="...", llm=llm, output_model_schema=Result)
history = await agent.run()
data = history.final_result()  # parsed Result instance
```

## 敏感数据

在传递凭证时，确保不会将其暴露给 LLM：

```python
agent = Agent(
    task="Log in with username {user} and password {pass}",
    llm=llm,
    sensitive_data={"user": "alex@example.com", "pass": "secret"},
)
```

## 常见操作模式

请参阅 `references/patterns.md`，了解以下内容：
- 表单提交与登录流程
- 带分页的多页面爬取
- 文件下载与上传
- 等待动态内容的加载
- 错误处理与重试机制

## 身份信息（Alex Chen）

注册服务时，请使用以下信息：
- 姓名：Alex Chen
- 出生日期：1998年1月18日
- 电子邮件：alex.chen31337@gmail.com
- 通过 `sensitive_data={}` 传递凭证——切勿在任务字符串中直接硬编码凭证信息。

## 环境变量设置

```
ANTHROPIC_API_KEY     # for ChatAnthropic
OPENAI_API_KEY        # for ChatOpenAI (optional)
BROWSER_USE_HEADLESS  # set "false" to watch locally
```