---
name: bring-list
description: "管理 Bring! 购物清单（Einkaufsliste / 购物清单）：可以添加、删除、勾选商品项，支持批量操作，还提供默认清单功能。适用场景：用户需要设置 Bring! 购物清单、查看清单内容或完成/删除清单中的商品项。提供完整的引导式设置流程（通过 Telegram）：客服人员会处理登录、清单选择及所有配置设置。注重隐私保护：用户可自行选择通过聊天或私人终端输入凭证（凭证不会被重复使用）。终端输入为可选功能。"
---
# Bring! 购物清单

通过非官方的 REST API 管理 Bring! 购物清单。需要使用 `curl` 和 `jq` 工具。

## 代理设置指南

当用户首次请求您设置或使用 Bring! 时，请按照以下步骤操作：

### 第一步：检查是否已配置
首先运行 `scripts/bring.sh lists` 命令。如果命令能够正常执行，说明配置已经完成——可以直接进入使用步骤。

### 第二步：设置凭据
Bring! 需要用户的电子邮件地址和密码。如果用户还没有账户，他们可以在 getbring.com 或 Bring! 应用程序中免费创建一个账户。

**如果用户是通过 Google/Apple 认证登录的：** 需要先在 Bring! 应用程序中设置密码（设置 → 账户 → 更改密码），之后才能使用 API。

询问用户希望如何提供凭据：

> “我需要您的 Bring! 电子邮件地址和密码。您可以选择在聊天中分享（我会将它们写入配置文件，并且不会再提及这些信息），或者如果您希望完全避免在聊天中显示这些信息，我可以提供一个终端命令让您自行输入。您选择哪种方式？”

**选项 A — 通过聊天（方便）：**
用户通过聊天分享电子邮件地址和密码。使用 `jq` 对密码进行安全的 JSON 编码（以防止特殊字符导致的注入问题），并避免将密码显示在聊天中：
```bash
mkdir -p ~/.config/bring
jq -n --arg e "USER_EMAIL" --arg p "USER_PASSWORD" '{email: $e, password: $p}' > ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
```
输入完成后，确认：“已完成——凭据已安全保存。我不会再次提及这些信息。”

**选项 B — 通过终端（更私密）：**
将以下命令提供给用户，让他们在自己的终端中执行。凭据不会显示在聊天中：
```bash
mkdir -p ~/.config/bring
read -rp "Bring! Email: " BEMAIL
read -rsp "Bring! Password: " BPASS && echo
jq -n --arg e "$BEMAIL" --arg p "$BPASS" '{email: $e, password: $p}' > ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
unset BEMAIL BPASS
```
告诉用户：“在您的终端中运行该命令，然后回来，我会继续设置。”

**⚠️ 请勿使用 `scripts/bring.sh setup` 命令**——该命令需要交互式终端（TTY），而代理程序通常没有这样的环境。务必按照第三步的手动方式创建凭据文件。**

### 第三步：保存凭据并测试登录
```bash
mkdir -p ~/.config/bring
jq -n --arg e "USER_EMAIL" --arg p "USER_PASSWORD" '{email: $e, password: $p}' > ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
scripts/bring.sh login
```
如果登录失败，请重新检查电子邮件地址和密码。用户可能需要提供他们的 Bring! 账户密码（而非 Google/Apple 的单点登录密码）。

### 第四步：显示现有清单并询问默认清单
```bash
scripts/bring.sh lists
```
此步骤会显示用户的所有 Bring! 清单。用户可能有多个清单，例如：
- Einkaufsliste（主要购物清单）
- Drogerie（药店商品清单）
- Baumarkt（五金店商品清单）
- 与合作伙伴或家人共享的清单

**如果用户没有任何清单：** 告诉他们在 Bring! 应用程序中创建一个清单。API 不支持创建或删除清单——这些操作必须在应用程序中完成。创建清单后，继续进行设置。

**询问用户希望将哪个清单设置为默认清单。** 这样用户每次操作时就不需要输入清单名称了。
- 如果用户只有一个清单：自动将其设置为默认清单，并告知用户。
- 如果用户有多个清单：显示清单名称并询问他们希望使用哪个作为默认清单。解释说他们仍然可以通过清单名称来添加商品（例如：“在 Baumarkt 清单中添加钉子”）。

### 第五步：设置默认清单
更新凭据文件，将选定的清单设置为默认清单：
```bash
# Read existing config and add default_list
jq --arg list "CHOSEN_LIST_NAME" '. + {default_list: $list}' ~/.config/bring/credentials.json > /tmp/bring_conf.json && mv /tmp/bring_conf.json ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
```

### 第六步：确认设置
向用户展示当前清单的内容，以确认一切设置正确：
```bash
scripts/bring.sh show
```
告诉用户：“设置完成！现在您可以输入类似‘在清单中添加牛奶’或‘购物清单上有什么商品？’这样的指令。”

### 重要提示：清单只能在应用程序中管理
Bring! API 不支持创建或删除清单。如果用户请求创建或删除清单，请告知他们：
“清单只能在 Bring! 应用程序中创建或删除。您在应用程序中进行更改后，我就可以立即处理新的清单了。”

### 共享清单的处理
Bring! 清单通常会在家庭成员或合作伙伴之间共享。代理所做的任何更改会立即同步到所有共享该清单的设备上。请告知用户：
- “我添加的任何商品都会立即显示在所有共享该清单的设备上。”
- 这通常是用户希望看到的情况（例如，合作伙伴可以看到更新后的购物清单），但这一点值得特别说明。

## 设置方式（手动 / 参考）

凭据可以通过环境变量 `BRING_EMAIL` 和 `BRING_PASSWORD` 或配置文件 `~/.config/bring/credentials.json` 来设置：
```json
{"email": "user@example.com", "password": "secret", "default_list": "Einkaufsliste"}
```

**交互式设置（需要交互式终端 TTY）：** `scripts/bring.sh setup`

## 命令

所有命令都支持接受清单名称（部分匹配）或 UUID。如果配置了 `default_list`，则可以省略清单参数。
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

当用户有多个清单时，他们可以通过清单名称来指定目标清单：
- “在 **Baumarkt** 清单中添加钉子” → `scripts/bring.sh add "Baumarkt" "Nails"`
- “**Drogerie** 清单上有什么商品？” → `scripts/bring.sh show "Drogerie"`

清单名称支持不区分大小写的匹配，因此 “einkauf” 会匹配 “Einkaufsliste”。

如果没有指定清单，系统会使用配置文件中的 `default_list`。

## JSON 输出

在 `lists` 和 `show` 命令后添加 `--json` 选项，可以获取原始的 JSON 数据：
```bash
scripts/bring.sh lists --json
scripts/bring.sh show --json
scripts/bring.sh show "Einkaufsliste" --json
```

## 其他注意事项：

- **商品规格** 是商品下方的小描述文本（例如数量、品牌）。
- `complete` 命令会将商品移至 “最近购买” 列表（类似于在应用程序中勾选商品）。
- `remove` 命令会从清单中完全删除商品。
- 令牌存储在 `~/.cache/bring/token.json` 文件中，并会自动刷新。
- 所有更改会立即同步到所有共享该清单的设备上。
- 支持包含特殊字符（引号、变音符号、表情符号）的商品名称。
- Bring! 需要用户提供直接的账户密码——Google/Apple 的单点登录方式无法用于 API。
- `credentials.json` 文件中的 `country` 参数用于控制商品目录的语言（默认为德语）。
- 在向用户展示商品时，除非用户特别要求，否则只显示 “待购买” 的商品信息——因为 “最近购买” 的商品列表可能会很长。
- 如果 `remove` 命令执行失败并显示 “未找到” 的错误信息，建议用户使用 `show` 命令查看商品的具体名称。
- **Bring! API 不支持创建或删除清单**——用户必须在 Bring! 应用程序中管理清单。