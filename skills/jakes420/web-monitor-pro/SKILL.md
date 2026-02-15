---
name: web-monitor
version: 3.4.2
description: "监控网页上的变化、价格下降、库存情况以及自定义条件。当用户请求监控某个网址、接收价格变动的通知、检查商品是否重新上架，或跟踪任何网站的更新时，可以使用该功能。此外，该工具还支持对现有监控项进行添加、删除、检查和报告操作。版本3新增了变化摘要、可视化差异对比、价格比较、模板支持、JavaScript渲染功能以及Webhook集成。"
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
python3 scripts/monitor.py setup
python3 scripts/monitor.py watch "https://example.com/product"
python3 scripts/monitor.py check
```

## 功能介绍

- 监控网页内容的变化、价格下降以及商品是否重新上架
- 智能化的变化摘要（例如：“价格从389美元降至331美元，优惠15%”）
- 可视化的并排对比功能，清晰显示具体变化内容
- 跟踪价格历史数据及趋势
- 支持多店铺间的价格比较
- 提供针对常见场景的预设模板（如价格下降、商品重新上架、促销等）
- 支持通过Playwright库对动态网页进行JavaScript渲染
- 支持将监控结果发送到Slack、Discord或任意自定义端点
- 支持分组管理、添加备注、生成快照以及导出数据
- 无需API密钥，数据存储在`~/.web-monitor/`目录中，默认使用`curl`工具进行数据获取

## 简单使用方式

这是最简单的使用方法：只需将程序指向目标网址，其余工作都会自动完成。

```bash
python3 scripts/monitor.py watch "https://example.com/product"
```

该工具能够自动识别目标网页的类型（产品页面、库存页面或普通页面），并据此设置相应的监控规则。无需额外配置。

如需更精细的控制，可添加相关选项：

```bash
python3 scripts/monitor.py watch "https://example.com" --group wishlist
python3 scripts/monitor.py watch "https://example.com" --browser --webhook "https://hooks.slack.com/..."
```

## 添加监控任务

如需更全面的监控功能，可以使用`add`命令：

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

**通用选项**（适用于`add`和`watch`命令）：

- `--label/-l`：监控任务的名称
- `--selector/-s`：需要关注的CSS选择器（例如`#price`、`.stock-status`）
- `--condition/-c`：触发警报的条件（详见下方条件语法）
- `--interval/-i`：检查间隔时间（默认为360分钟）
- `--group/-g`：监控任务的分类（如“愿望清单”、“工作”等）
- `--priority/-p`：警报优先级（高/中/低，默认为中等）
- `--target/-t`：目标价格
- `--browser/-b`：对于需要JavaScript渲染的网页，使用Playwright进行渲染
- `--webhook/-w`：设置Webhook发送地址，可重复应用于多个端点

## 检查监控状态

程序会返回监控状态（是否发生变化）、条件信息、价格数据以及易于阅读的变化摘要。例如：

- “价格从389美元降至331美元，优惠15%。这是30天内的最低价格。”
- “商品已重新上架！之前缺货了3天。”
- “新增内容：‘突发新闻：AI模型取得……’”

当检测到变化时，系统会自动生成HTML对比文件，该文件的路径会显示在`diff_path`字段中。

## 仪表盘

所有监控信息一目了然：

```bash
python3 scripts/monitor.py dashboard
python3 scripts/monitor.py dashboard --whatsapp
```

仪表盘会显示状态图标、最后一次检查时间、监控时长、当前价格、目标价格达成情况以及浏览器/Webhook配置。支持按类别对监控任务进行分组显示。

## 价格趋势

```bash
python3 scripts/monitor.py trend 3
python3 scripts/monitor.py trend 3 --days 30
```

可查看价格的变化趋势（上涨/下跌/稳定），以及价格的最小值/最大值/平均值，并附带日期信息。

## 多店铺价格比较

```bash
python3 scripts/monitor.py compare mygroup
python3 scripts/monitor.py compare --all
```

可比较同一类别内各店铺的价格，显示最便宜和最贵的商品，以及价格相对于平均价的折扣百分比。

**为现有监控任务添加竞争对手信息**：

```bash
python3 scripts/monitor.py add-competitor 3 "https://competitor.com/same-product"
```

可以在同一类别中为该任务添加一个新的竞争对手信息。

## 预设模板

提供了针对常见场景的预设模板，可节省配置时间：

```bash
python3 scripts/monitor.py template list
python3 scripts/monitor.py template use price-drop "https://example.com/product"
python3 scripts/monitor.py template use restock "https://example.com/product"
python3 scripts/monitor.py template use sale "https://example.com/deals"
```

可用模板包括：
- `price-drop`：监控价格下降情况，以当前价格作为基准
- `restock`：监控商品是否重新上架
- `content-update`：监控页面内容变化，并提供智能对比结果
- `sale`：监控促销信息
- `new-release`：监控新商品或新版本的发布

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

**生成快照**：

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

提供并排的HTML对比视图：左侧显示旧内容，右侧显示新内容。绿色表示新增内容，红色表示删除内容，黄色表示修改内容。

```bash
python3 scripts/monitor.py diff 3
python3 scripts/monitor.py screenshot 3
```

`diff`命令用于生成对比结果，并在浏览器中打开；`screenshot`命令用于保存当前页面内容以供后续对比使用。

## 报告生成

每周生成一次报告，格式适合通过WhatsApp发送：

```bash
python3 scripts/monitor.py report
```

## 分组管理

```bash
python3 scripts/monitor.py groups
```

列出所有监控任务所属的组别及其数量。

## 支持的引擎与Cloudflare

该工具使用多种引擎来获取网页内容。默认情况下（`--engine auto`），系统会依次尝试以下引擎，直到找到有效的引擎：
1. **curl**：快速且无依赖，适用于大多数网站
2. **cloudscraper**：能够处理Cloudflare设置的JavaScript限制
3. **playwright**：适用于依赖JavaScript的单页应用（SPA）

您可以查看系统中可用的引擎：

```bash
python3 scripts/monitor.py engines
```

**强制使用特定引擎**：

```bash
python3 scripts/monitor.py watch "https://example.com" --engine cloudscraper
python3 scripts/monitor.py add "https://example.com" --engine browser
```

**推荐安装cloudscraper**（适用于受Cloudflare保护的电子商务网站）：

```bash
pip3 install cloudscraper
```

每个监控任务的引擎设置是可自定义的，您可以为不同任务选择不同的引擎。

## JavaScript渲染

部分网站（如Amazon、Best Buy及大多数单页应用）使用JavaScript加载内容。默认的`curl`方法可能无法获取这些内容。如需使用Playwright进行渲染，请添加`--browser`参数：

```bash
python3 scripts/monitor.py watch "https://amazon.com/dp/B0EXAMPLE" --browser
```

如果未安装Playwright，系统会自动切换回`curl`方法，并会发出提示。您可以通过以下命令进行安装：

```bash
pip3 install playwright && python3 -m playwright install chromium
```

## Webhook通知

当满足条件或内容发生变化时，系统会发送JSON格式的POST请求：

```bash
python3 scripts/monitor.py add "https://example.com" --webhook "https://hooks.slack.com/services/..."
```

您可以使用`--webhook`参数为多个端点设置Webhook通知。通知内容包含`monitor_id`、`label`、`url`、事件详情（状态、条件是否满足、变化摘要、当前价格）以及时间戳。

在检查过程中，系统会自动触发Webhook通知。

## 数据导出与导入

**导入**时，系统会通过URL过滤重复数据。

## GUI控制台

```bash
python3 scripts/monitor.py gui
```

在浏览器中打开`~/.web-monitor/console.html`文件。这是一个独立的HTML页面，可查看所有监控任务、价格趋势、警报记录、分组信息以及模板设置。支持切换深色/浅色模式，支持过滤和排序功能，同时提供图表显示。无需额外依赖。

**注意**：使用`--no-open`参数可避免打开控制台窗口。

## 条件语法

- `price below 500` 或 `price < 500`：当价格低于设定阈值时触发警报
- `price above 1000` 或 `price > 1000`：当价格高于设定阈值时触发警报
- `contains 'in stock'`：当页面中出现“有库存”字样时触发警报
- `not contains 'out of stock'`：当页面中的“缺货”字样消失时触发警报

## 警报优先级

- **高**：立即触发警报
- **中**：默认优先级
- **低**：警报信息会被批量处理

## 使用Cron任务自动化监控

您可以设置定时任务来定期检查监控任务：

```
Task: Check all web monitors. Run: python3 <skill_dir>/scripts/monitor.py check
Report any monitors where status is "changed" or "condition_met" is true.
If nothing changed, stay silent.
```

推荐的时间间隔为每6小时（`0 */6 * * *`）。每周报告可在周一执行`report`命令生成。

## 用户反馈

```bash
python3 scripts/monitor.py feedback "your message"
python3 scripts/monitor.py feedback --bug "something broke"
python3 scripts/monitor.py feedback --idea "wouldn't it be cool if..."
python3 scripts/monitor.py debug
```

## 使用技巧

- 通常情况下，直接使用`watch`命令即可满足基本需求。只有在需要特定条件时才使用`add`命令。
- 使用`--selector`可以减少不必要的警报。如果您只关注价格变化，只需指定`#price`选择器即可。
- 将相关监控任务分组，然后使用`compare`功能来查找各店铺间的最佳优惠信息。
- 每个监控任务最多保存50个快照，每个快照的大小限制为10KB。
- 价格目标会在仪表盘和检查结果中显示达成情况。
- 在促销活动前使用`snapshot --note`命令生成基准数据，以便后续对比。
- 对于依赖JavaScript的网站，`--browser`选项是必需的。
- 结合Slack或Discord使用Webhook功能，实现实时警报，无需频繁轮询网站。