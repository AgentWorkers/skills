# OpenClaw AI Bot — 颜色区分的选项按钮功能

## 目的
每当机器人向用户展示选项时，必须根据选项的重要性、不可逆性或差异性自动为每个按钮设置颜色。机器人绝不会发送没有颜色或样式区分的选项按钮——颜色始终是必须的。

## 核心规则
**每当机器人向用户展示两个或多个选项时，必须对每个选项进行分类并自动分配一个 `style`。这是强制性的要求。**

---

## Telegram Bot API — 按钮样式
`InlineKeyboardButton` 和 `KeyboardButton` 中有两个字段：
- **`style`**（字符串，可选）——按钮颜色：
  - *(省略)* — 默认值：蓝色。**推荐/安全/主要操作的默认颜色。**
  - `"destructive"` — 红色。**表示不可逆、危险或高风险的操作。**
  - `"secondary"` — 灰色/暗色调。**表示低优先级、可忽略或中性的操作。**

- **`icon_custom_emoji_id`**（字符串，可选）——按钮上的自定义表情符号。

---

## 自动分类规则
当机器人生成一组选项按钮时，在发送之前必须将每个选项分类为以下三个级别之一：

### 第一级别 — 默认（蓝色）：推荐的操作
适用于以下情况：
- 最安全或最常见的操作
- 肯定的确认操作（如“是”、“继续”、“接受”、“开始”）
- 机器人推荐的操作
- 用于推进流程的操作

**操作：**省略 `style` 字段（或将其设置为 `null`）。

### 第二级别 — 高风险（红色）：不可逆的操作
适用于以下情况：
- 删除、移除或永久更改某些内容
- 取消正在进行的操作（可能导致数据丢失）
- 将用户屏蔽、禁止或限制其权限
- 拒绝或否决重要的请求
- 花费金钱、代币或信用点数
- 无法轻易撤销的操作

**操作：**将 `style` 设置为 `"destructive"`。

### 第三级别 — 低优先级（灰色）：可忽略的操作
适用于以下情况：
- 跳过、忽略或推迟操作（如“稍后处理”、“现在不用”
- 表示中性的备用选项（如“返回”、“取消”）
- 显示更多信息但不会导致任何后果的操作（如“详情”、“帮助”）
- 在所有选项中优先级最低的操作

**操作：**将 `style` 设置为 `"secondary"`。

---

## 颜色对比的重要性
当选项之间的重要性不同时，颜色必须能够体现这种差异：
- **高对比度**：选项的后果差异很大：
  ```
 "Delete my account" → destructive (red)
 "Keep my account"   → default (blue)
```

- **中等对比度**：主要操作和一个备用选项：
  ```
 "Subscribe"   → default (blue)
 "Not now"     → secondary (gray)
```

- **低对比度**：选项之间的差异较小：
  ```
 "Option A" → default (blue)
 "Option B" → default (blue)
 "Skip"     → secondary (gray)
```

- **同一组中的多个级别**：
  ```
 "Confirm purchase"  → default (blue)     — recommended
 "Change amount"     → secondary (gray)   — neutral/back
 "Cancel order"      → destructive (red)  — loses progress
```

---

## 分类示例
- 机器人询问：“是否批准这份文档？”
  ```json
[
  [{"text": "✅ Approve", "callback_data": "approve"},
   {"text": "❌ Reject", "callback_data": "reject", "style": "destructive"}],
  [{"text": "⏭ Review later", "callback_data": "skip", "style": "secondary"}]
]
```

- 机器人询问：“选择一个计划？”
  ```json
[
  [{"text": "Free Plan", "callback_data": "free"},
   {"text": "Pro Plan", "callback_data": "pro"}],
  [{"text": "Compare plans", "callback_data": "compare", "style": "secondary"}]
]
```
  （所有选项均为默认颜色；需要提供额外信息的链接显示为灰色）

- 机器人询问：“是否删除此聊天中的所有消息？”
  ```json
[
  [{"text": "🗑 Delete all", "callback_data": "delete_all", "style": "destructive"}],
  [{"text": "Keep messages", "callback_data": "keep"}]
]
```
  （高风险操作显示为红色；安全操作显示为蓝色）

- 机器人询问：“是否向 @user 转移 500 个代币？”
  ```json
[
  [{"text": "Send 500 tokens", "callback_data": "send", "style": "destructive"},
   {"text": "Cancel", "callback_data": "cancel", "style": "secondary"}]
]
```
  （花费代币属于高风险操作；取消操作显示为灰色）

---

## 实现方式 — 使用 Python 自动分类器
机器人必须使用分类函数来确定按钮的样式。以下是参考实现代码：
```python
import re

# Keywords that signal each tier (case-insensitive, matched against button text + callback_data)
DESTRUCTIVE_SIGNALS = [
    r"\bdelete\b", r"\bremove\b", r"\bban\b", r"\bblock\b",
    r"\breject\b", r"\bdecline\b", r"\brevoke\b", r"\bterminate\b",
    r"\bcancel order\b", r"\bcancel subscription\b",
    r"\bunsubscribe\b", r"\bdestroy\b", r"\bpurge\b",
    r"\bspend\b", r"\btransfer\b", r"\bpay\b", r"\bsend.*tokens?\b",
    r"\breset\b", r"\bclear all\b", r"\bwipe\b",
    r"\bleave\b", r"\bquit\b", r"\bdisconnect\b",
]

SECONDARY_SIGNALS = [
    r"\bskip\b", r"\bnot now\b", r"\bmaybe later\b", r"\blater\b",
    r"\bback\b", r"\bdismiss\b", r"\bclose\b",
    r"\bdetails\b", r"\bmore info\b", r"\bhelp\b", r"\babout\b",
    r"\bno thanks\b", r"\bnevermind\b",
    r"\bcancel$",  # plain "cancel" (no lost work) = secondary, not destructive
]


def classify_button_style(text: str, callback_data: str = "", context_hint: str = "") -> str | None:
    """
    Automatically determine the button style based on its text and context.

    Returns:
        "destructive" — red button (irreversible / high-stakes)
        "secondary"   — gray button (low-priority / dismiss)
        None          — default blue button (primary / recommended)

    context_hint: optional extra context like "this action costs money"
    """
    combined = f"{text} {callback_data} {context_hint}".lower()

    # Check destructive first (higher priority)
    for pattern in DESTRUCTIVE_SIGNALS:
        if re.search(pattern, combined):
            return "destructive"

    # Then secondary
    for pattern in SECONDARY_SIGNALS:
        if re.search(pattern, combined):
            return "secondary"

    # Default = primary (blue)
    return None


def build_choice_buttons(choices: list[dict]) -> list[list[dict]]:
    """
    Takes a list of raw choices and returns Bot API inline_keyboard rows
    with styles automatically assigned.

    Each choice dict:
        text (str):          Button label (required)
        data (str):          callback_data (required unless url is set)
        url (str):           URL button (optional, mutually exclusive with data)
        style (str|None):    Override style — if set, skip auto-classification
        context (str):       Extra hint for classifier (e.g. "costs money")
        emoji_id (str):      Custom emoji ID (optional)
        row (int):           Force button into a specific row (optional)

    Returns list of rows suitable for inline_keyboard.
    """
    # Group by row
    row_map: dict[int, list[dict]] = {}
    auto_row = 0
    for i, choice in enumerate(choices):
        btn: dict = {"text": choice["text"]}

        # Action
        if "url" in choice:
            btn["url"] = choice["url"]
        else:
            btn["callback_data"] = choice.get("data", choice["text"].lower().replace(" ", "_"))

        # Style — use override if provided, else auto-classify
        if "style" in choice and choice["style"] is not None:
            btn["style"] = choice["style"]
        else:
            auto_style = classify_button_style(
                choice["text"],
                choice.get("data", ""),
                choice.get("context", ""),
            )
            if auto_style:
                btn["style"] = auto_style

        # Custom emoji
        if "emoji_id" in choice:
            btn["icon_custom_emoji_id"] = choice["emoji_id"]

        # Row assignment
        target_row = choice.get("row", auto_row)
        row_map.setdefault(target_row, []).append(btn)

        # Auto-advance row every 2 buttons
        if len(row_map.get(auto_row, [])) >= 2:
            auto_row += 1

    return [row_map[k] for k in sorted(row_map.keys())]
```

### 在机器人中使用分类器：
```python
import requests

def send_choices(bot_token, chat_id, text, choices, parse_mode="HTML"):
    """Send a message with auto-colored choice buttons."""
    keyboard = build_choice_buttons(choices)
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": keyboard},
    }
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

# The bot just passes raw choices — colors are assigned automatically:
send_choices(TOKEN, chat_id, "Approve this document?", [
    {"text": "✅ Approve", "data": "approve"},
    {"text": "❌ Reject", "data": "reject"},          # auto → destructive (red)
    {"text": "⏭ Review later", "data": "later"},       # auto → secondary (gray)
])
```

---

## 使用 python-telegram-bot 库
> 如果该库版本尚未提供 `style` 参数，可以通过 `api_kwargs` 传递该参数。
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def auto_button(text, callback_data, context=""):
    style = classify_button_style(text, callback_data, context)
    kwargs = {"style": style} if style else {}
    return InlineKeyboardButton(text, callback_data=callback_data, api_kwargs=kwargs)

keyboard = InlineKeyboardMarkup([
    [auto_button("Approve", "approve"),
     auto_button("Reject", "reject")],
    [auto_button("Skip", "skip")],
])
await update.message.reply_text("Pick an option:", reply_markup=keyboard)
```

---

## 回复界面 — 同样适用这些规则
回复界面的按钮样式也遵循相同的规则。
```json
{
  "chat_id": "<CHAT_ID>",
  "text": "Delete your data?",
  "reply_markup": {
    "keyboard": [
      [
        {"text": "Keep my data"},
        {"text": "Delete everything", "style": "destructive"}
      ]
    ],
    "resize_keyboard": true,
    "one_time_keyboard": true
  }
}
```

---

## 按钮上的自定义表情符号
可以在按钮上同时使用 `style` 和自定义表情符号：
```json
{"text": "Boost", "callback_data": "boost", "style": "destructive", "icon_custom_emoji_id": "5368324170671202286"}
```

---

## 测试示例
以下是一个快速测试，展示了带有颜色区分的按钮效果：
```bash
./SKILL.sh <BOT_TOKEN> <CHAT_ID>
```

---

## 参考资料
- Telegram Bot API：https://core.telegram.org/bots/api
- Bot API 更新日志：https://coreTelegram.org/bots/api-changelog
- Telegram 博客文章：https://telegram.org/blog/crafting-android-design-and-more