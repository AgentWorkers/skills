---
name: feishu-contacts
description: 将 Feishu（Lark）中的联系人信息同步到 USER.md 文件中，以便代理能够根据名称识别私信发送者。此操作适用于设置 Feishu 身份识别功能、在人力资源信息更新后更新联系人信息，或配置多用户代理访问权限时使用。Feishu 的私信仅包含 `open_id`（不包含发送者名称），因此该脚本会在 USER.md 文件中直接嵌入一个 `open_id` 到 `name` 的映射表，以实现无需额外工具即可进行身份识别的功能。
---
# Feishu联系人同步

## 问题

Feishu（Lark）的私信（DM）仅包含发送者的`open_id`，而不包含姓名。群组消息中包含包含姓名的`Sender metadata`，但私信中不包含。如果没有查询表，代理程序可能会：
- 假设所有私信都来自`USER.md`文件中记录的用户（这是错误的）；
- 完全无法识别发送者的身份。

## 解决方案

将完整的联系人信息直接嵌入到`USER.md`文件中。由于工作区文件在网关启动时会被注入到系统提示中，代理程序可以直接将传入的元数据中的`open_id`与联系人表进行匹配，无需任何额外的工具调用。

## 重要提示：`open_id`是针对每个应用程序的

Feishu的`open_id`是针对每个应用程序进行区分的。同一个用户在不同Feishu应用程序中可能拥有不同的`open_id`。因此，每个使用不同Feishu应用程序的OpenClaw实例**必须使用自己的应用程序凭证来获取联系人信息**。

## 设置步骤

### 1. 确保Feishu应用程序具有联系人访问权限

应用程序需要具有`contact:user.employee_id:readonly`或`contact:user.base:readonly`的权限，才能通过联系人API列出用户信息。

### 2. 运行同步脚本

```bash
python3 scripts/sync_feishu_contacts.py <openclaw_config_path> <feishu_account_name> <user_md_path>
```

**示例：**
```bash
python3 scripts/sync_feishu_contacts.py ~/.openclaw/openclaw.json my_app ~/workspace/USER.md
```

**参数：**
- `openclaw_config_path`：`openclaw.json`文件的路径（其中包含Feishu应用程序的凭证信息）
- `feishu_account_name`：配置文件中`channels.feishu.accounts`下的账户名称
- `user_md_path`：`USER.md`文件的路径

### 3. `USER.md`文件的格式

脚本要求`USER.md`文件中包含以下格式的联系人信息部分：

```markdown
## 飞书通讯录 (App Name)
飞书 DM 不携带发送者姓名。用 inbound metadata 的 chat_id（格式 `user:ou_xxx`）匹配下表识别发送者。
| 姓名 | open_id |
|------|---------|
| Alice | ou_abc123 |
| Bob | ou_def456 |
```

**首次运行时：**
如果`USER.md`文件中不存在联系人信息部分，请手动添加该部分的标题和描述行，然后运行脚本以填充联系人表。

### 4. 在`AGENTS.md`文件中添加发送者身份信息

将以下内容添加到应用程序的启动序列中：

```
识别消息发送者（必须执行）：飞书 DM 不携带发送者姓名，只有 open_id（inbound metadata 的 chat_id 格式 `user:ou_xxx`）。提取 open_id，在 USER.md 的飞书通讯录表格中匹配找到姓名。不要假设 DM 对方就是主人——任何人都可能给你发私聊。群聊消息自带 Sender metadata 可直接使用。
```

### 5. 设置定期同步（可选）

添加一个系统定时任务（例如每周一早上7点）来更新联系人信息：

```bash
0 7 * * 1 python3 /path/to/scripts/sync_feishu_contacts.py ~/.openclaw/openclaw.json my_app ~/workspace/USER.md
```

**注意：**同步更新`USER.md`文件后，需要重启网关才能使更改生效（因为工作区文件在网关启动时会被缓存）。

## 多用户使用原则

`USER.md`文件应明确说明：
- 谁是“主要联系人”（即负责管理联系人信息的用户）；
- 代理程序服务于多个用户，因此不能自动假设私信发送者的身份；
- 应该按照用户的实际姓名来称呼他们。

## 隐私保护

- 联系人表中仅包含姓名和`open_id`（不包含电子邮件、电话号码或其他个人身份信息）；
- `open_id`是一个仅在特定Feishu应用程序内有效的标识符；
- 同步脚本会从`openclaw.json`文件中读取应用程序凭证，但不会将其显示出来。