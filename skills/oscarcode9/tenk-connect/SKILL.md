---
name: tenk-connect
description: 将您的 TenK 账户连接到您的 AI 助手。记录练习会话，查看进度，并管理您从开始学习到达到 10,000 小时学习目标的整个过程。
license: MIT
metadata:
  author: OscarCode9
  version: 1.0.0
  homepage: https://github.com/OscarCode9/tenK
  requires: curl, python3
---
# TenK Connect

您可以通过AI助手来管理您的TenK账户（tenk.oventlabs.com）。该工具支持记录练习会话、查看技能学习进度、检查统计数据，并帮助您追踪达到10,000小时练习目标的进程。

## 设置

首次使用时，请运行以下命令：

    bash <SKILL_DIR>/scripts/tenk.sh auth

系统会打开一个浏览器页面，用户需要使用TenK账户的登录凭据进行身份验证。认证成功后，系统会生成一个令牌，并将其保存在`~/.config/tenk-connect/token`文件中（文件权限设置为`chmod 600`）。

## 命令

- `tenk.sh auth`         ：通过OAuth设备流程进行身份验证
- `tenk.sh whoami`        ：显示当前登录的用户
- `tenk.sh skills`        ：列出所有已学习的技能及其累计练习时间
- `tenk.sh stats`        ：显示总练习时间以及距离10,000小时的完成百分比
- `tenk.sh log <skill> <minutes>`：记录指定技能的练习会话（可选备注）
- `tenk.sh streak`        ：显示最近一次针对某技能的练习记录
- `tenk.sh logout`        ：清除保存的令牌

## 使用方法

所有操作均通过执行`<SKILL_DIR>/scripts/tenk.sh <command>`来完成。

### 身份验证

在执行任何命令之前，请先验证您的身份：

    bash <SKILL_DIR>/scripts/tenk.sh whoami

如果验证失败，请先运行`auth`命令，并向用户显示相应的登录链接和验证码。

### 记录练习会话

当用户需要记录练习时间时（例如：“记录45分钟的吉他练习”），请按照以下步骤操作：
1. 运行`tenk.sh skills`以查找对应的技能（支持名称的模糊匹配）。
2. 运行`tenk.sh log <skill> <minutes>`来记录练习会话（可选备注）。
3. 根据返回的结果确认记录是否正确。

### 查看进度

当用户询问练习进度或相关统计数据时，可以执行以下命令：
- `tenk.sh stats`：查看总练习时间
- `tenk.sh skills`：查看每个技能的详细练习时间。

## 注意事项：
- 令牌的有效期为7天，过期后需要重新进行身份验证。
- 技能匹配不区分大小写，对技能名称支持模糊匹配。
- 认证URL：`https://tenk.oventlabs.com/#/authorize/<code>`
- API基础地址：`https://tenk.oventlabs.com/api`
- 该工具依赖于`curl`和`python3`（在macOS/Linux系统中为默认安装软件）。