---
name: bring-list
description: "管理 Bring! 购物清单（Einkaufsliste / 购物清单）：支持添加、删除、勾选商品项、批量操作以及使用默认清单。适用场景：用户希望设置 Bring! 购物清单、查看清单内容或完成/删除清单中的商品项。提供完整的引导式设置流程（通过 Telegram）：客服人员会处理登录、清单选择及所有配置设置。注重隐私保护：用户可以选择通过聊天或私人终端输入密码（密码不会被重复使用）。终端输入功能为可选。"
---
# Bring! 购物清单

通过非官方的 REST API 管理 Bring! 购物清单。需要使用 `curl` 和 `jq` 工具。

## 代理设置指南

当用户首次请求设置或使用 Bring! 时，请按照以下步骤操作：

### 第 1 步：检查是否已配置
首先运行 `scripts/bring.sh lists` 命令。如果命令能够正常执行，说明配置已经完成——可以直接进入使用步骤。

### 第 2 步：设置凭据
Bring! 需要用户的电子邮件地址和密码。如果用户还没有账户，他们可以在 getbring.com 或 Bring! 应用程序中免费创建一个账户。

**如果用户通过 Google/Apple 账户登录：** 需要在 Bring! 应用程序中先设置密码（设置 → 账户 → 更改密码），之后才能使用 API。

询问用户希望如何提供凭据：

> “我需要您的 Bring! 电子邮件地址和密码。您可以选择在聊天中直接提供（我会将它们写入配置文件，并且不会再提及），或者如果您希望完全保密，我可以提供一个终端命令让您私下输入。您选择哪种方式？”

**选项 A — 通过聊天（方便）：**
用户通过聊天提供电子邮件地址和密码。将信息直接写入配置文件，并且不会在聊天中显示：
```bash
mkdir -p ~/.config/bring
cat > ~/.config/bring/credentials.json << 'EOF'
{"email": "USER_EMAIL", "password": "USER_PASSWORD"}
EOF
chmod 600 ~/.config/bring/credentials.json
```
输入完成后，确认：“已完成——凭据已安全保存。我不会再次提及。”

**选项 B — 通过终端（更私密）：**
向用户提供以下终端命令，让他们在自己的终端中执行：```bash
mkdir -p ~/.config/bring
read -rsp "Bring! Email: " BEMAIL && echo
read -rsp "Bring! Password: " BPASS && echo
printf '{"email":"%s","password":"%s"}\n' "$BEMAIL" "$BPASS" > ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
unset BEMAIL BPASS
```
告知用户：“在您的终端中运行该命令，然后回来继续设置。”

**⚠️ 请勿使用 `scripts/bring.sh setup` 命令**——该命令需要交互式终端（TTY），而代理程序通常没有这种环境。务必按照第 3 步的说明手动创建凭据文件。**

### 第 3 步：保存凭据并测试登录
```bash
mkdir -p ~/.config/bring
cat > ~/.config/bring/credentials.json << 'EOF'
{"email": "USER_EMAIL", "password": "USER_PASSWORD"}
EOF
chmod 600 ~/.config/bring/credentials.json
scripts/bring.sh login
```
如果登录失败，请重新核对电子邮件地址和密码。用户可能需要输入自己的 Bring! 账户密码（而非 Google/Apple 的单点登录密码）。

### 第 4 步：显示现有清单并询问默认清单
```bash
scripts/bring.sh lists
```
此步骤会显示用户所有的 Bring! 清单。用户可能有多个清单，例如：
- Einkaufsliste（主购物清单）
- Drogerie（药店物品清单）
- Baumarkt（五金店物品清单）
- 与伴侣/家人共享的清单

**如果用户没有任何清单：** 告诉他们在 Bring! 应用程序中创建一个清单。API 不支持创建或删除清单，这些操作必须在应用程序中完成。创建清单后，继续进行设置。

**询问用户希望将哪个清单设置为默认清单。** 这样用户每次使用时就可以避免重复输入清单名称。

- 如果用户只有一个清单：自动将其设置为默认清单，并告知用户。
- 如果用户有多个清单：显示所有清单名称，然后询问他们希望使用哪个作为默认清单。解释说他们仍然可以通过清单名称来添加物品（例如：“在 Baumarkt 清单中添加钉子”）。

### 第 5 步：设置默认清单
更新凭据文件，将选定的清单设置为默认清单：
```bash
# Read existing config and add default_list
jq --arg list "CHOSEN_LIST_NAME" '. + {default_list: $list}' ~/.config/bring/credentials.json > /tmp/bring_conf.json && mv /tmp/bring_conf.json ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
```

### 第 6 步：确认设置
向用户展示当前清单的内容，以确认所有设置都正确：
```bash
scripts/bring.sh show
```
告知用户：“设置完成！现在您可以输入类似‘在清单中添加牛奶’或‘购物清单上有什么物品？’这样的指令。”

### 重要提示：清单只能在应用程序中管理
Bring! API 不支持创建或删除清单。如果用户请求创建新清单或删除清单，请告知他们：
“清单只能在 Bring! 应用程序中创建或删除。您在应用程序中进行更改后，我就可以立即处理新的清单了。”

### 共享清单的处理
Bring! 清单通常会在家庭成员或伴侣之间共享。代理程序所做的任何更改都会立即同步到所有共享该清单的设备上。请告知用户：
- “我添加的任何物品都会立即显示在所有共享该清单的设备上。”
- 这通常是用户希望看到的功能（例如，伴侣可以看到更新后的购物清单），但有必要明确说明。

## 设置方式（手动 / 参考）

凭据可以通过环境变量 `BRING_EMAIL` 和 `BRING_PASSWORD` 或配置文件 `~/.config/bring/credentials.json` 来设置：
```json
{"email": "user@example.com", "password": "secret", "default_list": "Einkaufsliste"}
```

**交互式设置（需要交互式终端 TTY）：** `scripts/bring.sh setup`

## 命令

所有命令都接受清单名称（部分匹配）或 UUID。如果配置了 `default_list`，则可以省略清单参数。
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

当用户有多个清单时，他们可以通过清单名称来定位特定的清单：
- “在 **Baumarkt** 清单中添加钉子” → `scripts/bring.sh add "Baumarkt" "Nails"`
- “**Drogerie** 清单上有什么物品？” → `scripts/bring.sh show "Drogerie"`

清单名称支持不区分大小写的匹配，因此 “einkauf” 会匹配 “Einkaufsliste”。

如果没有指定清单，系统会使用配置文件中的 `default_list`。

## JSON 输出

在 `lists` 和 `show` 命令后添加 `--json` 选项，可以获取原始 JSON 数据：
```bash
scripts/bring.sh lists --json
scripts/bring.sh show --json
scripts/bring.sh show "Einkaufsliste" --json
```

## 其他注意事项

- **规格说明**：是指物品下方的小描述文本（例如数量、品牌）。
- `complete` 命令会将物品移至 “最近购买” 的列表中（类似于在应用程序中勾选）。
- `remove` 命令会从清单中完全删除物品。
- 令牌存储在 `~/.cache/bring/token.json` 文件中，并会自动刷新。
- 更改会立即同步到所有共享该清单的设备上。
- 支持包含特殊字符（引号、变音符号、表情符号）的物品名称。
- Bring! 需要用户的直接账户密码——Google/Apple 的单点登录功能不适用于此 API。
- `credentials.json` 文件中的 `country` 参数用于控制物品目录的语言（默认为德语）。
- 在向用户展示物品时，除非用户特别要求，否则只显示 “待购买” 的部分——最近购买的物品列表可能会很长。
- 如果 `remove` 命令返回 “未找到” 的错误，请建议用户使用 `show` 命令查看物品的准确名称。
- **Bring! API 不支持创建或删除清单**——用户必须通过 Bring! 应用程序来管理清单。