---
name: wolt-cli
description: 使用 Nikita 提供的本地 Wolt CLI，您可以通过终端浏览餐厅信息、查看菜单/菜品/选项，并执行与 wolt.com 相关的操作（如查看用户资料、购物车内容以及进行结账预览）。该工具适用于在需要查找餐厅、查看餐厅目录、解析菜品/选项 ID、自动化购物车或用户资料管理任务，或调试 Wolt 的认证/位置/输出功能时使用。
---
# Wolt CLI

工具仓库：https://github.com/mekedron/wolt-cli

请访问该仓库以获取安装和构建的详细信息，然后使用本地的 `wolt` 可执行文件：

```bash
wolt <group> <command> [flags]
```

## 会话启动

1. 每个会话期间检查一次命令树结构：
```bash
wolt --help
```
2. 在代理操作中优先使用机器生成的输出结果：
```bash
... --format json
```
3. 解析来自请求包（envelope）的 `.data` 数据，并将 `.warnings` 和 `.error` 错误信息显示给用户。

## 安全规则

- 默认情况下以只读模式启动程序。
- 在执行以下命令之前需要用户明确确认：
  - `cart add`（添加商品到购物车）
  - `cart remove`（从购物车中移除商品）
  - `cart clear`（清空购物车）
  - `profile favorites add`（将地点添加到收藏夹）
  - `profile favorites remove`（从收藏夹中移除地点）
  - `profile addresses add`（添加地址）
  - `profile addresses update`（更新地址）
  - `profile addresses remove`（删除地址）
  - `profile addresses use`（使用地址）
  - `configure`（配置本地账户信息）
- 请注意：`checkout preview` 功能仅用于预览订单信息，Wolt CLI 并不会实际提交订单。

## 认证流程

使用明确的账户名称以避免混淆：

```bash
wolt configure --profile-name default --wtoken "<token>" --wrtoken "<refresh-token>" --overwrite
wolt profile status --profile default --format json --verbose
```

对于需要认证的命令，可以使用以下方式进行身份验证：
1. 显式指定认证参数（`--wtoken`、`--wrtoken`、`--cookie`）
2. 选择特定的账户认证字段
3. 使用默认的账户认证字段

当可用的新凭证出现时，过期的或 401 错误的访问令牌会自动更新，并重新保存到本地配置文件中。

## 地点相关规则

请严格遵循以下规则：
- 可以使用 `--address "<text>"` 来指定地点，或者同时使用 `--lat` 和 `--lon`。
- 不允许同时使用 `--address` 和 `--lat/--lon`。
- 如果没有指定其他地点信息，系统会使用用户的默认位置信息。
- 对于 `search venues/items` 和 `venue show/hours` 等操作，系统会使用 `--address` 或用户的默认位置信息（不支持直接使用 `--lat/--lon` 参数）。
- `discover`、`cart`、`checkout preview` 和 `profile favorites` 等功能都支持 `--lat/--lon` 参数。

## 命令分类

- 查找附近的选项：`discover feed`、`discover categories`、`search venues`、`search items`
- 详细查看某个场所的信息：`venue show`、`venue categories`、`venue search`、`venue menu`、`venue hours`
- 查看商品详情或修改购物车中的选项：`item show`、`item options`
- 管理购物车和价格信息：`cart count/show/add/remove/clear`，然后执行 `checkout preview`
- 查看账户信息及交易记录：`profile show/status/orders/payments/addresses/favorites`

对于大型市场场所，建议使用以下命令格式：
- `venue search <slug> --query "<text>"`（搜索特定场所）
- `venue menu <slug> --category <category-slug>`（查找特定类别的菜单）

## 输出与诊断信息

- 使用 `--format json|yaml` 可以以 JSON 或 YAML 格式输出请求包中的关键信息：`meta`、`data`、`warnings`（错误信息，可选）。
- 如果在请求过程中出现错误，可以使用 `--verbose` 参数重新运行程序以获取详细的错误日志和调试信息。

## 参考资料

- 完整的命令及参数说明：`references/command-reference.md`
- 可复用的工作流程示例：`references/workflows.md`
- 关于请求包解析和错误处理的说明：`references/output-and-errors.md`