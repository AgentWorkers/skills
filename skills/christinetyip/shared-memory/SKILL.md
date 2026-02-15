---
name: shared-memory
description: 与其他用户分享记忆和状态。适用于用户希望分享知识、创建用户/组、授予权限、设置家庭或团队共享功能、订阅记忆变更，或管理其记忆知识库的访问控制时。此共享记忆功能依赖于 Ensue——一个专为代理设计的共享记忆网络。
metadata:
  clawdbot:
    emoji: "🤝"
    requires:
      env:
        - ENSUE_API_KEY
    primaryEnv: ENSUE_API_KEY
    homepage: https://ensue-network.ai
---

# 共享内存

将您知识库中的内容与其他用户共享。同时，您可以管理用户、组以及命名空间上的细粒度权限设置。

## 快速入门

```bash
# Create user and group
{baseDir}/scripts/shared-memory.sh create-user mark
{baseDir}/scripts/shared-memory.sh create-group family
{baseDir}/scripts/shared-memory.sh add-member family mark

# Grant access
{baseDir}/scripts/shared-memory.sh grant group family read christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family update christine/shared/
```

## 命名空间组织

```
<username>/
├── private/    # Only this user
├── shared/     # Shared with others
└── public/     # Read-only to others
```

- 授予 `mark/shared/` 的访问权限 → 访问所有共享内容
- 授予 `mark/shared/recipes/` 的访问权限 → 仅访问食谱相关内容

## 命令

### 用户
| 命令 | 描述 |
|---------|-------------|
| `create-user <username>` | 创建用户 |
| `delete-user <username>` | 删除用户 |

### 组
| 命令 | 描述 |
|---------|-------------|
| `create-group <name>` | 创建组 |
| `delete-group <name>` | 删除组 |
| `add-member <group> <user>` | 将用户添加到组 |
| `remove-member <group> <user>` | 从组中移除用户 |

### 权限
| 命令 | 描述 |
|---------|-------------|
| `grant org <action> <pattern>` | 授予某个组织相应的权限 |
| `grant user <name> <action> <pattern>` | 授予某个用户相应的权限 |
| `grant group <name> <action> <pattern>` | 授予某个组相应的权限 |
| `revoke <grant_id>` | 撤销权限 |
| `list` | 列出所有权限设置 |
| `list-permissions` | 列出当前有效的权限 |

**权限操作类型**：`read`（读取）、`create`（创建）、`update`（更新）、`delete`（删除）

### 订阅
| 命令 | 描述 |
|---------|-------------|
| `subscribe <key>` | 在内容发生变化时接收通知 |
| `unsubscribe <key>` | 停止接收通知 |
| `list-subscriptions` | 查看所有订阅设置 |

## 示例：家庭共享

```bash
# Create user for partner
{baseDir}/scripts/shared-memory.sh create-user mark

# Create family group
{baseDir}/scripts/shared-memory.sh create-group family
{baseDir}/scripts/shared-memory.sh add-member family mark

# Grant mutual access to shared/ namespaces
{baseDir}/scripts/shared-memory.sh grant group family read christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family create christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family update christine/shared/
{baseDir}/scripts/shared-memory.sh grant group family read mark/shared/
{baseDir}/scripts/shared-memory.sh grant group family update mark/shared/
```

## 故障排除

如果命令执行失败，请首先检查是否已配置 Ensue API 密钥：

```bash
echo $ENSUE_API_KEY
grep -A2 'ensue-learning-memory' ~/.clawdbot/clawdbot.json
```

如果未找到 API 密钥，请告知用户前往 https://www.ensue-network.ai/login 获取免费密钥，并将其配置到 `~/.clawdbot/clawdbot.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "ensue-learning-memory": {
        "apiKey": "their-api-key-here"
      }
    }
  }
}
```

如果密钥存在但命令仍然失败，可能是密钥无效——请让用户重新生成一个有效的密钥。