---
name: bring
description: 管理 Bring! 购物清单：查看、添加或删除共享购物清单中的商品。当用户需要与 Bring! 购物清单应用程序进行交互、添加商品、查看清单内容或在购物后删除商品时，请使用此功能。
---

# 集成购物清单功能

您可以与 Bring! 购物清单进行交互，以管理所需的食品和购物项目。

## 先决条件

必须安装 `bring-shopping` npm 包：

```bash
npm install -g bring-shopping
```

## 初始设置

在首次使用之前，请配置 Bring 的登录凭据：

```bash
./bring configure <email> <password>
```

凭据存储在 `~/.openclaw/bring/config.json` 文件中。

## 常用操作

### 列出所有购物清单

获取所有可用的购物清单及其 UUID：

```bash
./bring lists
```

输出内容包括清单名称、UUID 和主题。

### 按名称查找清单

通过部分名称匹配来查找清单：

```bash
./bring findlist "Home"
./bring findlist "Groceries"
```

返回匹配的清单及其 UUID。

### 查看清单中的项目

显示购物清单中的所有项目：

```bash
./bring items <listUuid>
```

或使用默认清单（如果已设置）：

```bash
./bring items
```

返回待购买的项目以及最近购买的项目。

### 添加项目

将项目添加到购物清单中：

```bash
./bring add <listUuid> "<item-name>" "<optional-note>"
```

示例：
```bash
./bring add abc-123 "Latte" "2 litri"
./bring add abc-123 "Pane"
```

**提示：** 使用与 Bring 应用中已使用的名称相同的项目名称，以确保图标能够正确显示。

### 删除项目

从购物清单中删除项目（项目会被移动到“最近购买的项目”清单中）：

```bash
./bring remove <listUuid> "<item-name>"
```

### 设置默认清单

设置默认清单的 UUID，以避免每次使用时都需要指定：

```bash
./bring setdefault <listUuid>
```

设置默认清单后，您可以使用 `./bring items` 命令而无需指定清单 UUID。

### 管理清单语言

为清单设置语言（供参考）：

```bash
./bring setlang <listUuid> it-IT
./bring setlang <listUuid> es-ES
./bring setlang <listUuid> en-US
```

获取已配置的语言：

```bash
./bring getlang <listUuid>
```

支持的语言：`en-US`、`it-IT`、`es-ES`、`de-DE`、`fr-FR`

## 工作流程示例

### 向指定清单中添加项目

当用户说“将牛奶添加到‘Home’清单中”时：

1. 查找该清单：
   ```bash
   ./bring findlist "Home"
   ```

2. 检查该清单使用的语言/名称：
   ```bash
   ./bring items <listUuid>
   ```

3. 使用适当的名称添加项目（确保名称与清单中的项目名称匹配）：
   ```bash
   ./bring add <listUuid> "Latte"  # If list uses Italian
   # or
   ./bring add <listUuid> "Milk"   # If list uses English
   ```

### 查看所需物品

当用户询问“我的购物清单里有什么？”时：

```bash
./bring items <listUuid>
```

或者如果设置了默认清单：

```bash
./bring items
```

解析并以易读的格式显示清单中的项目。

### 将项目标记为已购买

当用户说“从清单中删除牛奶”时：

```bash
./bring remove <listUuid> "Latte"
```

## 多语言家庭

对于使用多种语言的家庭：

1. **检查每个清单中的现有项目**，以确定使用的语言。
2. **使用一致的命名规则**——确保名称与清单中的名称匹配。
3. **使用 `setlang` 命令设置清单语言（供参考）。
4. **根据上下文判断**——例如，如果清单中有“Latte”、“Pane”、“Uova”，则说明该清单使用的是意大利语。

Bring 应用会在项目名称与其目录中的名称匹配时自动显示图标。为了确保图标能够正确显示，请使用 Bring 应用能够识别的名称。

## 技术细节

- `bring` 包会设置 `NODE_PATH` 环境变量以定位 npm 包。
- 配置信息存储在 `~/.openclaw/bring/config.json` 文件中。
- 会话通过电子邮件/密码进行身份验证。
- 清单可以在家庭成员之间共享。
- 所有设备上的更改会实时同步。

## 注意事项

- 项目名称区分大小写。
- “remove” 命令会将项目移动到“最近购买的项目”清单中（而非永久删除）。
- 多个家庭成员可以共享清单。
- 每个清单可以使用不同的语言规范。
- 为了获得最佳的图标显示效果，请确保项目名称与您的清单中的名称匹配。