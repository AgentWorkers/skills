---
name: apo-cli
description: 通过 `apo-cli` 从 `apohealth.de` 网站搜索和排序药品。该工具支持按药品名称或 PZN（药品唯一编号）进行搜索、查看产品详情、浏览产品分类以及管理购物车。当用户提及 “Apotheke”（药店）、”pharmacy”（药房）、”Medikament”（药品）、”PZN”（药品唯一编号）、”apohealth” 或 “health products”（健康产品）等关键词时，相关功能会被触发。
---

# apohealth.de / apo-cli 技能

使用 `apo-cli` 在 apohealth.de 上搜索药品并管理购物车。`apo-cli` 是一个纯 Python 的命令行工具（CLI），其源代码位于 `{baseDir}/apo_cli.py` 文件中。

## 设置要求

1. 需要 Python 3.9 及更高版本（无需额外依赖）。
2. 无需登录——apohealth.de 支持无需身份验证的访问。

## 重要规则

1. **严禁完成购买**——仅允许构建购物车，用户必须自行完成结账操作。
2. 通过聊天界面进行交互时，务必提供购物车链接：`https://www.apohealth.de/cart/<variant_id>:<qty>,<variant_id>:<qty>,...`。由于代理端无法打开浏览器，因此用户需要一个可点击的链接。
3. 在执行任何可能删除数据的操作（如清空购物车）之前，请务必先确认。
4. 添加商品到购物车时，务必显示商品价格，以便用户随时了解购物情况。
5. 支持通过药品的 PZN（Pharmazentralnummer）进行搜索——用户可以直接提供 PZN 作为搜索条件。

## 命令行工具使用方法

```
python3 {baseDir}/apo_cli.py <resource> <action> [options]
```

## 核心工作流程

### 搜索产品
```bash
python3 {baseDir}/apo_cli.py search "Ibuprofen 400"       # by name
python3 {baseDir}/apo_cli.py search "04114918"             # by PZN
python3 {baseDir}/apo_cli.py search "Nasenspray" -n 20     # more results
```

### 查看产品详情
```bash
python3 {baseDir}/apo_cli.py product <handle>   # prices, variants, description
```

### 浏览商品类别
```bash
python3 {baseDir}/apo_cli.py categories                        # list all
python3 {baseDir}/apo_cli.py list --category bestseller         # browse category
python3 {baseDir}/apo_cli.py list --category schmerzen -n 10    # with limit
```

### 查看购物车
```bash
python3 {baseDir}/apo_cli.py cart                    # show cart
python3 {baseDir}/apo_cli.py cart add <variant_id>   # add product
python3 {baseDir}/apo_cli.py cart remove <variant_id> # remove product
python3 {baseDir}/apo_cli.py cart clear              # clear cart ⚠️
python3 {baseDir}/apo_cli.py cart checkout           # open browser for checkout
```

### 查看购物车状态
```bash
python3 {baseDir}/apo_cli.py status                  # CLI status info
```

## 完整命令参考

有关所有命令、选项和参数的详细信息，请参阅 `{baseDir}/references/commands.md`。