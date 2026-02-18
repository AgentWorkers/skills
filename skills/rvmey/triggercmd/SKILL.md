---
name: triggercmd
description: 通过 TRIGGERcmd REST API 列出并运行命令，可以远程控制 TRIGGERcmd 连接的计算机。
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

该技能支持两种认证方式（按顺序检查）：

1. **环境变量**（推荐）：将 `TRIGGERCMD_TOKEN` 设置为您的个人 API 令牌
   - 在 shell 中导出该变量：`export TRIGGERCMD_TOKEN='your-token-here'`
   - 或在每个命令前添加前缀：`TRIGGERCMD_TOKEN='your-token-here' <command>`

2. **令牌文件**：将令牌存储在 `~/.TRIGGERcmdData/token.tkn` 文件中
   - 该文件应仅包含原始令牌文本（不含引号、空格或尾随换行符）
   - 必须设置文件权限为只读：`chmod 600 ~/.TRIGGERcmdData/token.tkn`
   - 创建方法：`mkdir -p ~/.TRIGGERcmdData && read -s TOKEN && printf "%s" "$TOKEN" > ~/.TRIGGERcmdData/token.tkn && chmod 600 ~/.TRIGGERcmdData/token.tkn`

**获取令牌的方法：**
1. 登录至 https://www.triggercmd.com
2. 转到您的个人资料/设置页面
3. 复制 API 令牌（请妥善保管，切勿共享）

**安全提示：**切勿在共享终端或输出中打印、记录或粘贴令牌。

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

列出该账户在所有计算机上的所有命令。

```bash
curl -sS "${BASE_URL}/command/list" "${AUTH_HEADER[@]}" | jq '.records[] | {computer: .computer.name, name, voice, allowParams, id, mcpToolDescription}'
```

**格式化提示：**
- 为了方便查看，可以使用以下命令进行输出：`jq -r '.records[] | "\(.computer.name): \(.name) (voice: \(.voice // "-"))"'`
- 在建议后续操作时，需要包含 `allowParams` 信息，以便用户了解是否允许传递参数。
- 当请求摘要时，按 `.computer.name` 分组并使用项目符号列出每台计算机的命令。

## run_command

在指定的计算机上运行特定命令。

1. 解析计算机 ID（如果尚未知道 ID 的话）：

```bash
LIST_JSON=$(curl -sS "${BASE_URL}/command/list" "${AUTH_HEADER[@]}")
COMPUTER_ID=$(jq -r --arg NAME "$COMPUTER" '.records[] | select(.computer.name | ascii_downcase == ($NAME | ascii_downcase)) | .computer.id' <<<"$LIST_JSON" | head -n1)
COMMAND_ID=$(jq -r --arg NAME "$COMPUTER" --arg CMD "$COMMAND" '.records[] | select(.computer.name | ascii_downcase == ($NAME | ascii_downcase)) | select(.name | ascii_downcase == ($CMD | ascii_downcase)) | .id' <<<"$LIST_JSON" | head -n1)
```

2. 运行命令：

```bash
curl -sS -X POST "${BASE_URL}/run/trigger" \
  "${AUTH_HEADER[@]}" \
  -H "Content-Type: application/json" \
  -d "{\"computer\": \"$COMPUTER_ID\", \"command\": \"$COMMAND_ID\", \"params\": \"$PARAMS\"}"
```

- 如果命令不接受参数，请省略 `params` 部分。
- 成功执行命令后，会返回确认信息以及任何排队中的状态信息。这些信息都会显示给用户。

## 错误处理**

- **令牌文件缺失**：说明如何创建 `~/.TRIGGERcmdData/token.tkn` 文件，并提醒用户保持其安全性。
- **令牌无效（401/403 错误）**：要求用户重新生成令牌并覆盖现有文件。
- **计算机未找到**：显示可用的计算机名称（不区分大小写）。
- **命令未找到**：列出目标计算机的所有命令；如果相关命令支持参数传递，请将其标出。
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

3. 先列出计算机 ID，然后使用无风险的命令（例如切换一个无害的脚本）进行测试，再执行任何可能产生影响的操作。

## 安全注意事项**

- **切勿打印、记录或公开令牌值**。不要在命令输出或错误消息中显示令牌内容。
- 如果使用令牌文件方法，请确保 `~/.TRIGGERcmdData/token.tkn` 的权限设置为 `600`（仅允许所有者读取）。
- 对于临时会话或不需要将令牌保存到磁盘的情况，建议使用 `TRIGGERCMD_TOKEN` 环境变量。
- 在执行可能产生副作用的命令之前，请先征得用户同意。
- 遵守每台计算机的安全限制；如果不确定命令的具体功能，请在执行前先询问用户。
- 如果认证失败，请不要建议可能暴露令牌的命令；应引导用户通过 TRIGGERcmd 网站重新生成令牌。