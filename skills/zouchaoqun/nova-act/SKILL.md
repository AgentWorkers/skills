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

使用 Amazon Nova Act 进行基于 AI 的浏览器自动化操作。内置的脚本可以处理常见的任务；对于复杂的工作流程，您可以编写自定义脚本。如需获取免费的 API 密钥，请访问 https://nova.amazon.com/dev/api。

## 数据与隐私声明

**本技能的访问权限：**
- **读取：** `NOVA_ACT_API_KEY` 环境变量或 `~/.openclaw/openclaw.json` 文件中的 API 密钥
- **写入：** 当前工作目录中的 Nova Act 日志文件（包含截图和会话记录）

**日志文件可能包含的内容：**
- 访问过的每个页面的截图
- 页面的完整内容（HTML、文本）
- 浏览器操作以及 AI 的决策过程

**建议：**
- 请注意，日志文件可能会捕获访问页面中显示的 **个人身份信息（PII）或敏感数据**；
- 如果日志文件包含敏感内容，请在使用后及时审查或删除。

## 安全防护措施

### 对 AI 代理的指示

**在以下操作之前务必停止：**
- 任何可能导致财务损失的操作
- 任何涉及外部通信的操作
- 任何创建账户的操作
- 任何修改数据的操作

当任务包含可能产生实际影响的操作时（请参阅 `scripts/nova_act_runner.py` 文件中的 `MATERIAL_IMPACT_KEYWORDS`），您必须：
1. 导航到最终操作步骤（如结账页面、提交按钮或发布界面）
2. 确认最终操作是可执行的（按钮存在且处于启用状态）
3. 使用 `act_get()` 功能进行观察，但不要点击最终操作按钮
4. 在未完成操作的情况下向用户报告观察结果

**需要停止操作的类别：**
- **财务相关操作**：购买、付款、订阅、捐赠、下单
- **通信相关操作**：发布、分享、发送邮件、消息、推文
- **账户创建相关操作**：注册新账户
- **提交相关操作**：提交申请、报名、预订
- **删除或销毁相关操作**：删除数据、移除内容、取消操作

### 安全保障

在执行浏览器自动化操作时，本技能 **绝不会**：
- 完成实际的购买或财务交易
- 创建真实账户或注册服务
- 在任何平台上公开发布内容
- 发送邮件、消息或进行其他通信
- 提交会导致不可逆实际后果的表单

本技能 **始终会**：
- 在任何可能产生实际影响的操作之前停止
- 在执行不可逆操作之前请求用户的明确确认
- 在检测到可能产生实际影响的操作时报告观察结果
- 在输出中记录所有安全停止的操作

有关详细的安全部署指南，请参阅 `references/nova-act-cookbook.md`。

## 使用内置脚本快速入门

当需要执行浏览器自动化任务时，只需调用内置脚本：

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

其中 `url` 和 `task` 是由用户请求设置的 Python 字符串变量。

该脚本使用通用格式（包含摘要和详细信息列表）来记录操作结果。

## 编写自定义脚本

对于复杂的多步骤工作流程或特定的数据提取需求，您可以编写符合 PEP 723 标准的 Python 自定义脚本：

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

使用以下命令运行脚本：`uv run script.py`

## 核心 API 函数

### `nova_act(prompt)` - 执行操作

用于点击、输入、滚动和导航。**注意：** 操作的上下文最好在单次 `act()` 调用中保持一致，因此请将相关操作合并到一个提示中。

```python
nova.act("""
    Click the search box.
    Type 'automation tools' and press Enter.
    Scroll down to the results section.
    Select 'Relevance' from the sort dropdown.
""")
```

### `nova_act_get(prompt, schema)` - 提取数据

使用 Pydantic 模型或 Python 数据类型来结构化地提取数据：

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
    # SAFETY STOP: Only extracted data. Did NOT select a flight or proceed to booking.
```

### 表单填写

```python
with NovaAct(starting_page="https://example.com/contact") as nova:
    nova.act("""
        Fill the form: name 'Test User', email 'test@example.com'.
        Select 'United States' for country.
    """)

    # SAFETY STOP: Verify submit button exists but DO NOT click it
    submit_ready = nova.act_get(
        "Is there a submit button visible and enabled?",
        schema=bool
    )
    print(f"Form ready to submit: {submit_ready}")
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
1. **合并操作步骤**：Nova Act 最适合在单次 `act()` 调用中处理一系列操作。将相关操作合并到一个多行提示中。
2. **使用具体日期**：浏览器代理可能无法正确理解相对日期（如“下周一”）。请在任务提示中提供具体的日期（例如“2025 年 3 月 15 日”）。
3. **明确提示操作内容**：例如“点击底部的蓝色‘提交’按钮”，而不是简单地说“点击提交”。
4. **提供提取数据的结构化格式**：在使用 `act_get()` 时，务必提供数据提取的格式化模板。
5. **处理页面加载**：Nova Act 会等待页面加载完成，但在需要时可以添加对动态内容的显式等待时间。
6. **截图验证结果**：使用 `nova.page.screenshot()` 函数来保存操作结果。

## 资源：
- **`references/nova-act-cookbook.md`** — Nova Act 的最佳实践和安全指南，包括 `MATERIAL_IMPACT_KEYWORDS` 的详细说明以及安全的工作流程示例。在进行复杂自动化操作时，请参考该文档。
- **`README.md`** — 为用户提供的安装指南和安全注意事项。

## API 密钥：
- 必需设置 `NOVA_ACT_API_KEY` 环境变量
- 或者在 `~/.openclaw/openclaw.json` 文件中设置 `skills."nova-act".apiKey` 或 `skills."nova-act".env.NOVA_ACT_API_KEY`

## 注意事项：
- Nova Act 会启动真实的 Chrome 浏览器；请确保浏览器能够正常显示页面内容，或使用无头模式（headless mode）。
- 脚本会输出 `MEDIA:` 标识符，以便 OpenClaw 在支持的平台上自动保存截图。
- 如需使用无头模式，请执行 `NovaAct(starting_page="...", headless=True)`。
- 可通过 `nova.page` 访问底层的 Playwright 页面以执行更高级的操作。