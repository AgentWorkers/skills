---
name: nova-act
description: 使用 Amazon Nova Act 编写并执行 Python 脚本，以实现基于人工智能的浏览器自动化任务，例如航班搜索、数据提取和表单填写。
homepage: https://nova.amazon.com/act
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["uv"], "env": ["NOVA_ACT_API_KEY"] },
        "primaryEnv": "NOVA_ACT_API_KEY",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---
# Nova Act 浏览器自动化

使用 Amazon Nova Act 进行基于 AI 的浏览器自动化操作。内置的脚本可以处理常见的任务；对于复杂的工作流程，您可以编写自定义脚本。如需获取免费的 API 密钥，请访问：https://nova.amazon.com/dev/api

## 数据与隐私声明

**本技能会访问的数据：**
- **读取：** `NOVA_ACT_API_KEY` 环境变量或 `~/.openclaw/openclaw.json` 文件中的 API 密钥
- **写入：** 当前工作目录下的 Nova Act 日志文件（包含截图和会话记录）

**日志文件可能包含的内容：**
- 访问过的每个页面的截图
- 页面的完整内容（HTML、文本）
- 浏览器操作及 AI 的决策过程

**建议：**
- 请注意，日志文件可能会记录访问页面上显示的 **个人身份信息（PII）或敏感数据**；
- 如果日志文件包含敏感内容，请在使用后及时删除。

## 安全保障

在执行浏览器自动化操作时，本技能 **绝不会**：
- 完成任何实际的购买或财务交易
- 创建真实账户或注册服务
- 在任何平台上公开发布内容
- 发送电子邮件、消息或进行其他形式的通信
- 提交可能导致不可逆实际后果的表单

**本技能会始终：**
- 在执行任何可能产生实际影响的操作之前停止
- 在执行不可逆操作前请求用户的明确确认
- 报告发现的结果，而不会执行破坏性操作

## 使用内置脚本快速入门

当需要执行浏览器自动化任务时，只需调用内置脚本即可：

```python
import subprocess, os, sys

skill_dir = os.path.expanduser("~/.openclaw/skills/nova-act")
script = os.path.join(skill_dir, "scripts", "nova_act_runner.py")

result = subprocess.run(
    ["uv", "run", script, "--url", url, "--task", task],
    capture_output=True, text=True, env={**os.environ}
)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr, file=sys.stderr)
```

其中 `url` 和 `task` 是根据用户请求设置的 Python 字符串变量。

该脚本使用通用格式（摘要 + 详细信息列表）来记录操作结果。

## 编写自定义脚本

对于复杂的多步骤工作流程或特定的数据提取需求，可以使用符合 PEP 723 标准的 Python 脚本进行开发：

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["nova-act"]
# ///

from nova_act import NovaAct

with NovaAct(starting_page="https://example.com") as nova:
    # Execute actions with natural language
    # Combine steps into a single act() call to maintain context
    nova.act("Click the search box, type 'automation', and press Enter")

    # Extract data with schema
    results = nova.act_get(
        "Get the first 5 search result titles",
        schema=list[str]
    )
    print(results)

    # Take screenshot
    nova.page.screenshot(path="search_results.png")
    print(f"MEDIA: {Path('search_results.png').resolve()}")
```

运行方式：`uv run script.py`

## 核心 API 接口

### `nova_act(prompt)` - 执行操作

用于点击、输入、滚动和导航等操作。**注意：** 最佳做法是在一次 `act()` 调用中保持操作的连续性，因此请将相关操作组合在一起。

```python
nova.act("""
    Click the 'Sign In' button.
    Type 'hello@example.com' in the email field.
    Scroll down to the pricing section.
    Select 'California' from the state dropdown.
""")
```

### `nova_act_get(prompt, schema)` - 提取数据

使用 Pydantic 模型或 Python 类型来结构化地提取数据：

```python
from pydantic import BaseModel

class Flight(BaseModel):
    airline: str
    price: float
    departure: str
    arrival: str

# Extract single item
flight = nova.act_get("Get the cheapest flight details", schema=Flight)

# Extract list
flights = nova.act_get("Get all available flights", schema=list[Flight])

# Simple types
price = nova.act_get("What is the total price?", schema=float)
items = nova.act_get("List all product names", schema=list[str])
```

## 常见使用场景

### 航班搜索

```python
with NovaAct(starting_page="https://google.com/flights") as nova:
    # Combine steps to ensure the agent maintains context through the flow
    nova.act("""
        Search for round-trip flights from SFO to JFK.
        Set departure date to March 15, 2025.
        Set return date to March 22, 2025.
        Click Search.
        Sort by price, lowest first.
    """)

    flights = nova.act_get(
        "Get the top 3 cheapest flights with airline, price, and times",
        schema=list[Flight]
    )
```

### 表单填写

```python
with NovaAct(starting_page="https://example.com/signup") as nova:
    nova.act("""
        Fill the form: name 'John Doe', email 'john@example.com'.
        Select 'United States' for country.
        Check the 'I agree to terms' checkbox.
        Click Submit.
    """)
```

### 数据提取

```python
with NovaAct(starting_page="https://news.ycombinator.com") as nova:
    stories = nova.act_get(
        "Get the top 10 story titles and their point counts",
        schema=list[dict]  # Or use a Pydantic model
    )
```

## 最佳实践：
1. **组合操作步骤**：Nova Act 在一次 `act()` 调用中能更好地保持操作上下文。请将相关操作合并到一个多行的命令中。
2. **使用具体日期**：浏览器代理可能无法正确处理相对日期（如“下周一”）。请在命令中始终提供具体的日期（例如：“2025 年 3 月 15 日”）。
3. **明确命令内容**：例如，“点击页面底部的蓝色‘提交’按钮”比“点击提交”更具体。
4. **使用数据提取模板**：向 `act_get()` 提供数据提取的模板，以确保数据提取的准确性。
5. **处理页面加载**：Nova Act 会等待页面加载完成，但在需要时也可以手动设置等待时间以处理动态内容。
6. **截图验证结果**：使用 `nova.page.screenshot()` 来保存操作结果。

## API 密钥：
- 必需的环境变量：`NOVA_ACT_API_KEY`
- 或者在 `~/.openclaw/openclaw.json` 文件中设置 `skills."nova-act".apiKey` 或 `skills."nova-act".env.NOVA_ACT_API_KEY`

## 注意事项：
- Nova Act 会启动真实的 Chrome 浏览器；请确保浏览器能够正常显示页面内容，或使用无头模式（headless mode）。
- 脚本会输出 `MEDIA:` 标识，以便 OpenClaw 在支持的平台上自动保存截图。
- 如需无头模式运行，请使用：`NovaAct(starting_page="...", headless=True)`
- 可通过 `nova.page` 访问底层 Playwright 页面以执行更高级的操作。