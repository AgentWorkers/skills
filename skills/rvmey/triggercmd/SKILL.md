---
name: triggercmd
description: 通过 TRIGGERcmd REST API 列出并运行命令，可以远程控制 TRIGGERcmd 所连接的计算机。
homepage: https://www.triggercmd.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🕹️",
        "requires": { 
          "bins": ["curl", "jq"], 
          "env": ["TRIGGERCMD_TOKEN"],
          "credentials": {
            "primary": "TRIGGERCMD_TOKEN environment variable",
            "fallback": "~/.TRIGGERcmdData/token.tkn file (chmod 600)"
          }
        }
      },
  }
---
# TriggerCMD 技能

使用此技能可以检查并运行在本地 API 令牌关联的账户下注册的所有计算机上的 TRIGGERcmd 命令。

## 认证

该技能支持两种认证方法（按顺序检查）：

1. **环境变量**（推荐）：将 `TRIGGERCMD_TOKEN` 设置为您的个人 API 令牌
   - 在 shell 中导出该变量：`export TRIGGERCMD_TOKEN='your-token-here'`
   - 或在每个命令前加上前缀：`TRIGGERCMD_TOKEN='your-token-here' <command>`

2. **令牌文件**：将令牌存储在 `~/.TRIGGERcmdData/token.tkn` 文件中
   - 该文件应仅包含原始令牌文本（不含引号、空格或尾随换行符）
   - 必须设置文件权限：`chmod 600 ~/.TRIGGERcmdData/token.tkn`
   - 创建方法：`mkdir -p ~/.TRIGGERcmdData && read -s TOKEN && printf "%s" "$TOKEN" > ~/.TRIGGERcmdData/token.tkn && chmod 600 ~/.TRIGGERcmdData/token.tkn`

**获取令牌的方法：**
1. 登录到 https://www.triggercmd.com
2. 转到您的个人资料/设置页面
3. 复制 API 令牌（请妥善保管，切勿共享）

**安全提示：** 严禁在共享终端或输出中打印、记录或粘贴令牌。

## 常用环境辅助工具

```bash
# Get token from environment variable or file (checks env var first)
if [ -n "$TRIGGERCMD_TOKEN" ]; then
  TOKEN="$TRIGGERCMD_TOKEN"
elif [ -f ~/.TRIGGERcmdData/token.tkn ]; then
  TOKEN=$(cat ~/.TRIGGERcmdData/token.tkn)
else
  echo "Error: No token found. Set TRIGGERCMD_TOKEN env var or create ~/.TRIGGERcmdData/token.tkn" >&2
  exit 1
fi

AUTH_HEADER=("-H" "Authorization: Bearer $TOKEN")
BASE_URL=https://www.triggercmd.com/api
```

使用上述代码片段可以避免在每个命令中重复认证逻辑。

## list_commands

列出该账户下所有计算机上的所有命令。

```bash
curl -sS "${BASE_URL}/command/list" "${AUTH_HEADER[@]}" | jq '.records[] | {computer: .computer.name, name, voice, allowParams, id, mcpToolDescription}'
```

**格式化提示：**
- 为了便于阅读，可以使用以下命令格式化输出：`jq -r '.records[] | "\(.computer.name): \(.name) (voice: \(.voice // "-"))"'`
- 在建议后续命令时，应包含 `allowParams` 信息，以便用户了解是否允许传递参数。
- 当请求摘要时，按 `.computer.name` 分组并使用项目符号列出每台计算机的命令。

## run_command

使用计算机名称和命令名称，在指定的计算机上运行特定命令。

```bash
# Use jq to safely construct JSON payload and prevent injection
PAYLOAD=$(jq -n \
  --arg computer "$COMPUTER" \
  --arg command "$COMMAND" \
  --arg params "$PARAMS" \
  '{computer: $computer, command: $command, params: $params}')

curl -sS -X POST "${BASE_URL}/run/trigger" \
  "${AUTH_HEADER[@]}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
```

- `$COMPUTER` 应为计算机名称（例如：“MyLaptop”）
- `$COMMAND` 应为命令名称（例如：“calculator”）
- 如果命令不接受参数，请在 `jq` 命令中省略 `--arg params "$PARAMS"` 和 `params: $params`。
- 使用 `jq -n` 与 `--arg` 可确保所有值都被正确转义，从而防止 JSON 注入攻击。
- 成功的响应会返回确认信息以及任何排队中的状态信息，并将这些信息显示给用户。

## 错误处理**

- **令牌文件缺失**：说明如何创建 `~/.TRIGGERcmdData/token.tkn` 文件，并提醒用户保持其隐私。
- **令牌无效（401/403）**：要求用户重新生成令牌并覆盖现有文件。
- **计算机未找到**：显示可用的计算机名称（不区分大小写）。
- **命令未找到**：列出目标计算机的所有命令；如果相关命令允许传递参数，请将其突出显示。
- **API/网络问题**：显示 HTTP 状态码和响应内容以帮助调试。

## 测试流程**

1. 验证认证配置是否正确：
   ```bash
   [ -n "$TRIGGERCMD_TOKEN" ] || [ -f ~/.TRIGGERcmdData/token.tkn ] || echo "Error: No token configured"
   ```

2. 测试 API 连接性（使用上述辅助工具）：
   ```bash
   curl -sS "${BASE_URL}/command/list" "${AUTH_HEADER[@]}" | jq -r '.records[0].computer.name // "No commands found"'
   ```

3. 先通过列出计算机 ID 来进行命令的预测试，然后使用安全的命令（例如，运行一个无害的脚本）再进行任何可能造成影响的操作。

## 安全注意事项**

- **严禁打印、记录或暴露令牌值**。不要在命令输出或错误消息中显示令牌。
- 如果使用令牌文件方法，请确保 `~/.TRIGGERcmdData/token.tkn` 的权限设置为 `600`（仅允许所有者读取）。
- 对于临时会话或不需要将令牌持久化到磁盘的情况，建议使用 `TRIGGERCMD_TOKEN` 环境变量。
- 在执行可能产生副作用的命令之前，请先征得用户的同意。
- 遵守每台设备的安全限制；如果不确定命令的具体功能，请在执行前先询问用户。
- 如果认证失败，请不要建议可能暴露令牌的命令；而是引导用户通过 TRIGGERcmd 网站重新生成令牌。