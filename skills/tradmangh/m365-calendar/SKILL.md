---
name: m365-calendar
description: 通过 Microsoft Graph 实现 Microsoft 365 日历自动化功能，适用于 M365 Business（企业/学校版）和 M365 Home/Consumer（hotmail.com/outlook.com）用户。该功能可用于查看即将发生的事件、搜索日历条目（例如“午餐”）、检查参与者的回复状态（已接受/拒绝/待定）、创建或更新会议、将事件移至新的时间，以及解决与日历访问相关的 Graph/MSAL 认证/令牌缓存问题。支持通过设备代码流进行委托认证，并将每个用户的令牌缓存存储在本地。**令牌费用：**每次使用约 600 至 1500 个令牌（技能实现部分约需 2000 至 3000 个令牌，包括 Graph 调用及简单的数据解析）。
---
# M365 日历（Microsoft Graph）

建议将此技能的实现简化为使用内置脚本来完成核心功能。

## 安全性/使用限制

- **严禁**提交或共享令牌缓存或客户端密钥。
- **默认的密钥存储位置（每台机器）：`~/.openclaw/secrets/m365-calendar/`**

## 快速入门

1) **身份验证**（选择相应的配置文件/租户类型）：

```bash
# Business / work accounts
node skills/m365-calendar/scripts/auth-devicecode.mjs --profile business --tenant organizations --email you@company.com

# Consumer / home accounts (hotmail.com / outlook.com)
node skills/m365-calendar/scripts/auth-devicecode.mjs --profile home --tenant consumers --email you@outlook.com
```

2) **列出今日剩余的事件（欧洲/维也纳地区）**：

```bash
node skills/m365-calendar/scripts/list.mjs --profile tom-business --when today --tz Europe/Vienna
```

3) **搜索并显示与会者的回复**：

```bash
node skills/m365-calendar/scripts/search.mjs --profile tom-business --query "Mittagessen" --when tomorrow --tz Europe/Vienna
node skills/m365-calendar/scripts/get-event.mjs --profile tom-business --id <EVENT_ID> --tz Europe/Vienna
```

4) **将事件时间进行调整**：

```bash
node skills/m365-calendar/scripts/move-event.mjs --profile tom-business --id <EVENT_ID> \
  --start "2026-02-19T12:30" --end "2026-02-19T13:00" --tz Europe/Vienna
```

## 推荐的操作流程

当用户请求更改会议信息时，请按照以下步骤操作：

1) **准确识别目标事件**（通过日期范围和主题进行搜索，并确认事件ID）。
2) **读取事件详情并查看与会者的回复状态**。
3) **修改事件的开始/结束时间**。
4) **重新读取事件信息，并确认最终的事件开始/结束时间以及任何需要重置的回复状态**。

## 关于工作账户与个人账户（消费者账户）的注意事项

- 对于工作或学校账户（大多数“企业”租户），请使用 `--tenant organizations` 参数。
- 对于 hotmail/outlook.com 个人账户，请使用 `--tenant consumers` 参数。
- 如果希望使用一个通用配置文件来登录这两种类型的账户，请使用 `--tenant common` 参数。

**重要提示：** 使用 MSA（Microsoft Account Services）登录时，需要先进行应用注册，以允许使用个人 Microsoft 账户。

如果在个人账户使用设备代码进行登录时出现 `invalid_grant` 错误，请使用带有 `--clientId` 参数的命令重新执行身份验证。该参数应指向已配置为允许访问“任何组织目录中的账户和个人 Microsoft 账户”的应用程序。

如果自动获取令牌失败，请重新运行 `auth-devicecode.mjs` 脚本来处理该配置文件的问题。