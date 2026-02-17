---
name: bring-list
description: "管理 Bring! 购物清单。可以在共享的购物清单中添加、删除、完成或查看商品。当用户需要管理杂货/购物清单、添加要购买的商品、勾选已购买的商品或查看自己的 Bring! 清单内容时，可以使用该功能。"
---
# Bring! 购物清单

通过非官方的 REST API 管理 Bring! 购物清单。需要使用 `curl` 和 `jq` 工具。

## 代理设置指南

当用户首次请求设置或使用 Bring! 时，请按照以下步骤操作：

### 第一步：检查是否已配置
首先运行 `scripts/bring.sh lists` 命令。如果命令能够正常执行，说明配置已经完成——可以直接进入使用步骤。

### 第二步：请求用户提供凭据
告知用户：
- “我需要您的 Bring! 登录信息（邮箱 + 密码）。如果您还没有账户，可以在 getbring.com 或 Bring! 应用程序中免费创建一个。”
- **如果用户是通过 Google/Apple 账号登录的：** 需要先在 Bring! 应用程序中设置密码（设置 → 账户 → 更改密码）。
- **切勿在聊天中存储凭据。** 应将凭据直接写入配置文件 `~/.config/bring/credentials.json` 中。
- 如果用户不愿意在聊天中分享密码，建议他们手动创建该文件，文件内容格式为 `{"email": "...", "password": "..."}`。

**⚠️ 请勿使用 `scripts/bring.sh setup` 命令**——该命令需要交互式终端（TTY），而代理程序通常没有这样的环境。务必按照第三步的手动方式创建凭据文件。**

### 第三步：保存凭据并测试登录
```bash
mkdir -p ~/.config/bring
cat > ~/.config/bring/credentials.json << 'EOF'
{"email": "USER_EMAIL", "password": "USER_PASSWORD"}
EOF
chmod 600 ~/.config/bring/credentials.json
scripts/bring.sh login
```
如果登录失败，请重新核对邮箱和密码。用户可能需要提供 Bring! 应用程序中的密码（而非 Google/Apple 的单点登录密码）。

### 第四步：显示现有清单并询问默认清单
```bash
scripts/bring.sh lists
```
此步骤会显示用户所有的 Bring! 清单。用户可能有多个清单，例如：
- **Einkaufsliste**（主要购物清单）
- **Drogerie**（药店购物清单）
- **Baumarkt**（五金店购物清单）
- 与伴侣/家人共享的清单

**如果用户没有任何清单：** 建议他们先在 Bring! 应用程序中创建一个清单。API 不支持创建或删除清单，这些操作必须在应用程序中完成。创建清单后，继续进行下一步设置。

**询问用户哪个清单作为默认清单。** 这样用户每次使用时就不需要输入清单名称了。
- 如果用户只有一个清单：自动将其设置为默认清单，并告知用户。
- 如果用户有多个清单：显示所有清单的名称，然后询问使用哪个作为默认清单。解释用户仍然可以通过清单名称来添加或删除物品（例如：“在 **Baumarkt** 清单中添加钉子”）。

### 第五步：设置默认清单
更新配置文件 `~/.config/bring/credentials.json` 以包含选定的默认清单。

### 第六步：确认设置
向用户展示当前清单的内容，确认一切设置正确：
```bash
scripts/bring.sh show
```
告知用户：“设置完成！现在您可以输入类似‘在清单中添加牛奶’或‘购物清单上有什么物品？’这样的指令。”

### 重要提示：清单只能在应用程序中管理
Bring! API 不支持创建或删除清单。如果用户请求创建或删除清单，请告知他们：
“清单只能在 Bring! 应用程序中进行创建或删除。您在应用程序中完成操作后，我就可以立即开始处理新的清单了。”

## 共享清单的处理
Bring! 清单通常会在家庭成员或伴侣之间共享。代理程序所做的任何更改会立即同步到所有共享该清单的设备上。请告知用户：
“我添加的任何物品都会立即显示在所有共享该清单的设备上。”
- 这通常是用户希望看到的功能（例如，伴侣可以看到更新后的购物清单），但这一点需要特别说明。

## 设置方式（手动 / 参考）

凭据可以通过环境变量 `BRING_EMAIL` 和 `BRING_PASSWORD` 或配置文件 `~/.config/bring/credentials.json` 来设置：

```json
{"email": "user@example.com", "password": "secret", "default_list": "Einkaufsliste"}
```

**交互式设置（需要交互式终端 TTY）：** `scripts/bring.sh setup`

## 命令说明

所有命令都支持指定清单名称（部分匹配）或 UUID。如果配置了 `default_list`，则可以省略清单参数。

```bash
# List all shopping lists
scripts/bring.sh lists

# Show items on a list (or default list)
scripts/bring.sh show
scripts/bring.sh show "Einkaufsliste"

# Add item (with optional specification/quantity)
scripts/bring.sh add "Milch" "fettarm, 1L"
scripts/bring.sh add "Einkaufsliste" "Milch" "fettarm, 1L"

# Add multiple items at once (use "item|spec" for specifications)
scripts/bring.sh add-multi "Brot" "Käse|Gouda" "Butter|irische"

# Complete/check off item (moves to recently purchased)
scripts/bring.sh complete "Milch"

# Complete multiple items at once
scripts/bring.sh complete-multi "Milch" "Brot" "Käse"

# Move item back from recently to purchase list
scripts/bring.sh uncomplete "Milch"

# Remove item entirely
scripts/bring.sh remove "Milch"

# Remove multiple items at once
scripts/bring.sh remove-multi "Milch" "Brot" "Käse"
```

## 定位特定清单

当用户有多个清单时，可以通过名称来定位特定的清单：
- “在 **Baumarkt** 清单中添加钉子” → `scripts/bring.sh add "Baumarkt" "Nails"`
- “**Drogerie** 清单上有什么物品？” → `scripts/bring.sh show "Drogerie"`

清单名称支持不区分大小写的匹配，因此 “einkauf” 会匹配 “Einkaufsliste”。

如果没有指定清单，系统会使用配置文件中的 `default_list`。

## JSON 输出

在 `lists` 和 `show` 命令后加上 `--json` 选项，可以获取原始的 JSON 数据：

```bash
scripts/bring.sh lists --json
scripts/bring.sh show --json
scripts/bring.sh show "Einkaufsliste" --json
```

## 其他注意事项：
- **物品详情** 包括物品下的简短描述文本（如数量、品牌等）。
- `complete` 命令会将物品移至 “最近购买” 列表（类似于在应用程序中勾选该物品）。
- `remove` 命令会从清单中完全删除物品。
- 令牌（token）会缓存在 `~/.cache/bring/token.json` 文件中，并会自动更新。
- 所有更改会立即同步到所有共享该清单的设备上。
- 支持包含特殊字符（引号、变音符号、表情符号）的物品名称。
- Bring! 需要用户提供直接的账户密码——Google/Apple 的单点登录功能不适用于此 API。
- `credentials.json` 文件中的 `country` 参数用于控制物品目录的语言（默认为德语）。
- 在向用户展示物品时，除非用户特别要求查看最近购买的物品，否则只显示 “待购买” 的部分——最近购买的物品列表可能会很长。
- 如果 `remove` 命令执行失败并显示 “未找到” 的错误信息，建议用户使用 `show` 命令查看物品的准确名称。
- ** Bring! API 不支持创建或删除清单**——用户必须在 Bring! 应用程序中进行相关操作。