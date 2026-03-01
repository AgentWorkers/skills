---
name: blocker-min-input
description: 当用户被阻止（即无法访问某些功能或资源）时，应报告具体的阻止原因、已经尝试过的解决方法，以及用户需要提供的最小限度的信息（如用户名、密码等）。这样就可以快速解除阻止，避免不必要的来回沟通。
---
# 阻碍因素的最低输入要求

当遇到阻碍时，需要提供所有必要的信息以便快速解除阻碍。避免来回沟通。

## 问题

代理通常会：
- 仅简单地说“被阻塞了”，而不提供具体原因；
- 不报告尝试过的解决方法；
- 提出模糊的问题；
- 需要多次澄清。

## 工作流程

### 1. 阻碍因素的报告格式

```markdown
**Blocker**: Exact error/blocker text
**Attempts Made**: 
- Attempt 1: what + result
- Attempt 2: what + result
**Minimum Unblock Input**: Smallest user action needed
**Fallback Option**: Alternative if user cannot unblock
```

### 2. 尝试解决方法

在报告阻碍之前：
- 用正确的参数重新尝试相同的方法（至少一次）；
- 尝试一个备用方案；
- 如果两种方法都失败，则提供相关证据进行报告。

### 3. 最低输入要求示例

| 阻碍因素 | 最低输入信息 |
|---------|---------------|
| 缺少API密钥 | `Run: openclaw configure --section web` |
| 权限被拒绝 | `Grant write access to: D:\folder` 或 `Use fallback: C:\workspace\folder` |
| 身份验证失败 | `Check token in: openclaw.json` |

## 可执行操作的完成标准

| 标准 | 验证方式 |
|----------|-------------|
| 阻碍因素的文字描述与实际错误信息一致 | 逐字引用错误信息 |
- 记录了至少两次尝试 |
- 提供了具体的操作或命令 |
- 提供了备用方案 |

## 隐私/安全要求

- 报告中不得包含任何凭据信息；
- 从错误信息中删除令牌/密钥；
- 在处理敏感信息时使用通用路径。

## 自动触发条件

在以下情况下使用该流程：
- 任何工具调用失败两次；
- 需要用户输入才能继续操作；
- 检测到权限/认证问题。

---

**一份报告，一条输入信息，快速解除阻碍。**