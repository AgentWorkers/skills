---
name: openclaw-migration
description: 将用户的 OpenClaw 定制设置迁移到 Hermes Agent。从 `~/.openclaw` 文件夹中导入与 Hermes 兼容的内存配置、`SOUL.md` 文件、命令允许列表、用户技能以及选定的工作区资产，然后详细报告无法迁移的内容及其原因。
version: 1.0.0
author: Hermes Agent (Nous Research)
license: MIT
metadata:
  hermes:
    tags: [Migration, OpenClaw, Hermes, Memory, Persona, Import]
    related_skills: [hermes-agent]
---
# OpenClaw 到 Hermes 的迁移

当用户希望将他们的 OpenClaw 设置迁移到 Hermes Agent 时，可以使用此技能，同时尽量减少手动清理的工作量。

## CLI 命令

为了快速、非交互式的迁移，请使用内置的 CLI 命令：

```bash
hermes claw migrate              # Full interactive migration
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
hermes claw migrate --source /custom/path/.openclaw  # Custom source
```

该 CLI 命令会运行下面描述的相同迁移脚本。当您需要交互式的、有指导的迁移过程（包括预测试和逐项冲突解决）时，可以通过 Hermes Agent 使用此技能。

**首次设置：** `hermes setup` 向导会自动检测 `~/.openclaw` 文件，并在配置开始前提供迁移选项。

## 该技能的功能

它使用 `scripts/openclaw_to_hermes.py` 脚本来：

- 将 `SOUL.md` 文件导入 Hermes 主目录中
- 将 OpenClaw 的 `MEMORY.md` 和 `USER.md` 文件转换为 Hermes 的内存条目
- 将 OpenClaw 的命令审批规则合并到 Hermes 的 `command_allowlist` 中
- 迁移 Hermes 兼容的消息设置（如 `TELEGRAM_ALLOWED_USERS` 和 `MESSAGING_CWD`）
- 将 OpenClaw 的技能复制到 `~/.hermes/skills/openclaw-imports/` 目录
- 可选地将 OpenClaw 的工作区配置文件复制到指定的 Hermes 工作区
- 将兼容的工作区资源（如 `workspace/tts/`）复制到 `~/.hermes/tts/`
- 将没有直接 Hermes 目录的非机密文档归档
- 生成一份结构化的报告，列出迁移的项目、冲突项、被跳过的项及其原因

## 脚本路径

辅助脚本位于以下路径：

- `scripts/openclaw_to_hermes.py`

当此技能从 Skills Hub 安装后，其默认位置为：

- `~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py`

请不要猜测更短的路径（例如 `~/.hermes/skills/openclaw-migration/...`）。

在运行辅助脚本之前，请注意：

1. 优先使用 `~/.hermes/skills/migration/openclaw-migration/` 下的安装路径。
2. 如果该路径不可用，请检查已安装的技能目录，并根据 `SKILL.md` 文件中的信息来确定脚本的位置。
3. 仅在没有找到安装路径或技能被手动移动的情况下，才使用 `find` 命令来查找脚本。
4. 在调用终端工具时，不要传递 `workdir: "~"`。请使用用户的 home 目录作为绝对路径，或者完全省略 `workdir` 参数。

使用 `--migrate-secrets` 选项时，还会导入一组允许的 Hermes 兼容的秘密信息，目前包括：

- `TELEGRAM_BOT_TOKEN`

## 默认工作流程

1. 首先进行预测试。
2. 提供一个简单的总结，说明哪些内容可以迁移、哪些不能迁移、哪些内容将被归档。
3. 如果有 `clarify` 工具可用，使用它来获取用户的决策，而不是让用户自由输入文字回答。
4. 如果预测试发现导入的技能目录存在冲突，请在执行前询问用户如何处理这些冲突。
5. 在执行前，询问用户选择两种支持的迁移模式之一。
6. 仅当用户希望迁移工作区配置文件时，才询问目标工作区路径。
7. 使用相应的预设和参数执行迁移。
8. 总结迁移结果，特别是：
   - 迁移了哪些内容
   - 哪些内容被归档以供手动审核
   - 哪些内容被跳过及其原因

## 用户交互协议

Hermes CLI 支持 `clarify` 工具来进行交互式提示，但其限制如下：

- 每次只能选择一个选项
- 最多提供 4 个预定义的选项
- 提供一个自动的 “其他” 自由文本选项

它 **不** 支持在单个提示中显示多选复选框。

对于每次 `clarify` 调用，请确保：

- 提供一个非空的 `question`（问题）
- 仅对真正可选择的选项提供 `choices`（选项列表）
- 选项数量限制在 2-4 个纯字符串选项之间
- 不要使用占位符或截断的选项（如 `...`）
- 不要在问题中包含虚假的表单字段（如 “在此输入目录” 或空行）
- 对于开放式的路径问题，仅询问路径本身；用户可以在面板下方的 CLI 提示框中输入路径

如果 `clarify` 调用返回错误，请检查错误信息，修正问题内容，然后使用有效的 `question` 和正确的选项重新尝试。

当 `clarify` 可用且预测试显示需要用户决策时，您的 **下一个操作必须是调用 `clarify` 工具**。不要以普通的助手消息（如 “让我展示选项” 或 “您想做什么？”）来结束对话。如果需要用户决策，请先通过 `clarify` 获取用户的答案。

如果仍有未解决的决策，请不要在它们之间插入解释性信息。在收到一个 `clarify` 回答后，您的下一个操作应该是再次调用 `clarify`。

当预测试显示以下情况时，将 `workspace-agents` 视为未解决的决策：

- `kind="workspace-agents"`
- `status="skipped"`
- `reason` 中包含 “未提供工作区目标”

在这种情况下，在执行之前必须询问用户关于工作区配置文件的信息。不要默认认为用户选择了跳过该选项。

由于这个限制，请使用以下简化的决策流程：

1. 对于 `SOUL.md` 的冲突，使用 `clarify` 并提供以下选项：
   - `keep existing`（保持现有设置）
   - `overwrite with backup`（用备份覆盖）
   - `review first`（先查看）

2. 如果预测试显示一个或多个 `kind="skill"` 项且 `status="conflict`（存在冲突），使用 `clarify` 并提供以下选项：
   - `keep existing skills`（保持现有技能）
   - `overwrite conflicting skills with backup`（用备份覆盖冲突的技能）
   - `import conflicting skills under renamed folders`（将冲突的技能导入到重命名的文件夹中）

3. 对于工作区配置文件，使用 `clarify` 并提供以下选项：
   - `skip workspace instructions`（跳过工作区配置文件）
   - `copy to a workspace path`（复制到工作区路径）
   - `decide later`（稍后决定）

4. 如果用户选择复制工作区配置文件，请接着提出一个开放式的 `clarify` 问题，要求用户提供 **绝对路径**。

5. 根据用户的选择，使用以下命令参数执行迁移：
   - `user-data only`（仅迁移用户数据）
   - `full compatible migration`（完整兼容迁移）
   - `cancel`（取消迁移）

6. `user-data only` 表示：仅迁移用户数据和兼容的配置，但不导入允许的秘密信息。
   `full compatible migration` 表示：迁移用户数据和允许的秘密信息。

执行前的注意事项：

- 如果由于 “未提供工作区目标” 而导致 `workspace-agents` 被跳过，不要执行迁移。
- 解决此问题的有效方法只有：
  - 用户明确选择 “skip workspace instructions”
  - 用户明确选择 “decide later”（稍后决定）
  - 用户在选择了 “copy to a workspace path” 之后提供工作区路径
- 预测试中未提供工作区目标并不意味着可以执行迁移。
- 如果有任何未解决的 `clarify` 决策，请不要执行迁移。

使用以下格式的 `clarify` 问题作为默认模式：

- `{"question":"您现有的 SOUL.md 与导入的文件存在冲突。我应该怎么做？","choices":["keep existing","overwrite with backup","review first"]}`
- `{"question":"Hermes 中已经存在一个或多个导入的 OpenClaw 技能。应该如何处理这些技能冲突？","choices":["keep existing skills","overwrite conflicting skills with backup","import conflicting skills under renamed folders"]}`
- `{"question":"选择迁移模式：仅迁移用户数据，还是执行包含允许的秘密信息的完整兼容迁移？","choices":["user-data only","full compatible migration","cancel"]}`
- `{"question":"您是否希望将 OpenClaw 的工作区配置文件复制到 Hermes 工作区？","choices":["skip workspace instructions","copy to a workspace path","decide later"]}`
- `{"question":"请提供一个绝对路径，用于复制工作区配置文件。"}`

## 用户决策与命令的映射

将用户的决策准确地映射到相应的命令参数：

- 如果用户选择 “keep existing” 对于 `SOUL.md`，则不要添加 `--overwrite` 参数。
- 如果用户选择 “overwrite with backup”，则添加 `--overwrite` 参数。
- 如果用户选择 “review first”，则在执行前停止并查看相关文件。
- 如果用户选择 “keep existing skills”，则添加 `--skill-conflict skip` 参数。
- 如果用户选择 “overwrite conflicting skills with backup”，则添加 `--skill-conflict overwrite` 参数。
- 如果用户选择 “import conflicting skills under renamed folders”，则添加 `--skill-conflict rename` 参数。
- 如果用户选择 “user-data only”，则使用 `--preset user-data` 参数执行迁移，并且不要添加 `--migrate-secrets` 参数。
- 如果用户选择 “full compatible migration”，则使用 `--preset full --migrate-secrets` 参数执行迁移。
- 仅当用户明确提供了工作区路径时，才添加 `--workspace-target` 参数。
- 如果用户选择 “skip workspace instructions” 或 “decide later”，则不要添加 `--workspace-target` 参数。

在执行之前，用简单的语言重新说明命令的详细内容，并确保与用户的选项一致。

## 执行后的报告规则

执行完成后，以脚本的 JSON 输出作为最终结果。

1. 所有统计信息均基于 `report.summary`。
2. 仅将状态为 `migrated` 的项列出为 “成功迁移”。
- 除非报告显示某项的状态为 `migrated`，否则不要声称冲突已解决。
- 除非报告中的 `kind="soul"` 项的状态为 `migrated`，否则不要声称 `SOUL.md` 被覆盖。
- 如果 `report.summary.conflict` 大于 0，则需要包含冲突部分的报告。
- 如果统计信息和列出的项目不一致，请在响应前修复列表以匹配报告内容。
- 如果报告提供了 `output_dir` 路径，请在响应中包含该路径，以便用户可以查看 `report.json`、`summary.md`、备份文件和归档文件。
- 对于内存或用户配置文件溢出的情况，除非报告明确指出了归档路径，否则不要声称文件已被归档。如果 `details.overflow_file` 存在，请说明所有溢出文件都被导出到了该路径。
- 如果某个技能被导入到了重命名的文件夹中，请报告最终的路径，并提及 `details.renamed_from`。
- 如果 `report.skill_conflict_mode` 存在，请将其作为选择导入技能冲突策略的依据。
- 如果某个项的状态为 `skipped`，不要将其描述为被覆盖、备份或迁移。
- 如果 `kind="soul"` 的状态为 `skipped` 且原因是 “Target already matches source”（目标路径已存在），则说明该文件保持不变，不要提及备份。
- 如果导入的技能的 `details.backup` 为空，请不要暗示现有的 Hermes 技能被覆盖或备份。只需说明导入的文件被放置在了新的目标路径中，并提及 `details.renamed_from` 作为原始文件夹的路径。

## 迁移预设

在常规使用中，建议使用以下两种预设：

- `user-data`（仅迁移用户数据）
- `full`（迁移所有内容）

`user-data` 包括：

- `soul`（用户灵魂文件）
- `workspace-agents`（工作区代理）
- `memory`（内存文件）
- `user-profile`（用户配置文件）
- `messaging-settings`（消息设置）
- `command-allowlist`（命令允许列表）
- `skills`（技能文件）
- `tts-assets`（TTS 资源文件）
- `archive`（归档文件）

`full` 包含 `user-data` 中的所有内容，此外还包括：

- `secret-settings`（秘密设置）

辅助脚本仍然支持 `--include` / `--exclude` 参数来筛选类别，但将其视为高级功能，而不是默认行为。

## 命令

- 使用 ````bash
python3 ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py
```` 进行包含所有内容的预测试。
- 使用终端工具时，建议使用绝对路径格式的命令（如 ````json
{"command":"python3 /home/USER/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py","workdir":"/home/USER"}
````）。
- 使用 `user-data` 预设进行预测试：````bash
python3 ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --preset user-data
````
- 使用 ````bash
python3 ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset user-data --skill-conflict skip
```` 执行用户数据迁移。
- 使用 ````bash
python3 ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset full --migrate-secrets --skill-conflict skip
```` 执行完整兼容的迁移。
- 使用 ````bash
python3 ~/.hermes/skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py --execute --preset user-data --skill-conflict rename --workspace-target "/absolute/workspace/path"
```` 执行包含工作区配置文件的迁移。

默认情况下，不要使用 `$PWD` 或 home 目录作为工作区目标。请先询问用户的工作区路径。

## 重要规则

1. 除非用户明确表示立即执行，否则请先进行预测试。
- 默认情况下不要迁移秘密信息。除非用户明确要求迁移秘密信息，否则不要将令牌、认证数据、设备凭据和原始网关配置导入 Hermes。
- 除非用户明确允许，否则不要默认覆盖非空的工作区目标。启用覆盖功能时，辅助脚本会保留备份文件。
- 始终向用户提供被跳过的项的列表。该列表是迁移过程的一部分，不是可选的额外内容。
- 优先使用主 OpenClaw 工作区（`~/.openclaw/workspace/`），只有在主文件缺失时才使用默认工作区。
- 即使在迁移秘密信息的模式下，也只迁移有合法 Hermes 目录的秘密信息。不支持的认证数据必须被标记为跳过。
- 如果预测试显示有大量文件需要复制、存在冲突的 `SOUL.md` 文件或内存条目溢出，请在执行前分别指出这些问题。
- 如果用户不确定，建议使用 `user-data` 预设。
- 仅当用户明确提供了工作区路径时，才包括 `workspace-agents`。
- 将 `--include` / `--exclude` 参数视为高级选项，而不是常规操作。
- 如果 `clarify` 可用，不要在预测试总结中使用模糊的 “您想做什么？” 这样的问题。请使用结构化的后续提示。
- 如果可以使用具体的选择选项，请不要使用开放式的 `clarify` 提示。先提供可选选项，只有在需要输入绝对路径或查看文件时才使用自由文本。
- 在预测试后，如果仍有未解决的决策，请立即使用 `clarify` 获取用户的答案。
- 后续问题的优先顺序如下：
    - `SOUL.md` 冲突
    - 进口技能的冲突
    - 迁移模式
    - 工作区配置文件的路径
- 不要在同一条消息中承诺稍后提供选项。请通过调用 `clarify` 来获取用户的答案。
- 在得到迁移模式的答案后，请检查 `workspace-agents` 是否仍未解决。如果是，请立即进行工作区配置文件的 `clarify` 操作。
- 在得到任何 `clarify` 回答后，如果有其他未解决的决策，请立即进行下一个必要的决策。

## 预期结果

成功执行后，用户应该得到：

- Hermes 人物状态被导入
- Hermes 内存文件中包含了转换后的 OpenClaw 数据
- OpenClaw 技能文件位于 `~/.hermes/skills/openclaw-imports/`
- 迁移报告会显示任何冲突项、被跳过的项或未支持的数据