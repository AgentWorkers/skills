---
name: clawhub
description: 从 ClawHub（公开的 OpenClaw 技能注册库）中安装、搜索、更新和管理技能。当用户需要通过技能的唯一标识符（slug）来安装技能（例如 "clawhub install summarize"）、搜索技能、更新已安装的技能，或以任何方式管理 ClawHub 中的技能时，可以使用该功能。
---
# ClawHub 技能管理器

您可以通过 [ClawHub](https://clawhub.ai) 安装和管理技能。ClawHub 是 OpenClaw 的公共技能注册平台。

## 先决条件

系统路径（PATH）中必须包含 `clawhub` 命令行工具（CLI）。可以使用 `which clawhub` 命令进行验证。如果该工具不存在，请提示用户手动安装：

```bash
npm i -g clawhub
```

请勿在用户未确认的情况下自动安装技能。

## 命令

### 安装技能

```bash
cd ~/.openclaw/workspace && clawhub install <slug>
```

- `<slug>` 是来自 ClawHub 的技能标识符（例如：`summarize`、`weather`、`coding-agent`）
- 安装后的技能会被保存在工作区的 `./skills/` 目录下
- 需要启动一个新的 OpenClaw 会话才能使用该技能

### 搜索技能

```bash
clawhub search "<query>"
```

### 更新技能

```bash
# Update a specific skill
clawhub update <slug>

# Update all installed skills
clawhub update --all
```

### 其他常用命令

```bash
clawhub info <slug>       # Show skill details
clawhub list              # List installed skills
clawhub --help            # Full CLI reference
```

## 工作流程

1. 确保已安装 `clawhub` CLI（使用 `which clawhub` 命令检查，如未安装则进行安装）
2. 切换到工作区目录：`~/.openclaw/workspace`
3. 运行相应的 `clawhub` 命令
4. 告知用户启动一个新的会话（或重新启动 OpenClaw 服务器），以便技能能够生效

## 通过 WhatsApp 安装技能

用户可以通过向 OpenClaw 代理发送消息来安装技能：

```
clawhub install <slug>
```

示例：`clawhub install summarize`

代理会负责处理技能的安装过程，并在技能安装完成后向用户确认。

## 注意事项

- 所有 ClawHub 提供的技能都是公开的
- 对于第三方提供的技能，请谨慎使用——在使用前务必进行审查
- 工作区内的技能（位于 `<workspace>/skills/` 目录下）具有最高的优先级，会优先于系统管理的技能和捆绑提供的技能