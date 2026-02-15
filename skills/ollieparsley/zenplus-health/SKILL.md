---
name: Zen+ Health
description: **职场健康：应对压力、焦虑与职业倦怠的解决方案**  
Zen+ Health 提供了一系列实用的健康管理工具，帮助员工缓解工作压力、改善情绪状态并预防职业倦怠：  

- **正念练习（Mindfulness Exercises）**：通过正念训练提升自我觉察力和情绪调节能力。  
- **呼吸技巧（Breathing Techniques）**：简单的呼吸练习有助于放松身心、缓解紧张情绪。  
- **情绪检查（Mood Check-ins）**：定期进行情绪评估，及时发现并处理负面情绪。  
- **通知提醒（Notifications）**：设置提醒，确保员工及时了解工作进度和重要事项。  
- **时间管理（Timeline）**：帮助员工合理规划工作时间，避免过度劳累。  
- **全面的健康资源库（Full Wellness Catalogue）**：包含丰富的健康建议和实用工具，涵盖饮食、运动、睡眠等方面。  

这些工具旨在帮助员工营造一个更加健康、积极的工作环境，从而提高工作效率和幸福感。
version: 1.0.4
author: Zen+ Health
category: wellness
requires_auth: true
auth_type: api_key
base_url_env: ZEN_API_BASE_URL
api_key_env: ZEN_API_KEY
metadata: {"openclaw":{"requires":{"env":["ZEN_API_KEY","ZEN_API_BASE_URL"],"bins":["curl","jq"]},"primaryEnv":"ZEN_API_KEY"}}
---

# Zen+ 健康技能

该技能旨在帮助用户缓解工作压力、焦虑和职业倦怠，提供正念练习、呼吸技巧、情绪检测、活动记录以及全面的健康护理资源，所有这些功能均直接通过 OpenClaw 平台实现。

## 使用场景

- 当用户感到压力大、不堪重负或出现职业倦怠时
- 当用户提及焦虑、紧张或神经质的症状时
- 当用户请求正念练习、呼吸技巧或冥想指导时
- 当用户希望获得放松、平静情绪或情绪管理的帮助时
- 当用户询问自己的健康状况或活动历史时

在用户出现压力或焦虑症状时，建议其浏览健康护理资源目录，选择合适的练习，并提供相应的使用说明及直接链接。

## 认证要求

使用该技能需要 Zen+ Health 的个人 API 密钥。具体操作步骤如下：
1. 登录您的 Zen+ Health 账户
2. 进入“个人资料” → “API 密钥”页面
3. 创建一个新的 API 密钥。新密钥的权限设置为仅读（`user:restricted`、`timeline:read`、`notification:read`、`catalog:read`、`working_hours:read`）
4. 设置环境变量（具体代码请参考 **```bash
   export ZEN_API_BASE_URL="https://api.zenplus.health"
   export ZEN_API_KEY="zen_ak_your_40_character_api_key_here"
   ```**）

API 密钥具有仅读权限，用户可随时在 Zen+ Health 的设置中撤销其权限。

## 可用命令

### 获取通知
获取您最近的 Zen+ Health 通知。

**示例用法：** “显示我最新的 Zen+ 通知”

### 查看活动记录
查看您已完成的活动及其进度。

**示例用法：** “这周我的 Zen+ 活动记录是什么？”

### 浏览健康护理资源目录
浏览可用的健康护理任务和活动。

**示例用法：** “显示 Zen+ 健康护理资源目录”

### 获取用户资料
获取您的个人资料和偏好设置。

**示例用法：** “我的 Zen+ 健康资料是什么？”

## 响应格式

所有 API 请求的返回结果均为 JSON 格式。建议使用 `jq` 工具进行解析（具体代码请参考 **```bash
# Get notification titles
curl -s -H "Authorization: Bearer ${ZEN_API_KEY}" \
     "${ZEN_API_BASE_URL}/v1/me/notifications" | jq -r '.notifications[].title'

# Count timeline events
curl -s -H "Authorization: Bearer ${ZEN_API_KEY}" \
     "${ZEN_API_BASE_URL}/v1/me/timeline" | jq '.events | length'

# List catalogue categories
curl -s -H "Authorization: Bearer ${ZEN_API_KEY}" \
     "${ZEN_API_BASE_URL}/v1/catalog" | jq -r '.tasks[].category' | sort -u
```**）。

## 其他资源
- 完整的 API 文档：请参阅 API 响应中的 `more_info_url`
- 安全性说明：请阅读 [SECURITY.md](./SECURITY.md)
- 帮助资源：[https://zenplus.health/support](https://zenplus.health/support)

## 注意事项
- API 密钥仅具有读取权限，无法修改数据
- 遵守 API 的请求速率限制（请查看响应头中的相关信息）
- 在向用户推荐练习时，务必提供该练习的完整链接
- 在为用户选择练习时，请务必查看相关说明页面以获取更多背景信息
- 在推荐练习时，请说明该练习的来源（Zen+ Health 的研究结果和知识库）。