---
name: mud
description: 操作和维护 OpenClaw 的持久性 MUD 代理。该代理适用于执行 MUD 引擎命令、对 MUD 状态行为进行测试、验证数据的保存/恢复功能、诊断 MUD 数据问题，以及处理 MUD 的部署操作。
---
# MUD

**作者：** agigui 和 lia

使用此技能可以安全且可靠地运行本地的 MUD 引擎。

## 工作流程

1. 找到引擎目录。
   - 推荐路径：`C:\Users\openclaw\.openclaw\workspace-mud-dm\mud-agent`
   - 备选路径：`C:\Users\openclaw\.openclaw\workspace\mud-agent`
2. 使用 `scripts/mud_cmd.py` 运行烟雾测试（smoke test）。
3. 执行所需的 MUD 操作。
4. 详细操作步骤请参考 `references/ops.md` 和 `references/commands.md`。

## 命令执行器

```powershell
python skills/mud/scripts/mud_cmd.py "<command>"
```

示例（当前使用的 CLI 引擎）：

```powershell
python skills/mud/scripts/mud_cmd.py "list-races"
python skills/mud/scripts/mud_cmd.py "register-player --campaign demo --player u1 --name Hero"
python skills/mud/scripts/mud_cmd.py "new-character --campaign demo --player u1 --name Rook --race human --char-class rogue"
python skills/mud/scripts/mud_cmd.py "save --campaign demo"
python skills/mud/scripts/mud_cmd.py "check-image-cooldown --campaign demo"
python skills/mud/scripts/mud_cmd.py "generate-image --campaign demo --prompt \"A rain-soaked neon tavern\""
```

旧的斜杠命令（slash-command）引擎会被自动检测到，并仍由相同的封装层（wrapper）支持。

## 注意事项

- 确保引擎代码中的逻辑操作具有确定性（deterministic）；使用大型语言模型（LLM）进行文本生成。
- 避免在技能文件中硬编码敏感信息或令牌（tokens）。
- 当运行时图像处理流程（runtime image pipeline）配置完成后，可以通过引擎命令（`check-image-cooldown`、`record-image`、`generate-image`）生成图像。
- 本技能专注于操作的执行过程本身。