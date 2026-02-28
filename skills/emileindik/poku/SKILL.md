---
name: poku
description: >
 
Makes outbound phone calls on the user's behalf using the Poku API via the `exec` tool.
  Use when the user wants to call a restaurant, business, doctor's office, or
  any phone number to handle errands such as reservations, appointments,
  reminders, follow-ups, or bill disputes. Do not use for sending SMS, email,
  or looking up contact information only. Do not use if no phone number or
  business name is provided.
requires:
  env:
    - POKU_API_KEY
---

# Poku — 外拨电话

## 第1步：解析电话号码

- **原始号码**（例如 `917-257-7580`）——去除格式化信息，并在前面加上 +1（美国默认前缀）。结果：`+19172577580`。
- **个人联系姓名**——直接询问用户电话号码，不要猜测。
- **仅企业名称**——使用搜索工具查找电话号码，然后在继续操作前与用户确认。

此步骤的结果是<标准化后的电话号码>，该号码将用于第4步。

---

## 第2步：收集详细信息并确认意图

请阅读 `references/EXAMPLES.md`。每个模板都明确列出了该类型电话所需的具体信息。使用相应的模板来确定缺少哪些信息，然后仅向用户询问这些信息。

如果没有任何模板适用于该类型的电话，请询问用户：具体目的、所需的名称或参考编号。

根据实际情况推断合理的默认值，并告知用户。不要重复询问已经提供的信息。

在进入第3步之前，必须向用户说明计划并获得用户的确认。

> “我打算拨打 [号码]，联系 [地点]，目的是 [目的]。我会说明我是代表 [用户姓名] 打电话的。如果没有人接听，我会留言：[留言内容]。可以继续吗？如果可以，我稍后会去拨打电话。”

**在此阶段，收集任何可能有助于通话的额外信息（例如地址、保险信息、参考编号）。**

---

## 第3步：起草通话提示信息

如果 `references/EXAMPLES.md` 中有适用于该类型电话的模板，请使用该模板，并将所有占位符替换为实际值。切勿留下未填写的占位符。

如果没有合适的模板，请按照以下结构起草通话提示信息：
1. **身份**——代理的身份以及他们代表谁打电话。
2. **目的**——具体的通话目的，以及针对不同可能回答情况的应对策略。
3. **留言内容**——如果无人接听时应留下的具体留言。

---

## 第4步：拨打电话

使用 `exec` 工具执行 `curl` 命令来拨打电话（始终设置 `background: false`，并明确将 `yieldMs` 设置为 300000）。

```bash
curl -s -X POST \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "<drafted message from Step 3>", "to": "<normalized number>"}' \
  https://api.pokulabs.com/phone/call
```

在请求未完成期间切勿重试——通话可能会持续长达5分钟。如果 `POKU_API_KEY` 未设置，请停止操作并告知用户。有关错误代码，请参阅 `references/API.md`。

---

## 第5步：报告结果

一旦工具返回“响应”，立即通知用户。例如：“我刚刚完成了通话。我与 Kristin 联系过了，她已经确认了明天晚上7点的预约。”
首先报告重要的信息：确认的日期/时间、联系人姓名、参考编号以及后续步骤。如果响应中包含“无人接听”，请立即停止工具操作并报告情况。遇到任何错误时，直接报告原始留言内容，切勿重试。

---

## 参考资料

- `references/EXAMPLES.md`——每种电话类型的模板；请在第2步阅读。
- `references/API.md`——完整的参数参考信息和错误代码；如有需要，请在第4步查阅。