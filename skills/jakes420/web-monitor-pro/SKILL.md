---
name: web-monitor
version: 3.5.0
description: "监控网页上的变化、价格下降、库存情况以及自定义条件。当用户请求监视某个网址、接收价格变化的通知、检查商品是否重新上架，或跟踪网站的更新时，可以使用该功能。此外，该工具还支持对现有监控项进行添加、删除、检查及报告操作。版本3新增了变化摘要、可视化差异对比、价格比较、模板支持、JavaScript渲染功能以及Webhook集成。"
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "bins": ["python3", "curl"] },
      },
  }
---
# Web Monitor Pro

您可以监控任何网页，并实时了解其内容是否发生变化。

## 快速入门

```bash
python3 scripts/monitor.py quickstart                        # shows suggestions + engine status
python3 scripts/monitor.py watch "https://example.com/product"
python3 scripts/monitor.py check
```

### 首次运行

首次运行时，请使用 `quickstart` 命令。它会完成以下操作：
1. 创建数据目录。
2. 检查可用的数据获取引擎（`curl`、`cloudscraper`、`playwright`）。
3. 提供常见的监控场景建议（如价格下降、商品补货、页面更新、促销活动）。
4. 列出可用的模板。
5. 对于缺失的引擎，提供相应的提示。

该工具会根据这些信息询问用户需要监控的内容，并帮助用户进行设置。

## 功能介绍

- 监控网页内容的变化、价格下降以及商品补货情况。
- 智能化的变化摘要（例如：“价格从 $389 下降到 $331，节省了 15%”）。
- 提供直观的并排对比视图，显示具体发生了哪些变化。
- 支持价格历史数据的跟踪和趋势分析。
- 支持多店铺间的价格比较。
- 提供针对常见监控场景的预设模板（如价格下降、商品补货、促销活动）。
- 对于使用 JavaScript 动态渲染的网站，支持通过 `Playwright` 进行内容抓取。
- 支持将监控结果发送到 Slack、Discord 或其他自定义端点。
- 支持分组管理、添加备注、生成快照以及导出数据。
- 无需使用 API 密钥；数据存储在 `~/.web-monitor/` 目录中，默认使用 `curl` 作为数据获取引擎。

## 智能监控

最简单的使用方式是直接指向目标网页地址，工具会自动完成其余设置。

```bash
python3 scripts/monitor.py watch "https://example.com/product"
```

该工具能够自动识别目标页面类型（产品页面、库存页面或普通页面），并据此设置相应的监控策略。无需额外配置。

如需更多控制选项，可进一步调整参数：

```bash
python3 scripts/monitor.py watch "https://example.com" --group wishlist
python3 scripts/monitor.py watch "https://example.com" --browser --webhook "https://hooks.slack.com/..."
```

## 添加监控任务

如需更精细的控制，可以使用 `add` 命令添加新的监控任务：

```bash
python3 scripts/monitor.py add "https://example.com/product" \
  --label "Cool Gadget" \
  --condition "price below 500" \
  --interval 360 \
  --group "wishlist" \
  --priority high \
  --target 3000 \
  --browser \
  --webhook "https://hooks.slack.com/..."
```

**通用参数**（适用于 `add` 和 `watch` 命令）：
- `--label/-l`：监控任务的名称。
- `--selector/-s`：用于指定要监控的 CSS 选择器（例如 `#price`、`.stock-status`）。
- `--condition/-c`：设置触发警报的条件（详见下方条件语法说明）。
- `--interval/-i`：检查间隔时间（单位：分钟，默认为 360 分钟）。
- `--group/-g`：监控任务的所属组别（例如 “wishlist”、”work”）。
- `--priority/-p`：监控任务的优先级（高、中、低，默认为中等）。
- `--target/-t`：目标价格范围。
- `--browser/-b`：对于使用 JavaScript 动态渲染的网站，指定使用 `Playwright` 进行内容抓取。
- `--webhook/-w`：指定 Webhook 的 URL，可重复应用于多个端点。

## 检查监控任务状态

```bash
python3 scripts/monitor.py check                # check all
python3 scripts/monitor.py check --id 3          # check one
python3 scripts/monitor.py check --verbose       # include content preview
```

系统会返回监控任务的当前状态（是否发生变化）、条件信息、价格数据以及易于阅读的变化摘要。例如：
- “价格从 $389 下降到 $331，节省了 15%；这是 30 天以来的最低价格。”
- “商品已补货！之前缺货了 3 天。”
- “新增内容：‘突发新闻：AI 模型取得……’”

当检测到变化时，系统会自动生成 HTML 对比文件，该文件的路径会显示在 `diff_path` 字段中。

## 仪表盘

所有监控信息一目了然：

```bash
python3 scripts/monitor.py dashboard
python3 scripts/monitor.py dashboard --whatsapp
```

仪表盘会显示监控任务的状态图标、最后一次检查时间、监控时长、当前价格、目标价格达成情况以及浏览器/Webhook 配置信息。支持按组别对监控任务进行分类显示。

## 价格趋势

```bash
python3 scripts/monitor.py trend 3
python3 scripts/monitor.py trend 3 --days 30
```

显示价格的变化趋势（上涨/下降/稳定），以及最低价、最高价、平均价等数据，并提供价格趋势图。

## 多店铺价格比较

```bash
python3 scripts/monitor.py compare mygroup
python3 scripts/monitor.py compare --all
```

支持在同一组内比较多个店铺的价格，显示最便宜和最贵的商品，以及价格相对于平均价的优惠幅度。

## 添加竞争商品到现有监控任务

```bash
python3 scripts/monitor.py add-competitor 3 "https://competitor.com/same-product"
```

可以在同一组内为现有监控任务添加新的竞争商品，无需重新配置。

## 模板

提供针对常见监控场景的预设模板，可节省手动配置的时间：

```bash
python3 scripts/monitor.py template list
python3 scripts/monitor.py template use price-drop "https://example.com/product"
python3 scripts/monitor.py template use restock "https://example.com/product"
python3 scripts/monitor.py template use sale "https://example.com/deals"
```

可用模板包括：
- `price-drop`：监控价格下降情况，并将当前价格作为基准。
- `restock`：监控商品是否补货，显示 “有货”、“可购买” 等状态。
- `content-update`：监控页面内容变化，并提供智能对比功能。
- `sale`：监控促销活动，显示 “促销中” 或 “折扣” 等信息。
- `new-release`：监控新商品或新版本的发布。

这些模板已预先配置好了相关条件、检查间隔和优先级。

## 监控任务管理

```bash
python3 scripts/monitor.py list                    # all monitors
python3 scripts/monitor.py list --group wishlist   # filter by group
python3 scripts/monitor.py pause 3                 # skip during checks
python3 scripts/monitor.py resume 3                # re-enable
python3 scripts/monitor.py remove 3                # delete
```

## 添加备注和快照

您可以为任何监控任务添加备注或手动生成快照：

```bash
python3 scripts/monitor.py note 3 "waiting for Black Friday"
python3 scripts/monitor.py notes 3
```

**手动生成快照**：
```bash
python3 scripts/monitor.py snapshot 3
python3 scripts/monitor.py snapshot 3 --note "price before sale"
```

**查看历史记录**：
```bash
python3 scripts/monitor.py history 3
python3 scripts/monitor.py history 3 --limit 10
```

## 可视化对比

提供并排的 HTML 对比视图：左侧显示旧内容，右侧显示新内容。绿色表示新增内容，红色表示删除的内容，黄色表示修改的内容。

```bash
python3 scripts/monitor.py diff 3
python3 scripts/monitor.py screenshot 3
```

`diff` 命令会生成对比文件并在浏览器中打开；`snapshot` 命令会保存当前页面内容以供后续对比使用。

## 报告

提供每周汇总报告，格式适合通过 WhatsApp 发送：

```bash
python3 scripts/monitor.py report
```

## 组别管理

```bash
python3 scripts/monitor.py groups
```

列出所有监控任务所属的组别及其数量。

## 数据获取引擎与 Cloudflare 支持

该工具使用多种数据获取引擎来抓取网页内容。默认情况下（使用 `--engine auto`），系统会依次尝试不同的引擎，直到找到有效的引擎：
- **curl**：速度较快，无依赖性，适用于大多数网站。
- **cloudscraper**：能够处理 Cloudflare 的 JavaScript 限制，无需完整浏览器。
- **playwright**：适用于依赖大量 JavaScript 的单页应用程序（SPA）。

您可以查看系统中可用的引擎：

```bash
python3 scripts/monitor.py engines
```

**强制使用特定引擎**：
```bash
python3 scripts/monitor.py watch "https://example.com" --engine cloudscraper
python3 scripts/monitor.py add "https://example.com" --engine browser
```

建议在处理受 Cloudflare 保护的电子商务网站时安装 `cloudscraper`：

```bash
pip3 install cloudscraper
```

每个监控任务的引擎设置是可自定义的，您可以为不同的任务选择不同的引擎。

## JavaScript 动态渲染处理

像 Amazon、Best Buy 等网站通常使用 JavaScript 动态渲染内容。默认的 `curl` 方法可能无法获取到这些内容。如果您需要使用 `Playwright`，请添加 `--browser` 参数：

```bash
python3 scripts/monitor.py watch "https://amazon.com/dp/B0EXAMPLE" --browser
```

如果未安装 `Playwright`，系统会自动回退到使用 `curl`，并会提示您进行安装。

## Webhook 功能

当满足预设条件或内容发生变化时，系统会触发 JSON POST 请求：

```bash
python3 scripts/monitor.py add "https://example.com" --webhook "https://hooks.slack.com/services/..."
```

您可以使用 `--webhook` 参数为多个端点配置 Webhook。请求数据包含 `monitor_id`、`label`、`url`、事件详情（如 `status`、`condition_met`、`change_summary`、`current_price` 和 `timestamp`）。

系统会在每次检查时通过 Webhook 发送这些数据。

## 数据导出与导入

```bash
python3 scripts/monitor.py export > monitors.json
python3 scripts/monitor.py import monitors.json
```

导入数据时，系统会自动删除重复的记录。

## GUI 控制台

```bash
python3 scripts/monitor.py gui
```

在浏览器中打开 `~/.web-monitor/console.html` 文件。这是一个独立的 HTML 文件，可显示所有监控任务、价格趋势、警报记录、组别信息等。支持切换深色/浅色主题，支持过滤和排序功能，还提供价格趋势图。无需任何外部依赖。

您可以使用 `--no-open` 参数来避免打开控制台。

## 条件语法

- `price below 500` 或 `price < 500`：当价格低于指定阈值时触发警报。
- `price above 1000` 或 `price > 1000`：当价格高于指定阈值时触发警报。
- `contains 'in stock'`：当页面中显示 “有货” 等文字时触发警报。
- `not contains 'out of stock'`：当页面中不再显示 “缺货” 等文字时触发警报。

## 优先级设置

- **high**：立即触发警报。
- **medium**：默认优先级。
- **low**：数据会批量汇总处理。

## 使用 Cron 任务自动化监控

您可以设置定时任务来定期检查监控任务：

```
Task: Check all web monitors. Run: python3 <skill_dir>/scripts/monitor.py check
Report any monitors where status is "changed" or "condition_met" is true.
If nothing changed, stay silent.
```

推荐的时间间隔为每 6 小时（`0 */6 * * *`）。每周报告可在周一运行 `report` 命令生成。

## 用户反馈

```bash
python3 scripts/monitor.py feedback "your message"
python3 scripts/monitor.py feedback --bug "something broke"
python3 scripts/monitor.py feedback --idea "wouldn't it be cool if..."
python3 scripts/monitor.py debug
```

**使用建议**：
- 通常情况下，直接使用 `watch` 命令即可满足基本监控需求。只有在需要特定条件时才使用 `add` 命令。
- 使用 `--selector` 可减少不必要的信息干扰。如果您只关注价格变化，只需指定 `#price` 作为监控目标即可。
- 将相关监控任务分组，然后使用 `compare` 功能来查找不同店铺间的最佳价格。
- 每个监控任务最多保存 50 张快照，每张快照的大小限制为 10KB。
- 价格目标会在仪表盘和检查结果中显示进度信息。
- 在促销活动前使用 `snapshot --note` 命令生成基准数据，便于后续对比。
- 对于依赖大量 JavaScript 的网站，`--browser` 参数是必需的。

## 其他功能

- `watch` 命令通常是最佳的选择；只有在需要特定条件时才使用 `add` 命令。
- 使用 `--selector` 可减少不必要的信息显示。如果只需关注价格变化，只需指定 `#price` 作为监控目标。
- 将相关监控任务分组后，可以使用 `compare` 功能比较不同店铺的价格。
- 系统会保留最多 50 张快照，每张快照的大小限制为 10KB。
- 价格目标会在仪表盘和检查结果中显示。
- 在促销活动前使用 `snapshot --note` 命令生成基准数据，便于后续对比。
- 对于依赖 JavaScript 动态渲染的网站，`--browser` 参数是必需的。