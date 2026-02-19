---
name: bring-list
description: "这是ClawHub上最出色的Bring!技能。它没有任何依赖项，经过VirusTotal的安全检测，OpenClaw的评分高达“高置信度”（HIGH CONFIDENCE）。该技能支持完整的CRUD操作（创建、读取、更新、删除）、批量处理功能，还提供了默认的代理设置选项以及引导式代理配置流程——所有这些功能都由AI自动完成，让您无需手动操作。"
---
# Bring! 购物清单

通过非官方的 REST API 管理 Bring! 购物清单。需要使用 `curl` 和 `jq` 工具。

## 代理设置指南

当用户首次请求设置或使用 Bring! 时，请按照以下步骤操作：

### 第一步：检查是否已配置
首先运行 `scripts/bring.sh lists` 命令。如果命令能够正常执行，说明配置已经完成——可以直接进入使用步骤。

### 第二步：获取用户凭证
告诉用户：
- “我需要您的 Bring! 登录信息（邮箱 + 密码）。如果您还没有账户，可以在 getbring.com 或 Bring! 应用程序中免费创建一个。”
- **如果用户是通过 Google/Apple 登录的：** 他们需要先在 Bring! 应用程序中设置密码（设置 → 账户 → 更改密码）。
- **切勿在聊天中存储用户凭证。** 应将凭证直接写入配置文件 `~/.config/bring/credentials.json` 中。
- 如果用户不愿意在聊天中分享密码，可以建议他们手动创建该文件，格式如下：`{"email": "...", "password": "..."}`

**⚠️ 请勿使用 `scripts/bring.sh setup` 命令**——该命令需要交互式终端（TTY），而代理程序通常没有这样的环境。务必按照第三步的手动方式创建凭证文件。**

### 第三步：保存凭证并测试登录
```bash
mkdir -p ~/.config/bring
cat > ~/.config/bring/credentials.json << 'EOF'
{"email": "USER_EMAIL", "password": "USER_PASSWORD"}
EOF
chmod 600 ~/.config/bring/credentials.json
scripts/bring.sh login
```
如果登录失败，请重新核对邮箱和密码。用户可能需要提供 Bring! 应用程序中的密码（而非 Google/Apple 的单点登录密码）。

### 第四步：显示现有清单并选择默认清单
```bash
scripts/bring.sh lists
```
此步骤会显示用户的所有 Bring! 清单。用户可能有多个清单，例如：
- Einkaufsliste（主要购物清单）
- Drogerie（药店物品清单）
- Baumarkt（五金店物品清单）
- 与伴侣或家人共享的清单

**如果用户没有任何清单：** 建议他们先在 Bring! 应用程序中创建一个清单。API 不支持创建或删除清单，这些操作必须在应用程序中完成。创建清单后，继续进行后续设置。

**询问用户希望将哪个清单设置为默认清单。** 这样用户每次操作时就不需要手动输入清单名称了。
- 如果用户只有一个清单：自动将其设置为默认清单，并告知用户。
- 如果用户有多个清单：显示清单名称并询问使用哪个作为默认清单。同时解释用户仍然可以通过清单名称来添加或删除物品（例如：“在 Baumarkt 清单中添加钉子”）。

### 第五步：设置默认清单
更新凭证文件，将选定的清单设置为默认清单：
```bash
# Read existing config and add default_list
jq --arg list "CHOSEN_LIST_NAME" '. + {default_list: $list}' ~/.config/bring/credentials.json > /tmp/bring_conf.json && mv /tmp/bring_conf.json ~/.config/bring/credentials.json
chmod 600 ~/.config/bring/credentials.json
```

### 第六步：确认设置完成
向用户展示当前清单的内容，以确认一切设置正确：
```bash
scripts/bring.sh show
```
告诉用户：“设置完成！现在您可以输入类似‘在清单中添加牛奶’或‘购物清单里有什么?’这样的指令了。”

### 重要提示：清单只能在应用程序中管理
Bring! API 不支持创建或删除清单。如果用户请求创建或删除清单，请告知他们：
“清单只能在 Bring! 应用程序中进行创建或删除。您在应用程序中完成操作后，我就可以立即开始处理新的清单了。”

### 共享清单的处理
Bring! 清单通常会在家庭成员或伴侣之间共享。代理程序所做的任何更改会立即同步到所有共享该清单的设备上。请告知用户：
- “我添加的任何物品都会立即显示在所有共享该清单的设备上。”
- 这通常是用户希望看到的功能（例如，伴侣可以看到更新后的购物清单），但也需要特别说明。

## 设置方式（手动/参考）

凭证可以通过环境变量 `BRING_EMAIL` 和 `BRING_PASSWORD` 或配置文件 `~/.config/bring/credentials.json` 来设置：

```json
{"email": "user@example.com", "password": "secret", "default_list": "Einkaufsliste"}
```

**交互式设置（需要交互式终端 TTY）：** `scripts/bring.sh setup`

## 命令说明

所有命令都接受清单名称（部分匹配）或 UUID 作为参数。如果配置了 `default_list`，则可以省略清单名称参数。

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

当用户有多个清单时，可以通过清单名称来指定目标清单：
- “在 **Baumarkt** 清单中添加钉子” → `scripts/bring.sh add "Baumarkt" "Nails"`
- “**Drogerie** 清单里有什么？” → `scripts/bring.sh show "Drogerie"`

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
- **物品说明** 是物品下方的小段描述文字（例如数量、品牌）。
- `complete` 命令会将物品移至“最近购买”列表（类似于在应用程序中勾选的状态）。
- `remove` 命令会从清单中彻底删除物品。
- 令牌（token）存储在 `~/.cache/bring/token.json` 文件中，并会自动更新。
- 所有更改会立即同步到所有共享该清单的设备上。
- 支持包含特殊字符（引号、变音符号、表情符号）的物品名称。
- Bring! 需要用户提供直接的账户密码——Google/Apple 的单点登录功能不适用于此 API。
- `credentials.json` 文件中的 `country` 参数用于控制物品目录的语言（默认为德语）。
- 在向用户展示物品时，除非用户特别要求查看最近购买的物品，否则只显示“待购买”部分的物品——最近购买的物品列表可能会很长。
- 如果 `remove` 命令执行失败并显示“未找到”错误，请建议用户使用 `show` 命令核对物品名称。
- **创建/删除清单的功能不受 Bring! API 支持**——用户必须在 Bring! 应用程序中进行这些操作。