---
name: discord-markdown
description: 使用 Markdown 语法来格式化文本，适用于在 Discord 中编写消息、机器人回复、嵌入内容、论坛帖子、Webhook 数据或任何 destin 于 Discord 聊天界面的内容。当用户请求格式化文本（如使用 Markdown 格式）、发送 Discord 消息、与 Discord 机器人交互、使用 Discord 嵌入功能，或者需要文本能够被 Discord 渲染引擎正确显示时，该规则会生效。Markdown 支持以下格式化方式：加粗、斜体、下划线、删除线、剧透提示、带有语法高亮的代码块、标题、子文本、列表、块引用、带遮罩的链接、时间戳以及提及（mention）功能。所有需要被 Discord 正确显示的文本都应放在被引用的代码块中，这样用户就可以直接将其复制粘贴到 Discord 中，同时保留所有的 Markdown 格式。
---
# Discord Markdown 格式

本文档介绍了如何在 Discord 中使用 Markdown 格式化文本。Discord 使用了一种修改过的 Markdown 语法，并添加了一些独特的功能（如剧透提示、时间戳、子文本和公会导航等）。

## 输出格式 —— 至关重要

在为 Discord 用户编写消息时，**务必将最终的格式化文本放在一个代码块中**，这样用户就可以直接将其复制粘贴到 Discord 中，而不会丢失任何格式。

**原因：** Claude 的聊天界面会直接渲染 Markdown 格式的内容（例如，`**bold** 会被显示为 **bold**）。如果用户直接复制已渲染的文本，Markdown 语法会被删除，导致文本在粘贴后失去格式。而代码块可以保留原始的 Markdown 语法。

### 如何呈现 Discord 消息

请始终使用 `markdown` 标签将最终的可复制文本放在代码块中：

````
```markdown
# 🚀 公告

**这是加粗的**，~~这是删除线~~，以及 ||这是剧透内容||

> 这里是一个块引用

-# 子文本脚注
```
````

### 规则

1. **始终使用代码块** —— 使用三个反引号 `"""` 和 `markdown` 标签。
2. **整个消息必须放在一个代码块中** —— 用户复制到 Discord 的所有内容都必须放在一个代码块内。任何格式化的部分都不应出现在代码块之外。
3. **在代码块外说明** —— 将任何注释、选项或上下文放在代码块之前或之后，**切勿放在代码块内部**。
4. **处理嵌套代码块** —— 如果 Discord 消息本身包含代码块，请使用四个反引号 `"""` 作为外层代码块，以确保内部的三个反引号能够被正确显示。用户复制的是代码块之间的所有内容：
```
```
````markdown
这是示例代码：

```javascript
console.log("hello");
```
```
很酷吧？

5. **多条消息 = 多个代码块** —— 如果提供多个选项或消息序列，请为每个消息使用一个单独的代码块，并在上面加上标签。
6. **消息元数据摘要** —— 在每个 Discord 消息代码块之后，务必显示一个元数据摘要表。
7. **模板也是如此** —— 当展示参考文件中的模板时，也必须遵循相同的规则，将它们放在可复制的代码块中。
8. **切勿部分渲染** —— **不要** 将标题、加粗文本、代码片段或其他 Discord 格式的内容放在代码块之外。如果这些内容是消息的一部分，就必须放在代码块内。用户不应该需要手动组合已渲染的 Markdown 和代码块。

### 消息元数据摘要

在每个 Discord 消息代码块之后，添加一个包含以下统计信息的摘要表：

| 统计信息 | 描述                                      | 统计方法                                                                                                        |
| -------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **字符数**   | 消息的总字符数                              | 计算代码块内的所有字符数。聊天消息显示为 `X / 2,000`，嵌入描述显示为 `X / 4,096` |
| **章节数**   | 由标题分隔的章节数量                          | 计算所有的 `#`, `##`, `###` 标题。如果没有标题，则显示 `0`             |
| **用户提及** | 通过 `<@USER_ID>` 或 `<@!USER_ID>` 提及的用户数量          | 计算唯一的 `<@...>` 提及模式（不包括角色提及）                   |
| **角色提及** | 通过 `<@&ROLE_ID>` 提及的角色数量                    | 计算唯一的 `<@&...>` 提及模式。包括 `@everyone` 和 `@here`           |
| **频道提及** | 通过 `<#CHANNEL_ID>` 或 `<id:...>` 提及的频道数量          | 计算唯一的 `<#...>` 和 `<id:...>` 提及模式                   |
| **链接**     | 消息中的链接数量                              | 计算原始链接和带有 `[text](url)` 格式的链接数量                 |
| **代码块**    | 含有语言信息的代码块                          | 如果消息包含代码块，列出使用的语言（例如 `javascript`, `bash`）。如果没有语言信息，则显示 `—`     |

将摘要表以紧凑的形式直接显示在代码块下方：

```
| Stat               | Value          |
|--------------------|----------------|
| Characters         | 437 / 2,000    |
| Sections           | 3              |
| User Mentions      | 1              |
| Role Mentions      | 1 (@everyone)  |
| Channel Mentions   | 0              |
| URLs               | 0              |
| Code Blocks        | —              |
```

**注意事项：**

- 对于角色提及，请在括号中注明是否包含了 `@everyone` 或 `@here`，因为这些会影响到整个服务器。
- 对于代码块，列出每种使用的语言（例如 `javascript, bash`），如果没有语言标识，则显示 `(no lang)`。
- 如果字符数超过限制（2,000 个），请添加 ⚠️ 警告。
- 如果字符数超过限制，添加 🚫 并建议拆分消息。

### 示例交互

**用户：** “给我写一条关于新 SDK 发布的 Discord 公告，并附上代码示例。”

**Claude 的回复应如下所示：**

这是您的 SDK 公告：

````markdown
# 🚀 Volvox SDK v2.0 — Breaking Changes

Hey @everyone — we just shipped **v2.0** of the SDK and there are a few things you need to know before upgrading.

## What Changed

The `createJar` method now accepts an options object instead of positional arguments:

**Before:**

```ts
const jar = createJar("Lunch Spots", ["Chipotle", "Sweetgreen"], true);
```

**After:**

```ts
const jar = createJar({
  name: "Lunch Spots",
  options: ["Chipotle", "Sweetgreen"],
  allowDuplicates: true,
});
```

## New: Shake Events

```ts
jar.on("shake", (result) => {
  console.log(`🎉 选中的选项：${result.option}`);
});
```

> 💡 Full migration guide pinned in <#dev-resources>

Drop questions in <#sdk-support> — <@core-team> is standing by. 🫡

-# v2.0.0 • <t:1770537600:D>
````

| 统计信息 | 值                |
| -------- | ------------------ |
| 字符数    | 659 / 2,000          |
| 章节数    | 3                    |
| 用户提及    | 1                    |
| 角色提及    | 1 (@everyone)        |
| 频道提及    | 2                    |
| 链接      | 0                    |
| 代码块    | 3 — `ts`, `ts`, `ts`         |

**注意：** 外层代码块使用了四个反引号 `"""`，因为消息中包含嵌套的代码块。用户复制的是代码块之间的所有内容。

---

## 快速参考

| 格式        | 语法                         | 显示效果                                      |
| -------------- | -------------------------------------- |
| 加粗        | `**text**                        | **text**                                      |
| 斜体        | `*text*` 或 `_text_`                    | _text_                                      |
| 下划线        | `__text__`                      | 下划线文本                                      |
| 删除线        | `~~text~~`                      | 被删除线的文本                                      |
| 剧透提示      | `\|\|text\|\|`                    | 点击前隐藏的文本                                      |
| 内联代码      | `` `code` ``                    | 单倍行距显示的代码                                      |
| 加粗斜体      | `***text***`                    | **_text_`                                      |
| 下划线斜体      | `__*text*__`                    | 下划线斜体                                      |
| 下划线加粗      | `__**text**__`                    | 下划线加粗文本                                      |
| 下划线加粗斜体    | `__***text***__`                    | 三种样式都支持                                    |
| 删除线加粗    | `~~**text**~~`                    | 被删除线的加粗文本                                    |

## 文本格式化

### 强调文本

```
*italic* or _italic_
**bold**
***bold italic***
__underline__
~~strikethrough~~
||spoiler text||
```

### 组合样式

外部格式标记会按照以下顺序在 Discord 中生效：下划线 → 加粗 → 斜体 → 删除线。

```
__**bold underline**__
__*italic underline*__
__***bold italic underline***__
~~**bold strikethrough**~~
~~__**bold underline strikethrough**__~~
||**bold spoiler**||
```

### 转义

在任何 Markdown 字符前加上 `\` 可以使其按原样显示：

```
\*not italic\*
\*\*not bold\*\*
\|\|not a spoiler\|\|
```

## 标题

标题需要在 **行首** 使用 `#`，后面跟着一个空格。仅支持三级标题。

```
# Large Header
## Medium Header
### Small Header
```

**重要提示：** 标题不能内联显示。`#` 必须是行的第一个字符。

## 子文本

位于内容下方的灰色小字体文本，适用于脚注、免责声明或引用。

```
-# This renders as subtext
```

## 块引用

### 单行引用

```markdown
```
> This is a single block quote
```
```

### 多行引用

`>>>` 之后的所有内容（包括后续行）都会被视为引用：

```
>>> This entire block
including this line
and this line
are all quoted
```

## 列表

### 无序列表

使用 `-` 或 `*` 加空格来创建列表。嵌套列表时也需要使用空格：

```
- Item one
- Item two
  - Nested item
  - Another nested item
    - Deep nested
```

### 有序列表

```markdown
```
1. First item
2. Second item
3. Third item
```
```

**自动编号技巧：** 如果重复使用 `1.`，Discord 会自动递增编号：

```
1. First
1. Second (renders as 2.)
1. Third (renders as 3.)
```

## 代码块

### 内联代码

```markdown
```
Use `inline code` for short snippets
```
function hello() {
  return "world";
}
```

### 语法高亮

在开头的反引号后添加语言标识：

```markdown
```
```javascript
function hello() {
  return "world";
}
```

有关支持的语言列表，请参阅 [references/syntax-highlighting.md](references/syntax-highlighting.md)。

**常用语言：** `javascript`, `typescript`, `python`, `csharp`, `json`, `bash`, `css`, `html`, `sql`, `yaml`, `diff`, `markdown`

## 链接

### 遮罩链接

```markdown
```
[Click here](https://example.com)
```
```

**注意：** 遮罩链接在嵌入内容中有效，但在普通聊天中可能会显示预览。在某些情况下，Discord 可能会抑制机器人的链接预览。

### 自动链接

Discord 会自动链接任何有效的 URL：

```
Check out https://example.com for more info
```

### 阻止链接预览

将链接用尖括号括起来，以防止 Discord 生成预览：

```
<https://example.com>
```

## 时间戳

动态时间戳会根据用户的本地时区显示。

**格式：`<t:UNIX_TIMESTAMP:FORMAT_FLAG>`

| 标识符 | 显示格式                          | 示例                                      |
| ------- | -------------------------------------- |
| `t`    | 简短时间                          | `4:20 PM`                                      |
| `T`    | 长时间                          | `4:20:30 PM`                                      |
| `d`    | 简短日期                          | `02/08/2026`                                      |
| `D`    | 长日期                          | `February 8, 2026`                                      |
| `f`    | 简短日期/时间（默认）                    | `February 8, 2026 4:20 PM`                              |
| `F`    | 长日期/时间                        | `Sunday, February 8, 2026 4:20 PM`                              |
| `R`    | 相对时间                          | `2 hours ago`                                      |

**示例：**

```
Event starts <t:1770537600:F>
That was <t:1770537600:R>
```

**提示：** 可以使用 `Math.floor(Date.now() / 1000)` 或 `date +%s` 获取当前的 Unix 时间戳。

## 提及与引用

```
<@USER_ID>          → @username mention
<@!USER_ID>         → @username mention (nickname format)
<@&ROLE_ID>         → @role mention
<#CHANNEL_ID>       → #channel link
<id:browse>         → Browse Channels link
<id:customize>      → Customize Community link
<id:guide>          → Server Guide link
<id:linked-roles>   → Linked Roles link
```

## 表情符号

```
:emoji_name:                    → Standard/custom emoji
<:emoji_name:EMOJI_ID>          → Custom emoji
<a:emoji_name:EMOJI_ID>         → Animated custom emoji
```

## Discord 特有的注意事项

1. **不支持嵌套的引用** —— Discord 不支持 `>>` 用于嵌套引用。
2. **标题需要从行首开始** —— `#` 必须是行的第一个字符（不能内联显示）。
3. **下划线不是标准 Markdown 的格式** —— 在 Discord 中使用 `__text__` 表示下划线，但在标准 Markdown 中使用 `**` 表示下划线。
4. **剧透提示是 Discord 特有的** —— `||text||` 在标准 Markdown 中没有对应格式。
5. **列表需要换行** —— 列表必须在换行后开始，否则可能无法正确显示。
6. **嵌入内容中的 Markdown 格式有所不同** —— 嵌入内容中的某些格式可能与聊天消息中的格式不同。
7. **字符数限制** —— 标准消息最多 2,000 个字符；Nitro 用户最多 4,000 个字符。
8. **嵌入描述的限制** —— 嵌入描述最多 4,096 个字符。
9. **代码块的语言名称不区分大小写** —— `JS`, `js`, `JavaScript` 等都是有效的。

## 不同场景下的格式要求

> **提醒：** 无论在什么情况下，都请将最终的格式化文本放在代码块中，以便用户可以直接复制粘贴。请参考上面的“输出格式”部分。

### 聊天消息

支持完整的 Markdown 格式。字符限制为 2,000 个（Nitro 用户为 4,000 个）。

### 嵌入描述

支持完整的 Markdown 格式。链接限制为 4,096 个字符。遮罩链接在这里可以正常使用。

### 嵌入字段值

每个字段的 Markdown 格式限制为 1,024 个字符。

### 机器人消息 / Webhook

支持完整的 Markdown 格式。与聊天消息相同，可以使用嵌入格式来增强显示效果。

### 论坛帖子

帖子正文支持完整的 Markdown 格式。标题只能是纯文本。

## 资源

- **语法高亮：** [references/syntax-highlighting.md](references/syntax-highlighting.md) —— 支持的语言列表及示例。
- **模板：** [references/templates.md](references/templates.md) —— 提供常见的 Discord 格式化模式的复制粘贴模板。