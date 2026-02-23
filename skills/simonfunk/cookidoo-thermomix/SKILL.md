---
name: cookidoo
description: 通过非官方的 cookidoo-api 与 Cookidoo（Thermomix 食谱平台）进行交互。可以搜索食谱、管理膳食计划日历、购物清单、收藏夹以及自定义食谱。当用户提到“Cookidoo”、“Thermomix 食谱”、“膳食计划”、“Wochenplan”、“Einkaufsliste Thermomix”、“Cookidoo Rezepte”或希望以编程方式管理他们的 Thermomix/Cookidoo 账户时，可以使用该工具。
---
# Cookidoo 集成

这是一个非官方的 Cookidoo 平台（Vorwerk/Thermomix）集成方案，使用 [cookidoo-api](https://github.com/miaucl/cookidoo-api) Python 库实现。

## 设置

无需外部依赖项，仅使用 Python 标准库（urllib、json）。支持 Python 3.7 及更高版本。

### 环境变量（必需）

```
COOKIDOO_EMAIL=user@example.com
COOKIDOO_PASSWORD=secret
```

### 可选配置

```
COOKIDOO_COUNTRY=ch        # Default: ch (Switzerland)
COOKIDOO_LANGUAGE=de-CH    # Default: de-CH
```

**支持的国家/语言**：可以通过调用库中的 `get_country_options()` 和 `get_language_options()` 函数来获取相关信息。

## 命令行脚本

所有操作均通过 `scripts/cookidoo.py` 脚本完成：

```bash
python scripts/cookidoo.py <command> [args]
```

### 命令

| 命令 | 描述 |
|---|---|
| `login` | 测试登录凭据，显示用户信息 |
| `user-info` | 获取账户信息 |
| `subscription` | 检查当前订阅状态 |
| `recipe <id>` | 获取食谱详情（例如：r59322） |
| `calendar [date]` | 显示当周的饮食计划（默认为今天） |
| `calendar-add <date> <id> [...]` | 将食谱添加到饮食计划中（格式：YYYY-MM-DD） |
| `calendar-remove <date> <id>` | 从饮食计划中删除食谱 |
| `shopping-list` | 显示完整的购物清单（包括食材和其他物品） |
| `shopping-add <id> [...]` | 将食谱食材添加到购物清单中 |
| `shopping-remove <id> [...]` | 从购物清单中删除食谱食材 |
| `shopping-clear` | 清空整个购物清单 |
| `additional-items` | 显示额外的（手动添加的）购物物品 |
| `additional-add <item> [...]` | 将手动添加的物品添加到购物清单中 |
| `additional-remove <id> [...]` | 通过 ID 删除额外的物品 |
| `collections` | 显示自定义和管理中的收藏夹 |
| `collection-add <name>` | 创建自定义收藏夹 |
| `collection-remove <id>` | 删除自定义收藏夹 |

### 食谱 ID

食谱 ID 的格式为 `r59322` 或 `r907015`。您可以在 cookidoo.ch/de 网站上找到这些 ID，或者通过 API 获取它们。

## 认证

该 API 使用 OAuth 密码授权机制（与 Thermomix 应用相同）。令牌会在每个会话期间自动更新。无需 API 密钥，只需提供 Cookidoo 账户凭据即可。

## 限制

- 该集成并非官方提供的 API，而是基于对 Android 应用的逆向工程实现的。
- 食谱搜索功能并未直接在库中提供（需在 cookidoo.ch 网站上浏览食谱并手动提取 ID）。
- 某些功能需要激活 Cookidoo Premium 订阅（如自定义食谱等）。
- 为避免频繁批量请求，请合理使用 API，遵守速率限制。