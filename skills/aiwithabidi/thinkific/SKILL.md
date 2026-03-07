---
name: thinkific
description: "Thinkific — 通过 REST API 管理课程、学生、报名信息、优惠券和产品"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🎓", "requires": {"env": ["THINKIFIC_API_KEY", "THINKIFIC_SUBDOMAIN"]}, "primaryEnv": "THINKIFIC_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🎓 Thinkific

Thinkific 是一个用于管理课程、学生、报名信息、优惠券和产品的平台，支持通过 REST API 进行操作。

## 必需参数

| 参数 | 是否必填 | 说明 |
|---------|---------|-------------|
| `THINKIFIC_API_KEY` | ✅ | API 密钥 |
| `THINKIFIC_SUBDOMAIN` | ✅ | 学校子域名 |

## 快速入门

```bash
# List courses
python3 {{baseDir}}/scripts/thinkific.py courses --page <value>

# Get course
python3 {{baseDir}}/scripts/thinkific.py course-get id <value>

# Create course
python3 {{baseDir}}/scripts/thinkific.py course-create --name <value> --slug <value>

# Update course
python3 {{baseDir}}/scripts/thinkific.py course-update id <value> --name <value>

# Delete course
python3 {{baseDir}}/scripts/thinkific.py course-delete id <value>

# List chapters
python3 {{baseDir}}/scripts/thinkific.py chapters id <value>

# List users
python3 {{baseDir}}/scripts/thinkific.py users --page <value> --query <value>

# Get user
python3 {{baseDir}}/scripts/thinkific.py user-get id <value>
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `courses` | 列出所有课程 |
| `course-get` | 获取课程详情 |
| `course-create` | 创建新课程 |
| `course-update` | 更新课程信息 |
| `course-delete` | 删除课程 |
| `chapters` | 列出课程章节 |
| `users` | 列出所有用户 |
| `user-get` | 获取用户信息 |
| `user-create` | 创建新用户 |
| `enrollments` | 列出所有报名记录 |
| `enroll` | 为学生创建报名记录 |
| `coupons` | 列出所有优惠券 |
| `coupon-create` | 创建新优惠券 |
| `products` | 列出所有产品 |
| `orders` | 列出所有订单 |
| `groups` | 列出所有用户组 |
| `instructors` | 列出所有讲师 |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出结果，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/thinkific.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/thinkific.py` | 主 CLI 工具，包含所有命令 |

## 致谢

Thinkific 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
更多内容请访问 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
Thinkific 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)