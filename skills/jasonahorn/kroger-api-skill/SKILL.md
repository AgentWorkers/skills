# Kroger/QFC API 技能

## 概述
该技能用于搜索 Kroger/QFC 的商品、管理购物车、查询取货可用性以及创建取货订单。它使用官方的 Kroger API。QFC 连锁店 ID 为 213。

## 设置
1. 在 [developer.kroger.com](https://developer.kroger.com) 注册并创建应用程序。
2. 添加重定向 URI，例如：http://localhost
3. 授权范围：`product.compact locations.read fulfillment.readwrite orders.pickup.create`
4. 编辑 `state.json` 文件：添加 `client_id`、`client_secret` 和 `chain_id`（值为 “213”）
5. OAuth 流程：
   - 执行命令：`python3 scripts/client.py --state state.json oauth-url`
   - 访问指定 URL 并登录以获取授权码
   - 复制重定向页面中的授权码（例如：http://localhost?code=ABC123）
   - 再次执行命令：`python3 scripts/client.py --state state.json oauth-exchange ABC123`

## 使用方法（通过 exec 命令执行）
在项目工作区的根目录下运行以下命令：

### 搜索商品
```
python3 kroger-api.skill/scripts/client.py search \"milk\" --chain-id 213 --limit 5
```
输出结果为包含商品 `id`（UPC）、`attributes.description`、`attributes.brand` 等信息的 JSON 数据。

### 查找店铺位置
```
python3 kroger-api.skill/scripts/client.py locations 98101 --chain-id 213
```
输出结果为包含店铺位置的详细信息（如 `id`、`attributes.address.addressLine1` 等）。

### 管理本地购物车
```
python3 kroger-api.skill/scripts/client.py cart-add 0001111101001 2  # UPC qty
python3 kroger-api.skill/scripts/client.py cart-get
python3 kroger-api.skill/scripts/client.py cart-clear
```

### 查询商品可用性
```
python3 kroger-api.skill/scripts/client.py availability LOC123 --items '[{&quot;upc&quot;:&quot;UPC&quot;,&quot;quantity&quot;:1}]'
```

### 创建订单
```
python3 kroger-api.skill/scripts/client.py order-create LOC123 \&quot;2026-02-14T10:00:00Z\&quot; --items '[{&quot;upc&quot;:&quot;UPC&quot;,&quot;quantity&quot;:1}]'
```

### 零食清单集成
创建一个名为 `grocery-list.txt` 的文件：
```
milk
bread
eggs
```
```
python3 kroger-api.skill/scripts/client.py grocery --zip 98101
```
在该文件中列出所需商品及其对应的店铺位置。操作流程如下：对于每个商品，先搜索并获取其 UPC（例如选择第一个搜索结果），将其添加到购物车中，然后检查该商品的可用性，最后创建订单。

### 代理工作流程示例
1. 用户：在 Kroger 购物车中添加牛奶和鸡蛋。
2. 搜索“牛奶”，选择 UPC1 并将其添加到购物车。
3. 搜索“鸡蛋”，选择 UPC2 并将其添加到购物车。
4. 用户：查询距离 98101 最近的 QFC 店铺位置。
5. 设置购物车所选店铺的位置信息（`LOC`）。
6. 获取购物车中的商品信息。
7. 检查商品的可用性并选择取货时间。
8. 创建包含取货时间的订单。

## 数据结构（`state.json` 文件）
`state.json` 文件用于存储以下信息：令牌（tokens）、购物车信息（cart）以及店铺位置 ID（location_id）。

## 注意事项：
- 所有 API 接口均基于 Kroger 官方文档设计，请在 [developer.kroger.com/reference](https://developer.kroger.com/reference) 上进行验证。
- 商品的 UPC 可以通过 `product.id` 获取。
- 取货时间采用 ISO 8601 UTC 格式。
- 如遇错误，请检查 API 的返回响应。
- 令牌会自动更新。

该技能的代码文件应打包到名为 `kroger-api.skill/` 的目录中。