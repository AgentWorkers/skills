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
        "tools":
          {
            "nova_act":
              {
                "description": "Run a browser automation task using Amazon Nova Act.",
                "parameters":
                  {
                    "type": "object",
                    "properties":
                      {
                        "url":
                          {
                            "type": "string",
                            "description": "Starting URL for the browser session",
                          },
                        "task":
                          {
                            "type": "string",
                            "description": "Natural language task description. IMPORTANT: Resolve relative dates (e.g., 'next Monday') to specific dates (e.g., '2025-03-15') in the prompt.",
                          },
                      },
                    "required": ["url", "task"],
                  },
                "command":
                  [
                    "uv",
                    "run",
                    "{baseDir}/scripts/nova_act_runner.py",
                    "--url",
                    "{{url}}",
                    "--task",
                    "{{task}}",
                  ],
              },
          },
      },
  }
---

# Nova Act 浏览器自动化

使用 Amazon Nova Act 实现基于 AI 的浏览器自动化。内置的脚本可以处理常见的任务；对于复杂的工作流程，您可以编写自定义脚本。要获取免费的 API 密钥，请访问：https://nova.amazon.com/dev/api

## 使用内置脚本快速入门

执行浏览器任务并获取结果：

```bash
uv run {baseDir}/scripts/nova_act_runner.py --url "https://google.com/flights" --task "Find flights from SFO to NYC on March 15 and return the options"
```

该脚本使用通用的数据结构（摘要 + 详细信息列表）来捕获输出结果。

## 编写自定义脚本

对于复杂的多步骤工作流程或特定的数据提取需求，可以使用遵循 PEP 723 标准的 Python 脚本来实现：

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

## 核心 API 函数

### `nova_act(prompt)` - 执行操作

用于点击、输入、滚动、导航等操作。**注意：** 在单个 `act()` 调用中保持上下文的一致性，因此请将相关的操作组合在一起。

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

## 最佳实践

1. **组合操作**：Nova Act 在单个 `act()` 调用中能最好地保持操作上下文的一致性。将相关的操作组合到一个多行的提示语句中。
2. **使用具体的日期**：浏览器代理可能无法正确理解像“下周一”这样的相对日期。请始终在任务提示中提供具体的日期（例如：“2025 年 3 月 15 日”）。
3. **提示要具体**：例如，“点击页面底部的蓝色‘提交’按钮”比“点击提交”更清晰。
4. **使用数据结构进行提取**：在调用 `act_get()` 时，务必提供数据结构化的模式（schema）。
5. **处理页面加载**：Nova Act 会等待页面加载完成，但如果需要处理动态内容，请添加显式的等待时间。
6. **截图验证结果**：使用 `nova.page.screenshot()` 来捕获页面内容。

## API 密钥

- 环境变量 `NOVA_ACT_API_KEY`（必需）
- 或者在 `~/.openclaw/openclaw.json` 文件中设置 `skills."nova-act".apiKey` 或 `skills."nova-act".env.NOVA_ACT_API_KEY`。

## 注意事项

- Nova Act 会启动真实的 Chrome 浏览器；请确保浏览器可以正常显示页面内容，或者使用无头模式（headless mode）。
- 脚本会输出 `MEDIA:` 标签，以便 OpenClaw 在支持的平台上自动保存截图。
- 对于无头模式操作，可以使用 `NovaAct(starting_page="...", headless=True)`。
- 通过 `nova.page` 可以访问底层的 Playwright 页面以执行更高级的操作。