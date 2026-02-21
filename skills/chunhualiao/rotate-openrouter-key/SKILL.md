---
name: rotate-openrouter-key
description: >
  **安全地轮换 OpenClaw 安装中所有配置文件中的 OpenRouter API 密钥**  
  该脚本会查找所有存储 API 密钥的位置，更新这些密钥，然后重启网关，并验证新密钥是否能够正常使用。适用于需要执行以下操作的场景：  
  - “轮换 OpenRouter 密钥”  
  - “更改 OpenRouter API 密钥”  
  - “更新 OpenRouter 密钥”  
  - “替换 OpenRouter 密钥”
---
# 旋转 OpenRouter 密钥

安全地更换整个 OpenClaw 系统中的 OpenRouter API 密钥，同时处理所有配置文件、优先级链以及验证过程。

## 使用场景

- 用户请求“旋转我的 OpenRouter 密钥”或“更改 OpenRouter 密钥”
- 用户收到来自 OpenRouter 的 401 错误
- 用户禁用了旧密钥并需要设置新密钥
- 为提高安全性而定期旋转密钥

## 密钥优先级链

OpenClaw 从三个来源读取 OpenRouter API 密钥，优先级从高到低依次为：

1. **`~/.openclaw/.env`** — 环境文件，具有最高优先级，会覆盖其他设置
2. **`~/.openclaw/agents/<name>/agent/models.json`** — 每个代理的配置文件
3. **`~/.openclaw/openclaw.json`** — 全局配置文件

如果较高优先级的来源中仍然使用旧密钥，更新较低优先级的文件将无效。**必须更新实际被读取到的密钥所在的位置。**

## 工作流程

### 第一步：获取新密钥

向用户索取新密钥。新密钥必须以 `sk-or-v1-` 开头。

如果用户尚未生成新密钥，请引导他们访问 [openrouter.ai/keys](https://openrouter.ai/keys) 生成新密钥。

### 第二步：查找所有密钥所在的位置

```bash
# Find every file containing an OpenRouter key
grep -r "sk-or-v1" ~/.openclaw/ --include="*.json" --include=".env" -l 2>/dev/null

# Also check for uncommented key in .env
grep -v '^#' ~/.openclaw/.env 2>/dev/null | grep OPENROUTER_API_KEY
```

在开始修改之前，向用户报告找到的所有密钥位置。

### 第三步：更新所有位置并验证

运行辅助脚本——该脚本会一次性更新 `.env` 和 JSON 文件：

```bash
python3 scripts/update-openrouter-key.py --key "sk-or-v1-NEW-KEY" --verify
```

脚本功能包括：
- 查找所有包含 OpenRouter 密钥的配置文件（`.env` 和 JSON 文件）
- 在每次写入前创建带有时间戳的备份
- 仅更新密钥值（最小化修改范围）
- 在 OpenRouter API 中验证新密钥的有效性
- 报告更新的内容

使用 `--dry-run` 选项先进行预览：
```bash
python3 scripts/update-openrouter-key.py --key "sk-or-v1-NEW-KEY" --dry-run
```

### 第四步：重启网关

```bash
openclaw gateway restart
```

### 第五步：远程主机（如适用）

如果用户需要在其他机器上管理 OpenClaw，请通过 SSH 重复执行第 2-5 步骤：

```bash
ssh <host> "grep -r 'sk-or-v1' ~/.openclaw/ --include='*.json' --include='.env' -l"
```

然后远程运行更新脚本或将其复制到目标主机。

### 第六步：禁用旧密钥

**只有在确认新密钥在所有地方都生效后**，才可指导用户在 [openrouter.ai/keys](https://openrouter.ai/keys) 上安全地禁用或删除旧密钥。

## 范围与限制

**功能范围：** 在所有 OpenClaw 配置位置中查找、更新和验证 OpenRouter API 密钥。

**不涉及的功能：** 其他提供商的密钥（如 Anthropic、OpenAI）；密钥的生成（用户需在 openrouter.ai 上完成）；计费或使用相关问题。

## 错误处理

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| 更新后出现 401 错误 | 未找到某个配置文件 | 重新执行第 2 步以查找剩余的旧密钥 |
| 在 curl 中可以使用新密钥，但在机器人中无法使用 | `.env` 文件中的旧密钥覆盖了 JSON 文件中的密钥 | 检查并更新 `.env` 文件 |
| 网关无法重启 | 与其他问题相关 | 使用 `openclaw gateway stop && openclaw gateway start` 命令重启网关 |
| 远程主机仍然无法正常工作 | 忘记更新远程配置 | 通过 SSH 连接到远程主机并重复执行第 2-5 步骤 |

## 限制条件

- 无法生成或撤销密钥（用户需在 openrouter.ai 上完成这些操作）
- 无法在没有 SSH 访问权限的远程主机上更新密钥
- 不支持存储在 `~/.openclaw/` 之外的密钥（例如，在 systemd 环境文件中的密钥）