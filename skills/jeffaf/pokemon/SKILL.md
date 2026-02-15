---
name: pokemon
version: 1.0.0
description: "这是一个用于AI代理的命令行工具（CLI），帮助它们为用户查询宝可梦信息。该工具基于PokéAPI实现，无需任何身份验证（auth）即可使用。"
homepage: https://pokeapi.co
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["pokemon", "pokeapi", "games", "entertainment", "cli"]
---

# Pokémon 查询工具

这是一个为 AI 代理设计的命令行工具（CLI），用于帮助人类用户查询 Pokémon 的相关信息。例如：“喷火龙（Charizard）对什么类型 Pokémon 处于劣势？”——现在你的 AI 代理可以回答这个问题了。

该工具使用 PokéAPI 进行数据查询，无需注册账户或 API 密钥。

## 使用方法

```
"Look up Pikachu"
"What are fire type weaknesses?"
"Tell me about the ability Levitate"
"Search for dragon Pokémon"
```

## 命令列表

| 功能 | 命令                |
|--------|-------------------|
| 搜索    | `pokemon search "查询内容"`     |
| 获取详情 | `pokemon info <名称|ID>`       |
| 类型对战 | `pokemon type <名称>`       |
| 能力信息 | `pokemon ability <名称>`     |

### 使用示例

```bash
pokemon search pikachu        # Find Pokémon by partial name
pokemon info 25               # Get details by Pokédex number
pokemon info charizard        # Get details by name
pokemon type fire             # Fire type matchups
pokemon ability static        # Ability description
```

## 查询结果展示

**搜索结果：**
```
Pikachu
Pikachu-rock-star
Pikachu-belle
```

**详情信息：**
```
⚡ Pikachu [#25]
   Types: Electric
   Height: 0.4m | Weight: 6kg
   Base Stats:
     HP: 35 | Atk: 55 | Def: 40
     Sp.Atk: 50 | Sp.Def: 50 | Spd: 90
   Abilities: Static, Lightning rod
   Sprite: https://raw.githubusercontent.com/.../25.png
```

**简洁格式：**
```
[#25] Pikachu — Electric, HP: 35, Atk: 55, Def: 40, Spd: 90
```

**类型信息：**
```
🔥 Type: Fire

⚔️ Offensive:
   2x damage to: Grass, Ice, Bug, Steel
   ½x damage to: Fire, Water, Rock, Dragon
   0x damage to: None

🛡️ Defensive:
   2x damage from: Water, Ground, Rock
   ½x damage from: Fire, Grass, Ice, Bug, Steel, Fairy
   0x damage from: None
```

**能力信息：**
```
✨ Ability: Static

📖 Effect:
Pokémon with this Ability have a 30% chance of paralyzing
attacking Pokémon on contact.

🎯 Short: Has a 30% chance of paralyzing attacking Pokémon on contact.
```

## 注意事项

- 该工具基于 PokéAPI v2（pokeapi.co）开发。
- 无查询频率限制（但请合理使用）。
- 无需身份验证。
- 名称查询不区分大小写。
- 多词名称请使用连字符分隔：`pokemon info mr-mime`。
- 每次搜索最多返回 20 条匹配结果。

---

## 代理实现说明

**脚本位置：**
- **包装脚本：** `{skill_folder}/pokemon`  
- **具体功能脚本：** `scripts/pokemon`

**当用户询问 Pokémon 相关信息时：**
1. 运行 `./pokemon search "名称"` 来查找 Pokémon 的确切名称。
2. 运行 `./pokemon info <名称|ID>` 来获取完整的 Pokémon 信息。
3. 运行 `./pokemon type <类型>` 来查询该类型的对战情况。
4. 运行 `./pokemon ability <名称>` 来查看该 Pokémon 的能力详情。

**常见使用场景：**
- “X 对什么类型 Pokémon 处于劣势？” → 先查询类型信息，再查找该类型的对战策略。
- “对付 X 最有效的 Pokémon 是什么？” → 先获取相关 Pokémon 的类型信息，再判断哪种类型最有效。
- “X 是否具有 Y 能力？” → 查看该 Pokémon 是否具备某种能力。

**不适用场景：**
- 该工具不适用于查询非 Pokémon 相关的游戏信息、竞技排行榜或粉丝内容。