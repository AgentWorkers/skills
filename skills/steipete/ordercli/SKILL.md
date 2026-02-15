---
name: ordercli
description: 仅适用于 Foodora 的命令行工具（CLI），用于查询过去的订单和当前订单的状态（Deliveroo 的功能正在开发中）。
homepage: https://ordercli.sh
metadata: {"clawdbot":{"emoji":"🛵","requires":{"bins":["ordercli"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/ordercli","bins":["ordercli"],"label":"Install ordercli (brew)"},{"id":"go","kind":"go","module":"github.com/steipete/ordercli/cmd/ordercli@latest","bins":["ordercli"],"label":"Install ordercli (go)"}]}}
---

# ordercli

使用 `ordercli` 命令可以查看过去的订单信息并追踪当前处于活跃状态的订单（目前仅支持 Foodora）。

**快速入门（Foodora）：**
- `ordercli foodora countries`：显示所有支持的 Foodora 国家。
- `ordercli foodora config set --country AT`：设置当前使用的国家。
- `ordercli foodora login --email you@example.com --password-stdin`：使用指定邮箱和密码登录 Foodora 账户。
- `ordercli foodora orders`：列出所有已下的订单。
- `ordercli foodora history --limit 20`：查看最近 20 条订单记录。
- `ordercli foodora history show <orderCode>`：查看特定订单的详细信息。

**订单相关操作：**
- 查看活跃订单列表（包含订单状态）：`ordercli foodora orders`
- 监控订单状态变化：`ordercli foodora orders --watch`
- 查看特定订单的详细信息：`ordercli foodora order <orderCode>`
- 以 JSON 格式查看订单历史记录：`ordercli foodora history show <orderCode> --json`

**重新下单（将商品添加到购物车）：**
- 预览订单：`ordercli foodora reorder <orderCode>`
- 确认重新下单：`ordercli foodora reorder <orderCode> --confirm`
- 修改订单地址：`ordercli foodora reorder <orderCode> --confirm --address-id <id>`

**Cloudflare / Bot 防护设置：**
- 通过浏览器登录：`ordercli foodora login --email you@example.com --password-stdin --browser`
- 使用预设的浏览器配置文件：`--browser-profile "$HOME/Library/Application Support/ordercli/browser-profile"`
- 导入 Chrome 浏览器的 Cookie：`ordercli foodora cookies chrome --profile "Default"`

**会话导入（无需密码）：**
- `ordercli foodora session chrome --url https://www.foodora.at/ --profile "Default"`：导入 Foodora 会话信息。
- `ordercli foodora session refresh --client-id android`：刷新会话信息（适用于 Android 客户端）。

**Deliveroo（正在开发中，目前尚不可用）：**
- 需要 `DELIVEROO_BEARER_TOKEN`（可选 `DELIVEROO_COOKIE`）。
- `ordercli deliveroo config set --market uk`：设置使用 Deliveroo 服务。
- `ordercli deliveroo history`：查看 Deliveroo 的订单记录。

**注意事项：**
- 请使用 `--config /tmp/ordercli.json` 文件进行测试。
- 在执行任何重新下单或修改订单状态的操作之前，请务必先确认相关信息。