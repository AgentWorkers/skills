---
name: shipment-tracker
description: "**跨运输公司追踪包裹（USPS、UPS、FedEx、DHL、Amazon、OnTrac、LaserShip）**  
**使用场景：**  
- 当用户查询包裹状态时；  
- 当用户添加包裹跟踪号码时；  
- 当用户希望接收配送更新信息时；  
- 当用户提及包裹运输情况时。  
**工作原理：**  
- 该工具会读取包含包裹信息的 Markdown 文件；  
- 通过分析跟踪号码的模式自动识别运输公司；  
- 然后查询包裹的实时状态。  
**技术实现方式：**  
- 首先尝试通过 HTTP 直接查询包裹状态；  
- 对于那些需要使用 JavaScript 来加载页面的运输公司（如 UPS、FedEx 等），系统会建议用户通过浏览器进行查询。"
---
# 货物追踪器

该工具能够通过一个 Markdown 格式的货物文件，追踪多个运输公司的包裹。它能够根据追踪号码的格式自动识别运输公司。在状态查询方面，该工具采用混合方式：首先尝试通过 HTTP 直接获取信息，如果失败，则建议用户使用浏览器来查看完整的追踪详情。

## 货物文件格式

该工具会读取一个包含活跃货物信息的 Markdown 文件：

```markdown
# Active Shipments

| Order | Item | Carrier | Tracking | Link | Added |
|-------|------|---------|----------|------|-------|
| Acme #1234 | Widget | USPS | 9449050899562006763949 | [Track](https://...) | 2026-02-19 |
```

- **运输公司** 和 **追踪链接** 是可选字段——会根据追踪号码的格式自动识别
- 一旦包裹送达，相关条目将从文件中删除，以保持文件整洁
- 默认文件位置：工作区内的 `memory/shipments.md`

## 使用方法

```bash
# Check all active shipments
python3 scripts/shipment_tracker.py memory/shipments.md

# JSON output for integrations
python3 scripts/shipment_tracker.py memory/shipments.md --format json

# Detect carrier from a tracking number
python3 scripts/shipment_tracker.py --detect 9449050899562006763949
```

## 运输公司识别

该工具能够根据追踪号码的格式自动识别运输公司：

| 运输公司 | 标识模式示例 |
|---------|-----------------|
| USPS | 92, 93, 94, 95 + 后续 20-26 位数字 |
| UPS | 1Z + 后续 16 位字母数字组合 |
| FedEx | 12、15 或 20 位数字；前缀为 7489 |
| DHL | 10-11 位数字或 3 个字母 + 后续 7 位数字 |
| Amazon | TBA + 后续 12 位数字 |
| OnTrac | C 或 D + 后续 14 位数字 |
| LaserShip | L + 一个字母 + 后续 8 位数字 |

## 状态查询（混合方式）

1. **直接通过 HTTP 获取**：尝试使用 `urllib` 从运输公司的追踪页面获取包裹状态。这种方法适用于 USPS 及部分其他运输公司。
2. **使用浏览器**（备用方案）：当 HTTP 请求失败或运输公司的页面依赖大量 JavaScript 代码时，脚本会提供相应的浏览器命令，以便用户直接在浏览器中查看包裹状态。

如果脚本输出包含 `needs_browser_use: true`，则表示需要使用浏览器来查看包裹状态：

```python
python3 -c "
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse
async def main():
    browser = Browser(use_cloud=True)
    llm = ChatBrowserUse()
    agent = Agent(
        task='Go to <tracking_url> and extract the current tracking status, delivery date, and location',
        llm=llm, browser=browser
    )
    result = await agent.run(max_steps=10)
    print('TRACKING:', result)
asyncio.run(main())
"
```

这种方式可以确保在所有运输公司都能可靠地追踪包裹，即使是一些具有严格机器人检测机制的运输公司也是如此。

**需要使用浏览器的情况：**
- UPS、FedEx、Amazon（其追踪页面依赖大量 JavaScript）
- USPS（当基本解析方法失败时，例如状态更新较为复杂的情况下）
- 任何需要用户交互或填写表单的运输公司

## 工作流程

1. 用户提供追踪号码 → 运行 `--detect` 命令来识别运输公司
2. 将包裹信息及其订单详情添加到 `memory/shipments.md` 文件中
3. 可以在早晨例会或需要时运行脚本来检查所有包裹的状态
4. 对于需要使用浏览器查看状态的包裹，使用相应的浏览器命令和追踪链接
5. 一旦包裹送达，将其从货物文件中删除

## 系统要求

- Python 3.10 或更高版本
- 需要能够通过 HTTPS 访问运输公司的追踪页面（例如 `tools.usps.com`）——仅限读取数据，无需身份验证
- 该工具不进行文件写入、子进程调用或 shell 命令执行

## 必需条件

- Python 3.10 或更高版本
- 具备通过 HTTPS 访问运输公司追踪页面的功能
- （可选）对于依赖 JavaScript 的网站，需要具备使用浏览器来查看包裹状态的功能