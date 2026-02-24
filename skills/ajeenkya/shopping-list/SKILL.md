---
name: shopping-list
version: 1.0.0
description: >
  **智能购物清单**  
  具备分类功能、支持家庭成员共享以及记录购买历史。用户可以通过自然语言添加商品、勾选已购买的商品，并按类别对购物清单进行整理。适用于各种购物场景，无论是日常杂货采购，还是需要制定购物清单时（例如“我们需要买些什么”）。  
  **主要功能：**  
  1. **添加商品**：用户可以直接通过自然语言描述所需购买的商品，系统会自动将其添加到购物清单中。  
  2. **勾选已购买商品**：用户可以轻松勾选已购买的商品，以便快速查看已购物品。  
  3. **分类管理**：购物清单支持按类别进行排序和整理，便于用户快速查找所需商品。  
  4. **家庭成员共享**：支持家庭成员共同使用同一购物清单，方便大家共同规划购物计划。  
  5. **购买历史记录**：系统会自动记录用户的购买历史，方便日后查看和参考。  
  **使用场景：**  
  - 日常杂货采购  
  - 家庭购物计划  
  - 制定购物清单  
  - 查看已购商品  
  **简单操作示例：**  
  - “我们需要买些水果和蔬菜。” → 系统会自动创建一个购物清单，并列出相应的商品。  
  - “我已经买了苹果，可以把它从清单中划掉。” → 用户可以直接在清单中勾选并删除已购买的商品。  
  - “请帮我整理一下这个购物清单，按照水果、蔬菜和肉类分类。” → 系统会按照用户要求对清单进行分类整理。
---
# 购物清单

用于管理家庭的购物清单。可以添加商品及其数量，标记已勾选的项，并按类别进行整理。数据存储在 `skills/shopping-list/data/` 目录下。

有关完整的命令参考和输出格式，请参阅 `skills/shopping-list/references/commands.md`。

## 在执行每个命令之前

在每次操作购物清单之前，请按以下顺序进行检查：

1. 如果 `skills/shopping-list/data/` 目录不存在，请创建它。
2. 如果 `data/active.json` 文件不存在，请使用以下代码创建它：
   ```json
   {
     "items": [],
     "categories": ["Produce", "Dairy", "Meat", "Pantry", "Frozen", "Beverages", "Household", "Personal"],
     "lastModified": "<current ISO timestamp>"
   }
   ```
3. 如果 `data/active.json` 文件存在但无法解析为有效的 JSON 格式，请将其重命名为 `data/active.json.corrupt`，并创建一个新的默认文件。然后告知用户：“购物清单数据已损坏。已保存备份文件为 active.json.corrupt，并重新生成了新的清单。”
4. 如果 `data/config.json` 文件不存在，请使用以下代码创建它：`{"user": null, "snoozes": {}``
5. 如果 `config.json` 文件中的 `user` 值为 `null`，请询问用户：“是 AJ 还是 Shal 在添加商品？” 将用户的回答（小写形式）保存到 `config.json` 中，然后再继续执行原始命令。
6. 运行归档流程（详见下面的“归档”部分）。

本文档中的所有文件路径都是相对于 `skills/shopping-list/` 目录的，除非另有说明。

## 数据文件

### data/active.json

当前正在使用的购物清单，包含所有尚未归档的商品。

```json
{
  "items": [
    {
      "id": "F47AC10B-58CC-4372-A567-0E02B2C3D479",
      "name": "Whole Milk",
      "normalizedName": "whole milk",
      "quantity": 2,
      "unit": "gallons",
      "category": "Dairy",
      "checkedOff": false,
      "checkedOffDate": null,
      "addedBy": "aj",
      "addedDate": "2026-02-24T10:00:00Z",
      "notes": null
    }
  ],
  "categories": ["Produce", "Dairy", "Meat", "Pantry", "Frozen", "Beverages", "Household", "Personal"],
  "lastModified": "2026-02-24T10:00:00Z"
}
```

字段规则：
- `id`：通过 bash 中的 `uuidgen` 生成。如果该命令不可用，则使用当前 ISO 时间戳加上 4 个随机十六进制字符来生成 ID（例如：`2026-02-24T10:00:00Z-a3f1`）。
- `name`：用户提供的商品名称，去除前后的空格。为了显示目的，保留原始的大小写形式。
- `normalizedName`：始终计算为 `name.toLowerCase().trim()` 的结果。每次添加或编辑商品时都会重新计算该字段。该字段用于所有匹配和去重操作。
- `quantity`：可选。如果用户未指定数量，则默认为 `null`。如果指定了数量，必须是一个大于 0 的数字。允许使用小数值（例如：0.5 表示半磅）。
- `unit`：可选的文本字段（例如：“gallons”（加仑）、“lbs”（磅）、“bunch”（束）、“bag”（袋）。如果未指定，则默认为 `null`。
- `category`：`categories` 数组中的一个值，或者为 “Uncategorized”（未分类）。
- `checkedOff`：布尔值。初始值为 `false`。当用户勾选商品时，将其设置为 `true`。
- `checkedOffDate`：商品被勾选的 ISO 时间戳。如果未勾选，则为 `null`。
- `addedBy`：来自 `config.json` 中用户字段的小写字符串（例如：“aj” 或 “shal”）。
- `addedDate`：商品首次添加的 ISO 时间戳。
- `notes`：可选的文本字段，用于特殊说明（例如：“有机食品”、“Costco 规格”）。默认值为 `null`。
- `categories`（顶级数组）：已知的商品类别列表。包含 8 个预设类别，用户可以添加自定义类别。
- `lastModified`：ISO 时间戳。每次写入该文件时都会更新。

### data/config.json

存储会话持久化的用户配置信息。

```json
{ "user": "aj", "snoozes": {} }
```

- `user`：在首次交互时设置，并在会话之间保持不变。为小写字符串。
- `snoozes`：保留用于第二阶段的补货建议。目前暂时忽略该字段；在写入数据时保留该字段。

### data/history-YYYY-MM.json

每月购买的商品归档文件。每个月份生成一个文件，按需创建。

```json
{
  "month": "2026-02",
  "archivedItems": [
    { "...same fields as active item...", "archivedDate": "2026-02-25T08:00:00Z" }
  ]
}
```

当商品从活动状态转移到历史状态时，会为其添加 `archivedDate` 字段。保留活动状态下的所有原始字段。当一个月份还没有归档文件时，系统会自动创建一个新的文件。

## 核心操作

### 添加商品

将用户输入的自然语言内容解析为商品的名称、数量和单位。

**类别推断**：根据商品名称自动推断其所属类别。常见的映射规则如下：
- milk（牛奶）、cheese（奶酪）、yogurt（酸奶）、butter（黄油）归类为 Dairy（乳制品）；
- chicken（鸡肉）、beef（牛肉）、fish（鱼）归类为 Meat（肉类）；
- bananas（香蕉）、lettuce（生菜）、onions（洋葱）归类为 Produce（农产品）；
- rice（大米）、pasta（意大利面）、flour（面粉）归类为 Pantry（食品储藏）；
- dish soap（洗洁精）、paper towels（纸巾）归类为 Household（家居用品）；
- shampoo（洗发水）、toothpaste（牙膏）归类为 Personal（个人护理用品）；
- beer（啤酒）、wine（葡萄酒）、juice（果汁）归类为 Beverages（饮料）；
- frozen pizza（冷冻披萨）、ice cream（冰淇淋）归类为 Frozen（冷冻食品）。
如果映射不明确，系统会自动将商品归类为 “Uncategorized”（未分类）。系统不会提示用户手动选择类别。如果用户希望更改类别，可以输入 “将 X 移到 Y 类别”。

**多商品输入**：用户可以一次性添加多个商品，例如：“add eggs, bread, and 2 gallons milk”（添加鸡蛋、面包和 2 加仑牛奶），系统会生成 3 个独立的商品条目。系统会解析逗号和 “and” 作为商品分隔符。如果商品名称包含复合词（如 “hot dog buns”），系统会询问用户以获取准确的信息。

**处理重复商品**：在创建新商品之前，系统会检查活动清单中是否已经存在具有相同 `normalizedName` 的商品：
- 如果存在且未被勾选，系统会更新该商品的数量（如果用户提供了新的数量，则更新数量；否则保持不变）。不会创建重复条目。
- 如果存在且已被勾选，系统会取消勾选（将 `checkedOff` 设置为 `false`，`checkedOffDate` 设置为 `null`），并根据用户提供的数量更新数量。
- 如果存在且已被勾选，系统会取消勾选（将 `checkedOff` 设置为 `false`，`checkedOffDate` 设置为 `null`），并更新数量（如果用户提供了新的数量）。

**添加新类别**：如果用户指定了 `categories` 数组中不存在的类别，系统会将该类别添加到数组中，并将商品归入该类别。

系统会从 `config.json` 中获取 `addedBy` 值，并将 `addedDate` 设置为当前 ISO 时间戳。将 `checkedOff` 设置为 `false`，`checkedOffDate` 设置为 `null`，并在写入数据后更新 `lastModified` 字段。

### 勾选商品

根据 `normalizedName` 来匹配商品（不区分大小写，部分匹配也是允许的，例如：“milk” 会匹配 “whole milk”）。
- **匹配到一个商品**：将 `checkedOff` 设置为 `true`，并将 `checkedOffDate` 设置为当前 ISO 时间戳。确认用户的操作。
- **匹配到多个商品**：列出所有匹配的商品，然后询问用户要勾选哪一个。
- **没有匹配到的商品**：显示当前的商品列表，以便用户选择正确的商品。

已勾选的商品会保留在 `active.json` 中，并以斜线标记的形式显示，直到归档流程将其转移到历史记录中（24 小时后）。

### 删除商品

从活动清单中永久删除商品。不会生成归档记录，也不会在历史记录中留下痕迹。此功能用于处理用户误操作（例如：“我误将这个商品添加到了清单中”）的情况。

使用与勾选商品相同的规则来匹配商品，并确认用户的删除操作。

### 编辑商品

根据 `normalizedName` 来匹配目标商品，然后更新相应的字段。可编辑的字段包括：名称、数量、单位、类别和备注。

如果商品名称发生变化，系统会重新计算 `normalizedName`。如果商品的类别不在 `categories` 数组中，系统会将其添加到数组中。写入数据后更新 `lastModified` 字段。

### 更改用户

当用户输入 “switch to Shal” 或 “I'm AJ” 等指令时，系统会更新 `config.json` 中的 `user` 值。此后添加的所有商品都会使用新的用户名称作为 `addedBy`。

## 归档流程

此流程会在每次执行购物清单命令之前自动运行：

1. 读取 `data/active.json` 文件。
2. 找出所有 `checkedOff` 为 `true` 且 `checkedOffDate` 超过 24 小时的商品。
3. 如果没有符合条件的商品，跳过后续步骤。
4. 确定当前月份（例如：“2026-02”），然后读取 `data/history-2026-02.json` 文件。如果文件不存在，使用 `{ "month": "2026-02", "archivedItems": [] }` 创建该文件。
5. 将符合条件的商品添加到历史记录文件的 `archivedItems` 数组中，并为其设置 `archivedDate` 字段（当前 ISO 时间戳）。
6. 写入历史记录文件。
7. 从 `data/active.json` 文件中的 `items` 数组中删除已归档的商品。
8. 重新写入 `active.json` 文件。

**写入顺序很重要**：必须先写入历史记录文件，再写入活动清单文件。如果在两次写入之间中断，最坏的情况只是历史记录中出现重复条目。如果顺序颠倒，可能会导致数据丢失（即商品从活动清单中删除但未写入历史记录）。

`shopping clear` 命令会立即执行相同的流程，但会跳过 24 小时的等待时间，直接处理所有已勾选的商品。

## 显示清单

显示购物清单时，按照以下固定顺序对类别进行排序：
1. 首先显示预设的类别：Produce（农产品）、Dairy（乳制品）、Meat（肉类）、Pantry（食品储藏）、Frozen（冷冻食品）、Beverages（饮料）、Household（家居用品）、Personal（个人护理用品）；
2. 然后按字母顺序显示自定义类别；
3. “Uncategorized”（未分类）始终显示在最后。

对于没有商品的类别（仅考虑未勾选的商品），跳过该类别。在每个类别内部，按照 `normalizedName` 对商品进行字母排序。不要依赖 JSON 文件中存储的类别顺序。

已勾选的商品会在其所属类别中以斜线标记的形式显示，与未勾选的商品区分开来。这些商品会一直显示在清单上，直到被归档。

## 查看历史记录

当用户询问过去的购买记录时（例如：“上个月我们买了什么”、“购买历史”、“一月份买了什么”），系统会读取相应的 `data/history-YYYY-MM.json` 文件。结果会按日期分组显示（最新的记录在前），包括商品名称和数量。如果请求的月份没有对应的历史记录文件，系统会告知用户该月份没有购买记录。

注意：历史记录显示的是归档日期，而不是购买日期。例如，2 月 28 日勾选的商品会在 3 月的历史记录中显示。