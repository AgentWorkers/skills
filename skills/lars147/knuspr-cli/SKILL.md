---
name: knuspr
description: 通过 `knuspr-cli` 在 Knuspr.de 上管理杂货购物。该工具支持产品搜索、购物车管理、配送时间预约、购物清单查看、订单历史记录查询、优惠信息查看、收藏商品功能以及 meal suggestions（餐点建议）等。当用户提及 “Knuspr”、“杂货”、“Einkauf”、“Lebensmittel”、“Warenkorb”、“Lieferslot” 或 “购物清单” 等相关词汇时，系统会自动触发相应的功能。
---

# Knuspr CLI 技能

使用 `knuspr-cli` 与 Knuspr.de（德国杂货配送服务）进行交互——这是一个纯 Python 编写的 CLI 工具，位于 `{baseDir}/knuspr_cli.py` 文件中。

## 设置要求

1. 需要 Python 3.8 或更高版本（无需额外依赖）。
2. **登录**：执行 `python3 {baseDir}/knuspr_cli.py auth login`（或设置环境变量 `KNUSPR_EMAIL` 和 `KNUSPR_PASSWORD`）。
3. **最低订单金额**：39 欧元。

## 重要规则

1. **切勿完成购买**——仅允许用户创建购物车并预订配送时段。务必提示用户通过 `cart open` 命令或 Knuspr 网站/应用程序自行完成订单确认和支付。
2. **在程序化解析输出时，务必使用 `--json` 选项**。
3. 在执行任何可能破坏数据的状态更改操作（如清空购物车、删除商品列表或释放配送时段）之前，务必先进行确认。
4. 在将商品添加到购物车时，务必显示商品价格和总价，以便用户随时了解订单详情。

## CLI 使用方法

```
python3 {baseDir}/knuspr_cli.py <resource> <action> [options]
```

## 核心工作流程

### 搜索商品并添加到购物车
```bash
# Search products (use --json for parsing)
python3 {baseDir}/knuspr_cli.py product search "Hafermilch" --json
python3 {baseDir}/knuspr_cli.py product search "Käse" --bio --sort price_asc --json
python3 {baseDir}/knuspr_cli.py product search "Joghurt" --rette --json  # discounted items

# Add to cart
python3 {baseDir}/knuspr_cli.py cart add <product_id> -q <quantity>
python3 {baseDir}/knuspr_cli.py cart show --json  # verify cart & total
```

### 预订配送时段
```bash
python3 {baseDir}/knuspr_cli.py slot list --detailed --json  # show available slots with IDs
python3 {baseDir}/knuspr_cli.py slot reserve <slot_id>       # reserve a 15-min ON_TIME slot
python3 {baseDir}/knuspr_cli.py slot reserve <slot_id> --type VIRTUAL  # 1-hour window
python3 {baseDir}/knuspr_cli.py slot current --json          # check current reservation
python3 {baseDir}/knuspr_cli.py slot release                 # cancel reservation (ask first!)
```

### 创建购物清单
```bash
python3 {baseDir}/knuspr_cli.py list show --json             # all lists
python3 {baseDir}/knuspr_cli.py list show <list_id> --json   # products in a list
python3 {baseDir}/knuspr_cli.py list create "Wocheneinkauf"
python3 {baseDir}/knuspr_cli.py list add <list_id> <product_id>
python3 {baseDir}/knuspr_cli.py list to-cart <list_id>       # move entire list to cart
python3 {baseDir}/knuspr_cli.py list duplicate <list_id>     # duplicate a list
```

### 查看订单历史及重新下单
```bash
python3 {baseDir}/knuspr_cli.py order list --json
python3 {baseDir}/knuspr_cli.py order show <order_id> --json
python3 {baseDir}/knuspr_cli.py order repeat <order_id>      # add all items to cart
```

## 完整命令参考

有关所有命令、选项和参数的详细信息，请参阅 `{baseDir}/references/commands.md` 文件。