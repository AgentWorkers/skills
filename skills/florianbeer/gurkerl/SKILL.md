---
name: gurkerl
description: Gurkerl.at 提供通过 MCP（Grocery Shopping Platform）进行杂货购物的功能，用户可以搜索产品、管理购物车、查看订单、保存食谱以及将商品添加到收藏夹中。
homepage: https://www.gurkerl.at/seite/mcp-server
metadata:
  clawdbot:
    emoji: "🥒"
    requires:
      bins: ["curl", "jq"]
    env:
      - GURKERL_EMAIL
      - GURKERL_PASS
    tags:
      - grocery
      - shopping
      - austria
      - mcp
      - rohlik
      - delivery
---

# Gurkerl.at MCP 技能

这是一款奥地利的食品配送服务（隶属于 Rohlik 集团）。用户可以搜索产品、管理购物车、查看订单、浏览食谱等。

> **注意：** 该功能需要使用 Gurkerl 的官方 MCP 服务器。其他 Rohlik 集团的品牌（如 Rohlik.cz、Knuspr.de、Kifli.hu）也可以使用相同的方法，只需在脚本中更改 MCP 的 URL 即可。

## 设置

配置环境变量：
```bash
export GURKERL_EMAIL="your@email.com"
export GURKERL_PASS="your-password"
```

为了实现持久化访问，将以下配置添加到 `~/.config/systemd/user/clawdbot-gateway.service.d/gurkerl.conf` 文件中：
```ini
[Service]
Environment="GURKERL_EMAIL=your@email.com"
Environment="GURKERL_PASS=your-password"
```

## 命令行接口（CLI）使用方法

```bash
# Search products (German keywords)
gurkerl search_products '{"keyword":"Milch"}'
gurkerl search_products '{"keyword":"Bio Eier","sort_type":"orderPriceAsc"}'

# Get cart
gurkerl get_cart

# Add to cart
gurkerl add_items_to_cart '{"items":[{"productId":1234567,"quantity":2}]}'

# View orders
gurkerl fetch_orders '{"limit":3}'
gurkerl fetch_orders '{"order_type":"upcoming"}'

# Search recipes
gurkerl search_recipes_by_vector_similarity '{"query":"vegetarisch schnell"}'
```

## 可用工具

### 产品与搜索
| 工具 | 功能描述 |
|------|-------------|
| `search_products` | 通过关键词或过滤器搜索产品，支持德语关键词。|
| `get_products_details_batch` | 获取多个产品 ID 的详细信息 |
| `get_product_composition` | 获取产品的营养成分、过敏原和配料信息 |
| `get_category_products` | 浏览指定类别的产品 |
| `get_main_categories` | 列出商店的所有类别 |
| `get_brands_navigation` | 列出可用的品牌 |

### 购物车
| 工具 | 功能描述 |
|------|-------------|
| `get_cart` | 查看当前购物车的内容 |
| `add_items_to_cart` | 向购物车中添加产品（格式：`{"items":[{"productId":123,"quantity":1}]`） |
| `update_cart_item` | 修改商品的数量（格式：`{"product_id":123,"quantity":3}`） |
| `remove_cart_item` | 从购物车中删除商品（格式：`{"product_id":123}`） |
| `clear_cart` | 清空整个购物车 |

### 订单
| 工具 | 功能描述 |
|------|-------------|
| `fetch_orders` | 获取订单历史记录。参数：`limit`、`order_type`（已送达/即将送达/全部）、`date_from`、`date_to` |
| `repeat_order` | 重新下单（格式：`{"order_id":12345678}`） |
| `cancel_order` | 取消即将送达的订单（分两步：首先设置 `customer_confirmed`: `false`，然后再设置 `true`） |
| `get_alternative_timeslots` | 查看可用的配送时间 |
| `change_order_timeslot` | 更改配送时间 |

### 食谱
| 工具 | 功能描述 |
|------|-------------|
| `search_recipes_by_vector_similarity` | 基于语义相似性搜索食谱 |
| `get_recipe_detail` | 获取包含产品配料的完整食谱信息 |
| `generate_recipe_with_ingredients_search` | 根据用户提供的配料生成食谱 |
| `get_recipes_navigation` | 浏览食谱类别 |

### 用户与收藏夹
| 工具 | 功能描述 |
|------|-------------|
| `get_user_info` | 查看用户账户信息 |
| `get_user_credits` | 查看可用的积分/优惠券 |
| `get_user_addresses` | 查看保存的配送地址 |
| `get_all_user_favorites` | 查看所有收藏的产品 |
| `get_user_shopping_lists_preview` | 查看所有购物清单 |
| `get_user_shopping_list_detail` | 查看购物清单的内容 |
| `create_shopping_list` | 创建新的购物清单 |
| `add_products_to_shopping_list` | 将产品添加到购物清单中 |

### 客户服务
| 工具 | 功能描述 |
|------|-------------|
| `submit_claim` | 提交关于缺失或损坏商品的保修申请 |
| `get_customer_support_contact_info` | 获取客服联系方式（电话、电子邮件、WhatsApp） |
| `get_user_reusable_bags_info` | 查看可重复使用的购物袋的状态 |
| `adjust_user_reusable_bags` | 更正购物袋的数量 |

### 其他功能
| 工具 | 功能描述 |
|------|-------------|
| `calculate_average_user_order` | 根据历史订单数据生成平均订单信息 |
| `get_faq_content` | 查看常见问题解答（涵盖一般信息、特殊服务、价格相关、婴儿俱乐部、圣诞节等相关内容） |
| `fetch_all_job_listings` | 查看职位信息 |

## 搜索技巧

- 在搜索奥地利 Gurkerl 的产品时，请使用德语关键词，例如：“Milch”（牛奶）、“Brot”（面包）、“Eier”（鸡蛋）、“Käse”（奶酪）。
- 可用的过滤条件：`news`（新商品）、`sales`（促销商品）。
- 排序方式：`orderPriceAsc`（价格升序）、`orderPriceDesc`（价格降序）、`recommended`（默认排序方式）。
- 可选选项：`include_nutritions`（包含营养成分信息）、`include_allergens`（包含过敏原信息）。

## 示例工作流程

### 每周购物计划
```bash
# Check what's on sale
gurkerl search_products '{"filters":[{"filterSlug":"sales","valueSlug":"sales"}]}'

# Add milk to cart
gurkerl search_products '{"keyword":"Milch"}'  # Get product ID
gurkerl add_items_to_cart '{"items":[{"productId":MILK_ID,"quantity":2}]}'

# Review cart
gurkerl get_cart
```

### 重新下单
```bash
gurkerl fetch_orders '{"limit":1}'  # Get order ID
gurkerl repeat_order '{"order_id":ORDER_ID}'
```

### 查找食谱并添加配料
```bash
gurkerl search_recipes_by_vector_similarity '{"query":"schnelles Abendessen"}'
gurkerl get_recipe_detail '{"recipe_id":RECIPE_ID,"include_product_mapping":true}'
# Add matched products to cart
```