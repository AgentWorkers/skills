---
name: a2a-delegation-setup
description: >
  **@aramisfa/openclaw-a2a-outbound 的安装、启用、配置、验证及更新指南：在 OpenClaw 中的引导式设置与故障排除**
  本文档提供了关于如何安装、启用、配置、验证以及更新 `@aramisfa/openclaw-a2a-outbound` 的详细步骤。这些步骤将帮助您在 OpenClaw 环境中顺利使用该插件。
  ### 安装过程
  1. **从 GitHub 下载源代码**：
     访问 [GitHub 仓库](https://github.com/aramisfa/openclaw-a2a-outbound) 并克隆项目到本地。
  2. **构建项目**：
     在项目根目录下执行以下命令来构建源代码：
     ```
     git clone https://github.com/aramisfa/openclaw-a2a-outbound.git
     cd openclaw-a2a-outbound
     make
     ```
  3. **安装构建后的二进制文件**：
     将生成的二进制文件（通常位于 `build/bin` 目录下）添加到 OpenClaw 的 `bin` 目录中。具体操作方法取决于您的操作系统和 OpenClaw 的安装方式。
  ### 启用插件
  在 OpenClaw 中启用 `@aramisfa/openclaw-a2a-outbound` 插件通常涉及修改配置文件或运行特定的命令。请参考项目的文档或源代码中的说明来了解具体步骤。
  ### 配置插件
  根据项目的需求，您可能需要配置 `@aramisfa/openclaw-a2a-outbound` 的某些参数或设置。请查阅项目的文档或源代码以获取详细的配置指南。
  ### 验证插件功能
  安装和配置完成后，您需要验证插件是否按预期工作。这可能包括运行测试用例或检查插件产生的输出数据。具体验证方法取决于插件的功能。
  ### 更新插件
  为了确保您使用的是最新版本的 `@aramisfa/openclaw-a2a-outbound`，请定期从 GitHub 仓库获取更新并重新安装插件。具体操作步骤如下：
  1. **获取最新代码**：
     在项目根目录下执行以下命令来获取最新代码：
     ```
     git fetch origin
     ```
  2. **合并更改**：
     将最新的代码合并到本地分支：
     ```
     git merge main
     ```
  3. **构建并安装更新后的二进制文件**：
     重新构建项目并安装更新后的二进制文件。
  4. **重新启动 OpenClaw**：
     安装完成后，确保重新启动 OpenClaw 以使更改生效。
  ### 故障排除
  如果在安装、启用或使用过程中遇到问题，请查阅项目的文档或源代码中的错误日志（通常位于 `log` 目录下），或者查看 OpenClaw 的官方文档和社区论坛以获取帮助。
  希望本指南能帮助您顺利安装和配置 `@aramisfa/openclaw-a2a-outbound` 插件。如果您在过程中遇到任何问题，请随时联系项目的维护者或 OpenClaw 的社区支持。
homepage: "https://github.com/aramisfacchinetti/openclaw-a2a-plugins/tree/master/packages/openclaw-a2a-outbound#readme"
user-invocable: true
disable-model-invocation: true
---
# A2A 转发设置

当 `@aramisfa/openclaw-a2a-outbound` 插件仍需要在 OpenClaw Gateway 主机上进行安装、启用、配置、验证、更新或故障排除时，请使用此技能。

在设置完成后，切勿使用此技能进行常规的运行时转发操作。一旦插件准备就绪，请切换到内置的 `remote-agent` 技能和 `remote_agent` 工具。

## 相互操作规则

- 在进行任何安装、更新、重启或配置修改之前，请先征得许可。
- 在拥有 OpenClaw 配置和插件安装权限的 Gateway 主机上运行命令。
- 如果无法访问 Shell，应提供具体的命令和预期的验证步骤，而不要直接声称操作成功。

## 使用场景

- 首次安装 `@aramisfa/openclaw-a2a-outbound` 插件。
- 在 OpenClaw 中启用 `openclaw-a2a-outbound`。
- 配置目标或策略设置。
- 验证插件是否已准备好用于运行时转发。
- 更新或排查现有设置的故障。

## 禁用场景

- 当插件已经安装、启用、配置并经过验证，且任务仅为常规的运行时转发时，请勿使用此技能。

## 需要收集或确认的信息

- 需要配置的目标别名。
- 目标的基础 URL。
- 该目标是否应设置为默认目标。
- 通过 `plugins.entries.openclaw-a2a-outbound.config.policy.allowTargetUrlOverride` 是否允许直接覆盖 URL。

## 检查当前状态

首先运行以下命令：

```bash
openclaw plugins list
openclaw plugins info openclaw-a2a-outbound
openclaw config get plugins.entries.openclaw-a2a-outbound
openclaw config validate
```

只有当 `plugins.entries.openclaw-a2a-outbound.enabled` 和 `plugins.entries.openclaw-a2a-outbound.config.enabled` 都为 `true` 时，才能使用内置的运行时转发功能。

## 安装或更新

- 首次安装：
```bash
openclaw plugins install @aramisfa/openclaw-a2a-outbound --pin
```

- 更新：
```bash
openclaw plugins update openclaw-a2a-outbound
```

然后确保插件条目本身已被启用：

```bash
openclaw plugins enable openclaw-a2a-outbound
```

## 配置插件状态

在向插件配置中写入布尔值或数组时，请使用 `openclaw config set ... --strict-json` 命令。

需要检查的配置路径：

- `plugins.entries.openclaw-a2a-outbound.config.enabled`
- `plugins.entries.openclaw-a2a-outbound.config.targets`
- `plugins.entries.openclaw-a2a-outbound.config.policy.allowTargetUrlOverride`

**示例命令：**

```bash
openclaw config set plugins.entries.openclaw-a2a-outbound.config.enabled --strict-json true
openclaw config set plugins.entries.openclaw-a2a-outbound.config.targets --strict-json '[{"alias":"support","baseUrl":"https://support.example","default":true}]'
openclaw config set plugins.entries.openclaw-a2a-outbound.config.policy.allowTargetUrlOverride --strict-json false
openclaw config validate
```

请将示例中的别名、基础 URL、默认目标选择和 URL 覆盖策略替换为您之前确认的值。

## 激活并验证

通过重启 Gateway 来激活插件：

```bash
openclaw gateway restart
```

重启后，启动一个新的会话并进行验证：

```text
remote_agent { "action": "list_targets" }
```

如果 `list_targets` 命令成功执行且两个启用标志仍然为 `true`，则表示设置完成。

## 任务交接

设置完成后，停止使用此技能进行常规的转发操作。请改用内置的 `remote-agent` 技能和 `remote_agent` 工具。