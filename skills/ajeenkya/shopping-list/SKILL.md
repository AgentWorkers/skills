---
name: shopping-list
version: 1.0.1
description: 这是一个支持对话式操作的购物清单工具，具备分类功能、家庭成员共享功能以及购买历史记录功能。用户可以通过自然语言来添加商品、勾选已购买的商品、按类别对商品进行整理。适用于各种类型的购物清单，无论是日常杂货清单，还是需要创建“添加到购物清单”或“我们需要购买什么”等任务的场景。
---
# 购物清单

用于管理家庭购物清单。可以添加商品及其数量，并标记已选中的商品；支持按类别进行排序。数据存储在 `skills/shopping-list/data/` 目录下。

有关完整命令参考和输出格式，请参阅 `skills/shopping-list/references/commands.md`。

## 在执行每个命令之前

在执行任何购物清单操作之前，请按以下顺序进行检查：

1. 如果 `skills/shopping-list/data/` 目录不存在，请创建它。
2. 如果 `data/active.json` 文件不存在，请使用以下代码创建它：
   ```json
   {
     "items": [],
     "categories": ["Produce", "Dairy", "Meat", "Pantry", "Frozen", "Beverages", "Household", "Personal"],
     "lastModified": "<current ISO timestamp>"
   }
   ```
3. 如果 `data/active.json` 文件存在但无法解析为有效的 JSON 数据，请将其重命名为 `data/active.json.corrupt`，并创建一个新的默认文件。然后告知用户：“购物清单数据已损坏。已保存备份文件为 active.json.corrupt，并重新生成了购物清单。”
4. 如果 `data/config.json` 文件不存在，请使用以下代码创建它：`{"user": null, "snoozes": {}`
5. 如果 `config.json` 文件中的 `user` 值为 `null`，请询问用户：“您的名字是什么？我将使用这个名字来记录每件商品的添加者。” 将用户的回答（转换为小写）保存到 `config.json` 文件中，然后再执行原始命令。
6. 运行归档流程（详见下面的“归档”部分）。

本文档中的所有文件路径均为相对路径，除非另有说明。

## 数据文件

### data/active.json

当前正在使用的购物清单。其中包含所有尚未归档的商品。

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
- `id`：通过 bash 中的 `uuidgen` 命令生成。如果该命令不可用，则使用当前 ISO 时间戳加上 4 个随机十六进制字符来生成 ID（例如：`2026-02-24T10:00:00Z-a3f1`）。
- `name`：用户输入的商品名称，去除前后的空格。为了显示目的，保留原始的大小写形式。
- `normalizedName`：始终计算为 `name.toLowerCase().trim()` 的结果。每次添加或编辑商品时都会重新计算该字段。该字段用于所有匹配和去重操作。
- `quantity`：可选。如果用户未指定数量，则默认值为 `null`。如果指定了数量，必须是一个大于 0 的数字。允许使用小数值（例如：0.5 表示半磅）。
- `unit`：可选的文本字段（例如：“gallons”（加仑）、“lbs”（磅）、“bunch”（束）、“bag”（袋）。如果未指定，则默认值为 `null`。
- `category`：`categories` 数组中的一个值，或者为 “Uncategorized”（未分类）。
- `checkedOff`：布尔值。初始值为 `false`。当用户选中某件商品时，将其设置为 `true`。
- `checkedOffDate`：商品被选中的 ISO 时间戳。如果商品未被选中，则该字段为 `null`。
- `addedBy`：来自 `config.json` 中用户字段的小写字符串（例如：“aj” 或 “shal”）。
- `addedDate`：商品首次被添加的 ISO 时间戳。
- `notes`：用于记录特殊说明的文本字段（例如：“有机食品” 或 “Coco-Cola 大杯”）。默认值为 `null`。
- `categories`（顶层数组）：已知的商品类别列表。包含 8 个预设类别，用户可以添加自定义类别。
- `lastModified`：文件的最后修改时间戳。每次写入文件时都会更新。

### data/config.json

存储会话持久化的用户配置信息。

```json
{ "user": "aj", "snoozes": {} }
```

- `user`：在首次交互时设置，并在会话之间保持不变。为小写字符串。
- `snoozes`：预留用于第二阶段的补货建议。目前暂时忽略该字段；在写入数据时保留该字段。

### data/history-YYYY-MM.json

每月购买的商品归档文件。每个月份对应一个文件，按需生成。

```json
{
  "month": "2026-02",
  "archivedItems": [
    { "...same fields as active item...", "archivedDate": "2026-02-25T08:00:00Z" }
  ]
}
```

当商品从活动状态移至归档状态时，会为其添加 `archivedDate` 字段。保留活动状态下的所有原始字段。如果某个月份还没有归档文件，系统会自动创建一个新的归档文件。

## 核心操作

### 添加商品

将用户输入的自然语言文本解析为商品的名称、数量和单位。

**类别推断**：根据商品名称自动推断其所属类别。常见对应关系如下：
- milk/cheese/yogurt/butter 对应 Dairy（乳制品）
- chicken/beef/fish 对应 Meat（肉类）
- bananas/lettuce/onions 对应 Produce（农产品）
- rice/pasta/flour 对应 Pantry（食品储藏）
- dish soap/paper towels 对应 Household（家居用品）
- shampoo/toothpaste 对应 Personal（个人护理用品）
- beer/wine/juice 对应 Beverages（饮料）
- frozen pizza/ice cream 对应 Frozen（冷冻食品）
如果无法明确判断类别，将其标记为 “Uncategorized”（未分类）。切勿要求用户手动选择类别。如果用户需要更改类别，可以让他们输入 “将 X 移到 Y 类别”。

**多商品输入**：用户可以一次性添加多个商品，例如：“add eggs, bread, and 2 gallons milk”（添加鸡蛋、面包和 2 加仑牛奶），系统会生成 3 个独立的商品条目。系统会解析逗号和 “and” 作为商品分隔符。如果商品名称包含复合词（如 “hot dog buns”），请询问用户以获取准确信息，避免错误解析。

**处理重复商品**：在创建新商品之前，检查活动清单中是否已存在具有相同 `normalizedName` 的商品：
- 如果存在且未被选中，更新该商品的数量（如果用户提供了新数量，则更新数量；否则保持不变）。切勿创建重复条目。
- 如果存在且已被选中，取消选中状态（将 `checkedOff` 设置为 `false`，`checkedOffDate` 设置为 `null`），并根据需要更新数量。
- 如果用户指定了新的类别，请将该商品添加到 `categories` 数组中，并将其归入相应的类别。

将 `addedBy` 字段设置为 `config.json` 中记录的用户名称。将 `addedDate` 设置为当前的 ISO 时间戳。将 `checkedOff` 设置为 `false`，`checkedOffDate` 设置为 `null`。写入数据后更新 `lastModified` 字段。

### 选中商品

根据 `normalizedName` 来匹配商品（不区分大小写，部分匹配也有效，例如：“milk” 可匹配 “whole milk”）。
- **匹配到单个商品**：将 `checkedOff` 设置为 `true`，并将 `checkedOffDate` 设置为当前的 ISO 时间戳。确认用户的操作。
- **匹配到多个商品**：列出所有匹配到的商品，让用户选择要选中的商品。
- **未匹配到商品**：显示当前的商品列表，以便用户确认正确的商品。

被选中的商品会保留在 `active.json` 中，并以斜线标记显示，直到归档流程将其移至历史记录中（24 小时后）。

### 删除商品

从活动清单中永久删除某件商品。不会生成归档记录。此功能用于处理用户误操作（例如误删商品）。

使用与选中商品相同的规则根据 `normalizedName` 来匹配商品，并确认用户是否真的要删除该商品。

### 修改商品

根据 `normalizedName` 来匹配目标商品，然后更新相应的字段。可编辑的字段包括：名称、数量、单位、类别和备注。
如果商品名称发生变化，重新计算 `normalizedName`。如果商品的类别不在 `categories` 数组中，将其添加到数组中。写入数据后更新 `lastModified` 字段。

### 更改用户

当用户输入 “switch to Shal” 或 “I'm AJ” 等指令时，更新 `config.json` 中的 `user` 值。此后添加的所有商品都将使用新的用户名称作为 `addedBy`。

## 归档流程

此流程会在每次执行购物清单命令之前自动运行：

1. 读取 `data/active.json` 文件。
2. 找出所有 `checkedOff` 为 `true` 且 `checkedOffDate` 超过 24 小时的商品。
3. 如果没有符合条件的商品，则跳过后续步骤。
4. 确定当前月份（例如：“2026-02”），并读取 `data/history-2026-02.json` 文件。如果文件不存在，则创建一个新文件，内容为 `{"month": "2026-02", "archivedItems": []}`。
5. 将符合条件的商品添加到历史记录文件的 `archivedItems` 数组中，并为其设置 `archivedDate` 为当前的 ISO 时间戳。
6. 保存历史记录文件。
7. 从 `data/active.json` 文件的 `items` 数组中删除已归档的商品。
8. 保存活动清单文件。

**写入顺序很重要**：必须先保存历史记录文件，再保存活动清单文件。如果在两次写入过程中中断，最坏的情况只是历史记录中出现重复条目。如果顺序颠倒，可能会导致数据丢失（例如：商品从活动清单中删除但未写入历史记录）。

`shopping clear` 命令会立即执行相同的归档流程，但不会等待 24 小时。

## 显示清单

显示购物清单时，按以下顺序对类别进行排序：
1. 首先显示预设的类别：Produce（农产品）、Dairy（乳制品）、Meat（肉类）、Pantry（食品储藏）、Frozen（冷冻食品）、Beverages（饮料）、Household（家居用品）、Personal（个人护理用品）。
2. 自定义类别按字母顺序排列。
3. “Uncategorized”（未分类）始终显示在列表的最后。

对于没有商品的类别，跳过该类别的显示（仅考虑未选中的商品）。在每个类别内部，按 `normalizedName` 对商品进行字母排序。不要依赖 JSON 文件中存储的类别顺序。

被选中的商品会在其所属类别中以斜线标记显示，以便与未选中的商品区分开来。这些商品会一直显示在清单上，直到被归档。

## 查看历史记录

当用户询问过去的购买记录时（例如：“上个月买了什么？”、“购买历史” 或 “一月份买了什么？”），系统会读取相应的 `data/history-YYYY-MM.json` 文件。结果按日期排序（最新的记录在前），并显示商品名称和数量。如果请求的月份没有对应的归档文件，系统会告知用户该月份没有购买记录。

注意：历史记录显示的是归档日期，而非购买日期。例如：2 月 28 日选中的商品会在 3 月的历史记录中显示。