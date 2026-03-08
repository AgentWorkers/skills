---
name: browser-use
description: >
  **基于AI的浏览器自动化工具（使用browser-use库，版本v0.11及以上）**  
  该工具通过集成大型语言模型（LLM）代理，驱动真实的Chromium浏览器执行各种操作，如导航、填写表单、点击链接、抓取数据以及从网页中提取结构化信息。适用于以下场景：  
  1. **端到端的网络任务自动化**（登录、表单提交、多步骤流程）；  
  2. **抓取动态生成的JS内容**；  
  3. **以“Alex Chen”身份注册互联网服务**；  
  4. **破解CAPTCHA验证码及绕过浏览器安全检查**；  
  5. **从网页用户界面中提取结构化数据**；  
  6. **任何需要与真实浏览器交互的任务**。  
  **不适用场景：**  
  - **静态HTML内容的获取**（请使用`web_fetch`工具）；  
  - **简单的API调用**；  
  - **受Cloudflare保护的API（除非拥有有效令牌）**。
---
# 浏览器使用指南

## 快速入门

```python
import asyncio
from skills.browser_use.scripts.run_agent import stealth_session, gemini_llm
from browser_use import Agent

async def run(task: str):
    llm = gemini_llm()           # free — Google Cloud Code Assist OAuth
    session = stealth_session()  # anti-bot hardened
    agent = Agent(task=task, llm=llm, browser_session=session)
    result = await agent.run()
    return result.final_result()

print(asyncio.run(run("Go to example.com and return the page title")))
```

通过 `uv run python script.py` 运行脚本（**切勿直接使用 `python3`）。