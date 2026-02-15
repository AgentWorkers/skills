---
name: gurkerlcli
version: 0.1.6
description: 在奥地利，用户可以通过 gurkerl.at 进行在线食品杂货购物。当用户询问“食品杂货”、“购物”、“订购食品”、“Gurkerl”或想要在奥地利在线搜索/订购食品时，可以使用该平台。
tools: [bash]
---

# 🥒 gurkerlcli - 奥地利在线杂货购物工具

这是一个用于 [gurkerl.at](https://gurkerl.at) 在线杂货购物的命令行接口（仅支持奥地利地区）。

## 安装

```bash
# Via Homebrew
brew tap pasogott/tap
brew install gurkerlcli

# Or via pipx
pipx install gurkerlcli
```

## 认证

**使用前需要登录：**

```bash
gurkerlcli auth login --email user@example.com --password xxx
gurkerlcli auth whoami     # Check login status
gurkerlcli auth logout     # Clear session
```

会话信息会安全地存储在 macOS 的 Keychain 中。

**另一种方式：使用环境变量**

```bash
export GURKERL_EMAIL=your-email@example.com
export GURKERL_PASSWORD=your-password
```

或者将相关设置添加到 `~/.env.local` 文件中以实现持久化。

## 命令

### 🔍 搜索商品

```bash
gurkerlcli search "bio milch"
gurkerlcli search "äpfel" --limit 10
gurkerlcli search "brot" --json          # JSON output for scripting
```

### 🛒 购物车

```bash
gurkerlcli cart list                     # View cart contents
gurkerlcli cart add <product_id>         # Add product
gurkerlcli cart add <product_id> -q 3    # Add with quantity
gurkerlcli cart remove <product_id>      # Remove product
gurkerlcli cart clear                    # Empty cart (asks for confirmation)
gurkerlcli cart clear --force            # Empty cart without confirmation
```

### 📝 购物清单

```bash
gurkerlcli lists list                    # Show all lists
gurkerlcli lists show <list_id>          # Show list details
gurkerlcli lists create "Wocheneinkauf"  # Create new list
gurkerlcli lists delete <list_id>        # Delete list
```

### 📦 订购历史

```bash
gurkerlcli orders list                   # View past orders
```

## 示例使用流程

### 查看购物车中的商品

```bash
gurkerlcli cart list
```

**输出结果：**

```
🛒 Shopping Cart
┌─────────────────────────────────┬──────────────┬───────────────┬──────────┐
│ Product                         │          Qty │         Price │ Subtotal │
├─────────────────────────────────┼──────────────┼───────────────┼──────────┤
│ 🥛 nöm BIO-Vollmilch 3,5%       │     2x 1.0 l │ €1.89 → €1.70 │    €3.40 │
│ 🧀 Bergbaron                    │     1x 150 g │         €3.99 │    €3.99 │
├─────────────────────────────────┼──────────────┼───────────────┼──────────┤
│                                 │              │        Total: │    €7.39 │
└─────────────────────────────────┴──────────────┴───────────────┴──────────┘

⚠️  Minimum order: €39.00 (€31.61 remaining)
```

### 搜索商品并添加到购物车

```bash
# Find product
gurkerlcli search "hafermilch"

# Add to cart (use product ID from search results)
gurkerlcli cart add 123456 -q 2
```

### 从购物车中删除商品

```bash
# List cart to see product IDs
gurkerlcli cart list --json | jq '.items[].product_id'

# Remove specific product
gurkerlcli cart remove 123456
```

## 调试

使用 `--debug` 标志可查看详细的输出信息：

```bash
gurkerlcli cart add 12345 --debug
gurkerlcli cart remove 12345 --debug
```

## 提示

- **最低订单金额：** 39.00 欧元（含运费）
- **配送时间：** 请查看 gurkerl.at 网站上的可用配送时间
- **促销商品：** 价格带有箭头（例如：€1.89 → €1.70）表示正在打折
- **JSON 输出：** 使用 `--json` 标志可获取数据用于脚本编写或自动化操作

## 限制

- ⏳ 目前尚未实现结账功能（请通过网站完成）
- 仅支持奥地利地区（维也纳、格拉茨、林茨周边地区）
- 🔐 需要拥有有效的 gurkerl.at 账户

## 更新日志

- **v0.1.6**：修复了从购物车中删除商品的逻辑（使用 DELETE 请求而非 POST 请求）
- **v0.1.5**：修复了为已存在商品添加到购物车的逻辑（使用 POST 请求而非 PUT 请求）

## 链接

- [gurkerl.at](https://gurkerl.at)
- [GitHub 仓库](https://github.com/pasogott/gurkerlcli)