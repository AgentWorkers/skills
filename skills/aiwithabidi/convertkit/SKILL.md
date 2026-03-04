---
name: convertkit
description: "ConvertKit（简称“Kit”）是一款专为内容创作者设计的营销工具，通过其API可以轻松管理订阅者、表单、邮件发送流程、标签以及自动化营销活动。用户可以利用ConvertKit构建邮件列表、设置自动发送的邮件序列、发送邮件通知，并追踪订阅者的互动情况。该工具完全基于Python标准库开发，无需依赖任何第三方库或服务，非常适合用于内容创作者的电子邮件营销、新闻通讯管理、订阅者增长以及目标受众的拓展。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "✉️", "requires": {"env": ["CONVERTKIT_API_KEY"]}, "primaryEnv": "CONVERTKIT_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# ✉️ ConvertKit

ConvertKit 是一款用于创建营销自动化工具的平台，允许您通过 ConvertKit API 管理订阅者、表单、邮件发送序列、标签以及自动化流程。

## 主要功能

- **订阅者管理**：添加、标记、搜索和分组订阅者。
- **表单管理**：列出表单及其对应的订阅者。
- **邮件发送序列**：创建和管理员工邮件发送计划（即“滴灌式邮件”策略）。
- **邮件发送**：创建并发送一次性邮件。
- **标签操作**：创建、应用或移除订阅者的标签。
- **自动化规则**：查看自动化工作流程。
- **自定义字段**：管理订阅者的自定义信息。
- **订阅者搜索**：通过电子邮件或自定义属性查找订阅者。
- **数据分析**：订阅者增长情况、表单转化率、邮件发送序列的统计信息。
- **批量操作**：批量标记或取消标记多个订阅者。

## 所需参数

| 参数 | 是否必需 | 说明 |
|--------|---------|-------------------|
| `CONVERTKIT_API_KEY` | ✅ | 用于访问 ConvertKit API 的密钥/令牌 |

## 快速入门

```bash
# List subscribers
python3 {baseDir}/scripts/convertkit.py subscribers --limit 50 --sort created_at
```

```bash
# Get subscriber details
python3 {baseDir}/scripts/convertkit.py subscriber-get 12345
```

```bash
# Add a subscriber
python3 {baseDir}/scripts/convertkit.py subscriber-add --email "user@example.com" --first-name "Jane"
```

```bash
# Search by email
python3 {baseDir}/scripts/convertkit.py subscriber-search "user@example.com"
```

## 命令

### `subscribers`
列出所有订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py subscribers --limit 50 --sort created_at
```

### `subscriber-get`
获取订阅者的详细信息。
```bash
python3 {baseDir}/scripts/convertkit.py subscriber-get 12345
```

### `subscriber-add`
添加新的订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py subscriber-add --email "user@example.com" --first-name "Jane"
```

### `subscriber-search`
通过电子邮件地址搜索订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py subscriber-search "user@example.com"
```

### `tags`
列出所有的标签。
```bash
python3 {baseDir}/scripts/convertkit.py tags
```

### `tag-create`
创建一个新的标签。
```bash
python3 {baseDir}/scripts/convertkit.py tag-create "VIP Customer"
```

### `tag-apply`
将标签应用到指定的订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py tag-apply --tag 123 --email user@example.com
```

### `tag-remove`
移除订阅者的标签。
```bash
python3 {baseDir}/scripts/convertkit.py tag-remove --tag 123 --email user@example.com
```

### `forms`
列出所有的表单。
```bash
python3 {baseDir}/scripts/convertkit.py forms
```

### `form-subscribers`
列出与特定表单关联的订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py form-subscribers 456
```

### `sequences`
列出所有的邮件发送序列。
```bash
python3 {baseDir}/scripts/convertkit.py sequences
```

### `sequence-subscribers`
列出与特定邮件发送序列关联的订阅者。
```bash
python3 {baseDir}/scripts/convertkit.py sequence-subscribers 789
```

### `broadcasts`
列出所有的邮件发送任务。
```bash
python3 {baseDir}/scripts/convertkit.py broadcasts --limit 20
```

### `broadcast-create`
创建一个新的邮件发送任务。
```bash
python3 {baseDir}/scripts/convertkit.py broadcast-create '{"subject":"Weekly Update","content":"<p>Hello!</p>"}'
```

### `broadcast-send`
发送一封邮件。
```bash
python3 {baseDir}/scripts/convertkit.py broadcast-send 12345
```

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，可添加 `--human` 参数。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/convertkit.py subscribers --limit 5

# Human-readable
python3 {baseDir}/scripts/convertkit.py subscribers --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------------|
| `{baseDir}/scripts/convertkit.py` | 主要的命令行工具（CLI），用于执行所有 ConvertKit 相关操作 |

## 数据政策

本技能 **绝不将数据存储在本地**。所有请求都会直接发送到 ConvertKit API，结果会返回到标准输出（stdout）。您的数据将保存在 ConvertKit 的服务器上。

## 致谢
---
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi) 提供技术支持 |
本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)