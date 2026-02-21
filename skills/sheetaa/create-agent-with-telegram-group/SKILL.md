---
name: create-agent-with-telegram-group
description: 创建一个新的 OpenClaw 代理，并将其绑定到一个专用的 Telegram 组，工作目录为 `~/claw-<agent-name>`。当用户请求“一个代理对应一个组”的设置、Telegram 组的绑定，或需要重复配置代理时，请使用此方法。务必询问用户需要使用哪种模型，并获取必要的初始化信息（参见 `USER.md`、`IDENTITY.md`、`SOUL.md` 文件），同时将组的回复模式设置为“无需提及发送者名称”（no-mention-required）。
---
# 创建代理并设置专属的Telegram群组

为每个代理创建一个专属的Telegram群组，将代理绑定到该群组，并设置一个独立的工作空间路径。

## 首先使用脚本的规则

对于需要执行确定性操作的步骤，优先使用预打包的脚本（更稳定且Token成本更低）。只有在脚本无法处理特殊情况时，才进行手动JSON编辑。

使用以下脚本：
- `scripts/provision_config.py` 用于代理配置、绑定以及设置“禁止提及”（no-mention）功能（会自动备份`openclaw.json`文件）。
- `scripts/init_workspace.py` 用于初始化`USER.md`、`IDENTITY.md`和`SOUL.md`文件。

## 配置安全机制

- `scripts/provision_config.py` 会读取和写入`~/.openclaw/openclaw.json`文件。
- 默认情况下，它会创建一个备份文件：`~/.openclaw/openclaw.json.bak.<timestamp>`。
- 它只会更新以下内容：
  - `agents.list`（添加/更新目标代理）
  - `bindings`（添加目标Telegram群组的绑定信息）
  - `channelsTelegram.groups.<chat_id>.requireMention=false`（设置禁止提及的规则）
  - `gateway.reload.mode`（如果不存在，则设置为默认的“hybrid”模式）

## 输入参数

在执行前需要收集以下信息：
- `agent_name`（必需）
- `model`（必需）：明确询问用户要使用的模型；模型相关信息必须从用户的`~/.openclaw/openclaw.json`文件中获取（不要硬编码示例值）
- 可选的`telegram_group_title`（自定义群组名称）
- 初始化偏好设置（必须询问）：
  - 是否要创建/更新`USER.md`文件
  - 是否要创建/更新`IDENTITY.md`文件
  - 是否要创建/更新`SOUL.md`文件
- 如果启用了初始化功能，在写入文件之前需要收集以下内容：
  - `USER.md`：用户名/偏好称呼/语言/目标/备注
  - `IDENTITY.md`：代理显示名称/风格/表情符号（可选）
  - `SOUL.md`：角色/任务/语气/约束条件（简短的要点列表）

**规范化`agent_name`的规则：**
- 仅保留小写字母、数字和连字符。
- 将空格/下划线替换为 `-`。
- 在路径和ID中使用这个规范化后的值。

**Telegram群组标题的规则：**
- 如果用户提供了`telegram_group_title`，则直接使用该标题。
- 如果没有提供，则根据`agent_name`生成默认标题（使用PascalCase格式）。
  - 例如：`test-skill` -> `TestSkill`，`bilingual-agent` -> `BilingualAgent`。

## 工作流程：

1. 首先从`~/.openclaw/openclaw.json`文件中读取可用的模型列表，然后与用户确认输入信息（代理名称、模型、初始化文件设置以及可选的Telegram群组标题）。
  - 示例发现命令（支持字典和列表格式的模型列表）：
    ```
    python3 - <<'PY'
    import json, os
    json.load(open(os.path.expanduser '~/.openclaw/openclaw.json'))
    prov = c.get('models',{})
    for p, v in prov.items():
        ms = v.get('models',{})
        if isinstance(ms, dict):
            ids = ms.keys()
        else:
            ids = [m.get('id') for m in ms if isinstance(m, dict) and m.get('id')]
        for mid in ids:
            print(f"{p}/{mid}")
    PY
    ```

2. 构建工作空间路径（格式为`~/claw-<agent-name>`），如果路径不存在则创建它。

3. 确定群组标题：
    - 如果用户提供了`telegram_group_title`，则使用该标题。
    - 否则，使用`agent_name`的PascalCase格式生成默认标题。

4. 创建并绑定Telegram群组（使用确定的群组标题）：
    - 使用浏览器自动化或用户账户流程来完成群组的创建和绑定（Telegram机器人API可能无法可靠地完成此操作）。
    - 如果浏览器自动化不可用，则请求用户完成最基本的手动操作，之后再继续后续步骤。

5. 通过脚本创建/更新OpenClaw配置（推荐方式）：
    ```
    python3 scripts/provision_config.py --agent-name <agent-name> --model <model> --chat-id <chat_id>
    ```
    这个命令会设置代理信息、工作空间路径、绑定信息以及“禁止提及”的规则。

6. 应用配置并激活配置：
    - 如果启用了热重载功能，通过日志验证配置是否已正确应用。
    - 如果未启用热重载或配置未应用，则重启代理服务器并验证启动是否正常。

7. 加载代理的运行时文件（首次运行时必须执行）：
    - 确保`~/.openclaw/agents/<agent-id>/agent`文件存在。
    - 确保相关的认证和模型文件存在（如果缺少，可以从`main`代理文件中复制）：
      - `auth-profiles.json`
      - `auth.json`
      - `models.json`

8. 如果需要初始化代理，请先询问用户所需的信息，然后写入相应的文件：
    - 收集`USER.md`、`IDENTITY.md`和`SOUL.md`文件所需的字段。
    - 接着运行：
    ```
    python3 scripts/init_workspace.py --workspace <workspace> --agent-name <agent-name> [--with-user] [--with-identity] [--with-soul]
    ```
    如果用户提供了自定义文本，在脚本初始化后应用这些文本（覆盖默认值）。

9. 确保当前配置的有效性（例如，群组的`allowFrom`设置是否合法）。

10. 配置完成后进行验证：
    - 向群组发送测试消息，并要求用户回复“ping”。
    - 确认代理在回复时没有使用`@mention`标签。

11. 返回完成总结信息，包括：
    - 代理名称
    - 选择的模型
    - 工作空间路径
    - 群组标题
    `chat_id`
    “禁止提及”的设置（`enabled`/`disabled`）
    状态以及下一步操作（如果有）。

## Telegram自动化规则：

- 群组的创建/删除和成员操作应使用浏览器自动化或用户账户流程。
- 对于浏览器自动化，建议使用已登录的Telegram会话对应的Chrome代理配置文件。
- 如果没有可用的Chrome标签页，请求用户先附加一个标签页，然后再继续操作。
- 如果Telegram显示了无法自动处理的确认或验证码，请求用户手动点击一次，之后再继续。

## OpenClaw命令的查找方法

不要自行发明新的OpenClaw命令。
- 当不知道代理的创建/更新命令的语法时，运行`openclaw help`。
- 如果需要，运行`openclaw <subcommand> --help`来查看相关子命令的用法。
- 仅使用系统发现的命令格式。

## 函数幂等性原则：

- 如果`~/claw-<agent-name>`文件已经存在，则直接重用它。
- 如果已经存在同名群组，需要确认是继续使用现有群组还是创建新的群组。
- 如果代理已经存在，则更新其模型、绑定信息或工作空间路径，而不是重复创建。

## 必须执行的可靠性检查：

- 验证绑定到的群组的“禁止提及”设置是否正确（`requireMention=false`）。
- 验证代理配置是否已成功应用：
  - 检查热重载模式和状态日志（例如“config hot reload applied”或“restarting telegram channel”）。
  - 如果热重载功能未启用或配置未应用，则重启代理服务器并重新检查日志。
- 向新创建的群组发送一条机器人发起的测试消息，然后验证用户是否能正常回复“ping”。
- 在确认“ping”和“pong”消息的交互成功之前，不要宣布操作成功。

## 失败处理：

- 如果群组创建成功但绑定失败：
  - 保留已创建的群组。
  - 报告具体的失败步骤。
  - 提供下一步操作的指导（例如，通过单个命令继续执行）。

- 如果无法自动获取`chat_id`：
  - 将此情况视为部分成功，并提供获取`chat_id`的最简方法，然后继续绑定操作。

## 输出模板：

返回简洁的状态信息：
- `agent`：<agent-name>
- `model`：<selected-model>
- `workspace`：`~/claw-<agent-name>`
- `telegram_group`：<title>
- `chat_id`：<id 或 PENDING>
- `binding`：<done|pending>
- `reply_without_mention`：<enabled|disabled>
- `initialized_files`：`USER.md, IDENTITY.md, SOUL.md 或其中的一部分`
- `verification`：<passed|failed>
- `next_step`：<none 或具体的下一步操作>