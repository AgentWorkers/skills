---
name: food-order
description: 使用 `ordercli` 重新排序 Foodora 的订单并追踪订单的预计到达时间（ETA）或状态。未经用户明确批准，切勿确认任何操作。触发条件包括：下单、重新排序订单以及追踪订单的预计到达时间。
homepage: https://ordercli.sh
metadata: {"clawdbot":{"emoji":"🥡","requires":{"bins":["ordercli"]},"install":[{"id":"go","kind":"go","module":"github.com/steipete/ordercli/cmd/ordercli@latest","bins":["ordercli"],"label":"Install ordercli (go)"}]}}
---

# 通过 `ordercli` 重新订购 Foodora 的餐食

**目标**：安全地重新订购之前的 Foodora 餐食（先查看预览；只有在用户明确表示“确认/下单”后才能完成订单）。

**重要的安全规则**：
- 除非用户明确确认要下单，否则切勿运行 `ordercli foodora reorder ... --confirm` 命令。
- 应优先提供仅查看预览的步骤；展示订单更改后的效果，并请求用户的确认。
- 如果用户不确定如何操作，应停止在预览阶段并询问用户问题。

**设置（只需执行一次）**：
- 国家设置：`ordercli foodora countries` → `ordercli foodora config set --country AT`
- 使用密码登录：`ordercli foodora login --email you@example.com --password-stdin`
- （推荐）无需密码登录：`ordercli foodora session chrome --url https://www.foodora.at/ --profile "Default"`

**查找需要重新订购的订单**：
- 最近的订单列表：`ordercli foodora history --limit 10`
- 订单详情：`ordercli foodora history show <orderCode>`
- （如需机器可读的格式）：`ordercli foodora history show <orderCode> --json`

**预览重新订购的订单（购物车内容不变）**：
`ordercli foodora reorder <orderCode>`

**下单（购物车内容会发生变化；需要用户明确确认）**：
- 先确认订单，然后再执行：`ordercli foodora reorder <orderCode> --confirm`
- 如果需要多个收货地址，请询问用户正确的 `--address-id`（可以从用户的 Foodora 账户或之前的订单信息中获取），然后执行：`ordercli foodora reorder <orderCode> --confirm --address-id <id>`

**跟踪订单状态**：
- 预计到达时间/订单状态：`ordercli foodora orders`
- 实时更新：`ordercli foodora orders --watch`
- 单个订单详情：`ordercli foodora order <orderCode>`

**调试/安全测试**：
- 使用临时配置文件：`ordercli --config /tmp/ordercli.json ...`