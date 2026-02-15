---
name: moodle-ws
description: >
  **使用 REST Web 服务与 Moodle 4.x 集成**  
  当用户请求创建课程、注册/取消用户注册、创建或更新教学活动（如测验、作业、论坛），发送评分，或在启用了 REST Web 服务的 Moodle 网络环境中列出课程/学生信息时，可使用此技能。
---
# Moodle Web Services (REST) – 技能

## 1. 背景与要求

此技能用于通过 **Web Services (REST)** 来操作 **Moodle 4.x**。

主要功能包括：

- 创建课程
- 注册/取消用户注册
- 创建/更新教学活动：
  - 测验（问卷）
  - 作业（任务）
  - 论坛
- 发送评分
- 获取课程和学生列表

要求：

- Moodle 的基础 URL（例如：`https://moodle.ejemplo.com`）
- 具有适当权限的 Web Service 令牌（角色需具备以下权限：
  - 创建课程
  - 管理学生注册
  - 管理教学活动
  - 管理评分

**重要提示：**切勿将令牌保存在聊天记录中。请让用户将其配置在本地文件或环境变量中。

建议将令牌保存在非版本化的配置文件中，例如：

```bash
~/.openclaw/workspace/secrets/moodle-ws.json
```

## 7. 作者与使用说明

**moodle-ws** 技能由 **Exe Andino** 设计。

该技能适用于以下场景：

- 将 Moodle 4.x 与 OpenClaw 助手集成
- 自动化教师的教学和管理任务（如创建课程、管理学生注册、安排教学活动、记录评分）

建议遵循以下原则：

- 为这种集成使用专用的 Web Service 令牌
- 不要对 URL 和令牌的配置进行版本控制或公开
- 在生产环境使用前，先在测试环境中进行充分测试。